from os.path import isdir, join, exists
from collections import namedtuple
from dataclasses import dataclass

"""
使用dataclass类来限制参数的具体类型。
setxxx函数本意通过解包来实现比较方便的格式化，未来可能放在类的__str__方法里面
"""


@dataclass
class cfg_m660q:
    ref_model: str = "../model/cwbq"
    ray: str = "../model/mray_cwbq.dat"  # 射线路径文件
    m660q_out: str = "m660q_cwbq_Pcs1.out"  # 输出文件名
    iflat: int = 1  # 是否做展平变换，0表不做，1表做
    itype: int = 1  # 计算震相的类型 >0表示Ps，<0 表示Sp
    # ,"LayerCount",

    def __str__(self):
        return _str_m660q(self)



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
    sac_user_num_rayp: int = 1
    # 速度模型的位置
    ref_model: str = "../model/cwbq"
    # 筛选事件， 0,1,2 分别表示 震中距(km), 震中距(degree)，反方位角
    # 0: dist; 1: gcarc; 2: baz
    event_filt_flag: int = 1
    event_filt_min: int = 28
    event_filt_max: int = 95
    # 没搞懂的参数名称
    _nw: str = "47,3 4,4 6,5 7,6 8,7 9,8 10,9 11,10 12,11 13,12 14,13 15,14 16,15 17,16 18,17 19,18 20,19 21,20 22,21 23,22 24,23 25,24 26,25 27,26 28,27 29,28 30,29 31,30 32,31 33,32 34,33 35,34 36,35 37,36 38,37 39,38 40,39 41,40 42,41 43,42 44,43 45,44 46,45 47,46 48,47 49,48 50,49 51"
    _ndw: str = "2  6  12  23   38           32-, 100-, 207-, 407-, 666-km"
    rfdata_path: str = "../data/"  # 项目文件夹路径
    # 简便起见，这里推荐一次只计算一个项目
    num_sub: int = 1  # 项目文件夹数量
    name_sub: str = "f2p5_dt01_s1"  # 项目文件夹名称
    name_lst: str = "datalist.txt"  # 项目文件夹内 台站目录 的文件名，台站目录格式为
    # 台站名\n接收函数数量\n接收函数的文件名\n...\n 空行\n 新台站....
    # 最后为台站总数

    def __str__(self):
        return _str_pierce_new_n(self)



@dataclass
class cfg_binr_vary_scan_n:
    # ccp叠加剖面的划分，这里的坐标均按之前计算得到的笛卡尔坐标表示，距离为km。这里 begin 和end 使用不同的值，以获得一系列平行的剖面。
    # 表示剖面组 的起止点位置，step表示每次起点移动的距离
    # 如果起点的begin和end相同，则有不同的起点
    Descar_la_begin: float = 205.
    Descar_lo_begin: float = -900.
    Descar_la_end: float = 205.
    Descar_lo_end: float = -900.
    Descar_step: float = 100.
    # 每个剖面的设置，剖面长度，方位角范围，方位角step。同样可以获得不同的剖面
    # min max 设置不同的值，以获取一个旋转的剖面
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
    moveout_flag: int = -1
    moveout_gcarc: float = 180.
    # 是否对振幅做归一化处理，0表示不做，其他的表示对每个RF单独做一次
    norm_flag: int = 1
    # 输出的深度坐标与对应的实际深度\
    _ninw: str = "5       3    6    9    12    17          49-, 100-, 153-, 207-, 297-km"
    # 叠加的标记。 没看懂，这里推荐打开
    stack_flag: int = 1
    # 没看懂，推荐为0
    ioutb: int = 0
    # piercing point data file number
    npief: int = 1
    # 转换点数据信息的文件名，从pierce_new_n 这一步获得。
    binr_out_name: str = "pierc_cwbq_nf2p5_wncc-s1_Pcs.dat"

    def __str__(self):
        return _str_binr_vary_scan_n(self)


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
    nzmod: int = 800
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

    def __str__(self):
        return _str_hdpming(self)


def _str_m660q(cfg):
    return \
f"* velocity model file\n\
{cfg.ref_model}\n\
* ray file\n\
{cfg.ray}\n\
* output file\n\
{cfg.m660q_out}\n\
* iflat, itype (= 0: free-surface refl.; else: conversion (>0: Ps; <0: Sp))\n\
{cfg.iflat:01d}     {cfg.itype:01d}\n\
\n"


def _str_pierce_new_n(cfg):
    return \
