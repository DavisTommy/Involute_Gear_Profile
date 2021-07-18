#!/usr/bin/env python
# coding: utf-8

# In[5]:


import matplotlib.pyplot as plt
import math
import numpy as np


def arc(r,a1,a2):   #To draw the addendum & dedendum arc
    cords =np.array([[],[]])
    for a in np.arange(a1,a2,.01):
        cords =np.append(cords,[[r*math.cos(a)],[r*math.sin(a)]], axis=1)
    return cords

def radial(th,r1,r2):  #To draw a radial line from r1 to r2
    cords =np.array([[],[]])
    for r in np.arange(r1,r2,0.01):
        cords =np.append(cords,[[r*math.cos(th)],[r*math.sin(th)]], axis=1)
    return cords

def rot_matrix(th):   #Rotational Matrix
    return [[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]]


N = 20
m = 10
phi = 20* math.pi / 180
bw = 17.63
rp = m * N / 2
rb = rp * math.cos(phi)
rd = rp - 1.25 * m
ra = rp + m
b_angle = 17.63/ rb

up = np.array([[],[]])     
down = np.array([[],[]])
gear_cord = np.array([[],[]])
tooth_cord = np.array([[],[]])

t=0;
#Construction of concave up part of the gear
while True:
    x = rb* (math.cos(t) + t* math.sin(t))
    y = rb* (math.sin(t) - t* math.cos(t))
    if (rd*rd <= x*x + y*y <= ra*ra):
        up = np.append(up, [[x], [y]], axis=1)
    elif (x*x + y*y > ra*ra):
        t_1 = math.atan(y / x)
        break
    t += 0.001
#Construction of Concave down part of teeth
down = np.flip(np.dot(rot_matrix(b_angle), [up[0], up[1] * -1]), 1)  #taking the mirror image and rotating it by base angle and flipping it    


# Construction of tooth profile
if rd < rb:
    tooth_cord = radial(0, rd, rb)  # line connecting dedentum circle and base circle

tooth_cord = np.concatenate((tooth_cord, up, arc(ra, t_1, b_angle - t_1), down), axis=1)  # Tooth part



if rd < rb:
    tooth_cord = np.concatenate((tooth_cord, radial(b_angle, rd, rb)), axis=1)# line connecting base circle and dedendum circle

tooth_cord = np.concatenate((tooth_cord, arc(rd, b_angle, 2 * math.pi / 20)), axis=1)  # Dedendum arc


# Construction of 20 tooths
for i in range(N):
    rot = i * 2 * math.pi / N
    gear_cord = np.concatenate((gear_cord, np.dot(rot_matrix(rot), tooth_cord)), axis=1)

# Plotting gear profile
plt.plot(gear_cord[0], gear_cord[1])
plt.show()


# In[ ]:




