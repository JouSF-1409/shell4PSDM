from os.path import isdir, join, exists
from collections import namedtuple
from dataclasses import dataclass

"""
使用dataclass类来限制参数的具体类型。
setxxx函数本意通过解包来实现比较方便的格式化，未来可能放在类的__str__方法里面
"""


# cfg_m660q = namedtuple(
#    ### 该设置主要做走时文件的工作
#    "cfg_m660q",
#    [
#        "ref_model"   # 速度模型文件
#        ,"ray"      # 射线路径文件
#        ,"m6690q_out"   # 输出文件名
#        ,"iflat"           # 是否做展平变换，0表不做，1表做
#        ,"itype"       # 计算震相的类型 >0表示Ps，<0 表示Sp
#        #,"LayerCount"
#    ]
# )
@dataclass
class cfg_m660q:
    ref_model: str = "cwbq"
    ray: str = "mray_cwbq.dat"  # 射线路径文件
    m660q_out: str = "m660q_cwbq_Pcs1.out"  # 输出文件名
    iflat: int = 1  # 是否做展平变换，0表不做，1表做
    itype: int = 1  # 计算震相的类型 >0表示Ps，<0 表示Sp
    # ,"LayerCount",


def setcfg_m660q(cfg: cfg_m660q, path):
    """保存m660q的配置文件

    Parameters
    ----------
    cfg : cfg_m660q, 配置信息
    path : PSDM的文件夹, 会检测是否存在必要的可执行程序文件
    """

    try:
        path2m660 = join(path, "m660q");
        if not exists(join(path2m660, "M660q_model")):
            raise IOError("no M660q_model exits in dic, plz make before running")

        outs = open(
            join(path2m660, "m660q_model.in"),
            'w'
        )

        print(
            "* velocity model file\n\
            %s\n\
            * ray file\n\
            %s\n\
            * output file\n\
            %s\n\
            * iflat, itype (= 0: free-surface refl.; else: conversion (>0: Ps; <0: Sp))\n\
            %d     %d\n\
            \n\
            " % (cfg), file=outs
        )
        outs.close()
    except:
        raise IOError("failed while writing m660q cfg file")


# default_cfg_pierce_new_n = cfg_Pierce_new_n(
#    "pierc_cwbq_nf2p5_wncc-s1_Pcs.dat",
#    38.0,117.0,
#    1251, 0,
#    "../model/cwbq",
#    1,28.0,95.0,
#    "47,3 4,4 6,5 7,6 8,7 9,8 10,9 11,10 12,11 13,12 14,13 15,14 16,15 17,16 18,17 19,18 20,19 21,20 22,21 23,22 24,23 25,24 26,25 27,26 28,27 29,28 30,29 31,30 32,31 33,32 34,33 35,34 36,35 37,36 38,37 39,38 40,39 41,40 42,41 43,42 44,43 45,44 46,45 47,46 48,47 49,48 50,49 51",
#    "2  6  12  23   38           32-, 100-, 207-, 407-, 666-km",
#    "../data/",
#    1,"f2p5_dt01_s1","datalist.txt"
# )
@dataclass
class cfg_Pierce_new_n:
    # 射线追踪并计算选定深度上的转换点位置。为下一步共转换点叠加与时差校正准备输入文件
    # 根据输出的转换点分布（数据覆盖）设计剖面和叠加窗大小等。
    pierc_out: str = "pierc_cwbq_nf2p5_wncc-s1_Pcs.dat"  # 射线计算结果输出
    # 中心点的位置
    # 以给定的参考点为原点将大地坐标系（经纬度）转换为笛卡尔坐标系进行后续计算和成像，其中正北为Y轴正方向，正东为X轴正方向。
    center_la: float = 38.0
    center_lo: float = 117.0
    # 输出的 事件长度 in npts； 射线参数保存的位置, 0 for user0
    out_npts: int = 1251,
    sac_user_num_rayp: int = 0
    # 速度模型的位置
    ref_model: str = "../model/cwbq"
    # 筛选事件， 0,1,2 分别表示 震中距(km), 震中距(degree)，反方位角
    # 0: dist; 1: gcarc; 2: baz
    event_filt_flag: int = 1
    event_filt_min: int = 28
    event_filt_max: int = 95
    # 没搞懂的参数名称
    _nw: str = "47,3 4,4 6,5 7,6 8,7 9,8 10,9 11,10 12,11 13,12 14,13 15,14 16,15 17,16 18,17 19,18 20,19 21,20 22,21 23,22 24,23 25,24 26,25 27,26 28,27 29,28 30,29 31,30 32,31 33,32 34,33 35,34 36,35 37,36 38,37 39,38 40,39 41,40 42,41 43,42 44,43 45,44 46,45 47,46 48,47 49,48 50,49 51",
    _ndw: str = "2  6  12  23   38           32-, 100-, 207-, 407-, 666-km",
    rfdata_path: str = "../data/"  # 项目文件夹路径
    # 简便起见，这里推荐一次只计算一个项目
    num_sub: int = 1  # 项目文件夹数量
    name_sub: str = "f2p5_dt01_s1"  # 项目文件夹名称
    name_lst: str = "datalist.txt"  # 项目文件夹内 台站目录 的文件名，台站目录格式为
    # 台站名\n接收函数数量\n接收函数的文件名\n...\n 空行\n 新台站....
    # 最后为台站总数


