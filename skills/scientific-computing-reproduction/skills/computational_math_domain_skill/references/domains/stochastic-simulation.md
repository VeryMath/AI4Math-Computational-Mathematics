# Domain Card: Stochastic Simulation

Use when code performs Monte Carlo, MCMC, particle methods, stochastic processes, random sampling, or uncertainty estimation.

Common evidence:

- random seed, sampler, proposal distribution, burn-in, chain, particles;
- confidence intervals, effective sample size, variance estimates;
- repeated trials or statistical summaries.

Validation signals:

- seed and reproducibility statement;
- sample size and uncertainty interval;
- convergence diagnostics for chains;
- comparison to analytic expectation or benchmark distribution;
- sensitivity to number of samples.

Failure risks:

- single random run reported as deterministic evidence;
- missing seed;
- insufficient sample size;
- benchmark leakage when tuning on evaluation data.

