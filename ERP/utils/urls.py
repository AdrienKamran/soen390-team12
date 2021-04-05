from django.urls import path

from utils.views import SubscriptionCreateView, SubscriptionDeleteView

urlpatterns = [
    path('add',
         SubscriptionCreateView.as_view(),
         name='subscriptions_create'),
    path('delete',
         SubscriptionDeleteView.as_view(),
         name='subscriptions_delete')
]
