import  texture
from tkinter import NW
from random import randint , choice

_camera_x = 0
_camera_y = 0
GROUND = 'g'
WATER = 'w'
CONCRETE = 'c'
BRICK = 'b'
AIR = 'a'
MISSLE = 'm'
FUEL = "f"
SERDZE = "s"
OPIT = "o"
NOEX = "n"
SPEED = "v"
BLOCKSIZE = 64
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
#WIDTH = SCREEN_WIDTH * 6
#HEIGHT = SCREEN_HEIGHT * 6
_canvas = None
_map = []

def load_map(file_name):
    global  _map
    _map = []
    with open(file_name) as f:
        i = 0
        for  line in f:
            bloks = line.strip().replace('\t','')
            row = []
            for j in range(len(bloks)):
                cell = _Cell(_canvas, bloks[j],j * BLOCKSIZE, i * BLOCKSIZE)
                row.append(cell)
            _map.append(row)
            i +=1
        #print(_map)



def initialaze(canv):
    global _canvas
    _canvas = canv
    #load_map('../map/2.tmap')
    create_map(20,20)

def create_map(rows = 20 , cols = 20):
    global _map
    _map = []
    for i in range(rows):
        row = []
        for j in range(cols):
            block = GROUND
            if i ==0 or j ==0 or i == rows-1 or j == cols-1:
                block = CONCRETE
            elif randint(1 , 100)<= 35:
                block = choice([BRICK,WATER,CONCRETE , MISSLE , FUEL , SERDZE , OPIT , SPEED])
            cell = _Cell(_canvas,block,BLOCKSIZE * j,BLOCKSIZE * i)
            row.append(cell)
        _map.append(row)

def update_map(all=False):
    first_row = get_row(_camera_y)
    last_row = get_row(_camera_y + SCREEN_HEIGHT) + 1
    first_col = get_col(_camera_x)
    last_col = get_col(_camera_x + SCREEN_HEIGHT) + 1
    if all:
        first_row = 0
        first_col = 0
        last_row = get_rows()-1
        last_col = get_cols()-1
    for i in range(first_row,last_row+1):
        for j in  range(first_col,last_col+1):
            update_cell(i,j)

def get_row(y):
    return int(y)//BLOCKSIZE

def get_col(x):
    return  int(x)//BLOCKSIZE

def set_camera_xy(x , y):
    global _camera_x , _camera_y
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    if x > get_width() - SCREEN_WIDTH:
        x = get_width() - SCREEN_WIDTH
    if y > get_height() - SCREEN_HEIGHT:
        y = get_height() - SCREEN_HEIGHT
    update_all = False
    if abs(_camera_x - x)>= BLOCKSIZE or abs(_camera_y-y)>= BLOCKSIZE:
        update_all = True
    _camera_x = x
    _camera_y = y
    if update_all:
        update_map(all=True)

def get_rows():
    return len(_map)

def get_cols():
    return len(_map[0])

def get_width():
    return get_cols() * BLOCKSIZE

def get_height():
    return get_rows() * BLOCKSIZE

def move_camera(delta_x , delta_y):
    set_camera_xy(_camera_x + delta_x , _camera_y + delta_y)

def get_screen_x(world_X):
    return world_X - _camera_x

def get_screen_y(world_Y):
    return world_Y - _camera_y

def get_block(row,col):
    if _inside_of_map(row, col):
        return _map[row][col].get_block()
    return AIR

def update_cell(row , col):
    if _inside_of_map(row,col):
        _map[row][col].update()

def destroy(row,col):
    if row < 1 or col < 1 or row >= get_rows()-1 or col >= get_cols()-1:
        return False
    return _map[row][col].destroy()


def _inside_of_map(row,col):
    if row < 0 or col < 0 or row >= get_rows() or col >= get_cols():
        return False
    return True

def take(row,col):
    if _inside_of_map(row, col):
        return  _map[row][col].take()
    return  AIR

def destroy_blocks():

    for i in range(len(_map)):
        for j in range(len(_map[i])):
            if _map[i][j]=="b":
                _map[i][j]="g"
    update_map(True)
    #print(_map)

class _Cell:
    def __init__(self, canvas,block,x,y):
        self.__canvas = canvas
        self.__block = block
        self.__screen_x = get_screen_x(x)
        self.__screen_y = get_screen_y(y)
        self.__x = x
        self.__y = y
        self.__create_element(block)

    def _take_NOEX(self):
        block = self.get_block()
        if block == self.BRICK:
            self.set_block(GROUND)
            return block
        else:
            return AIR

    def take(self):
        block = self.get_block()
        #print(block)
        if block == MISSLE or block == FUEL or block == SERDZE or block == OPIT or block == NOEX or block == SPEED:
            self.set_block(GROUND)
            return block
        else:
            return AIR

    def __create_element(self,block):
        if block != GROUND:
            self.__id = self.__canvas.create_image(self.__screen_x , self.__screen_y, image = texture.get(block), anchor=NW)

    def __del__(self):
        try:
            self.__canvas.delete(self.__id)
        except:
            self.__delete_element()

    def set_block(self,block):
        if self.__block == block:
            return
        elif block == GROUND:
            self.__delete_element()
        elif self.__block == GROUND:
            self.__create_element(block)
        else:
            self.intemconfig(self.__id, image = texture.get(block))
        self.__block = block

    def destroy(self):
        if self.get_block() == BRICK:
            self.set_block(GROUND)
            return True
        return False

    def __delete_element(self):
        try:
            self.__canvas.delete(self.__id)
        except:
            pass

    def get_block(self):
        return self.__block

    def update(self):
        if self.__block == GROUND:
            return
        screen_x = get_screen_x(self.__x)
        screen_y = get_screen_y(self.__y)
        if self.__screen_x == screen_x and self.__screen_y == screen_y:
            return
        self.__canvas.moveto(self.__id,x = screen_x, y = screen_y)
        self.__screen_x = screen_x
        self.__screen_y = screen_y
