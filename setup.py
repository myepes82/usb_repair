from setuptools import setup, find_packages

setup(
    name='repair_usb',
    version='1.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'repair_usb=repair_usb:main_console',
        ],
    },
    install_requires=[
        'tk',
    ],
)
