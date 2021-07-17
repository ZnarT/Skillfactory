#!/usr/bin/env python
# coding: utf-8

# Над проектом работал: Артём Знаменский
# Написать: artem.znamenskii@yandex.ru
#     
#     
# ЮНИТ 0. Введение в Data Science > 
# PYTHON-Итог.Задачи по пройденным темам. > 
# 6. Итоговое практическое задание
#     
#     
# ###    БАЗОВЫЕ ЗАДАЧИ:
# 
#     Плюс напротив задачи значит, что задача выполнена.
#     + 1. Разработать игру "Крестики-нолики";
#     + 2. Размер игрового поля 3x3;
#     + 3. Вывод игры должен осуществляться в консоль;
#     + 4. В коде игры должны применяться "форматированные строки".
#       
# ###    РЕАЛИЗОВАНЫЕ ЗАДАЧИ
#     
#       1. Приём и запоминание имён игроков;
#       2. Обращение по именам к игрокам в момент их хода;
#       3. Принимает координаты ячейки, 
#          в которую игрок хочет поставить симовол;
#       4. Проверяет координаты (входят ли координаты в игровое поле,
#          не занята ли символом ячейка по данному адресу).
# 
#     # ----- Добавлено от 16.07.2021 -----
# 
#       5. Отображение игрового поля (вынесено в отдельную функцию);
#      *6. Реализована очистка консоли
#          (работает только в терминале при запуски файла с расширением ".py");
#       7. Теперь игра определяет победителя
#          (проверка относительно сложная, т.к. сделана с учётом возможного 
#          расширения функционала игры);
#       8. Игра завершается, если есть победитель.
#       9. Игру можно досрочно завершить введя команду "Выход".
# 
#     # ----- Планируется после 16.07.2021 -----
# 
#      10. Есть желание добавить возможность задавать 
#          размер и форму игрового поля игроками.
# 
# ###    ПРОБЛЕМЫ
# 
#       1. Некорректное отображение вывода в терминале VS Code 
#          при исполнении программы с расширением .ipunb
#----------------------------------------------------------------------#
def game_core():
    '''Функция запускает игру крестики-нолики.'''
    
    '''Знакомство с игроками'''
    print("Введите имя игрока, который будет ходить первым:", end = " ")
    player_X = input()
    print("Введите имя игрока, который будет ходить вторым:", end = " ")
    player_O = input()    
    

    '''Создание игрового поля'''
    # Определение осей координат
    # ox,oy = 3,3
    ox,oy = set_field_size()

    # Определение длины выигрышной комбинации
    max_len = ox if ox >= oy else oy
    win_combo = max_len if max_len <= 5 else 5
    
    # Создание пустого поля
    field = [["•" for x in range(ox)] for y in range(oy)]
    
    # Создание и вставка оси координат "Y"
    list(map(lambda line_oy, y: 
             line_oy.insert(0,str(y+1)), 
             field, range(oy)))
    
    # Создание и вставка оси координат "X"
    line_ox = [str(x+1) for x in range(ox)]
    line_ox.insert(0," ")
    field.insert(0,line_ox)
    
    # Показать игровое поле и оси 'X' и 'Y'
    print_field(field)
    
    '''Реализация ходов игроками'''
    # Игрок, который в данный момент совершает ход
    active_player = None
    
    # Игроки поочерёдно делают ходы
    for move in range(ox*oy):

        # Передача инициативы другому игроку и смена знака
        active_player = player_O if active_player == player_X else player_X
        sign = "X" if active_player == player_X else "O"
        
        print(f"Ходит {active_player}.",
              "Укажите координаты хода, через запятую:", end = " ")
        answer = ""

        while answer.lower() != "выход":
            
            # Игрок определят ячейку для ввода знака или выходит из игры
            answer = input()
            
            if answer.lower() == "выход":
                return print(f"{active_player} завершил игру.")

            x, y = map(int, answer.split(","))
            
            # Проверка значений введённых игроком
            if not (1 <= x <= ox) or not (1 <= y <= oy):
                print("Вы указали неверные координаты!",
                      "Введите другие координаты:", end = " ")
            elif field[y][x] != "•":
                print("Это поле занято!",
                      "Введите координаты заново:", end = " ")
            else: break    
        
        # Фиксирование хода на игровом поле
        field[y].pop(x)
        field[y].insert(x, sign)
        
        
        # Показать обновлённое игровое поле и оси 'X' и 'Y'
        print_field(field)
        
        # Поиск победной комбинации
        if check_win_area(field,x,y,ox,oy,win_combo):
            return print(f"{active_player} победил!")


