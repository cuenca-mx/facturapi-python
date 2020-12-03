from importlib.machinery import SourceFileLoader

from setuptools import find_packages, setup

version = SourceFileLoader('version', 'facturapi/version.py').load_module()


with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name='facturapi',
    version=version.__version__,
    author='Cuenca',
    author_email='dev@cuenca.com',
    description='Facturapi API Client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cuenca-mx/facturapi-python',
    packages=find_packages(),
    include_package_data=True,
    package_data=dict(facturapi=['py.typed']),
    python_requires='>=3.6',
    install_requires=[
        'requests>=2.4,<2.25',
        'pydantic==1.7.3',
        'dataclasses>=0.7;python_version<"3.7"',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
