from django.urls import path
from . import views

urlpatterns = [
    path('giftcards', views.gift_cards, name='handle multiple gift cards get and add'),
    path('giftcard', views.gift_card, name='handle single gift card get and edit'),
    path('giftcards/delete', views.delete_gift_cards, name='handle multiple gift cards delete'),
    path('giftcard/validate', views.validate_gift_card, name='handle multiple gift cards delete'),
    path('methods', views.payment_methods, name='Payment methods'),    
    path('do',views.apply_payment, name='apply payment')
]