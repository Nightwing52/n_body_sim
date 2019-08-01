import math
import random
import numpy as np
from barn_hut import *
from display import *

tau=2*math.pi

def vel_verlet(n, t_total, delta_t, x_0, y_0, v_0x, v_0y, m):
    x, y, v_x, v_y, a_x, a_y=x_0, y_0, v_0x, v_0y, np.zeros(n), np.zeros(n)

    t=0.0
    n=0
    while t < t_total:
        head=Tree.build_tree(n, x, y, m)
        for i in range(n):
            a_prime=head.find_force(x[i], y[i])
            a_xprime=a_prime[0]
            a_yprime=a_prime[1]
            x[i]+=v_x[i]*delta_t+0.5*a_xprime*delta_t**2
            y[i]+=v_y[i]*delta_t+0.5*a_yprime*delta_t**2
            v_x[i]+=0.5*(a_xprime+a_x[i])*delta_t
            v_y[i]+=0.5*(a_yprime+a_y[i])*delta_t
            a_x[i]=a_xprime
            a_y[i]=a_yprime
        if n % 10 == 0:
            display_term(n, x, y, v_x, v_y, m, t)
            COM=head.__get_COM__()
            print("COM_x: "+str(COM[0])+" COM_y: "+str(COM[1]))
        t+=delta_t
        n+=1
        
def gen_exp_disk(n, M, a, dr=0.001):
    num=0
    m, x, y, v_x, v_y=np.zeros(n), np.zeros(n), np.zeros(n), np.zeros(n), np.zeros(n)
    sigma_max=(M*math.e)/(2*math.pi*a**2*(math.e-2))
    while num < n:
        sigma_i=sigma_max*random.random()
        r_i=a*random.random()
        if sigma_i <= sigma_max*math.exp(-r_i/a): #good sample
            m_i=sigma_max*2*math.pi*r_i*math.exp(-r_i/a)*dr #mass of thin disk
            m[num]=m_i
            theta=tau*random.random()
            x[num]=r_i*math.cos(theta)+0.5
            y[num]=r_i*math.sin(theta)+0.5
            v=math.sqrt(2*M/r_i)*random.random()
            v_x[num]=v*math.cos(theta)
            v_y[num]=v*math.sin(theta)
            num+=1
    return [m, x, y, v_x, v_y]
