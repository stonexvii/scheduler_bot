from datetime import time, datetime


def timestamp():
    now = datetime.now()
    return now.strftime('%H:%M:%S %D/%m/%Y')


def print_message(message: str):
    print('=' * len(message))
    print(message)
    print('=' * len(message))


def on_start():
    msg = f'Bot is started at {timestamp()}'
    print_message(msg)


def on_shutdown():
    msg = f'Bot is shutdown at {timestamp()}'
    print_message(msg)


def time_formater(current_time: time):
    return f'{current_time.hour:0>2}:{current_time.minute:0>2}'
