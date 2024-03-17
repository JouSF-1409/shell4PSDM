"""
现在这里是为了 帮助我个人 做psdm 的成像实验
一些需要的文件是通过
单位为km， s/km

需要自主添加nmo.dat
"""
from os.path import join
from datetime import datetime as time
from ccp import Profile
from util import runner_psdm



npy_ccp = ""
preparelist={
    # Concordant structural variations from the surface to the base of the upper mantle in
    #   depth_dat  bin_rad domperiod  width  slide_val    lat1      lon1     lat2      lon2
    'aa':(npy_ccp, '100',    '1',   '150',   '20',    '35.7',    '116.8',   '35.8',   '120.3'),
    'bb':(npy_ccp, '100',    '1',   '150',   '20',    '38.4',    '117.5',   '43.9',   '119.5'),
    'cc':(npy_ccp, '100',    '1',   '150',   '20',    '36.3',    '114.6',   '43.3',   '120.4'),
    'dd':(npy_ccp, '100',    '1',   '150',   '20',    '42.2',    '114.0',   '38.4',   '121.3'),
    'ee':(npy_ccp, '100',    '1',   '150',   '20',    '42.3',    '112.3',   '36.1',   '120.0'),
    'ff':(npy_ccp, '100',    '1',   '150',   '20',    '40.4',    '108.2',   '40.4',   '120.8'),
    'gg':(npy_ccp, '100',    '1',   '150',   '20',    '39.2',    '108.8',   '35.2',   '120.8'),
    # Lithospheric structure beneath the central and western North China Craton and adjacent regions from S-receiver function imaging
    'E1':(npy_ccp, '100',    '1',   '150',   '20',    '32.5',    '115.6',   '27.3',   '121.0'),
    'E2':(npy_ccp, '100',    '1',   '150',   '20',    '34.9',    '116.3',   '34.9',   '119.0'),
    'E3':(npy_ccp, '100',    '1',   '150',   '20',    '37.5',    '118.1',   '42.5',   '119.4'),
    'E4':(npy_ccp, '100',    '1',   '150',   '20',    '35.0',    '114.2',   '42.5',   '120.6'),
    'E5':(npy_ccp, '100',    '1',   '150',   '20',    '38.1',    '120.0',   '41.7',   '113.7'),
    'E6':(npy_ccp, '100',    '1',   '150',   '20',    '40.0',    '111.7',   '35.0',   '118.8'),
    'E7':(npy_ccp, '100',    '1',   '150',   '20',    '40.0',    '107.5',   '40.0',   '121.0'),
    'E8':(npy_ccp, '100',    '1',   '150',   '20',    '34.4',    '118.8',   '38.8',   '107.5'),
    'W1':(npy_ccp, '100',    '1',   '150',   '20',    '37.5',    '102.8',   '31.9',   '114.4'),
    'W2':(npy_ccp, '100',    '1',   '150',   '20',    '33.8',    '105.0',   '30.0',   '111.9'),
    'W3':(npy_ccp, '100',    '1',   '150',   '20',    '35.5',    '105.0',   '35.0',   '115.0'),
    'W4':(npy_ccp, '100',    '1',   '150',   '20',    '31.3',    '110.0',   '38.8',   '109.4'),
    'W5':(npy_ccp, '100',    '1',   '150',   '20',    '38.3',    '106.7',   '31.3',   '105.0'),
    'W6':(npy_ccp, '100',    '1',   '150',   '20',    '41.3',    '111.3',   '29.4',   '111.3'),
    'W7':(npy_ccp, '100',    '1',   '150',   '20',    '36.7',    '115.0',   '30.0',   '110.0'),
    'W8':(npy_ccp, '100',    '1',   '150',   '20',    '33.8',    '116.3',   '35.8',   '107.5'),
    # Intralithospheric mantle structures recorded continental subduction
    'NC1':(npy_ccp, '100',    '1',   '150',   '20',    '36.0',    '119.5',   '36.5',   '116.5'),
    'NC3':(npy_ccp, '100',    '1',   '150',   '20',    '40.0',    '118.2',   '44.0',   '118.0'),
    'NC4':(npy_ccp, '100',    '1',   '150',   '20',    '40.0',    '112.5',   '39.5',   '107.0'),
    'NC5':(npy_ccp, '100',    '1',   '150',   '20',    '36.0',    '114.0',   '36.0',   '108.5'),
    'NC6':(npy_ccp, '100',    '1',   '150',   '20',    '40.0',    '124.0',   '45.0',   '116.0'),
    'NC7':(npy_ccp, '100',    '1',   '150',   '20',    '32.0',    '108.0',   '42.0',   '112.0'),

}

