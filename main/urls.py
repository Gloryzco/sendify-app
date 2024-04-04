from django.urls import path, include
from . import views


urlpatterns = [
    path('profiles/', views.ProfileView.as_view()),
    path('profiles/<int:id>', views.ProfileDetailView.as_view()),
    path('events/', views.EventPreferenceView.as_view()),
    path('events/<int:id>', views.EventPreferenceDetailView.as_view()),
    path('subscriptions/', views.SubscriptionListView.as_view()),
    path('subscriptions/<int:id>', views.SubscriptionDetailView.as_view()),
    path('subscriptions/check/', views.check_subscription),
    path('subscriptions/new/', views.subscribe),
    path('receive-sms/', views.receive_sms),
    path('receive-twilio-sms/', views.receive_twilio_sms),
    
]
