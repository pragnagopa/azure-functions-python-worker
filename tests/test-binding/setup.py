##
# Copyright (c) 2017-present MagicStack Inc.
# All rights reserved.
#
# See LICENSE for details.
##


from setuptools import setup


setup(
    name='foo-binding',
    version='1.0',
    packages=['foo'],
    entry_points={
        'azure.functions.bindings': [
            'foo=foo.binding:Binding',
        ]
    },
)
