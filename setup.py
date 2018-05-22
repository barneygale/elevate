from distutils.core import setup

setup(
    name='elevate',
    version='0.1.3',
    author='Barney Gale',
    author_email='barney.gale@gmail.com',
    url='https://github.com/barneygale/elevate',
    license='MIT',
    description='Python library for requesting root privileges',
    long_description=open('README.rst').read(),
    packages=["elevate"],
)
