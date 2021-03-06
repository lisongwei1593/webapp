import logging
import os
from logging.handlers import TimedRotatingFileHandler

from webapp.settings import BASE_DIR

wx_pay_log = logging.getLogger('wx_apy')
if len(wx_pay_log.handlers) == 0:
    level = logging.DEBUG
    # filename='d:\\project\\source\\test1\\stars\\logs\\log.txt'
    filename = BASE_DIR+'/logs/fin/wx_pay_log.txt'
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    hdlr = TimedRotatingFileHandler(filename,"midnight",1)
    format = '%(asctime)s %(levelname)s %(module)s.%(funcName)s Line:%(lineno)d%(message)s'
    fmt = logging.Formatter(format)
    hdlr.setFormatter(fmt)

    wx_pay_log.addHandler(hdlr)
    wx_pay_log.setLevel(level)

    logging.Handler().flush()