from flask import Flask, request, jsonify, make_response
from auth import check_odoo_login

app = Flask(__name__)


@app.route('/')
def index():
    return 'Server Works!'


@app.route('/api/login/', methods=['POST'])
def login():
    """
    Manage app login
    :return: True or False
    """
    data = request.get_json()

    if data['host'] and data['port'] and data['database'] and data['username'] and data['password']:
        response = check_odoo_login(data, 'login')

        return make_response(jsonify({"message": response[0]}), response[1])
    else:
        return make_response(jsonify({"message": "Unauthorized - 401"}), 401)


@app.route('/api/call_kw/', methods=['POST'])
def call_kw():
    """
    Manage call to methods in Odoo
    :return: Response
    """
    options = []

    try:
        data = request.get_json()

        if data['host'] and data['port'] and data['database'] and data['username'] and data['password']:
            response = check_odoo_login(data, 'call_kw')

            if data['options']:
                options = data['options']

            if response and data['model'] and data['method']:
                result = response.execute(data['model'], data['method'], options)

                return make_response(jsonify({"message": "Response success - 200", "response": result}), 200)
            else:
                return make_response(jsonify({"message": response[0]}), response[1])
        else:
            return make_response(jsonify({"message": "Unauthorized - 401"}), 401)
    except Exception:
        return make_response(jsonify({"message": "Not Implemented - 501"}), 501)


if __name__ == "__main__":
    app.run(host='0.0.0.0',
            debug=False,
            port=8080)
