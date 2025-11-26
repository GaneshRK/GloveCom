from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem
from django.contrib.auth.signals import user_logged_in
from .forms import CartAddProductForm, OrderCreateForm
from django.urls import reverse
from django.conf import settings
import stripe
from decimal import Decimal
# stripe.api_key = settings.STRIPE_SECRET_KEY
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Cart, CartItem, Product
from .utils import get_user_cart
from django.contrib.auth.decorators import login_required

CART_SESSION_ID = 'cart'

def temp_payment(request):
    return render(request, 'shop/temp.html')


@receiver(user_logged_in)
def merge_cart(sender, user, request, **kwargs):
    session_cart = request.session.get(CART_SESSION_ID, {})
    if not session_cart:
        return

    cart = get_user_cart(user)

    for pid, qty in session_cart.items():
        try:
            product = Product.objects.get(pk=pid)
        except Product.DoesNotExist:
            continue

        item, created = cart.items.get_or_create(product=product)
        item.quantity += int(qty)
        item.save()

    # clear session cart after merging
    request.session[CART_SESSION_ID] = {}


def _cart_add(request, product_id, quantity=1):
    cart = request.session.get(CART_SESSION_ID, {})
    qty = cart.get(str(product_id), 0)
    cart[str(product_id)] = qty + int(quantity)
    request.session[CART_SESSION_ID] = cart

def _cart_remove(request, product_id):
    cart = request.session.get(CART_SESSION_ID, {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session[CART_SESSION_ID] = cart

def _get_cart_items(request):
    cart = request.session.get(CART_SESSION_ID, {})
    items = []
    total = Decimal('0.00')
    for pid, qty in cart.items():
        try:
            product = Product.objects.get(pk=pid)
        except Product.DoesNotExist:
            continue
        line_total = product.price * int(qty)
        items.append({'product': product, 'quantity': int(qty), 'line_total': line_total})
        total += line_total
    return items, total

def product_list(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'shop/product_list.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    form = CartAddProductForm()
    images = product.images.all()
    specifications = product.specifications.all()
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'form': form,
        'images': images,
        'specifications': specifications
    })
@login_required(login_url='users:login')
def cart_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    qty = int(request.POST.get('quantity', 1))

    cart = get_user_cart(request.user)
    item, created = cart.items.get_or_create(product=product)
    item.quantity += qty
    item.save()

    return redirect('shop:cart_detail')

def cart_remove(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.user.is_authenticated:
        cart = get_user_cart(request.user)
        cart.items.filter(product=product).delete()
    else:
        _cart_remove(request, pk)

    return redirect('shop:cart_detail')


def cart_detail(request):
    if request.user.is_authenticated:
        cart = get_user_cart(request.user)
        items = cart.items.all()
        total = cart.get_total()
    else:
        items, total = _get_cart_items(request)

    return render(request, 'shop/cart_detail.html', {
        'cart_items': items,
        'total': total,
    })

# @login_required(login_url='users:login')
# def checkout(request):
#     buy_now = request.session.get('buy_now')

#     if buy_now:
#         product = get_object_or_404(Product, pk=buy_now['product_id'])
#         quantity = buy_now.get('quantity', 1)
#         items = [{
#             'product': product,
#             'quantity': quantity,
#             'line_total': product.price * quantity
#         }]
#         total = product.price * quantity
#     else:
#         items, total = _get_cart_items(request)

#     if request.method == 'POST':
#         form = OrderCreateForm(request.POST)
#         if form.is_valid():
#             order = form.save(commit=False)
#             order.user = request.user
#             order.save()

#             for it in items:
#                 OrderItem.objects.create(
#                     order=order,
#                     product=it['product'],
#                     price=it['product'].price,
#                     quantity=it['quantity']
#                 )

#             # --- Stripe Checkout Session ---
#             line_items = []
#             for it in items:
#                 line_items.append({
#                     'price_data': {
#                         'currency': 'inr',  # change if needed
#                         'unit_amount': int(it['product'].price * 100),  # in paise
#                         'product_data': {
#                             'name': it['product'].title,
#                         },
#                     },
#                     'quantity': it['quantity'],
#                 })

#             checkout_session = stripe.checkout.Session.create(
#                 payment_method_types=['card'],
#                 line_items=line_items,
#                 mode='payment',
#                 success_url=request.build_absolute_uri('/checkout/success/'),
#                 cancel_url=request.build_absolute_uri('/checkout/cancel/'),
#             )

#             return redirect(checkout_session.url)
#     else:
#         form = OrderCreateForm()

#     return render(request, 'shop/checkout.html', {
#         'form': form,
#         'cart_items': items,
#         'total': total,
#         'stripe_public_key': settings.STRIPE_PUBLIC_KEY
#     })
@login_required(login_url='users:login')
def checkout(request):
    # Check if user is buying a single product now
    buy_now = request.session.get('buy_now')

    if buy_now:
        product = get_object_or_404(Product, pk=buy_now['product_id'])
        quantity = buy_now.get('quantity', 1)
        items = [{
            'product': product,
            'quantity': quantity,
            'line_total': product.price * quantity
        }]
        total = product.price * quantity
    else:
        # Assume _get_cart_items(request) returns (items_list, total_amount)
        items, total = _get_cart_items(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            # Save each item in the order
            for it in items:
                OrderItem.objects.create(
                    order=order,
                    product=it['product'],
                    price=it['product'].price,
                    quantity=it['quantity']
                )

            # Clear buy_now from session if used
            if 'buy_now' in request.session:
                del request.session['buy_now']

            # Redirect to a success page (no payment involved)
            return redirect('shop:checkout_success')
    else:
        form = OrderCreateForm()

    return render(request, 'shop/checkout.html', {
        'form': form,
        'cart_items': items,
        'total': total,
    })
def checkout_success(request):
    session_id = request.GET.get('session_id')
    if session_id:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            order_id = session.metadata.get('order_id')
            order = Order.objects.get(pk=order_id)
            order.status = 'paid'
            order.save()
            request.session.pop('buy_now', None)
            request.session.pop(CART_SESSION_ID, None)
            return render(request, 'shop/checkout_success.html', {'order': order})
        except Exception:
            pass
    return render(request, 'shop/checkout_success.html', {'order': None})

def checkout_cancel(request):
    return render(request, 'shop/checkout_cancel.html')

@login_required(login_url='users:login')
def buy_now(request, pk):
    product = get_object_or_404(Product, pk=pk)

    quantity = int(request.POST.get("quantity", 1))

    request.session['buy_now'] = {
        'product_id': product.id,
        'quantity': quantity
    }
    request.session.modified = True

    return redirect('shop:checkout')
