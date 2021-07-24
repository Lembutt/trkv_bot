def get_local_ip():
    # source: https://www.programcreek.com/python/?CodeExample=get+local+ip
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip


if get_local_ip() != '194.32.248.49':
    BOT_TOKEN = '1674654459:AAFJAi86yYzQD-Qa958B_pKBSktDP1wpRUc'
    DB_HOST = 'lemtest.ru'
    DB_SCHEMA = 'test'
else:
    BOT_TOKEN = '1829893184:AAHmXd9pADxa0dyOr0R4DNGRvR7_b1gdVts'
    DB_HOST = '127.0.0.1'
    DB_SCHEMA = 'prod'

DB_NAME = 'tarkov'
DB_USER = 'tark'
DB_PASS = 'fasQHmjvI6'


ADMINS = [200843088, 484206299, 510811457]
MARKET_TOKEN = '2U7VepHLqy5HEapX'
MARKET_API = 'https://tarkov-market.com/api/v1/'