f"* output file name: iaj\n\
{cfg.pierc_out}\n\
* the coordinate center of line: evla0,evlo0\n\
{cfg.center_la:.1f}, {cfg.center_lo:.1f}\n\
 * output time point number: np0, irayp\n\
{cfg.out_npts}      {cfg.sac_user_num_rayp}\n\
* model file\n\
{cfg.ref_model}\n\
* * ivar (0: dist; 1: gcarc; 2: baz),varmin,varmax\n\
{cfg.event_filt_flag}     {cfg.event_filt_min}     {cfg.event_filt_max}\n\
* NW,(NWI(I),NWID(I),I=1,NW)\n\
{cfg._nw}\n\
* NDW(1:5): indexs in NWI for outputting piercing points at 5 depths\n\
{cfg._ndw}\n\
* directory containing RFs\n\
{cfg.rfdata_path}\n\
* number of subdirectories\n\
{cfg.num_sub}\n\
{cfg.name_sub}\n\
{cfg.name_lst}\n\
\n"


def _str_binr_vary_scan_n(cfg):
    return \
f"* begin and end coordinate of start point, point interval(km): begla0,beglo0,endla0,endlo0,dsp\n\
{cfg.Descar_la_begin},{cfg.Descar_lo_begin},{cfg.Descar_la_end},{cfg.Descar_lo_end},{cfg.Descar_step}\n\
* profile length and azimuth range and interval: xlenp,alphab,alphae,dalp\n\
{cfg.Profile_len}, {cfg.az_min}, {cfg.az_max}, {cfg.az_step}\n\
* the spacing between bins, least number of traces, rnumtra, UTM_PROJECTION_ZONE(new)\n\
{cfg.bins_step}     {cfg.trace_num_min}      {cfg.ratio_trace}      {cfg.UTM_zone}\n\
* time file name: timefile\n\
{cfg.timefile}\n\
* output file name: outfile\n\
{cfg.outpufile}\n\
* ouput number of time samples in each trace: npt, dt\n\
{cfg.out_trace_npts}     {cfg.out_trace_dt}\n\
* the indexes of reference ray among 1 -- nw: ninw, (inw0(i),i=1,ninw)   \n\
{cfg.nw_pair}\n\
* minimum YBIN (km)\n\
{cfg.minYbin}\n\
* DYBIN (km)\n\
{cfg.Dybin}\n\
* maximum YBIN (km)\n\
{cfg.maxYbin}\n\
*temporary directory name to store the intermedial files (.img)\n\
{cfg.tmpdir}\n\
* moveout index: idist, gcarc1  (only useful for idist=1)\n\
{cfg.moveout_flag}  {cfg.moveout_gcarc}\n\
* inorm\n\
{cfg.norm_flag} \n\
* output number and depth indexes in ninw: noutd,(ioutd(i),i=1,noutd)\n\
{cfg._ninw}\n\
* output index for stacking: istack\n\
{cfg.stack_flag} \n\
* output index for gcarc, baz and p: ioutb\n\
{cfg.ioutb}\n\
* piercing point data file number: npief\n\
{cfg.npief}\n\
* input file name: infile\n\
{cfg.binr_out_name}\n"


def _str_hdpming(cfg):
    return \
f"* imethod (phshift=0; phscreen=1, hybscreen: else),irefvel,vscale \n\
{cfg.imethod}      {cfg.irefvel}     {cfg.vscale}\n\
* fmin, fmax (Minimum and maximum frequencies), ifreqindl, ifreqindr\n\
{cfg.fmin}    {cfg.fmax}    {cfg.ifreqindl}    {cfg.ifreqindr}\n\
* nxmod, nzmod, nx, nz\n\
{cfg.nxmod}    {cfg.nzmod}   {cfg.nx}     {cfg.nz}\n\
* dx, dz\n\
{cfg.dx}   {cfg.dz}\n\
* ntrace, nt, dt (in sec.), nt0, ntb\n\
{cfg.ntrace}    {cfg.nt}    {cfg.dt}    {cfg.nt0}    {cfg.ntb}\n\
* FD method (15, 45, 65)\n\
{cfg._FD}\n\
* nxleft, nxright\n\
{cfg.nxleft}    {cfg.nxright}\n\
* ifmat (=0: ascii vel. file; else: binary vel. file)\n\
{cfg.ifmat}\n\
* modvelocity\n\
{cfg.velmod}\n\
* tx_data (input seismic data)\n\
{cfg.tx_data}\n\
* migdata (output imaging data)\n\
{cfg.migdata}\n\
* intrace\n\
{cfg.intrace}\n\
* first trace index: itrfirst\n\
{cfg.itrfirst}\n"