# cfg_Pierce_new_n = namedtuple("cfg_Pierce_new_n", [
#    # 射线追踪并计算选定深度上的转换点位置。为下一步共转换点叠加与时差校正准备输入文件
#    # 根据输出的转换点分布（数据覆盖）设计剖面和叠加窗大小等。
#    "pierc_out"  # 射线计算结果输出
#    # 中心点的位置
#    # 以给定的参考点为原点将大地坐标系（经纬度）转换为笛卡尔坐标系进行后续计算和成像，其中正北为Y轴正方向，正东为X轴正方向。
#    ,"center_la","center_lo"
#    # 输出的 事件长度 in npts； 射线参数保存的位置, 0 for user0
#    ,"out_npts",    "sac_user_num_rayp"
#    # 速度模型的位置
#    ,"ref_model"
#    # 筛选事件， 0,1,2 分别表示 震中距(km), 震中距(degree)，反方位角
#    # 0: dist; 1: gcarc; 2: baz
#    ,"event_filt_flag" ,"event_filt_min","event_filt_max"
#    # 没搞懂的参数名称
#    ,"nw"
#    ,"ndw"
#    ,"rfdata_path"  # 项目文件夹路径
#    # 简便起见，这里推荐一次只计算一个项目
#    ,"num_sub"      # 项目文件夹数量
#    ,"name_sub"     # 项目文件夹名称
#    ,"name_lst"     # 项目文件夹内 台站目录 的文件名，台站目录格式为
#                    # 台站名\n接收函数数量\n接收函数的文件名\n...\n 空行\n 新台站....
#                    # 最后为台站总数
# ])

def setcfg_Pierce_new_n(cfg: cfg_Pierce_new_n, path):
    """
    同理
    """
    try:
        path2stack = join(path, "stack")
        if not exists(join(path2stack, "pierc_new_n")):
            raise IOError("no pierc_new_n exits in dic, plz make before running")

        outs = open(
            join(path2stack, "pierc_new_n.in"),
            'w+')
        print(
            "* output file name: iaj\n\
            %s\n\
            * the coordinate center of line: evla0,evlo0\n\
            %f, %f\n\
             * output time point number: np0, irayp\n\
            %d      %d\n\
            * model file\n\
            %s\n\
            * * ivar (0: dist; 1: gcarc; 2: baz),varmin,varmax\n\
            %d     %f     %f\n\
            * NW,(NWI(I),NWID(I),I=1,NW)\n\
            %s\n\
            * NDW(1:5): indexs in NWI for outputting piercing points at 5 depths\n\
            %s\n\
            * directory containing RFs\n\
            %s\n\
            * number of subdirectories\n\
            %d\n\
            %s\n\
            %s\n\
            \n" % cfg, file=outs
        )
        outs.close()
    except:
        raise IOError("failed while prepare Pierc_new_n")


