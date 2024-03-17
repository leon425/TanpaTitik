from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import *
from .forms import *
import json
import requests
import time
from .shipping import *
import http.client
import midtransclient

class EditProfile(PasswordChangeView):
    form_edit_profile = PasswordChangeForm
    success_url = reverse_lazy('profile')


def base2(request):
    return render(request, "main/base2.html", {})

def home (request):
    firstProduct = Products.objects.get(name="Blue Vest") #First Displayed in the Carousel
    products = Products.objects.all()
    testimony = Testimony.objects.all()
    faqs = FAQs.objects.all()
    logo = Additional.objects.get(name="logo")

    if request.user.is_authenticated == True:
        customer = Customer.objects.get(user=request.user)
        customer_wishlist = Wishlist.objects.filter(customer=customer)
        order, created = Order.objects.get_or_create(customer=customer, current=True) 
    else:
        customer = None
        customer_wishlist = []
        order = {'get_cart_total':0, 'get_cart_items':0}

    if request.POST.get("remove_search_button"):
        print("remove_search_button")

    if request.method == 'POST':
        searched = request.POST.get("search_bar", "")
        products = Products.objects.filter(name__contains=searched)
        print("ues")
        # alter the product 
        # add description (Showing Result for)
        # add a close button (To give back the products queryset back)
    else:
        searched = ""

    

    return render(request, "main/home.html", {"logo":logo,"user":request.user,"customer":customer,"products":products,"firstProduct":firstProduct,"order":order,"customer_wishlist":customer_wishlist,"testimony":testimony,"faqs":faqs, "searched":searched})

def product(request, pk): #pk is the product id
    logo = Additional.objects.get(name="logo")
    products = Products.objects.all()
    thisProduct = Products.objects.get(id=pk)
    ruler_icon = Additional.objects.get(name="ruler_icon")
    thumbs_up = Additional.objects.get(name="thumbs_up")
    thumbs_down = Additional.objects.get(name="thumbs_down")
    thisProduct_img = Products_img.objects.filter(product=thisProduct)

    # Product Review
    product_star_dict={}
    for product in products:
        star_array =[]
        for i in range(1,6):
            star_array.append(len(product.products_review_set.all().filter(star=i)))
            # print(product,i,product.products_review_set.all().filter(star=i))
            # print(len(product.products_review_set.all().filter(star=i)))
        product_star_dict[product.id] = (star_array)
    print(product_star_dict)


    if request.user.is_authenticated == True:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, current=True) 
        customer_wishlist = Wishlist.objects.filter(customer=customer)
        itemInCart = OrderItem.objects.filter(order=order,product=thisProduct)
        itemInWishlist = Wishlist.objects.filter(customer=customer, product=thisProduct)
    else: 
        customer = None
        order = {'get_cart_total':0, 'get_cart_items':0}
        itemInCart = []
        itemInWishlist = []
        customer_wishlist = []

    # print(thisProduct_stock)
    return render(request, "main/product.html", {"logo":logo,"thisProduct":thisProduct,"thisProduct_img":thisProduct_img, "order":order,"itemInCart":itemInCart,"itemInWishlist":itemInWishlist, "customer_wishlist":customer_wishlist,"ruler_icon":ruler_icon,"product_star_dict":product_star_dict, "thumbs_up":thumbs_up, "thumbs_down":thumbs_down, "products":products,})

def cart(request):
    coupon_icon = Additional.objects.get(name="coupon_icon")
    logo = Additional.objects.get(name="logo")
    user = request.user
    if request.user.is_authenticated:
        customer = request.user.customer
        customer_wishlist = Wishlist.objects.filter(customer=customer)
        order, created = Order.objects.get_or_create(customer=customer, current=True) 
        items = order.orderitem_set.all()
        
    else:
        customer = None
        customer_wishlist = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        items = []

    context = {"collection":"collection","logo":logo,"items":items, "order":order,"customer_wishlist":customer_wishlist,"coupon_icon":coupon_icon,"user":user,}
    return render(request, "main/cart.html", context)

def wishlist(request):
    logo = Additional.objects.get(name="logo")
    wishlist = Wishlist.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, current=True)
        customer_wishlist = Wishlist.objects.filter(customer=customer)
    else: 
        customer = None
        order = {'get_cart_total':0, 'get_cart_items':0}
        customer_wishlist = []


    context = {"logo":logo,"wishlist":wishlist,"customer_wishlist":customer_wishlist,"customer":customer,"order":order,}
    return render(request, "main/wishlist.html", context)

