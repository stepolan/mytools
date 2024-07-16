import requests
from bs4 import BeautifulSoup
import yaml
import argparse
import os

def get_conda_license(package_name):
    url = f"https://anaconda.org/conda-forge/{package_name}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        license_tag = soup.find('i', class_='icon-key')
        if license_tag:
            return license_tag.next_sibling.strip()
    return "License not found"

def get_pip_license(package_name):
    package_name = package_name.split('==')[0]
    url = f"https://pypi.org/project/{package_name}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        license_tag = soup.find('p', class_='package-header__pip-instructions')
        if license_tag:
            license_text = license_tag.find_next_sibling('p')
            if license_text:
                return license_text.text.split('License')[1].split(' ')[1].strip()
    return "License not found"

def read_requirements(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip() and not line.startswith('#')]

def read_environment(file_path):
    with open(file_path, 'r') as file:
        env_data = yaml.safe_load(file)
        dependencies = env_data.get('dependencies', [])
        conda_packages = []
        pip_packages = []
        for dep in dependencies:
            if isinstance(dep, str):
                conda_packages.append(dep)
            elif isinstance(dep, dict) and 'pip' in dep:
                pip_packages.extend(dep['pip'])
        return conda_packages, pip_packages

def write_to_markdown(conda_licenses, pip_licenses, output_file):
    with open(output_file, 'w') as file:
        file.write("# Python Package Licenses\n\n")
        file.write("## Conda Packages\n")
        for pkg, license in conda_licenses.items():
            file.write(f"- **{pkg}**: {license}\n")
        file.write("\n## Pip Packages\n")
        for pkg, license in pip_licenses.items():
            file.write(f"- **{pkg}**: {license}\n")

def main():
    parser = argparse.ArgumentParser(description="Fetch licenses for Python packages listed in environment.yml and requirements.txt")
    parser.add_argument('-d', '--directory', default='.', help="Directory containing the environment.yml and requirements.txt files")
    parser.add_argument('-e', '--envfile', default='environment.yml', help="Path to the environment.yml file")
    parser.add_argument('-r', '--reqfile', default='requirements.txt', help="Path to the requirements.txt file")
    parser.add_argument('-o', '--output', default='py_pkg_licenses.md', help="Output markdown file")

    args = parser.parse_args()

    env_file_path = os.path.join(args.directory, args.envfile)
    req_file_path = os.path.join(args.directory, args.reqfile)

    conda_packages, pip_packages = read_environment(env_file_path)
    pip_packages.extend(read_requirements(req_file_path))

    conda_licenses = {pkg: get_conda_license(pkg) for pkg in conda_packages}
    pip_licenses = {pkg: get_pip_license(pkg) for pkg in pip_packages}

    write_to_markdown(conda_licenses, pip_licenses, args.output)

if __name__ == "__main__":
    main()