@dataclass
class cfg_binr_vary_scan_n:
    # ccp叠加剖面的划分，这里的坐标均按之前计算得到的笛卡尔坐标表示，距离为km
    # 表示剖面组 的起止点位置，step表示每次起点移动的距离
    # 如果起点的begin和end相同，则有不同的起点
    Descar_la_begin: float = 205.
    Descar_lo_begin: float = -900.
    Descar_la_end: float = 205.
    Descar_lo_end: float = -900.
    Descar_step: float = 100.
    # 每个剖面的设置，剖面长度，方位角范围，方位角step。同样可以获得不同的剖面
    Profile_len: float = 700.
    az_min: float = 90.
    az_max: float = 90.
    az_step: float = 10.
    # 叠加窗的设置，相邻叠加窗中心点的距离，bin中最小接收函数数量，最小数量下的比率（决定了接收函数的归一化方法），UTMOST投影下研究区域的代表值
    # 如果bin的单元内接收函数的个数小于least number of traces，bin的范围会根据YBIN的设置自动扩大，直到大于最大DYBIN停止外扩。
    # 振幅的归一化：当RF的个数小于rnumtra*numtra时，采用SUM()/(rnumtra*numtra) 代替SUM()/(num of RFs in stacking)，否则还是用SUM()/(num of RFs in stacking)。这样做的目的是为压制RF数目较少的叠加振幅。
    bins_step: float = 2
    trace_num_min: int = 2
    ratio_trace: float = 1
    UTM_zone: float = 50
    # m660q 中计算的输出表，不同深度转换波的理论到时
    timefile: str = "m660q_cwbq_Pcs1.out"
    # ccp叠加的输出文件名
    outpufile: str = "inw20cw_ispwnccaz90_yb15-100vnt2_xb200_dx2_norm0_nf2p5-s1_Pcs"
    # 输出的每道采样点数， 采样间隔，
    out_trace_npts: int = 1001
    out_trace_dt: float = 0.1
    # nw, ninw pair?
    nw_pair: str = "20,1 -200,2 120,3 120,4 120,5 120,6 120,7 120,8 120,9 120,10 120,11 120,12 120,13 120,14 120,15 120,16 120,17 120,18 120,19 120,20 120"
    # Ybin 的一些设计，有些看不明白
    minYbin: str = "15,20,25,30,30,32,32,34,34,36,36,38,38,40,40,42,44,46,48,50"
    Dybin: str = "-2,2,2,2,2,2,3,3,3,3,3,3,3,4,4,4,4,4,4,4"
    maxYbin: str = "30,40,50,60,60,65,65,70,70,75,75,80,80,80,80,85,90,90,95,100"
    # 处理过程中的临时文件夹
    tmpdir: str = "../temp"
    # flag = 0,1,<0; 0表用pierc_new_n的平均震中距为参考做动校正, <0为不做动校正，=1为按选择的震中距为参考做动校正
    # 由于张周提前做了动校正，这里他的内容将其关掉
    moveout_flag: int = 0,
    moveout_gcarc: float = 180.
    # 是否对振幅做归一化处理，0表示不做，其他的表示对每个RF单独做一次
    norm_flag: int = 1
    # 输出的深度坐标与对应的实际深度
    _ninw: str = "5       3    6    9    12    17          49-, 100-, 153-, 207-, 297-km"
    # 叠加的标记。 没看懂，这里推荐打开
    stack_flag: int = 1
    # 没看懂，推荐为0
    ioutb: int = 0
    # piercing point data file number
    npief: int = 1
    # 转换点数据信息的文件名，从pierce_new_n 这一步获得。
    binr_out_name: str = "pierc_cwbq_nf2p5_wncc-s1_Pcs.dat"


