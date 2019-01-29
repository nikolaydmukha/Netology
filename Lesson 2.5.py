# Задача №1
# Необходимо реализовать менеджер контекста, печатающий на экран:
#
# Время запуска кода в менеджере контекста;
# Время окончания работы кода;
# Сколько было потрачено времени на выполнение кода.
# Задача №2
# Придумать и написать программу, использующая менеджер контекста из задания 1.
# Если придумать не получиться, использовать программу из предыдущих домашних работ.

import datetime
import time
import random

class ContextManagerShowTime:
    def __init__(self, path_to_file):
        print("Вход в менеджер контекста")
        self.start = datetime.datetime.now()
        self.start_sec = time.time()
        self.path = path_to_file

    def __enter__(self):
        print(f"Начало работы {self.start}")
        print("Sleeping just for 5 seconds...")
        time.sleep(5)
        self.file = open(self.path, "w")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = datetime.datetime.now()
        self.end_sec = time.time()
        duration = round(self.end_sec - self.start_sec)
        print(f"Окончание работы {self.end}")
        print(f"Общее время выполнения программы {duration} секунд")
        print("Выходим из менеджера контекста!")
        self.file.close()

# Задача 1, 2
path_to_file = "matrix.txt"
with ContextManagerShowTime(path_to_file) as file:
# Заполним данные для формирования матрицы
    first = int(input("Введите первое число: "))
    second = int(input("Введите второе число: "))
    i = 0
    matrix = []
    while i <= first:
        matrix_temp = []
        j = 0
        while j <= second:
            matrix_temp.append(random.randrange(1, second))
            j += 1
        i += 1
        matrix.append(matrix_temp)
# Запишем матрицу в файл
    for line in matrix:
        temp_list = []
        for element in line:
            temp_list.append(str(element))
        file.file.write(" ".join(temp_list) + "\n")

