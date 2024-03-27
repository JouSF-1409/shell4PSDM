"""
这一段代码改写自 张周博士的 GCSRF包，感谢张周博士的工作
"""
from glob import glob
from os.path import join
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
from ccp import Profile
from cfgPSDM import cfg_Hdpmig, cfg_m660q, cfg_Pierce_new_n,cfg_binr_vary_scan_n


def add_right_cax(ax, pad, width):
    '''
    在一个ax右边追加与之等高的cax.
    pad是cax与ax的间距.
    width是cax的宽度.
    '''
    axpos = ax.get_position()
    caxpos = mpl.transforms.Bbox.from_extents(
        axpos.x1 + pad,
        axpos.y0,
        axpos.x1 + pad + width,
        axpos.y1
    )
    cax = ax.figure.add_axes(caxpos)
    return cax
def plot3_comp(path2PSDM:str,
               prof:Profile,
               m660q:cfg_m660q,
               pierc:cfg_Pierce_new_n,
               binr:cfg_binr_vary_scan_n,
               hdp:cfg_Hdpmig):

    # 设置字体参数
    config = {"font.family": 'sans-serif',
              "font.size": 22, "mathtext.fontset": 'stix'}
    rcParams.update(config)
    noutd = 5 # 这个好像是输出转换点的深度，顶格五个，定死就行。
    ## 打开 ccp的三个文件与偏移成像的结果
    # ccp三个文件需要一定的形式推导，所以不是绝对路径
    with open(
        join(path2PSDM,"bin",f"stack_{binr.outpufile}.dat"), 'rb'
    )as _f:
        data = np.fromfile(_f, dtype=np.float32)
        profile = (np.reshape(data, (hdp.nxmod, binr.out_trace_npts)))
    with open(
        join(path2PSDM, "bin", f"{binr.outpufile}_yb.dat"), 'rb'
    ) as _f:
        data_yb = np.fromfile(_f, dtype=np.float32)
        yb_data = (np.reshape(data_yb, (noutd, hdp.nxmod)))
    with open(
        join(path2PSDM, "bin", f"{binr.outpufile}_num.dat"), 'rb'
    ) as _f:
        data_num = np.fromfile(_f, dtype=np.float32)
        num_data = (np.reshape(data_num, (noutd, hdp.nxmod)))
    with open(
        join(path2PSDM, "bin", f"{hdp.migdata}"), 'rb'
    ) as _f:
        data_mig = np.fromfile(_f, dtype=np.float32)
        profile_mig = (np.reshape(data_mig, (hdp.nxmod, hdp.nzmod)))


    Zrange = np.linspace(0, hdp.nzmod * hdp.dz, hdp.nzmod)
    Trange = np.linspace(0, binr.out_trace_npts * binr.out_trace_dt, binr.out_trace_npts)
    # 水平的坐标轴，新的研究中使用了lat 取代了prof length
    #Xrange = np.linspace(0, binr.Profile_len, hdp.nxmod)
    #timelen = (binr.out_trace_npts - 1) * binr.out_trace_dt
    # 选择最长的一边作为横轴
    LonRange = np.linspace(prof.plon1, prof.plon2, hdp.nxmod)

    fig, ax = plt.subplots(3, 1, figsize=(16, 14), sharex=True,
                    gridspec_kw={'height_ratios': [2, 3, 3]})
    im00 = ax[0].plot(LonRange, yb_data[1], 'k', lw=4, label="Half Bin Width(km)")
    ax[0].set_ylabel("Half Bin Width(km)")
    ax_00 = ax[0].twinx()
    ax_00.plot(LonRange, num_data[1, :], 'r', label="RF num")
    ax_00.set_ylabel("RF number")
    ax_00.set_title("Parameters at 100km")
    ax[0].legend(loc=2)
    ax_00.legend(loc=1)
    # 这里修改 CCP的最大值最小值
    im1 = ax[1].pcolor(LonRange, Trange, profile.T,
                        cmap="coolwarm", vmin=-0.1, vmax=0.1)
    cax = add_right_cax(ax[1], pad=0.02, width=0.02)
    cbar = fig.colorbar(im1, cax=cax)
    # 这里设置色标棒 1 的最大值最小值
    im1.set_clim(-0.1, 0.15)
    ax[1].set_ylim([0, 20])
    ax[1].set_ylabel("T(s)")
    ax[1].invert_yaxis()
    ax[1].set_title("CCP stack section")
    # 这里修改 偏移成像的 最大值最小值
    im1 = ax[2].pcolormesh(LonRange, Zrange, profile_mig.T,
                    cmap="jet", vmin=-0.1, vmax=0.1)
    cax = add_right_cax(ax[2], pad=0.02, width=0.02)
    cbar = fig.colorbar(im1, cax=cax)
    # 这里设置色标棒 2 的最大值最小值
    im1.set_clim(-0.1, 0.15)
    ax[2].set_ylim([0, 200])
    ax[2].set_xlabel("Latitute ($\degree$)")
    ax[2].set_ylabel("Depth(km)")
    ax[2].grid()
    #ax[2].plot(stalstdata.stla, stalstdata.moho,color='white', marker='o', linestyle='', ms=5)
    #ax[2].plot(stalstdata.stla, stalstdata.lab, color='white', marker='o', linestyle='', ms=5)
    #ax[2].plot(stalstdata.stla, 5 + np.zeros(len(stalstdata.stla)), color='r', linestyle='', marker='v', ms=10)
    ax[2].invert_yaxis()
    ax[2].set_title(f"Migration Result")
    ax[2].text(0.65, 0.1, f"Mig Freq{hdp.fmin}-{hdp.fmax}Hz",
                fontdict={'size': '24', 'color': 'k'}, transform=ax[2].transAxes)
    plt.savefig(join(path2PSDM,"trans",hdp.migdata+".png"),
                    dpi=300, bbox_inches='tight')