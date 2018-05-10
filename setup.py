from setuptools import setup

setup(
    name='death-rates',
    version='1.0.0',
    packages=['death_rates'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask-cors',
        'requests',
        'pandas',
        'xlrd'
    ],
)