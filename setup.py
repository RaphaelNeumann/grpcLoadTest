from setuptools import setup
setup(
    name = 'grpcLoadTest',
    version = '0.0.1',
    packages = ['grpcLoadTest'],
    scripts=['./scripts/grpcLoadTest'],
    install_requires = [
        'grpcio',
        'grpcio-tools',
        'argparse',
    ],
    entry_points = {
        'console_scripts': [
            'pycli = grpcLoadTest.__main__:main'
        ]
    })