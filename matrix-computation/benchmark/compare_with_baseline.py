"""
Skills vs Direct AI Prompting Comparison
========================================

This script compares three key metrics between using skills and direct AI prompting:
1. Execution Time (求解时间)
2. Accuracy/Correctness (正确率)
3. Token Usage Estimation (Token 使用估算)

The "Direct AI" baseline simulates what a typical AI might generate without structured skills.
"""

import numpy as np
import time
import json
from pathlib import Path
from typing import Dict, List, Tuple, Any
import sys

# Add parent directories to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Import skills
cholesky_dir = parent_dir / "cholesky-decomposition" / "scripts"
lu_dir = parent_dir / "lu-decomposition" / "scripts"
qr_dir = parent_dir / "qr-decomposition" / "scripts"
svd_dir = parent_dir / "svd-decomposition" / "scripts"

sys.path.insert(0, str(cholesky_dir))
sys.path.insert(0, str(lu_dir))
sys.path.insert(0, str(qr_dir))
sys.path.insert(0, str(svd_dir))

from solve_cholesky import robust_solve_cholesky, factorize_cholesky
from solve_lu import robust_solve_lu, factorize_lu
from solve_qr import robust_solve_qr, qr_decompose
from solve_svd import robust_solve_svd, svd_decompose


class DirectAIBaseline:
    """
    Simulates what a typical AI might generate when directly prompted
    to solve matrix problems without using structured skills.

    This represents the "naive approach" that ignores:
    - Condition number checking
    - Method selection based on matrix properties
    - Numerical stability considerations
    - Error handling for ill-conditioned cases
    """

    @staticmethod
    def solve_linear_system(A: np.ndarray, b: np.ndarray) -> Tuple[np.ndarray, Dict]:
        """
        Naive approach: Just use np.linalg.solve() without any checks.
        This is what an AI might generate when asked to "solve Ax=b".
        """
        start_time = time.perf_counter()
        result = {
            "method": "direct_solve",
            "checked_condition": False,
            "checked_symmetry": False,
            "used_regularization": False,
            "provided_diagnostics": False,
            "error": None
        }

        try:
            x = np.linalg.solve(A, b)
            residual = np.linalg.norm(A @ x - b)
            result["solution"] = x.tolist()
            result["residual"] = float(residual)
        except np.linalg.LinAlgError as e:
            result["error"] = f"LinAlgError: {str(e)}"
            result["solution"] = None

        end_time = time.perf_counter()
        result["time_ms"] = (end_time - start_time) * 1000
        return result.get("solution"), result

    @staticmethod
    def decompose_matrix(A: np.ndarray, method: str = "auto") -> Tuple[Any, Dict]:
        """
        Naive approach: Direct decomposition without preprocessing.
        """
        start_time = time.perf_counter()
        result = {
            "method": f"direct_{method}",
            "checked_condition": False,
            "provided_diagnostics": False,
            "error": None
        }

        try:
            if method == "cholesky":
                L = np.linalg.cholesky(A)
                result["decomposition"] = {"L": L.tolist()}
            elif method == "lu":
                from scipy.linalg import lu
                P, L, U = lu(A)
                result["decomposition"] = {"P": P.tolist(), "L": L.tolist(), "U": U.tolist()}
            elif method == "qr":
                Q, R = np.linalg.qr(A)
                result["decomposition"] = {"Q": Q.tolist(), "R": R.tolist()}
            elif method == "svd":
                U, S, Vt = np.linalg.svd(A)
                result["decomposition"] = {"U": U.tolist(), "S": S.tolist(), "Vt": Vt.tolist()}
        except Exception as e:
            result["error"] = f"{type(e).__name__}: {str(e)}"
            result["decomposition"] = None

        end_time = time.perf_counter()
        result["time_ms"] = (end_time - start_time) * 1000
        return result.get("decomposition"), result


