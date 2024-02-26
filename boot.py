"""
这里规定了整个代码的运行逻辑，
以及PSDM 程序库的位置
"""
from os.path import join,isfile,exists,expanduser, isdir
from pathlib import Path
from glob import glob
from shutil import copy
from datetime import datetime
from subprocess import Popen, PIPE


#from init  import path2PSDM
from cfgPSDM import cfg_m660q, cfg_Pierce_new_n, cfg_Hdpmig, cfg_binr_vary_scan_n




path2PSDM=join(expanduser("~"),"src/chen_rfunc")

def set_new_cfg(path2cfg, cfg):
    if exists(path2cfg):
        print(f"{path2cfg} exist, backup and write a new one")
        copy(path2cfg,
             f"{path2cfg}.{datetime.isoformat()}.bac")
    with open(path2cfg) as f:
        f.write(
            cfg.__str__()
        )

def runner_psdm(path2PSDM, base_cfg, changes:dict):
    """
    规定需要 psdm 的路径情况，
    基础的cfg， 对cfg 的某种改动，
    尽可能简短ifelse 的距离和逻辑理解的难度吧
    """

    if not isinstance(base_cfg,(cfg_m660q,cfg_Pierce_new_n,cfg_binr_vary_scan_n,cfg_Pierce_new_n)):
        raise TypeError("base_cfg should be at least one in cfgPSDM")
    # set changes
    for _i,_j in changes:
        setattr(base_cfg, _i, _j)
    # save changes and run
    if isinstance(base_cfg,cfg_m660q):
        path2cfg = join(path2PSDM,'m660q',"m660q_model.in")
        cmd = join(path2PSDM,'m660q','M660q_model')
    elif isinstance(base_cfg, cfg_Pierce_new_n):
        path2cfg = join(path2PSDM,'stack','pierc_new_n.in')
        cmd = join(path2PSDM,'stack','pierc_new_n')
    elif isinstance(base_cfg, cfg_binr_vary_scan_n):
        path2cfg = join(path2PSDM,'stack','binr_vary_scan_n.inp')
        cmd = join(path2PSDM,'stack','binr_vary_scan_n')
    else:
        path2cfg = join(path2PSDM,'poststack','hdpmig.in')
        cmd = join(path2PSDM,'poststack','hdpmig.x')

    set_new_cfg(path2cfg, base_cfg)

    proc0 = Popen(
        cmd,
        stdin=None,
        stdout=PIPE,
        stderr=PIPE,
        shell=True)
    outinfo02, errinfo02 = proc0.communicate()

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


# if __name__ == "__main__":
