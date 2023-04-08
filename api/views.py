from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import status

from .models import Product, Cart, Order
from .serializers import ProductSerializer, CartSerializer, OrderSerializer


@api_view(['GET', 'POST'])
@permission_classes((AllowAny, ))
def get_create_products(request):
    if request.method == 'POST':
        if request.user.is_superuser is True:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    elif request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', "PATCH", "DELETE"])
@permission_classes((IsAdminUser, ))
def get_edit_delete_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = ProductSerializer(product, instance=product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PATCH'])
@permission_classes((IsAuthenticated, ))
def get_edit_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)

    if request.method == 'GET':
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = CartSerializer(cart, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def create_order(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    order = Order()

    for product in cart.products.all():
        order.products.add(product)

    order.save()
    cart.products.clear()

    serializer = OrderSerializer(order)
    return Response(serializer.data)


