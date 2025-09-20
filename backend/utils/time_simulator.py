
import requests
from datetime import datetime
import datetime as dt


class SimulateTime:
    def get_current_time(self) -> dt.datetime:
        current_time = requests.get(
            'http://time:5004/time/currentTime').json()['data']
        # turn string to datetime
        current_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
        return current_time

    def get_current_speed(self) -> int:
        current_speed = requests.get(
            'http://time:5004/time/getTimeAcc').json()['data']
        current_speed = int(current_speed)

        return current_speed


time_con = SimulateTime()
