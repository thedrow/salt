#!/usr/bin/env python
# coding: utf-8

# import Python Libs
from collections import OrderedDict

# Import Salt Libs
from distutils.version import LooseVersion
from mock import Mock
from salt.states import boto_vpc

# Import Salt Testing Libs
from salttesting import TestCase

required_boto_version = '2.8.0'
region = 'us-east-1'
access_key = 'GKTADJGHEIQSXMKKRBJ08H'
secret_key = 'askdjghsdfjkghWupUjasdflkdfklgjsdfjajkghs'
conn_parameters = {'region': region, 'key': access_key, 'keyid': secret_key, 'profile': {}}
cidr_block = '10.0.0.0/24'

boto_vpc_exists_mock = Mock()
boto_vpc.__salt__ = {
    'boto_vpc.exists': boto_vpc_exists_mock,
    'boto_vpc.create': Mock()
}

try:
    import boto

    HAS_BOTO = True
except ImportError:
    HAS_BOTO = False

try:
    import moto
    from moto import mock_ec2

    HAS_MOTO = True
except ImportError:
    HAS_MOTO = False

    def mock_ec2(self):
        '''
        if the mock_ec2 function is not available due to import failure
        this replaces the decorated function with stub_function.
        Allows boto_vpc unit tests to use the @mock_ec2 decorator
        without a "NameError: name 'mock_ec2' is not defined" error.
        '''

        def stub_function(self):
            pass

        return stub_function


def _has_required_boto():
    '''
    Returns True/False boolean depending on if Boto is installed and correct
    version.
    '''
    if not HAS_BOTO:
        return False
    elif LooseVersion(boto.__version__) < LooseVersion(required_boto_version):
        return False
    else:
        return True


def _has_required_moto():
    '''
    Returns True/False boolean depending on if Moto is installed and correct
    version.
    '''
    if not HAS_MOTO:
        return False
    else:
        import pkg_resources

        if LooseVersion(pkg_resources.get_distribution('moto').version) < LooseVersion('0.3.7'):
            return False
        return True


class BotoVpcPresentStateTestCase(TestCase):
    @mock_ec2
    def test_that_when_a_vpc_does_not_exist_with_the_provided_name_it_is_created(self):
        boto_vpc_exists_mock.return_value = False
        state_result = boto_vpc.present('TestVPC', cidr_block=cidr_block, **conn_parameters)

        self.assertEqual(state_result['changes'], {'old': 'VPC TestVPC did not exist', 'new': 'VPC TestVPC was created'})

if __name__ == '__main__':
    from integration import run_tests
    run_tests(BotoVpcPresentStateTestCase)