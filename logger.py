import logging
import logging.handlers
from datetime import datetime

class Logger:

    def __init__(self):
        LOG_FILENAME = 'logs/simplavortaro.log'

        # Set up a specific logger with our desired output level
        self.logger = logging.getLogger('Simpla Vortaro Logger')
        self.logger.setLevel(logging.DEBUG)

        # Add the log message handler to the logger
        # (logs are up to 50 MiB)
        handler = logging.handlers.RotatingFileHandler(
            LOG_FILENAME, maxBytes=5*1000*1000, backupCount=10)
        self.logger.addHandler(handler)

    @staticmethod
    def get_time():
        return datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f')

    def log_search(self, word, ip):
        self.logger.info('%s Searched word: "%s" IP: %s' %
                         (self.get_time(), word, ip))

    def log_view_word(self, word, ip):
        self.logger.info('%s Viewed word: "%s" IP: %s' % 
                         (self.get_time(), word, ip))
        
