import logging

def setup_logging(filename):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    tf = logging.Formatter(fmt='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')

    fh = logging.FileHandler(filename, mode='w')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(tf)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(tf)
    logger.addHandler(ch)

    return logger
    
