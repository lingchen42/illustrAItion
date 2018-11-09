from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
#    path('', views.DrawingList.as_view()),
    path(r'<sentence>/', views.DetailDrawing),
]

urlpatterns = format_suffix_patterns(urlpatterns)