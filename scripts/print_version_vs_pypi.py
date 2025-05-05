import os
import toml
import requests
from packaging.version import Version, InvalidVersion
from pathlib import Path

def extract_info(pyproject_path):
    try:
        data = toml.load(pyproject_path)
        project = data.get('project') or {}
        name = project.get('name')
        version = project.get('version')
        return name, version
    except Exception as e:
        return None, None

def get_latest_version_from_pypi(package_name):
    try:
        url = f"https://pypi.org/pypi/{package_name}/json"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()['info']['version']
    except Exception:
        pass
    return None

def compare_versions(local, remote):
    try:
        local_v = Version(local)
        remote_v = Version(remote)
        if local_v == remote_v:
            return "✅"
        elif local_v < remote_v:
            return "🔼"
        else:
            return "🔽"
    except InvalidVersion:
        return "❓"

def main():
    base_path = Path("../packages")
    pyproject_files = base_path.rglob("pyproject.toml")

    header = f"{'File':30} | {'Local':10} | {'PyPI':15} | {'↕'}"
    print(header)
    print(f"{'='*30} | {'='*10} | {'='*15} | ===")

    for filepath in pyproject_files:
        name, local_version = extract_info(filepath)
        if not name or not local_version:
            print(f"{str(name):30} | {'Not Found':10} | {'Not Found':15} | ❓")
            continue

        pypi_version = get_latest_version_from_pypi(name)
        status = compare_versions(local_version, pypi_version) if pypi_version else "❓"

        print(f"{str(name):30} | {local_version:10} | {pypi_version or 'Not Found':15} | {status}")

if __name__ == "__main__":
    main()
