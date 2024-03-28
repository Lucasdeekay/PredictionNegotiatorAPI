# views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import joblib

from MyApp.models import Product
from MyApp.serializers import ProductSerializer


def login_user(request):
    #  Check if the form is valid
    if request.method == "POST":
        # Process the input
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()
        # Authenticate the user login details
        user = authenticate(request, email=email, password=password)
        # Check if user exists
        if user is not None:
            # Log in the user
            login(request, user)
            data = {
                'success': "Login sucessful",
            }
            # Redirect to dashboard page
            return Response(data, status=status.HTTP_200_OK)
        # If user does not exist
        else:
            data = {
                'error': "Invalid login credentials",
            }
            # Redirect back to the login page
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


def register_user(request):
    #  Check if the form is valid
    if request.method == "POST":
        # Process the input
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()
        if User.objects.filter(**{"username": username, "email": email}).exists():
            data = {
                'error': "User already exists",
            }
            # Redirect back to the login page
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            User.objects.create_user(username=username, password=password, email=email)
            data = {
                'success': "Registration successful",
            }
            # Redirect to dashboard page
            return Response(data, status=status.HTTP_200_OK)


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email').strip()

        if User.objects.filter(**{"email": email}).exists():
            user = User.objects.get(email=email)
            data = {
                'user_id': user.id,
                'success': "Proceed to change password",
            }
            # Redirect back to the login page
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                'error': "User does not exist",
            }
            # Redirect to dashboard page
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


def retrieve_password(request):
    #  Check if the form is valid
    if request.method == "POST":
        # Process the input
        user_id = request.POST.get('user_id').strip()
        user = User.objects.get(id=int(user_id))
        password = request.POST.get('password').strip()
        user.set_password(password)
        user.save()
        data = {
            'success': "Password change successful",
        }
        # Redirect to dashboard page
        return Response(data, status=status.HTTP_200_OK)


def logout_user(request):
    # logout user
    logout(request)
    # redirect to login page
    return Response({}, status=status.HTTP_200_OK)


def profile(request):
    data = {
        'username': request.user.username,
    }
    # Redirect to dashboard page
    return Response(data, status=status.HTTP_200_OK)


def dashboard(request):
    products = Product.objects.all()
    products_serializer = ProductSerializer(products, many=True)
    data = {
        'username': request.user.username,
        'products': products_serializer.data,
    }
    # Redirect to dashboard page
    return Response(data, status=status.HTTP_200_OK)


def details(request, product_id):
    product = Product.objects.get(id=int(product_id))

    scaler = MinMaxScaler()
    loaded_model = joblib.load('price_predictor.joblib')
    data = pd.DataFrame({
        'discounted_price': [100.0],
        'discount_percentage': [20.0],
        'rating': [4.5],
        'rating_count': [1000]
    })

    data_scaled = scaler.transform(data)
    predicted_price = loaded_model.predict(data_scaled)

    product_serializer = ProductSerializer(product)
    data = {
        'product': product_serializer.data,
        'predicted_price': predicted_price[0][0],
    }
    # Redirect to dashboard page
    return Response(data, status=status.HTTP_200_OK)