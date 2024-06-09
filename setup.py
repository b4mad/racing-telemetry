from setuptools import setup, find_packages

setup(
    name='telemetry',
    version='0.1.0',
    packages=find_packages(include=['telemetry', 'telemetry.retrieval', 'telemetry.adapter']),
    install_requires=[
        # Add any dependencies here
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='A library for telemetry data analysis',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/racing-data-analysis',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
