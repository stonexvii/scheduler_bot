from datetime import time


def on_start():
    print('Bot is started!')


def on_shutdown():
    print('Bot is shutdown...')


def time_formater(current_time: time):
    return f'{current_time.hour:0>2}:{current_time.minute:0>2}'
