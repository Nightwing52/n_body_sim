# n_body_sim
An n-body simulator written in Python utilizing the Barnes-Hut algorithm for computing forces.

barn_hut.py: builds the quad-tree for the integrator to use.
integrator.py: numerically integrates the equations of motion using Velocity Verlet. By construction, this algorithm conserves the constants of motion (mainly energy and momenta) at the cost of roundoff error. File also provides IC.
main.py: runs a simulation.
display.py: not really working. Just text outputs the COM for now.
