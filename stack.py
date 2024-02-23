"""
包含了两类函数的调用，
1. pierc_new_n
2. binr_vary_scan_n
"""
from glob import glob
from os import listdir
from subprocess import Popen, PIPE
from os.path import isdir,join, isfile
from pathlib import Path
from math import floor

from init import path2PSDM
from cfgPSDM import cfg_Pierce_new_n, cfg_binr_vary_scan_n
from util import _str_pierce_new_n, _str_binr_vary_scan_n,get_datalist, isAsciiVelmod, retryPath,matchLayerDepth




class pierc_new_n(cfg_Pierce_new_n):

    def check(self):
        isAsciiVelmod(self.ref_model,funcDir=join(path2PSDM,"stack"))
        cmd = join(path2PSDM, "stack", "pierc_new_n")
        if not isfile(cmd):
            raise FileNotFoundError("make pierc_new_n first")
        # 检查datalist 文件( 未测试过PSDM 是否支持多个项目一起使用
        for _i in range(self.num_sub):
            proj_dir = join(self.rfdata_path,self.name_sub.split()[_i])
            if not isdir(proj_dir):
                proj_dir = join(path2PSDM, proj_dir)
                if not isdir(proj_dir):
                    raise FileNotFoundError(f"subdir {proj_dir} not found")
        if not isfile(join(proj_dir, self.name_lst)):
            print(f"file {self.name_lst} not found, will be generated")
            get_datalist(proj_dir)

    def run(self):
        # 写入配置文件
        l = open(join(path2PSDM, "stack", "pierc_new_n.in"), "w")
        l.write(self.__str__())
        l.close()
        cmd = join(path2PSDM, "stack", "pierc_new_n")
        # 调用抄自张周，未经测试
        proc0 = Popen(
                cmd,
                stdin=None,
                stdout=PIPE,
                stderr=PIPE,
                shell=True)
        outinfo02, errinfo02 = proc0.communicate()

    @property
    def ndw(self):
        return self._ndw

    @property.setter
    def ndw(self, value:list):
        """
        使用list 保存5个深度值，然后根据速度模型转换到index。然后再转化为需要的str
        """
        if len(value) != 5:
            raise ValueError("ndw must contains 5 depths")
        #使用默认的降序排列
        value.sort()
        for _i in value:
            if _i < 0:
                raise ValueError("ndw must be positive")
        
        path = isAsciiVelmod(self.ref_model)
        indexDepth = matchLayerDepth(path, value)

        self._ndw = '   '.join(indexDepth)+\
                    "\t\t\t"+\
                    '-,'.join(value)+"km"

    # 输入文件中选定的深度数目(NW)，
    # 索引与对应深度(NWI(I), DEP(I), I=1,NW)。  
    # ray number, ray indexes, corresponding depth indexes
    # 射线数量，射线索引，对应深度索引   
    @property
    def nw(self):
        return self._nw
    @property.setter
    def nw(self, value):
        # 未完成，没看懂
        if value not in [1, 2, 3, 4, 5]:
            raise ValueError("nw must be 1, 2, 3, 4 or 5")
        self._nw = value


    def __str__(self):
        return \
_str_pierce_new_n(self)

class binr_vary_scan_n(cfg_binr_vary_scan_n):
    
    def check(self):
        # 好像只能检查timefile 的路径
        cmd = join(path2PSDM,"stack")
        retryPath(self.timefile, cmd)
    
    @property
    def ninw(self):
        return self._ninw
    @property.setter
    def ninw(self, value:list, velmod:str):
        ### 虽然inp文件没有要求 提供velmod，但为了实现深度与坐标之间的对应，还是需要一个velmod
        if(len(value) != 5):
            print("best to provide 5 depths")
        value.sort()
        velmod=retryPath(velmod,funcDir=join(path2PSDM,"stack"))
        match=matchLayerDepth(velmod, value)
        self._ninw="    .join(match)+\n"+\
                    "\t\t\t\t"+\
                    "-,".join(value)+"km\n"

    def run(self):
        cmd = join(path2PSDM, "stack", "binr_vary_scan_n")
        l = open(join(path2PSDM, "stack", "binr_vary_scan_n.inp"), "w");l.write(self.__str__());l.close()
        proc0 = Popen(
            cmd,
            stdin=None,
            stdout=PIPE,
            stderr=PIPE,
            shell=True)
        outinfo02, errinfo02 = proc0.communicate()


    def getProfile(self):
        """
        从配置中生成profile 信息
        """
        nPara=1; nRot=1;
        if self.Descar_la_begin !=self.Descar_la_end \
            and self.Descar_lo_begin != self.Descar_lo_end:
            nPara = 1
        if self.az_min != self.az_max:
            nRot = floor((self.az_max -self.az_min)/self.az_step)+1
        return nPara, nRot


    def __str__(self):
        return \
_str_binr_vary_scan_n(self)

    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    get_datalist("D:/project/chen_rfunc/data/f2p5_dt01_s1")
    #print(pierc_new_n())