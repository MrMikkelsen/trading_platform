from utils.security import api_required
from flask import request, Blueprint
from DB.functions.teams import get_team_login

authorization_blueprint = Blueprint('auth', __name__)


@authorization_blueprint.route('/login', methods=['POST'])
@api_required
def post_login():
    '''
    :param api_key: api_key belonging to the team or admin
    :return: Users login information
    '''

    # Check if api_key exists
    api_key = request.json.get("api_key")
    team_login = get_team_login(api_key)

    if team_login is None:
        return "Invalid API key", 403
    else:
        return team_login, 200
