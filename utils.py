import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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
            rx = sx[main_index] - sx
            ry = sy[main_index] - sy

            rx[rx == 0] = 1
            ry[ry == 0] = 1

            r = np.sqrt(rx**2 + ry**2)

            F = G*body_masses[main_index]*body_masses/(r**2)

            Fx = F*rx/r
            Fy = F*ry/r

            Fx[main_index] = 0
            Fy[main_index] = 0

            yield np.array([Fx, Fy])      

    def field(body_masses, main_index):

        while True:
            G = Constants.G
            sx, sy = yield
            rx = sx[main_index] - sx
            ry = sy[main_index] - sy

            rx[rx == 0] = 1
            ry[ry == 0] = 1

            r = np.sqrt(rx**2 + ry**2)

            E = G*body_masses[main_index]/(r**2)

            Ex = E*rx/r
            Ey = E*ry/r

            Ex[main_index] = 0
            Ey[main_index] = 0

            yield np.array([Ex, Ey])

    def potential(body_masses, main_index):

        G = Constants.G
        sx, sy = yield
        rx = sx[main_index] - sx
        ry = sy[main_index] - sy

        rx[rx == 0] = 1
        ry[ry == 0] = 1

        r = np.sqrt(rx**2 + ry**2)

        V = G*body_masses[main_index]/(r)

        Vx = V*rx/r
        Vy = V*ry/r

        Vx[main_index] = 0
        Vy[main_index] = 0

        yield np.array([Vx, Vy])

    def potential_energy(body_masses, main_index):

        G = Constants.G
        sx, sy = yield
        rx = sx[main_index] - sx
        ry = sy[main_index] - sy

        rx[rx == 0] = 1
        ry[ry == 0] = 1

        r = np.sqrt(rx**2 + ry**2)

        U = G*body_masses[main_index]/(r**2)

        Ux = U*rx/r
        Uy = U*ry/r

        Ux[main_index] = 0
        Uy[main_index] = 0

        yield np.array([Ux, Uy])



class Planet:
    def __init__(self, mass, radius, pos: tuple, v: tuple):
    
        self.mass = mass
        self.radius = radius
        self.pos = np.array(pos)
        self.velocity = np.array(v)
        self.log = [np.copy(self.pos)]

    def update_pos(self, acceleration, fps, log: bool = False):
        time = 500000/fps
        v = self.velocity

        s = (v*time)+(acceleration*time**2)/2

        self.pos += s
        self.velocity += acceleration*time

        if log:
            self.log.append(np.copy(self.pos))

class Animate:
    def __init__(self, obj: Planet | list):
        self.fig, self.ax = plt.subplots(figsize = (12, 9))

        self.ax.set_xlim(-10000, 10000)
        self.ax.set_ylim(-10000, 10000)

        self.ax.grid(True, linestyle = "--", alpha = 0.5)

        if isinstance(obj, Planet):
            arr = np.array(obj.log)
            self.pos = np.expand_dims(arr.T, axis=-1) 
        elif isinstance(obj, list):
            pos_temp = []
            for i in obj:
                if isinstance(i, Planet):
                    pos_temp.append(i.log)
                else:
                    raise TypeError("Expected a class object or a list containing objects!")
            pos = np.array(pos_temp)
            self.pos = np.transpose(pos, (2, 1, 0))
        else:
            raise TypeError("Expected a class object or a list containing objects!")
        
        initial_pos = self.pos[:, 0, :].T
        self.scatter = self.ax.scatter(
            initial_pos[:, 0],
            initial_pos[:, 1],
            s = [100, 150], 
            c = ['blue', 'red']
        )

    def update(self, frame: int):
        current_pos = self.pos[:, frame, :]
        self.scatter.set_offsets(current_pos.T)
        return self.scatter,

    def draw(self, frame_count, fps: int, save: bool = False):
        if fps > 0:
            time = 1000/fps
        else:
            raise ValueError("FPS cannot be 0 or less than 0!")
        self.ani = FuncAnimation(self.fig, self.update, frames=frame_count, interval = time, blit = True)
        if save:
            self.ani.save("Animation.mp4", writer="ffmpeg")
        plt.show()