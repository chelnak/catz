import subprocess


def run():
    """
    Run all unittests. Equivalent to:
    `poetry run python -m unittest discover -s tests`
    """
    subprocess.run(["python", "-m", "unittest", "discover", "-s", "."])
