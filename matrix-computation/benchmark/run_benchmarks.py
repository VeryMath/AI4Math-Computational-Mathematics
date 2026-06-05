"""
Matrix Computation Skills Benchmark
===================================

This script runs real benchmarks on the matrix computation skills
to measure accuracy, performance, and robustness.
"""

import numpy as np
import time
import json
from pathlib import Path
from typing import Dict, List, Tuple, Any
import sys

# Add parent directories to path to import skills
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Import skills by adding their directories to path
cholesky_dir = parent_dir / "cholesky-decomposition" / "scripts"
lu_dir = parent_dir / "lu-decomposition" / "scripts"
qr_dir = parent_dir / "qr-decomposition" / "scripts"
svd_dir = parent_dir / "svd-decomposition" / "scripts"
choose_dir = parent_dir / "choose_decomposition" / "scripts"

sys.path.insert(0, str(cholesky_dir))
sys.path.insert(0, str(lu_dir))
sys.path.insert(0, str(qr_dir))
sys.path.insert(0, str(svd_dir))
sys.path.insert(0, str(choose_dir))

from solve_cholesky import robust_solve_cholesky, factorize_cholesky, reconstruction_error as cholesky_recon_error
from solve_lu import robust_solve_lu, factorize_lu, reconstruction_error as lu_recon_error
from solve_qr import robust_solve_qr, qr_decompose
from solve_svd import robust_solve_svd, svd_decompose, reconstruction_error as svd_recon_error
from choose_decomposition import choose_decomposition


