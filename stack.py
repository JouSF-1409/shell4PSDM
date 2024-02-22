"""
包含了两类函数的调用，
1. pierc_new_n
2. binr_vary_scan_n
"""
from glob import glob
from os import listdir
from os.path import isdir,join
from pathlib import Path

from init import path2PSDM
from cfgPSDM import cfg_Pierce_new_n, cfg_binr_vary_scan_n

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
    subdirs = [d for d in listdir(path) if isdir(join(path, d))]
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



class pierc_new_n(cfg_Pierce_new_n):
    def __str__(self):
        return \
f"* output file name: iaj\n\
{self.pierc_out}\n\
* the coordinate center of line: evla0,evlo0\n\
{self.center_la:.1f}, {self.center_lo:.1f}\n\
 * output time point number: np0, irayp\n\
{self.out_npts}      {self.sac_user_num_rayp}\n\
* model file\n\
{self.ref_model}\n\
* * ivar (0: dist; 1: gcarc; 2: baz),varmin,varmax\n\
{self.event_filt_flag}     {self.event_filt_min}     {self.event_filt_max}\n\
* NW,(NWI(I),NWID(I),I=1,NW)\n\
{self.nw}\n\
* NDW(1:5): indexs in NWI for outputting piercing points at 5 depths\n\
{self.ndw}\n\
* directory containing RFs\n\
{self.rfdata_path}\n\
* number of subdirectories\n\
{self.num_sub}\n\
{self.name_sub}\n\
{self.name_lst}\n\
\n"

class binr_vary_scan_n(cfg_binr_vary_scan_n):
    def __str__(self):
        return \
f"* begin and end coordinate of start point, point interval(km): begla0,beglo0,endla0,endlo0,dsp\n\
{self.Descar_la_begin},{self.Descar_lo_begin},{self.Descar_la_end},{self.Descar_lo_end},{self.Descar_step}\n\
* profile length and azimuth range and interval: xlenp,alphab,alphae,dalp\n\
{self.Profile_len}, {self.az_min}, {self.az_maz}, {self.az_step}\n\
* the spacing between bins, least number of traces, rnumtra, UTM_PROJECTION_ZONE(new)\n\
{self.bins_step}     {self.trace_num_min}      {self.ratio_trace}      {self.UTM_zone}\n\
* time file name: timefile\n\
{self.timefile}\n\
* output file name: outfile\n\
{self.outpufile}\n\
* ouput number of time samples in each trace: npt, dt\n\
{self.out_trace_npts}     {self.out_trace_dt}\n\
* the indexes of reference ray among 1 -- nw: ninw, (inw0(i),i=1,ninw)   \n\
{self.nw_pair}\n\
* minimum YBIN (km)\n\
{self.minYbin}\n\
* DYBIN (km)\n\
{self.Dybin}\n\
* maximum YBIN (km)\n\
{self.maxYbin}\n\
*temporary directory name to store the intermedial files (.img)\n\
{self.tmpdir}\n\
* moveout index: idist, gcarc1  (only useful for idist=1)\n\
{self.moveout_flag}  {self.moveout_gcarc}\n\
* inorm\n\
{self.norm_flag} \n\
* output number and depth indexes in ninw: noutd,(ioutd(i),i=1,noutd)\n\
{self.ninw}\n\
* output index for stacking: istack\n\
{self.stack_flag} \n\
* output index for gcarc, baz and p: ioutb\n\
{self.ioutb}\n\
* piercing point data file number: npief\n\
{self.npief}\n\
* input file name: infile\n\
{self.binr_out_name}\n"

    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    get_datalist("D:/project/chen_rfunc/data/f2p5_dt01_s1")
    #print(pierc_new_n())