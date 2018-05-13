# -*- coding: utf-8 -*-
"""Fabfile for automating some mundane tasks."""
from fabric.api import env
from fabric.operations import put

env.forward_agent = True


def deploy():
    """Deploy my code."""
    env.hosts = ['raspberrypi']
    put('.', '/home/alarm/code')