def checkout(request):
    logo = Additional.objects.get(name="logo")
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, current=True)
        customer_wishlist = Wishlist.objects.filter(customer=customer)
        newAddress,created = ShippingAddress.objects.get_or_create(customer=customer)
        items = order.orderitem_set.all()

        # SHIPPING ADDRESS FORM
        if request.method == 'POST':
            form_shipping = LocationForm(request.POST)

            # REGISTER NEW ADDRESS FORM
            if form_shipping.is_valid():
                address = form_shipping.cleaned_data["address"]
                district = form_shipping.cleaned_data["district"]
                city = form_shipping.cleaned_data["city"]
                province = form_shipping.cleaned_data["province"]
                zipcode = form_shipping.cleaned_data["zipcode"]
                if ShippingAddress.objects.filter(customer=customer).exists():
                    ShippingAddress.objects.filter(customer=customer).delete()
                newAddress, created = ShippingAddress.objects.get_or_create(customer=customer, address=address, district=district, city=city, province=province, zipcode=zipcode)


        # CALCULATE THE SHIPPING COST AND DELIVERY TIME
        if ShippingAddress.objects.filter(customer=customer).exists() and newAddress.city != None and newAddress.province !=None :
            selectedCity = City.objects.get(name=newAddress.city)
            city_identifier = selectedCity.identifier

            def shippingCost(originID,destinationID):
                conn = http.client.HTTPSConnection("api.rajaongkir.com")
                payload = f"origin={originID}&destination={destinationID}&weight=700&courier=pos"
                headers = {
                    'key': "3921e2bb12875d82fe604ae0b153d62b",
                    'content-type': "application/x-www-form-urlencoded"
                    }
                conn.request("POST", "/starter/cost", payload, headers)
                res = conn.getresponse()
                data = res.read()
                return(json.loads(data.decode('utf-8'))) #Change the data type from byte to string to dictionary
            
            # THE ORIGINID IS TENTATIF (South Tangerang City)
            result = shippingCost(455,city_identifier)
            final_shipping_cost = result['rajaongkir']['results'][0]['costs']
            print(final_shipping_cost)

            for i in final_shipping_cost:
                if i['service'] == 'Pos Reguler':
                    order.shipping_cost = i['cost'][0]['value']
                    deliveryTime = i['cost'][0]['etd'].split(" ")
                    order.delivery_time = int(deliveryTime[0])+1
                    order.save()

            # [{'service': 'Pos Reguler', 'description': 'Pos Reguler', 
            #   'cost': [{'value': 30000, 'etd': '7 HARI', 'note': ''}]}]
        
        if City.objects.filter(name=newAddress.city).exists():
            newAddress_isValid = True
        else:
            newAddress_isValid = False

        # PAYMENT INTEGRATION
        # Create Snap API instance
        snap = midtransclient.Snap(
            # Set to true if you want Production Environment (accept real transaction).
            is_production=False,
            server_key='SB-Mid-server-hlFNJieGBtXM7-IfvdUpFlPo'
        )
        # Build API parameter
        param = {
            "transaction_details": {
                "order_id": str(order.id+103),
                "gross_amount": order.calculate_subtotal
            }, "credit_card":{
                "secure" : True
            }, "customer_details":{
                "first_name": customer.user.first_name,
                "last_name": customer.user.last_name,
                "email": customer.user.email,
            }, "content-type":"application/json",
                "accept":"application/json",
        }

        transaction = snap.create_transaction(param)
        
        transaction_token = transaction['token']
        print(transaction_token)
        payment_url = "https://app.sandbox.midtrans.com/snap/v2/vtweb/"+transaction_token
  
    else:
        customer = "Guest"
        order = {'get_cart_total':0, 'get_cart_items':0}
        customer_wishlist = []
        newAddress = None
        items = []
        newAddress_isValid = False
        payment_url = "#"

    form_shipping = LocationForm()
    
    context = {"logo":logo,"customer":customer,"order":order,"items":items, "form_shipping":form_shipping,"newAddress":newAddress, "newAddress_isValid":newAddress_isValid, "customer_wishlist":customer_wishlist,"payment_url":payment_url}
    return render(request, "main/checkout.html", context) 

