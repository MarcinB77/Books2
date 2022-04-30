from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from .forms import SearchForm, AddBookForm
from .models import Book

import requests

from .serializers import BookSerializer

from decouple import config

API_KEY = config('API_KEY')


# Create your views here.
class BookListView(ListView):
    model = Book
    queryset = Book.objects.order_by('title')
    context_object_name = 'book_list'


class BookDetailView(DetailView):
    model = Book


class AddBook(LoginRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('book_list:list')


class BookEditView(LoginRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('book_list:list')


class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('book_list:list')


def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            title = form.data.get('title')
            author = form.data.get('author')
            isbn = form.data.get('isbn')

            terms_l = [title, author, isbn]
            terms = {f"{item}": item for item in terms_l if len(item) > 1}

            url = f'https://www.googleapis.com/books/v1/volumes?q={terms}&key={API_KEY}'

            response = requests.get(url)
            results = response.json()

            return render(request, 'book_list/search.html', context={'form': form, 'results': results})
    else:
        form = SearchForm()
    return render(request, 'book_list/search.html', context={'form': form})


@login_required
def add_from_google(request, isbn):
    """ do poprawki """

    url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={API_KEY}'
    response = requests.get(url)
    result = response.json()
    try:
        authors = str(result['items'][0]['volumeInfo']['authors'])
        author = authors.replace('[', '').replace(']', '').replace("'", "")
    except KeyError:
        author = ""
    try:
        pub_date_x = result['items'][0]['volumeInfo']['publishedDate']
        pub_date = int(pub_date_x.split("-")[0])
    except KeyError:
        pub_date = ""
    try:
        pages = int(result['items'][0]['volumeInfo']['pageCount'])
    except KeyError:
        pages = ""
    try:
        cover_link = result['items'][0]['volumeInfo']['imageLinks']['smallThumbnail']
    except KeyError:
        cover_link = ""
    try:
        language = result['items'][0]['volumeInfo']['language']
    except KeyError:
        language = ""
    try:
        title = result['items'][0]['volumeInfo']['title']
    except KeyError:
        title = ""
    data = {'title': title,
            'author': author,
            'pub_date': pub_date,
            'isbn': isbn,
            'pages': pages,
            'cover_link': cover_link,
            'language': language,
            }

    form = AddBookForm(data)
    if form.is_valid():
        form.save()
        return redirect('book_list:list')
    return render(request, 'book_list/book_form.html', context={'form': form})


# API Views section

class BookFilter(filters.FilterSet):
    class Meta:
        model = Book
        fields = {
            'title': ['icontains'],
            'author': ['icontains'],
            'isbn': ['exact'],
            'pub_date': ['gte', 'lte'],
            'pages': ['gte', 'lte'],
            'language': ['icontains']
        }


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_class = BookFilter

    @action(methods=['GET'], detail=False)
    def newest(self):
        newest = self.get_queryset().order_by('id').last()
        serializer = self.get_serializer_class()(newest)
        return Response(serializer.data)


@api_view(['GET'])
def api_overview():
    api_urls = {
        'List': '/book-list',
        'Detail View': '/book-detail/<int:pk>',
        'Create': '/book-create',
        'Update': '/book-update/<int:pk>',
        'Delete': '/book-delete/<int:pk>'
    }
    return Response(api_urls)


@api_view(['GET'])
def book_detail(pk):
    book = Book.objects.get(id=pk)
    serializer = BookSerializer(book, many=False)

    return Response(serializer.data)


@api_view(['POST'])
def book_create(request):
    serializer = BookSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST', 'GET'])
def book_update(request, pk):
    book = Book.objects.get(id=pk)
    serializer = BookSerializer(instance=book, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE', 'GET'])
def book_delete(pk):
    book = Book.objects.get(id=pk)
    book.delete()

    return Response('Item successfully deleted.')
