import logging
import os
from datetime import datetime

class Logger:
    def __init__(self):
        # Create logs directory if it doesn't exist
        self.base_log_dir = 'logs'
        if not os.path.exists(self.base_log_dir):
            os.makedirs(self.base_log_dir)
        
        # Create timestamp folder
        self.timestamp = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
        self.log_dir = os.path.join(self.base_log_dir, self.timestamp)
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        # Set up logging
        self.log_file = os.path.join(self.log_dir, 'download_log.txt')
        
        # Configure logger
        self.logger = logging.getLogger('CardDownloader')
        self.logger.setLevel(logging.DEBUG)
        
        # Create file handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', 
                                    datefmt='%m/%d/%Y %H:%M:%S.%f')
        
        # Add formatter to handlers
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message):
        self.logger.info(message)
    
    def error(self, message):
        self.logger.error(message)
    
    def debug(self, message):
        self.logger.debug(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def get_log_dir(self):
        return self.log_dir