#----------------------------------------------------------------------#
def print_field(field):
    import os
    os.system('cls||clear') # Очистка терминала
    
    # Отображение игрового поля, осей 'X' и 'Y' и хода игрока
    for y in range(len(field)): print(*field[y], sep=' ')

def check_win_area(field,x,y,ox,oy,win_combo):
    '''Функция определяет область, 
    в которой есть возможно обнаружить победную комбинацию.
    '''
    sign = field[y][x]
    
    # Определяем границы области, где возможна выигрышная комбинация
    # (линия) из знаков для горизонтали и вертикали
    x_min = 1 if x-(win_combo-1) <= 1 else x-(win_combo-1)
    x_max = ox if x+(win_combo-1) > ox else x+(win_combo-1)
    
    y_min = 1 if y-(win_combo-1) <= 1 else y-(win_combo-1)
    y_max = oy if y+(win_combo-1) > oy else y+(win_combo-1)
    
    # Считаем знаки по горизонтали
    if count_signs(sign,field,win_combo,
                   x_min,x_max,
                   y,0,
                   x_min,1): return True
    # Считаем знаки по вертикали
    if count_signs(sign,field,win_combo,
                   y_min,y_max,
                   y_min,1,
                   x,0): return True

    # Определяем границы области, где возможна выигрышная комбинация
    # (линия) из знаков для убывающей диагонали
    delta_start = x-x_min if x-x_min <= y-y_min else y-y_min
    delta_finish = x_max-x if x_max-x <= y_max-y else y_max-y

    # Считаем знаки по убывающей диагонали
    if count_signs(sign,field,win_combo,
                   x-delta_start,x+delta_finish,
                   y-delta_start,1,
                   x-delta_start,1): return True

    # Определяем границы области, где возможна выигрышная комбинация
    # (линия) из знаков для растущей диагонали
    delta_start = y_max-y if y_max-y <= x-x_min else x-x_min
    delta_finish = y-y_min if y-y_min <= x_max-x else x_max-x

    # Считаем знаки по растущей диагонали
    if count_signs(sign,field,win_combo,
                   x-delta_start,x+delta_finish,
                   y+delta_start,-1,
                   x-delta_start,1): return True   

    return False

def count_signs(sign,field,win_combo,
                range_start,range_finish,
                y_start,y_changer,
                x_start,x_changer):
    '''Функция ищет выигрышную комбинацию в заданной области.'''
    
    count = 0
    
    for step in range(range_start,range_finish+1):
        
        if field[y_start][x_start] == sign:
            count += 1 
            if count == win_combo:
                return True
        else:
            count = 0
            
        y_start += y_changer
        x_start += x_changer

    return False 

def set_field_size():
    '''Через данную функцию задают размер и форму игрового поля'''

    print("Размери поля не может быть меньше 3х3 и больше 10х10. \n",
          "Укажите размер игрового поля в клетках через запятую X, Y:", end = " ")

    # Просим игрока ввести размер поля до тех пор, 
    # пока не введёт допустимый размер поля
    while True:

        ox, oy = map(int, input().split(","))
        
        # Проверка значений введённых игроком
        if not (3 <= ox <= 10) or not (3 <= oy <= 10):
            print("Вы указали недопустимый размер поля",
                    "Введите другие размеры:", end = " ")
        else: break

    return ox, oy  

#---------------- START GAME ------------------------------------------#
game_core()