class SolverError(Exception):
    pass


class ISolver:

    # NOTE: our systems do not depend on time,
    # so the input t0 will never be used by the
    # the derivatives function f
    # However, removing it will not simplify
    # our functions so we might as well keep it
    # and build a more general library that
    # we will be able to reuse some day

    def __init__(self, f, t0, y0, max_step_size=0.01):
        self.f = f
        self.t0 = t0
        self.y0 = y0
        self.max_step_size = max_step_size

    def integrate(self, t):
        """ Compute the solution of the system at t
            The input `t` given to this method should be increasing
            throughout the execution of the program.
            Return the new state at time t.
        """
        raise NotImplementedError


class DummySolver(ISolver):
    def  integrate (self,t):
        # print("je commence integrate")
        # h=self.max_step_size
        # print("j'ai calculé h")
        # N = (t-self.t0)//(h+1)
        # print("j'ai calculé N")
        # k=1
        # print ("je rentre dans la boucle")
        # while ((k*(t-self.t0)/N)<t):
        #     print("je suis dans la boucle")
        #     for k in range (len(self.y0)):
        #         self.y0[k] += (k*(t-self.t0)/N) * self.y0[k]
        #     k+=1
        # print ("je suis sorti de la boucle")
        # return self.y0 
        h = self.max_step_size
        n=(t-self.t0)//(h+1)
        if(n==0):
             pas_fix=t-self.t0
        else:
            pas_fix=(t-self.t0)/n

        while(self.t0<t):
            y =self.f(self.t0,self.y0)
            for k in range (len(self.y0)):       
                self.y0[k] += y[k] * pas_fix 
                self.t0 += pas_fix
        return self.y0