# cfg_binr_vary_scan_n = namedtuple(
#    # 包括动校正的ccp叠加程序
#    "cfg_binr_vary_scan_n",
#    [
#    # ccp叠加剖面的划分，这里的坐标均按之前计算得到的笛卡尔坐标表示，距离为km
#    # 表示剖面组 的起止点位置，step表示每次起点移动的距离
#    # 如果起点的begin和end相同，则有不同的起点
#    "Descar_la_begin", "Descar_lo_begin", "Descar_la_end", "Descar_lo_end", "Descar_step",
#     # 每个剖面的设置，剖面长度，方位角范围，方位角step。同样可以获得不同的剖面
#     "Profile_len", "az_min", "az_max", "az_step",
#    # 叠加窗的设置，相邻叠加窗中心点的距离，bin中最小接收函数数量，最小数量下的比率（决定了接收函数的归一化方法），UTMOST投影下研究区域的代表值
#    #如果bin的单元内接收函数的个数小于least number of traces，bin的范围会根据YBIN的设置自动扩大，直到大于最大DYBIN停止外扩。
#    # 振幅的归一化：当RF的个数小于rnumtra*numtra时，采用SUM()/(rnumtra*numtra) 代替SUM()/(num of RFs in stacking)，否则还是用SUM()/(num of RFs in stacking)。这样做的目的是为压制RF数目较少的叠加振幅。
#     "bins_step", "trace_num_min", "ratio_trace","UTM_zone",
#    # m660q 中计算的输出表，不同深度转换波的理论到时
#    "timefile",
#    # ccp叠加的输出文件名
#    "outpufile",
#    # 输出的每道采样点数， 采样间隔，
#     "out_trace_npts", "out_trace_dt", "temp_folder",
#    # nw, ninw pair?
#    "nw_pair",
#    # Ybin 的一些设计，有些看不明白
#    "minYbin","Dybin","maxYbin",
#    # 处理过程中的临时文件夹
#    "tmpdir",
#    # flag = 0,1,<0; 0表用pierc_new_n的平均震中距为参考做动校正, <0为不做动校正，=1为按选择的震中距为参考做动校正
#    # 由于张周提前做了动校正，这里他的内容将其关掉
#    "moveout_flag",    "moveout_gcarc",
#    # 是否对振幅做归一化处理，0表示不做，其他的表示对每个RF单独做一次
#    "norm_flag",
#    # 输出的深度坐标与对应的实际深度
#    "ninw",
#    # 叠加的标记。 没看懂，这里推荐打开
#    "stack_flag",
#    # 没看懂，推荐为1
#    "ioutb",
#    # piercing point data file number
#    "npief",
#    # 转换点数据信息的文件名，从pierce_new_n 这一步获得。
#    "binr_out_name"]
# )

def setcfg_binr_vary_scan_n(cfg: cfg_binr_vary_scan_n, path):
    """
    同理
    """
    try:
        path2stack = join(path, "stack")
        if not exists(join(path2stack, "binr_vary_scan_n")):
            raise IOError("no binr_vary_scan_n exits in dic, plz make before running")
        outs = open(
            join(path2stack, "binr_vary_scan_n.inp"),
            'w'
        )
        print(
            "* begin and end coordinate of start point, point interval(km): begla0,beglo0,endla0,endlo0,dsp\n\
            %f,%f,%f,%f,%f,\n\
            * profile length and azimuth range and interval: xlenp,alphab,alphae,dalp\n\
            %f,%f,%f,%f\n\
            * the spacing between bins, least number of traces, rnumtra, UTM_PROJECTION_ZONE(new)\n\
            %d %d %f %d\n\
            * time file name: timefile\n\
            %s\n\
            * output file name: outfile\n\
            %s\n\
            * ouput number of time samples in each trace: npt, dt\n\
            %d     %f\n\
            * the indexes of reference ray among 1 -- nw: ninw, (inw0(i),i=1,ninw)   \n\
            %s\n\
            * minimum YBIN (km)\n\
            %f\n\
            * DYBIN (km)\n\
            %f\n\
            * maximum YBIN (km)\n\
            %f\n\
            *temporary directory name to store the intermedial files (.img)\n\
            %s\n\
            * moveout index: idist, gcarc1  (only useful for idist=1)\n\
            %d  %f\n\
            * inorm\n\
            %d \n\
            * output number and depth indexes in ninw: noutd,(ioutd(i),i=1,noutd)\n\
            %s\n\
            * output index for stacking: istack\n\
            %d \n\
            * output index for gcarc, baz and p: ioutb\n\
            %d\n\
            * piercing point data file number: npief\n\
            %d\n\
            * input file name: infile\n\
            %s\n\
            " % (cfg), file=outs
        )
        outs.close()

    except:
        raise IOError("failed while prepare binr_vary_scan_n")


