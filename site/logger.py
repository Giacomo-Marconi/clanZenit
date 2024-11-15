import logging

class Log:
    def __init__(self, name, log_file, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger


if __name__ == "__main__":
    custom_logger = Log('logger', 'logFile.log')
    logger = custom_logger.get_logger()
    logger.info('info message')
    logger.error('error message')