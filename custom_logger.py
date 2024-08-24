import logging
import sys

def setup_custom_logger(name, log_to_screen=False, log_to_file=True, loglevel=logging.INFO):
    
    class MultiLineFormatter(logging.Formatter):
        def format(self, record):
            original_message = super().format(record)
            lines = original_message.splitlines()

            formatted_lines = [self._fmt % dict(asctime=self.formatTime(record, self.datefmt),
                                                levelname=record.levelname,
                                                message=line) for line in lines]
            
            return "\n".join(formatted_lines)
    
    formatter = MultiLineFormatter(fmt='%(asctime)s %(levelname)-8s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
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

logger = setup_custom_logger('reactlog', log_to_file=True, log_to_screen=False)