# cfg_Hdpmig = namedtuple(
#    "Hdpmig",
#    [
#        # 方法的选择，参考速度的选取方式，真正的参考速度是选取的参考速度*vscale
#        # imethod = 0: phase-shift; = 1: phase-screen; = else: pseudo-screen
#        "imethod","irefvel","vscale",
#        # 用于偏移成像的频率范围(截止区间),平滑点数
#        "fmin","fmax","ifreqindl","ifreqindr",
#        # 道数， 深度， 剖面与深度方向上，大于道数和深度的最小2的整数倍点，
#        "nxmod", "nzmod", "nx", "nz",
#        # 剖面上道的采样间隔， 垂直方向上的深度间隔
#        "dx","dz",
#        # 道数，npts， 采样间隔， 时间域上大于npts 的最小指数, 为节约时间计算的开始点数
#        "ntrace", "nt", "dt", "nt0", "ntb",
#        # 只有在hybscreen 时才会用到，只能为15，45，60 其中的一个
#        "FD",
#        # 空间剖面上向两侧平滑的点数
#        "nxleft", "nxright",
#        # 输入偏移成像用的速度模型的格式：0-ASCII码，即文本文件，1-二进制的2D速度模型，包括偏移速度？
#        "ifmat",
#        # 速度模型路径
#        "velmod",
#        # 输入的叠加波场，即之前ccp叠加得到的结果
#        "tx_data",
#        # 最终结果的文件名
#        "migdata",
#        # ntrace是选择的输入道数间隔，如果intrace为正，则从tx_data文件中读取的输入波场是按正常顺序由第十三行参数itrfirst定义的第一道位置开始、每间隔intrace道的波场；如果intrace为负，则第十三行参数为输入波场的各道位置文件名，从tx_data中读取的是对应于该文件中给出的各道波场。这两个参数一般用不上，主要在测试中使用。
#        "intrace", "itrfirst"
#
#    ]
# )
# default_cfg_Hdpming = cfg_Hdpmig(
#    0,0,1.0,
#    0.01,1.2,0,40,
#    351,800,1024,800,
#    2,0.5,
#    351,1001,0.1,2048,1,
#    45,
#    40,40,
#    0,
#    "../model/cwbq",
#    "../stack/stack_inw20cw_ispwnccaz90_yb15-100vnt2_xb200_dx2_norm0_nf2p5-s1_Pcs.dat",
#    "image_dx2dz05_inw20cw_ispwnccaz90_yb15-100vnt2_xb200_norm0_nf2p5-s1_Pcs_f0.01-1.20tl0r40_cwbq_nx351nz800.dat",
#    1,1
# )
@dataclass
class cfg_Hdpmig:
    # 方法的选择，参考速度的选取方式，真正的参考速度是选取的参考速度*vscale
    # imethod = 0: phase-shift; = 1: phase-screen; = else: pseudo-screen
    imethod: int = 0
    irefvel: int = 0
    vscale: float = 1.0
    # 用于偏移成像的频率范围(截止区间),平滑点数
    fmin: float = 0.01
    fmax: float = 1.2
    ifreqindl: float = 0
    ifreqindr: float = 40
    # 道数， 深度， 剖面与深度方向上，大于道数和深度的最小2的整数倍点，
    nxmod: int = 351
    nzmod: int = 1001
    nx: int = 1024
    nz: int = 800
    # 剖面上道的采样间隔， 垂直方向上的深度间隔
    dx: int = 2
    dz: int = 0.5
    # 道数，npts， 采样间隔， 时间域上大于npts 的最小指数, 为节约时间计算的开始点数
    ntrace: int = 351
    nt: int = 1001
    dt: float = 0.1
    nt0: int = 2048
    ntb: int = 1
    # 只有在hybscreen 时才会用到，只能为15，45，60 其中的一个
    _FD: int = 45
    # 空间剖面上向两侧平滑的点数
    nxleft: int = 40
    nxright: int = 40
    # 输入偏移成像用的速度模型的格式：0-ASCII码，即文本文件，1-二进制的2D速度模型，包括偏移速度？
    ifmat: int = 0
    # 速度模型路径
    velmod: str = "../model/cwbq"
    # 输入的叠加波场，即之前ccp叠加得到的结果
    tx_data: str = "../stack/stack_inw20cw_ispwnccaz90_yb15-100vnt2_xb200_dx2_norm0_nf2p5-s1_Pcs.dat"
    # 最终结果的文件名
    migdata: str = "image_dx2dz05_inw20cw_ispwnccaz90_yb15-100vnt2_xb200_norm0_nf2p5-s1_Pcs_f0.01-1.20tl0r40_cwbq_nx351nz800.dat",
    # ntrace是选择的输入道数间隔，如果intrace为正，则从tx_data文件中读取的输入波场是按正常顺序由第十三行参数itrfirst定义的第一道位置开始、每间隔intrace道的波场；如果intrace为负，则第十三行参数为输入波场的各道位置文件名，从tx_data中读取的是对应于该文件中给出的各道波场。这两个参数一般用不上，主要在测试中使用。
    intrace: int = 1
    itrfirst: int = 1


