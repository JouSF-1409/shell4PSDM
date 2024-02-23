from subprocess import Popen, PIPE
from os.path import isfile,join, exists

from init import path2PSDM
from cfgPSDM import cfg_m660q
from util import isAsciiVelmod, retryPath


from obspy.core import UTCDateTime

from util import _str_m660q, isAsciiVelmod, retryPath


class m660q(cfg_m660q):
    def check(self):
        isAsciiVelmod(self.ref_model)
        if not isfile(join(path2PSDM, "m660q", "M660q_model")):
            raise FileNotFoundError("make m660q model first")
    def run(self):
        # 写入配置文件
        l = open(join(path2PSDM, "m660q", "M660q_model.in"), "w")
        l.write(self.__str__())
        l.close()
        # 调用抄自张周，未经测试
        cmd = join(path2PSDM, "m660q", "M660q_model")
        proc0 = Popen(
                        cmd,
                        stdin=None,
                        stdout=PIPE,
                        stderr=PIPE,
                        shell=True)
        outinfo02, errinfo02 = proc0.communicate()

    def __str__(self):
        return _str_m660q(self)

    def gen(self):
        if not exists(self.ref_model):
            raise FileNotFoundError(f"ref_model file {self.ref_model} not found")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    a = m660q()
    print(a.__str__())