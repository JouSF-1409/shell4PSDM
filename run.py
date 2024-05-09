from os.path import join
from datetime import datetime as time

from ccp import Profile, initProf,set_prof, get_UTM, set_prof_ori, gen_psdm_list
from util import runner_psdm

from cfgPSDM import cfg_binr_vary_scan_n, cfg_Hdpmig, cfg_m660q, cfg_Pierce_new_n

# path2PSDM="/home/project/ChinArray3-PRF/psdm/psdm_major"
path2PSDM = "/home/jous/Desktop/F/project/sRF/opt/psdm/psdm_major_srf"
timestap = time.now().strftime("%Y.%m.%d.%H.%M.%S")

# velmod, 速度模型的格式参考velmod.py里的内容，
# 在这里初始化velmod, 但这里我们使用默认的cwbq模型
velmod_path = "cwbq"

# 数据位置
# prj_dir = "/home/project/ChinArray3-PRF/"
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
    runner_psdm(path2PSDM, m660q)
    return m660q


## 第二步， 射线路径计算
#  需要速度模型文件， 设置的参数文件，
def runner_pierce(prof: Profile):
    from ccp import gen_psdm_list

    pierce = cfg_Pierce_new_n()
    pierce.parser(prof)

    # pierce.name_lst = "datalist.txt"
    # 筛选距离台站300km 范围内的数据进行ccp叠加
    # 生成rfs.lst 文件，用于 psdm 的ccp叠加， 所有的单位都是km, s/km
    # 需要一个sta.lst，格式为 台站名\tstla\tstlo
    # 这里因为原始数据包括了一个datalist.txt，所以不再重复生成
    pierce.name_lst = gen_psdm_list(
        join(prj_dir, data_dir, "sta.lst"), join(prj_dir, data_dir), 300, prof
    )
    # pierce.name_lst = "rfs.lst"
    pierce.out_npts = 800
    pierce.rfdata_path = prj_dir
    pierce.name_sub = data_dir
    pierce.pierc_out = f"pierce_{prof.stamp}.out"
    runner_psdm(path2PSDM, pierce, prof.stamp)
    return pierce


## 第三步 ccp叠加
def runner_ccp_stack(prof: Profile, m660q: cfg_m660q, pierce: cfg_Pierce_new_n):
    binr = cfg_binr_vary_scan_n()
    binr.paser(m660q, pierce, prof)

    # ccp的输出文件
    # 这里不能使用相对路径，因为
    # 这里不能使用相对路径或者绝对路径，因为结果 会在bin 文件夹下面以stack_{outputfile}.dat 为名称
    binr.outpufile = f"ccp_stack_{prof.stamp}"

    runner_psdm(path2PSDM, binr, prof.stamp)
    return binr


## 第四步 Hidpim.x 偏移成像
# 这里改动比较少，多尝试一翻
def runner_hdp_exam(prof: Profile, binr: cfg_binr_vary_scan_n):
    hdp = cfg_Hdpmig()
    hdp.paser(binr)

    fmins = (0.01, 0.03, 0.05)
    fmaxs = (0.4, 0.5, 0.7, 0.9, 1)
    ifreql = (5, 10, 20, 40)
    ifreqr = (5, 10, 20, 40)

    for fmin in fmins:
        for fmax in fmaxs:
            for ql in ifreql:
                for qr in ifreqr:
                    try:
                        hdp.fmin = fmin
                        hdp.fmax = fmax
                        hdp.ifreqindl = ql
                        hdp.ifreqindr = qr

                        hdp.tx_data = f"stack_{binr.outpufile}.dat"
                        # 偏移叠加结果
                        hdp.migdata = f"mig_{prof.pname}_bp_c_{fmin}_{fmax}_Dl_{ql}_Dr_{qr}.dat"
                        runner_psdm(path2PSDM, hdp, timestap)
                    except:
                        continue
                    yield hdp


    # hdp.fmin = 0.1
    hdp.fmax = 0.5
    # hdp.ifreqindl = 20
    # hdp.ifreqindr = 40

    hdp.nxleft = 40
    hdp.nxright = 40

    ## 输入输出文件
    # ccp叠加的输出结果
    return hdp
