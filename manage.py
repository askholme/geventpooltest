#!/usr/bin/env python
import os
import sys
from gevent import monkey#; monkey.patch_all()
monkey.patch_os()
monkey.patch_time()
monkey.patch_thread( _threading_local=False)
monkey.patch_sys()
monkey.patch_socket()
monkey.patch_select()
monkey.patch_ssl()
monkey.patch_subprocess()

from psycogreen.gevent import patch_psycopg; patch_psycopg();

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "geventpooltest.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
