# CCP PLOT PART
##################################################################################################
# Plot CCP stacking section with bin size and RF numbers at chosen depth
# Inputs (parameters set in binr_vary_scan_n.inp): F:\GCSRF_test\Section003\psdm\PSDM_qseis2022_IASP\stack
# 1. outfile    -   output file name, no prefix and postfix
#                   e.g. stack_*.dat, *_yb.dat, *_num.dat
# 2. xlenp      -   profile length (km)
# 3. npt        -   output number of time samples in each trace
# 4. dx         -   the spacing between bins along the profile (km)
# 5. dt         -   time interval (s)
# 6. noutd      -   output number in ninw （ the indexes of reference ray among 1 -- nw: ninw, (inw0(i),i=1,ninw) ）

import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib as mpl
import os
import numpy as np
import pandas as pd

### 定制化图件 #####################################################################################
# 通过更新 rcParams，你可以定制化图形的各个方面，如字体、线型、颜色等
config = {"font.family": 'sans-serif',
          "font.size": 22, "mathtext.fontset": 'stix'}
rcParams.update(config)
# 在给定的Axes对象右侧添加一个与其等高的colorbar（cax）
def add_right_cax(ax, pad, width):
    '''
    在一个ax右边追加与之等高的cax.
    pad是cax与ax的间距.
    width是cax的宽度.    '''
    axpos = ax.get_position() # 获取ax的位置信息
    # 计算cax的位置
    caxpos = mpl.transforms.Bbox.from_extents(
        axpos.x1 + pad,
        axpos.y0,
        axpos.x1 + pad + width,
        axpos.y1
    )
    cax = ax.figure.add_axes(caxpos) # 在figure上添加一个新的Axes对象，位置由caxpos确定
    return cax
##################################################################################################

### 输入参数设置 #################################################################################
xlenp = 1000  ### profile length (km)
npt = 1001 ### time samples
dt = 0.1 ### time interval (s)
depth = 800  # imaging depth (km)
dz = 0.5  # depth interval, km per grid along Z
prolen = xlenp  # profile length
dx = 50  # trace interval, km per grid along X
nz = int(depth/dz)  # depth number
nx = int(prolen/dx)+1  # trace number
###### CCP叠加坐标范围 ##########
Yrange = np.linspace(0, nz*dz, nz) # 深度域
Trange = np.linspace(0, npt*dt, npt) # 时间域
Xrange = np.linspace(0, xlenp, int(xlenp/dx)+1) # 测线范围
###################################
# 叠加窗的设计，随着深度的增大菲涅尔带增大，可以灵活设计bin的半宽
# * output number and depth indexes in ninw: noutd,(ioutd(i),i=1,noutd)', file=binr_conf
# '5 6 13 16 19 36      40-, 100-, 150-, 210-, 300-km', file=binr_conf
noutd = 5 
###################################
numbin = int(xlenp/dx+1) ### bin number
timelen = (npt-1)*dt ### time length

###### CCP叠加相关文件 ###########
cwdfd = os.getcwd() # current work directory
PSDM_pro_path = cwdfd+"/psdm/PSDM_qseis2022_IASP/"
binr_out_name = '2022_binr_out_Qseis_1s'
###########################################################################################
stacked_field = PSDM_pro_path+"/stack/stack_"+binr_out_name+".dat"  # CCP stack file
###########################################################################################
yb_file = PSDM_pro_path+"/stack/"+binr_out_name+"_yb.dat"  # Half Bin Width
num_file = PSDM_pro_path+"/stack/"+binr_out_name+"_num.dat" # RF number
pro_xy_file = PSDM_pro_path+"/stack/"+binr_out_name+"_profile.txt" # profile file
pro_xy = pd.read_csv(pro_xy_file, sep='\s+', header=None,
                     names=["lon", "lat", "decx", "decy", "offset"])
LatRange = pro_xy.lat # 测线纬度范围

###########################################################################################################
### 读取CCP叠加画图所需文件
# CCP stack section
with open(stacked_field, 'rb') as f:
    for k in range(1):
        data = np.fromfile(f, dtype=np.float32)
        profile = (np.reshape(data, (numbin, npt)))
