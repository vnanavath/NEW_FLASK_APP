import logging

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler('log_file.txt')
console_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)
console_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
file_handler.setFormatter(file_formatter)
logger.addHandler(console_handler)
logger.addHandler(file_handler)
