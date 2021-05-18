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

       

class DummySolver(ISolver):
   
    def __init__(self, f, t0, y0, max_step_size=0.01):
        self.f = f
        self.t0 = t0
        self.y0 = y0
        self.max_step_size = max_step_size

    def integrate(self, t):
        h = self.max_step_size
        N = int((t-self.t0)/h)
        y = self.y0
        for i in range(0,N):
            y = y + h*self.f(y)
        #on rajoute la petite portion de pas
        y = y + t-(self.t0+h*N)*self.f(y)
        return y
    pass
