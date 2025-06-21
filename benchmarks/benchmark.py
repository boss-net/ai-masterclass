import logging
import time
from dataclasses import dataclass
from typing import Any, Callable, Dict

logger = logging.getLogger(__name__)


@dataclass
class BenchmarkResult:
    name: str
    duration: float
    success: bool
    error: str = None
    metrics: Dict[str, Any] = None


class BenchmarkRunner:
    def __init__(self, module_name: str):
        self.module_name = module_name
        self.results = []
        self.metrics = MetricsCollector()

    def run(self, func: Callable, *args, **kwargs) -> BenchmarkResult:
        """Run a benchmark test."""
        start_time = time.time()

        try:
            result = func(*args, **kwargs)
            success = True
            error = None
        except Exception as e:
            result = None
            success = False
            error = str(e)
            logger.error(f"Benchmark failed: {e}")

        duration = time.time() - start_time

        # Collect metrics
        metrics = self.metrics.collect()

        # Create result
        result = BenchmarkResult(
            name=func.__name__,
            duration=duration,
            success=success,
            error=error,
            metrics=metrics,
        )

        self.results.append(result)
        return result

    def report(self) -> Dict[str, Any]:
        """Generate benchmark report."""
        total_duration = sum(r.duration for r in self.results)
        success_count = sum(1 for r in self.results if r.success)
        failure_count = len(self.results) - success_count

        return {
            "module": self.module_name,
            "total_tests": len(self.results),
            "success": success_count,
            "failures": failure_count,
            "total_duration": total_duration,
            "average_duration": total_duration / len(self.results)
            if self.results
            else 0,
            "results": [r.__dict__ for r in self.results],
        }

    def save_report(self, path: str):
        """Save benchmark report to file."""
        import json

        report = self.report()
        with open(path, "w") as f:
            json.dump(report, f, indent=2)

        logger.info(f"Benchmark report saved to {path}")
