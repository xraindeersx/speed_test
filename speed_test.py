#!/usr/bin/env python3

import argparse
import requests
import sys
import time


class SpeedTester:
    BYTES_IN_MB = 1024 * 1024
    CHUNK_SIZE = 64 * 1024

    def __init__(self, url: str, requests_count: int = 10, timeout: float = 30.0) -> None:
        if requests_count <= 0:
            raise ValueError("requests_count must be greater than 0")
        if timeout <= 0:
            raise ValueError("timeout must be greater than 0")

        self.url = url
        self.requests_count = requests_count
        self.timeout = timeout

    def request_once(self) -> tuple[float, int]:
        start = time.perf_counter()
        total_bytes = 0
        with requests.get(
            self.url,
            headers={
                "User-Agent": "Mozilla/5.0 (speed-test-script)",
                "Accept-Encoding": "identity",
            },
            timeout=self.timeout,
            stream=True,
        ) as response:
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=self.CHUNK_SIZE):
                if chunk:
                    total_bytes += len(chunk)
        elapsed = time.perf_counter() - start
        return elapsed, total_bytes

    def run(self) -> dict[str, float]:
        total_time_sec = 0.0
        total_bytes = 0

        for index in range(1, self.requests_count + 1):
            try:
                elapsed, payload_size = self.request_once()
            except requests.RequestException as exc:
                raise RuntimeError(f"request {index} failed: {exc}") from exc

            total_time_sec += elapsed
            total_bytes += payload_size

        average_time_sec = total_time_sec / self.requests_count
        total_mb = total_bytes / self.BYTES_IN_MB
        speed_mb_s = total_mb / total_time_sec if total_time_sec > 0 else 0.0

        return {
            "average_time_sec": average_time_sec,
            "total_bytes": float(total_bytes),
            "total_mb": total_mb,
            "speed_mb_s": speed_mb_s,
            "total_time_sec": total_time_sec,
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run sequential HTTP requests and calculate average download speed."
    )
    parser.add_argument("url", help="Target URL for download")
    parser.add_argument(
        "requests_count",
        nargs="?",
        type=int,
        default=10,
        help="Number of sequential requests (default: 10)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Request timeout in seconds (default: 30)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        tester = SpeedTester(
            url=args.url,
            requests_count=args.requests_count,
            timeout=args.timeout,
        )
    except ValueError as exc:
        print(f"invalid arguments: {exc}", file=sys.stderr)
        return 1

    try:
        metrics = tester.run()
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"{metrics['speed_mb_s']:.3f} MB/s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
