from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    CompanyListCreateView, CompanyDetailView,
    BranchListCreateView, BranchDetailView,
    BuildingListCreateView, BuildingDetailView,
    FloorListCreateView, FloorDetailView,
    RoomListCreateView, RoomDetailView,
    AssetListCreateView, AssetDetailView,
    UserListCreateView, UserDetailView,
    RoleListCreateView, RoleDetailView,
    PermissionListCreateView, PermissionDetailView
)

urlpatterns = [

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # refresh token

    # Company URLs
    path('companies/', CompanyListCreateView.as_view(), name='company-list-create'),
    path('companies/<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),

    # Branch URLs
    path('branches/', BranchListCreateView.as_view(), name='branch-list-create'),
    path('branches/<int:pk>/', BranchDetailView.as_view(), name='branch-detail'),

    # Building URLs
    path('buildings/', BuildingListCreateView.as_view(), name='building-list-create'),
    path('buildings/<int:pk>/', BuildingDetailView.as_view(), name='building-detail'),

    # Floor URLs
    path('floors/', FloorListCreateView.as_view(), name='floor-list-create'),
    path('floors/<int:pk>/', FloorDetailView.as_view(), name='floor-detail'),

    # Room URLs
    path('rooms/', RoomListCreateView.as_view(), name='room-list-create'),
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),

    # Asset URLs
    path('assets/', AssetListCreateView.as_view(), name='asset-list-create'),
    path('assets/<int:pk>/', AssetDetailView.as_view(), name='asset-detail'),

    # User URLs
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

    # Role URLs
    path('roles/', RoleListCreateView.as_view(), name='role-list-create'),
    path('roles/<int:pk>/', RoleDetailView.as_view(), name='role-detail'),

    # Permission URLs
    path('permissions/', PermissionListCreateView.as_view(), name='permission-list-create'),
    path('permissions/<int:pk>/', PermissionDetailView.as_view(), name='permission-detail'),
]
