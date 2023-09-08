#!/usr/bin/python3
""" web_static folder archiver"""

from fabric.api import local
import datetime import datetime


def do_pack():
    """ generate a tgz archive"""
    try:
        # Create the "versions" directory if it doesn't exist
        local("mkdir -p versions")

        # Compress the contents of the "web_static" folder
        local("tar -cvzf versions/web_static_{}.tgz web_static/".
              format(datetime.strftime("%Y%m%d%H%M%S")))

        # Return the archive path if successful
        return ("versions/web_static_{}.tgz".format(datetime.
                                                    strftime("%Y%m%d%H%M%S")))
    except:
        return None
