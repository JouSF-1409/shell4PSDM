"""
目的是跑通 王旭博士给的示例数据，
包含了shell4PSDM 的最小逻辑，包括传递几个配置文件中重复的部分
"""

from os.path import join
from datetime import datetime as time
from ccp import Profile, set_prof, get_UTM, set_prof_ori, gen_psdm_list
from util import runner_psdm

from cfgPSDM import cfg_binr_vary_scan_n,cfg_Hdpmig,cfg_m660q,cfg_Pierce_new_n

# 在这里配置psdm_major 的路径
path2PSDM = "/home/jousk/project/psdm_major/"
timestap = time.now().strftime("%Y.%m.%d.%H.%M.%S")

# velmod, 速度模型的格式参考velmod.py里的内容，
# 在这里初始化velmod, 但这里我们使用默认的cwbq模型
velmod_path="../model/cwbq"

# 数据位置
prj_dir = "/home/jousk/project/data/"
data_dir = "f2p5_dt01_s1"


## 第一步，生成射线参数文件
## 需要文件：
# 1. 配置文件: m660q.in
# 2. 射线路径文件，因为将所有模型插值成cwbq 的形状，所以不用变
# 3. 参考速度模型
# 4. nmo.dat 文件，格式为 层数
#                       gcarc,rayp(s/deg)

# cirl+ 左键 点击，查看每个参数的含意
def runner_m660q():
	m660q = cfg_m660q()
	m660q.m660q_out =  f"m660.Pcs.out"
	runner_psdm(path2PSDM, m660q)
	return m660q

## 第二步， 射线路径计算
#  需要速度模型文件， 设置的参数文件，
def runner_pierce(prof:Profile):
	from ccp import gen_psdm_list
	pierce = cfg_Pierce_new_n()
	pierce.parser(prof)

	pierce.name_lst = "datalist.txt"
	# 筛选距离台站300km 范围内的数据进行ccp叠加
	# 生成rfs.lst 文件，用于 psdm 的ccp叠加， 所有的单位都是km, s/km
	# 需要一个sta.lst，格式为 台站名\tstla\tstlo
	# 这里因为原始数据包括了一个datalist.txt，所以不再重复生成
	#pierce.name_lst = gen_psdm_list(join(prj_dir,data_dir,"sta.lst"),join(prj_dir, data_dir),300,prof)
	pierce.out_npts = 800
	pierce.rfdata_path = prj_dir
	pierce.name_sub = data_dir
	pierce.pierc_out = f"pierce_{timestap}.out"
	runner_psdm(path2PSDM,pierce,timestap)
	return pierce

## 第三步 ccp叠加
def runner_ccp_stack(prof:Profile,
                     m660q:cfg_m660q,
                     pierce:cfg_Pierce_new_n):
	# 初始化配置文件，继承上一步的参数
	# 并计算剖面相关的参数
	binr = cfg_binr_vary_scan_n()
	binr.paser(m660q,pierce,prof)

	# 数据类型设置
	binr.out_trace_npts = 800
	# ccp的输出文件
	# 这里不能使用相对路径，因为
	# 这里不能使用相对路径或者绝对路径，因为结果 会在bin 文件夹下面以stack_{outputfile}.dat 为名称 输出不定数目的文件，具体数目视 cfg文件所定义。
	binr.outpufile = f"ccp_stack_{timestap}"

	runner_psdm(path2PSDM,binr,timestap)
	return binr

## 第四步 Hidpim.x 偏移成像
# 这里改动比较少，多尝试一翻
def runner_hdp(prof:Profile,
               binr:cfg_binr_vary_scan_n):
	hdp = cfg_Hdpmig()
	hdp.paser(binr)
	## 输入输出文件
	# ccp叠加的输出结果
	hdp.tx_data = f"stack_{binr.outpufile}.dat"
	# 偏移叠加结果
	hdp.migdata = f"mig_{timestap}.dat"
	runner_psdm(path2PSDM, hdp,timestap)
	return hdp

if __name__ == "__main__":
    #m660q 只跑一遍
	m660q=runner_m660q()
	from plot_like_zhang import plot3_comp
	timestap = f"default_{time.now().strftime('%Y.%m.%d.%H.%M.%S')}"
	# 设置剖面特征，Ybin有点复杂，这里不处理。
	# 如果想要修改，使用全局变量进行介入
	prof = Profile("default",
		# lat1， lon1， lat2，  lon2， slide_val
			39.2, 106,
			40,   115,
			2)
	pierc=runner_pierce(prof)
	stack=runner_ccp_stack(prof,m660q,pierc)
	hdp=runner_hdp(prof,stack)
	# 进行绘图
	plot3_comp(path2PSDM, prof,m660q,pierc,stack,hdp)

