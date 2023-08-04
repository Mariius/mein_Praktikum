import logging

class LogExample():
    def __init__(self, logger=None, log_concept=True, log_file=None):
        if log_concept:
            self._log = logger or logging.getLogger()
        else:
            self._log = logger or logging.getLogger('logex')
        self._log.setLevel(logging.INFO)
            
        # own logging concept
        if log_concept:
            # basic console logger: receives messages too
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)

            # additionally, log to file
            if log_file != None:
                logFileName = log_file
                fileLog = logging.FileHandler(logFileName, 'w', 'utf-8')
                fileLog.setLevel(logging.INFO)

            # create formatter and add it to the handlers
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch.setFormatter(formatter)
            if log_file != None:
                fileLog.setFormatter(formatter)

            # add the handlers to the logger
            self._log.addHandler(ch)
            if log_file != None:
                self._log.addHandler(fileLog)
                self._log.info("Write log into file '{}'.".format(log_file)) 
                
    def test(self):
        self._log.info("Test")


if __name__ == '__main__':
    logex = LogExample()
    logex.test()
