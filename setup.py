from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='config-params',
    version='0.0.1',
    description='Confuration Parameter Parser',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kuenishi/config-params',
    author='Kota Uenishi',
    author_email='kuenishi+configparams@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='configuration parameter',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=3.5, <4',
    install_requires=['pyyaml'],
    extras_require={
        'test': ['coverage', 'pytest', 'flake8', 'pytest-xdist'],
    },
    project_urls={
        'Source': 'https://github.com/kuenishi/config-params',
    },
)
