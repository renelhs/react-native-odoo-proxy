import odoorpc


def check_odoo_login(access_data, request_type):
    """
    Check login against Odoo server
    :return: object or response message and code
    """
    try:
        odoo = odoorpc.ODOO('127.0.0.1', port=8069)
    except Exception:
        return ['Bad Gateway - 502', 502]

    try:
        odoo.login(access_data['database'], access_data['username'], access_data['password'])

        if odoo and request_type == 'login':
            return ['Login success - 200', 200]
        else:
            return odoo
    except Exception:
        return ['Forbidden - 403', 403]
