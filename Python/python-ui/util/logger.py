import logging
import logging.handlers
import os
# from config.VarConfig import parentDirPath



parentDirPath = os.path.abspath('..')

def logconfig():

    logger = logging.getLogger("LX")
    # 全局默认级别WARNING
    logger.setLevel(logging.DEBUG)

    # 生成Handler对象
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    fh = logging.FileHandler(parentDirPath + "\\log\\log.txt", encoding="utf8")
    fh.setLevel(logging.DEBUG)

    # 生成formatter对象
    # 把formatter对象 绑定到Handler对象
    file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s %(message)s")
    console_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(console_formatter)
    fh.setFormatter(file_formatter)

    # 把Handler对象 绑定到logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger

log = logconfig()

def Logd(msg):
    log.debug(msg)

def Logi(msg):
    log.info(msg)

def Logw(msg):
    log.warning(msg)

def Loge(msg):
    log.error(msg)

def Logc(msg):
    log.critical(msg)


