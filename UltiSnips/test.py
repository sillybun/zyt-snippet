import logging
logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.DEBUG)

logging.debug("this is for debug")
logging.info()
logging.warning()
logging.error()
logging.critical()
