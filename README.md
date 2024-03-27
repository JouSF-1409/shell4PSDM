# shell4PSDM

使用python 作为shell 程序调用 陈凌老师 的PSDM程序。

目的是提供一个批量处理，准确回顾，有充足空间写注释的调用环境

如果要采用不同类型的速度结构，`velmod.py`中提供了一定的方法用于将`tvel`格式与传统格式的速度结构转换为PSDM格式的速度结构。
但需要用户手动修改配置参数中的速度文件路径

文件结构：

* `boot`：抽象的运行逻辑。包括写、备份参数文件，根据运行的方法写配置方法。
* `cfg_history`，供参考的参数列表
* `cfgPSDM`，规定了参数文件的各个方面，包括一定的注释
* `velmod`，提供了一些用于将`tvel`格式与传统格式的速度结构转换为PSDM格式的速度结构 的方法
* `junk_class`,一些失败的尝试

运行逻辑：

参考`example`的用法。

推荐用户以字典的形式存储修改的参数，
然后调用`boot`中的方法进行调用。