from django.urls import path
from .views import fetch_repos, scan_repository, show_reports
from . import views

app_name = 'codereview'

urlpatterns = [
    path('repos/', fetch_repos, name='fetch-repos'),
    path('scan_repository/', scan_repository, name='scan_repository'),
    path('reports/', show_reports, name='show-reports'),
    path('reports/<int:report_id>/download/', views.download_scan_report, name='download_scan_report'),

]