"""
使用工具对ccp profile 进行批量操作。
一些辅助ccp profile select 的工具

设立的一些方法
min_sta2prof(): 计算台站到测线的最短距离（非垂直距离
gen_psdm_list(): 生成一个用于psdm 的
"""
from glob import glob
from os import chdir
from collections import namedtuple
# 测线形状的类
Profile = namedtuple("Profile",
                     "plat1 plon1 plat2 plon2 step")

import numpy as np
from seispy.geo import distaz
from seispy.rf2depth_makedata import _load_mod


def min_sta2prof(stla, stlo, pro:Profile):
    """
    计算台站到测线的最短距离（非垂直距离
    :param stla, stlo: 台站位置
    :param pro: 测线位置
    :return: 最小距离
    """

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
    last = 6370
    for _i in range(lons.shape[0]):
        dist = distaz(stla, stlo, lats[_i], lons[_i]).degreesToKilometers()
        if dist > last:
            return dist
    return dist

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
        dtype = {'names': ('station', 'stla', 'stlo'), 'formats': ('U20', 'f4', 'f4')}
        stas, stlos, stlas  = np.loadtxt(sta_list, dtype=dtype, unpack=True, ndmin=1)
    except:
        raise IOError("需要一个 台站目录\n 格式为\n台站名   stla    stlo")

    try:
        chdir(data_path)
    except:
        raise FileExistsError("检查数据目录")
    lst = open("rfs.lst","w")
    for _i in range(stas.shape[0]):
        if min_sta2prof(stlas[_i], stlos[_i], pro) > min_sit: continue


        # 开始寻找匹配的数据文件
        # 匹配条件是需要重点修改的内容
        nums=0
        rf_lst = []
        for _tr in glob(f"*/*{stas[_i]}*ri"):
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

def trans_ccp_profile(pro:Profile):
    """
    将ccp 剖面 的格式，从首尾+step 转换为中间点+两端距离
    :param pro:
    :return:
    """
    dist = distaz(pro.plat1, pro.plon1, pro.plat2, pro.plat2).degreesToKilometers()/2
    return (pro.plat1+pro.plat2)/2, (pro.plon1+pro.plon2)/2, dist