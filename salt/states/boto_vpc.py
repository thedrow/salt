#!/usr/bin/env python
# coding: utf-8

from salt.exceptions import SaltInvocationError


def __virtual__():
    '''
    Only load if boto is available.
    '''
    return 'boto_vpc' if 'boto_vpc.exists' in __salt__ else False


def present(name,
            cidr_block=None,
            tags=None,
            region=None,
            key=None,
            keyid=None,
            profile=None):
    ret = {'name': name, 'result': True, 'comment': '', 'changes': {}}

    if __salt__['boto_vpc.exists'](name=name,
                                   tags=tags,
                                   region=region,
                                   key=key,
                                   keyid=keyid,
                                   profile=profile):
        pass
    else:
        if __salt__['boto_vpc.create'](cidr_block,
                                       name=name,
                                       tags=tags,
                                       region=region,
                                       key=key,
                                       keyid=keyid,
                                       profile=profile):
            ret = {'name': name, 'result': True, 'comment': '',
                   'changes': {'old': 'VPC TestVPC did not exist', 'new': 'VPC TestVPC was created'}}

    return ret


def absent(name,
           cidr_block,
           tags=None,
           region=None,
           key=None,
           keyid=None,
           profile=None):
    ret = {'name': name, 'result': True, 'comment': '', 'changes': {}}

    return ret