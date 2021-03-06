from setuptools import setup, find_packages

setup(
    name='clampy',
    version='0.1',
    description='A Python package to control a patch-clamp amplifier',
    url='https://github.com/romainbrette/clampy/',
    author='Romain Brette',
    author_email='romain.brette@inserm.fr',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],
    packages=find_packages(),
    install_requires=['numpy', 'scipy', 'brian2', 'nidaqmx']
)
