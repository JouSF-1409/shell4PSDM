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
    "nw_pair" : "20,1 -400,2 120,3 120,4 120,5 120,6 120,7 120,8 120,9 120,10 120,11 120,12 120,13 120,14 120,15 120,16 120,17 120,18 120,19 120,20 120",
    "minYbin" :"15,20,25,30,30,32,32,34,34,36,36,38,38,40,40,42,44,46,48,50",
    "Dybin" : "-50,2,2,2,2,2,3,3,3,3,3,3,3,4,4,4,4,4,4,4",
    "tmpdir" : "../temp",
    "moveout_flag" : 1,
    "moveout_gcarc" : 180.,
    "norm_flag" : 0,
    "_ninw" : "5 6 13 16 19 36      40-, 100-, 150-, 210-, 300-km",
    "stack_flag" : 1,
    "npief" : 1,
    "ioutb" : 0,
    "binr_out_name" : "2022_binr_out_Qseis_1s"
}

ZhangZhou_S_wave_Hdpmig = {
   "imethod" : 0,
   "irefvel" : 0,
   "vscale" : 1.0,
   "fmin" : 0.03,
   "fmax" : 0.5,
   "ifreqindl" : 0,
   "ifreqindr" : 40,
   "nxmod" : 21,
   "nzmod" : 1600,
   "nx" : 1024,
   "nz" : 1600,
   "dx" : 50,
   "dz" : 0.5,
   "ntrace" : 21,
   "nt" : 1001,
   "dt" : 0.1,
   "nt0" : 2048,
   "ntb" : 1,
   "_FD" : 45,
   "nxleft" : 4,
   "nxright" : 4,
   "ifmat" : 0,
   "velmod" : "../model/CDmod",
   "tx_data" : "../stack/stack_"+"2022_binr_out_Qseis_1s"+".dat",
   "migdata" : "QseisMig_hdpmig.joe.dat"
}

ZhangZhou_S_wave_Plot = {
   "xlenp" : 1000,
   "npt" : 1001,
   "dt" : 0.1,
   "depth" : 800  ,
   "dz" : 0.5  ,
   "prolen" : 1000  ,
   "dx" : 50  ,
   "noutd" : 5
   #"yb_file" : PSDM_pro_path+"/stack/"+binr_out_name+"_yb.dat",
   #"num_file" : PSDM_pro_path+"/stack/"+binr_out_name+"_num.dat"
}
