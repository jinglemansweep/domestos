import logging

def LogSetup(name, format_string, datestamp_string):
    logger = logging.getLogger(name)
    logger.handlers = []
    formatter = logging.Formatter("%s " % format_string, datestamp_string)
    file_hdlr = logging.FileHandler("%s.log" % name)
    file_hdlr.setFormatter(formatter)
    stdout_hdlr = logging.StreamHandler()
    stdout_hdlr.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_hdlr)
    logger.addHandler(stdout_hdlr)
    return logger
