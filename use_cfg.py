import configparser
from os.path import expanduser

class PlotPara(object):
    def __init__(self):
        self.mainpath = expanduser('~')
        self.stacked_field = expanduser('~')
        self.yb_file = expanduser('~')
        self.num_file = expanduser('~')
        self.pro_xy_file = expanduser('~')
        self.stalst_file = expanduser('~')
        self.filename = expanduser('~')
        self.xlenp = 1000  
        self.npt = 1001
        self.dt = 0.1
        self.depth = 800 
        self.dz = 0.5
        self.dx = 50
        self.noutd = 5

    @classmethod
    def read_para(cls, cfg_file):
        cf = configparser.RawConfigParser(allow_no_value=True)
        pa = cls()
        try:
            cf.read(cfg_file)
        except Exception:
            raise FileNotFoundError('Cannot open configure file %s' % cfg_file)
        sections = cf.sections()
        for key, value in cf.items('path'):
            if value == '':
                continue
            elif key == 'mainpath':
                pa.mainpath = value
            elif key == 'stacked_field':
                pa.stacked_field = value
            elif key == 'yb_file':
                pa.yb_file = value
            elif key == 'num_file':
                pa.num_file = value
            elif key == 'pro_xy_file':
                pa.pro_xy_file = value
            elif key == 'stalst_file':
                pa.stalst_file = value
            elif key == 'filename':
                pa.filename = value
            else:
                pa.__dict__[key] = value
        sections.remove('path')
        for key, value in cf.items('input_para'):
            if value == '':
                continue
            elif key == 'xlenp':
                pa.xlenp = value
            elif key == 'npt':
                pa.npt = value
            elif key == 'dt':
                pa.dt = value
            elif key == 'depth':
                pa.depth = value
            elif key == 'dz':
                pa.dz = value
            elif key == 'dx':
                pa.dx = value
            elif key == 'noutd':
                pa.noutd = value
            else:
                pa.__dict__[key] = value
        return pa

if __name__ == '__main__':
    cfg_file = 'plot.cfg'
    para = PlotPara.read_para(cfg_file)
    print(para)
    print(para.stacked_field)
    print(para.noutd)