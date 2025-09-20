import functools
import time
from collections import deque, defaultdict
from queue import LifoQueue, Full
from flask import request
from DB.models.team import Team
from DB.session import get_session
from sqlalchemy import select
from utils.time_simulator import time_con


class TimeWindowQueue:
    def __init__(self, size, time_window):
        self.queue = deque(maxlen=size)
        self.time_window = time_window

    def add_request(self):
        current_time = time.time()
        while self.queue and current_time - self.queue[0] > self.time_window:
            self.queue.popleft()
        if len(self.queue) >= self.queue.maxlen:
            return False
        self.queue.append(current_time)
        return True


####
# define the time window in seconds for the rate limit
request_limit = 5
time_window = 1.0
team_request_limit = defaultdict(
    lambda: TimeWindowQueue(request_limit, time_window))
###


def is_valid(api_key):
    with get_session() as session:
        team = session.query(Team).filter(
            Team.api_key == api_key).first()
        return True if team else False


def api_required(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if request.json:
            api_key = request.json.get("api_key")
        else:
            return {"message": "Please provide an API key"}, 400
        # Check if API key is correct and valid
        with get_session() as session:
            team = session.query(Team).filter(Team.api_key == api_key).first()
        if team:
            # Check if competition and paused and that the request was made by a team
            if time_con.get_current_speed() == 0 and team.role == "group":
                return {"message": "The competition is paused"}, 503
            # Check if the team has reached the rate limit
            if not team_request_limit[team.id].add_request():
                return {"message": "The rate limit has been reached"}, 429
            # if func takes a team as argument, pass it
            if "team" in func.__code__.co_varnames:
                kwargs["team"] = team
            return func(*args, **kwargs)
        else:
            return {"message": "The provided API key is not valid"}, 403
    return decorator


def admin_required(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        # Check if the team is an admin
        team = kwargs.get("team")
        if not team or team.role != "admin":
            return {"message": "You must be an admin to access this endpoint"}, 403
        return func(*args, **kwargs)
    return decorator
