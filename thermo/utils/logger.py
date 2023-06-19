import logging

ml_logger = logging.getLogger(__name__)

handler = logging.StreamHandler()

# the formatter determines what our logs will look like
fmt = "%(levelname)s  \t %(message)s \t in file: %(filename)s, function: %(funcName)s"
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)

ml_logger.addHandler(handler)
ml_logger.setLevel(logging.DEBUG)
