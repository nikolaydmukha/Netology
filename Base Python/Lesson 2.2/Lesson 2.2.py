# Вы приехали помогать на ферму Дядюшки Джо и видите вокруг себя множество разных животных:

# гусей "Серый" и "Белый"
# корову "Маньку"
# овец "Барашек" и "Кудрявый"
# кур "Ко-Ко" и "Кукареку"
# коз "Рога" и "Копыта"
# и утку "Кряква"
# Со всеми животными вам необходимо как-то взаимодействовать:

# кормить
# корову и коз доить
# овец стричь
# собирать яйца у кур, утки и гусей
# различать по голосам(коровы мычат, утки крякают и т.д.)
# Задача №1
# Нужно реализовать классы животных, не забывая использовать наследование, определить общие методы взаимодействия с животными и дополнить их в дочерних классах, если потребуется.

# Задача №2
# Для каждого животного из списка должен существовать экземпляр класса. Каждое животное требуется накормить и подоить/постричь/собрать яйца, если надо.

# Задача №3
# У каждого животного должно быть определено имя(self.name) и вес(self.weight).

# Необходимо посчитать общий вес всех животных(экземпляров класса);
# Вывести название самого тяжелого животного.
# Задача №4
# Для подготовки к следующей лекции прочитайте про исключения.
class Animals:
    def __init__(self, voice, name, legs, weight, kind, color):
        self.name = name  # имя
        self.legs = legs  # количетсво лап/ног
        self.weight = weight  # вес
        self.color = color  # цвет
        self.voice = voice  # голос
        self.kind = kind  # вид животного

    def give_food(self):
        print("{} накормлен(а)!".format(self.name))

    def show_voice(self):
        print("Голос подвида '{}' по имени {} звучит как {}!".format(self.kind, self.name, self.voice))


class BigAnimals(Animals):
    def __init__(self, voice, name, legs, weight, kind, color):
        super().__init__(voice, name, legs, weight, kind, color)

    def get_milk(self):
        if self.kind == "корова":
            milk = 10  # надоили 10 литров молока
            print("Надоили {} литра(ов) молока у коровы {}".format(milk, self.name))
        else:
            milk = 2  # надоили 10 литров молока
            print("Надоили {} литра(ов) молока у овцы {}".format(milk, self.name))

    def cut(self):
        massa = 1
        print("Состригли {} кг шерсти у овцы {}".format(massa, self.name))


class SmallAnimals(Animals):
    def __init__(self, voice, name, legs, weight, kind, color):
        super().__init__(voice, name, legs, weight, kind, color)

    def get_eggs(self):
        if self.kind == "кура":
            count = 10
            print("Собрали {} яиц у куры по кличке {}".format(count, self.name))
        elif self.kind == "гусь":
            count = 8
            print("Собрали {} яиц у гуся по кличке {}".format(count, self.name))
        else:
            count = 2
            print("Собрали {} яиц у утки по кличке {}".format(count, self.name))


# Создадим экземпляры классов
cow = BigAnimals(voice="МууууМуууу", name="Манька", legs=4, weight=10, kind="корова", color="коричневый")
sheep_bar = BigAnimals(voice="БеееБеее", name="Барашек", legs=4, weight=30, kind="овца", color="белый")
sheep_kud = BigAnimals(voice="БеееБеее", name="Кудрявый", legs=4, weight=40, kind="овца", color="чёрный")
goat_roga = BigAnimals(voice="Бее", name="Рога", legs=2, weight=23, kind="коза", color="белый")
goat_kopyta = BigAnimals(voice="Бее", name="Копыта", legs=2, weight=18, kind="коза", color="чёрный")
chicken_koko = SmallAnimals(voice="КуКаРеКу", name="Ко-ко", legs=2, weight=7, kind="кура", color="белый")
chicken_kuku = SmallAnimals(voice="КуКаРеКу", name="Кукареку", legs=2, weight=4, kind="кура", color="коричневый")
duck = SmallAnimals(voice="КряКря", name="Кряква", legs=2, weight=6, kind="утка", color="чёрный")
goose_gray = SmallAnimals(voice="ГаГаГа", name="Серый", legs=2, weight=10, kind="гусь", color="серый")
goose_white = SmallAnimals(voice="ГаГаГа", name="Белый", legs=2, weight=8, kind="гусь", color="белый")

# Накормим всех
print("Покормим всех:")
cow.give_food()
sheep_bar.give_food()
sheep_kud.give_food()
goat_roga.give_food()
goat_kopyta.give_food()
chicken_koko.give_food()
chicken_kuku.give_food()
duck.give_food()
goose_gray.give_food()
goose_white.give_food()
print("\n")

# Подстричь овец
print("Подстрижём овец:")
sheep_bar.cut()
sheep_kud.cut()
print("\n")

# Прказать звучание голоса
print("Демонстрация голоса:")
cow.show_voice()
sheep_bar.show_voice()
sheep_kud.show_voice()
goat_roga.show_voice()
goat_kopyta.show_voice()
chicken_koko.show_voice()
chicken_kuku.show_voice()
duck.show_voice()
goose_gray.show_voice()
goose_white.show_voice()
print("\n")

# Собрать яйца
print("Собираем яйца:")
chicken_koko.get_eggs()
chicken_kuku.get_eggs()
duck.get_eggs()
goose_gray.get_eggs()
goose_white.get_eggs()
print("\n")

# Подоить
print("Подоить животных:")
cow.get_milk()
sheep_bar.get_milk()
sheep_kud.get_milk()
print("\n")

# Найдём самых тяжелых и суммарный вес всех животных
# Создадим кортеж(чтобы меньше занимать памяти) из весов всех животных
weights = (
    cow.weight,
    sheep_bar.weight,
    sheep_kud.weight,
    goat_roga.weight,
    goat_roga.weight,
    chicken_koko.weight,
    chicken_kuku.weight,
    duck.weight,
    goose_gray.weight,
    goose_white.weight,
)

# Найдем максимальный вес и вес всех животных
max_weight = max(weights)
# Сосчитаем вес всех животных
sum_weight = (sum((int(weights[i]) for i in range(0, int(len(weights))))))
print("Суммарный вес всех животных равен {} кг".format(sum_weight))

# Убедимся, что только одно животное имеет максимальный вес. Если нет, то выведем всех
# Нам понадобится словарь, чтобы информативно вывести данные о тяжеловесах
zoo_weights = [
    {'kind': cow.kind, cow.name: cow.weight},
    {'kind': sheep_bar.kind, sheep_bar.name: sheep_bar.weight},
    {'kind': sheep_kud.kind, sheep_kud.name: sheep_kud.weight},
    {'kind': goat_roga.kind, goat_roga.name: goat_roga.weight},
    {'kind': goat_kopyta.kind, goat_roga.name: goat_roga.weight},
    {'kind': chicken_koko.kind, chicken_koko.name: chicken_koko.weight},
    {'kind': chicken_kuku.kind, chicken_kuku.name: chicken_kuku.weight},
    {'kind': duck.kind, duck.name: duck.weight},
    {'kind': goose_gray.kind, goose_gray.name: goose_gray.weight},
    {'kind': goose_white.kind, goose_white.name: goose_white.weight},
]
output_max_weights = "\nМаксимальный вес:\n"

for item in zoo_weights:
    temp_list_keys = list(item.keys())
    temp_list = list(item.values())
    kind = temp_list_keys[1]
    name = temp_list[0]
    if max_weight in temp_list:
        output_max_weights += "{} кг у {}({}) \n".format(max_weight, kind, name)
print(output_max_weights)