# urls redirect to purchase product => tempQWmUpMeekhv9NGxBGf5PzCnu8
def temp(request):
    
    # def handle_http_notification(request):
    #     if request.method == 'POST':
    #         payload = request.body.decode('utf-8')
    #         json_payload = json.loads(payload)

    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.filter(customer=customer, current=True)
        thisOrder = order[0]
    else:
       customer = None
       thisOrder = 0
    return redirect("/checkout/done/"+thisOrder)

def checkout_done(request,pk):
    logo = Additional.objects.get(name="logo")
    products = Products.objects.all()
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order_checkout_done_array = Order.objects.filter(customer=customer, id=pk) #pk
        order_checkout_done = order_checkout_done_array[0]
        print(order_checkout_done)
        order, created = Order.objects.get_or_create(customer=customer, current=True) # For the logo
        items = order_checkout_done.orderitem_set.all()
        customer_wishlist = Wishlist.objects.filter(customer=customer)
        newAddress, created = ShippingAddress.objects.get_or_create(customer=customer)

        order_checkout_done.current = False
        order_checkout_done.save()

        # REMOVE PRODUCT ORIGINAL STOCK
        for item in items:
            print(item.product.remove_stock(item.quantity))
            item.product.save()

        # # ORDER PLACEMENT
        # if order_checkout_done.status == OrderStatus.objects.get(name="Placed"): 

        #     # SETTING THE PAYMENT
        #     if Payment.objects.filter(customer=customer,order=order_checkout_done).exists():
        #         payment = Payment.objects.get(customer=customer,order=order_checkout_done)
        #     else:
        #         payment= Payment.objects.create(customer=customer, order=order_checkout_done, payment_method=order_checkout_done.payment_method, complete=False)

        #     # ORDER IS COMPLETE AND NOT CURRENT ANYMORE (CAN'T EDIT IN CART)
        #     order_checkout_done.current = False
        #     order_checkout_done.save()
        #     print(order_checkout_done.current)

        #     # REMOVE PRODUCT ORIGINAL STOCK
        #     # for item in items:
        #     #     print(item.product.remove_stock(item.quantity))
        #     #     item.product.save()

        #     # IF MORE THAN 5 HOURS UNPAID
        #     time_difference = time.time() - payment.payment_timestamp.timestamp()
        #     if time_difference >= 5 * 60 * 60: # Have been Tested. FAILED TO WORK PROPERLY
        #     # if time_difference >= 60:
        #         order_checkout_done.status = OrderStatus.objects.get(name="Cancelled")
        #         order_checkout_done.save()
        #         payment.delete()
        #         print(order_checkout_done.status)
        #         # reject => delete payment. order set to false
        #         # product stock restore

        #     # If Image uploaded => Status -> Pending
        #     if request.method == 'POST':
        #         payment_evidence_form = PaymentEvidence(request.POST, request.FILES)
        #         if payment_evidence_form.is_valid():
        #             payment_evidence_pict = payment_evidence_form.cleaned_data.get("payment_evidence")
        #             payment.payment_evidence = payment_evidence_pict
        #             payment.complete = True
        #             payment.save()
        #             order_checkout_done.status = OrderStatus.objects.get(name="Pending (Waiting For Verification)")
        #             order_checkout_done.save()
                    

        #             # send email to admin
        #             # Send email to customer => Your payment is being verified. Estimated time wait: 1 hour.

                    
        #     if order_checkout_done.status == OrderStatus.objects.get(name="Cancelled"):
        #         # RESTORE THE PRODUCT STOCK
        #         for item in items:
        #             print(item.product.restore_stock(item.quantity))
        #             item.product.save()

        #     if order_checkout_done.status == OrderStatus.objects.get(name="Pending (Waiting For Verification)"): # Waiting for admin verification
        #         pass

        #     # Admin Verifiy
        #     if order_checkout_done.complete == True:
        #         order_checkout_done.status = OrderStatus.objects.get(name="Packaged") #paid
        #         order_checkout_done.save()
        #         # send email to customer => Your order is being confirmed

                    
        #         if order_checkout_done.payment_method == "Cash On Delivery":
        #             # wait for user confirmation regarding the policy
        #             # payment.complete == True
        #             # order.status == "paid"
        #             # order.save()
        #             pass

        #         if order_checkout_done.payment_method == "QRIS" or order_checkout_done.payment_method == "Bank Transfer":
        #             # wait for the uploaded evidence -> Verification. Last step = order.status = pending
        #             # Then, wait for user confirmation regarding the policy
        #             pass
                    
        #         # Make code to cancel order after 1 hour paying

        #         # delivery status = packaged, delivered

    else: 
        customer = None
        order = {'get_cart_total':0, 'get_cart_items':0}
        order_checkout_done = {'get_cart_total':0, 'get_cart_items':0}
        customer_wishlist = []
        newAddress, created = None
    
    payment_evidence_form = PaymentEvidence()
    context = {"logo":logo,"wishlist":wishlist,"customer_wishlist":customer_wishlist,"customer":customer,"order":order,"order_checkout_done":order_checkout_done, "newAddress":newAddress,"payment_evidence_form":payment_evidence_form,}
    return render(request,"main/checkout_done.html",context)


