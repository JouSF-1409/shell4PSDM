from os.path import join, isfile

import numpy as np
from scipy.interpolate import interp1d

from init import path2PSDM


"""
本段脚本的目的是，导入自定义速度结构模型
根据速度模型的层 和 目标深度 进行换算，导入自定义速度模型，
使用特定方法返回所需信息

逻辑上只接受一次转换波，即 从左往右，依次在更深的层发生转换
"""



def velmod_from_tvel(velFile,modPSDM):
    """
    将tvel 格式的速度模型转换为psdm 格式的速度模型。
    保持二者在速度与 界面分布上的一致。
    """

def velmod_from_normals(velFile,modPSDM):
    """
    将普通格式的速度模型转换为psdm 格式的速度模型
    保持前后在速度与界面分布上的一致
    Parameters
    ----------
    velFile
    modPSDM: psdm 的cwdp 速度模型

    Returns
    -------

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
    read_vel(path2Mod)

