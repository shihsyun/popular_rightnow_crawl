from fake_useragent import UserAgent
from fake_useragent import FakeUserAgentError
import logging
from logging.handlers import RotatingFileHandler


def main():

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    log_file_handler = RotatingFileHandler('/tmp/fake_useragent.log', maxBytes=1024**2, encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s')
    log_file_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(log_file_handler)
    logging.info('fake_useragent fetch data now.....')

    try:
        ua = UserAgent()
        ua.update()
    except FakeUserAgentError as e:
        logging.error('fake_useragent fetch data fail, Exception occured: %s' %e , exc_info=True)


if __name__== "__main__":
    main()                             
