# Пишем код для исключений - удар мимо поля, удар в уже пораженный участок, и исключение родитель, общее для всего
# остального.
from random import randint
#поскольку это мой класс исключений, он наследуется от Exception'а
class BattleException(Exception):
    pass
# эти наследуются от родителя
class BattleBoardException(BattleException):
    def __str__(self):    # используем магический метод str
        return "Вы выстрелили за пределы поля!"


class BoardShotException(BattleException):
    def __str__(self):
        return "Вы уже сюда стреляли!"


class BoardWrongShipException(BattleException):
    pass

# Создаем точки на оси для последующего отмечания строки и столбца
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):    # создаем метод сравнения точек в последующих списках
        return self.x == other.x and self.y == other.y

    def __repr__(self):  # метод repr - то, как обьекты будут отображаться в системе
        return f"({self.x}, {self.y})"

# Создаем корабль,с параметрами - длина, расположение носа корабля(точка), направление(вертикаль/горизонталь),
# количество жизней(сколько неподбитых точек корабля осталось). Содаем метод dots, который возвращает список
# всех точек корабля.

class Ship:
    def __init__(self, bow, lenght, direction):
        self.bow = bow  #нос кобрабля
        self.lenght = lenght  #длина
        self.direction = direction  #направление
        self.lives = lenght  #жизнь корабля, это по сути, его длина

    @property
    def dots(self):
        ship_dots = []  #создаем пустой список для точек размещения корабля
        for i in range(self.lenght):  #расположение носа от точек x, y в Dot
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.direction == 0: #горизонталь
                cur_x += i

            elif self.direction == 1:   #вертикаль
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))    #добаляем в список

        return ship_dots    #возвращаем список

    # проверка на попадание в корабль
    def got_shot(self, shot):    #принимает себя и удар
        return shot in self.dots

# Создаем игровую доску. Это двумерный список, в котором хранятся состояния каждой из клеток, также список
# кораблей доски. Параметр hid типа bool(информация о том, нужно ли скрывать корабли на доске (для вывода доски
# оопонента), или нет (для своей доски)) и количество живых кораблей на доске.

class Board:
    def __init__(self, hid=False, size=6):  #по умолчанию размер 6
        self.size = size
        self.hid = hid  #прятать ли кобарли?

        self.count = 0  #для количества пораженных кораблей

        self.field = [["O"] * size for _ in range(size)]    #создание сетки для отображения состояния

        self.busy = []  #пустой список для использованных точек
        self.ships = []     #список кораблей

    def add_ship(self, ship):   #размещение корабля

        for d in ship.dots:     #проверяем, чтобы точки не выходили за границы поля
            if self.out(d) or d in self.busy:    #и не заняты
                raise BoardWrongShipException()    #если да, то вызываем исключение
        for d in ship.dots:     #проходим по всем точкам
            self.field[d.x][d.y] = "•"  #заполняем символом корабля
            self.busy.append(d)     #добавляем точку в список занятых точек

        self.ships.append(ship)     #добавляем корабль в список кораблей
        self.contour(ship)      #обводим корабль по контуру

    def contour(self, ship, verb=False):    #переменная around нужна для отделения кораблей друг от друга, чтобы они не со
        #касались, verb показывает нужно ли ставить точки вокруг корабля
        around = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:     #проходим все точки, которые соседствуют с кораблем
            for dx, dy in around:   #точки проводим по списку around
                cur = Dot(d.x + dx, d.y + dy)   #сдвигаем исходную точку на новую
                if not (self.out(cur)) and cur not in self.busy:    #если точка не выходит за границы и не занята
                    if verb:    #если нужно ставить точки вокруг корабля
                        self.field[cur.x][cur.y] = "."  #ставим символ,чтобы показать, что текущая точка занята
                    self.busy.append(cur)   #записываем точку в список занятых точек

    def __str__(self):  #делаем вывод корабля на доску
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:    #корабль скрываем
            res = res.replace("•", "O")     #заменяем символы, чтобы пользователь не видел, где корабли противника
        return res

    def out(self, d):   #проверка на то, если точка за пределами поля
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))  #координаты не лежат от 0 до size

    def shot(self, d):  #проверка выстрела
        if self.out(d):  #если стреляют за пределы поля вызываем нужное исключение
            raise BattleBoardException()

        if d in self.busy:     #если выстрел есть в списке уже использованных клеток
            raise BoardShotException()

        self.busy.append(d)  #невзирая на результат проверки,выстрел добавляем в список busy

        for ship in self.ships:     #проверяем на попадаение
            if d in ship.dots:      #если корабль подстрелян
                ship.lives -= 1     #минус одна жизнь/длина
                self.field[d.x][d.y] = "X"      #отмечаем на поле попадание по координатам строки и столбца
                if ship.lives == 0:     #если у корабля не осталось жизней
                    self.count += 1     #записываем пораженный корабль в счет
                    self.contour(ship, verb=True)   #если кобраль уничтожен, точки вокруг корабля ставить НУЖНО(контур)
                    print("Корабль уничтожен!")
                    return False    #чтобы дать понять, что дальше не нужно делать ход
                else:
                    print("Корабль ранен!")
                    return True     #даем знать, что нужно ходить дальше

        self.field[d.x][d.y] = "."      #попадания не случилось, отмечаем пустой выстрел символом
        print("Мимо!")
        return False       #окончание хода

    def begin(self):    #обнуляем список занятых точек при начале игры(сначала мы хранили там точки вокруг кораблей,
        # теперь там точки куда стрелял игрок)
        self.busy = []

