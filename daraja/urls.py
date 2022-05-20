from django.urls import path

from daraja.views import InitiateSTKPush, STKPushCallback, TransactionView

urlpatterns = [
    path('mpesa/', InitiateSTKPush.as_view(), name='initiate_stk_push'),
    path('mpesa/callback/', STKPushCallback.as_view(), name='stk_push_callback'),
    path('mpesa/status/<id>/', TransactionView.as_view(), name='transactions'),
]
