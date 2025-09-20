import hackathon_linc as lh
import time

if __name__ == '__main__':
    lh.init('69129c03-d311-4cb5-ba86-9ac429aac9dd')

    lh.buy('STOCK1', 1)
    time.sleep(0.2)
    lh.stoploss('STOCK1', 1, 680)
    time.sleep(0.2)
    lh.sell('STOCK1', 1)
