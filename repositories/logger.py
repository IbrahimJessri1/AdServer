
import logging
logging.basicConfig(filename='logs/logs.log', filemode='a', format='%(levelname)s - %(message)s', level=logging.ERROR)


my_logger = logging.getLogger()