from ..utils.vector import Vector, Vector2
from .constants import G

from simulator.graphics import Screen


def gravitational_force(pos1, mass1, pos2, mass2):
    """ Return the force applied to a body in pos1 with mass1
        by a body in pos2 with mass2
    """
    """ Return the force applied to a body in pos1 with mass1
        by a body in pos2 with mass2
    """
    r=Vector.norm(pos1-pos2)
    Force2sur1=-(G*mass1*mass2/(r*r*r))*(pos1-pos2)
    # print(Force2sur1)
    return Force2sur1



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
    def derivatives (self, t0, y0):
        # input()
        # n = int(len(y1)/4)
        # if (n!=len(self.world)):
        #     y2=Vector (len(self.world)*4)
        #     for k in range (len(self.world)*4):
        #         y2[k]=y1[k+len(self.world)*4]
        #     y0=y2
        # else:
        #     y0=y1
        # print(y0)
        # print (y0)
        # input()
        n = int(len(y0)/4)
        y = Vector(4*n)
        
        # print("je rentre dans la boucle")
        # print(y0)
        for i in range (n):
            # print(y)
            y[i]=y0[len(self.world)*n+i]
            y[i+len(self.world)]= y0[len(self.world)*(n+1)+i]
            F = Vector2(0,0)
            for k in range (n):
                # print(i,k)
                if (k!=i): #on vérifie que ce ne sont pas les mêmes corps
                    F += (gravitational_force(Vector2(y0[2*i],y0[2*i+1]), self.world._bodies[i].mass, Vector2(y0[k*2],y0[k*2+1]), self.world._bodies[k].mass))                   
            y[2*len(self.world)+i] = F.get_x()
            y[3*len(self.world)+i] = F.get_y()
        # print("voici le nouveau vecteur y")
        # print(y)
        y=list(y)
        # print(y)
        # print(y)
        # print(y0)

        return y



    def make_solver_state (self):
        y0=[]
        for body in self.world.bodies():
            y0.append(body.position.get_x())
            y0.append(body.position.get_y())
            
        for body in self.world.bodies():
            y0.append(body.velocity.get_x())
            y0.append(body.velocity.get_y())
        return y0



