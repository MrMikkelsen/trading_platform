import datetime as dt


class SimulateTime:
    """
    This is used to simulate the time in the backend.
    """
    simulated_initial_time: dt.datetime = None
    simulated_time: dt.datetime = None
    real_last_time: dt.datetime = None
    DEFAULT_ACCELERATION = None
    acceleration: int = None

    def __init__(self, initial_time, acceleration):
        self.simulated_initial_time = self.simulated_time = initial_time
        self.acceleration = acceleration
        self.DEFAULT_ACCELERATION = acceleration
        self.real_last_time = dt.datetime.now()

    def get_current_speed(self) -> int:
        return self.acceleration

    def get_current_time(self) -> dt.datetime:
        # difference in seconds between last time and now
        current_time = dt.datetime.now()
        diff = (current_time - self.real_last_time).total_seconds()
        diff *= self.acceleration
        self.simulated_time += dt.timedelta(seconds=diff)
        self.real_last_time = current_time
        # Keep simulated time to operate only in open market hours (7 am to 3 pm)
        if self.simulated_time.hour < 7:
            self.simulated_time = self.simulated_time.replace(
                hour=7, minute=0, second=0)
        elif self.simulated_time.hour > 15:
            self.simulated_time = self.simulated_time.replace(
                hour=7, minute=0, second=0) + dt.timedelta(days=1)
        # skip weekends
        if self.simulated_time.weekday() > 4:
            self.simulated_time = self.simulated_time.replace(
                hour=7, minute=0, second=0) + dt.timedelta(days=7 - self.simulated_time.weekday())

        return self.simulated_time

    def reset_time(self, time=None) -> dt.datetime:
        '''
        Defaults to initial time
        '''
        self.simulated_time = time if time is not None else self.simulated_initial_time
        return self.simulated_time

    def change_acceleration(self, acceleration: int):
        self.get_current_time()  # Update time before changing acceleration
        self.acceleration = acceleration

    def pause_time(self):
        self.get_current_time()
        self.acceleration = 0

    def resume_time(self):
        self.get_current_time()
        self.acceleration = self.DEFAULT_ACCELERATION
