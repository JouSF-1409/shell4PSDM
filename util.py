"""
提供一些辅助功能，一个垃圾桶
isAsciiVelmod(): 简单分析是否为所需的五列速度模型
get_datalist(): 生成datalist.txt文件，get_datalist.sh的替代品
genRayPath(): 生成转换波位置文件
matchLayerDepth(): 读取速度模型文件，返回深度对应的层号
gen2pow(): 生成离给定整数最近的，2的幂次方数
"""

from os import listdir
from os.path import join, isfile, isdir
from glob import glob
from pathlib import Path

from numpy import power


from init import path2PSDM
#from m660q import m660q
#from stack import pierc_new_n, binr_vary_scan_n
#from migrate import hdpming

def gen2pow(n:int):
    rate=0
    while(power(2,rate)<n):
        rate+=1
    return power(2,rate)

def matchLayerDepth(url:str, Layers:list):
    """
    读取速度模型文件，返回深度对应的层号
    range 的逻辑有一定问题
    """
    l = open(url).readlines()
    Layers.sort()
    depth = 0
    vis=[];vi=1
    for _i in range(len(depth)):
        
        while(depth[_i]<depth):
            # 排除空行和第一行
            if l[_i].strip() == "":
                _i+=1
                continue
            if len(l[_i].strip().split()) == 1:
                _i+=1
                continue
            depth+=float(l[vi].strip().split()[3])
            vi+=1
        vis.append(vi)
    if len(vis) != len(Layers):
        raise ValueError("depth can not be found in ref_model. might be too deep to search")
    l.close()
    return vis


def genRayPath(rayFile,nLayers,phase='Ps'):
    """
    生成射线参数文件
    考虑到逻辑的复杂性，这里强制将结果保存到 PSDM 里的m660q目录
    并且会强制覆盖同名文件，注意备份
    Phase只能为 Ps 或 Sp， 使用了异或
    这里的行数依然不确定怎么对应。看得头晕眼花的
    """
    if phase not in ['Ps','Sp']:
        raise ValueError("phase must be Ps or Sp")
    rayFile = join(path2PSDM, "m660q", rayFile)
    if isfile(rayFile):
        print(f"rayp file {rayFile} exists, will be overwritten")

    try:
        rayfile=open(rayFile,'w')

        print(nLayers, file=rayfile)
        for cc_n in range(0, nLayers):
            str_idx = ("%2d " % nLayers)
            str_flg = '   '
            for ii in range(nLayers, 0, -1):
                str_idx += ("%2d" % ii)
                if (ii <= cc_n ^ phase == 'Sp'):
                    str_flg += ("%2d" % 3)
                else:
                    str_flg += ("%2d" % 5)
            print(str_idx, file=rayfile)
            # print(str_idx)
            print(str_flg, file=rayfile)
        rayfile.close()
    except:
        raise IOError(f"file {rayFile} can not be written")

def retryPath(url:str, funcDir=None):
    if not isfile(url) :
        if (funcDir is None) and (not isfile(join(funcDir, url))):
            raise FileNotFoundError(f"file {url} not found")
        else:
            url = join(funcDir, url)
    return url

def isAsciiVelmod(url:str, cor=4,funcDir=None):
    """
    路径的有效性需要靠调用者保证
    这里只考虑绝对路径与相对路径的情况

    如果mainfunc不给出，只检查绝对路径。
    同时，速度模型只做数量上的检查，不做物理或数值上的检查。

    PSDM有两种速度模型，一种是五列的，一种是四列的。
    区别在于第五列，即层数列。
    速度模型的形式如下：
    # 层数
    # vp      # vs     # 密度     # 层厚     # 深度  # 第几层
    -----------------------------------------------------------
        82
    3.000     1.800     2.300     1.600       1.6       1
    4.700     2.800     2.600     2.700       4.3       2

    >>> path2PSDM = 'D:\project\chen_rfunc'
    >>> isAsciiVelmod("cwbq",funcDir=join(path2PSDM, "m660q"))
    True
    """

    url = retryPath(url, funcDir)

    try:
        l=open(url, "r")
        lines = l.readlines()
        nline = int(lines[0].strip())+1
        # remove empty lines
        while not lines[-1].strip():
            lines.pop()
        if len(lines) != nline:
            raise IOError(f"file {url} is not a valid velocity model")

        for _i in lines[1:]:
            if len(_i.split()) < cor:
                raise IOError(f"file {url} has no enough columns")

        l.close()
    except:
        raise IOError(f"file {url} is not a valid velocity model")
    return True

def get_datalist(path:str, match_rule='*.eqr'):
    """
    一个非常简单的，get_datalist.sh替代品
    主要是不想写py 调用shell，文件夹太乱
    """
    if not isdir(path):
        path = join(path2PSDM,path)
        if not isdir(path):
            raise FileNotFoundError(f"rf directory {path} not found")

    l = open(join(path, "datalist.txt"), "w")
    # then we find the rf dir

    # 这段 纯炫技， 目前没有比较好的方法只遍历文件夹，不遍历文件夹的内容。
    # 考虑到文件的数量可能会比较多，listdir 未来可能会改为迭代器
    #subdirs = [d for d in listdir(path) if isdir(join(path, d))]
    subdirs = [ d for d in Path(path).iterdir() if d.is_dir()]
    print(subdirs)
    for subdir in subdirs:
        eqr_files = glob(join(path, subdir, match_rule))

        # f-string 有一定的约束
        tmp = "{}\n{}\n{}\n".format(
            subdir,
            len(eqr_files),
            "\n".join([Path(f).name for f in eqr_files])
        )
        l.write(tmp)
    l.close()

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
{cfg.nw}\n\
* NDW(1:5): indexs in NWI for outputting piercing points at 5 depths\n\
{cfg.ndw}\n\
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
{cfg.Profile_len}, {cfg.az_min}, {cfg.az_maz}, {cfg.az_step}\n\
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
{cfg.ninw}\n\
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
{cfg.FD}\n\
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

if __name__ == '__main__':
    import doctest
    doctest.testmod()