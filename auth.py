import odoorpc

# Configure your Odoo server HOST and PORT
ODOO_HOST = '127.0.0.1'
ODOO_PORT = 8069


def check_odoo_alive():
    try:
        return odoorpc.ODOO(ODOO_HOST, port=ODOO_PORT, timeout=60)
    except Exception:
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
