import threading
import time
import random
import hackathon_linc as lh


def get_historic_prices():
    start = time.time()
    result = lh.get_historical_data(365)
    print(f"getting historical data took {time.time()-start} seconds")
    return result


def load_keys():
    keys = [

        # "60dea4e8-9bf9-4beb-b632-37560311bd11",
        "bab37a22-507e-4140-81b2-1f3f56824079",
        "6c535b92-dbb3-487a-a21b-73f545ce4598",
        "d787d207-e85a-4899-9f44-f9a110ad9cf9",
        "68ecf186-2844-4caf-9d4c-dd1c6ca5a5b8",
        "b7949dfc-2bc4-4132-b795-a751f34c1c55",
        "49f208b9-fb83-421b-8c28-80b78411d323",
        "78d8a05d-c9da-44bb-92e5-3aa1c84a9e7e",
        "f7a26b39-3fdf-4137-ad24-e72cdecc3395",
        "108873b7-97d5-4b1e-b2b7-dde75c0a2d2d",
        "cc42702e-cbf3-42ea-9a9b-a68fdf39c596"


    ]
    return keys


def buy_sell_thread(api_key):
    securities = ["STOCK1", "STOCK2", "STOCK3", "STOCK4",
                  "STOCK5", "STOCK6", "STOCK7", "STOCK8", "STOCK9", "STOCK10"]
    from hackathon_linc import ipaddr as u
    #print(f"buying with key: {api_key}")
    u.token = api_key
    try:

        while True:
            u.token = api_key
            print(f"buying with key: {u.token}")
            lt = lh.buy(random.choice(securities), 1)
            print(lt)
            lh.get_portfolio()
            lh.sell(random.choice(securities), 1)
            time.sleep(0.1)
            a = time.time()
            lh.buy(random.choice(securities), 1, 89)
            lh.sell(random.choice(securities), 1)
            print(f"time to buy and sell {time.time() - a}")
            lh.get_portfolio()
            lh.get_completed_orders()
            lh.get_pending_orders()
            lh.stoploss(random.choice(securities), 1, 50)
            time.sleep(1)
            get_historic_prices()
    except Exception as e:
        print(f"Thread with key {api_key} raised an error: {str(e)}")


if __name__ == '__main__':
    threads = []
    keys = load_keys()
    for key in keys:
        # lh.init(key)
        thread = threading.Thread(target=buy_sell_thread, args=(key,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
        time.sleep(5)
