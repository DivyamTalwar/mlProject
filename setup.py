from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT = '-e .'


def get_requirements(file_path: str) -> List[str]:
    '''
    This function will return the list of requirements.
    '''
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.strip() for req in requirements if req.strip()]

        # Remove '-e .' if present
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements


setup(
    name='mlproject',
    version='0.0.1',
    author='Divyam Talwar',
    author_email='divyamtalwar0@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)


"""
find_packages():
Automatically detects all Python packages in your project by looking for folders containing an __init__.py file.

get_requirements() function: Reads the requirements.txt file.

"""
