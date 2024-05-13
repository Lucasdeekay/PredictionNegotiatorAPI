# views.py
import json
import requests

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import pandas as pd
import joblib

from MyApp.models import Product
from MyApp.serializers import ProductSerializer



def login_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            password = data.get('password')

            if User.objects.filter(**{"email": email}).exists():
                username = User.objects.get(email=email).username
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return JsonResponse({'success': 'Login successful', 'username': user.username}, status=200, safe=False)
                else:
                    return JsonResponse({'error': 'Invalid credentials'}, status=401, safe=False)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401, safe=False)
        except Exception as e:
            return JsonResponse({'error': f'Internal server error: {str(e)}'}, status=500, safe=False)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405, safe=False)



def register_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username').strip()
            email = data.get('email').strip()
            password = data.get('password').strip()
            if User.objects.filter(**{"username": username, "email": email}).exists():
                return JsonResponse({'error': "User already exists"}, status=400, safe=False)
            else:
                User.objects.create_user(username=username, password=password, email=email)
                return JsonResponse({'success': "Registration successful"}, status=200, safe=False)
        except Exception as e:
            return JsonResponse({'error': f'Internal server error: {str(e)}'}, status=500, safe=False)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405, safe=False)


def forgot_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email').strip()

            if User.objects.filter(**{"email": email}).exists():
                user = User.objects.get(email=email)
                data = {
                    'user_id': user.id,
                    'success': "Proceed to change password",
                }
                return JsonResponse(data, status=200, safe=False)
            else:
                data = {
                    'error': "User does not exist",
                }
                # Redirect to dashboard page
                return JsonResponse(data, status=400, safe=False)
        except Exception as e:
            return JsonResponse({'error': f'Internal server error: {str(e)}'}, status=500, safe=False)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405, safe=False)



def retrieve_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            user_id = data.get('user_id').strip()
            user = User.objects.get(id=int(user_id))
            password = data.get('password').strip()
            user.set_password(password)
            user.save()
            data = {
                'success': "Password change successful",
            }
            # Redirect to dashboard page
            return JsonResponse(data, status=status.HTTP_200_OK, safe=False)
        except Exception as e:
            return JsonResponse({'error': f'Internal server error: {str(e)}'}, status=500, safe=False)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405, safe=False)


def logout_user(request):
    # logout user
    logout(request)
    # redirect to login page
    return JsonResponse({}, status=status.HTTP_200_OK, safe=False)



def dashboard(request):
    products = Product.objects.all()
    products_serializer = ProductSerializer(products, many=True)
    data = {
        'username': request.user.username,
        'products': products_serializer.data,
    }
    # Redirect to dashboard page
    return JsonResponse(data, status=status.HTTP_200_OK, safe=False)



def details(request):
    if request.method == 'POST':

        model_url = "static/price_predictor_pipeline.joblib"

        try:
            data = json.loads(request.body.decode('utf-8'))
            product_id = data.get('product_id').strip()

            product = Product.objects.get(id=int(product_id))
            product_serializer = ProductSerializer(product)

            model = joblib.load(model_url)

            data = pd.DataFrame({
                'discounted_price': [product.discounted_price],
                'discount_percentage': [product.discount_percentage],
                'rating': [product.rating],
                'rating_count': [product.rating_count]
            })

            predicted_price = model.predict(data)

            data = {
                'product': product_serializer.data,
                'predicted_price': predicted_price[0][0],
            }
            # Redirect to dashboard page
            return JsonResponse(data, status=status.HTTP_200_OK, safe=False)
        except Exception as e:
            return JsonResponse({'error': f'Internal server error: {str(e)}'}, status=500, safe=False)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405, safe=False)
