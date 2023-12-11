from django.urls import path
from . import views

app_name = "profile"

urlpatterns = [
    # My Profile
    path("me/", views.MyProfileDetailView.as_view(), name="me"),
    # Applied vacancies
    path("my-vacancies/", views.show_my_vacancies, name="show_my_vacancies"),
    # Other people's profile
    path("<uuid:user_id>/", views.ProfileDetailView.as_view(), name="profile"),
    # Create review
    path(
        "<uuid:profile_id>/review/create/", views.review_profile, name="review_profile"
    ),
    # My applications
    path("my-applications/", views.show_my_applications, name="show_my_applications"),
    # Delete application
    path(
        "my-applications/<uuid:application_id>/delete",
        views.delete_application,
        name="delete_application",
    ),
    # Delete review
    path(
        "<uuid:profile_id>/review/<uuid:review_id>/delete",
        views.delete_profile_review,
        name="delete_profile_review",
    ),
    # Update Review
    path(
        "<uuid:profile_id>/review/<uuid:review_id>/update",
        views.update_profile_review,
        name="update_profile_review",
    ),
    path("<uuid:profile_id>/update", views.update_profile, name="update_profile"),
]
