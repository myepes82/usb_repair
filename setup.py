from setuptools import setup, find_packages

setup(
    name='repair_usb',
    version='1.0.0',
    author='Marlon Yepes',
    author_email='marlondevjs@gmail.com',
    description='USB Repairing tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/myepes82/usb_repair',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    entry_points={
        'console_scripts': [
            'repair_usb=main:main',
        ],
    },
)
