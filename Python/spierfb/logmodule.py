import logging
import logging.handlers

def logConfig():

    logger = logging.getLogger("joker")
    logger.setLevel(logging.DEBUG)                      # 全局默认级别WARNING
    ch = logging.StreamHandler()                        # 生成Handler对象
    ch.setLevel(logging.DEBUG)
    # fh = logging.FileHandler("./" + "//log//log.txt", encoding="utf8")
    fh = logging.FileHandler("../log.log", encoding="utf8")
    fh.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s %(message)s")# 把formatter对象 绑定到Handler对象
    console_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(console_formatter)
    fh.setFormatter(file_formatter)
    logger.addHandler(ch)                               # 把Handler对象 绑定到logger
    logger.addHandler(fh)
    return logger

log = logConfig()

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