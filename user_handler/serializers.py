from .models_permission import CustomPermission
from rest_framework import serializers

class CustomPermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomPermission
        fields = '__all__'