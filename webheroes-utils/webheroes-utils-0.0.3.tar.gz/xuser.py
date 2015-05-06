
import sys, os, netifaces
from utils.discovery	import get_docker_ip
from .			import crud

mysql_ip		= get_docker_ip('mysql')

crud.connect(
    host		= mysql_ip,
    user		= "root",
    passwd		= "",
    db			= ""
)

def level( user_id ):
    if user_id == None:
        return None
    cursor		= crud.execute(
        """ SELECT * FROM users WHERE user_id = %s """,
        (user_id,)
    )
    user_data		= cursor.fetchone()
    return user_data.get('user_level', None)
    

def check_root( user_id=None ):
    return None if user_id is None else level(user_id) == 0

def check_user( user_id=None ):
    return None if user_id is None else level(user_id) == 2

def check_public( user_id=None ):
    return None if user_id is None else level(user_id) == 1


def is_root( lev=None ):
    return None if lev is None else int(lev) == 0

def is_user( lev=None ):
    return None if lev is None else int(lev) == 2

def is_public( lev=None ):
    return None if lev is None else int(lev) == 1
