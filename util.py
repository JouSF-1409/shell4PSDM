"""
提供一些辅助功能
isAsciiVelmod(): 简单分析是否为所需的五列速度模型
"""

from os.path import join, isfile

from init import path2PSDM

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

if __name__ == '__main__':
    import doctest
    doctest.testmod()