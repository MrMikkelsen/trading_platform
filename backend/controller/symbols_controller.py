from utils.exchange import prices_con
from flask import jsonify, Blueprint

symbol_blueprint = Blueprint('symbols', __name__)


@symbol_blueprint.route('/', methods=['GET'])
def get_symbols():
    '''
    :return: list of all symbols
    '''
    symbols = prices_con.get_all_symbols()
    return jsonify(symbols), 200
