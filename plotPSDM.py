import os


import numpy as np
import pandas as pd
import matplotlib as mpl
from matplotlib import rcParams
import matplotlib.pyplot as plt


cwdfd = os.getcwd()
PSDM_pro_path = cwdfd+"/psdm/PSDM_qseis2022_IASP/"
def plotObserve():
    # Observation System PLOT PART
    ##################################################################################################
    config = {"font.family": 'sans-serif',
              "font.size": 16, "mathtext.fontset": 'stix'}
    rcParams.update(config)
    sta_xy_file = PSDM_pro_path+"/stack/station.dat"
    pierce_xy_file1 = PSDM_pro_path+"/stack/depth1.dat"
    pierce_xy_file2 = PSDM_pro_path+"/stack/depth2.dat"

    pierce_xy_file3 = PSDM_pro_path+"/stack/depth3.dat"
    pierce_xy_file4 = PSDM_pro_path+"/stack/depth4.dat"
    pierce_xy_file5 = PSDM_pro_path+"/stack/depth5.dat"
    pro_xy_file = PSDM_pro_path+"/stack/"+binr_out_name+"_profile.txt"
    sta_xy = pd.read_csv(sta_xy_file, sep='\s+', header=None,
                         names=["lat", "lon", "decy", "decx"])
    pierce_xy1 = pd.read_csv(pierce_xy_file1, sep='\s+',
                             header=None, names=["lat", "lon", "decy", "decx"])
    pierce_xy2 = pd.read_csv(pierce_xy_file2, sep='\s+',
                             header=None, names=["lat", "lon", "decy", "decx"])
    pierce_xy3 = pd.read_csv(pierce_xy_file3, sep='\s+',
                             header=None, names=["lat", "lon", "decy", "decx"])
    pierce_xy4 = pd.read_csv(pierce_xy_file4, sep='\s+',
                             header=None, names=["lat", "lon", "decy", "decx"])
    pierce_xy5 = pd.read_csv(pierce_xy_file5, sep='\s+',
                             header=None, names=["lat", "lon", "decy", "decx"])
    pro_xy = pd.read_csv(pro_xy_file, sep='\s+', header=None,
                         names=["lon", "lat", "decx", "decy", "offset"])
    # CD_xy=pd.read_csv("/home/georom1996/PracticeJoe/PyPSDM/SW_China_Vs_model/sw.lst",sep='\s+',header=None,names=["lon","lat"])
    plt.figure(figsize=(20, 8))
    # plt.set_title("Observation System View")
    # plt.scatter(pierce_xy.lon,pierce_xy.lat)
    # plt.plot(pro_xy.lon,pro_xy.lat)
    plt.subplot(121)
    # plt.scatter(pierce_xy3.decx,pierce_xy3.decy,color='gray',marker='.')
    plt.scatter(pierce_xy2.decx, pierce_xy2.decy, color='green', marker='.')
    plt.scatter(pierce_xy1.decx, pierce_xy1.decy, color='red', marker='.')

    # plt.scatter(pierce_xy4.decx,pierce_xy4.decy,color='brown',marker='+')
    # plt.scatter(pierce_xy5.decx,pierce_xy5.decy,color='cyan',marker='+')
    plt.scatter(sta_xy.decx, sta_xy.decy, color='k', marker='^',)
    # plt.scatter(CD_xy.lon,CD_xy.lat,color='blue',marker='^')
    plt.plot(pro_xy.decx, pro_xy.decy, 'blue', linewidth=3)

    # plt.axis('equal')
    plt.subplot(122)

    # plt.scatter(pierce_xy3.lon,pierce_xy3.lat,color='gray',marker='.')
    plt.scatter(pierce_xy2.lon, pierce_xy2.lat, color='green', marker='.')
    plt.scatter(pierce_xy1.lon, pierce_xy1.lat, color='red', marker='.')
    # plt.scatter(pierce_xy4.lon,pierce_xy4.lat,color='brown',marker='+')
    # plt.scatter(pierce_xy5.lon,pierce_xy5.lat,color='cyan',marker='+')
    plt.scatter(sta_xy.lon, sta_xy.lat, color='k', marker='^')
    # plt.scatter(CD_xy.lon,CD_xy.lat,color='blue',marker='^')
    plt.plot(pro_xy.lon, pro_xy.lat, 'blue', linewidth=3)
    plt.savefig(cwdfd+"/figs/"+"example002_IASP_Station_Map.jpg",
                dpi=300, bbox_inches='tight')
    # plt.axis('equal')

