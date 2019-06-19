from setuptools import setup, find_packages

with open('requirements.txt') as file:
    reqs = file.read().splitlines()

setup(
    name='budget-analysis',
    version='1.0.0',
    scripts=['scripts/BudgetAnalysis'],
    packages=find_packages(),
    description='Simple Budget Analysis tool',
    author='Brent Barbachem',
    author_email='barbacbd@dukes.jmu.edu',
    license='Proprietary',
    include_package_data=True,
    install_requires=reqs,
    dependency_links=[
        'https://pypi.org/simple/'
    ],
    zip_safe=False
)
