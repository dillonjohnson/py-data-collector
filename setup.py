from setuptools import setup
import os

the_lib_folder = os.path.dirname(os.path.realpath(__file__))

requirement_path = the_lib_folder + '/requirements.txt'
install_requires = []
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()

setup(
    name='py-data-collector',
    version='1.0',
    packages=[
        'py_data_collector',
        'py_data_collector.sources',
        'py_data_collector.transformers'
    ],
    url='',
    license='',
    author='dillonjohnson',
    author_email='dillonjohnson1015@gmail.com',
    description='This library is to collect various data points.',
    install_require=install_requires
)
