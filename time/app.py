from flask import Flask, request, jsonify
from datetime import datetime
from time_simulator import SimulateTime

app = Flask(__name__)

DEFAULT_ACCELERATION = 60 * 60
START_DATE = datetime(1999, 2, 8, 7, 0, 0)
time_con = SimulateTime(START_DATE, DEFAULT_ACCELERATION)

#START_DATE = datetime(2010, 2, 8, 8, 0, 0)
#START_DATE = datetime(2015, 4, 22, 7, 0, 0)

@app.route('/time/reset', methods=['POST'])
def reset_time():
    '''
    :param time: time to reset to
    :return: new time
    '''
    time = request.json.get("date")
    if time is not None:
        try:
            time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            return jsonify('Invalid time format'), 400
    time_con.reset_time(time)
    return str(time_con.reset_time(time)), 200


@ app.route('/time/setTimeAcc', methods=['POST'])
def set_time_acc():
    '''
    :param acc: acceleration of time
    :return: new acceleration'''
    ratio_res = request.json.get("ratio")
    try:
        # *60 to convert the input into minutes
        ratio = int(ratio_res["ratio"]) * 60
    except ValueError:
        return jsonify('Invalid ratio format'), 400

    time_con.change_acceleration(ratio)
    return {"data": str(ratio)}, 200


@ app.route('/time/getTimeAcc', methods=['GET'])
def get_time_acc():
    '''
    :return: current acceleration of time
    '''
    return {"data": str(time_con.get_current_speed())}, 200


@ app.route('/time/currentTime', methods=['GET'])
def get_current_time():
    '''
    :return: current time
    '''
    time = time_con.get_current_time().isoformat() \
        .replace("T", " ")[0: 16] + ":00"
    return {"data": time}, 200


@ app.route('/time/pauseTime', methods=['PUT'])
def pause_time():
    '''
    :return: current time
    '''
    time_con.pause_time()
    return {"data": "Time paused"}, 200


@ app.route('/time/resumeTime', methods=['PUT'])
def resume_time():
    '''
    :return: current time
    '''
    time_con.resume_time()
    return {"data": "Time resumed"}, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
