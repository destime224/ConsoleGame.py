#!/bin/python
from os import system, uname
from colorama import Fore # Колары

# Не судите за грязь
# Это python

R = Fore.RED # Красный цвет
G = Fore.GREEN # Зелёный цвет
RE = Fore.RESET # Сброс цвета

class Entity: # Класс сущности
    def __init__(self,x,y,ty): # Координаты и значок
        self.__x = x
        self.__y = y
        self.type = ty

    @property
    def position(self): # Свойство для координат
        return self.__x, self.__y

    # Я знаю, что надо было просто позволить доставать
    # x и y, а не городить свойства. Я потом это осознал

    @position.setter
    def position(self,pos): # Сеттер
        self.__x, self.__y = pos

class Player(Entity): # Класс игрока
    def getKey(self): # Ввод для игрока
        anw = input(":")
        return anw

class Enemy(Entity): # Класс врагов
    def __init__(self,x,y,ty,cy=None):
        super().__init__(x,y,ty) # Выполняем init родителя
        self.__cycle = 0
        self.__cycleMap = cy

    def doCycle(self): # Следуем маршруту
        # Если маршрута нет, то просто передаём None
        if not(self.__cycleMap is None):
            if self.__cycle == len(self.__cycleMap):
                self.__cycle = 0
            Map.entityMove(self,self.__cycleMap[self.__cycle][0],
                    self.__cycleMap[self.__cycle][1])
            self.__cycle += 1

class Map: # Класс карты (не имеет объектов)
    PLAYER = Player(1,1,"@") # Представление игрока
    WIN = Entity(10,8,G+"$"+RE) # Представление доллара
    ENEMIES_CYCLE = [ # Пути для врагов (должны быть цикличны)
            ((1,0),(0,-1),(0,-1),(-1,0),(-1,0),(0,1),(0,1),(1,0)),
            ((0,1),(1,0),(-1,0),(0,-1),(0,-1),(-1,0),(1,0),(0,1)),
            ((0,-1),(1,0),(-1,0),(0,1))]
    ENEMIES = ( # Представление врагов (в кортеже)
            Enemy(2,4,R+"&"+RE,ENEMIES_CYCLE[0]), 
            Enemy(6,5,R+"&"+RE,ENEMIES_CYCLE[1]),
            Enemy(9,1,R+"&"+RE,ENEMIES_CYCLE[2]))

    MAP = [ # Представление карты
            ["#","#","#","#","#","#","#","#","#","#","#","#"],
            ["#"," "," ","#"," "," ","#"," "," "," ","#","#"],
            ["#"," "," ","#"," "," "," "," "," "," "," ","#"],
            ["#","#"," ","#","#"," "," ","#","#","#"," ","#"],
            ["#"," "," "," ","#","#"," "," ","#"," "," ","#"],
            ["#"," ","#"," ","#"," "," "," ","#"," ","#","#"],
            ["#"," "," "," ","#"," "," ","#","#"," "," ","#"],
            ["#"," ","#","#","#"," "," "," ","#","#"," ","#"],
            ["#"," "," "," "," "," ","#"," ","#"," "," ","#"],
            ["#","#","#","#","#","#","#","#","#","#","#","#"]
        ]
    # Отображение объектов на карте
    MAP[PLAYER.position[1]][PLAYER.position[0]] = PLAYER.type
    MAP[WIN.position[1]][WIN.position[0]] = WIN.type
    for en in ENEMIES:
        MAP[en.position[1]][en.position[0]] = en.type

    def __init__(): # Защита от создания карт-объектов
        raise SyntaxError("This class cannot have a objects")

    @staticmethod
    def clear(): # Очистка экрана
        if uname()[0] == "Windows":
            system("CLS") # Для Windows
        else:
            system("clear") # Для Mac и Linux

    @classmethod
    def draw(cls): # Отображение карты на консоле
        cls.clear()
        text = "\n "
        for y in cls.MAP:
            for x in y:
                text += x
            print(text)
            text = " "

    @classmethod
    def entityMove(cls,ent,dx,dy): # Перемещение сущностей
        if cls.MAP[ent.position[1]-dy][ent.position[0]+dx] != "#":
            if ent.type == cls.MAP[ent.position[1]][ent.position[0]]:
                cls.MAP[ent.position[1]][ent.position[0]] = " "
            cls.MAP[ent.position[1]-dy][ent.position[0]+dx] = ent.type
            ent.position = (ent.position[0]+dx,ent.position[1]-dy)

    @classmethod
    def enemyDoCycle(cls): # Выполнение маршрута для врагов
        for en in cls.ENEMIES:
            en.doCycle()

    @classmethod
    def winOrLose(cls): # Проверка для победы или проигрыша
        if cls.PLAYER.position == cls.WIN.position:
            cls.draw()
            input("You win! Enter any key to exit: ")
            quit()
        for en in cls.ENEMIES:
            if cls.PLAYER.position == en.position:
                cls.draw()
                input("You lose. Enter any key to exit: ")
                quit()

    @classmethod
    def start(cls): # Начатие цикла
        cls.draw()
        print("Take a dollar to win.\nu - up\nd - down\nr - right\nl - left") # Обучение
        # Цикл в try для очистки при выходе с игры
        try:
            while True:
                anw = cls.PLAYER.getKey() # Достаём вход
                if anw == "u":
                    cls.entityMove(cls.PLAYER,0,1)
                elif anw == "d":
                    cls.entityMove(cls.PLAYER,0,-1)
                elif anw == "l":
                    cls.entityMove(cls.PLAYER,-1,0)
                elif anw == "r":
                    cls.entityMove(cls.PLAYER,1,0)
                cls.enemyDoCycle()
                cls.winOrLose()
                cls.draw()
        except (SystemExit, EOFError, KeyboardInterrupt):
            cls.clear()

Map.start() # Старт
