from os.path import isfile,join, exists

from init import path2PSDM
from cfgPSDM import cfg_m660q
from util import isAsciiVelmod,retryPath

from obspy.core import UTCDateTime

def genRayPath(rayFile,nLayers,phase='Ps'):
    """
    生成射线参数文件
    考虑到逻辑的复杂性，这里强制将结果保存到 PSDM 里的m660q目录
    并且会强制覆盖同名文件，注意备份
    Phase只能为 Ps 或 Sp， 使用了异或
    这里的行数依然不确定怎么对应。看得头晕眼花的
    """
    if phase not in ['Ps','Sp']:
        raise ValueError("phase must be Ps or Sp")
    rayFile = join(path2PSDM, "m660q", rayFile)
    if isfile(rayFile):
        print(f"rayp file {rayFile} exists, will be overwritten")

    try:
        rayfile=open(rayFile,'w')

        print(nLayers, file=rayfile)
        for cc_n in range(0, nLayers):
            str_idx = ("%2d " % nLayers)
            str_flg = '   '
            for ii in range(nLayers, 0, -1):
                str_idx += ("%2d" % ii)
                if (ii <= cc_n ^ phase == 'Sp'):
                    str_flg += ("%2d" % 3)
                else:
                    str_flg += ("%2d" % 5)
            print(str_idx, file=rayfile)
            # print(str_idx)
            print(str_flg, file=rayfile)
        rayfile.close()
    except:
        raise IOError(f"file {rayFile} can not be written")

class m660q(cfg_m660q):


    def __str__(self):
        return \
f"* velocity model file\n\
{self.ref_model}\n\
* ray file\n\
{self.ray}\n\
* output file\n\
{self.m660q_out}\n\
* iflat, itype (= 0: free-surface refl.; else: conversion (>0: Ps; <0: Sp))\n\
{self.iflat:01d}     {self.itype:01d}\n\
\n\
"
    def gen(self):
        if not exists(self.ref_model):
            raise FileNotFoundError(f"ref_model file {self.ref_model} not found")


if __name__ == "__main__":
    import doctest
    doctest.testmod()