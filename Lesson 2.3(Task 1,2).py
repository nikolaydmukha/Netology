"""Задача №1
Нужно реализовать Польскую нотацию для двух положительных чисел. Реализовать нужно будет следующие операции:

Сложение
Вычитание
Умножение
Деление
Например, пользователь вводит: + 2 2 Ответ должен быть: 4

Задача №2
С помощью выражения assert проверять, что первая операция в списке доступных операций (+, -, *, /).
С помощью конструкций try/expcept ловить ошибки и выводить предупреждения Типы ошибок:

Деление на 0
Деление строк
Передано необходимое количество аргументов
и тд.

"""
operators = ("+", "-", "*", "/")
while True:
        example = input("Ведите пример в Польской нотации: ")
        if not example:
            print("Выход!")
            break
        else:
            split_str = example.split()
            if len(split_str) < 3:# в рамках данной задачи должно быть введено не менее 3 элементов
                print("Введены не все данные!")
            elif len(split_str) > 3:
                print("Введены слишком много данных!")
            else:
#                if split_str[0] not in operators:
                assert(split_str[0] in operators), "Вы ввели недопустимые оператор! Завершаем работу прораммы!"
                #     print("Вы ввели недопустимые оператор! Повторите ввод!")
                # else:
                try:
                    int(split_str[1])
                    int(split_str[2])
                except ValueError:
                    print("Ошибка!Один или оба операнда не числового типа")
                    continue
                if int(split_str[1]) < 0 or int(split_str[2]) < 0:
                    print("Вы ввели отрицательно число. По условию задачи число должно быть положительным!")
                    continue
                if split_str[0] == "+":
                    result = int(split_str[1]) + int(split_str[2])
                elif split_str[0] == "-":
                    result = int(split_str[1]) - int(split_str[2])
                elif split_str[0] == "*":
                    result = int(split_str[1]) * int(split_str[2])
                elif split_str[0] == "/":
                     try:
                        result = int(split_str[1]) / int(split_str[2])
                     except ZeroDivisionError:
                        print("Ошибка при вводе данных: деление на нуль.")
                        continue
                print("Результат выражения в Польской нотации'{}' = {}".format(example, result))