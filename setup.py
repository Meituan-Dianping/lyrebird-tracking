from setuptools import setup
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='lyrebird-tracking',
    version='0.10.2',
    packages=['lyrebird_tracking'],
    url='https://github.com/meituan/lyrebird-tracking',
    author='HBQA',
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    zip_safe=False,
    classifiers=(
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
    ),
    entry_points={
        'console_scripts': [
        ],
        'lyrebird_data_handler': [
            'tracking = lyrebird_tracking.tracking:TrackingHandler'
        ],
        'lyrebird_web': [
            'tracking = lyrebird_tracking.webui:Tracking'
        ]
    },
    install_requires=[
        'lyrebird', 'jsonschema'
    ]

)