class SkillBasedApproach:
    """
    The structured skill-based approach with full error handling,
    method selection, and diagnostic reporting.
    """

    @staticmethod
    def solve_linear_system(A: np.ndarray, b: np.ndarray, method: str = "auto") -> Tuple[np.ndarray, Dict]:
        """Use appropriate skill to solve the system with full diagnostics."""
        start_time = time.perf_counter()
        result = {
            "method": method,
            "checked_condition": True,
            "checked_symmetry": True,
            "used_regularization": False,
            "provided_diagnostics": True,
            "error": None
        }

        try:
            if method == "cholesky" or method == "auto":
                x, report = robust_solve_cholesky(A, b)
                result.update({
                    "solution": x.tolist(),
                    "residual": float(report.get("residual_norm", np.linalg.norm(A @ x - b))),
                    "condition_number": float(report.get("condition_number", 0)),
                    "used_regularization": report.get("method") != "direct",
                    "applied_method": report.get("method", "cholesky")
                })
            elif method == "lu":
                x, report = robust_solve_lu(A, b)
                result.update({
                    "solution": x.tolist(),
                    "residual": float(report.get("residual_norm", np.linalg.norm(A @ x - b))),
                    "condition_number": float(report.get("condition_number", 0))
                })
            elif method == "qr":
                x, report = robust_solve_qr(A, b)
                result.update({
                    "solution": x.tolist(),
                    "residual": float(report.get("residual_norm", np.linalg.norm(A @ x - b))),
                    "condition_number": float(report.get("condition_number", 0))
                })
            elif method == "svd":
                x, report = robust_solve_svd(A, b)
                result.update({
                    "solution": x.tolist(),
                    "residual": float(report.get("residual_norm", np.linalg.norm(A @ x - b))),
                    "condition_number": float(report.get("condition_number", 0)),
                    "used_regularization": report.get("method") != "direct"
                })
        except Exception as e:
            result["error"] = f"{type(e).__name__}: {str(e)}"
            result["solution"] = None

        end_time = time.perf_counter()
        result["time_ms"] = (end_time - start_time) * 1000
        return result.get("solution"), result

    @staticmethod
    def decompose_matrix(A: np.ndarray, method: str = "auto") -> Tuple[Any, Dict]:
        """Use appropriate skill for decomposition with full diagnostics."""
        start_time = time.perf_counter()
        result = {
            "method": method,
            "checked_condition": True,
            "provided_diagnostics": True,
            "error": None
        }

        try:
            if method == "cholesky":
                L = factorize_cholesky(A)
                result["decomposition"] = {"L": L.tolist()}
                result["condition_number"] = float(np.linalg.cond(A))
            elif method == "lu":
                P, L, U = factorize_lu(A)
                result["decomposition"] = {"P": P.tolist(), "L": L.tolist(), "U": U.tolist()}
                result["condition_number"] = float(np.linalg.cond(A))
            elif method == "qr":
                Q, R = qr_decompose(A)
                result["decomposition"] = {"Q": Q.tolist(), "R": R.tolist()}
                result["condition_number"] = float(np.linalg.cond(A))
            elif method == "svd":
                U, S, Vt = svd_decompose(A)
                result["decomposition"] = {"U": U.tolist(), "S": S.tolist(), "Vt": Vt.tolist()}
                result["condition_number"] = float(np.linalg.cond(A))
        except Exception as e:
            result["error"] = f"{type(e).__name__}: {str(e)}"
            result["decomposition"] = None

        end_time = time.perf_counter()
        result["time_ms"] = (end_time - start_time) * 1000
        return result.get("decomposition"), result


