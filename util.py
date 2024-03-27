"""
提供一些辅助功能，一个垃圾桶
get_datalist(): 生成datalist.txt文件，get_datalist.sh的替代品
genRayPath(): 生成转换波位置文件
matchLayerDepth(): 读取速度模型文件，返回深度对应的层号
gen2pow(): 生成离给定整数最近的，2的幂次方数
get_datalist(): 最简单的， get_datalist.sh的替代品
"""
from datetime import datetime
from os.path import join, isfile, isdir, exists
from glob import glob
from pathlib import Path
from shutil import copy
import subprocess

from numpy import power

from cfgPSDM import cfg_m660q, cfg_Pierce_new_n, cfg_binr_vary_scan_n, cfg_Hdpmig

def paser_flesh(path2PSDM:str):
    """
    检查各路径和文件是否存在并成立
    """
    bins=["binr_vary_scan_n","hdpmig.x","M660q_model","pierc_new_n"]
    psdm_bin = join(path2PSDM, "bin")
    psdm_default_cfg = join(path2PSDM, "model")
    psdm_cfg_history = join(path2PSDM, "history")
    psdm_trans = join(path2PSDM,'trans')
    psdm_tmp = join(path2PSDM, 'tmp')
    bins = [join(psdm_bin, _i) for _i in bins]
    for _i in bins:
        if not isfile(_i):
            raise FileNotFoundError("plz make all before run psdm")
    for _i in (psdm_cfg_history, psdm_tmp, psdm_trans):
        if not exists(_i):
            Path(_i).mkdir(exist_ok=True)

def paser_backup(path2PSDM:str):
    """
    备份生成的所有文件
    """

path2PSDM=""
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


def retryPath(url:str, funcDir=None):
    if not isfile(url) :
        if (funcDir is None) and (not isfile(join(funcDir, url))):
            raise FileNotFoundError(f"file {url} not found")
        else:
            url = join(funcDir, url)
    return url


def set_new_cfg(path2cfg, cfg):
    """
    写新cfg 的时候，将已经存在的cfg备份为 文件名+时间+.bac的格式
    """
    if exists(path2cfg):
        print(f"{path2cfg} exist, backup and write a new one")
        copy(path2cfg,
             f"{path2cfg}.{datetime.now().strftime('%Y.%m.%d')}.bac")
    f = open(path2cfg, 'w')
    f.write(cfg.__str__())
    f.close()

def runner_psdm_dict(path2PSDM, base_cfg, changes:dict):
    """
    规定需要 psdm 的路径情况，
    基础的cfg， 对cfg 的某种改动
    """

    if not isinstance(base_cfg,(cfg_m660q,cfg_Pierce_new_n,cfg_binr_vary_scan_n,cfg_Pierce_new_n)):
        raise TypeError("base_cfg should be at least one in cfgPSDM")
    # set changes
    for _i,_j in changes:
        setattr(base_cfg, _i, _j)
    runner_psdm(path2PSDM, base_cfg)


def runner_psdm(path2PSDM, base_cfg,stamp="junk"):
    """
    保存配置文件，运行，并备份配置文件
    stamp 一般为 剖面名+程序运行的时间。但这里开放自定义
    """
    # save changes and run
    if isinstance(base_cfg,cfg_m660q):
        path2cfg = join(path2PSDM,'bin',"m660q_model.in")
        cmd = join(path2PSDM,'bin','M660q_model')
    elif isinstance(base_cfg, cfg_Pierce_new_n):
        path2cfg = join(path2PSDM,'bin','pierc_new_n.in')
        cmd = join(path2PSDM,'bin','pierc_new_n')
    elif isinstance(base_cfg, cfg_binr_vary_scan_n):
        path2cfg = join(path2PSDM,'bin','binr_vary_scan_n.inp')
        cmd = join(path2PSDM,'bin','binr_vary_scan_n')
    elif isinstance(base_cfg, cfg_Hdpmig):
        path2cfg = join(path2PSDM,'bin','hdpmig.in')
        cmd = join(path2PSDM,'bin','hdpmig.x')
    else:
        raise ValueError("not a valid cfg class")

    set_new_cfg(path2cfg, base_cfg)
    subprocess.call([cmd],cwd=join(path2PSDM,'bin'))

    copy(
        path2cfg,
        f"{path2cfg}_{stamp}"
    )