# shell4PSDM

使用python 作为shell 调用 陈凌老师的PSDM程序，感谢陈凌与王旭老师的整理与分享。

提供了以下功能：

* psdm的shell调用
* 将 psdm 输出的二进制文件转换为 gmt 能识别的文本文件与 grd 文件
* 与 Lupei Zhu 的 CCP 叠加程序联动

基本文件

* `run_demo`：用于跑王旭博士提供的示例数据，用于展示 shell4PSDM 的炒作流程
* `cfgPSDM`，规定了参数文件的各个方面，包括一定的注释
* `velmod`，提供了一些用于将`tvel`格式与传统格式的速度结构转换为PSDM格式的速度结构 的方法

环境需求：

* python>3.9
* numpy，matplotlib，netCDF4

未来计划：

如果未来还在这行干，应该会做的一些改进：

* 将深度相关的几个变量写个类，目前缺少个比较方便的迭代方法
