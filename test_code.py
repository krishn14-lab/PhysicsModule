import utils
import numpy as np

g_values = []
fps = 60
duration = 60
sim_scale = 5.8

frame_count = fps*duration

radius_E = 1000.0
mass_E = 10000000.0

mass_S = 1500000000.0
radius_S = 50000.0

mass_X = 12000000.0
radius_X = 1500.0

Earth = utils.Planet(mass_E, radius_E, pos=(5000.0, 0.0), v=(0.0, 0.005))
Sun = utils.Planet(mass_S, radius_S, pos=(0.0,0.0), v=(0.0001,0.0))
X = utils.Planet(mass_X, radius_X, pos=(-6000.0, 0.0), v=(0.0, 0.0035))

masses = np.array([Earth.mass, Sun.mass, X.mass])
g_Earth = utils.Gravity.field(masses, 0)
g_Sun = utils.Gravity.field(masses, 1)
g_X = utils.Gravity.field(masses, 2)

sx = np.array([Earth.pos[0], Sun.pos[0], X.pos[0]])
sy = np.array([Earth.pos[1], Sun.pos[1], X.pos[1]])

for i in range(1, frame_count+1):

    g_Earth.send(None)
    g_Sun.send(None)
    g_X.send(None)

    g1 = np.array(g_Earth.send((sx,sy)))
    g2 = np.array(g_Sun.send((sx,sy)))
    g3 = np.array(g_X.send((sx,sy)))

    net_g = g1 + g2 + g3
    net_g = net_g.T

    Earth.update_pos(net_g[0], fps, log=True, scale=sim_scale)
    Sun.update_pos(net_g[1], fps, log=True, scale=sim_scale)
    X.update_pos(net_g[2], fps, log=True, scale=sim_scale)
    
    sx[0], sy[0] = Earth.pos
    sx[1], sy[1] = Sun.pos
    sx[2], sy[2] = X.pos

animation1 = utils.Animate([Earth, Sun, X])
animation1.draw(frame_count, fps, save=False)