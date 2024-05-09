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
path2PSDM = "/home/jous/Desktop/F/project/pRF/opt/psdm/psdm_major/"
timestap = time.now().strftime("%Y.%m.%d.%H.%M.%S")

# velmod, 速度模型的格式参考velmod.py里的内容，
# 在这里初始化velmod, 但这里我们使用默认的cwbq模型
velmod_path="../model/cwbq"

# 数据位置
prj_dir = "/home/jous/Desktop/F/project/pRF/"
data_dir = "4_decon_clean/"


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

	pierce.name_lst = "datalist.txt"
	# 筛选距离台站300km 范围内的数据进行ccp叠加
	# 生成rfs.lst 文件，用于 psdm 的ccp叠加， 所有的单位都是km, s/km
	# 需要一个sta.lst，格式为 台站名\tstla\tstlo
	# 这里因为原始数据包括了一个datalist.txt，所以不再重复生成
	pierce.name_lst = gen_psdm_list(join(prj_dir,data_dir,"sta.lst"),join(prj_dir, data_dir),200,prof)
	pierce.out_npts = 800
	pierce.rfdata_path = prj_dir
	pierce.name_sub = data_dir
	pierce.center_la = (prof.plat1+prof.plat2)/2
	pierce.center_lo = (prof.plon1+prof.plon2)/2
	pierce.pierc_out = f"pierce_{prof.stamp}.out"
	runner_psdm(path2PSDM,pierce,timestap)
	return pierce

## 第三步 ccp叠加
def runner_ccp_stack(prof:Profile,
                     m660q:cfg_m660q,
                     pierce:cfg_Pierce_new_n):

	binr = cfg_binr_vary_scan_n()
	## 设置剖面， 起点，长度，方位角
	binr = set_prof_ori(prof,binr)
	binr.UTM_zone = get_UTM(prof)

	# 数据类型设置
	binr.out_trace_npts = 800

	# 叠加窗设置
	binr.bins_step = prof.step

	# 叠加设置,归一化和动校正在这里标注
	#binr.moveout_flag = 0
	## 输入输出文件
	# m660q的输出文件
	binr.timefile = m660q.m660q_out
	# pierc 的输出文件
	binr.pierc_out = pierce.pierc_out
	# ccp的输出文件
	# 这里不能使用相对路径，因为
	# 这里不能使用相对路径或者绝对路径，因为结果 会在bin 文件夹下面以stack_{outputfile}.dat 为名称 输出不定数目的文件，具体数目视 cfg文件所定义。
	binr.outpufile = f"ccp_stack_{prof.stamp}"

	runner_psdm(path2PSDM,binr,timestap)
	return binr

## 第四步 Hidpim.x 偏移成像
# 这里改动比较少，多尝试一翻
def runner_hdp(prof:Profile,
               binr:cfg_binr_vary_scan_n):
	hdp = cfg_Hdpmig()
	## 输入输出文件
	# ccp叠加的输出结果
	hdp.tx_data = f"stack_{binr.outpufile}.dat"
	## 剖面
	hdp.nxmod = int(binr.Profile_len/binr.bins_step)+1
	hdp.ntrace = hdp.nxmod
	hdp.dt = binr.out_trace_dt
	hdp.dx = binr.bins_step
	hdp.nt = binr.out_trace_npts

	hdp.ifreqindl = 0
	hdp.ifreqindr = 30
	hdp.nxleft = 2
	hdp.nxright = 2
	hdp.fmax = 0.5
	# 偏移叠加结果
	hdp.migdata = f"mig_{prof.pname}_bp_c_{hdp.fmin}_{hdp.fmax}_Dl_{hdp.ifreqindl}_Dr_{hdp.ifreqindr}.dat"

	runner_psdm(path2PSDM, hdp,prof.stamp)
	return hdp
def compare():
    #m660q 只跑一遍
	m660q=runner_m660q()
	from plot_with_ccp import plot3_comp
	for name, info in preparelist.items():
	# 记录每个剖面的名称，程序运行的时间
#		try:
		if name == 'ff' or name == 'gg':
			timestap = f"{name}_{time.now().strftime('%Y.%m.%d.%H.%M.%S')}"
            # 设置剖面特征，Ybin有点复杂，这里不处理。
            # 如果想要修改，使用全局变量进行介入
			prof = Profile(
                name,
                # lat1， lon1， lat2，  lon2， slide_val
                float(info[5]),
                float(info[6]),
                float(info[7]),
                float(info[8]),
                float(info[4]),
            )
			pierc = runner_pierce(prof)
			stack = runner_ccp_stack(prof, m660q, pierc)
			hdp = runner_hdp(prof, stack)
            # 进行绘图
			plot3_comp(path2PSDM, prof, m660q, pierc, stack, hdp)
#		except:
			#continue

def myProf():
    # 这段是自己的剖面
	from profList import myList
	# m660q 只跑一遍
	m660q = runner_m660q()
	from plot_with_ccp import plot3_comp

	timestap = f"default_{time.now().strftime('%Y.%m.%d.%H.%M.%S')}"
	# 设置剖面特征，Ybin有点复杂，这里不处理。
	# 如果想要修改，使用全局变量进行介入
	for name, info in myList.items():
		# 记录每个剖面的名称，程序运行的时间
		#try:
		if name[:2] == 'DB':
			timestap = f"{name}_{time.now().strftime('%Y.%m.%d.%H.%M.%S')}"
			# 设置剖面特征，Ybin有点复杂，这里不处理。
            # 如果想要修改，使用全局变量进行介入
			prof = Profile(
				name,
				# lat1， lon1， lat2，  lon2， slide_val
				float(info[1]),
				float(info[0]),
				float(info[3]),
				float(info[2]),
				float(info[4]),
				timestap
			)
			pierc = runner_pierce(prof)
			stack = runner_ccp_stack(prof, m660q, pierc)
			hdp = runner_hdp(prof, stack)
            # 进行绘图
			plot3_comp(path2PSDM, prof, m660q, pierc, stack, hdp)
		#except:
		#	continue
if __name__ == "__main__":
	myProf()

