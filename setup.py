'''
The setup.py file is an essential part of packaging and
distributing Python projects. It is used by setuptools
(or distutils in older Python versions) to define the configuration
of your project, such as its metadata, dependencies, and more
'''


from setuptools import find_packages, setup
# From network_security this will scan all the files
from typing import List

def get_reqirements() -> List[str]:
    """
    This function will return list of requirements
    """
    requirements_lst:List[str] = []
    try:
        with open('requirements.txt', 'r') as file:
            # Read the line from the file
            lines = file.readlines()
            # Process each line
            for line in lines:
                requirements = line.strip()
                # Ignore the empty lines and -e .
                if requirements and requirements!='-e .':
                    requirements_lst.append(requirements)
                    
                
    except FileNotFoundError:
        print('No requirements.txt file found.')
        
    return requirements_lst

setup(
    name = 'Network_Security',
    version = '0.0.0.1',
    author = 'Kunal ',
    author_email= 'gauravvaishya143@gmail.com',
    packages = find_packages(),
    install_requires = get_reqirements()
    # This will try to get the package name from requirements.txt file
    # This will create a files in Data_Security in the folder
)