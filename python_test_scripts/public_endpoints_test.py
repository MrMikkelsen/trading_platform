
from time import time
import threading
import requests
API_KEY = '95c72466-97c7-483f-985e-4d764e093f46'
BASE_URL = '144.91.87.145'


def get_history_stocks(ticker='all', days=7):
    url = f'http://{BASE_URL}/data/days={days}'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.1.2222.33 Safari/537.36",
        "Accept-Encoding": "*",
        "Connection": "keep-alive"
    }
    # get on url and put "api_key" in body as type json without ticker in body
    try:
        response = requests.get(
            url, json={'api_key': API_KEY}, headers=headers)
    except Exception as e:
        print("error. Our server blocked us.")
    # print(response.json())


def get_all_stocks():
    url = f'http://{BASE_URL}/symbols'
    # get on url and put "api_key" in body
    response = requests.get(url)
    # print(response)


def decide_threads_and_func(nbr_threads, func, **kwargs):
    # decide how many threads to use
    # decide which function to use
    threads = []
    for _ in range(nbr_threads):
        th = threading.Thread(target=func, kwargs=kwargs)
        th.start()
        threads.append(th)
    for th in threads:
        th.join()


def main():
    start = time()
    print("Time to init: ", time() - start)

    for thread_test in [1, 10, 40]:
        start = time()
        decide_threads_and_func(thread_test, get_all_stocks)
        print(
            f'get_all_stocks : Number of threads: {thread_test}, time: {time() - start}')

    for thread_test in [1, 10, 40]:
        start = time()
        decide_threads_and_func(
            thread_test, get_history_stocks, ticker='STOCK1')
        print(
            f'7 days!! Number of threads: {thread_test}, time: {time() - start}')

    for thread_test in [1, 10, 40]:
        start = time()
        decide_threads_and_func(
            func=get_history_stocks,
            nbr_threads=thread_test,
            ticker='STOCK1',
            days=30)
        print(
            f'30 DAYS !! Number of threads: {thread_test}, time: {time() - start}')

    for thread_test in [1, 10, 40]:
        start = time()
        decide_threads_and_func(
            func=get_history_stocks,
            nbr_threads=thread_test,
            ticker='STOCK1',
            days=90)

        print(
            f'90 DAYS !! Number of threads: {thread_test}, time: {time() - start}')


if __name__ == "__main__":
    main()
