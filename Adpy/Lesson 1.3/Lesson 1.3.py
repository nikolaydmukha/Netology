from datetime import datetime
import os

# 1
def logger(decorated_func):
    def wrapper(*args):
        result = decorated_func(*args)
        arg = []
        for param in args:
            arg.append(param)
        dict_data = {
            'Время вызова': str(datetime.now()),
            'Имя функции': decorated_func.__name__,
            'Парамтеры вызова': arg,
            'Результат работы программы': result
        }
        with open(os.path.abspath('result'), 'w', encoding='utf-8') as f:
            for key, val in dict_data.items():
                f.write('{}: {} \n'.format(key, val))
    return wrapper


# 2
def decorator_path(path):
    def logger(decorated_func):
        def wrapper(*args):
            result = decorated_func(*args)
            arg = []
            for param in args:
                arg.append(param)
            dict_data = {
                'Время вызова': str(datetime.now()),
                'Имя функции': decorated_func.__name__,
                'Парамтеры вызова': arg,
                'Результат работы программы': result
            }
            with open(path, 'w', encoding='utf-8') as f:
                for key, val in dict_data.items():
                    f.write('{}: {} \n'.format(key, val))
        return wrapper
    return logger


@logger
def print_text(text1, text2):
    return text1 + "<->" + text2


@decorator_path(os.path.abspath('result_path'))
def print_text_path(text1, text2):
    return text1 + "," + text2


if __name__ == '__main__':
    print_text('1', '2')
    print_text_path('Hello', 'Word')

