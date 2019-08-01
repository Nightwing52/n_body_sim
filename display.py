import matplotlib.pyplot as plt
import seaborn as sb
import math

def display_term(n, x, y, v_x, v_y, m, t):
    E=0.0
    for i in range(n):
        E+=0.5*m[i]*(v_x[i]**2+v_y[i]**2)
    print("Total energy at time "+str(t)+": "+str(E))

def display_rot_curve(v, r):
    return
