import os
import subprocess

env = os.environ.copy()
env["PYTHONIOENCODING"] = "utf-8"
env["DBT_PROFILES_DIR"] = "."

def run_mf(args):
    cmd = [os.path.join(".venv", "Scripts", "mf.exe")] + args
    print(f"\n==================================================")
    print(f"Running: {' '.join(cmd)}")
    print(f"==================================================")
    res = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace", cwd=".", env=env)
    print("STDOUT:")
    print(res.stdout)
    if res.stderr:
        print("STDERR:")
        print(res.stderr)
    return res.returncode

if __name__ == "__main__":
    run_mf(["validate-configs"])
    run_mf(["list", "metrics"])
    run_mf(["query", "--metrics", "active_customers,active_customers_365d,engaged_customers_30d", "--group-by", "customer__segment"])
    run_mf(["query", "--metrics", "total_revenue", "--group-by", "metric_time__month"])
