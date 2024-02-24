"""
整个代码运行的逻辑，修改配置参数时的模板
"""

def modi(cfg,
         modifier: dict):
    """
    修改cfg文件的逻辑，
    使用setattr 对配置文件进行修改
    """
    for key, value in modifier.items():
        if hasattr(cfg, key):
            setattr(cfg, key, value)
        else:
            raise AttributeError(f"cfg has no attribute {key}")

    # 所有的类使用check 方法对配置参数进行检查
    # 使用run 方法运行，move 方法备份运行结果
    cfg.check()
    cfg.run()
    cfg.move()
    return cfg

# if __name__ == "__main__":
