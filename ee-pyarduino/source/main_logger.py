import os
import logging
from datetime import datetime

from source.file_handle import create_folder_if_not_exist

log_folder = 'log'
   
# create path for logs (if not exist)
create_folder_if_not_exist(log_folder)

# Setup logging concept
# configure default logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# basic console logger: receives INFO messages too
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# addtionally, log to file on every HIL application start
log_file_name = datetime.now().strftime('%Y%m%d_%H%M%S') + '_one_wire.log'
file_log = logging.FileHandler(os.path.join(log_folder, log_file_name), 'w', 'utf-8')
# set level of file log
file_log.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
file_log.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(ch)
logger.addHandler(file_log)

## Start test system
logger.info('Start main logging concept')