def about (request):
    logo = Additional.objects.get(name="logo")
    logo2 = Additional.objects.get(name="logo2")
    about_us_1 = Additional.objects.get(name="about_us_1")
    about_us_2 = Additional.objects.get(name="about_us_2")
    about_us_3 = Additional.objects.get(name="about_us_3")
    about_us_4 = Additional.objects.get(name="about_us_4")
    identities = Identity.objects.all()

    ceo = MeetTheTeam.objects.filter(division="CEO (Chief Executive Officer)")
    production_division = MeetTheTeam.objects.filter(division="Production Division")
    marketing_division = MeetTheTeam.objects.filter(division="Marketing Division")
    design_division = MeetTheTeam.objects.filter(division="Design Division")
    finance_division = MeetTheTeam.objects.filter(division="Finance Division")

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, current=True)
        customer_wishlist = Wishlist.objects.filter(customer=customer)
    else: 
        customer = None
        order = {'get_cart_total':0, 'get_cart_items':0}
        customer_wishlist = []

    context = {"logo":logo,"logo2":logo2,"customer_wishlist":customer_wishlist,"customer":customer,"order":order, "identities":identities, "ceo":ceo, "production_division":production_division, "marketing_division":marketing_division, "design_division":design_division, "finance_division":finance_division, "about_us_1":about_us_1, "about_us_2":about_us_2,"about_us_3":about_us_3,"about_us_4":about_us_4, }
    return render(request, "main/about.html", context)

def profile(request):
    logo = Additional.objects.get(name="logo")
    wardrobe = Additional.objects.get(name="wardrobe")
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, current=True)
        placed_order_by_customer = Order.objects.filter(customer=customer,current=False)
        customer_wishlist = Wishlist.objects.filter(customer=customer)
        newAddress, created = ShippingAddress.objects.get_or_create(customer=customer)
    else: 
        return redirect('register_page')

    context = {"logo":logo,"wardrobe":wardrobe,"customer_wishlist":customer_wishlist,"customer":customer,"order":order,"newAddress":newAddress,"placed_order_by_customer":placed_order_by_customer,}
    return render(request,"main/profile.html",context)

def loginPage(request):
    logo = Additional.objects.get(name="logo")
    logo2 = Additional.objects.get(name="logo2")
    form = None

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, current=True)
        customer_wishlist = Wishlist.objects.filter(customer=customer)
    else: 
        customer = None
        order = {'get_cart_total':0, 'get_cart_items':0}
        customer_wishlist = []

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request,'Username or Password is incorrect')
            # context = {"logo":logo,"logo2":logo2,"customer_wishlist":customer_wishlist,"customer":customer,"order":order,"form":form}
            # return render(request,"registration/login.html",context) # make sure we're sending this to login page

    context = {"logo":logo,"logo2":logo2,"customer_wishlist":customer_wishlist,"customer":customer,"order":order,"form":form}
    return render(request,"registration/login.html",context)

