''' Searializers module for models of api '''
from rest_framework import serializers
from .models import EntryType, AccountType, Account, LedgerEntry, MonthlyStats
from user_handler.models import Vendor

class EntryTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = EntryType
        fields= '__all__'


class AccountTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountType
        fields= '__all__'

class AccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Account
        fields= '__all__'

class LedgerEntrySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LedgerEntry
        fields= '__all__'

class MonthlyStatsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MonthlyStats
        fields= '__all__'
