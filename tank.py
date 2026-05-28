from hitbox import Hitbox
from tkinter import *
from  random import randint
import World
import texture as skin
class Tank:
    __count = 0
    #__SIZE = 100

    def __init__(self ,canvas, x , y, model = 'Т-14 nug' , ammo = 100 , speed = 10,
            #file_up = "../img/tankT34_up.png",
            #file_down = "../img/tankT34_down.png",
            #file_left = "../img/tankT34_left.png",
            #file_right = '../img/tankT34_right.png' ,
            bot = True):
        self.__bot = bot
        self.__target = None
        #self.__skin_up = PhotoImage(file = file_up)
        #self.__skin_down = PhotoImage(file=file_down)
        #self.__skin_left = PhotoImage(file=file_left)
        #self.__skin_right = PhotoImage(file=file_right)
        self.__hitbox = Hitbox(x, y, self.get_sise(), self.get_sise() , padding= 2)
        self.__canvas = canvas
        Tank.__count += 1
        self.__model = model
        self.__hp = 100
        self.__xp = 0
        self.__ammo = ammo
        self.__fuel = 10000
        self.__speed = speed
        self.__x = x #
        self.__y = y #
        self.__vx = 0
        self.__vy = 0
        self.__dx = 0
        self.__dy = 0
        if self.__x < 0:
            self.__x = 0
        if self.__y <0:
            self.__y = 0
        self.__create()
        self.__usual_speed = speed
        self.__super_speed = speed*2
        self.__water_speed = speed/2
        self.__oldspeed = self.__speed
        self.__s = 0
        self.__in_water = 0

        #self.__right()

    def __set_x2_speed(self):
        if self.__s  == 0:
            self.__set_super_speed()
            self.__s =+1




    def __take_ammo(self):
        self.__ammo += 10
        if self.__ammo > 100:
            self.__ammo = 100

    def __take_fuel(self):
        self.__fuel += 10
        if self.__fuel > 10000:
            self.__fuel = 100

    def __take_SERDZE(self):
        self.__hp += 10
        if self.__hp > 100:
            self.__hp = 100

    def __take_OPIT(self):
        self.__xp += 10

    def __set_usual_speed(self):
        self.__speed = self.__usual_speed

    def __set_super_speed(self):

        self.__speed = self.__super_speed


    def __set_water_speed(self):
        self.__speed = self.__water_speed

    def __check_map_collision(self):
        details = {}
        #self.__set_usual_speed()
        result = self.__hitbox.check_map_collision(details)
        if result:
            self.__on_map_collision(details)
            return True
        return False
    def __on_map_collision(self,details):

        if World.WATER in details and len(details) == 1:

            if self.__in_water == 0:
                self.__in_water = 1
                print('Въехал в воду')
                self.__oldspeed = self.__speed
                self.__set_water_speed()
                print(self.__speed)
            else:
                self.__speed = self.__oldspeed
        elif World.MISSLE in details:
            pos = details[World.MISSLE]
            if World.take(pos["row"],pos["col"])!= World.AIR:
                self.__take_ammo()
        elif World.FUEL in details:
            pos = details[World.FUEL]
            if World.take(pos["row"],pos["col"])!= World.AIR:
                self.__take_fuel()
        elif World.SERDZE in details:
            pos = details[World.SERDZE]
            if World.take(pos["row"],pos["col"])!= World.AIR:
                self.__take_SERDZE()
        elif World.OPIT in details:
            pos = details[World.OPIT]
            if World.take(pos["row"],pos["col"])!= World.AIR:
                self.__take_OPIT()
        #elif World.NOEX in details:
        #    pos = details[World.NOEX]
        #    if World.take(pos["row"],pos["col"])!= World.AIR:
        #        World.destroy_blocks()
        elif World.SPEED in details:
            pos = details[World.SPEED]
            if World.take(pos["row"], pos["col"]) != World.AIR:
                self.__set_x2_speed()
        else:
            self.__undo_move()
            if self.__bot:
                self.__AI_change_orientation()

    def __check_out_of_world(self):
        if self.__hitbox.left < 0 or self.__hitbox.top < 0 or self.__hitbox.right >= World.get_width() or self.__hitbox.bottom >= World.get_height():
            self.__undo_move()
            if self.__bot:
                self.__AI_change_orientation()

    def fire(self):
        if self.__ammo > 0:
            self.__ammo -= 1
        print('стрельба')

    def forward(self):
        self.__vx = 0
        self.__vy = -1
        self.__canvas.itemconfig(self.__id, image=skin.get("tank_up"))
            #self.__repaint()
            #print(self)

    def backward (self):
        self.__vx = 0
        self.__vy = 1
        self.__canvas.itemconfig(self.__id, image=skin.get("tank_down"))
            #self.__repaint()
            #print(self)

    def left (self):
        self.__vx = -1
        self.__vy = 0
        self.__canvas.itemconfig(self.__id, image=skin.get("tank_left"))
            #self.__repaint()
            #print(self)

    def right(self):
        self.__vx = 1
        self.__vy = 0
        self.__canvas.itemconfig(self.__id,image = skin.get("tank_right"))
            #self.__repaint()
            #print(self)

    def __AI(self):
        if randint (1,30) == 1:
            if randint(1 , 10) < 9 and self.__target is not  None:
                self.__AI_goto_target()
            else:
                self.__AI_change_orientation()

    def set_target(self,target):
        self.__target = target

    def __AI_goto_target(self):
        if randint(1 , 2) == 1:
            if self.__target.get_x() < self.get_x():
                self.left()
            else:
                self.right()
        else:
            if self.__target.get_y() < self.get_y():
                self.forward()
            else:
                self.backward()

    def __AI_change_orientation(self):
        rand = randint(0,3)
        if rand == 0:
            self.left()
        if rand == 1:
            self.right()
        if rand == 2:
            self.forward()
        if rand == 3:
            self.backward()

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_ammo(self):
        return self.__ammo

    def get_model(self):
        return self.__model

    def get_hp(self):
        return self.__hp

    def get_xp(self):
        return self.__xp

    def get_fuel(self):
        return self.__fuel

    def get_speed(self):
        return self.__speed

    @staticmethod
    def get_quantity():
        return Tank.__count

    #@staticmethod
    def get_sise(self):
        return skin.get("tank_up").width()

    def update(self):

        if self.__fuel > self.__speed:
            if self.__bot:
                self.__AI()
            if (not self.__check_map_collision()):
                if (self.__in_water == 1):
                    print('Выехал из воды')
                    self.__in_water = 0
                    self.__speed = self.__oldspeed
                    print(self.__speed)
            self.__dx = self.__vx * self.__speed
            self.__dy = self.__vy * self.__speed
            self.__x += self.__dx
            self.__y += self.__dy
            self.__fuel -= self.__speed
            self.__update_hitbox()
            self.__check_out_of_world()

            self.__repaint()

    def __undo_move(self):
        if self.__dx == 0 and self.__dy == 0:
            return
        self.__x -= self.__dx
        self.__y -= self.__dy
        self.__update_hitbox()
        self.__repaint()
        self.__dx = 0
        self.__dy = 0

    def __create(self):
        #self.id = self.__canvas.create_rectangle(self.__x, self.__y, self.__x + Tank.__SIZE, self.__y + Tank.__SIZE, fill="red")
        self.__id = self.__canvas.create_image(self.__x,self.__y, image = skin.get("tank_up"),anchor ='nw')

    def __repaint(self):
        self.__canvas.moveto(self.__id, x = World.get_screen_x(self.__x), y = World.get_screen_y(self.__y))

    def __update_hitbox(self):
        self.__hitbox.moveto(self.__x, self.__y)

    def intersects(self,other_tank):
        value = self.__hitbox.intersects(other_tank.__hitbox)
        if value:
            self.__undo_move()
            if self.__bot:
                self.__AI_change_orientation()
        return value

    def __del__(self):
        print("танк удален")
        try:
            self.__canvas.delete(self.__id)
        except Exception:
            pass

    def __str__(self):
        return (f"координаты: x = {self.__x} , y = {self.__y} , модель: {self.__model} , боеприпасы : {self.__ammo}")

#player = Tank(100,50,"W-12 сёмга",100,10)

#player.fire()
#player.forward()
#player.backward()
#player.backward()
#player.left()
#player.right()
#print(player)