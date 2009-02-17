import logging

def logsetup():
    logger = logging.getLogger("domestos")
    logger.handlers = []
    formatter = logging.Formatter('[%(asctime)s] %(module)s\t%(levelname)-8s%(message)s', '%Y-%m-%d %H:%M:%S',)
    file_hdlr = logging.FileHandler("domestos.log")
    file_hdlr.setFormatter(formatter)
    stdout_hdlr = logging.StreamHandler()
    stdout_hdlr.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_hdlr)
    logger.addHandler(stdout_hdlr)
    return logger