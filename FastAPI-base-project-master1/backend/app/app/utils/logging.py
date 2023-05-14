import logging


def lprint(*msg, sep=" ", context="\t "):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(context)
    logging.info(sep.join(map(str, msg)))