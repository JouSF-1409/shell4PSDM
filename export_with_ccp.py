"""
最后还是得写个类，真的麻烦。。。。。
需要实现的功能：
1. export_wiggle： 将 NMO步骤的内容输出层wiggle 所需的格式
2. export_count: 将层上统计到的数据输出到plot 所需的格式
3. export_psdm： 将psdm 的结果转换为netcdf4格式
"""

from os.path import join

import numpy as np
from netCDF4 import Dataset

from ccp import Profile
from cfgPSDM import cfg_binr_vary_scan_n,cfg_Hdpmig

class save2GRD():
    """
    用于导出grd格式的一个类
    需要一个类，export_psdm，共享一些变量，比如
    path2PSDM，
    siteRange, ccpRange，depthRange， 横纵的坐标
        siteRange, ccpRange 分别是经纬度的坐标和 和 水平距离的坐标
    需要几个共通的参数文件，主要是binr，和hdp的东西
    仔细想象，还需要topo文件的处理，哎，全是麻烦事
    """
    def __init__(self,path2PSDM:str,
                 prof:Profile,
                 cfg_binr:cfg_binr_vary_scan_n, cfg_hdp:cfg_Hdpmig):
        """
        初始化一些变量
        """
        self.path2PSDM=path2PSDM
        self.prof = prof
        self.cfg_binr = cfg_binr
        self.cfg_hdp = cfg_hdp
        # 换算坐标
        if np.abs(prof.plon1 - prof.plon2) < np.abs(prof.plat1 - prof.plat2):
            self.siteRange = np.linspace(
                prof.plat1, prof.plat2, cfg_hdp.nxmod)
        else:
            self.siteRange = np.linspace(
                prof.plon1, prof.plon2, cfg_hdp.nxmod)
        self.depthRange = np.linspace(
            -1*cfg_hdp.nzmod * cfg_hdp.dz,0, cfg_hdp.nzmod
        )
    def default_paser(self):
        # 在这里选择要运行哪几步
        self.export_topo()
        self.trans_ccp()
        self.export_wiggle()
        self.export_psdm()
        self.export_plot_cfg()
    def limit_parser(self):
        self.export_wiggle()
        self.export_psdm()
        self.export_limit_plot_cfg()
    def export_topo(self):
        """
        初始化topo 文件
        """
        self.max_topo=0
        self.min_topo=0
        _j=open(join(self.path2PSDM, "ccp", f"{self.prof.pname}.topo"),"r")
        topo=join(self.path2PSDM, "trans", f"{self.prof.pname}.topo")
        _k=open(topo,"w")
        for _l in _j.readlines():
            words = _l.split()
            if len(words) !=4:
                continue
            if np.abs(self.prof.plon1 - self.prof.plon2) < np.abs(self.prof.plat1 - self.prof.plat2):
                if float(words[3])<self.min_topo:
                    self.min_topo=float(words[3])
                if float(words[3])>self.max_topo:
                    self.max_topo=float(words[3])
                _k.write(f"{words[1]}\t{words[3]}\n")
            else:
                if float(words[3])<self.min_topo:
                    self.min_topo=float(words[3])
                if float(words[3])>self.max_topo:
                    self.max_topo=float(words[3])
                _k.write(f"{words[0]}\t{words[3]}\n")
        _j.close()
        _k.close()
        self.topo=topo
        return topo
    def export_wiggle(self, desample:int = 3):
        """
        将binr 的结果导出成文本文件交给gmt wiggle工具
        并且输出一个叠加数量文件
        """
        if desample>=self.cfg_hdp.nxmod/3:
            raise ValueError('desample must be less than nxmod/3')
        # 读取两个文件
        binr = join(self.path2PSDM, "bin", f"stack_{self.cfg_binr.outpufile}.dat")
        binr_count = join(self.path2PSDM, "bin", f"{self.cfg_binr.outpufile}_num.dat")
        Trange=np.linspace(
            0, self.cfg_binr.out_trace_npts * self.cfg_binr.out_trace_dt, self.cfg_binr.out_trace_npts
        )
        # 将数据读入并转换为必要的格式，
        # binr 输出的数据按行表示，每一行表示一个
        with open(binr_count, "rb") as _f:
            # 这里选第二行表示150km，第一行表示100km
            binr_count=np.fromfile(_f, dtype=np.float32) \
                         .reshape((5, self.cfg_hdp.nxmod))[2, :]
        with open(binr, "rb") as _f:
            binr=np.fromfile(_f, dtype=np.float32)\
                    .reshape((self.cfg_hdp.nxmod,self.cfg_binr.out_trace_npts))
        # 这里调整输出路径与输出样式
        path2binr_count = join(self.path2PSDM, "trans",
                               f"{self.prof.pname}.150km.binr_count")
        path2wiggle = join(self.path2PSDM, "trans",
                          f"{self.prof.pname}.wiggle")
        # 输出坐标与数据，写的很丑
        with open(path2wiggle, "w") as _f:
            #
            for _i in range(desample, self.cfg_hdp.nxmod, desample):
                _f.write(">\n")
                for _time,_amp in zip(Trange, binr[_i, :]):
                    _f.write(f"{self.siteRange[_i]}\t-{_time}\t{_amp}\n")
        with open(path2binr_count, "w") as _f:
            for _site, _num in zip(self.siteRange, binr_count):
                _f.write(f"{_site}\t{_num}\n")
        self.count = path2binr_count
        self.max_bin=np.max(binr_count)
        self.min_bin=np.min(binr_count)
        self.wiggle=path2wiggle
        return path2wiggle
    def export_psdm(self):
        """
        将psdm 结果输出为netcdf4格式
        """
        mig = join(self.path2PSDM, "bin", f"{self.cfg_hdp.migdata}")
        path2psdm_path = join(self.path2PSDM, "ccp", f"{self.prof.pname}.psdm")
        grd_psdm = Dataset(path2psdm_path, "w", format="NETCDF4")
        # 读取数据，并转换格式，所有数据按行存储
        with open (mig, "rb") as _f:
            mig = np.fromfile(_f, dtype=np.float32)\
                        .reshape((self.cfg_hdp.nxmod, self.cfg_hdp.nzmod))
        # ccp.grd 有三个变量，x,y,z
        # x表示横向变量，y表示纵向，即深度，
        # z.shape = (y.shape,x.shape)

        grd_psdm.createDimension("x",self.cfg_hdp.nxmod)
        grd_psdm.createDimension("y",self.cfg_hdp.nzmod)
        x = grd_psdm.createVariable('x', 'f8',('x',))
        y = grd_psdm.createVariable('y', 'f8',('y',))
        data = grd_psdm.createVariable('data', 'f8', ('y', 'x'))
        x[:] = self.siteRange
        y[:] = np.linspace(-1*self.cfg_hdp.nzmod * self.cfg_hdp.dz, 0, self.cfg_hdp.nzmod)[::-1]
        data[:,:] = mig.T

        grd_psdm.close()

        self.psdm=path2psdm_path

        return path2psdm_path

    def trans_ccp(self):
        # 这里将数据转储了，但是
        # ccp.grd 有三个变量，x,y,z
        # x表示横向变量，y表示纵向，即深度，
        # z.shape = (y.shape,x.shape)

        path2ccp=join(self.path2PSDM,"ccp",
                               f"ccp.{self.prof.pname}.grd")
        ccp_ori = Dataset(path2ccp)
        path2ccp=join(self.path2PSDM,"trans",
                               f"{self.prof.pname}.ccp")
        ccp_new = Dataset(path2ccp,"w")
        ccp_new.createDimension("x",
                                ccp_ori["x"][:].data.shape[0])
        ccp_new.createDimension("y",
                                ccp_ori["y"][:].data.shape[0])
        x = ccp_new.createVariable('x', 'f8',('x',))
        y = ccp_new.createVariable('y', 'f8',('y',))
        # 注意这里的(y,x)
        data = ccp_new.createVariable('data', 'f8', ('y', 'x'))
        if np.abs(self.prof.plon1 - self.prof.plon2) < np.abs(self.prof.plat1 - self.prof.plat2):
            x[:]=np.linspace(self.prof.plat1, self.prof.plat2, ccp_ori["x"][:].data.shape[0])
        else:
            x[:]=np.linspace(self.prof.plon1, self.prof.plon2, ccp_ori["x"][:].data.shape[0])
        y[:] = ccp_ori["y"][:].data
        data[:,:] = ccp_ori["z"][:].data
        ccp_new.close()

        self.ccp = path2ccp
        return path2ccp
    def export_plot_cfg(self):
        """
        配置绘图文件所需的参数
        """
        if np.abs(self.prof.plon1 - self.prof.plon2) < np.abs(self.prof.plat1 - self.prof.plat2):
            R=f"{self.prof.plat1}/{self.prof.plat2}"
            t="latitude"
        else:
            self.siteRange=np.linspace(
                self.prof.plon1, self.prof.plon2, self.cfg_hdp.nxmod)

            R = f"{self.prof.plon1}/{self.prof.plon2}"
            t="longitude"
        with open(join(self.path2PSDM,"trans",f"{self.prof.pname}.cfg"),"w") as _f:
            _f.write(
f"prof={self.prof.pname}\ntopo={self.topo}\ncount={self.count}\n\
binr={self.wiggle}\nccp={self.ccp}\npsdm={self.psdm}\n\n\
topoR=-R{R}/{self.min_topo-(self.max_topo-self.min_topo)*0.07}/{self.max_topo+(self.max_topo-self.min_topo)*0.07}\n\
topoB='-Bya1000f500+lelevation -Bxf1g1 -BWSt'\n\
countR='-R{R}/{self.min_bin-(self.max_bin-self.min_bin)*0.07}/{self.max_bin+(self.max_bin-self.min_bin)*0.07}'\n\
countB='-Bya350f200 -BE'\n\
binrR=-R{R}/-30/0\n\
binrB='-Bya10f5g5+ltime(s) -Bxf1g1 -BSWrt'\n\
ccpR='-R{R}/-300/0'\n\
ccpB='-Bya50f50g50+lDepth(km) -Bxf1g4'\n\
psdmR=$ccpR\n\
psdmB='-Bya50f50g50+lDepth(km) -Bxf1g1+l{t}(@[\degree@[)'\n\
cpt_ccp=ccp.cpt\n\
cpt_psdm=ccp.cpt"
        )

    def export_limit_plot_cfg(self):
        if np.abs(self.prof.plon1 - self.prof.plon2) < np.abs(self.prof.plat1 - self.prof.plat2):
            R=f"{self.prof.plat1}/{self.prof.plat2}"
            t="latitude"
        else:
            self.siteRange=np.linspace(
                self.prof.plon1, self.prof.plon2, self.cfg_hdp.nxmod)

            R=f"{self.prof.plon1}/{self.prof.plon2}"
            t="longitude"
        with open(join(self.path2PSDM, "trans", f"{self.prof.pname}.cfg"), "w") as _f:
            _f.write(
f"prof={self.prof.pname}\ntopo={self.topo}\ncount={self.count}\n\
binr={self.wiggle}\nccp={self.ccp}\npsdm={self.psdm}\n\n\
topoR=NULL\n\
topoB=NULL\n\
countR='-R{R}/{self.min_bin - (self.max_bin - self.min_bin) * 0.07}/{self.max_bin + (self.max_bin - self.min_bin) * 0.07}'\n\
countB='-Bya350f200 -BE'\n\
binrR=-R{R}/-30/0\n\
binrB='-Bya10f5g5+ltime(s) -Bxf1g1 -BSWrt'\n\
ccpR=NULL\n\
ccpB=NULL\n\
psdmR=$ccpR\n\
psdmB='-Bya50f50g50+lDepth(km) -Bxf1g1+l{t}(@[\degree@[)'\n\
cpt_ccp=NULL\n\
cpt_psdm=ccp.cpt"
            )
