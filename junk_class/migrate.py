"""
偏移成像的方法
"""

from os.path import join, isfile
from cfgPSDM import cfg_Hdpmig
from init import path2PSDM
from subprocess import Popen, PIPE
from util import _str_hdpming, gen2pow, isAsciiVelmod


class hdpming(cfg_Hdpmig):
    def check(self, gen2=False):
        # 检查道数是否相等
        if self.nxmod != self.ntrace:
            raise ValueError("nxmod must be equal to ntrace")
        # 有两个参数需要做傅里叶变换，这里的*2 是为了与示例结果中的情况保持一致
        if gen2:
            self.nt0 = gen2pow(self.nt) * 2
            self.nx = gen2pow(self.nxmod) * 2
        if self.ifmat == 0:
            isAsciiVelmod(self.velmod, join(path2PSDM, "poststack"))

    def run(self):
        cmd = join(path2PSDM, "poststack", "hdpming.x")

        proc0 = Popen(
            cmd,
            stdin=None,
            stdout=PIPE,
            stderr=PIPE,
            shell=True)
        outinfo02, errinfo02 = proc0.communicate()

    @property
    def FD(self):
        return self._FD

    @property.setter
    def FD(self, value):
        if value not in [15, 45, 65]:
            raise ValueError("FD value must be 15, 45 or 65")
        else:
            self._FD = value

    def __str__(self):
        return _str_hdpming(self)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
