from units import Tank
from random import randint
from missile_collection import check_misiles_collision
import World
from tkinter import NW

id_screen_text = 0
_player = None
_tanks = []
_canvas = None
_wave = 1

def initialize(canv):
    global _canvas, id_screen_text
    _canvas = canv
    player = spawn(False)
    _player = player
    enemy = spawn(True).set_target(player)
    spawn(True).set_target(player)
    id_screen_text = _canvas.create_text(10, 10, text=_get_screen_text(),
                                         font=('TkDefaultFont',20, 'bold'),
                                         fill="white", anchor=NW)
    #player = Tank(canvas=canv, x=World.BLOCKSIZE * 2, y=World.BLOCKSIZE * 4, ammo=100, bot=False , speed= 2)
    #player_2 = Tank(canvas=canv, x=World.BLOCKSIZE * 4, y=World.BLOCKSIZE * 6, ammo=100, bot=True , speed= 2)

    #player_2.set_target(player)
    #_tanks.append(player)
    #_tanks.append(player_2)
    # spawn(False)
    # for i in range(1):
    #     spawn(True).set_target(get_player())
def _get_screen_text():
    global _wave
    if get_player().is_destroyed():
        return f"Потрачено , пройдено волн: {_wave - 1} , опыта получено: {0}"
    if len(_tanks) ==1:
        return "Победа"
    return f"Врагов: {len(_tanks) - 1} , волна: {_wave}"

def _update_screen_text():
    _canvas.itemconfig(id_screen_text, text=_get_screen_text())

def get_player():
    return _tanks[0]

def update():
    global _wave
    _update_screen_text()
    #for tank in _tanks:
    #    tank.update()
    #    check_collision(tank)
    start = len(_tanks) - 1
    for i in  range(start , -1 , -1):
        if _tanks[i].is_destroyed() and i != 0:
            del _tanks[i]
            i = i - 1
            if len(_tanks) == 1:
                for e in range(_wave):
                    enemy = spawn(True).set_target(_player)
                    spawn(True).set_target(_player)
                _wave += 1
        else:
            _tanks[i].update()
        check_collision(_tanks[i])
        check_misiles_collision(_tanks[i])

def check_collision(tank):
    for other_tank in _tanks:
        if tank == other_tank:
            continue
        if tank.intersects(other_tank):
            return True
    return False

def spawn(is_bot =True):
    cols = World.get_cols()
    rows = World.get_rows()
    while True:
        col = randint(1,cols - 1)
        row = randint(1,rows - 1)
        if World.get_block(row , col) != World.GROUND:
            continue
        t = Tank(_canvas, row ,col , bot= is_bot)
        if not  check_collision(t):
            _tanks.append(t)
            return  t

#def spawn_enemy():
#    while True:
#        pos_x = randint(200 , 800)
#        pos_y = randint(200 , 600)
#        t = Tank(_canvas , x = pos_x , y = pos_y, speed=1)
#        if not check_collision(t):
#            t.set_target(get_player())
#            _tanks.append(t)
#            return True

