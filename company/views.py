from rest_framework import generics
from rest_framework.permissions import (AllowAny)

from .models import (
    Company, Branch, Building, Floor, Room, Asset,
    User, Role, Permissions
)
from .serializer import (
    CompanySerializer, BranchSerializer, BuildingSerializer,
    FloorSerializer, RoomSerializer, AssetSerializer,
    UserSerializer, RoleSerializer, PermissionSerializer
)
from .permission import HasPermission


class ListCreateView(generics.ListCreateAPIView):
    permission_classes = [HasPermission]


class RetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [HasPermission]


class CompanyListCreateView(ListCreateView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [HasPermission]


class CompanyDetailView(RetrieveUpdateDestroyView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [HasPermission]


class BranchListCreateView(ListCreateView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [HasPermission]


class BranchDetailView(RetrieveUpdateDestroyView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [HasPermission]


class BuildingListCreateView(ListCreateView):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = [HasPermission]


class BuildingDetailView(RetrieveUpdateDestroyView):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = [HasPermission]


class FloorListCreateView(ListCreateView):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer
    permission_classes = [HasPermission]


class FloorDetailView(RetrieveUpdateDestroyView):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer
    permission_classes = [HasPermission]


class RoomListCreateView(ListCreateView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [HasPermission]


class RoomDetailView(RetrieveUpdateDestroyView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [HasPermission]


class AssetListCreateView(ListCreateView):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [HasPermission]


class AssetDetailView(RetrieveUpdateDestroyView):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [HasPermission]


class UserListCreateView(ListCreateView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [HasPermission]


class UserDetailView(RetrieveUpdateDestroyView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [HasPermission]


class RoleListCreateView(ListCreateView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [HasPermission]


class RoleDetailView(RetrieveUpdateDestroyView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [HasPermission]


class PermissionListCreateView(ListCreateView):
    queryset = Permissions.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [AllowAny]


class PermissionDetailView(RetrieveUpdateDestroyView):
    queryset = Permissions.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [HasPermission]
