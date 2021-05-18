from ..utils.vector import Vector, Vector2
from .constants import G


def gravitational_force(pos1, mass1, pos2, mass2):
    x1=Vector2.get_x(pos1)
    x2=Vector2.get_x(pos2)
    y1=Vector2.get_y(pos1)
    y2=Vector2.get_y(pos2)
    Fnorm = G*mass1*mass2/((x1-x2)^2+(y1-y2)^2)
    F=[Fnorm*(pos2[0]-pos1[0]),Fnorm*(pos2[1]-pos1[1])]
    return F


class IEngine:
    def __init__(self, world):
        self.world = world

    def derivatives(self, t0, y0):
        """ This is the method that will be fed to the solver
            it does not use it's first argument t0,
            its second argument y0 is a vector containing the positions 
            and velocities of the bodies, it is laid out as follow
                [x1, y1, x2, y2, ..., xn, yn, vx1, vy1, vx2, vy2, ..., vxn, vyn]
            where xi, yi are the positions and vxi, vyi are the velocities.

            Return the derivative of the state, it is laid out as follow
                [vx1, vy1, vx2, vy2, ..., vxn, vyn, ax1, ay1, ax2, ay2, ..., axn, ayn]
            where vxi, vyi are the velocities and axi, ayi are the accelerations.
        """
        raise NotImplementedError

    def make_solver_state(self):
        """ Returns the state given to the solver, it is the vector y in
                y' = f(t, y)
            In our case, it is the vector containing the 
            positions and speeds of all our bodies:
                [x1, y1, x2, y2, ..., xn, yn, vx1, vy1, vx2, vy2, ..., vxn, vyn]
            where xi, yi are the positions and vxi, vyi are the velocities.
        """
       
        raise NotImplementedError


class DummyEngine(IEngine):
    
    def __init__(self, world):
        self.world = world

    def derivatives(self, t0, y0):

        n = len(y0)/4
        y=[]
        masses=[]
        for i in range(n):
            for body in self.world.bodies:
                posx = Vector2.get_x(body.position)
                posy = Vector2.get_y(body.position)
                if (posx == y0[2*i]) and (posy == y0[2*i+1]):
                    masses.append(body.mass)
            
        for i in range(2*n,4*n):
            y.append(y0[i])
            
        for i in range(n):
            F=[0,0]
            for k in range (n):
                if k !=i:
                    F[0]+=gravitational_force([y0[2*i],y0[2*i+1]],masses[i],[y0[2*k],y0[2*k+1]],masses[k])[0]
                    F[1]+=gravitational_force([y0[2*i],y0[2*i+1]],masses[i],[y0[2*k],y0[2*k+1]],masses[k])[1]
            y.append(F[0]/masses[i])
            y.append(F[1]/masses[i])
        return y
                
            
    
    def make_solver_state(self):
    
        y0=[]
        for body in self.world.bodies:
            y0.append(body.position[0])
            y0.append(body.position[1])
            
        for body in self.world.bodies:
            y0.append(body.velocity[0])
            y0.append(body.velocity[1])
        
