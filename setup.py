#!/usr/bin/env python

#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

import re
import os.path
from io import open
from setuptools import find_packages, setup


# Change the PACKAGE_NAME only to change folder and different name
PACKAGE_NAME = "azure-iothub-device"
PACKAGE_PPRINT_NAME = "Azure IoT Hub Device"

# a-b-c => a/b/c
package_folder_path = PACKAGE_NAME.replace('-', '/')
# a-b-c => a.b.c
namespace_name = PACKAGE_NAME.replace('-', '.')

# Version extraction inspired from 'requests'
with open(os.path.join(package_folder_path, '__init__.py'), 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name=PACKAGE_NAME,
    version=version,
    description='Microsoft Azure {} Client Library for Python'.format(PACKAGE_PPRINT_NAME),
    long_description='test iot hub client',
    license='MIT License',
    author='Pierre Cauchois',
    author_email='pierreca@microsoft.com',
    url='https://github.com/pierreca/iothub-python',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
    ],
    zip_safe=False,
    packages=find_packages(exclude=["samples", "tests"]),
    install_requires=[
    ]
)