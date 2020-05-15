from django.urls import URLResolver, URLPattern
from django.conf import settings
from django.urls import resolve
from simple_im.urls import urlpatterns
from django.urls import get_resolver


x = get_resolver().reverse_dict.keys()

function_names = []
black_list = ['serve','ObtainJSONWebToken', 'RefreshJSONWebToken', 'csrf']

for (i, res) in enumerate(x):
    if (type(res).__name__ == "function"):
        if not black_list.__contains__(res.__name__):
            function_names.append(res.__name__)

print(function_names)

with open('user_handler/models_permission.py','w') as out_to:
    out_to.write('from django.db import models\n')
    out_to.write('\n')
    out_to.write('class CustomPermission(models.Model):\n')
    out_to.write('    name = models.CharField(max_length=255)\n')
    for name in function_names:
        out_to.write('    '+name+' = models.BooleanField(default=True)\n')
    out_to.write('    def __str__(self):\n')
    out_to.write('        return f"{self.name}"\n')
    

