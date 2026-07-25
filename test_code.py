import utils
import numpy as np

g_values = []

pos_log = []

radius_E = utils.Constants.Re
mass_E = utils.Constants.Me

Earth = utils.Planet(mass_E, radius_E, (utils.Constants.AU, 10000.0), v=(10000.0, 0.0))
Sun = utils.Planet(utils.Constants.Ms, utils.Constants.Rs, (0.0,0.0), v=(0.0,0.0))

masses = np.array([Earth.mass, Sun.mass])
g_Earth = utils.Gravity.field(masses, 0)
g_Sun = utils.Gravity.field(masses, 1)

sx = np.array([Earth.pos[0], Sun.pos[0]])
sy = np.array([Earth.pos[1], Sun.pos[1]])

for i in range(1,31):

    g_Earth.send(None)
    g_Sun.send(None)

    g1 = np.array(g_Earth.send((sx,sy)))
    g2 = np.array(g_Sun.send((sx,sy)))

    net_g = g1+g2
    net_g = net_g.T

    Earth.update_pos(net_g[0], 30)
    Sun.update_pos(net_g[1], 30)
    
    sx[0], sy[0] = Earth.pos
    sx[1], sy[1] = Sun.pos

    pos_log.append([Earth.pos, Sun.pos])

print(pos_log)
