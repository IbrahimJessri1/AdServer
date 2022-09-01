from config.db import user_collection, role_permission_collection
from . import generics as gen
from fastapi import HTTPException, status

class Authorize:
    def auth(permission, username):
        role = gen.get_one(user_collection, {"username" : username})["role"]
        role_permissions = gen.get_one(role_permission_collection, {"role" : role})
        if(role_permissions and (permission in role_permissions["permissions"])):
            return
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED") 
