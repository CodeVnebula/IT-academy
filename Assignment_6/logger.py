import logging

def setup_sql_logging(log_file:str):
    logger = logging.getLogger('sqlalchemy.engine')
    logger.setLevel(logging.INFO) 

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)