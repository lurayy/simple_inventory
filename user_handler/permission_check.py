from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from .serializers import CustomPermissionSerializer 

def bind(f):
    return f.__get__(f, type(f))

def check_permission(f_name, token):
    try:
        valid_data = VerifyJSONWebTokenSerializer().validate({'token':token})
        user = valid_data['user']
        permissions = CustomPermissionSerializer(user.role).data
        if permissions[f_name]:
            return {'status':True}
        else:
            return False
    except Exception as exp:
        return ({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
