from django.urls import path
from . import views

app_name = 'book_list'

urlpatterns = [
    path('', views.BookListView.as_view(), name='list'),
    path('add/', views.AddBook.as_view(), name='add'),
    path('detail/<int:pk>', views.BookDetailView.as_view(), name='detail'),
    path('edit/<int:pk>', views.BookEditView.as_view(), name='edit'),
    path('delete/<int:pk>', views.BookDeleteView.as_view(), name='delete'),
    path('search/', views.search, name='search'),
    path('add-fg/<str:isbn>', views.add_from_google, name='add_from_google'),
    path('api/', views.api_overview, name='api'),
    path('api/book-list/', views.BookViewSet.as_view({'get': 'list'}), name='book-list'),
    path('api/book-detail/<int:pk>', views.book_detail, name='book-detail'),
    path('api/book-create', views.book_create, name='book-create'),
    path('api/book-update/<int:pk>', views.book_update, name='book-update'),
    path('api/book-delete/<int:pk>', views.book_delete, name='book-delete'),
]
