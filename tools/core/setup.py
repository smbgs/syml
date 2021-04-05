# from pipenv.project import Project
# from pipenv.utils import convert_deps_to_pip
from setuptools import setup, find_packages

# TODO: use pipenv to get proper requirements or parse them manually
# pfile = Project(chdir=False).parsed_pipfile
#
# requirements = convert_deps_to_pip(pfile['packages'], r=False)
# test_requirements = convert_deps_to_pip(pfile['dev-packages'], r=False)

import json

with open('Pipfile.lock') as fd:
    lock_data = json.load(fd)
    install_requires = [
        package_name + package_data['version']
        for package_name, package_data in lock_data['default'].items()
    ]
    tests_require = [
        package_name + package_data['version']
        for package_name, package_data in lock_data['develop'].items()
    ]

setup(
    name="syml_core",
    version="0.1.0",
    install_requires=install_requires,
    tests_require=tests_require,

    package_dir={'': 'src'},
    packages=find_packages(where='src'),
)