def setcfg_Hdpmig(cfg: cfg_Hdpmig, path):
    try:
        path2migrat = join(path, "poststack")
        if not exists(join(path2migrat, "hdpmig.x")):
            raise IOError("no hdpmig.x exits in dic, plz make before running")
        outs = open(
            join(path2migrat, "hdpmig.in"),
            'w'
        )
        print(
            "* imethod (phshift=0; phscreen=1, hybscreen: else),irefvel,vscale \n\
            %d %d %f\n\
            * fmin, fmax (Minimum and maximum frequencies), ifreqindl, ifreqindr\n\
            %f %f %f %f\n\
            * nxmod, nzmod, nx, nz\n\
            %d %d %d %d\n\
            * dx, dz\n\
            %f %f\n\
            * ntrace, nt, dt (in sec.), nt0, ntb\n\
            %d %d %f %f %d\n\
            * FD method (15, 45, 65)\n\
            %d\n\
            * nxleft, nxright\n\
            %d %d\n\
            * ifmat (=0: ascii vel. file; else: binary vel. file)\n\
            %d\n\
            * modvelocity\n\
            %s\n\
            * tx_data (input seismic data)\n\
            %s\n\
            * migdata (output imaging data)\n\
            %s\n\
            * intrace\n\
            %d\n\
            * first trace index: itrfirst\n\
            %d\n\
            " % (cfg), file=outs
        )
        outs.close()

    except:
        raise IOError("failed while prepare hdpmig")

# default_cfg_m660q = cfg_m660q(
#    "cwbq","mray_cwbq.dat","m660q_cwbq_Pcs1.out",
#    1,1
# )
# default_cfg_pierce_new_n = cfg_Pierce_new_n(
#    "pierc_cwbq_nf2p5_wncc-s1_Pcs.dat",
#    38.0,117.0,
#    1251, 0,
#    "../model/cwbq",
#    1,28.0,95.0,
#    "47,3 4,4 6,5 7,6 8,7 9,8 10,9 11,10 12,11 13,12 14,13 15,14 16,15 17,16 18,17 19,18 20,19 21,20 22,21 23,22 24,23 25,24 26,25 27,26 28,27 29,28 30,29 31,30 32,31 33,32 34,33 35,34 36,35 37,36 38,37 39,38 40,39 41,40 42,41 43,42 44,43 45,44 46,45 47,46 48,47 49,48 50,49 51",
#    "2  6  12  23   38           32-, 100-, 207-, 407-, 666-km",
#    "../data/",
#    1,"f2p5_dt01_s1","datalist.txt"
# )
# default_cfg_bin_var_scan_n = cfg_binr_vary_scan_n(
#    205.0,-900.0,205.0,-900.0,100.0,
#    700.0,90.3,90.0,10.0,
#    2,2,1.0,50,
#    "m660q_cwbq_Pcs1.out",
#    "inw20cw_ispwnccaz90_yb15-100vnt2_xb200_dx2_norm0_nf2p5-s1_Pcs",
#    1001,0.1,
#    "20,1 -200,2 120,3 120,4 120,5 120,6 120,7 120,8 120,9 120,10 120,11 120,12 120,13 120,14 120,15 120,16 120,17 120,18 120,19 120,20 120",
#    "15,20,25,30,30,32,32,34,34,36,36,38,38,40,40,42,44,46,48,50",
#    "-2,2,2,2,2,2,3,3,3,3,3,3,3,4,4,4,4,4,4,4",
#    "30,40,50,60,60,65,65,70,70,75,75,80,80,80,80,85,90,90,95,100",
#    "../temp",
#    1,180.0,
#    0,
#    "5       3    6    9    12    17          49-, 100-, 153-, 207-, 297-km",
#    1,0,1,
#    "pierc_cwbq_nf2p5_wncc-s1_Pcs.dat"
# )
# default_cfg_Hdpming = cfg_Hdpmig(
#    0,0,1.0,
#    0.01,1.2,0,40,
#    351,800,1024,800,
#    2,0.5,
#    351,1001,0.1,2048,1,
#    45,
#    40,40,
#    0,
#    "../model/cwbq",
#    "../stack/stack_inw20cw_ispwnccaz90_yb15-100vnt2_xb200_dx2_norm0_nf2p5-s1_Pcs.dat",
#    "image_dx2dz05_inw20cw_ispwnccaz90_yb15-100vnt2_xb200_norm0_nf2p5-s1_Pcs_f0.01-1.20tl0r40_cwbq_nx351nz800.dat",
#    1,1
# )
