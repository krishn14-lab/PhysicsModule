import numpy as np

class Constants:

    G = 6.6743 * 10**(-11)

    Me = 5.9722 * 10**24
    Ms = 1.989 * 10**30

    Re = 6371000
    Rs = 695700000

    AU = 1.496 * 10**11

class Gravity:
    
    def force(body_masses, main_index):

        while True:
            G = Constants.G
            sx, sy = yield
            try:
                rx = sx[main_index] - sx
                ry = sy[main_index] - sy

                rx[rx == 0] = 1
                ry[ry == 0] = 1

                Fx = G*body_masses[main_index]*body_masses/(rx**2)
                Fy = G*body_masses[main_index]*body_masses/(ry**2)

                Fx[0][main_index] = 0
                Fy[0][main_index] = 0

                yield [Fx, Fy]

            except Exception:
                print("Error")

    def field(body_masses, main_index):

        while True:
            G = Constants.G
            sx, sy = yield
            rx = sx[main_index] - sx
            ry = sy[main_index] - sy

            rx[rx == 0] = 1
            ry[ry == 0] = 1

            Ex = G*body_masses[main_index]/(rx**2)
            Ey = G*body_masses[main_index]/(ry**2)

            Ex[main_index] = 0
            Ey[main_index] = 0

            yield [Ex, Ey]

    def potential(body_masses, main_index):

        G = Constants.G
        sx, sy = yield
        try:
            rx = sx[main_index] - sx
            ry = sy[main_index] - sy

            rx[rx == 0] = 1
            ry[ry == 0] = 1

            Vx = G*body_masses[main_index]/(rx)
            Vy = G*body_masses[main_index]/(ry)

            Vx[0][main_index] = 0
            Vy[0][main_index] = 0

            yield [Vx, Vy]

        except Exception:
            print("Error")

    def potential_energy(body_masses, main_index):

        G = Constants.G
        sx, sy = yield
        try:
            rx = sx[main_index] - sx
            ry = sy[main_index] - sy

            rx[rx == 0] = 1
            ry[ry == 0] = 1

            Ux = G*body_masses[main_index]*body_masses/(rx)
            Uy = G*body_masses[main_index]*body_masses/(ry)

            Ux[0][main_index] = 0
            Uy[0][main_index] = 0

            yield [Ux, Uy]

        except Exception:
            print("Error")


class Planet:
    def __init__(self, mass, radius, pos, v):
    
        self.mass = mass
        self.radius = radius
        self.pos = np.array(pos)
        self.velocity = np.array(v)

    def update_pos(self, acceleration, fps):
    
        time = 1/fps
        v = self.velocity

        s = (v*time)+(acceleration*time**2)/2

        self.pos += s
        self.velocity += acceleration*time

