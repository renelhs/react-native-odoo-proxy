import os
import odoorpc


def check_odoo_alive():
    odoo_host = os.getenv("HOST")
    odoo_port = os.getenv("PORT")

    try:
        return odoorpc.ODOO(odoo_host, port=int(odoo_port))
    except Exception as e:
        print('ERROR Checking alive:', e)
        return ['Bad Gateway - 502', 502]


def check_odoo_login(access_data, request_type):
    """
    Check login against Odoo server
    :return: object or response message and code
    """
    try:
        odoo = check_odoo_alive()
        odoo.login(access_data['database'], access_data['username'], access_data['password'])

        if odoo and request_type == 'login':
            return ['Login success - 200', 200]
        else:
            return odoo
    except Exception:
        return ['Forbidden - 403', 403]