def registerPage(request):
    logo = Additional.objects.get(name="logo")
    logo2 = Additional.objects.get(name="logo2")
    form = CreateUserForm() #Replace UserCreationForm(). It's the replica or the modified form

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, current=True)
        customer_wishlist = Wishlist.objects.filter(customer=customer)
    else: 
        customer = None
        order = {'get_cart_total':0, 'get_cart_items':0}
        customer_wishlist = []

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save() #All the form is saved (built-in feature)
            # Create The Customer Object
            customer_name = str(user.first_name)+" "+str(user.last_name)
            customer_created = Customer.objects.create(user=user,name=customer_name,email=user.email)
            user = form.cleaned_data.get('username')
            messages.success(request,"Account was created for "+user)
            return redirect("login_page")

    context = {"logo":logo,"logo2":logo2,"customer_wishlist":customer_wishlist,"customer":customer,"order":order,"form":form}
    return render(request,"registration/register.html",context)

def logoutUser(request):
    logout(request)
    return redirect('login_page')

def superUserPage(request):
    logo = Additional.objects.get(name="logo")
    logo2 = Additional.objects.get(name="logo2")
    setOrderStatusForm = SetOrderStatus()

    if request.user.is_superuser:
        setOrderStatusForm = SetOrderStatus(request.POST)
        if setOrderStatusForm.is_valid():
            if request.POST.get("setOrderStatusBtn"):
                orderId = request.POST.get("setOrderStatusBtn")

                orderStatus = setOrderStatusForm.cleaned_data["status"]
                orderToChange = Order.objects.get(id=orderId)
                orderToChange.status = OrderStatus.objects.get(name=orderStatus)
                orderToChange.save()
            

    orderToBeReviewed = Order.objects.filter(current=False)

    context = {"logo":logo,"logo2":logo2,"orderToBeReviewed":orderToBeReviewed,"setOrderStatusForm":setOrderStatusForm,}
    return render(request,"admin/super_user_page.html",context)

def updateItem(request):

    # HOME - ADD TO WISHLIST
    #Get the data from JS
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print(productId, action)
    
    # Get the customer and order
    customer = request.user.customer
    product = Products.objects.get(id=productId)
    # order, created = Order.objects.get_or_create(customer=customer, complete=False) #if add to cart
    wishlist, created = Wishlist.objects.get_or_create(customer=customer, product=product)
    if action == "add":
        print("added")
        wishlist.save()
    elif action == "remove":
        wishlist.delete()
        # product.inWishlist = False
        # product.save()
        
    return JsonResponse('Item was added', safe=False) #We want to return a Json, not a template

def updateCart(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print(productId, action)

    customer = request.user.customer
    product = Products.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, current=True) 
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.save()
    if action == "remove":
        orderItem.delete()

    return JsonResponse('Cart was updated', safe=False) 

# CART - UPDATE CART QUANTITY
def updateCartQuantity(request):
    customer = request.user.customer
    data = json.loads(request.body)
    itemId = data['itemId']
    sideAction = data['sideAction']
    item = OrderItem.objects.get(id=itemId)
    print(item)

    if sideAction == "add":
        item.quantity += 1
        item.save()
    if sideAction == "remove":
        item.quantity -= 1
        item.save()

    return JsonResponse('Cart quantity was updated', safe=False) 


def removeFromCartWishlist(request):
    customer = request.user.customer
    
    
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print(productId, action)

    thisProduct = Products.objects.get(id=productId)

    if action == "cart_remove":
        order, created = Order.objects.get_or_create(customer=customer, current=True)
        item = OrderItem.objects.filter(order=order,product=thisProduct)
        item.delete()
    
    if action == "wishlist_remove":
        wishlist = Wishlist.objects.get(product=thisProduct)
        wishlist.delete()

    return JsonResponse('Remove', safe=False) 

# PAYMENT METHOD
def paymentMethod(request):
    customer = request.user.customer
    data = json.loads(request.body)
    paymentMethod = data['paymentMethod']
    
    order = Order.objects.get(customer=customer, current=True)
    order.payment_method = paymentMethod
    print(order.payment_method)
    order.save()

    return JsonResponse('Payment method', safe=False)

def confirmOrder(request):
    customer = request.user.customer
    data = json.loads(request.body)
    status = data['status']
    order = Order.objects.get(customer=customer, current=True)
    order.status = OrderStatus.objects.get(name=status)
    order.save()

    items = order.orderitem_set.all()
    for item in items:
            print(item.product.remove_stock(item.quantity))
            item.product.save()

    return JsonResponse("confirm order", safe=False)

def load_cities(request):
    if request.method == 'GET':
        province_id = request.GET.get('province')
        cities = City.objects.filter(province_id=province_id)
        return render(request,"additional/city_options.html", {"cities":cities,})




