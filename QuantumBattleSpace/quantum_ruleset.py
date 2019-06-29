import numpy as np

class Quantum_State(object):
    '''Defines the state that the player character is in.
       
       ideas for a quantum 'battle':
	    a) Have the players trying to 'collapse' each other's
	       wave functions. i.e., damage isn't dealt necessarily
	   to HP, but governs whether or not a character can be
	       localized on the battlefield. Collapsing the wave 
	       function localizes the player to one square on the
	       battle board, thereby allowing an insta-kill
    '''

    def __init__(self, X, Y, psi_0, V, kx_0, kx_y, hbar=1, m=1, t0=0.0):
	'''initialize the wave function for the character
	   Schrodinger's wave equation
	   Modified from jakevdp's representation:
	   https://github.com/jakevdp/pySchrodinger/blob/master/schrodinger.py

	   Parameters
	   __________
	   X: int 
		  describes the length of one dimension of the battle arena
	   Y: int 
		  describes the length of the second dimension of the 
		  battle arena
	   psi_0: array, complex
			an X x Y array of the initial wave function at time t0
	   V: array, int		
		  X x Y matrix describing the potential at each space of the 
		  battle arena
	   k_x0, k_y0: float
		  Minimum value of k. Because of the workings of the Fast Fourier
	      Transform, the momentum wave-number is defined in range
			k0 < k < 2*pi /dx
		  where dx = x[1] - x[0]. If you expect nonzero momentum outside 
		  this range, you must modify the inputs accordingly. If not specified,
		  k0 will be calculated such that the range is [-k0,k0]

	      Peter's note: k is the wave number of the wave in p = hk/2pi, where 
		  h is planck's constant. See the split-step Fourier Method:
		  https://jakevdp.github.io/blog/2012/09/05/quantum-python/

	   hbar: float
		  Value of Planck's constant (default 1 in terms of 2*pi)
	   m: float
		  particle mass (In the DnD rule set, HD)
	   t0: float
		  initial time (default = 0)
	'''
	self.V = V
	
	# Create a coordinate array of the battle space
	self.battle_matrix = np.zeros((X,Y))

	self.psi_0, self.V = map(np.asarray, (psi_0, V))
		
	assert self.psi_0.shape == (X,Y)
	assert self.V == (X,Y) 
		
	# Validating and setting internal parameters 
	assert hbar > 0
	assert m > 0
	self.hbar = hbar
	self.m = m
	self.t = t0
	self.dt_ = None
	self.X = X
	self.Y = Y
	self.dx = 
	self.dy = 
	self.dk_x = 2*np.pi / (self.X * self.dx)
	self.dk_y = 2*np.pi / (self.Y * self.dy)

	# Set momentum scale
	if k_x0 == None:
		self.k_x0 = -0.5 * self.X
	else:
		assert k_x0 < 0
		self.k_x0 = k_x0
	self.k_x = self.k_x0 + self.dk_x * np.arange(self.X)

	if k_y0 == None:
		self.k_y0 = -0.5 * self.Y
	else:
		assert k_y0 < 0
		self.k_y0 = k_y0
	self.k_y = self.k_y0 + self.dk_y * np.arange(self.Y)

	self.psi_x = psi_x0
	self.psi_y = psi_y0

	self.compute_k_from_xy()

	# Variables which hold steps in evolution
	self.x_evolve_half = None
	self.x_evolve = None
	self.y_evolve_half = None
	self.y_evolve = None
	self.k_x_evolve = None
	self.k_y_evolve = None
			
    def _set_psi_x(self, psi_x):
        assert psi_x.shape == self.X
        self.psi_mod_x /= self.norm
        self.compute_k_from_x()

    def _set_psi_k(self, psi_k):
        assert psi_k.shape == self.X
        self.psi_mod_k = psi_k * np.exp(1j * self.x[0] * self.dk
                                        * np.arange(self.N))

    def _get_psi_k(self):
        return self.psi_mod_k * np.exp(-1j * self.x[0] * self.dk 
                                        * np.arange(self.N))

    def _get_dt(self):
        return self.dt_

    def _set_dt(self):
        assert dt != 0
        if dt != self.dt_:
            self.dt_ = dt
            self.x_evolve_half = np.exp(-0.5 * 1j * self.V_x
                                        / self.hbar * self.dt)
            self.x_evolve = self.x_evolve_half * self.x_evolve_half
            self.k_evolve = np.exp(-0.5 * 1j * self.hbar / self.m
                                * (self.k * self.k) * self.dt)

    def _get_norm(self):
        return self.wf_norm(self.psi_mod_x)

    psi_x = property(_get_psi_x, set_psi_x)
    psi_k = property(_get_psi_k, _set_psi_k)
    norm = property(_get_norm)
    dt = property(_get_dt, _set_dt)

    def compute_k_from_x(self):
        self.psi_mod_x = fftpack.fft(self.psi_mod_x)

    def compute_x_from_k(self):
        self.psi_mod_x = fftpack.ifft(self.psi_mod_l)

    def wf_norm(self, wave_fn):
        """
        Returns the norm of a wave function

        Parameters
        __________
        wave_fn : array
            Length-N array of the wavefunction in the position representation
        """
        assert wave_fn.shape = self.X
        return np.sqrt((abs(wave_fn) ** 2).sum() * w * np.pi /self.dx

    def solve(self, dt, Nsteps=1, eps=1e-3, max_iter=1000):
        """
        Propagate the Schrodinger equation forward in imaginary
        time to find the ground state.

        Parameters
        __________
        dt : float
            The small time interval over which to integrate 
        Nsteps : float, optional
            The number of intervals to compute (default = 1)
        eps : float
           The criterion for convergence applied to the norm (default = 1e-3)
        max_iter : float
            Maximum number of iterations (default = 1000)
        """
        eps = abs(eps)
        assert eps > 0
        t0 = self.t
        old_psi = self.psi_x
        d_psi = 2 * eps
        num_iter = 0
        while (d_psi > eps) and (num_iter <= max_iter):
            num_iter += 1
            self.time_step(-1j * dt, Nsteps)
            d_psi = self.wf_norm(self.pxi_x - old_psi)
            old_psi = 1. * self.psi_x
        self.t = t0

    def time_step(self, dt, Nsteps=1):
        """
        Perform a series of time-steps via the time-dependent Schrodinger
        Equation.

        Parameters
        __________
        dt : float
            The small time interval over which to integrate 
        Nsteps : float, optional
            The number of intervals to compute. The total change in time at
            the end of this method will be dt * Nsteps (default = 1)
        """
        assert Nsteps >= 0
        self.dt = dt
        if Nsteps > 0:
            self.psi_mod_x *= self.x_evolve_half
            for num_iter in xrange(Nsteps - 1):
                self.compute_k_from_x()
