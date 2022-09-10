from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, AddCategoryForm, AddCardForm
from .models import Category
from .services.categories import get_categories_by_user
from .services.cards import get_card_to_learn, remember_card
from .exceptions import IncorrectRememberTypeError


def login_view(request):
    if request.user.is_authenticated:
        return reverse(redirect('app:dashboard'))

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            username = data.get('username')
            password = data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('app:dashboard'))
                else:
                    form.invalid_login_error()
            else:
                form.invalid_login_error()
    else:
        form = LoginForm()

    return render(request, 'app/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return reverse(redirect('app:dashboard'))

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('app:login'))
    else:
        form = UserCreationForm()

    return render(request, 'app/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(reverse('app:login'))


@login_required
def dashboard_view(request):
    categories = get_categories_by_user(request.user)
    return render(request, 'app/dashboard.html', {'categories': categories})


@login_required
def learn_card_view(request, category_id):
    if request.method == 'POST':
        card_id = request.POST['card_id']
        remember_type = request.POST['remember_type']

        try:
            remember_card(card_id, remember_type)
        except IncorrectRememberTypeError:
            return HttpResponse('Something went wrong.', status=500)

        return HttpResponseRedirect(request.path_info)

    card_to_learn = get_card_to_learn(category_id)
    return render(request, 'app/learn.html', {'card': card_to_learn})


@login_required
def single_category_view(request, category_id):
    categories = get_categories_by_user(request.user, category_id)
    return render(request, 'app/single_category.html', {'categories': categories, 'parent_id': category_id})


@login_required
def add_new_card_view(request):
    if request.method == 'POST':
        form = AddCardForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            card = form.save(commit=False)

            card.user = request.user
            card.save()

            return redirect(reverse('app:dashboard'))
    else:
        form = AddCardForm(request.user)

    return render(request, 'app/add_card.html', {'form': form})


@login_required
def add_new_category_view(request):
    if request.method == 'POST':
        form = AddCategoryForm(request.user, request.POST)
        if form.is_valid():
            category = form.save(commit=False)

            category.user = request.user
            category.save()

            return redirect(reverse('app:dashboard'))
    else:
        form = AddCategoryForm(request.user)

    return render(request, 'app/add_category.html', {'form': form})


@login_required
def delete_category_view(request, category_id):
    category = Category.objects.get(id=category_id)

    if request.method == 'POST':
        category.delete()
        return redirect(reverse('app:dashboard'))

    return render(request, 'app/delete_category.html', {'category': category})
