from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy, reverse

from .models import FoodUser
from .decorators import login_required, annon_required
from .helper import *


def food(request):
    if request.method == "POST":
        food_name = request.POST.get('food')
        food_meal_time = request.POST.get('meal_time')
        crawl_food(food_name, food_meal_time)
        return HttpResponse("ВЗЕХМЕ ХРАНАТА!")
    return render(request, 'food.html', {})


@annon_required(redirect_url=reverse_lazy('profile'))
def home(request):
    return render(request, 'home.html', {})


@login_required(redirect_url=reverse_lazy('home'))
def profile(request):
    email = request.session['food_email']
    user = FoodUser.objects.get(email=email)

    name, _, _, gender, years, weight, height, BMI, max_cal = get_cls_get_attr(FoodUser, request)

    if request.method == 'POST':
        name, _, _, gender, years, weight, height = get_user_post_attr(request)

        BMI = int(weight) / ((int(height) / 100)**2)
        calc_cal = max_calories(int(height), int(weight), int(years), gender)
        new_password = request.POST.get('new_password')

        new_food_user = FoodUser.objects.filter(name=name)\
                                        .update(password=new_password,
                                                years=years,
                                                weight=weight,
                                                height=height,
                                                BMI=BMI,
                                                max_cal=calc_cal)

        return render(request, 'profile.html', locals())
    return render(request, 'profile.html', locals())


def registration(request):
    if request.method == 'POST':
        name, email, password, gender, years, weight, height =\
            get_user_post_attr(request)

        if not FoodUser.exists(email):
            calc_BMI = int(weight) / ((int(height) / 100)**2)
            print(calculate_normal_BMI(int(years), calc_BMI))
            calc_cal = max_calories(int(height), int(weight), int(years), gender)
            u = FoodUser(
                name=name,
                email=email,
                password=password,
                gender=gender,
                years=years,
                weight=weight,
                height=height,
                BMI=calc_BMI,
                max_cal=calc_cal
            )
            u.save()

        else:
            error = "User already exists"
        return redirect(reverse('profile'))
    return render(request, 'register.html', locals())


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        u = FoodUser.login_user(email, password)

        if u is None:
            error = 'Wrong username or password'
        else:
            request.session['food_email'] = email
            return redirect(reverse('profile'))
    return HttpResponse(error)


def logout(request):
    request.session.flush()
    return redirect(reverse('home'))