def runner_hdp(prof: Profile, binr: cfg_binr_vary_scan_n):
    hdp = cfg_Hdpmig()
    hdp.paser(binr)


    hdp.fmin = 0.01
    hdp.fmax = 1
    hdp.ifreqindl = 10
    hdp.ifreqindr = 5

   # hdp.nxleft = 40
   # hdp.nxright = 40
    hdp.tx_data = f"stack_{binr.outpufile}.dat"
    # 偏移叠加结果
    hdp.migdata = f"mig_{prof.pname}_bp_c_{hdp.fmin}_{hdp.fmax}_Dl_{hdp.ifreqindl}_Dr_{hdp.ifreqindr}.dat"
    runner_psdm(path2PSDM, hdp, timestap)

    ## 输入输出文件
    # ccp叠加的输出结果
    return hdp


def compare():
    # 这段是比较与前人的工作
    from profList import preparelist

    # m660q 只跑一遍
    m660q = runner_m660q()
    from plot_with_ccp import plot3_comp

    # from plot_like_zhang import plot3_comp

    timestap = f"default_{time.now().strftime('%Y.%m.%d.%H.%M.%S')}"
    # 设置剖面特征，Ybin有点复杂，这里不处理。
    # 如果想要修改，使用全局变量进行介入
    for name, info in preparelist.items():
        # 记录每个剖面的名称，程序运行的时间
        try:
            # if name == 'ff' or name == 'gg':
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
                timestap,
            )
            pierc = runner_pierce(prof)
            stack = runner_ccp_stack(prof, m660q, pierc)
            hdp = runner_hdp(prof, stack)
            # 进行绘图
            plot3_comp(path2PSDM, prof, m660q, pierc, stack, hdp)
        except:
            continue


def myProf():
    # 这段是自己的剖面
    from profList import myList

    # m660q 只跑一遍
    m660q = runner_m660q()
    from plot_with_ccp import plot3_comp

    # timestap = f"default_{time.now().strftime('%Y.%m.%d.%H.%M.%S')}"
    # 设置剖面特征，Ybin有点复杂，这里不处理。
    # 如果想要修改，使用全局变量进行介入
    for name, info in myList.items():
        #if name == "OD1":
        #    continue
        # 记录每个剖面的名称，程序运行的时间
        # print(f"now we at profile {name}")
        #try:
            timestap = f"{name}_{time.now().strftime('%Y.%m.%d.%H.%M.%S')}"
            # 设置剖面特征，Ybin有点复杂，这里不处理。
            # 如果想要修改，使用全局变量进行介入
            prof = initProf(name,info)
            pierc = runner_pierce(prof)
            stack = runner_ccp_stack(prof, m660q, pierc)
            hdp = runner_hdp(prof, stack)
            plot3_comp(path2PSDM, prof, m660q, pierc, stack, hdp)
            # hdp = runner_hdp(prof, stack)
            # 进行绘图
        #except:
        #    continue
def export_grd():
    # m660q 只跑一遍

    m660q = runner_m660q()
    from export_with_ccp import save2GRD
    from profList import myList
    # timestap = f"default_{time.now().strftime('%Y.%m.%d.%H.%M.%S')}"
    # 设置剖面特征，Ybin有点复杂，这里不处理。
    # 如果想要修改，使用全局变量进行介入
    for name, info in myList.items():
        if name[:2] == "DB":
        #    continue
        # 记录每个剖面的名称，程序运行的时间
        # print(f"now we at profile {name}")
        #try:

            # 设置剖面特征，Ybin有点复杂，这里不处理。
            # 如果想要修改，使用全局变量进行介入
            prof = initProf(name,info)
            pierc = runner_pierce(prof)
            stack = runner_ccp_stack(prof, m660q, pierc)
            hdp = runner_hdp(prof, stack)
            # 这一步将数据导出为grd文件
            grd=save2GRD(path2PSDM,prof,stack,hdp)
            grd.default_paser()

if __name__ == "__main__":
    myProf()
