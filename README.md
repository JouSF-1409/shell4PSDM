# shell4PSDM

使用python 写的PSDM脚本调用，目的是一个更好的，适用于批量处理的PSDM脚本调用。

目前的组织逻辑：

* `init.py`:规定全局变量，包括PSDM程序目录
* `runMethod.py`:规定运行逻辑，并实际调用
* `plotPSDM.py`：未来可能分拆，PSDM相关的画图功能
* `cfgPSDM`: 目前只是规定了配置文件的默认值和数值类型，写了一个比较完善的注释说明，具体的实现和输出要看对应类的`__str__`等方法

