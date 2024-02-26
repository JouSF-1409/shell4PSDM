
from m660q import m660q
import os
### 所有的配置类，都按PSDM 公开的方法进行配置
### 这里推荐的方法是将参数配置为字典，在 runMethod.py 中 modi 前import 参数
# 然后交给 modi 方法做运行。
### 这个文件的存在意义是，给出一些配置的示例。后人可以根据这些文件的示例，
# 初始化，并做简单修改。 用注释形成必要的笔记。
# 使用字典的一个好处是，可以最小化改动，突出每次改动的内容。
# 同时字典能兼容 json， cfg 等多种配置语言

# 这里给出张周的 S波配置示例
###############################################################
ZhangZhou_S_wave_m660= {
   "ref_model" : 'CDmod',
    "Ps_ray" : "mray_joe.Sp.dat",
    "iflat":0,
    "itype": -1
}

# Parameters I concerned about
# build mray_joe.Ps.dat and mray_joe.Sp.dat
LayerCount = 51
ZhangZhou_S_wave_pierc= {
    "pierc_out" : "../pierc_use.dat",
    "center_la" : 27.5,
    "center_lo" : 104,
    "out_npts" : 1251,
    "sac_user_num_rayp" : 0,
    "ref_model" : "../data/CDmod",
    "event_filt_flag" : 1,
    "event_filt_min" : 70.0,
    "event_filt_max" : 80.0,
    "rfdata_path" : "../data/",
    "num_sub":1,
    "name_sub": "sub_name",
    "name_lst": "datalist.txt"
}

ZhangZhou_S_wave_binr = {
    "Descar_la_begin" : -500.,
    "Descar_lo_begin" : 0,
    "Descar_la_end": -500,
    "Descar_lo_end": 0,
    "Descar_step" :100,
    "Profile_len" : 1000.,
    "az_min" : 90.,
    "az_max" :90.,
    "az_step" :10.,
    "bins_step" :2.,
    "trace_num_min":2,
    "ratio_trace":1,
    "UTM_zone":50,
    "timefile":"mray_joe.Sp.dat",
    "outputfile": '2022_binr_out_Qseis_1s.dat',
    "out_trace_npts" : 1001,
    "out_trace_dt" : 0.1,
    "nw_pair" :

}

ZhangZhou_S_wave_Hdpmig = {
   "method_flag" : 0,
   "refvel_flag" : 0,
   "vscale" : 1.0,
   "freq_min" : 0.03
   "freq_max" : 0.5
   "freq_idx_b" : 0
   "freq_idx_e" : 40
   "nxmod" : 21
   "nzmod" : 1600
   "nx" : 1024
   "nz" : 1600
   "dx" : 50
   "dz" : 0.5
   "ntrace" : 21
   "nt" : 1001
   "dt" : 0.1
   "nt0" : 2048
   "nt_step" : 1
   "FD_ang" : 45
   "smoothpt_left" : 4
   "smoothpt_right" : 4
   "mod_format_flag" : 0
   "mig_model" : "../model/CDmod"
   "stacked_field" : "../stack/stack_"+binr_out_name+".dat"
   "hdpmig_out_field" = sub_name+"_" + str(freq_min)+"_"+str(freq_max)+"_hdpmig.joe.dat"
}

ZhangZhou_S_wave_Plot = {
   "xlenp" : 1000
   "npt" : 1001
   "dt" : 0.1
   "depth" : 800  
   "dz" : 0.5  
   "prolen" : 1000  
   "dx" : 50  
   "noutd" : 5
   "yb_file" : PSDM_pro_path+"/stack/"+binr_out_name+"_yb.dat"
   "num_file" : PSDM_pro_path+"/stack/"+binr_out_name+"_num.dat"
}

##################################################################################################
trace_num_min = 2
ratio_trace = 1.0
UTM_zone = 48
out_trace_npts = 1001
out_trace_dt = 0.1
temp_folder = '../temp'
moveout_flag = 0
moveout_gcarc = 0
norm_flag = 1
stack_flag = 1
npief = 1
out_idx_flag = 0
binr_out_name = '2022_binr_out_Qseis_1s'
# [binr_vary_scan_n Parameters Part End]

##################################################################################################
# [Hdpmig.x Parameters Part Begin]
method_flag = 0
refvel_flag = 0
vscale = 1.0
freq_min = 0.03
freq_max = 0.5
freq_idx_b = 0
freq_idx_e = 40
nxmod = 21
nzmod = 1600
nx = 1024
nz = 1600
dx = 50
dz = 0.5
ntrace = 21
nt = 1001
dt = 0.1
nt0 = 2048
nt_step = 1
FD_ang = 45
smoothpt_left = 4
smoothpt_right = 4
mod_format_flag = 0
mig_model = "../model/CDmod"
stacked_field = "../stack/stack_"+binr_out_name+".dat"
hdpmig_out_field = sub_name+"_" + \
    str(freq_min)+"_"+str(freq_max)+"_hdpmig.joe.dat"

##################################################################################################
# [Plot]
cwdfd = os.getcwd()
PSDM_pro_path = cwdfd+"/psdm/PSDM_qseis2022_IASP/"

# plot Observation System
sta_xy_file = PSDM_pro_path+"/stack/station.dat"
pierce_xy_file1 = PSDM_pro_path+"/stack/depth1.dat"
pierce_xy_file2 = PSDM_pro_path+"/stack/depth2.dat"
pierce_xy_file3 = PSDM_pro_path+"/stack/depth3.dat"
pierce_xy_file4 = PSDM_pro_path+"/stack/depth4.dat"
pierce_xy_file5 = PSDM_pro_path+"/stack/depth5.dat"
pro_xy_file = PSDM_pro_path+"/stack/"+binr_out_name+"_profile.txt"

# plot CCP
xlenp = 1000
npt = 1001
dt = 0.1
depth = 800  
dz = 0.5  # depth interval, km per grid along Z
prolen = 1000  # profile length
dx = 50  # trace interval, km per grid along X
nz = int(depth/dz)  # depth number
nx = int(prolen/dx)+1  # trace number
Yrange = np.linspace(0, nz*dz, nz)
Trange = np.linspace(0, npt*dt, npt)
Xrange = np.linspace(0, xlenp, int(xlenp/dx)+1)
noutd = 5
numbin = int(xlenp/dx+1)
timelen = (npt-1)*dt
stacked_field = PSDM_pro_path+"/stack/stack_"+binr_out_name+".dat"
yb_file = PSDM_pro_path+"/stack/"+binr_out_name+"_yb.dat"
num_file = PSDM_pro_path+"/stack/"+binr_out_name+"_num.dat"
LatRange = pro_xy.lat