### 全局变量区
# 设置psdm 相关的路径
path2PSDM="/home/jous/Desktop/F/project/ChinArray3-PRF/psdm/psdm_major/"
psdm_bin = join(path2PSDM, "bin")
psdm_default_cfg = join(path2PSDM, "model")
psdm_cfg_history = join(path2PSDM, "history")
psdm_trans = join(path2PSDM, "trans")

# velmod, 速度模型的格式参考velmod.py里的内容，
# 在这里初始化velmod, 但这里我们使用默认的cwbq模型
velmod_path=join(path2PSDM,"model","cwbq")

# 数据位置
prj_dir = "/home/jous/Desktop/F/project/ChinArray3-PRF/"
data_dir = join(prj_dir,"4_decon_clean")


## 第一步，生成射线参数文件
## 需要文件：
# 1. 配置文件: m660q.in
# 2. 射线路径文件，因为将所有模型插值成cwbq 的形状，所以不用变
# 3. 参考速度模型
# 4. nmo.dat 文件，格式为 层数
#                       gcarc,rayp(s/deg)

# cirl+ 左键 点击，查看每个参数的含意

from cfgPSDM import cfg_m660q
m660q = cfg_m660q()
m660q.m660q_out = join(psdm_trans, f"m660.Pcs.{time.now().strftime('%Y.%m.%d')}.out")
runner_psdm(path2PSDM,m660q)

## 第二步， 射线路径计算
#  需要速度模型文件， 设置的参数文件，
from cfgPSDM import cfg_Pierce_new_n
from ccp import gen_psdm_list
pierce = cfg_Pierce_new_n()
# 剖面的经纬度，步长
prof = Profile(
    40.4, 108.2,
    40.4, 120.8, 1
)
# 生成rfs.lst 文件，用于 psdm 的ccp叠加， 所有的单位都是km, s/km
#gen_psdm_list(join(data_dir,"sta.lst"),data_dir,300,prof)
pierce.out_npts = 1024
pierce.rfdata_path = prj_dir
pierce.name_sub = "4_decon_clean"
pierce.name_lst = "rfs.lst"
pierce.center_la = (prof.plat1+prof.plat2)/2
pierce.center_lo = (prof.plon1+prof.plon2)/2
pierce.pierc_out = join(psdm_trans,
                        f"pierce_{time.now().strftime('%Y.%m.%d')}.out")
runner_psdm(path2PSDM,pierce)

## 第三步 ccp叠加
from cfgPSDM import cfg_binr_vary_scan_n
from seispy.geo import distaz
binr = cfg_binr_vary_scan_n()
## 设置剖面， 起点，长度，方位角
binr.Descar_la_begin = prof.plat1
binr.Descar_la_end = prof.plat1
binr.Descar_lo_begin = prof.plon1
binr.Descar_lo_end = prof.plon1
dist = distaz(prof.plat1, prof.plon1,
                          prof.plat2, prof.plon2)
binr.Profile_len = dist.degreesToKilometers()
binr.az_min = dist.baz
binr.az_max = dist.baz

# 数据类型设置
binr.out_trace_npts = 900

# 叠加窗设置
binr.bins_step = 10

# 叠加设置,归一化和动校正在这里标注

## 输入输出文件
# m660q的输出文件
binr.timefile = m660q.m660q_out
# pierc 的输出文件
binr.binr_out_name = pierce.pierc_out
# ccp的输出文件
binr.outpufile = join(psdm_trans,
                          # 文件名
                          f"ccp_stack_{time.now().strftime('%Y.%m.%d')}.dat")


runner_psdm(path2PSDM,binr)
