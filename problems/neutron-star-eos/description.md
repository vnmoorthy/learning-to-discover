# STARFORGE: the neutron-star equation of state

Neutron stars hold the densest stable matter in the Universe. Their structure is set by one function, the equation of state (EOS) P(eps), which relates pressure to energy density above nuclear saturation density (n_sat = 0.16 fm^-3). It cannot yet be computed from first principles at these densities.

Given an EOS, the Tolman-Oppenheimer-Volkoff (TOV) equations predict the mass M and radius R of each star. A companion equation for the tidal Love number k2 predicts the tidal deformability Lambda, which gravitational waves measure. Observations then constrain the EOS:

- 2 M_sun pulsars (PSR J0348+0432, J0740+6620)
- NICER mass-radius measurements
- the GW170817 tidal deformability

STARFORGE is an autonomous computational lab built around this problem. It asks four questions:

1. Is the solver correct? We check it against analytic limits and an independent second implementation.
2. How stiff must matter be? We find the minimum sound speed c_s^2 that supports 2 M_sun.
3. What do first-order phase transitions to quark matter do? A Maxwell construction with a constant-sound-speed quark phase can create disconnected hybrid branches and "twin stars". We test the Seidov stability criterion on these models.
4. What do the observations jointly imply? A multimessenger MCMC pipeline answers this one.

Units are G = c = 1 with lengths in km, and results are reported in M_sun, km and MeV/fm^3. Every EOS satisfies the first law d(eps) = (eps + P) dn / n and causality 0 <= c_s^2 <= 1, except across explicit first-order jumps.

Every result carries a novelty level (1 reproduction to 5 potentially novel); nothing is claimed as a discovery. Most results are levels 1-2, and the twin-star maps are level 3. The inference chains did not converge, so no posterior is reported.
