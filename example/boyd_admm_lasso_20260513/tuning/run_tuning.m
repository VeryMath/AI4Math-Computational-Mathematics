function run_tuning()
%RUN_TUNING Grid search for Boyd ADMM Lasso rho and alpha.

scriptDir = fileparts(mfilename('fullpath'));
runDir = fileparts(scriptDir);
sourceDir = fullfile(runDir, 'source');
tuningDir = scriptDir;
figDir = fullfile(tuningDir, 'tuning_figures');

if ~exist(tuningDir, 'dir'), mkdir(tuningDir); end
if ~exist(figDir, 'dir'), mkdir(figDir); end
addpath(sourceDir);

rhos = [0.1, 0.3, 1.0, 3.0, 10.0];
alphas = [1.0, 1.2, 1.5, 1.8];
baselineObjective = 17.2693553575;
objectiveTolerance = 0.1;

logPath = fullfile(tuningDir, 'tuning.log');
fid = fopen(logPath, 'w');
if fid < 0
    error('Could not open tuning log: %s', logPath);
end
cleanup = onCleanup(@() fclose(fid));

fprintf(fid, 'Boyd ADMM Lasso rho/alpha tuning\n');
fprintf(fid, 'Run directory: %s\n', runDir);
fprintf(fid, 'MATLAB version: %s\n', version);
fprintf(fid, 'Timestamp: %s\n', char(datetime('now','TimeZone','local')));
fprintf(fid, 'Baseline objective: %.12g\n', baselineObjective);
fprintf(fid, 'Objective tolerance: %.12g\n\n', objectiveTolerance);

trial = 0;
rows = struct([]);

for rho = rhos
    for alpha = alphas
        trial = trial + 1;
        fprintf('Trial %02d: rho=%.4g alpha=%.4g\n', trial, rho, alpha);
        fprintf(fid, '=== Trial %02d: rho=%.12g alpha=%.12g ===\n', trial, rho, alpha);

        [A, b, lambda] = make_problem();
        elapsedTimer = tic;

        try
            solverOutput = evalc('[x, history] = lasso(A, b, lambda, rho, alpha);');
            elapsed = toc(elapsedTimer);
            iterations = numel(history.objval);
            finalObjective = history.objval(end);
            finalRNorm = history.r_norm(end);
            finalEpsPri = history.eps_pri(end);
            finalSNorm = history.s_norm(end);
            finalEpsDual = history.eps_dual(end);
            primalSatisfied = finalRNorm < finalEpsPri;
            dualSatisfied = finalSNorm < finalEpsDual;
            objectiveClose = abs(finalObjective - baselineObjective) <= objectiveTolerance;
            status = "success";
            errorMessage = "";
        catch ME
            elapsed = toc(elapsedTimer);
            solverOutput = getReport(ME, 'extended', 'hyperlinks', 'off');
            iterations = NaN;
            finalObjective = NaN;
            finalRNorm = NaN;
            finalEpsPri = NaN;
            finalSNorm = NaN;
            finalEpsDual = NaN;
            primalSatisfied = false;
            dualSatisfied = false;
            objectiveClose = false;
            status = "error";
            errorMessage = string(ME.message);
        end

        rows(trial).trial = trial; %#ok<AGROW>
        rows(trial).rho = rho;
        rows(trial).alpha = alpha;
        rows(trial).iterations = iterations;
        rows(trial).final_objective = finalObjective;
        rows(trial).r_norm = finalRNorm;
        rows(trial).eps_pri = finalEpsPri;
        rows(trial).s_norm = finalSNorm;
        rows(trial).eps_dual = finalEpsDual;
        rows(trial).primal_satisfied = primalSatisfied;
        rows(trial).dual_satisfied = dualSatisfied;
        rows(trial).objective_close = objectiveClose;
        rows(trial).valid = primalSatisfied && dualSatisfied && objectiveClose && status == "success";
        rows(trial).elapsed_seconds = elapsed;
        rows(trial).status = status;
        rows(trial).error_message = errorMessage;

        fprintf(fid, '%s\n', solverOutput);
        fprintf(fid, 'summary: iterations=%g final_objective=%.12g r_norm=%.12g eps_pri=%.12g s_norm=%.12g eps_dual=%.12g valid=%d elapsed_seconds=%.6f status=%s\n\n', ...
            iterations, finalObjective, finalRNorm, finalEpsPri, finalSNorm, finalEpsDual, rows(trial).valid, elapsed, status);
    end
end

T = struct2table(rows);
writetable(T, fullfile(tuningDir, 'tuning_results.csv'));

validRows = T(T.valid, :);
if isempty(validRows)
    successRows = T(strcmp(T.status, "success"), :);
    if isempty(successRows)
        best = T(1, :);
        selectionStatus = "no_successful_trials";
    else
        best = sortrows(successRows, {'iterations', 'final_objective', 'elapsed_seconds', 'rho'});
        best = best(1, :);
        selectionStatus = "best_success_without_valid_objective_constraint";
    end
else
    best = sortrows(validRows, {'iterations', 'final_objective', 'elapsed_seconds', 'rho'});
    best = best(1, :);
    selectionStatus = "best_valid_trial";
end

bestStruct = struct();
bestStruct.selection_status = selectionStatus;
bestStruct.trial = best.trial;
bestStruct.rho = best.rho;
bestStruct.alpha = best.alpha;
bestStruct.iterations = best.iterations;
bestStruct.final_objective = best.final_objective;
bestStruct.r_norm = best.r_norm;
bestStruct.eps_pri = best.eps_pri;
bestStruct.s_norm = best.s_norm;
bestStruct.eps_dual = best.eps_dual;
bestStruct.primal_satisfied = best.primal_satisfied;
bestStruct.dual_satisfied = best.dual_satisfied;
bestStruct.objective_close = best.objective_close;
bestStruct.valid = best.valid;
bestStruct.elapsed_seconds = best.elapsed_seconds;
bestStruct.baseline = struct('rho', 1.0, 'alpha', 1.0, 'iterations', 15, 'final_objective', baselineObjective);

jsonText = jsonencode(bestStruct, PrettyPrint=true);
write_text(fullfile(tuningDir, 'best_parameters.json'), jsonText);

fprintf(fid, 'Best parameters:\n%s\n', jsonText);
fprintf('Best trial %d: rho=%.4g alpha=%.4g iterations=%g objective=%.12g valid=%d\n', ...
    best.trial, best.rho, best.alpha, best.iterations, best.final_objective, best.valid);
end

function [A, b, lambda] = make_problem()
randn('seed', 0);
rand('seed', 0);

m = 1500;
n = 5000;
p = 100/n;

x0 = sprandn(n, 1, p);
A = randn(m, n);
A = A * spdiags(1./sqrt(sum(A.^2))', 0, n, n);
b = A*x0 + sqrt(0.001)*randn(m, 1);

lambdaMax = norm(A'*b, 'inf');
lambda = 0.1*lambdaMax;
end

function write_text(path, text)
fid = fopen(path, 'w');
if fid < 0
    error('Could not open file for writing: %s', path);
end
cleanup = onCleanup(@() fclose(fid));
fprintf(fid, '%s\n', text);
end
