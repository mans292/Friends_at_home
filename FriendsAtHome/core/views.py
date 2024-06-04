from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Products, Order, User, Cart, CartItem
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
import requests
from django.http import JsonResponse
import base64
from django.views.decorators.csrf import csrf_exempt
import hashlib
import secrets



def home(request):
    products = Products.objects.all()
    context = {'products':products}

    return render(request, 'core/home.html', context)

def product_info(request, pk):
    product = Products.objects.get(id=pk)
    return render(request, 'core/product_info.html', {'product':product})

def policies(request):
    return render(request, 'core/policies.html')

def villkor(request):
    return render(request, 'core/villkor.html')

def care(request):
    return render(request, 'core/care.html')

def remove_from_cart(request, pk):
    sid = request.session.session_key
    cart, created = Cart.objects.get_or_create(session_id=sid)
    product = Products.objects.get(id=pk)
    cart.remove_from_cart(product)

    return redirect('create_order')

def add_quantity(request, pk):
    sid = request.session.session_key
    cart, created = Cart.objects.get_or_create(session_id=sid)
    product = Products.objects.get(id=pk)
    cart.add_quantity(product)

    return redirect('create_order')

def decrease_quantity(request, pk):
    sid = request.session.session_key
    cart, created = Cart.objects.get_or_create(session_id=sid)
    product = Products.objects.get(id=pk)
    cart.decrease_quantity(product)

    return redirect('create_order')

def add_to_cart(request, pk):
    sid = request.session.session_key

    if not sid:
        request.session.save()
        sid = request.session.session_key

    product = Products.objects.get(id=pk)
    cart, created = Cart.objects.get_or_create(session_id=sid)
    cart.add_to_cart(product)
    
    return redirect('create_order')


def about(request):
    return render(request, 'core/about.html')



def create_klarna_order(request):
    username = 'PK85112_7e1a7ac12aca'
    password = 'KBIdHmtTZL3xJbpq'
    endcoded_credentials = base64.b64encode(f'{username}:{password}'.encode()).decode()
    url = 'https://api.playground.klarna.com/checkout/v3/orders'

    sid = request.session.session_key
    if not sid:
        request.session.save()
        sid = request.session.session_key

    cart, created = Cart.objects.get_or_create(session_id=sid)
    cart_items = CartItem.objects.filter(cart=cart)

    tot_price = 0
    tax = 0
    for item in cart_items:
        price = item.product.price * item.quantity
        tot_price += price
        tax += float(price) - float(price) * 0.8

    context0_1 = {'cart_items':cart_items, 'tot_price':tot_price, 'tax':f'{tax: .2f}'}

    if request.method == 'POST':
        order_amount = 0
        order_lines = []

        for item in cart_items:
            if item.product:
                product_quantity = request.POST.get(f'quantity_{item.product.name}')

                product_price = int(product_quantity) * (item.product.price * 100)

                total_tax_amount = product_price - (product_price * 10000/(12500))

                item = {
                    "type": "physical",
                    "name": item.product.name,
                    "quantity": int(product_quantity),
                    "quantity_unit": "st",
                    "unit_price": int(item.product.price * 100),
                    "tax_rate": 2500,
                    "total_amount": int(product_price),
                    "total_discount_amount": '0',
                    "total_tax_amount": int(total_tax_amount),
                    "shipping_attributes": {
                        "weight": 1000,
                        "dimensions": {
                           "height": 90,
                           "width": 200,
                           "length": 500, 
                        }
                    }
                }

                order_amount += product_price
                order_lines.append(item)
    
        order_tax_amount = order_amount - (order_amount * 10000/(12500))

        headers = {
            "content-Type": "application/json",
            "Klarna-Partner": "string",
            "Authorization": f'Basic {endcoded_credentials}'
        }

        data = {
            "purchase_country": "SE",
            "purchase_currency": "SEK",
            "locale": "sv-SE",
            "order_amount": int(order_amount),
            "order_tax_amount": int(order_tax_amount),
            "order_lines": order_lines,

            "merchant_urls": {
                "terms": "https://www.example.com/terms.html",
                "checkout": "https://0756-90-229-239-11.ngrok-free.app/checkout.php?sid={checkout.order.id}",
                "confirmation": "https://127.0.0.1:8001/thankyou.php?sid={checkout.order.id}",
                "push": "https://0756-90-229-239-11.ngrok-free.app/kco/push.php?klarna_order_id={checkout.order.id}"
            }
        }

        response = requests.post(url, data=json.dumps(data), headers=headers).json()
        context = {'html_snippet':response.get('html_snippet')}

        return render(request, 'core/render_klarna_order.html', context)
    return render(request, 'core/cart.html', context0_1)





def read_klarna_order(request):
    sid = request.GET.get('sid')
   
    url = 'https://api.playground.klarna.com/checkout/v3/orders/'+(sid)

    username = 'PK85112_7e1a7ac12aca'
    password = 'KBIdHmtTZL3xJbpq'
    endcoded_credentials = base64.b64encode(f'{username}:{password}'.encode()).decode()
    headers = {
        "content-type": "application/json",
        "Klarna-Partner": "string",
        "Authorization": f'Basic {endcoded_credentials}'
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    
    html_snippet = data.get('html_snippet')

    return render(request, 'core/confirmation.html', {'html_snippet':html_snippet})



@csrf_exempt
def push(request):

    if request.method == 'POST':
        klarna_order_id = request.GET.get('klarna_order_id')
        
        username = 'PK85112_7e1a7ac12aca'
        password = 'KBIdHmtTZL3xJbpq'
        endcoded_credentials = base64.b64encode(f'{username}:{password}'.encode()).decode()

        url = f'https://api.playground.klarna.com/ordermanagement/v1/orders/{klarna_order_id}'

        headers = {
        "content-type": "application/json",
        "Klarna-Partner": "string",
        "Authorization": f'Basic {endcoded_credentials}'
        }

        response = requests.get(url, headers=headers)
        
        data = response.json()

        order_lines = data['order_lines'][0]
        print(order_lines)
        billing_address = data['billing_address']
        print(billing_address)
        given_name = billing_address['given_name']
        total_amount = int(order_lines['total_amount'])/100
        print(total_amount)
        print(given_name)
        

        url_acknowledge = f'https://api.playground.klarna.com/ordermanagement/v1/orders/{klarna_order_id}/acknowledge'

        requests.post(url_acknowledge, headers=headers)
        return HttpResponse()
    else:
        return HttpResponse(status=405)
    







