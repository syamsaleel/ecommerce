from django.shortcuts import render ,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm,UserRegisterForm
from .cart import Cart
from .forms import OrderForm
from .models import Order
from django.contrib.auth import logout
from .models import Profile

from django.contrib.auth import(
    authenticate,
    get_user_model,
    login,
    logout
)

def home(request):
    message = "Welcome to our Ecommerce Web App!"
    context = {'message': message}
    return render(request, 'webapp/new.html', context)


def login_view(request):
    form=UserLoginForm(request.POST or None)
    if form.is_valid():
        username=form.cleaned_data.get('username')
        password=form.cleaned_data.get('password')
        user =authenticate(username=username,password=password)
        login(request,user)

        return redirect('home')
    context ={
        'form':form,
    }
    return render(request, "webapp/login.html", context)

from .models import Profile

def register_view(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()

        # Create a profile for the newly registered user
        profile = Profile.objects.create(user=user, address='', phone_number='')

        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect('profile')
    
    context = {'form': form}
    return render(request, 'webapp/signup.html', context)




from .models import Profile
from django.contrib.auth.models import User
from .forms import ProfileForm


@login_required
def profile_view(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user,complete=False)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=user_profile)

    context = {'form': form}
    return render(request, 'webapp/profile.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


from .models import Product

@login_required
def product_list(request):
    products = Product.objects.all()
    context={
        'products': products
        }
    return render(request, 'webapp/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'webapp/product_detail.html', context)


from .cart import Cart


def cart(request):
    cart = Cart(request)
    products = Product.objects.filter(pk__in=cart.cart.keys())
    context = {'cart': cart, 'products': products}
    return render(request, 'webapp/cart.html', context)

def add_to_cart(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(pk=product_id)
    cart.add(product, quantity=1)
    return redirect('cart')


def update_cart(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(pk=product_id)
    quantity = int(request.POST.get('quantity'))
    cart.update(product, quantity)
    return redirect('cart')

def remove_cart(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(pk=product_id)
    cart.remove(product)
    return redirect('cart')

#@login_required
#def create_profile(request):
#    try:
#        profile = request.user.profile
#    except Profile.DoesNotExist:
#        profile = Profile(user=request.user)
#        profile.save()
#    return redirect('webapp/detail.html') 

#@login_required
#def profile_detail(request):
#    profile = request.user.profile
#    return render(request, 'webapp/detail.html', {'profile': profile})


#from django.contrib.auth.decorators import login_required
#from .models import Profile
#from django.contrib.auth.models import User


@login_required
def profile_view(request):
    user = request.user
    try:
        user_profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        # Handle the case where the profile doesn't exist
        user_profile = None

    context = {
        'user': user,
        'user_profile': user_profile
    }
    return render(request, 'webapp/profile.html', context)



from .forms import ProfileEditForm

@login_required
def profile_edit(request):
    user = request.user
    try:
        user_profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        user_profile = None

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=user_profile, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=user_profile, user=request.user)

    context = {
        'user': user,
        'form': form
    }
    return render(request, 'webapp/profile_edit.html', context)








from django.core.paginator import Paginator
from django.contrib import messages
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .forms import OrderCreateForm
from .models import OrderItem
from .cart import Cart

from django.http import HttpResponse

from .forms import OrderCreateForm
from .models import Order
import traceback

def create_order(request):
    cart = Cart(request)
    if request.user.is_authenticated:
        customer = get_object_or_404(User, id=request.user.id)
        form = OrderCreateForm(request.POST or None, initial={"name": customer.first_name, "email": customer.email})
        if request.method == 'POST':
            if form.is_valid():
                order = form.save(commit=False)
                order.user = request.user
                order.total_price = cart.get_total_price()
                try:
                    order.save()
                except Exception as e:
                    print(f"Error saving order: {e}")
                    import traceback
                    traceback.print_exc()
                    messages.error(request, "An error occurred while saving the order.")
                    return redirect('successfull')

                print(f"Order ID: {order.pk}")  # Print the order id for debugging

                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        quantity=item['quantity'],
                        price=item['product'].price,
                    )

                cart.clear()
                return render(request, 'webapp/successfull.html', {'order': order})

            else:
                messages.error(request, "Fill out your information correctly.")

        if len(cart) > 0:
            return render(request, 'webapp/order.html', {"form": form})

    return redirect('/')



def successfull_view(request):
    return render(request, 'webapp/successfull.html')

#def order_list(request):
#    my_order = Order.objects.filter(customer_id=request.user.id).order_by('-created_at')
#    paginator = Paginator(my_order, 5)
#    page = request.GET.get('page')
#    myorder = paginator.get_page(page)

 #   return render(request, 'order/list.html', {"myorder": myorder})


#def order_details(request, id):
#    order_summary = get_object_or_404(Order, id=id)

 #   if order_summary.customer_id != request.user.id:
 #       return redirect('store:index')

 #   ordered_items = OrderItem.objects.filter(order_id=id)
 #   context = {
 #       "order_summary": order_summary,
  #      "ordered_items": ordered_items
   # }
   # return render(request, 'order/details.html', context)

from django.shortcuts import render, redirect
from .models import Product

def admin_panel(request):
    if request.user.is_authenticated and request.user.is_superuser:
        products = Product.objects.all()
        print(products)
        return render(request, 'webapp/admin_panel.html', {'products': products})
    else:
        return redirect('home')  # Redirect non-superusers to the home page

def update_quantity(request, product_id):
    if request.user.is_superuser and request.method == 'POST':
        quantity = request.POST.get('quantity')
        product = Product.objects.get(pk=product_id)
        product.quantity = quantity
        product.save()
    return redirect('webapp/admin_panel')

