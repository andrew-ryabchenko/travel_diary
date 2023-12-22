import logging
from logging.handlers import RotatingFileHandler

# Create a logger
logger = logging.getLogger('failed_login')
logger.setLevel(logging.DEBUG)  # Set the logging level

# Create a handler that writes log messages to a file, with rotation
log_file = 'failed_logins.txt'
handler = RotatingFileHandler(log_file, maxBytes=1024*1024*5, backupCount=3) # 5MB per file, 3 backups
handler.setLevel(logging.DEBUG)

# Create a formatter and set it for the handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(ip)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

if __name__ == "__main__":
    # Example logging messages
    logger.debug('This is a debug message', extra = {"ip": "127.0.0.1"})
