"""
偏移成像的方法
"""

from cfgPSDM import cfg_Hdpmig
class hdpming(cfg_Hdpmig):
    def __str__(self):
        return \
f"* imethod (phshift=0; phscreen=1, hybscreen: else),irefvel,vscale \n\
{self.imethod}      {self.irefvel}     {self.vscale}\n\
* fmin, fmax (Minimum and maximum frequencies), ifreqindl, ifreqindr\n\
{self.fmin}    {self.fmax}    {self.ifreqindl}    {self.ifreqindr}\n\
* nxmod, nzmod, nx, nz\n\
{self.nxmod}    {self.nzmod}   {self.nx}     {self.nz}\n\
* dx, dz\n\
{self.dx}   {self.dz}\n\
* ntrace, nt, dt (in sec.), nt0, ntb\n\
{self.ntrace}    {self.nt}    {self.dt}    {self.nt0}    {self.ntb}\n\
* FD method (15, 45, 65)\n\
{self.FD}\n\
* nxleft, nxright\n\
{self.nxleft}    {self.nxright}\n\
* ifmat (=0: ascii vel. file; else: binary vel. file)\n\
{self.ifmat}\n\
* modvelocity\n\
{self.velmod}\n\
* tx_data (input seismic data)\n\
{self.tx_data}\n\
* migdata (output imaging data)\n\
{self.migdata}\n\
* intrace\n\
{self.intrace}\n\
* first trace index: itrfirst\n\
{self.itrfirst}\n"