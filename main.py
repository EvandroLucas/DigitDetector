import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np
import math
import random
import sys
import random
from random import randrange
from camera import *

from egl import *

from predict import *


def drawText(position, textString, size):     
    pygame.init() # now use display and fonts
    font = pygame.font.Font (None, size)
    textSurface = font.render(textString, True, (0,0,0,0),(255,255,255,255))     
    textData = pygame.image.tostring(textSurface, "RGBA", True)     
    glRasterPos3d(*position)   
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)


def draw_ground(size,color,height):
    eglSetHexColor(color)
    glBegin(GL_POLYGON)     
    glVertex3f(size,size*(-1),height)
    glVertex3f(size*(-1),size*(-1),height)
    glVertex3f(size*(-1),size,height)
    glVertex3f(size,size,height)
    glEnd()

def draw_tile(row,col,height = 0.01, color=COLOR_BLACK):
    y = 14 - row
    x = -14 + col -1
    p1 = (x,y,height)
    p2 = (x+1,y,height)
    p3 = (x+1,y+1,height)
    p4 = (x,y+1,height)
    eglRectangle(p1,p2,p3,p4,color)

def centered(number_mat):
    # First we find the center of mass: 
    cm = [0,0]
    size = 0
    for i, row in enumerate(number_mat):
        for j, num in enumerate(row):
            if 0 < num <= 1:
                size += 1
    for i, row in enumerate(number_mat):
        for j, num in enumerate(row):
            if 0 < num <= 1:
                cm[0] += i/size
                cm[1] += j/size

    new_mat = np.zeros((28,28))
    h_shift = int(14 - cm[0])
    v_shift = int(14 - cm[1])
    for i, row in enumerate(number_mat):
        for j, num in enumerate(row):
            new_i = i + h_shift
            new_j = j + v_shift
            if 0 < new_i < 28 and 0 < new_j < 28:
                new_mat[new_i][new_j] = num

    return new_mat

