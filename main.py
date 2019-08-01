from integrator import *

n, M, a=10000, 1.0, 0.3
init_con=gen_exp_disk(n, M, a)
m, x_0, y_0, v_x0, v_y0=init_con[0], init_con[1], init_con[2], init_con[3], init_con[4]
t_total, delta_t=1.0, 0.001
vel_verlet(n, t_total, delta_t, x_0, y_0, v_x0, v_y0, m)
