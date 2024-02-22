import matplotlib.pyplot as plt
import pandas as pd
import os
from matplotlib import rcParams
# Observation System PLOT PART
##################################################################################################
config = {"font.family": 'sans-serif',
          "font.size": 16, "mathtext.fontset": 'stix'}
rcParams.update(config)

binr_out_name = '2022_binr_out_Qseis_1s'
cwdfd = os.getcwd() # current work directory
PSDM_pro_path = cwdfd+"/psdm/PSDM_qseis2022_IASP/"
pierce_xy_file1 = PSDM_pro_path+"/stack/depth1.dat"
pierce_xy_file2 = PSDM_pro_path+"/stack/depth2.dat"
sta_xy_file = PSDM_pro_path+"/stack/station.dat"
pro_xy_file = PSDM_pro_path+"/stack/"+binr_out_name+"_profile.txt"

pierce_xy1 = pd.read_csv(pierce_xy_file1, sep='\s+',
                         header=None, names=["lat", "lon", "decy", "decx"])
pierce_xy2 = pd.read_csv(pierce_xy_file2, sep='\s+',
                         header=None, names=["lat", "lon", "decy", "decx"])
sta_xy = pd.read_csv(sta_xy_file, sep='\s+', header=None,
                     names=["lat", "lon", "decy", "decx"])
pro_xy = pd.read_csv(pro_xy_file, sep='\s+', header=None,
                     names=["lon", "lat", "decx", "decy", "offset"])

plt.figure(figsize=(20, 8))
plt.subplot(121)
plt.scatter(pierce_xy2.decx, pierce_xy2.decy, color='green', marker='.')
plt.scatter(pierce_xy1.decx, pierce_xy1.decy, color='red', marker='.')
plt.scatter(sta_xy.decx, sta_xy.decy, color='k', marker='^',)
plt.plot(pro_xy.decx, pro_xy.decy, 'blue', linewidth=3)

plt.subplot(122)
plt.scatter(pierce_xy2.lon, pierce_xy2.lat, color='green', marker='.')
plt.scatter(pierce_xy1.lon, pierce_xy1.lat, color='red', marker='.')
plt.scatter(sta_xy.lon, sta_xy.lat, color='k', marker='^')
plt.plot(pro_xy.lon, pro_xy.lat, 'blue', linewidth=3)
plt.savefig(cwdfd+"/figs/"+"observation_system_plot.jpg",
            dpi=300, bbox_inches='tight')