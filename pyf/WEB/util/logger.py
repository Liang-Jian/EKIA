import logging
import logging.handlers
import os
# from config.VarConfig import parentDirPath


def logconfig():

    logger = logging.getLogger("UI")
    # 全局默认级别WARNING
    logger.setLevel(logging.DEBUG)

    # 生成Handler对象
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    fh = logging.FileHandler(parentDirPath + "//log//log.txt", encoding="utf8")
    fh.setLevel(logging.DEBUG)

    # 生成formatter对象
    # 把formatter对象 绑定到Handler对象
    file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s %(message)s")
    console_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # console_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s")
    ch.setFormatter(console_formatter)
    fh.setFormatter(file_formatter)

    # 把Handler对象 绑定到logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger

log = logconfig()

def logger_debug(msg):
    log.debug(msg)

def logger_info(msg):
    log.info(msg)

def logger_warning(msg):
    log.warning(msg)

def logger_error(msg):
    log.error(msg)

def logger_critical(msg):
    log.critical(msg)

# if __name__ == '__main__':
#     logger_debug("logger_debug")
#     logger_info("logger_info")
#     logger_warning("logger_warning")
#     logger_error("logger_error")
#     logger_critical("logger_critical")

