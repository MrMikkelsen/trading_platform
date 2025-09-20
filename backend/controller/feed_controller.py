from DB.functions.teams import get_all_teams_cumulative_data, get_group_data_one_group, get_and_collect_all_group_data
from flask import Blueprint, jsonify

feed_blueprint = Blueprint('feed', __name__)


@feed_blueprint.route('/cumulativeData', methods=['GET'])
def get_cumulative_profit_data():
    # TODO: error handling
    return jsonify(get_all_teams_cumulative_data()), 200

# TODO: can probably remove one of these functions, because if no offset just have it be 0 instead, right now it is just copied from old backend


@feed_blueprint.route('/groupData', methods=['GET'])
def get_all_group_data():
    # TODO error handling
    return jsonify(get_and_collect_all_group_data()), 200


@feed_blueprint.route('/groupData/offset=<offset>', methods=['GET'])
def get_all_group_data_offset(offset):
    try:
        offset = int(offset)
    except Exception as error:
        return str(error), 400
    # TODO error handling
    return jsonify(get_and_collect_all_group_data(offset)), 200


@feed_blueprint.route('/token=<token>/groupData', methods=['GET'])
def get_group_data(token):
    # TODO: Error handling

    # Check that all data is available for calculations
    return jsonify(get_group_data_one_group(token)), 200


@feed_blueprint.route('/token=<token>/groupData/offset=<offset>', methods=['GET'])
def get_group_data_offset(token, offset):
    # TODO: Error handling
    try:
        offset = int(offset)
    except Exception as error:
        return str(error), 400

    # Check that all data is available for calculations
    return jsonify(get_group_data_one_group(token, offset=offset)), 200