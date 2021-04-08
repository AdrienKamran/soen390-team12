from django.urls import path

from notifications.views import SubscriptionCreateView, SubscriptionDeleteView

urlpatterns = [
    path('add', SubscriptionCreateView.as_view(), name='subscriptions_create'), #An endpoint to create a subscription
    path('delete', SubscriptionDeleteView.as_view(), name='subscriptions_delete') #An endpoint to delete a subscription
]
