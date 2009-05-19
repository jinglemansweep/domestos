import logging

def LogSetup(name, format_string, datestamp_string, level="DEBUG"):
    logger = logging.getLogger(name)
    logger.handlers = []
    formatter = logging.Formatter("%s " % format_string, datestamp_string)
    file_hdlr = logging.FileHandler("%s.log" % name)
    file_hdlr.setFormatter(formatter)
    stdout_hdlr = logging.StreamHandler()
    stdout_hdlr.setFormatter(formatter)
    if level == "DEBUG":
        logger.setLevel(logging.DEBUG)
    if level == "INFO":
        logger.setLevel(logging.INFO)
    if level == "WARNING":
        logger.setLevel(logging.WARNING)
    if level == "ERROR":
        logger.setLevel(logging.ERROR)
    logger.addHandler(file_hdlr)
    logger.addHandler(stdout_hdlr)
    return logger
