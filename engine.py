import datetime
import dotenv
import gc
import os
import pandas as pd
import shutil
import time

from get_full_info import get_full_info
from fetch_links import get_links
from multiprocessing.pool import ThreadPool

from ranges import ranges_for_parser

dotenv.load_dotenv("./venv/.env")


def the_parser(range_of_pages):
    parsed_data = []
    for n in range(range_of_pages[0], range_of_pages[1]):
        linx = get_links(os.getenv('URL').format(n))
        workers = len(linx)
        with ThreadPool(workers) as pool:
            parsed_data += pool.map(get_full_info, linx)

    return parsed_data


def refactor_and_save_to_excel(data, num) -> None:
    df = pd.DataFrame(data=data,
                      columns=['name', 'branch', 'street', 'zip', 'city', 'webpage', 'telephone', 'email'])

    df['email'] = [str(x).replace(",",
                                  ";").replace("[",
                                               "").replace("]",
                                                           "").replace("'",
                                                                       "") for x in
                   df['email'].values]

    df['telephone'] = [str(x).replace("[",
                                      "").replace("]",
                                                  "").replace("'",
                                                              "") for x in df['telephone'].values]

    df.to_excel(f'output_file/database_{datetime.date.today()}_{num}.xlsx',
                sheet_name=f'poland{num}', index=False)


class timer:
    def __init__(self, message):
        self.message = message

    def __enter__(self):
        self.start = time.time()
        now = datetime.datetime.now()
        print(f'Started at: {now}')
        return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed_time = (time.time() - self.start)
        print(self.message.format(elapsed_time))


if __name__ == '__main__':

    parser_ranges = ranges_for_parser(780)

    for rang in parser_ranges:

        with timer('Executed in: {}s'):
            os.mkdir('img')
            refactor_and_save_to_excel(the_parser(rang), parser_ranges.index(rang))
            shutil.rmtree('img')
        gc.collect()

    # with timer('Executed in: {}s'):
    #     os.mkdir('img')
    #     refactor_and_save_to_excel(the_parser((150,180)), 6)
    #     shutil.rmtree('img')
    # gc.collect()

