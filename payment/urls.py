from django.urls import path
from . import views

urlpatterns = [
    path('giftcards/get', views.get_multiple_gift_cards, name='handle multiple gift cards get and add'),
    path('giftcard/get', views.get_gift_card_details, name='handle single gift card get and edit'),
    path('giftcards/delete', views.delete_gift_cards, name='handle multiple gift cards delete'),
    path('giftcard/validate', views.validate_gift_card, name='handle multiple gift cards delete'),
    path('giftcard/uniquecard/delete', views.delete_unique_cards, name='delete unique cards'),
    path('giftcard/update', views.update_gift_card, name="update gift card"),

    path('payment/methods/get', views.get_payment_methods, name='Payment methods'),    
    path('payment/do',views.apply_payment, name='apply payment')
]