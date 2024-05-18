from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status

import pandas as pd
import joblib
from rest_framework.decorators import api_view
from rest_framework.response import Response

from MyApp.models import Product
from MyApp.serializers import ProductSerializer


@api_view(["POST"])
def login_user(request):
    if request.method == 'POST':
        try:
            email = request.data.get('email').strip()
            password = request.data.get('password')

            if User.objects.filter(**{"email": email}).exists():
                username = User.objects.get(email=email).username
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return Response({'success': 'Login successful', 'username': user.username}, status=200)
                else:
                    return Response({'error': 'Invalid credentials'}, status=401)
            else:
                return Response({'error': 'Invalid credentials'}, status=401)
        except Exception as e:
            return Response({'error': f'Internal server error: {str(e)}'}, status=500)

    else:
        return Response({'error': 'Method not allowed'}, status=405)


@api_view(["POST"])
def register_user(request):
    if request.method == 'POST':
        try:
            username = request.data.get('username').strip()
            email = request.data.get('email').strip()
            password = request.data.get('password')
            if User.objects.filter(**{"username": username, "email": email}).exists():
                return Response({'error': "User already exists"}, status=400)
            else:
                User.objects.create_user(username=username, password=password, email=email)
                return Response({'success': "Registration successful"}, status=200)
        except Exception as e:
            return Response({'error': f'Internal server error: {str(e)}'}, status=500)

    else:
        return Response({'error': 'Method not allowed'}, status=405)


@api_view(["POST"])
def forgot_password(request):
    if request.method == 'POST':
        try:
            email = request.data.get('email').strip()

            if User.objects.filter(**{"email": email}).exists():
                user = User.objects.get(email=email)
                data = {
                    'user_id': user.id,
                    'success': "Proceed to change password",
                }
                return Response(data, status=200)
            else:
                data = {
                    'error': "User does not exist",
                }
                # Redirect to dashboard page
                return Response(data, status=400)
        except Exception as e:
            return Response({'error': f'Internal server error: {str(e)}'}, status=500)

    else:
        return Response({'error': 'Method not allowed'}, status=405)


@api_view(["POST"])
def retrieve_password(request):
    if request.method == 'POST':
        try:
            user_id = request.data.get('user_id').strip()
            user = User.objects.get(id=int(user_id))
            password = request.data.get('password').strip()
            user.set_password(password)
            user.save()
            data = {
                'success': "Password change successful",
            }
            # Redirect to dashboard page
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Internal server error: {str(e)}'}, status=500)

    else:
        return Response({'error': 'Method not allowed'}, status=405)


@api_view(["POST"])
def logout_user(request):
    # logout user
    logout(request)
    # redirect to login page
    return Response({}, status=status.HTTP_200_OK)


@api_view(["GET"])
def dashboard(request):
    products = Product.objects.all()
    products_serializer = ProductSerializer(products, many=True)
    data = {
        'username': request.user.username,
        'products': products_serializer.data,
    }
    # Redirect to dashboard page
    return Response(data, status=status.HTTP_200_OK)


@api_view(["GET"])
def details(request, product_id):
    if request.method == 'GET':

        model_url = "static/price_predictor_pipeline.joblib"

        try:
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
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Internal server error: {str(e)}'}, status=500)

    else:
        return Response({'error': 'Method not allowed'}, status=405)
