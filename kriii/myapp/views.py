from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from myapp.form import CustomeraddressForm
from myapp.models import ProductModel,Cart,Wishlist,CustomeraddressModel,Order
import razorpay


def HomeView(request):
    data = ProductModel.objects.all()
    return render(request,'home.html',{'data':data})

def signup(request):
    if request.method =='POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.info(request,'User already exists')

        if User.objects.filter(email=email).exists():
            messages.info(request,'Email already exists')

        usr = User(username=username,email=email)
        usr.set_password(password)
        usr.save()

    return render(request,'signup.html')

def LoginInfo(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']



        usr = authenticate(username=username, password=password)
    
        if usr is not None:
            login(request, usr)
            return redirect('home')
            
        
        else:
            messages.error(request,'Password not correct')
            return redirect('login')

     
    return render(request,'login.html')

def LogoutView(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('home')

def Productdetails(request,id):
    data = ProductModel.objects.get(id=id)
    return render(request,'productdetail.html',{'i':data})

def CartView(request):        
    cart_count = Cart.objects.filter(user=request.user).count()
    cart_items = Cart.objects.filter(user=request.user)

    sub_total = 0
    ship_charge = 70
    GST = 120
    grand_total = 0
    # get data for order
    user = request.user
    get_address_id = request.GET.get('add')
    print(get_address_id, "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

    for i in cart_items:
        
        sub_total += i.prod_total()
        grand_total = sub_total + ship_charge + GST
        GST = grand_total*0.18
        print(grand_total, "ggggggggggggggggggggggggggggg")
    
    # sub_total = 0
    # ship_charge = 30
    # GST = 120
    # grand_total = 0
    # for i in cart_items:
    #     sub_total += i.prod_total()
    # grand_total = sub_total + ship_charge + GST

    context = {'cart_count': cart_count, 'cart_items': cart_items, 'sub_total': sub_total,'ship_charge': ship_charge, 'GST': GST, 'grand_total': grand_total,}
    return render(request, 'cart.html', context)

def Add_to_cartView(request, id):
    user = request.user
    prod = ProductModel.objects.get(id=id)
    item_exist = Cart.objects.filter(product=prod).exists()

    if item_exist:
        get_item = Cart.objects.get(product__id=id)
        get_item.quantity += 1
        get_item.save()
        return redirect('/cart/')
    else:
        product = ProductModel.objects.get(id=id)
    Cart(user=user, product=product).save()
    return redirect('/cart/')

def pluse_quantity(request, id):
    get_item = Cart.objects.get(id=id)
    if get_item:
        get_item.quantity += 1
        get_item.save()
        return redirect('/cart/')


def minus_quantity(request, id):
    get_item = Cart.objects.get(id=id)
    if get_item:
        get_item.quantity -= 1
        get_item.save()
        if get_item.quantity == 0:
            get_item.delete()
        return redirect('/cart/')


def DeleteView(request, id):
    get_item = Cart.objects.get(id=id)
    get_item.delete()
    get_name = get_item.product.name
    print(get_name)
    messages.error(request, f'{get_name} - Successfully delete')
    return redirect('/cart/')

def clearcart(request):
    cart_items = Cart.objects.filter(user=request.user)
    cart_items.delete()
    messages.error(request, 'Cart Successfully Cleared')
    return redirect('/cart/')

def WishListView(request):        
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    wishlist_items = Wishlist.objects.filter(user=request.user)
    cart_count = Cart.objects.filter(user=request.user).count()


    context = {'wishlist_count': wishlist_count, 'wishlist_items': wishlist_items,'cart_count':cart_count}
    return render(request, 'wishlist.html', context)

def Add_to_wishlist(request, id):
    user = request.user
    prod = ProductModel.objects.get(id=id)
    item_exist = Wishlist.objects.filter(product=prod).exists()

    if item_exist:
        get_item = Wishlist.objects.get(product__id=id)
        get_item.quantity += 1
        get_item.save()
        return redirect('/wishlist/')
    else:
        product = ProductModel.objects.get(id=id)
    Wishlist(user=user, product=product).save()
    return redirect('/wishlist/')

def ListDeleteView(request, id):
    get_item = Wishlist.objects.get(id=id)
    get_item.delete()
    get_name = get_item.product.name
    print(get_name)
    messages.error(request, f'{get_name} - Successfully delete')
    return redirect('/wishlist/')


def CustomerAddressView(request):
    all_address = CustomeraddressModel.objects.filter(user=request.user)
    if request.user.is_authenticated:
        form = CustomeraddressForm(instance=request.user)
        context = {'form': form}
        if request.method == 'POST':
            form = CustomeraddressForm(request.POST)
            if form.is_valid():
                fm = form.save(commit=False)
                fm.user = request.user
                fm.save()

                messages.info(request, 'Address Successfully Added')
                return redirect('/address/')
        else:
            form = CustomeraddressForm(instance=request.user)

        context = {'form': form, 'all_address': all_address}
        return render(request, 'address.html', context)
    else:
        messages.info(request, '☹︎ Please Login First')
        return redirect('/signin/')


#CustAdd Update Start

def UpdateaddressView(request, id):
    address = CustomeraddressModel.objects.all()  # Show data of Student Table
    set_address = CustomeraddressModel.objects.get(id=id)
    if request.method == 'POST':
        form = CustomeraddressForm(
            request.POST, request.FILES, instance=set_address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student Successfully Updated')
            return redirect('/address/')
    else:
        form = CustomeraddressForm(instance=set_address)
    context = {'form': form, 'address': address}
    return render(request, 'address.html', context)

def AddressDeleteView(request, id):
    address = CustomeraddressModel.objects.get(id=id)
    address.delete()
    messages.error(request, 'address Successfully delete')
    return redirect('/address/')

#Custadd Update End

#Cust add delete start

def AddressDeleteView(request, id):
    address = CustomeraddressModel.objects.get(id=id)
    address.delete()
    messages.error(request, 'address Successfully delete')
    return redirect('/address/')


def CheckoutView(request):
    cart_count = Cart.objects.filter(user=request.user).count()
    cart_items = Cart.objects.filter(user=request.user)
    all_address = CustomeraddressModel.objects.filter(user=request.user)
    # totals count -----
    sub_total = 0
    ship_charge = 70
    GST = 120
    grand_total = 0
    # get data for order
    usr = request.user
    get_address_id = request.GET.get('add')
    print(get_address_id, "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

    for i in cart_items:
        sub_total += i.prod_total()
        grand_total = sub_total + ship_charge + GST
        print(grand_total, "ggggggggggggggggggggggggggggg")
    # payment Start
    amount = (grand_total)*100 
    client = razorpay.Client(
        auth=("rzp_test_XhWHxn3hErs5Or", "Q85hbICGMOD4aJRCHJKQXRF7"))
    payment = client.order.create(
        {'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
    # payment End
    if get_address_id:
        address = CustomeraddressModel.objects.get(id=get_address_id)
        for i in cart_items:
            order_data = Order(
                user=usr,
                customer=address,
                product=i.product,
                quantity=i.quantity

            )
            order_data.save()
        cart_items.delete()
    context = {'cart_count': cart_count, 'cart_items': cart_items, 'sub_total': sub_total,
               'ship_charge': ship_charge, 'GST': GST, 'grand_total': grand_total, 'all_address': all_address,
               'payment': payment}
    return render(request, 'checkout.html', context)


def OrderView(request):
    cust_order = Order.objects.filter(user=request.user)
    context = {'cust_order': cust_order}
    return render(request, 'order.html', context)






# Create your views here.
