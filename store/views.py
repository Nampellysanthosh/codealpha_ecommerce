from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.utils.http import url_has_allowed_host_and_scheme
from decimal import Decimal

from .models import Product, Order, OrderItem
from .forms import UserRegistrationForm, CheckoutForm


def home_view(request):
    """
    Homepage displaying featured products and category options.
    """
    categories = [cat[0] for cat in Product.CATEGORY_CHOICES]
    products = Product.objects.all()
    
    selected_category = request.GET.get('category', '')
    query = request.GET.get('q', '').strip()

    if selected_category:
        products = products.filter(category__iexact=selected_category)
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) | 
            Q(category__icontains=query)
        )

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': query,
    }
    return render(request, 'store/home.html', context)


def product_detail_view(request, pk):
    """
    Product detailed page showing image, description, price, stock, and quantity selector.
    """
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)


def _get_cart_items_and_total(session):
    """
    Helper function to load cart items from session and calculate totals.
    """
    cart = session.get('cart', {})
    cart_items = []
    total_price = Decimal('0.00')

    for product_id_str, quantity in cart.items():
        try:
            product = Product.objects.get(pk=int(product_id_str))
            subtotal = product.price * quantity
            total_price += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
                'out_of_stock': quantity > product.stock,
            })
        except Product.DoesNotExist:
            continue

    return cart_items, total_price


def cart_view(request):
    """
    View shopping cart contents, modify quantities, or proceed to checkout.
    """
    cart_items, total_price = _get_cart_items_and_total(request.session)
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'store/cart.html', context)


def cart_add_view(request, pk):
    """
    Add a product to session cart or update its quantity.
    """
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
        except (ValueError, TypeError):
            quantity = 1
    else:
        quantity = 1

    if quantity < 1:
        quantity = 1

    cart = request.session.get('cart', {})
    product_id_str = str(product.id)
    current_qty = cart.get(product_id_str, 0)
    new_qty = current_qty + quantity

    if product.stock <= 0:
        messages.error(request, f"Sorry, '{product.name}' is currently out of stock.")
        return redirect('product_detail', pk=product.pk)

    if new_qty > product.stock:
        messages.warning(
            request, 
            f"Only {product.stock} units of '{product.name}' available in stock. Added maximum available."
        )
        cart[product_id_str] = product.stock
    else:
        cart[product_id_str] = new_qty
        messages.success(request, f"Added {quantity} x '{product.name}' to your shopping cart!")

    request.session['cart'] = cart
    request.session.modified = True

    # Keep navigation on this site when honoring a submitted or referrer URL.
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER')
    if not next_url or not url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = 'cart'
    return redirect(next_url)


def cart_update_view(request, pk):
    """
    Update item quantity directly from the cart view.
    """
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart', {})
    product_id_str = str(product.id)

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'increase':
            current_qty = cart.get(product_id_str, 0)
            if current_qty + 1 > product.stock:
                messages.warning(request, f"Cannot add more. Only {product.stock} in stock.")
            else:
                cart[product_id_str] = current_qty + 1
        elif action == 'decrease':
            current_qty = cart.get(product_id_str, 0)
            if current_qty - 1 <= 0:
                del cart[product_id_str]
                messages.info(request, f"Removed '{product.name}' from your cart.")
            else:
                cart[product_id_str] = current_qty - 1
        elif action == 'set':
            try:
                new_qty = int(request.POST.get('quantity', 1))
            except (ValueError, TypeError):
                new_qty = 1

            if new_qty <= 0:
                if product_id_str in cart:
                    del cart[product_id_str]
                    messages.info(request, f"Removed '{product.name}' from your cart.")
            elif new_qty > product.stock:
                cart[product_id_str] = product.stock
                messages.warning(request, f"Adjusted quantity to maximum available stock ({product.stock}).")
            else:
                cart[product_id_str] = new_qty

        request.session['cart'] = cart
        request.session.modified = True

    return redirect('cart')


def cart_remove_view(request, pk):
    """
    Remove product completely from session cart.
    """
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart', {})
    product_id_str = str(product.id)

    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, f"Removed '{product.name}' from your shopping cart.")

    return redirect('cart')


