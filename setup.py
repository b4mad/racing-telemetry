from setuptools import setup, find_packages

setup(
    name='racing-telemetry',
    version='0.1.1',
    packages=find_packages(include=['telemetry']),
    install_requires=[
    ],
    author='Marcel Hild',
    author_email='hild@b4mad.net',
    description='A library for telemetry data analysis',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/b4mad/racing-telemetry',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
