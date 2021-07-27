from django.urls import path
from . import views

app_name = 'news'
urlpatterns = [
    path('', views.home, name='home_page'),
    # path('category/<str:category_slug>/', views.home, name='news_category'),
    path('category_tab/<str:category_slug>/', views.show_category_tab, name='show_category_tab'),
    path('post_detail/<str:post_slug>/', views.post_detail, name='news_post_detail'),
    path('search/', views.search_post, name='news_search'),
    path('tags/<str:tag_slug>/', views.display_taged_post, name='post_by_tag'),


    path('login/', views.login, name='login'),
]