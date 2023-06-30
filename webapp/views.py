from django.shortcuts import render ,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm,UserRegisterForm,ProductForm,OrderCreateForm,ProfileForm
from .cart import Cart
from django.contrib.auth import logout
from .models import Profile
from django.contrib import messages
from django.contrib import messages
from django.views import View
from .models import OrderItem,Profile,Product,Order
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
import traceback

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


from django.shortcuts import render, get_object_or_404
from .models import Order

def order_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, 'webapp/successfull.html', {'order': order})


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

                print(f"Order ID: {order.pk}") 

                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        quantity=item['quantity'],
                        price=item['product'].price,
                    )

                cart.clear()
                return redirect('order_success', order_id=order.pk) 

            else:
                messages.error(request, "Fill out your information correctly.")

        if len(cart) > 0:
            return render(request, 'webapp/order.html', {"form": form})

    return redirect('/')



def successfull_view(request):
    return render(request, 'webapp/successfull.html')




@method_decorator(login_required, name='dispatch')
class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        context = {'form': form}
        return render(request, 'webapp/login.html', context)

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('adminhome')
                else:
                    return redirect('home')

        context = {'form': form}
        return render(request, 'webapp/login.html', context)
    
@login_required
def admin_home(request):
    products = Product.objects.all()
    context = {'products': products}
   
    return render(request, 'webapp/admin_home.html')


def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New product added successfully.')
            return redirect('adminhome')
    else:
        form = ProductForm()

    context = {'form': form}
    return render(request, 'webapp/create_product.html', context)

def user_list(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'webapp/users_list.html', context)

def product_list(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'webapp/product_list.html', context)

def order_list(request):
    orders=Order.objects.all()
    context = {'orders': orders}
    return render(request, 'webapp/order_list.html', context)