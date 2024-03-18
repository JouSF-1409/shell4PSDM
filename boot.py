"""
现在这里是为了 帮助我个人 做psdm 的成像实验
一些需要的文件是通过
单位为km， s/km

需要自主添加nmo.dat
"""
from os.path import join
from math import floor
from datetime import datetime as time
from ccp import Profile
from util import runner_psdm



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
binr.moveout_flag = 0
## 输入输出文件
# m660q的输出文件
binr.timefile = m660q.m660q_out
# pierc 的输出文件
binr.binr_out_name = pierce.pierc_out
# ccp的输出文件
# 这里不能使用相对路径或者绝对路径，因为结果 会在bin 文件夹下面以stack_{outputfile}.dat 为名称
binr.outpufile = f"ccp_stack_{time.now().strftime('%Y.%m.%d')}"

runner_psdm(path2PSDM,binr)

## 第四步 Hidpim.x 偏移成像
# 这里改动比较少，多尝试一翻

from cfgPSDM import cfg_Hdpmig
hdp = cfg_Hdpmig()
## 输入输出文件
# ccp叠加的输出结果
hdp.tx_data = f"stack_{binr.outpufile}.dat"
# 偏移叠加结果
hdp.migdata = f"../trans/mig_{time.now().strftime('%Y.%m.%d')}.dat"
## 剖面
hdp.nxmod = int(binr.Profile_len/binr.bins_step)+1
hdp.ntrace = hdp.nxmod
hdp.dx = binr.bins_step
hdp.nt = binr.out_trace_npts
runner_psdm(path2PSDM, hdp)