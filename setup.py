# Automatically created by: scrapyd-deploy

from setuptools import setup, find_packages

import adslproxy

setup(
    name='adslproxy',
    version=adslproxy.version(),
    packages=find_packages(),
    author='Germey',
    keywords=['adsl', 'proxy'],
    author_email='cqc@cuiqingcai.com',
    url='http://pypi.python.org/pypi/adslproxy/',
    license='MIT License',
    description='ADSLProxy Package',
    long_description='ADSL Stable Proxy Service',
    install_requires=['requests>=2.13.0', 'tornado>=4.4.3', 'redis>=2.10.5']
)
