import odoorpc


def check_odoo_login(access_data):
    """
    Check login against Odoo server
    :return: true or false
    """
    try:
        odoo = odoorpc.ODOO('192.168.2.143', port=int(access_data['port']))
        odoo.login(access_data['database'], access_data['username'], access_data['password'])

        return odoo
    except Exception:
        return False
