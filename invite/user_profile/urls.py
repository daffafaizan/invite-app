from django.urls import path
from . import views

app_name = "profile"

urlpatterns = [
    path("me/", views.MyProfileDetailView.as_view(), name="me"),
    path("my-vacancies/", views.show_my_vacancies, name="show_my_vacancies"),
    path("<uuid:user_id>/", views.ProfileDetailView.as_view(), name="profile"),
    path(
        "<uuid:profile_id>/review/create/", views.review_profile, name="review_profile"
    ),
    path("my-applications/", views.show_my_applications, name="show_my_applications"),
    path(
        "my-applications/<uuid:application_id>/delete",
        views.delete_application,
        name="delete_application",
    ),
    path(
        "<uuid:profile_id>/review/<uuid:review_id>/delete",
        views.delete_profile_review,
        name="delete_profile_review",
    ),
    path("error/<str:message>/", views.error_page, name="error_page"),
]