class BenchmarkRunner:
    """Run benchmarks on matrix computation skills"""

    def __init__(self):
        self.results = {
            "decomposition_accuracy": [],
            "computation_time": [],
            "ill_conditioned_handling": [],
            "method_selection": [],
            "consistency": []
        }

    def generate_test_matrices(self) -> Dict[str, np.ndarray]:
        """Generate various test matrices"""
        matrices = {}

        # 1. Well-conditioned SPD matrix
        np.random.seed(42)
        A = np.random.randn(10, 10)
        matrices["well_conditioned_spd"] = A.T @ A + 5 * np.eye(10)

        # 2. Ill-conditioned Hilbert matrix (12x12)
        n = 12
        matrices["hilbert_12"] = np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)])

        # 3. Random rectangular matrix (overdetermined)
        matrices["rectangular_over"] = np.random.randn(15, 8)

        # 4. Random rectangular matrix (underdetermined)
        matrices["rectangular_under"] = np.random.randn(8, 15)

        # 5. Sparse SPD matrix (tridiagonal)
        n = 100
        matrices["sparse_spd"] = np.zeros((n, n))
        for i in range(n):
            matrices["sparse_spd"][i, i] = 2.0
            if i > 0:
                matrices["sparse_spd"][i, i-1] = -1.0
                matrices["sparse_spd"][i-1, i] = -1.0

        # 6. Random general square matrix
        matrices["general_square"] = np.random.randn(10, 10)

        return matrices

    def benchmark_decomposition_accuracy(self) -> List[Dict]:
        """Test decomposition accuracy"""
        print("=" * 60)
        print("TEST 1: Decomposition Accuracy")
        print("=" * 60)

        matrices = self.generate_test_matrices()
        results = []

        # Test Cholesky on SPD matrix
        A_spd = matrices["well_conditioned_spd"]
        b = np.ones(10)
        x, report = robust_solve_cholesky(A_spd, b)
        L = factorize_cholesky(A_spd)
        recon_error = cholesky_recon_error(A_spd, L)
        results.append({
            "method": "Cholesky",
            "matrix": "well_conditioned_spd",
            "reconstruction_error": float(recon_error),
            "residual_norm": float(report.get("residual_norm", 0))
        })
        print(f"Cholesky on SPD: recon_error = {recon_error:.2e}, residual = {report.get('residual_norm', 0):.2e}")

        # Test LU on general square matrix
        A_general = matrices["general_square"]
        b = np.ones(10)
        try:
            P, L, U = factorize_lu(A_general)
            recon_error = lu_recon_error(A_general, P, L, U)
            x, report = robust_solve_lu(A_general, b)
            residual = report.get("residual_norm", np.linalg.norm(A_general @ x - b))
            results.append({
                "method": "LU",
                "matrix": "general_square",
                "reconstruction_error": float(recon_error),
                "residual_norm": float(residual)
            })
            print(f"LU on general square: recon_error = {recon_error:.2e}, residual = {residual:.2e}")
        except Exception as e:
            print(f"LU test failed: {e}")

        # Test QR on rectangular matrix
        A_rect = matrices["rectangular_over"]
        b = np.ones(15)
        try:
            Q, R = qr_decompose(A_rect)
            recon_error = np.linalg.norm(A_rect - Q @ R)
            x, report = robust_solve_qr(A_rect, b)
            residual = report.get("residual_norm", np.linalg.norm(A_rect @ x - b))
            results.append({
                "method": "QR",
                "matrix": "rectangular_over",
                "reconstruction_error": float(recon_error),
                "residual_norm": float(residual)
            })
            print(f"QR on rectangular: recon_error = {recon_error:.2e}, residual = {residual:.2e}")
        except Exception as e:
            print(f"QR test failed: {e}")

        # Test SVD on various matrices
        for name in ["well_conditioned_spd", "rectangular_over", "general_square"]:
            A = matrices[name]
            try:
                U, S, Vt = svd_decompose(A)
                recon_error = svd_recon_error(A, U, S, Vt)
                results.append({
                    "method": "SVD",
                    "matrix": name,
                    "reconstruction_error": float(recon_error),
                    "residual_norm": 0.0
                })
                print(f"SVD on {name}: recon_error = {recon_error:.2e}")
            except Exception as e:
                print(f"SVD test on {name} failed: {e}")

        self.results["decomposition_accuracy"] = results
        return results

    def benchmark_computation_time(self) -> List[Dict]:
        """Test computation time for different methods"""
        print("\n" + "=" * 60)
        print("TEST 2: Computation Time")
        print("=" * 60)

        results = []
        sizes = [50, 100, 200, 500]
        n_runs = 10

        for size in sizes:
            print(f"\nTesting size {size}x{size}:")

            # Generate SPD matrix
            np.random.seed(42)
            A = np.random.randn(size, size)
            A_spd = A.T @ A + size * np.eye(size)
            b = np.ones(size)

            # Time Cholesky
            times = []
            for _ in range(n_runs):
                start = time.perf_counter()
                x, report = robust_solve_cholesky(A_spd, b)
                end = time.perf_counter()
                times.append(end - start)
            cholesky_time = np.mean(times)
            print(f"  Cholesky: {cholesky_time*1000:.2f} ms")

            # Time LU
            times = []
            for _ in range(n_runs):
                start = time.perf_counter()
                x, report = robust_solve_lu(A, b)
                end = time.perf_counter()
                times.append(end - start)
            lu_time = np.mean(times)
            print(f"  LU: {lu_time*1000:.2f} ms")

            # Time SVD
            times = []
            for _ in range(n_runs):
                start = time.perf_counter()
                U, S, Vt = svd_decompose(A)
                end = time.perf_counter()
                times.append(end - start)
            svd_time = np.mean(times)
            print(f"  SVD: {svd_time*1000:.2f} ms")

            results.append({
                "size": size,
                "cholesky_time_ms": float(cholesky_time * 1000),
                "lu_time_ms": float(lu_time * 1000),
                "svd_time_ms": float(svd_time * 1000)
            })

        self.results["computation_time"] = results
        return results

    def benchmark_ill_conditioned_handling(self) -> List[Dict]:
        """Test handling of ill-conditioned matrices"""
        print("\n" + "=" * 60)
        print("TEST 3: Ill-conditioned Matrix Handling")
        print("=" * 60)

        results = []

        # Test Hilbert matrices of different sizes
        for n in [8, 10, 12, 15]:
            print(f"\nTesting Hilbert matrix {n}x{n}:")
            A = np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)])
            cond = np.linalg.cond(A)
            print(f"  Condition number: {cond:.2e}")

            result = {
                "matrix": f"hilbert_{n}",
                "condition_number": float(cond)
            }

            # Try Cholesky
            try:
                x, report = robust_solve_cholesky(A, np.ones(n))
                result["cholesky_success"] = True
                result["cholesky_method"] = report.get("method", "unknown")
                result["cholesky_error"] = None
                print(f"  Cholesky: Success (method: {report.get('method')})")
            except Exception as e:
                result["cholesky_success"] = False
                result["cholesky_error"] = str(e)
                print(f"  Cholesky: Failed - {type(e).__name__}")

            # Try SVD (should always work)
            try:
                x, report = robust_solve_svd(A, np.ones(n))
                result["svd_success"] = True
                result["svd_method"] = report.get("method", "unknown")
                result["svd_error"] = None
                print(f"  SVD: Success (method: {report.get('method')})")
            except Exception as e:
                result["svd_success"] = False
                result["svd_error"] = str(e)
                print(f"  SVD: Failed - {e}")

            results.append(result)

        self.results["ill_conditioned_handling"] = results
        return results

    def benchmark_method_selection(self) -> List[Dict]:
        """Test automatic method selection"""
        print("\n" + "=" * 60)
        print("TEST 4: Method Selection Accuracy")
        print("=" * 60)

        results = []
        test_cases = [
            ("SPD matrix", "cholesky", "well_conditioned_spd"),
            ("General square", "lu", "general_square"),
            ("Rectangular (over)", "qr", "rectangular_over"),
            ("Rectangular (under)", "svd", "rectangular_under"),
        ]

        matrices = self.generate_test_matrices()

        for description, expected_method, matrix_key in test_cases:
            A = matrices[matrix_key]
            b = np.ones(A.shape[0]) if A.shape[0] == A.shape[1] else np.ones(A.shape[0])

            choice = choose_decomposition(A, b if A.shape[0] == A.shape[1] else None)
            selected_method = choice.get("method", "unknown")

            is_correct = selected_method == expected_method

            result = {
                "description": description,
                "matrix_key": matrix_key,
                "expected_method": expected_method,
                "selected_method": selected_method,
                "correct": is_correct,
                "reason": choice.get("reason", "")
            }

            results.append(result)

            status = "[OK]" if is_correct else "[FAIL]"
            print(f"{status} {description}: expected {expected_method}, got {selected_method}")

        accuracy = sum(1 for r in results if r["correct"]) / len(results) * 100
        print(f"\nMethod selection accuracy: {accuracy:.1f}%")

        self.results["method_selection"] = results
        return results

    def benchmark_consistency(self) -> List[Dict]:
        """Test consistency - same input should give same output"""
        print("\n" + "=" * 60)
        print("TEST 5: Consistency (Multiple Runs)")
        print("=" * 60)

        results = []

        # Test Cholesky consistency
        np.random.seed(123)
        A = np.random.randn(10, 10)
        A_spd = A.T @ A + 10 * np.eye(10)
        b = np.ones(10)

        solutions = []
        for i in range(5):
            x, report = robust_solve_cholesky(A_spd, b)
            solutions.append(x)

        # Check if all solutions are identical
        max_diff = max(np.linalg.norm(solutions[i] - solutions[j])
                      for i in range(len(solutions)) for j in range(i+1, len(solutions)))

        results.append({
            "method": "Cholesky",
            "runs": 5,
            "max_difference": float(max_diff),
            "consistent": max_diff < 1e-10
        })

        print(f"Cholesky consistency: max_diff = {max_diff:.2e} ({'PASS' if max_diff < 1e-10 else 'FAIL'})")

        # Test SVD consistency
        singular_values = []
        for i in range(5):
            U, S, Vt = svd_decompose(A_spd)
            singular_values.append(S)

        max_sv_diff = max(np.linalg.norm(singular_values[i] - singular_values[j])
                         for i in range(len(singular_values)) for j in range(i+1, len(singular_values)))

        results.append({
            "method": "SVD",
            "runs": 5,
            "max_difference": float(max_sv_diff),
            "consistent": max_sv_diff < 1e-10
        })

        print(f"SVD consistency: max_diff = {max_sv_diff:.2e} ({'PASS' if max_sv_diff < 1e-10 else 'FAIL'})")

        self.results["consistency"] = results
        return results

    def run_all_benchmarks(self) -> Dict:
        """Run all benchmarks"""
        print("\n" + "=" * 60)
        print("Matrix Computation Skills Benchmark Suite")
        print("=" * 60)
        print(f"NumPy version: {np.__version__}")
        print(f"Platform: {sys.platform}")
        print("=" * 60)

        self.benchmark_decomposition_accuracy()
        self.benchmark_computation_time()
        self.benchmark_ill_conditioned_handling()
        self.benchmark_method_selection()
        self.benchmark_consistency()

        return self.results

    def save_results(self, filename: str = "benchmark_results.json"):
        """Save results to JSON file"""
        output_path = Path(__file__).parent / filename

        # Convert numpy types to native Python types
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

    def print_summary(self):
        """Print summary of benchmark results"""
        print("\n" + "=" * 60)
        print("BENCHMARK SUMMARY")
        print("=" * 60)

        # Decomposition accuracy
        if self.results["decomposition_accuracy"]:
            print("\n1. Decomposition Accuracy:")
            for r in self.results["decomposition_accuracy"]:
                print(f"   {r['method']} on {r['matrix']}: recon_error = {r['reconstruction_error']:.2e}")

        # Method selection
        if self.results["method_selection"]:
            accuracy = sum(1 for r in self.results["method_selection"] if r["correct"]) / len(self.results["method_selection"]) * 100
            print(f"\n2. Method Selection Accuracy: {accuracy:.1f}%")

        # Ill-conditioned handling
        if self.results["ill_conditioned_handling"]:
            print("\n3. Ill-conditioned Handling:")
            for r in self.results["ill_conditioned_handling"]:
                cholesky_status = f"Success ({r.get('cholesky_method', 'unknown')})" if r["cholesky_success"] else "Failed"
                svd_status = f"Success ({r.get('svd_method', 'unknown')})" if r["svd_success"] else "Failed"
                print(f"   {r['matrix']} (cond={r['condition_number']:.2e}):")
                print(f"     Cholesky: {cholesky_status}, SVD: {svd_status}")

        # Consistency
        if self.results["consistency"]:
            print("\n4. Consistency Test:")
            for r in self.results["consistency"]:
                status = "PASS" if r["consistent"] else "FAIL"
                print(f"   {r['method']}: {status} (max_diff = {r['max_difference']:.2e})")


if __name__ == "__main__":
    runner = BenchmarkRunner()
    runner.run_all_benchmarks()
    runner.save_results()
    runner.print_summary()
