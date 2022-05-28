from django.urls import path

from daraja.views import InitiateSTKPush, STKPushCallback, TransactionView, InitiateSTKPushSavings, STKPushCallbackSavings, TransactionViewSavings

urlpatterns = [
    path('mpesa/', InitiateSTKPush.as_view(), name='initiate_stk_push'),
    path('mpesa/callback/', STKPushCallback.as_view(), name='stk_push_callback'),
    path('mpesa/status/<id>/', TransactionView.as_view(), name='transactions'),
    path('mpesa/savings/', InitiateSTKPushSavings.as_view(), name='initiate_stk_push_savings'),
    path('mpesa/savings/callback/', STKPushCallbackSavings.as_view(), name='stk_push_callback_savings'),
    path('mpesa/savings/status/<id>/', TransactionViewSavings.as_view(), name='transactions_savings'),
]
