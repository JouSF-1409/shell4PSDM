
from init import path2PSDM
from cfgPSDM import cfg_m660q


class m660q(cfg_m660q):


    def __str__(self):
        return \
f"* velocity model file\n\
{self.ref_model}\n\
* ray file\n\
{self.ray}\n\
* output file\n\
{self.m660q_out}\n\
* iflat, itype (= 0: free-surface refl.; else: conversion (>0: Ps; <0: Sp))\n\
{self.iflat:01d}     {self.itype:01d}\n\
\n\
"


if __name__ == "__main__":
    l = m660q()
    print(l.__str__())