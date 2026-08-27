import time
import inspect
from pathlib import Path
from functools import wraps
from datetime import datetime


class Debug:
    def __init__(self, enabled=False):
        self.enabled = enabled
        self.timings = []

        # Store model usage history
        self.model_usage = []

    def log(self, message):
        """Print a debug message."""
        if not self.enabled:
            return

        print(f"[DEBUG] {message}")

    def save_on_file(self, message, filename="debug_log.txt"):
        """Append a debug message to a file."""
        if not self.enabled:
            return

        path = Path(filename)

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with path.open("a", encoding="utf-8") as file:
            file.write(
                f"[{timestamp}] [DEBUG] "
                f"{message}\n"
            )

    def timer(self, func):
        """Decorator for measuring function execution time."""

        # Handle generator functions such as streaming LLM responses
        if inspect.isgeneratorfunction(func):

            @wraps(func)
            def generator_wrapper(*args, **kwargs):
                if not self.enabled:
                    yield from func(*args, **kwargs)
                    return

                start = time.perf_counter()

                try:
                    yield from func(*args, **kwargs)

                finally:
                    elapsed = time.perf_counter() - start

                    self._record_timing(
                        func.__name__,
                        elapsed
                    )

            return generator_wrapper

        # Handle normal functions
        @wraps(func)
        def wrapper(*args, **kwargs):

            if not self.enabled:
                return func(*args, **kwargs)

            start = time.perf_counter()

            try:
                return func(*args, **kwargs)

            finally:
                elapsed = time.perf_counter() - start

                self._record_timing(
                    func.__name__,
                    elapsed
                )

        return wrapper

    def _record_timing(self, function_name, elapsed):
        """Store execution time."""
        self.timings.append({
            "function": function_name,
            "elapsed": elapsed
        })

    def show_timings(self):
        """Display execution timings as a table."""
        if not self.enabled:
            return

        if not self.timings:
            print("[DEBUG] No timing data.")
            return

        total = sum(
            item["elapsed"]
            for item in self.timings
        )

        print("\n[DEBUG] EXECUTION TIME")
        print("-" * 58)

        print(
            f"{'Function':<30}"
            f"{'Time (s)':>12}"
            f"{'% Total':>12}"
        )

        print("-" * 58)

        for item in self.timings:
            elapsed = item["elapsed"]

            percentage = (
                elapsed / total * 100
                if total > 0
                else 0
            )

            print(
                f"{item['function']:<30}"
                f"{elapsed:>12.4f}"
                f"{percentage:>11.1f}%"
            )

        print("-" * 58)

        print(
            f"{'TOTAL':<30}"
            f"{total:>12.4f}"
            f"{'100.0%':>12}"
        )

    def clear_timings(self):
        """Reset timing data."""
        self.timings.clear()

    def record_model_usage(
    self,
    response,
    provider_name="Ollama"
    ):
        """Record model usage statistics."""

        if not self.enabled:
            return None

        def get_value(obj, key, default=None):
            if isinstance(obj, dict):
                return obj.get(key, default)

            return getattr(obj, key, default)

        model = get_value(
            response,
            "model",
            "unknown"
        )

        prompt_tokens = (
            get_value(
                response,
                "prompt_eval_count",
                0
            ) or 0
        )

        output_tokens = (
            get_value(
                response,
                "eval_count",
                0
            ) or 0
        )

        total_tokens = (
            prompt_tokens
            + output_tokens
        )

        # Ollama duration is nanoseconds
        eval_duration = (
            get_value(
                response,
                "eval_duration",
                0
            ) or 0
        )

        eval_duration_seconds = (
            eval_duration / 1_000_000_000
        )

        tokens_per_second = (
            output_tokens / eval_duration_seconds
            if eval_duration_seconds > 0
            else 0.0
        )

        # Ollama local
        cost = 0.0

        usage = {
            "provider": provider_name,
            "model": model,
            "prompt_tokens": prompt_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "tokens_per_second": tokens_per_second,
            "cost": cost
        }

        self.model_usage.append(usage)

        return usage

    def show_model_usage(self):
        """Display recorded model usage as a table."""

        if not self.enabled:
            return

        if not self.model_usage:
            print("\n[DEBUG] No model usage data.")
            return

        print("\n[DEBUG] MODEL USAGE")

        print("-" * 105)

        print(
            f"{'Provider':<12}"
            f"{'Model':<22}"
            f"{'Prompt':>12}"
            f"{'Output':>12}"
            f"{'Total':>12}"
            f"{'Token/s':>12}"
            f"{'Cost':>16}"
        )

        print("-" * 105)

        total_prompt = 0
        total_output = 0
        total_tokens = 0
        total_cost = 0.0

        total_generation_time = 0.0

        for usage in self.model_usage:

            provider = usage.get(
                "provider",
                "unknown"
            )

            model = usage.get(
                "model",
                "unknown"
            )

            prompt_tokens = usage.get(
                "prompt_tokens",
                0
            )

            output_tokens = usage.get(
                "output_tokens",
                0
            )

            tokens = usage.get(
                "total_tokens",
                0
            )

            tokens_per_second = usage.get(
                "tokens_per_second",
                0.0
            )

            cost = usage.get(
                "cost",
                0.0
            )

            total_prompt += prompt_tokens
            total_output += output_tokens
            total_tokens += tokens
            total_cost += cost

            cost_display = f"${cost:.6f}"

            print(
                f"{provider:<12}"
                f"{model:<22}"
                f"{prompt_tokens:>12}"
                f"{output_tokens:>12}"
                f"{tokens:>12}"
                f"{tokens_per_second:>12.2f}"
                f"{cost_display:>16}"
            )

        print("-" * 105)

        total_cost_display = (
            f"${total_cost:.6f}"
        )

        print(
            f"{'TOTAL':<34}"
            f"{total_prompt:>12}"
            f"{total_output:>12}"
            f"{total_tokens:>12}"
            f"{'-':>12}"
            f"{total_cost_display:>16}"
        )

    def clear_model_usage(self):
        """Reset recorded model usage."""
        self.model_usage.clear()