#создаем родительский класс игрока
class Player:
    def __init__(self, board, enemy):   #в инит передаем 2 доски, свою и оппонента
        self.board = board
        self.enemy = enemy

    def ask(self):      #метод создан для потомков(будем его переопределять)
        raise NotImplementedError()

    def move(self):     #делаем выстрел в бесконечном цикле
        while True:
            try:
                target = self.ask()     #просим дать координаты выстрела
                repeat = self.enemy.shot(target)    #если выстрел прошел удачно
                return repeat   #возвращаем ход
            except BattleException as e:     #если неудачно, что вылезает исключение
                print(e)


class AI(Player):   #ход компьютера
    def ask(self):  #переопределяем от класса Игрок
        d = Dot(randint(0, 5), randint(0, 5))   #используем импортированный метод рандомного числа
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")   #отображение хода компьютера
        return d    #возращаем ход


class User(Player):     #класс пользоватаеля наследуем от Игрока
    def ask(self):      #где мы в постоянном цикле спрашиваем координаты
        while True:
            cords = input("Ваш ход: ").split()  #запрос координат

            if len(cords) != 2:     #и делаем проверки на длину
                print(" Введите 2 координаты! ")
                continue

            x, y = cords    #присваиваем коодинатам разные переменные чтобы проверить

            if not (x.isdigit()) or not (y.isdigit()):  #тип данных
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)   #убеждаемся, что тип данных int

            return Dot(x - 1, y - 1)    #возвращаем координаты, вычитая единицу,тк
            # индексация списка в 0, а пользователь пишет с 1



class Game:
    def __init__(self, size=6):
        self.size = size
        player = self.random_board()    #образуем доску пользователя
        computer = self.random_board()    #образуем доску компьютера
        computer.hid = True               #скрываем кобарли компютера

        self.ai = AI(computer, player)        #создаем игроков
        self.us = User(player, computer)

    def random_board(self):     #рандомное создание поля
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):     #метод установки корабля
        lens = [3, 2, 2, 1, 1, 1, 1]    #список длин кораблей
        board = Board(size=self.size)   #создаем доску
        attempts = 0    #счетчик для количество попыток
        for l in lens:  #в бесконечном цикле расставляем каджый корабль
            while True:
                attempts += 1
                if attempts > 2000:     #если попыток больше 2000, возвращаем пустую доску
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)    #если корабль установился, завершаем попытки его установить
                    break
                except BoardWrongShipException:
                    pass
        board.begin()   #обнуляем список занятых точек
        return board    #возвращваем доску

    def greet(self):    #приветствие
        print("-------------------")
        print(" Добро пожаловать  ")
        print("      в игру       ")
        print("    морской бой!   ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def loop(self):     #петля игры
        num = 0         #номер хода
        while True:
            print("-" * 27)
            print("Доска пользователя:")
            print(self.us.board)    #выводим доску пользователя
            print("-" * 27)
            print("Доска компьютера:")
            print(self.ai.board)    #выводим доску компьютера
            if num % 2 == 0:    #очередность хода / если четный -ходит пользователь
                print("-" * 27)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 27)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:      #если произошло попадаие и нужно стрелять опять, функция выполняется
                num -= 1    #но в номер хода это не идет

            if self.ai.board.count == 7:    #если счет равен количеству кораблей
                print("-" * 27)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:    #если счет равен количеству кораблей
                print("-" * 27)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()