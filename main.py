import missile_collection
from tkinter import *
import tanks_collection
import World
import texture

KEY_LEFT , KEY_RIGHT , KEY_UP , KEY_DOWN = 37 , 39 , 38 , 40
KEY_W = 87
KEY_S = 83
KEY_A = 65
KEY_D = 68
FPS = 60

def update():
    tanks_collection.update()
    missile_collection.update()
    player = tanks_collection.get_player()
    World.set_camera_xy(player.get_x()-World.SCREEN_WIDTH//2 + player.get_size()//2 , player.get_y()-World.SCREEN_HEIGHT//2 + player.get_size()//2)
    World.update_map()
    w.after(1000//FPS, update)



def key_press(event):
    player = tanks_collection.get_player()
    if player.is_destroyed():
        return
    elif event.keycode == KEY_W:
         player.forward()
    elif event.keycode == KEY_S:
        player.backward()
    elif event.keycode == KEY_A:
        player.left()
    elif event.keycode == KEY_D:
        player.right()
    elif event.keycode == KEY_UP:
        World.move_camera(0 , -5)
    elif event.keycode == KEY_DOWN:
        World.move_camera(0, 5)
    elif event.keycode == KEY_LEFT:
        World.move_camera(-5 , 0)
    elif event.keycode == KEY_RIGHT:
        World.move_camera(5 , 0)
    elif event.keycode == 32:
        player.fire()

def load_textures():
    texture.load("tank_down", "img/tank_down.png")
    texture.load("tank_up", "img/tank_up.png")
    texture.load("tank_left", "img/tank_left.png")
    texture.load("tank_right", "img/tank_right.png")

    texture.load("tank_down_player", "img/tank_down_player.png")
    texture.load("tank_up_player", "img/tank_up_player.png")
    texture.load("tank_left_player", "img/tank_left_player.png")
    texture.load("tank_right_player", "img/tank_right_player.png")
    texture.load("tank_destroy_player", "img/tank_destroy.png")

    texture.load(World.BRICK,"img/brick.png")
    texture.load(World.WATER,"img/water.png")
    texture.load(World.CONCRETE, "img/wall.png")
    texture.load(World.MISSLE, "img/bonus.png")

    texture.load(World.FUEL, "img/топливо.png")
    texture.load(World.SERDZE, "img/сердце.png")
    texture.load(World.OPIT, "img/золотое-яблоко.png.png")
    #texture.load(World.NOEX, "img/анонимус.png")
    texture.load(World.SPEED,"img/скорость_я_скорость.png")

    texture.load('missile_up', 'img/missile_up.png')
    texture.load('missile_down', 'img/missile_down.png')
    texture.load('missile_left', 'img/missile_left.png')
    texture.load('missile_right', 'img/missile_right.png')

w = Tk()
load_textures()
w.title("танки на минималках")
canv = Canvas(w , width= World.SCREEN_WIDTH , height= World.SCREEN_HEIGHT , bg= "green")
canv.pack()
World.initialaze(canv)
tanks_collection.initialize(canv)
missile_collection.initielize(canv)

w.bind("<KeyPress>", key_press)
update()
w.mainloop()