@login_required(login_url='login')
def checkout_view(request):
    """
    Checkout page requiring login. Validates cart & stock, processes order within DB transaction.
    """
    cart_items, total_price = _get_cart_items_and_total(request.session)

    if not cart_items:
        messages.warning(request, "Your shopping cart is empty. Please add products before checking out.")
        return redirect('home')

    # Check if any cart item exceeds available stock
    for item in cart_items:
        if item['quantity'] > item['product'].stock:
            messages.error(
                request, 
                f"Item '{item['product'].name}' has only {item['product'].stock} units left. Please update your cart."
            )
            return redirect('cart')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Re-verify stock inside atomic transaction to prevent race conditions
                    for item in cart_items:
                        prod = Product.objects.select_for_update().get(pk=item['product'].pk)
                        if prod.stock < item['quantity']:
                            raise ValueError(f"Insufficient stock for {prod.name}. Available: {prod.stock}")

                    # Create Order
                    order = form.save(commit=False)
                    order.user = request.user
                    order.total_amount = total_price
                    order.status = 'Pending'
                    order.save()

                    # Create OrderItems & update Product stock
                    for item in cart_items:
                        prod = Product.objects.select_for_update().get(pk=item['product'].pk)
                        OrderItem.objects.create(
                            order=order,
                            product=prod,
                            product_name=prod.name,
                            quantity=item['quantity'],
                            price=prod.price,
                            subtotal=prod.price * item['quantity']
                        )
                        # Reduce stock
                        prod.stock -= item['quantity']
                        prod.save()

                    # Clear session cart
                    request.session['cart'] = {}
                    request.session.modified = True

                    messages.success(request, f"Thank you! Your order #{order.id} has been placed successfully.")
                    return redirect('order_success', pk=order.pk)

            except ValueError as ve:
                messages.error(request, str(ve))
                return redirect('cart')
            except Exception as e:
                messages.error(request, "An error occurred while processing your order. Please try again.")
    else:
        # Pre-fill form if user has profile details
        initial_data = {
            'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'email': request.user.email,
        }
        form = CheckoutForm(initial=initial_data)

    context = {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'store/checkout.html', context)


@login_required(login_url='login')
def order_success_view(request, pk):
    """
    Order success confirmation page.
    """
    order = get_object_or_404(Order, pk=pk)

    # Users can only view their own order, unless they are staff.
    if order.user != request.user and not request.user.is_staff:
        messages.error(request, "You are not authorized to view this order summary.")
        return redirect('home')

    context = {
        'order': order,
        'order_items': order.items.all(),
    }
    return render(request, 'store/order_success.html', context)


@login_required(login_url='login')
def orders_list_view(request):
    """
    Display order history for the logged-in user.
    """
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'store/orders.html', context)


@login_required(login_url='login')
def order_detail_view(request, pk):
    """
    Display details for a specific order owned by the user.
    """
    order = get_object_or_404(Order, pk=pk)
    
    # Enforce user authorization check
    if order.user != request.user and not request.user.is_staff:
        messages.error(request, "Unauthorized access: You can only view your own orders.")
        return redirect('orders')

    context = {
        'order': order,
        'order_items': order.items.all(),
    }
    return render(request, 'store/order_detail.html', context)


def search_view(request):
    """
    Search products by name, description, or category.
    """
    query = request.GET.get('q', '').strip()
    products = Product.objects.none()
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) | 
            Q(category__icontains=query)
        )

    categories = [cat[0] for cat in Product.CATEGORY_CHOICES]
    context = {
        'products': products,
        'search_query': query,
        'categories': categories,
    }
    return render(request, 'store/home.html', context)


def category_view(request, category):
    """
    Filter products by category name.
    """
    products = Product.objects.filter(category__iexact=category)
    categories = [cat[0] for cat in Product.CATEGORY_CHOICES]
    
    context = {
        'products': products,
        'selected_category': category,
        'categories': categories,
    }
    return render(request, 'store/home.html', context)


def register_view(request):
    """
    User registration view with validation and automatic login.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            messages.success(request, f"Account created successfully for @{user.username}! You are now logged in.")
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'store/register.html', context)


def login_view(request):
    """
    User login view supporting standard Django authentication.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                next_page = request.GET.get('next')
                if not next_page or not url_has_allowed_host_and_scheme(
                    next_page,
                    allowed_hosts={request.get_host()},
                    require_https=request.is_secure(),
                ):
                    next_page = 'home'
                return redirect(next_page)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid credentials entered. Please check your username and password.")
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
    }
    return render(request, 'store/login.html', context)


def logout_view(request):
    """
    User logout view.
    """
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')


def custom_404(request, exception=None):
    """
    Custom 404 error page.
    """
    return render(request, 'store/404.html', status=404)