def plotCCP():
    # CCP PLOT PART
    ##################################################################################################
    # Plot CCP stacking section with bin size and RF numbers at chosen depth
    # Inputs (parameters set in binr_vary_scan_n.inp):
    # 1. outfile    -   output file name, no prefix and postfix
    #                   e.g. stack_*.dat, *_yb.dat, *_num.dat
    # 2. xlenp      -   profile length (km)
    # 3. npt        -   output number of time samples in each trace
    # 4. dx         -   the spacing between bins along the profile (km)
    # 5. dt         -   time interval (s)
    # 6. noutd      -   output number in ninw
    config = {"font.family": 'sans-serif',
              "font.size": 22, "mathtext.fontset": 'stix'}
    rcParams.update(config)


    def add_right_cax(ax, pad, width):
        '''
        在一个ax右边追加与之等高的cax.
        pad是cax与ax的间距.
        width是cax的宽度.    '''
        axpos = ax.get_position()
        caxpos = mpl.transforms.Bbox.from_extents(
            axpos.x1 + pad,
            axpos.y0,
            axpos.x1 + pad + width,
            axpos.y1
        )
        cax = ax.figure.add_axes(caxpos)
        return cax


    ##################################################################################################
    xlenp = 1000
    npt = 1001
    dt = 0.1
    depth = 800  # imaging depth (km)
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
    with open(stacked_field, 'rb') as f:
        for k in range(1):
            data = np.fromfile(f, dtype=np.float32)
            profile = (np.reshape(data, (numbin, npt)))
    with open(yb_file, 'rb') as f_yb:
        for k_yb in range(1):
            data_yb = np.fromfile(f_yb, dtype=np.float32)
            yb_data = (np.reshape(data_yb, (noutd, numbin)))
    with open(num_file, 'rb') as f_num:
        for k_yb in range(1):
            data_num = np.fromfile(f_num, dtype=np.float32)
            num_data = (np.reshape(data_num, (noutd, numbin)))

    method = "Qseis"
    vol_data = "Mig"
    filename = PSDM_pro_path+"/poststack/"+hdpmig_out_field
    with open(filename, 'rb') as f:
        for k in range(1):
            data_mig = np.fromfile(f, dtype=np.float32)
            profile_mig = (np.reshape(data_mig, (nx, nz)))

    fig, ax = plt.subplots(3, 1, figsize=(16, 14), sharex=True,
                           gridspec_kw={'height_ratios': [2, 3, 3]})
    im00 = ax[0].plot(LatRange, yb_data[1], 'k', lw=4, label="Half Bin Width(km)")
    ax[0].set_ylabel("Half Bin Width(km)")
    # ax[0].legend(["Half Bin Width (km)"])
    ax_00 = ax[0].twinx()
    ax_00.plot(LatRange, num_data[1, :], 'r', label="RF num")
    # ax_00.set_ylim([0,400])
    ax_00.set_ylabel("RF number")
    ax_00.set_title("Parameters at 100km")
    ax[0].legend(loc=2)
    ax_00.legend(loc=1)

    im1 = ax[1].pcolor(LatRange, Trange, profile.T,
                       cmap="coolwarm", vmin=-0.6, vmax=0.6)
    # im1=ax[1].contourf(Xrange,Trange,profile.T)
    cax = add_right_cax(ax[1], pad=0.02, width=0.02)
    cbar = fig.colorbar(im1, cax=cax)
    im1.set_clim(-0.5, 0.5)
    ax[1].set_ylim([0, 30])
    # ax[1].set_xlabel("Offset (km)")
    ax[1].set_ylabel("T(s)")
    ax[1].invert_yaxis()
    ax[1].set_title("CCP stack section")
    # fig.colorbar()
    im1 = ax[2].pcolormesh(LatRange, Yrange, profile_mig.T,
                           cmap="jet", vmin=-0.6, vmax=0.6)
    # im1=ax[1].contourf(Xrange,Trange,profile.T)
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
    # ax[0].set_title("Migration section")
    # ax[2].text(0.65,0.02,(method+"_"+str(vol_data)+" Freq "+str(freq_min)+"-"+str(freq_max)+"Hz"),fontdict={'size':'24','color':'k'},transform=ax[2].transAxes)
    # plt.tight_layout()
    # plt.savefig("/home/georom1996/PracticeJoe/PyPSDM/SynPSDM/QseisMigration2022.png",bbox_inches='tight')
    # plt.savefig("/home/georom1996/PracticeJoe/PyPSDM/SynPSDM/"+model_tag+"QseisMigration2022.pdf",format='pdf')
    plt.savefig(cwdfd+"/figs/"+"example002_IASP_PSDM_Map.jpg",
                dpi=300, bbox_inches='tight')

