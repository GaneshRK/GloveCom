from .models import Cart

def get_user_cart(user):
    if not user.is_authenticated:
        return None
    cart, created = Cart.objects.get_or_create(user=user)
    return cart
