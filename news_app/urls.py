from django.urls import path
from news_app import views as news_views

urlpatterns = [
    path("", news_views.HomePageView.as_view(), name="home-page"),
    # path("contact/", news_views.contact_page, name="contact"),
    # path("contact/success/", news_views.success_page, name="success"),
    path('search/', news_views.search_view, name='search-view')
]
