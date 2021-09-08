from flask import Flask, request, send_from_directory, render_template, jsonify
import json
from utils import get_currencies

with open("config.json", 'r') as f:
    datastore = json.load(f)

app = Flask(__name__, template_folder='.')


def validate_input_str(query_string, supported_curr):
    input_params = query_string.decode('utf8').split('&')
    if len(input_params) < 3:
        return {'code': 400, 'message': 'Invalid input'}
    input_dict = {}
    for param in input_params:
        param_list = param.split('=')
        if len(param.split('=')) == 2:
            input_dict[param_list[0]] = param_list[1]
    from_curr = supported_curr.get(input_dict['from'], None)
    if not from_curr:
        return {'code': 400, 'message': 'From cur not supported'}
    to_curr = supported_curr.get(input_dict['to'], None)
    if not to_curr:
        return {'code': 400, 'message': 'TO cur not supported'}
    try:
        amount = int(input_dict['amount'])
        if amount < 0:
            return {'code': 400, 'message': 'Invalid amount input'}
    except Exception as e:
        return {'code': 400, 'message': 'Invalid amount input'}

    precision_value = 4
    try:
        precision = input_dict.get('precision', None)
        if precision:
            precision_value = int(precision)
        if precision_value < 0:
            return {'code': 400, 'message': 'Invalid precission input'}

    except Exception as e:
        return {'code': 400, 'message': 'Invalid precission input'}

    # from, to currencies are safe, return same input amount
    if (from_curr == to_curr):
        preci_amount = "{0:.{1}f}".format(amount, precision_value)
        return {'code': 200, 'amount': preci_amount, 'curr': to_curr}
    from_value = supported_curr[input_dict['from']]
    to_value = supported_curr[input_dict['to']]
    final_amount = to_value * amount / from_value
    print(f'final_amount:{final_amount}')
    preci_amount = "{0:.{1}f}".format(final_amount, precision_value)
    return {'code': 200, 'amount': preci_amount, 'curr': to_curr}


@app.route("/")
def hello():
    return render_template("default.html")


@app.route("/convert", methods=["GET", "POST", "PUT"])
def convert_api():
    supported_curr = get_currencies()
    validation_result = validate_input_str(
        request.query_string, supported_curr)
    if validation_result['code'] == 400:
        return jsonify({"message": "Invalid input"}), 400

    return jsonify({"message": validation_result['amount']}), 200

    pass
    return jsonify({"message": "1.0000"}), 200


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=900)
