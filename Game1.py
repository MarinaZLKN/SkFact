# Создаем игру Крестики-Нолики
# Создаем приветсвтие
def greet():
    print("Welcome to Tic-Tac-Toe Game!")
    print(" ")
    print("First starts X, second 0!")
    print("")
    print("Good luck!")

greet()

# Создаем матрицу
field = [['-'] * 3 for _ in range(3)]

# Определяем поле
def field_appear(f):
    print("  0 1 2")
    for i in range(len(field)):
        print(str(i), *field[i])


# Запрашивеам координаты и проверяем
def ask_coords(f):
    while True:
        coords = input('Enter the coordinates: ').split()  # введено 2 цифры
        if len(coords) != 2:
            print('Enter two coordinates!')
            continue

        if not(coords[0].isdigit() and coords[1].isdigit()):  # введены цифры
            print('Please, use digits!')
            continue
        x, y = map(int, coords)
        if not (0 <= x <= 2 and 0 <= y <= 2):  # диапазон ввода
            print("Out of range")
            continue
        if field[x][y] != "-":  # доступность клетки
            print("The cell is taken!")
            continue
        break
    return x, y

# проверка на выйгрышную комбинацию
def win(f, u):
    def checking(x1, x2, x3, user):
        if x1 == user and x2 == user and x3 == user:
            return True
        for i in range(3):
            if checking(f[i][0], f[i][1], f[i][2], user) or checking(f[0][i], f[1][i], f[2][i], user) or \
                    checking(f[0][0], f[1][1], f[2][2], user) or checking(f[2][0], f[1][1], f[0][2], user):
                return True
    return False


# складываем

field = [['-'] * 3 for _ in range(3)]
count = 0
while True:
    if count == 9:  # проверка на количество ходов
        print("The Game is over! It's a tie!")
        break
    if count % 2 == 0:  # определение очередности хода
        user = 'x'
    else:
        user = '0'
    field_appear(field)
    x, y = ask_coords(field)
    field[x][y] = user
    count += 1
    if win(field, user):   # добавляем проверку
        print(f'{user} has won the Game!')
        field_appear(field)
        break





