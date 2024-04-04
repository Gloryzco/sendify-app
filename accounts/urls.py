from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', views.CustomUserViewSet, basename="user")


# def is_route_selected(url_pattern):
#     urls = [
#         "users/activation/",
#     ]

#     for u in urls:
#         match = url_pattern.resolve(u)
#         print(match)
#         if match:
#             return False
#     return True

# # Filter router URLs removing unwanted ones
# selected_user_routes = list(filter(is_route_selected, router.urls))
# Of course, instead of [] you'd have other URLs from your app here:

# print(router.urls)

urlpatterns = [
    path('auth/', include(router.urls)),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/admin/', views.AdminListCreateView().as_view()),
    path('auth/admin/<uuid:user_id>/assign-roles/', views.assign_role),
    path('auth/login/', views.user_login, name="login_view"),
    path("auth/logout/", views.logout_view, name="logout_view"),
    path('auth/otp/verify/', views.otp_verification),
    path('auth/otp/new/', views.reset_otp),
   
    path("permissions/", views.PermissionList.as_view(), name="permissions"),
    path("modules/", views.ModuleAccessList.as_view(), name="modules"),
    path("roles/", views.GroupListCreate.as_view(), name="roles"),
    path("roles/<int:id>", views.GroupDetail.as_view(), ),
    path("activity-logs/", views.activity_logs)
    
]
