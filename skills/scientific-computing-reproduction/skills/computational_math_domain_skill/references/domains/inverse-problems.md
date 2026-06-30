# Domain Card: Inverse Problems

Use when code recovers hidden variables, parameters, images, signals, or fields from indirect/noisy observations.

Common evidence:

- forward model, observation operator, adjoint, regularization, prior, data fidelity;
- tomography, deconvolution, parameter estimation, system identification;
- reconstruction error, PSNR, SSIM, residual, posterior samples.

Validation signals:

- data/noise assumptions;
- reconstruction metric against ground truth or benchmark;
- residual and regularization tradeoff;
- sensitivity to regularization parameter;
- comparison with baseline method.

Failure risks:

- evaluating on synthetic data without stating generation process;
- tuning regularization on test data;
- claiming visual recovery without quantitative metric;
- changing the forward model to make a demo run.

