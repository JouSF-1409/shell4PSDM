# 这里给出张周的 S波配置示例
###############################################################
ZhangZhou_S_wave_m660 = {
    # 参考速度模型
    "ref_model": 'CDmod',
    # 射线路径文件
    "Ps_ray": "mray_joe.Sp.dat",
    "iflat": 0,  # 是否做展平变换，0表不做，1表做
    "itype": -1  # 计算震相的类型 >0表示Ps，<0 表示Sp
}

# Parameters I concerned about
# build mray_joe.Ps.dat and mray_joe.Sp.dat
LayerCount = 51
ZhangZhou_S_wave_pierc = {
    # 射线追踪并计算选定深度上的转换点位置。为下一步共转换点叠加与时差校正准备输入文件
    # 根据输出的转换点分布（数据覆盖）设计剖面和叠加窗大小等。
    "pierc_out": "../pierc_use.dat",
    # 中心点的位置
    # 以给定的参考点为原点将大地坐标系（经纬度）转换为笛卡尔坐标系进行后续计算和成像，其中正北为Y轴正方向，正东为X轴正方向。
    "center_la": 27.5, "center_lo": 104,
    "out_npts": 1251,
    # 输出的 事件长度 in npts； 射线参数保存的位置, 0 for user0
    "sac_user_num_rayp": 0,
    # 速度模型的位置
    "ref_model": "../data/CDmod",
    # 筛选事件， 0,1,2 分别表示 震中距(km), 震中距(degree)，反方位角
    # 0: dist; 1: gcarc; 2: baz
    "event_filt_flag": 1,
    "event_filt_min": 70.0, "event_filt_max": 80.0,
    # 项目文件夹路径
    "rfdata_path": "../data/",
    # 简便起见，这里推荐一次只计算一个项目
    "num_sub": 1,
    "name_sub": "sub_name",  # 项目文件夹名称
    "name_lst": "datalist.txt"  # 提供了生成list 的函数
    # 项目文件夹内 台站目录 的文件名，台站目录格式为
    # 台站名\n接收函数数量\n接收函数的文件名\n...\n 空行\n 新台站....
}

ZhangZhou_S_wave_binr = {
    # ccp叠加剖面的划分，这里的坐标均按之前计算得到的笛卡尔坐标表示，距离为km
    # 表示剖面组 的起止点位置，step表示每次起点移动的距离
    # 如果起点的begin和end相同，则有不同的起点
    "Descar_la_begin": -500., "Descar_la_end": -500,
    "Descar_lo_begin": 0, "Descar_lo_end": 0,
    "Descar_step": 100,
    # 每个剖面的设置，剖面长度，方位角范围，方位角step。同样可以获得不同的剖面
    "Profile_len": 1000.,
    "az_min": 90., "az_max": 90., "az_step": 10.,
    # 叠加窗的设置，相邻叠加窗中心点的距离，bin中最小接收函数数量，最小数量下的比率（决定了接收函数的归一化方法），UTMOST投影下研究区域的代表值
    # 如果bin的单元内接收函数的个数小于least number of traces，bin的范围会根据YBIN的设置自动扩大，直到大于最大DYBIN停止外扩。
    # 振幅的归一化：当RF的个数小于rnumtra*numtra时，采用SUM()/(rnumtra*numtra) 代替SUM()/(num of RFs in stacking)，否则还是用SUM()/(num of RFs in stacking)。这样做的目的是为压制RF数目较少的叠加振幅。
    "bins_step": 2.,
    "trace_num_min": 2,
    "ratio_trace": 1,
    "UTM_zone": 50,
    # m660q 中计算的输出表，不同深度转换波的理论到时
    "timefile": "mray_joe.Sp.dat",
    # ccp叠加的输出文件名
    "outputfile": '2022_binr_out_Qseis_1s.dat',
    # 输出的每道采样点数， 采样间隔，
    "out_trace_npts": 1001, "out_trace_dt": 0.1,
    # nw, ninw pair?
    "nw_pair": "20,1 -400,2 120,3 120,4 120,5 120,6 120,7 120,8 120,9 120,10 120,11 120,12 120,13 120,14 120,15 120,16 120,17 120,18 120,19 120,20 120",
    # 叠加窗涉及
    "minYbin": "15,20,25,30,30,32,32,34,34,36,36,38,38,40,40,42,44,46,48,50",
    "Dybin": "-50,2,2,2,2,2,3,3,3,3,3,3,3,4,4,4,4,4,4,4",
    # 处理过程中的临时文件夹
    "tmpdir": "../temp",
    # flag = 0,1,<0; 0表用pierc_new_n的平均震中距为参考做动校正, <0为不做动校正，=1为按选择的震中距为参考做动校正
    # 由于张周提前做了动校正，这里他的内容将其关掉
    "moveout_flag": -1,
    "moveout_gcarc": 180.,
    # 是否对振幅做归一化处理，0表示不做，其他的表示对每个RF单独做一次
    "norm_flag": 0,
    "_ninw": "5 6 13 16 19 36      40-, 100-, 150-, 210-, 300-km",
    # 叠加的标记。 没看懂，这里推荐打开
    "stack_flag": 1,
    # piercing point data file number
    "npief": 1,
    # 转换点数据信息的文件名，从pierce_new_n 这一步获得。
    "ioutb": 0,
    "binr_out_name": "2022_binr_out_Qseis_1s"
}

ZhangZhou_S_wave_Hdpmig = {
    # 方法的选择，参考速度的选取方式，真正的参考速度是选取的参考速度*vscale
    # imethod = 0: phase-shift; = 1: phase-screen; = else: pseudo-screen
    "imethod": 0, "irefvel": 0, "vscale": 1.0,
    # 用于偏移成像的频率范围(截止区间),平滑点数
    "fmin": 0.03, "fmax": 0.5,
    "ifreqindl": 0, "ifreqindr": 40,
    # 道数， 深度， 剖面与深度方向上，大于道数和深度的最小2的整数倍点，
    "nxmod": 21, "nzmod": 1600,
    "nx": 1024, "nz": 1600,
    # 剖面上道的采样间隔， 垂直方向上的深度间隔
    "dx": 50, "dz": 0.5,
    # 道数，npts， 采样间隔， 时间域上大于npts 的最小指数, 为节约时间计算的开始点数
    "ntrace": 21,
    "nt": 1001, "dt": 0.1,
    "nt0": 2048, "ntb": 1,
    # 只有在hybscreen 时才会用到，只能为15，45，60 其中的一个
    "_FD": 45,
    # 空间剖面上向两侧平滑的点数
    "nxleft": 4,
    "nxright": 4,
    # 输入偏移成像用的速度模型的格式：0-ASCII码，即文本文件，1-二进制的2D速度模型，包括偏移速度？
    "ifmat": 0,
    # 速度模型路径
    "velmod": "../model/CDmod",
    # 输入的叠加波场，即之前ccp叠加得到的结果
    "tx_data": "../stack/stack_" + "2022_binr_out_Qseis_1s" + ".dat",
    # 最终结果的文件名
    "migdata": "QseisMig_hdpmig.joe.dat"
}

ZhangZhou_S_wave_Plot = {
    "xlenp": 1000,
    "npt": 1001,
    "dt": 0.1,
    "depth": 800,
    "dz": 0.5,
    "prolen": 1000,
    "dx": 50,
    "noutd": 5
    # "yb_file" : PSDM_pro_path+"/stack/"+binr_out_name+"_yb.dat",
    # "num_file" : PSDM_pro_path+"/stack/"+binr_out_name+"_num.dat"
}
