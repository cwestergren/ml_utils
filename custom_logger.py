import logging
import sys

def setup_custom_logger(name, log_to_screen=False, log_to_file=True, loglevel=logging.INFO):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
        
    logger = logging.getLogger(name)
    logger.setLevel(loglevel)
    
    if log_to_screen:
        screen_handler = logging.StreamHandler(stream=sys.stdout)
        screen_handler.setFormatter(formatter)
        logger.addHandler(screen_handler)
    
    if log_to_file:
        now =  datetime.now().strftime("%Y%m%d-%H%M%S")
        file_handler = logging.FileHandler(f'{now}_{name}.log', mode='w')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

logger = setup_custom_logger('reactlog', log_to_file=False, log_to_screen=True)
