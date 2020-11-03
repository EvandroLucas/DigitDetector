from OpenGL.GL import *
from OpenGL.GLU import *
import sys
import math
from egl import *
from coord import *

class Rotation:

    def __init__(self,up,down,right,left):
        self.up = up
        self.down = down 
        self.right = right
        self.left = left

class Camera :

    def round_all(self):
        self.pos.round()
        self.aim.round()
        self.up.round()

    def __init__(self,pos_tuple,aim_tuple,up_tuple):
        self.pos = Coord(pos_tuple[0],pos_tuple[1],pos_tuple[2])
        self.aim = Coord(aim_tuple[0],aim_tuple[1],aim_tuple[2])
        self.up  = Coord( up_tuple[0], up_tuple[1], up_tuple[2])        
        self.pos_mov = Coord(0,0,0)
        self.aim_mov = Coord(0,0,0)
        self.up_mov  = Coord(0,0,0)

        self.looking = Rotation(0,0,0,0)


    def look(self):
        gluLookAt(self.pos.x,self.pos.y,self.pos.z,
                self.aim.x,self.aim.y,self.aim.z,
                self.up.x,self.up.y,self.up.z)

    def move_front_back(self,coord,step=1,z = False):
        self.normalize_aim()
        two_dee_coord = Coord(coord.x,coord.y,0)
        s = math.sqrt( math.pow(two_dee_coord.x,2) + math.pow(two_dee_coord.y,2))
        two_dee_coord.x = two_dee_coord.x / s
        two_dee_coord.y = two_dee_coord.y / s
        xmov = step * two_dee_coord.x
        ymov = step * two_dee_coord.y
        zmov = 0
        if z :
            zmov = step * two_dee_coord.z

        self.pos_mov.x += xmov
        self.pos_mov.y += ymov
        self.pos_mov.z += zmov
        self.aim_mov.x += xmov
        self.aim_mov.y += ymov
        self.pos_mov.z += zmov


    def move_to(self,coord,step=1,z = False):
        self.move_front_back(coord,step = step,z = z)

    def move_against(self,coord,step=1,z = False):
        self.move_front_back(coord,step = step * (-1),z = z)

    def move_right_to(self,coord,step=0.05):
        self.normalize_aim()
        aim_vec = coord - self.pos
        rot_aim = Coord(aim_vec.y,(-1)*aim_vec.x,0)
        two_dee_coord = Coord(rot_aim.x,rot_aim.y,0)
        s = math.sqrt( math.pow(two_dee_coord.x,2) + math.pow(two_dee_coord.y,2))
        two_dee_coord.x = two_dee_coord.x / s
        two_dee_coord.y = two_dee_coord.y / s

        n = self.pos + two_dee_coord
        xmov = step * (n.x -  self.pos.x)
        ymov = step * (n.y -  self.pos.y)

        self.pos_mov.x += xmov
        self.pos_mov.y += ymov
        self.aim_mov.x += xmov
        self.aim_mov.y += ymov

    def move_left_to(self,coord,step=0.05):
        self.move_right_to(self.aim,step = (-1)*step)

    def move_on_axis(self,ammount,axis):
        self.normalize_aim()
        if axis == "x" :
            self.pos_mov.x += ammount
            self.aim_mov.x += ammount
        if axis == "y" :
            self.pos_mov.y += ammount
            self.aim_mov.y += ammount
        if axis == "z" :
            self.pos_mov.z += ammount
            self.aim_mov.z += ammount

    def look_up(self,a):
        self.looking.up = a
    def look_down(self,a):
        self.looking.down = a
    def look_right(self,a):
        self.looking.right = a
    def look_left(self,a):
        self.looking.left = a
    
    def do_look_vertical(self,speed):
        self.normalize_aim()
        step = (speed) * (math.pow(self.pos.z - self.aim.z,3) / 10 + 0.1)
        self.aim.z += step
        self.normalize_aim()

    def do_look_up(self,speed):
        self.do_look_vertical(speed)

    def do_look_down(self,speed):
        self.do_look_vertical(speed * (-1))

    def do_look_horizontal(self,angle):
        self.correct_aim()
        aim_vec = self.aim - self.pos
        a = round(math.radians(angle),4)
        u = round((math.cos(a)*aim_vec.x) - (math.sin(a)*aim_vec.y) ,4)
        v = round((math.sin(a)*aim_vec.x) + (math.cos(a)*aim_vec.y) ,4)
        self.aim = Coord(self.pos.x + u,self.pos.y + v,self.aim.z)
        self.aim.round()
        self.normalize_aim()

    def do_look_right(self,angle):
        self.do_look_horizontal((-1) *angle)

    def do_look_left(self,angle):
        self.do_look_horizontal((angle))


    def normalize_aim(self):
        a = Coord(self.aim.x,self.aim.y,self.aim.z)
        p = Coord(self.pos.x,self.pos.y,self.pos.z)
        v = a - p
        u = v.normalize()
        n = p + u
        self.aim = n

    
    def print_stats(self):
        pos = self.pos
        aim = self.aim
        up = self.up
        posm = self.pos_mov
        aimm = self.aim_mov
        upm= self.up_mov
        # print()
        # print("POS : " + f'({pos.x: .1f} ,{pos.y: .1f},{pos.z: .1f})' + f'({posm.x: .4f} ,{posm.y: .4f},{posm.z: .4f})')
        # print("AIM : " + f'({aim.x: .1f} ,{aim.y: .1f},{aim.z: .1f})' + f'({aimm.x: .4f} ,{aimm.y: .4f},{aimm.z: .4f}), dist : ' + str((self.aim - self.pos).size()))
        # print(" UP : " + f'({up.x: .1f} ,{up.y: .1f},{up.z: .1f})' + f'({upm.x: .4f} ,{upm.y: .4f},{upm.z: .4f})')
        # print("LOK : " + f'(U : {self.looking.up: .1f} , D : {self.looking.down: .1f}, L: {self.looking.left: .1f}), R: {self.looking.right: .1f})')

    def correct_aim(self):
        aim = self.aim
        pos = self.pos
        aim.round(4)
        aim.round(4)
        if aim.x == pos.x and aim.y == pos.y:
            print("Correcting aim...")
            self.aim.x += 000.1
        self.normalize_aim()

    def update(self):
        self.pos += self.pos_mov
        self.aim += self.aim_mov
        self.up  += self.up_mov


        if self.looking.right > 0:
            self.do_look_right(self.looking.right)
            self.normalize_aim()
        if self.looking.left > 0:
            self.do_look_left(self.looking.left)
            self.normalize_aim()
        if self.looking.up > 0:
            self.do_look_up(self.looking.up)
            self.normalize_aim()
        if self.looking.down > 0:
            self.do_look_down(self.looking.down)
            self.normalize_aim()

        self.round_all()

        self.print_stats()

        self.looking = Rotation(0,0,0,0)
        self.pos_mov = Coord(0,0,0)
        self.aim_mov = Coord(0,0,0)
        self.up_mov = Coord(0,0,0)