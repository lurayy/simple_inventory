from .models_permission import CustomPermission
from rest_framework import serializers
from .models import Profile, UserActivities, Setting, Notification, NotificationSetting, UserActivities, ActivityLog, Country


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


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'



class UserActivitiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserActivities
        fields = '__all__'

class NotificationSettingSerializer(serializers.ModelSerializer):

    class Meta:
        model = NotificationSetting
        fields = '__all__'



class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'


class ActivityLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActivityLog
        fields = '__all__'