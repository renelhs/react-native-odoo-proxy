import os
import logging
from flask import Flask, request, jsonify, make_response, render_template
from auth import check_odoo_alive, check_odoo_login
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SHOW_LOGS'] = os.getenv("SHOW_LOGS")

if app.config['SHOW_LOGS'] == 'True':
    proxy_log_file = os.getenv("PROXY_LOG_FILE")
    logging.basicConfig(filename=proxy_log_file, level=logging.DEBUG,
                        format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


@app.route('/')
def index():
    app.logger.info('Info level home')
    app.logger.warning('Warning level home')
    app.logger.error('Error level home')
    message = ""
    response = check_odoo_alive()

    if type(response) == list and '502' in response[0]:
        message += "But, there is an error trying to connect Odoo server: [Bad Gateway - 502], " \
                   "check if Odoo is running and proxy configurations HOST and/or PORT are correct."

    return render_template('home.html', message=message)


@app.route('/api/login/', methods=['POST'])
def login():
    """
    Manage app login
    :return: True or False
    """
    data = request.get_json()

    if data['database'] and data['username'] and data['password']:
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
    app.logger.info('Info level call Odoo')
    app.logger.warning('Warning level call Odoo')
    app.logger.error('Error level call Odoo')
    options = []

    try:
        data = request.get_json()

        if data['host'] and data['port'] and data['database'] and data['username'] \
                and data['password']:
            response = check_odoo_login(data, 'call_kw')

            if 'options' in data:
                options = data['options']

            if response and data['model'] and data['method']:
                result = response.execute(data['model'], data['method'], options)

                return make_response(jsonify({"message": "Response success - 200",
                                              "response": result}), 200)
            else:
                return make_response(jsonify({"message": response[0]}), response[1])
        else:
            return make_response(jsonify({"message": "Unauthorized - 401"}), 401)
    except Exception:
        return make_response(jsonify({"message": "Not Implemented - 501"}), 501)


def build_logs(file_url):
    """Creates logging information"""
    number_logs_lines = int(os.getenv("NUMBER_LOGS_LINES"))

    try:
        with open(file_url) as f:
            logs = f.readlines()[-number_logs_lines:]

        return logs
    except IOError:
        return ['Log file not found, check your configuration file.']


@app.route('/proxy-logs')
def proxy_logs():
    """Returns proxy logging information"""
    if app.config['SHOW_LOGS'] == 'True':
        log_file = os.getenv("PROXY_LOG_FILE")

        return render_template('logs.html', log_type="Proxy", logs_data=build_logs(log_file))

    return render_template('no_debug.html')


@app.route('/odoo-logs')
def odoo_logs():
    """Returns odoo logging information"""
    if app.config['SHOW_LOGS'] == 'True':
        log_file = os.getenv("ODOO_LOG_FILE")

        return render_template('logs.html', log_type="Odoo", logs_data=build_logs(log_file))

    return render_template('no_debug.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0',
            debug=True,
            port=8080)
