"""
为PSDM 写的配置文件，目标是一个更好用，能用于

"""

from os.path import join,expanduser

path2PSDM=join(expanduser("~"),"src/chen_rfunc")

if __name__ == "__main__":
    print(path2PSDM)