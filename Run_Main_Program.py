import os
import logging
from datetime import datetime
from mysql.connector import ProgrammingError
import smtplib, os


X = lambda s: os.system(s)
os.chdir('C:/Users/hayysoft/Documents/BluguardScripts')


def Run_Main_Program():
    try:
        logger = logging.getLogger('Run Server')
        logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler('C:/Users/hayysoft/Documents/LogFiles/Run_Main_Program.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.info('\nProgram started!')

        X('python Main_Program.py')
    except KeyboardInterrupt as e:
        logger.exception(e)
        # import Twilio_Config
    except Exception as e:
        logger.exception(e)
        # import Twilio_Config
    finally:
        logger.info('Program Finished!\n')
        # import Twilio_Config
        X('python Main_Program.py')


try:
    Run_Main_Program()
except RuntimeError:
    # import Twilio_Config
    Run_Main_Program()
except RuntimeWarning:
    # import Twilio_Config
    Run_Main_Program()
finally:
    # import Twilio_Config
    Run_Main_Program()

