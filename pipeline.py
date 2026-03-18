import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

scripts = Path(__file__).parent


def run(script):
    result = subprocess.run(
        [sys.executable, script],
        capture_output=False,
        text=True,
    )
    return script, result.returncode


with ThreadPoolExecutor(max_workers=2) as executor:
    futures = {
        executor.submit(run, scripts / "historical-gtfs.py"): "gtfs",
        executor.submit(run, scripts / "historical-weather.py"): "weather",
    }
    for future in as_completed(futures):
        script, code = future.result()
        if code != 0:
            print(f"{script} failed with exit code {code}")
            sys.exit(code)

subprocess.run([sys.executable, scripts / "to-csv.py"], check=True)
