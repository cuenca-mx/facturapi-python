from importlib.machinery import SourceFileLoader

from setuptools import find_packages, setup

version = SourceFileLoader('version', 'facturapi/version.py').load_module()

install_requirements = [
    'dataclasses>=0.6;python_version<"3.7"',
    'requests>=2.22.0,<3.0.0',
]

test_requires = [
    'pytest',
    'pytest-vcr',
    'pytest-cov',
    'coverage<5.0,>=3.6',
    'flake8==3.7.9',
    'isort>=4.3.21,<4.4',
    'black>=19.10b0,<20.0',
    'mypy>=0.770',
]

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='dhl',
    version=version.__version__,
    author='Cuenca',
    author_email='dev@cuenca.com',
    description='Client library for Facturapi',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://https://github.com/cuenca-mx/facturapi-python',
    packages=find_packages(),
    include_package_data=True,
    package_data=dict(dhl=['py.typed']),
    python_requires='>=3.6',
    install_requires=install_requirements,
    setup_requires=['pytest-runner'],
    tests_require=test_requires,
    extras_require=dict(test=test_requires),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
