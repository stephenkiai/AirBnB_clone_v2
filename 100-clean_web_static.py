#!/usr/bin/python3
""" 
    Fabric script (based on the file 3-deploy_web_static.py)
    that deletes out-of-date archives, using the function do_clean
"""
env.hosts = ['52.91.202.128', '54.197.207.49']
env.user = "ubuntu"


def do_clean(number=0):
    """ deletes out-of-date archives """

    number = int(number)

    if number == 0:
        number = 2
    else:
        number += 1

    local('cd versions ; ls -t | tail -n +{} | xargs rm -rf'.format(number))
    path = '/data/web_static/releases'
    run('cd {} ; ls -t | tail -n +{} | xargs rm -rf'.format(path, number))