# Half Bin Width
with open(yb_file, 'rb') as f_yb:
    for k_yb in range(1):
        data_yb = np.fromfile(f_yb, dtype=np.float32)
        yb_data = (np.reshape(data_yb, (noutd, numbin)))
# RF number
with open(num_file, 'rb') as f_num:
    for k_yb in range(1):
        data_num = np.fromfile(f_num, dtype=np.float32)
        num_data = (np.reshape(data_num, (noutd, numbin)))
# PSDM stack section
method = "Qseis"
vol_data = "Mig"
stalst_file = cwdfd+"/psdm/PSDM_qseis2022_IASP/SP.lat.lon.lst"  # station list
stalstdata = pd.read_csv(stalst_file, delim_whitespace=True, header=None, names=[
                         'stnm', 'stlo', 'stla', 'stel', 'moho', 'lab'])
sub_name = "QseisMig"
freq_min = 0.03
freq_max = 0.5
##################################################################
hdpmig_out_field = sub_name+"_" + \
    str(freq_min)+"_"+str(freq_max)+"_hdpmig.joe.dat"
filename = PSDM_pro_path+"/poststack/"+hdpmig_out_field # PSDM stack file
##################################################################
with open(filename, 'rb') as f:
    for k in range(1):
        data_mig = np.fromfile(f, dtype=np.float32)
        profile_mig = (np.reshape(data_mig, (nx, nz)))
##############################################################################################

### plot
fig, ax = plt.subplots(3, 1, figsize=(16, 14), sharex=True,
                       gridspec_kw={'height_ratios': [2, 3, 3]})
###############################################################
###### subplot1: 接收函数叠加数量
im00 = ax[0].plot(LatRange, yb_data[1], 'k', lw=4, label="Half Bin Width(km)")
ax[0].set_ylabel("Half Bin Width(km)")
ax_00 = ax[0].twinx()
ax_00.plot(LatRange, num_data[1, :], 'r', label="RF num")
ax_00.set_ylabel("RF number")
ax_00.set_title("Parameters at 100km")
ax[0].legend(loc=2)
ax_00.legend(loc=1)
###############################################################
###### subplot2: 时间域 CCP 叠加
im1 = ax[1].pcolor(LatRange, Trange, profile.T,
                   cmap="coolwarm", vmin=-0.6, vmax=0.6)
cax = add_right_cax(ax[1], pad=0.02, width=0.02)
cbar = fig.colorbar(im1, cax=cax)
im1.set_clim(-0.5, 0.5)
ax[1].set_ylim([0, 30])
ax[1].set_ylabel("T(s)")
ax[1].invert_yaxis()
ax[1].set_title("CCP stack section")
#####################################################################
####### subplot3: PSDM 叠加
im1 = ax[2].pcolormesh(LatRange, Yrange, profile_mig.T,
                       cmap="jet", vmin=-0.6, vmax=0.6)
cax = add_right_cax(ax[2], pad=0.02, width=0.02)
cbar = fig.colorbar(im1, cax=cax)
im1.set_clim(-0.45, 0.55)
ax[2].set_ylim([0, 250])
ax[2].set_xlabel("Latitute ($\degree$)")
ax[2].set_ylabel("Depth(km)")
ax[2].grid()
ax[2].plot(stalstdata.stla, stalstdata.moho,
           color='white', marker='o', linestyle='', ms=5)
ax[2].plot(stalstdata.stla, stalstdata.lab,
           color='white', marker='o', linestyle='', ms=5)
ax[2].plot(stalstdata.stla, 5+np.zeros(len(stalstdata.stla)),
           color='r', linestyle='', marker='v', ms=10)
ax[2].invert_yaxis()
ax[2].set_title(method+"_"+str(vol_data))
ax[2].text(0.65, 0.1, (method+"_"+str(vol_data)+" Freq "+str(freq_min)+"-" +
           str(freq_max)+"Hz"), fontdict={'size': '24', 'color': 'k'}, transform=ax[2].transAxes)
# plt.tight_layout() # 调整子图间距
plt.savefig(cwdfd+"/figs/"+"CCP_PSDM.jpg", dpi=300, bbox_inches='tight')
