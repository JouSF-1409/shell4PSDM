from os.path import join, isfile
from math import floor

import numpy as np
from scipy.interpolate import interp1d

from util import retryPath, path2PSDM

"""
本段脚本的目的是，导入自定义速度结构模型
根据速度模型的层 和 目标深度 进行换算，导入自定义速度模型，
使用特定方法返回所需信息

逻辑上只接受一次转换波，即 从左往右，依次在更深的层发生转换

isAsciiVelmod(): 简单分析是否为所需的五列速度模型
"""


def velmod_from_tvel(velFile,modPSDM):
    """
    将tvel 格式的模型转换为一般的层状模型，然后转换为PSDM 使用的速度模型格式
    """
    mod_ori = np.loadtxt(velFile,dtype=np.float64,
    # 需要跳过顶部的注释行
                         skiprows=2)
    l = floor(mod_ori.shape[0]/2)
    mod_nor = np.zeros((l, mod_ori.shape[1]))
    for _i in range(l):
        mod_nor[_i:] = mod_ori[2*_i,:]
    np.savetxt(velFile+".vel",
               mod_nor,fmt="%6.5f")
    velmod_from_normals(velFile+".vel",modPSDM)


def velmod_from_normals(velFile,modPSDM):
    """
    将普通格式的速度模型转换为psdm 格式的速度模型
    保持前后在速度与界面分布上的一致
    Parameters
    ----------
    velFile: 普通 文件路径，或者 至少3列的速度模型
        深度    vp    vs
    modPSDM: psdm 的cwdp 速度模型
        vp   vs  rho  层厚  深度  层号
    默认不会有密度， 这里参考seispy 使用
        Brocher (2005) formula.计算 rho，不清楚在 密度在psdm 中的作用
    """

    mod_ori = np.loadtxt(velFile, dtype=np.float64)
    if mod_ori.shape[2]<3:
        raise ValueError("should has at least 3cols")
    mod_PSDM = np.loadtxt(modPSDM, skiprows=1)
    dep_ori = mod_ori[:,0]
    vp = mod_ori[:,1]
    vs = mod_ori[:,2]
    rho = 1.6612*vp - 0.4721*vp**2 + 0.0671*vp**3 - 0.0043*vp**4 + 0.000106*vp**5


    mod_new = np.zeros_like(mod_PSDM)
    mod_new[:,3:] = mod_PSDM[:,3:]
    mod_new[:0] = interp1d(dep_ori,vp,
                           kind='linear')(mod_PSDM[:4])
    mod_new[:1] = interp1d(dep_ori,vs,
                           kind='linear')(mod_PSDM[:4])
    mod_new[:2] = interp1d(dep_ori,rho,
                           kind='linear')(mod_PSDM[:4])

    with open(velFile+'.psdm') as f:
        f.write(f"\t\t\t{mod_new.shape[0]}")
        for _i in range(mod_new.shape[0]):
            # 很丑陋，因为未来可能会需要做格式化输出
            f.write(
                f"{mod_new[_i,0]}\
                \t{mod_new[_i,1]}\
                \t{mod_new[_i,2]}\
                \t{mod_new[_i,4]}\
                \t{mod_new[_i,4]}\
                \t{mod_new[_i,5]}"
            )


def mod_psdm_to_tvel(modPSDM):
    """
    将PSDM 的速度模型转换为正常的速度模型
    """


def genRayPath(rayFile,nLayers,phase='Ps'):
    """
    为转换波生成射线参数文件，只考虑了Ps与Sp 转换波
    这个阶段只需要了解 一共需要速度模型中的多少层即可

    """
    if phase not in ['Ps','Sp']:
        raise ValueError("phase must be Ps or Sp")
    # 这里强制将结果保存到 PSDM 里的m660q目录
    rayFile = join(path2PSDM, "m660q", rayFile)
    if isfile(rayFile):
        print(f"rayp file {rayFile} exists, will be overwritten")

    try:
        rayfile=open(rayFile,'w')
        print(nLayers, file=rayfile)
        # 射线路径索引行，每行都一样。
        ray_index = f"{nLayers:2d} "
        for _i in range(nLayers):
            ray_index += f"2d"
        for _i in range(nLayers):
            ray_flag = '   '
            for _j in range(nLayers, 0, -1):
                if (_j <= _i ^ phase == 'Sp'):
                    ray_flag += ("%2d" % 3)
                else:
                    ray_flag += ("%2d" % 5)

            print(ray_index, file=rayfile)
            # print(str_idx)
            print(ray_flag, file=rayfile)
        rayfile.close()
    except:
        raise IOError(f"file {rayFile} can not be written")


if __name__ == '__main__':
    path2Mod = "G:/src_ongoing/PSDM_wncc-example/model/cwbq"
    #read_vel(path2Mod)


def isAsciiVelmod(url:str, cor=4,funcDir=None):
    """
    路径的有效性需要靠调用者保证
    这里只考虑绝对路径与相对路径的情况

    如果mainfunc不给出，只检查绝对路径。
    同时，速度模型只做数量上的检查，不做物理或数值上的检查。

    PSDM有两种速度模型，一种是五列的，一种是四列的。
    区别在于第五列，即层数列。
    速度模型的形式如下：
    # 层数
    # vp      # vs     # 密度     # 层厚     # 深度  # 第几层
    -----------------------------------------------------------
        82
    3.000     1.800     2.300     1.600       1.6       1
    4.700     2.800     2.600     2.700       4.3       2

    >>> path2PSDM = 'D:\project\chen_rfunc'
    >>> isAsciiVelmod("cwbq",funcDir=join(path2PSDM, "m660q"))
    True
    """

    url = retryPath(url, funcDir)

    try:
        l=open(url, "r")
        lines = l.readlines()
        nline = int(lines[0].strip())+1
        # remove empty lines
        while not lines[-1].strip():
            lines.pop()
        if len(lines) != nline:
            raise IOError(f"file {url} is not a valid velocity model")

        for _i in lines[1:]:
            if len(_i.split()) < cor:
                raise IOError(f"file {url} has no enough columns")

        l.close()
    except:
        raise IOError(f"file {url} is not a valid velocity model")
    return True
