import utils
import numpy as np

g_values = []
fps = 50

radius_E = 1000.0
mass_E = 10000000.0

mass_S = 1000000000.0
radius_S = 5000.0

Earth = utils.Planet(mass_E, radius_E, pos=(5000.0, 0.0), v=(0.0, 0.003))
Sun = utils.Planet(mass_S, radius_S, pos=(0.0,0.0), v=(0.0,0.0))

masses = np.array([Earth.mass, Sun.mass])
g_Earth = utils.Gravity.field(masses, 0)
g_Sun = utils.Gravity.field(masses, 1)

sx = np.array([Earth.pos[0], Sun.pos[0]])
sy = np.array([Earth.pos[1], Sun.pos[1]])

for i in range(1,1001):

    g_Earth.send(None)
    g_Sun.send(None)

    g1 = np.array(g_Earth.send((sx,sy)))
    g2 = np.array(g_Sun.send((sx,sy)))

    net_g = g1 + g2
    net_g = net_g.T

    Earth.update_pos(net_g[0], fps, log=True)
    Sun.update_pos(net_g[1], fps, log=True)
    
    sx[0], sy[0] = Earth.pos
    sx[1], sy[1] = Sun.pos

animation1 = utils.Animate([Earth, Sun])
animation1.draw(1000, fps, save=True)