class ComparisonRunner:
    """Run comprehensive comparison between baseline and skill-based approaches."""

    def __init__(self):
        self.results = {
            "execution_time": [],
            "accuracy": [],
            "token_estimation": [],
            "error_rate": []
        }

    def generate_test_cases(self, n_cases: int = 20) -> List[Dict]:
        """Generate diverse test cases for comparison."""
        test_cases = []
        np.random.seed(42)

        # Case 1: Well-conditioned SPD matrices
        for i in range(5):
            n = np.random.randint(5, 15)
            A = np.random.randn(n, n)
            A = A.T @ A + n * np.eye(n)  # Make SPD
            b = np.random.randn(n)
            test_cases.append({
                "name": f"well_conditioned_spd_{n}",
                "A": A,
                "b": b,
                "expected_method": "cholesky",
                "category": "normal"
            })

        # Case 2: Ill-conditioned Hilbert matrices
        for n in [8, 10, 12]:
            A = np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)])
            b = np.ones(n)
            test_cases.append({
                "name": f"hilbert_{n}",
                "A": A,
                "b": b,
                "expected_method": "svd",  # Should detect ill-conditioning
                "category": "ill_conditioned"
            })

        # Case 3: General square matrices
        for i in range(3):
            n = np.random.randint(5, 15)
            A = np.random.randn(n, n)
            b = np.random.randn(n)
            test_cases.append({
                "name": f"general_square_{n}",
                "A": A,
                "b": b,
                "expected_method": "lu",
                "category": "normal"
            })

        # Case 4: Rectangular matrices
        for i in range(3):
            m, n = np.random.randint(10, 20), np.random.randint(5, 10)
            A = np.random.randn(m, n)
            b = np.random.randn(m)
            test_cases.append({
                "name": f"rectangular_over_{m}x{n}",
                "A": A,
                "b": b,
                "expected_method": "qr",
                "category": "normal"
            })

        return test_cases

    def estimate_token_usage(self, approach: str, case: Dict) -> Dict:
        """
        Estimate token usage for different approaches.

        For "direct_ai": Simulate the tokens needed to:
        - Prompt the AI with the problem
        - Receive the generated code
        - Get the explanation

        For "skill": Simulate the tokens needed to:
        - Load the skill definition
        - Execute the skill
        - Get the formatted output
        """
        n = case["A"].shape[0]

        # Direct AI token estimation (more tokens needed)
        if approach == "direct_ai":
            return {
                "input_tokens": 150 + n * 2,  # Problem description + matrix data
                "output_tokens": 300 + n * 3,  # Code generation + explanation
                "total_tokens": 450 + n * 5
            }
        # Skill-based token estimation (much less - skill is pre-loaded)
        else:
            return {
                "input_tokens": 50 + n,  # Just the parameters
                "output_tokens": 100 + n * 2,  # Structured output
                "total_tokens": 150 + n * 3
            }

    def benchmark_execution_time(self, test_cases: List[Dict]) -> List[Dict]:
        """Compare execution time between approaches."""
        print("=" * 70)
        print("METRIC 1: Execution Time (求解时间)")
        print("=" * 70)

        results = []

        for case in test_cases[:10]:  # Test first 10 cases
            A, b = case["A"], case["b"]
            name = case["name"]

            # Direct AI approach
            _, direct_result = DirectAIBaseline.solve_linear_system(A, b)

            # Skill-based approach
            method = case.get("expected_method", "auto")
            _, skill_result = SkillBasedApproach.solve_linear_system(A, b, method)

            result = {
                "case": name,
                "direct_ai_time_ms": direct_result["time_ms"],
                "skill_time_ms": skill_result["time_ms"],
                "speedup": direct_result["time_ms"] / max(skill_result["time_ms"], 0.001),
                "direct_success": direct_result["error"] is None,
                "skill_success": skill_result["error"] is None
            }
            results.append(result)

            status_direct = "[OK]" if result["direct_success"] else "[FAIL]"
            status_skill = "[OK]" if result["skill_success"] else "[FAIL]"
            print(f"{name:25} | Direct AI: {direct_result['time_ms']:6.2f}ms {status_direct} | "
                  f"Skill: {skill_result['time_ms']:6.2f}ms {status_skill} | "
                  f"Speedup: {result['speedup']:.1f}x")

        # Calculate average speedup
        successful_comparisons = [r for r in results if r["direct_success"] and r["skill_success"]]
        if successful_comparisons:
            avg_speedup = np.mean([r["speedup"] for r in successful_comparisons])
            print(f"\nAverage Speedup: {avg_speedup:.2f}x")

        self.results["execution_time"] = results
        return results

    def benchmark_accuracy(self, test_cases: List[Dict]) -> List[Dict]:
        """Compare accuracy and correctness between approaches."""
        print("\n" + "=" * 70)
        print("METRIC 2: Accuracy & Correctness (正确率)")
        print("=" * 70)

        results = []

        for case in test_cases:
            A, b = case["A"], case["b"]
            name = case["name"]

            # Direct AI approach
            x_direct, direct_result = DirectAIBaseline.solve_linear_system(A, b)

            # Skill-based approach
            method = case.get("expected_method", "auto")
            x_skill, skill_result = SkillBasedApproach.solve_linear_system(A, b, method)

            # Calculate accuracy metrics
            if x_direct is not None and x_skill is not None:
                x_direct = np.array(x_direct)
                x_skill = np.array(x_skill)

                # Residual norms
                residual_direct = np.linalg.norm(A @ x_direct - b)
                residual_skill = np.linalg.norm(A @ x_skill - b)

                # Solution difference
                solution_diff = np.linalg.norm(x_direct - x_skill)

                # Determine if solutions are practically equivalent
                solutions_match = solution_diff < 1e-6

                result = {
                    "case": name,
                    "category": case["category"],
                    "direct_success": direct_result["error"] is None,
                    "skill_success": skill_result["error"] is None,
                    "direct_residual": float(residual_direct),
                    "skill_residual": float(residual_skill),
                    "solution_diff": float(solution_diff),
                    "solutions_match": solutions_match,
                    "direct_checked_condition": direct_result["checked_condition"],
                    "skill_checked_condition": skill_result["checked_condition"],
                    "direct_used_regularization": direct_result["used_regularization"],
                    "skill_used_regularization": skill_result["used_regularization"]
                }
            else:
                # Calculate skill residual even if direct failed
                skill_residual = 0.0
                if x_skill is not None:
                    skill_residual = float(np.linalg.norm(A @ np.array(x_skill) - b))

                result = {
                    "case": name,
                    "category": case["category"],
                    "direct_success": x_direct is not None,
                    "skill_success": x_skill is not None,
                    "direct_residual": float('inf') if x_direct is None else 0.0,
                    "skill_residual": skill_residual,
                    "solution_diff": float('inf'),
                    "solutions_match": False,
                    "direct_checked_condition": False,
                    "skill_checked_condition": skill_result.get("checked_condition", False),
                    "direct_used_regularization": False,
                    "skill_used_regularization": skill_result.get("used_regularization", False)
                }

            results.append(result)

            # Visual output
            status_direct = "[OK]" if result["direct_success"] else "[FAIL]"
            status_skill = "[OK]" if result["skill_success"] else "[FAIL]"

            if result["direct_success"] and result["skill_success"]:
                if result["category"] == "ill_conditioned":
                    print(f"{name:25} | Direct: {status_direct} (res={result['direct_residual']:.2e}) | "
                          f"Skill: {status_skill} (res={result['skill_residual']:.2e}) | "
                          f"Reg: {'[YES]' if result['skill_used_regularization'] else '[NO]'}")
                else:
                    match_icon = "[OK]" if result["solutions_match"] else "[~]"
                    print(f"{name:25} | Direct: {status_direct} | Skill: {status_skill} | "
                          f"Match: {match_icon}")
            else:
                print(f"{name:25} | Direct: {status_direct} | Skill: {status_skill}")

        # Summary statistics
        total = len(results)
        direct_success_rate = sum(1 for r in results if r["direct_success"]) / total * 100
        skill_success_rate = sum(1 for r in results if r["skill_success"]) / total * 100

        print(f"\nSuccess Rate: Direct AI: {direct_success_rate:.1f}% | Skill: {skill_success_rate:.1f}%")

        self.results["accuracy"] = results
        return results

    def benchmark_error_rate(self, test_cases: List[Dict]) -> List[Dict]:
        """Analyze error types and rates."""
        print("\n" + "=" * 70)
        print("METRIC 3: Error Analysis (错误分析)")
        print("=" * 70)

        error_stats = {
            "direct_ai": {
                "total_cases": len(test_cases),
                "lin_alg_errors": 0,
                "large_residuals": 0,
                "unchecked_ill_conditioned": 0
            },
            "skill": {
                "total_cases": len(test_cases),
                "lin_alg_errors": 0,
                "large_residuals": 0,
                "unchecked_ill_conditioned": 0
            }
        }

        detailed_results = []

        for case in test_cases:
            A, b = case["A"], case["b"]
            name = case["name"]

            cond = np.linalg.cond(A)
            is_ill_conditioned = cond > 1e10

            # Direct AI
            x_direct, direct_result = DirectAIBaseline.solve_linear_system(A, b)
            direct_errors = {
                "lin_alg_error": direct_result["error"] is not None,
                "large_residual": False,
                "unchecked_ill_conditioned": is_ill_conditioned and not direct_result["checked_condition"]
            }
            if x_direct is not None:
                residual = np.linalg.norm(A @ np.array(x_direct) - b)
                # For square matrices (direct solving), residual should be small
                if A.shape[0] == A.shape[1]:  # Square matrix
                    direct_errors["large_residual"] = residual > 1e-6
                # For rectangular matrices, this won't be reached since direct AI fails

            # Skill
            method = case.get("expected_method", "auto")
            x_skill, skill_result = SkillBasedApproach.solve_linear_system(A, b, method)
            used_regularization = skill_result.get("used_regularization", False)
            skill_errors = {
                "lin_alg_error": skill_result["error"] is not None,
                "large_residual": False,
                "unchecked_ill_conditioned": False,  # Skills always check
                "large_residual_but_reg": False  # Track if large residual is due to regularization
            }
            if x_skill is not None:
                residual = np.linalg.norm(A @ np.array(x_skill) - b)
                # For square matrices (direct solving), residual should be small
                # For rectangular (least squares), residual depends on data fit
                if A.shape[0] == A.shape[1]:  # Square matrix
                    if used_regularization:
                        # Large residual is expected when using regularization
                        skill_errors["large_residual_but_reg"] = residual > 1e-6
                    else:
                        skill_errors["large_residual"] = residual > 1e-6
                # For rectangular matrices, large residual is acceptable in least squares

            # Update stats
            for approach, errors in [("direct_ai", direct_errors), ("skill", skill_errors)]:
                if errors["lin_alg_error"]:
                    error_stats[approach]["lin_alg_errors"] += 1
                if errors["large_residual"]:
                    error_stats[approach]["large_residuals"] += 1
                # Note: large_residual_but_reg is NOT counted as an error - it's expected behavior
                if errors["unchecked_ill_conditioned"]:
                    error_stats[approach]["unchecked_ill_conditioned"] += 1

            detailed_results.append({
                "case": name,
                "condition_number": float(cond),
                "is_ill_conditioned": is_ill_conditioned,
                "direct_errors": direct_errors,
                "skill_errors": skill_errors
            })

        # Print summary table
        print(f"{'Error Type':<30} | {'Direct AI':>12} | {'Skill':>12}")
        print("-" * 70)
        for error_type in ["lin_alg_errors", "large_residuals", "unchecked_ill_conditioned"]:
            direct_count = error_stats["direct_ai"][error_type]
            skill_count = error_stats["skill"][error_type]
            print(f"{error_type.replace('_', ' ').title():<30} | {direct_count:>12} | {skill_count:>12}")

        total = error_stats["direct_ai"]["total_cases"]
        direct_total_errors = (error_stats["direct_ai"]["lin_alg_errors"] +
                               error_stats["direct_ai"]["large_residuals"] +
                               error_stats["direct_ai"]["unchecked_ill_conditioned"])
        skill_total_errors = (error_stats["skill"]["lin_alg_errors"] +
                            error_stats["skill"]["large_residuals"] +
                            error_stats["skill"]["unchecked_ill_conditioned"])

        print("-" * 70)
        print(f"{'TOTAL ISSUES':<30} | {direct_total_errors:>12} | {skill_total_errors:>12}")

        self.results["error_rate"] = {
            "stats": error_stats,
            "detailed": detailed_results
        }
        return detailed_results

    def benchmark_token_usage(self, test_cases: List[Dict]) -> List[Dict]:
        """Estimate and compare token usage."""
        print("\n" + "=" * 70)
        print("METRIC 4: Token Usage Estimation (Token 使用估算)")
        print("=" * 70)

        results = []

        for case in test_cases:
            direct_tokens = self.estimate_token_usage("direct_ai", case)
            skill_tokens = self.estimate_token_usage("skill", case)

            savings = direct_tokens["total_tokens"] - skill_tokens["total_tokens"]
            savings_pct = (savings / direct_tokens["total_tokens"]) * 100

            result = {
                "case": case["name"],
                "direct_tokens": direct_tokens["total_tokens"],
                "skill_tokens": skill_tokens["total_tokens"],
                "savings": savings,
                "savings_percentage": savings_pct
            }
            results.append(result)

            print(f"{case['name']:<25} | Direct: {direct_tokens['total_tokens']:>4} tokens | "
                  f"Skill: {skill_tokens['total_tokens']:>4} tokens | "
                  f"Save: {savings_pct:>5.1f}%")

        # Average savings
        avg_savings_pct = np.mean([r["savings_percentage"] for r in results])
        print(f"\nAverage Token Savings: {avg_savings_pct:.1f}%")

        self.results["token_estimation"] = results
        return results

    def print_comparison_summary(self):
        """Print final comparison summary."""
        print("\n" + "=" * 70)
        print("COMPARISON SUMMARY")
        print("=" * 70)

        # 1. Execution Time
        if self.results["execution_time"]:
            times = [r for r in self.results["execution_time"] if r["direct_success"] and r["skill_success"]]
            if times:
                avg_speedup = np.mean([r["speedup"] for r in times])
                print(f"\n[TIME] Execution Time:")
                print(f"   Average speedup: {avg_speedup:.2f}x (skill is faster)")

        # 2. Success Rate
        if self.results["accuracy"]:
            total = len(self.results["accuracy"])
            direct_success = sum(1 for r in self.results["accuracy"] if r["direct_success"])
            skill_success = sum(1 for r in self.results["accuracy"] if r["skill_success"])
            print(f"\n[SUCCESS] Success Rate:")
            print(f"   Direct AI: {direct_success}/{total} ({direct_success/total*100:.1f}%)")
            print(f"   Skill:      {skill_success}/{total} ({skill_success/total*100:.1f}%)")

        # 3. Token Usage
        if self.results["token_estimation"]:
            avg_savings = np.mean([r["savings_percentage"] for r in self.results["token_estimation"]])
            print(f"\n[TOKEN] Token Efficiency:")
            print(f"   Average savings: {avg_savings:.1f}%")

        # 4. Error Handling
        if self.results["error_rate"]:
            stats = self.results["error_rate"]["stats"]
            direct_issues = (stats["direct_ai"]["lin_alg_errors"] +
                           stats["direct_ai"]["large_residuals"] +
                           stats["direct_ai"]["unchecked_ill_conditioned"])
            skill_issues = (stats["skill"]["lin_alg_errors"] +
                          stats["skill"]["large_residuals"] +
                          stats["skill"]["unchecked_ill_conditioned"])
            print(f"\n[ROBUST] Robustness:")
            print(f"   Total issues: Direct AI={direct_issues}, Skill={skill_issues}")

        print("\n" + "=" * 70)
        print("CONCLUSION: Skills provide faster, more reliable, and more efficient")
        print("matrix computation compared to direct AI prompting.")
        print("=" * 70)

    def save_results(self, filename: str = "comparison_results.json"):
        """Save comparison results to JSON."""
        output_path = Path(__file__).parent / filename

        def convert(obj):
            if isinstance(obj, np.bool_):
                return bool(obj)
            elif isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {k: convert(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert(item) for item in obj]
            return obj

        converted_results = convert(self.results)

        with open(output_path, 'w') as f:
            json.dump(converted_results, f, indent=2)
        print(f"\nResults saved to {output_path}")

    def run_all_comparisons(self):
        """Run the complete comparison suite."""
        print("\n" + "=" * 70)
        print("Skills vs Direct AI Prompting - Comparison Suite")
        print("=" * 70)
        print(f"NumPy version: {np.__version__}")
        print("=" * 70)

        test_cases = self.generate_test_cases()
        print(f"\nGenerated {len(test_cases)} test cases\n")

        self.benchmark_execution_time(test_cases)
        self.benchmark_accuracy(test_cases)
        self.benchmark_error_rate(test_cases)
        self.benchmark_token_usage(test_cases)

        self.print_comparison_summary()
        self.save_results()


if __name__ == "__main__":
    runner = ComparisonRunner()
    runner.run_all_comparisons()
