from .models_permission import CustomPermission
from rest_framework import serializers
from .models import Profile, UserActivities, Setting


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'


class CustomPermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomPermission
        fields = '__all__'

class UserActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = UserActivities
        fields = '__all__'


class SettingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Setting
        exclude = ('id',)