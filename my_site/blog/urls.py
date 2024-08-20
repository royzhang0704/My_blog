"""
包含所有視圖的url
"""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.StartingPage.as_view(), name="starting-page"),
    path("posts", views.AllPost.as_view(), name="posts-page"),
    path("posts/<slug:slug>", views.PostDetail.as_view(), name="post-detail-page"),
    path("read-later", views.ReadLater.as_view(), name="read-later"),
    path("stock_index", views.stock_index, name="stock-index"),
    path("cash_form_page", views.cash_form_page, name="stock-cash"),
    path("stock_form_page", views.stock_form_page, name="stock-stock"),
    path('edit-cash/<int:id>/', views.cash_form_page, name='edit-cash'),
]
