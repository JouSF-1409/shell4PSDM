"""
使用工具对ccp profile 进行批量操作。
一些辅助ccp profile select 的工具

设立的一些方法
min_sta2prof(): 计算台站到测线的最短距离（非垂直距离
gen_psdm_list(): 生成一个用于psdm 的
"""
from glob import glob
from os import chdir
from math import floor
from collections import namedtuple
from datetime import datetime as time
# 测线形状的类
Profile = namedtuple("Profile",
                     "pname plat1 plon1 plat2 plon2 step stamp")

import numpy as np

from cfgPSDM import cfg_binr_vary_scan_n

def initProf(name, pos):
    if len(pos) == 5:
        timestap=f"{name}_{time.now().strftime('%Y.%m.%d.%H.%M.%S')}"
        return Profile(
            name,
            # lat1， lon1， lat2，  lon2， slide_val
            float(pos[1]), float(pos[0]), float(pos[3]),float(pos[2]),
            2,
            timestap,
        )
    else:
        raise ValueError(f"try another init function to init prof")
def get_UTM(Prof:Profile):
    """
    >>> get_UTM(Profile("a", 32.5, 115.6,32.5,115.6,2))
    >>> 49
    """
    return floor(
        (360. + Prof.plon1 + Prof.plon2)/12
    )

def set_prof(Prof:Profile, cfg_binr:cfg_binr_vary_scan_n):
    from geographiclib.geodesic import Geodesic
    distaz = Geodesic.WGS84

    cfg_binr.Descar_la_begin = distaz.Inverse(Prof.plat1, Prof.plon2, Prof.plat2, Prof.plon2)['s12']/2000
    cfg_binr.Descar_lo_begin = distaz.Inverse(Prof.plat1, Prof.plon1, Prof.plat1, Prof.plon2)['s12']/2000

    dist = distaz.Inverse(Prof.plat1, Prof.plon1,
                  Prof.plat2, Prof.plon2)
    az = dist['azi1']
    if az < 0:
        az += 360
    if az < 180:
        cfg_binr.Descar_lo_begin *= -1
    if az < 90 or az > 270:
        cfg_binr.Descar_la_begin *= -1
    cfg_binr.Descar_la_end = cfg_binr.Descar_la_begin
    cfg_binr.Descar_lo_end = cfg_binr.Descar_lo_begin
    cfg_binr.Profile_len = dist['s12']/1000
    cfg_binr.az_min = az
    cfg_binr.az_max = az
    return cfg_binr

def set_prof_ori(Prof:Profile, cfg_binr:cfg_binr_vary_scan_n):
    from distaz import distaz
    cfg_binr.Descar_la_begin = distaz(Prof.plat1, Prof.plon2, Prof.plat2, Prof.plon2).degreesToKilometers()/2
    cfg_binr.Descar_lo_begin = distaz(Prof.plat1, Prof.plon1, Prof.plat1, Prof.plon2).degreesToKilometers()/2

    dist = distaz(Prof.plat1, Prof.plon1,
                  Prof.plat2, Prof.plon2)
    if dist.baz < 180:
        cfg_binr.Descar_lo_begin *= -1
    if dist.baz < 90 or dist.baz > 270:
        cfg_binr.Descar_la_begin *= -1
    cfg_binr.Descar_la_end = cfg_binr.Descar_la_begin
    cfg_binr.Descar_lo_end = cfg_binr.Descar_lo_begin
    cfg_binr.Profile_len = dist.degreesToKilometers()
    cfg_binr.az_min = dist.baz
    cfg_binr.az_max = dist.baz
    return cfg_binr

def min_sta2prof(stla, stlo, pro:Profile):
    """
    计算台站到测线的最短距离（非垂直距离
    :param stla, stlo: 台站位置
    :param pro: 测线位置
    :return: 最小距离
    """
    #print(f"stla:{stla}, stlo:{stlo}, pro:{pro}")
    from geographiclib.geodesic import Geodesic
    distaz = Geodesic.WGS84
    space = distaz.Inverse(
        pro.plat1, pro.plon1,
        pro.plat2, pro.plon2
    )['s12']/1000/pro.step
    lats = np.linspace(
        pro.plat1, pro.plat2, int(space)
    )
    lons = np.linspace(
        pro.plon1, pro.plon2, int(space)
    )
    dist = [distaz.Inverse(stla,stlo,lats[_i],lons[_i])['s12']/1000 for _i in range(len(lats))]
    return min(dist)

def min_sta2prof_ori(stla, stlo, pro:Profile):
    from distaz import distaz
    space = distaz(
        pro.plat1, pro.plon1,
        pro.plat2, pro.plon2
    ).degreesToKilometers()/pro.step
    lats = np.linspace(
        pro.plat1, pro.plat2, int(space)
    )
    lons = np.linspace(
        pro.plon1, pro.plon2, int(space)
    )
    dist = [distaz(stla,stlo,lats[_i],lons[_i]).degreesToKilometers() for _i in range(len(lats))]
    return min(dist)

def gen_psdm_list(sta_list:str,
                  data_path:str,
                  min_sit:float,
                  pro:Profile):
    """
    生成一个 用于psdm 的file list,
    搜索的逻辑需要用户进行自定义
    :param sta_list: 台站目录
    :param min_sit: 距离剖面的最大距离，按转换点计算，一般不超过300km(~3°)为宜
    :param data_path:接收函数的数据目录
    :param pro: 使用的ccp 剖面
    :return: 在目录下面，生成一个名为sta.lst 的文件，按照psdm 的目标格式进行计算
    """
    try:
        dtype = {'names': ('station', 'stlo', 'stla'), 'formats': ('U20', 'f4', 'f4')}
        stas, stlos, stlas  = np.loadtxt(sta_list, dtype=dtype, unpack=True, ndmin=1)
    except:
        raise IOError("需要一个 台站目录\n 格式为\n台站名   stlo    stla")

    try:
        chdir(data_path)
    except:
        raise FileExistsError("检查数据目录")
    lst = open("rfs.lst","w")
    for _i in range(stas.shape[0]):
        if min_sta2prof_ori(stlas[_i], stlos[_i], pro) > min_sit: continue


        # 开始寻找匹配的数据文件
        # 匹配条件是需要重点修改的内容
        nums=0
        rf_lst = []
        for _tr in glob(f"{stas[_i]}/*{stas[_i]}*ri"):
            _tr = _tr.split('/')[1]
            nums +=1
            rf_lst.append(_tr)
        if nums ==0:
            continue
        lst.write(f"{stas[_i]}\n")
        lst.write(f"{nums}\n")
        lst.write("\n".join(rf_lst)+"\n\n")

    lst.write("\n\n\n\n\n\n")
    lst.close()
    return "rfs.lst"

def trans_ccp_profile(pro:Profile):
    """
    将ccp 剖面 的格式，从首尾+step 转换为中间点+两端距离
    :param pro:
    :return:
    """
    dist = distaz.Inverse(pro.plat1, pro.plon1, pro.plat2, pro.plat2)['s12']/1000/2
    return (pro.plat1+pro.plat2)/2, (pro.plon1+pro.plon2)/2, dist

if __name__ == "__main__":
    import doctest
    doctest.testmod()
