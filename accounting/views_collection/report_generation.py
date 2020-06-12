# from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
# from django.http import JsonResponse
# from django.views.decorators.http import require_http_methods
# from user_handler.permission_check import bind, check_permission
# import json
# from inventory.utils import  str_to_datetime
# from django.core.exceptions import ObjectDoesNotExist
# from django.db import IntegrityError
# from accounting.models import EntryType, AccountType, Account, LedgerEntry, MonthlyStats
# from accounting.utils import accounts_to_json, entry_types_to_json, accounts_types_to_json, ledger_entries_to_json



# @require_http_methods(['POST'])
# @bind
# def generate_profit_loss_statement(self, request):
#     response_json = {'status':False}
#     if check_permission(self.__name__, request.headers['Authorization'].split(' ')[1]):
#         try:
#             json_str = request.body.decode(encoding='UTF-8')
#             data_json = json.loads(json_str)
#             if data_json['action'] == "get":
                