# Domain Card: Differential Equations

Use when code solves ODEs, SDEs, DAEs, time-stepping schemes, or dynamical systems.

Common evidence:

- Runge-Kutta, BDF, Adams, Euler-Maruyama, time grid, state vector;
- tolerances such as absolute/relative tolerance;
- stiffness, event handling, conservation law, stability;
- trajectory plots or time-series error metrics.

Validation signals:

- convergence with step refinement;
- error against analytic or reference solution;
- conserved quantity drift;
- stability under smaller time step;
- seed and sample size for stochastic equations.

Failure risks:

- stiff problem solved with unstable explicit scheme;
- time step chosen only for the demo;
- plotting output mistaken for numerical validation;
- randomness not seeded or uncertainty not reported.

