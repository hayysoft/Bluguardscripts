import time
import logging



def Clear_Raw_Data_Json(filename):
    with open(f'C:/Users/hayysoft/Documents/Scripts/interview/media/{filename}', 'w') as fp:
        fp.write('[]')

    return f'Cleared {filename}'

    # with open('C:/Users/hayysoft/Documents/Scripts/interview/media/incorrect_raw_data.json', 'w') as fp:
    #     fp.write('[]')



try:
    logger = logging.getLogger('Clear raw_data.json and incorrect_raw_data.json')
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('C:/Users/hayysoft/Documents/LogFiles/Clear_Raw_and_Incorrect.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.info('\nProgram started!')

    raw_data = Clear_Raw_Data_Json('raw_data.json')
    incorrect_raw_data = Clear_Raw_Data_Json('incorrect_raw_data.json')
    logger.info(f'{raw_data}')
    logger.info(f'{incorrect_raw_data}')
except KeyboardInterrupt as e:
    logger.exception(e)
except Exception as e:
    logger.exception(e)
finally:
    logger.info('Program Finished!\n')


print('Successfully cleared individual files!')
time.sleep(3)
