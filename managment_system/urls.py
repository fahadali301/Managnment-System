from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView, RedirectView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from managment_system.views import DashboardView

schema_view = get_schema_view(
   openapi.Info(
      title="Your API",
      default_version='v1',
      description="API documentation for your project",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

def realtime_list(page_title, resource, endpoint, form_url):
    return TemplateView.as_view(
        template_name='realtime/list.html',
        extra_context={
            'page_title': page_title,
            'page_name': f"{resource}-list",
            'resource': resource,
            'endpoint': endpoint,
            'form_url': form_url,
            'item_label': page_title[:-1] if page_title.endswith('s') else page_title,
        },
    )


def realtime_form(item_label, resource, endpoint, list_url):
    return TemplateView.as_view(
        template_name='realtime/form.html',
        extra_context={
            'item_label': item_label,
            'page_name': f"{resource}-form",
            'resource': resource,
            'endpoint': endpoint,
            'list_url': list_url,
        },
    )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(('company.urls', 'company'), namespace='company')),

    # Versioned API namespace for university backend
    path('api/v1/auth/', include(('company.urls', 'auth'), namespace='auth-v1')),
    path('api/v1/academics/', include(('academics.urls', 'academics'), namespace='academics-v1')),
    path('api/v1/students/', include(('students.urls', 'students'), namespace='students-v1')),

    # Swagger/OpenAPI docs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Frontend page views
    path('', RedirectView.as_view(url='/login/', permanent=False), name='home'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='register.html'), name='register'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('students/', TemplateView.as_view(template_name='students.html'), name='students'),
    path('enrollments/', TemplateView.as_view(template_name='enrollments.html'), name='enrollments'),
    path('programs/', TemplateView.as_view(template_name='programs.html'), name='programs'),

    path('companies/', realtime_list('Companies', 'companies', '/api/companies/', '/companies/new/'), name='companies-list'),
    path('companies/new/', realtime_form('Company', 'companies', '/api/companies/', '/companies/'), name='companies-form'),

    path('branches/', realtime_list('Branches', 'branches', '/api/branches/', '/branches/new/'), name='branches-list'),
    path('branches/new/', realtime_form('Branch', 'branches', '/api/branches/', '/branches/'), name='branches-form'),

    path('buildings/', realtime_list('Buildings', 'buildings', '/api/buildings/', '/buildings/new/'), name='buildings-list'),
    path('buildings/new/', realtime_form('Building', 'buildings', '/api/buildings/', '/buildings/'), name='buildings-form'),

    path('floors/', realtime_list('Floors', 'floors', '/api/floors/', '/floors/new/'), name='floors-list'),
    path('floors/new/', realtime_form('Floor', 'floors', '/api/floors/', '/floors/'), name='floors-form'),

    path('rooms/', realtime_list('Rooms', 'rooms', '/api/rooms/', '/rooms/new/'), name='rooms-list'),
    path('rooms/new/', realtime_form('Room', 'rooms', '/api/rooms/', '/rooms/'), name='rooms-form'),

    path('assets/', realtime_list('Assets', 'assets', '/api/assets/', '/assets/new/'), name='assets-list'),
    path('assets/new/', realtime_form('Asset', 'assets', '/api/assets/', '/assets/'), name='assets-form'),

    path('roles/', realtime_list('Roles', 'roles', '/api/roles/', '/roles/new/'), name='roles-list'),
    path('roles/new/', realtime_form('Role', 'roles', '/api/roles/', '/roles/'), name='roles-form'),

    path('users/', realtime_list('Users', 'users', '/api/users/', '/users/new/'), name='users-list'),
    path('users/new/', realtime_form('User', 'users', '/api/users/', '/users/'), name='users-form'),

    path('employees/', realtime_list('Employees', 'employees', '/api/employees/', '/employees/'), name='employees-list'),
]