def main():

    predictor = Predictor(model = "MLPClassifier")
    curr_pred = "MLPClassifier"
    number_mat = np.zeros((28,28))

    max_frequency = 4
    freq = 0

    display = (800,600)
    pygame.display.set_mode(display,DOUBLEBUF|OPENGL)
    pygame.mouse.set_visible(True)

    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0]/display[1]), 0.1, 1000)
    view_mat = np.matrix(np.identity(4), copy=False, dtype='float32')
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glGetFloatv(GL_MODELVIEW_MATRIX, view_mat)
    glLoadIdentity()

    camera = Camera( (10,0,50) , (10,0.1,0) , (0,0,1) )
    camera.correct_aim()

    while True:
        glMatrixMode(GL_MODELVIEW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_SPACE:
                    number_mat = np.zeros((28,28))
                if event.key == pygame.K_0:
                    predictor = Predictor(model = "Perceptron")
                    curr_pred = "Perceptron"
                if event.key == pygame.K_1:
                    predictor = Predictor(model = "GaussianNB")
                    curr_pred = "GaussianNB"
                if event.key == pygame.K_2:
                    predictor = Predictor(model = "LinearSVM")
                    curr_pred = "LinearSVM"
                if event.key == pygame.K_3:
                    predictor = Predictor(model = "MLPClassifier")
                    curr_pred = "MLPClassifier"
                if event.key == pygame.K_4:
                    predictor = Predictor(model = "RBF_SVM")
                    curr_pred = "RBF_SVM"
                if event.key == pygame.K_5:
                    predictor = Predictor(model = "DecisionTreeClassifier")
                    curr_pred = "DecisionTreeClassifier"
                if event.key == pygame.K_6:
                    predictor = Predictor(model = "GradientBoostingClassifier")
                    curr_pred = "GradientBoostingClassifier"
                if event.key == pygame.K_7:
                    predictor = Predictor(model = "AdaBoostClassifier")
                    curr_pred = "AdaBoostClassifier"
                if event.key == pygame.K_8:
                    predictor = Predictor(model = "PassiveAggressiveClassifier")
                    curr_pred = "PassiveAggressiveClassifier"
                if event.key == pygame.K_9:
                    predictor = Predictor(model = "NearestCentroid")
                    curr_pred = "NearestCentroid"
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    number_mat = centered(number_mat)
                

        glPushMatrix()
        glLoadIdentity()
        glMultMatrixf(view_mat)
        glGetFloatv(GL_MODELVIEW_MATRIX, view_mat)

        t = eglHexToTuple("#FFFFFF")
        glClearColor(t[0],t[1],t[2],1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        camera.update()
        camera.look()

        pos = pygame.mouse.get_pos()
        posx = math.floor((pos[0] - 52) * (28/400)) + 1
        posy = math.floor((pos[1] - 98) * (28/400)) + 1
        truepos = [posx,posy]
        pressed1, pressed2, pressed3 = pygame.mouse.get_pressed()

        if 1 <= posx <= 28 and 1 <= posy <= 28:
            pygame.mouse.set_visible(False)
            draw_tile(posy,posx,color= "#00DA99")
            draw_tile(posy,posx+1,color= "#14FFB9")
            draw_tile(posy+1,posx,color= "#14FFB9")
            draw_tile(posy,posx-1,color= "#14FFB9")
            draw_tile(posy-1,posx,color= "#14FFB9")
            draw_tile(posy+1,posx+1,color= "#82FFDA")
            draw_tile(posy-1,posx-1,color= "#82FFDA")
            draw_tile(posy-1,posx+1,color= "#82FFDA")
            draw_tile(posy+1,posx-1,color= "#82FFDA")
        else:
            pygame.mouse.set_visible(True)

        def fill_brush(x,y,value):
            if 1 <= x <= 28 and 1 <= y <= 28:
                v = number_mat[x-1][y-1] + value
                number_mat[x-1][y-1] = max(0,min(v,1))
                draw_tile(x,y,color= COLOR_PINK)

        if pressed1: 
            fill_brush(posy,posx,1)
            fill_brush(posy,posx+1,0.5)
            fill_brush(posy+1,posx,0.5)
            fill_brush(posy,posx-1,0.5)
            fill_brush(posy-1,posx,0.5)

            fill_brush(posy+1,posx+1,0.3)
            fill_brush(posy-1,posx-1,0.3)
            fill_brush(posy-1,posx+1,0.3)
            fill_brush(posy+1,posx-1,0.3)
        elif pressed3: 
            fill_brush(posy,posx,-1)
            fill_brush(posy,posx+1,-1)
            fill_brush(posy+1,posx,-1)
            fill_brush(posy,posx-1,-1)
            fill_brush(posy-1,posx,-1)
            fill_brush(posy+1,posx+1,-1)
            fill_brush(posy-1,posx-1,-1)
            fill_brush(posy-1,posx+1,-1)
            fill_brush(posy+1,posx-1,-1)


        drawText((18,8,0),"PREDICTION: ",50)
        if freq < max_frequency:    
            pred = predictor.predict_from_matrix(centered(number_mat))
            freq += 2
        else:
            freq -= 1
        drawText((25,0,0),str(pred),100)

        drawText((-7,14.5,0),"Draw a single digit :  ",32)
        drawText((-13,-17,0),"Current Classifier : " + curr_pred,32)
        drawText((17,-7,0),"Instructions :  ",32)
        drawText((19,-9,0),"- Draw  : LEFT_CLICK ",27)
        drawText((19,-11,0),"- Erase : RIGHT_CLICK ",27)
        drawText((19,-13,0),"- Clear : SPACE ",27)
        drawText((19,-15,0),"- Center : SHIFT ",27)
        drawText((19,-17,0),"- Change Classifier : 0..9 ",27)

        draw_ground(14,"#D9D9D9",0)

        for i, row in enumerate(number_mat):
            for j, num in enumerate(row):
                if 0 < num <= 1:
                    c = max(0,200 - (num*255))
                    color = eglTupleToHex((c,c,c,255))
                    draw_tile(i+1,j+1,color = color)


        glPopMatrix()

        pygame.display.flip()
        pygame.event.pump()

if __name__ == "__main__":
    main()