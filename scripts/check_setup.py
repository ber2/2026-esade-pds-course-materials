import importlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = REPO_ROOT / "data" / "raw"
REQUIRED_PYTHON = (3, 12)
REQUIRED_PACKAGES = ["pandas", "pyarrow", "plotly", "nbformat", "ipykernel"]
MAXIMUM_PANDAS_MAJOR = 2
EXPECTED_ROWS = {
    "olist_customers_dataset.csv": 99_441,
    "olist_order_items_dataset.csv": 112_650,
    "olist_order_payments_dataset.csv": 103_886,
    "olist_order_reviews_dataset.csv": 104_719,
    "olist_orders_dataset.csv": 99_441,
    "olist_products_dataset.csv": 32_951,
    "olist_sellers_dataset.csv": 3_095,
    "product_category_name_translation.csv": 71,
}
PASS = "OK  "
FAIL = "FAIL"


def report(passed, message):
    print(f"[{PASS if passed else FAIL}] {message}")
    return passed


def check_python():
    version = sys.version_info
    return report(
        version[:2] == REQUIRED_PYTHON,
        f"Python {version.major}.{version.minor}.{version.micro} at {sys.executable}",
    )


def check_package(name):
    try:
        module = importlib.import_module(name)
    except ImportError:
        return report(False, f"{name} is missing: run  conda env update -f environment.yml --prune")
    version = getattr(module, "__version__", "unknown")
    if name == "pandas" and int(version.split(".")[0]) > MAXIMUM_PANDAS_MAJOR:
        return report(False, f"pandas {version}: this course needs pandas 2.x. Run  conda env update -f environment.yml --prune")
    return report(True, f"{name} {version}")


def count_rows(path):
    with open(path, encoding="utf-8") as file:
        return sum(1 for _ in file) - 1


def check_data_file(name, expected_rows):
    path = RAW_DIR / name
    if not path.is_file():
        return report(False, f"data/raw/{name} is missing: run  python scripts/download_data.py")
    rows = count_rows(path)
    return report(rows == expected_rows, f"data/raw/{name}: {rows:,} rows (expected {expected_rows:,})")


def main():
    print("Environment")
    results = [check_python()] + [check_package(name) for name in REQUIRED_PACKAGES]
    print("\nData")
    results += [check_data_file(name, rows) for name, rows in EXPECTED_ROWS.items()]
    print()
    if all(results):
        print("All good. You are ready for the session.")
        return
    print("Something is not right. Fix the FAIL lines above. If you cannot, bring this whole output to class.")
    sys.exit(1)


if __name__ == "__main__":
    main()
