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
    try:
        data = request.get_json()

        if data['host'] and data['port'] and data['database'] and data['username'] and data['password']:
            check_login = check_odoo_login(data)

            if check_login:
                return make_response(jsonify({"message": "Login success"}), 200)
            else:
                return make_response(jsonify({"message": "Login error"}), 500)
    except Exception:
        return make_response(jsonify({"message": "Invalid data provided"}), 500)


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
            odoo = check_odoo_login(data)

            if data['options']:
                options = data['options']

            if odoo and data['model'] and data['method']:
                response = odoo.execute(data['model'], data['method'], options)

                return make_response(jsonify({"message": "Response success", "response": response}), 200)
            else:
                return make_response(jsonify({"message": "Server error"}), 500)
        else:
            return make_response(jsonify({"message": "Invalid data provided"}), 500)
    except Exception:
        return make_response(jsonify({"message": "Invalid data provided"}), 500)


if __name__ == "__main__":
    app.run(host='0.0.0.0',
            debug=False,
            port=8080)
