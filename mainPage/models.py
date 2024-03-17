from django.db import models
from django.contrib.auth.models import User
# from .shipping import *

class Additional(models.Model):
    name = models.CharField(max_length=200)
    img = models.ImageField(null=True, blank=True, upload_to="images/") 

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True) #null and true so that you don't get errors when changing the models
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    # Purchase and Transaction history (?) => From OrderItem then convert to

    @property
    def wishlist_length(self):
        customer_wishlist = self.wishlist_set.all()
        return len(customer_wishlist)

    def __str__(self):
        return self.name

# PRODUCTS
class Products(models.Model):
    name = models.CharField(max_length=200)
    product_index = models.IntegerField(default=0)
    img = models.ImageField(null=True, blank=True, upload_to="images/")
    color_circle = models.CharField(null=True, blank=True, max_length=200) #charfield or array?
    gender = models.CharField(null=True, blank=True, max_length=200)
    price = models.IntegerField(null=True,blank=True)
    offer = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(null=True, blank=True, max_length=200)
    bio = models.CharField(null=True, blank=True, max_length=200)
    overview = models.CharField(null=True, blank=True, max_length=200)
    material = models.CharField(null=True, blank=True, max_length=200)
    type = models.CharField(null=True, blank=True, max_length=200)
    size = models.CharField(null=True, blank=True, max_length=200)
    color = models.CharField(null=True, blank=True, max_length=200)
    color_hex = models.CharField(null=True, blank=True, max_length=200)
    stock = models.IntegerField(null=True,blank=True)

    #  if we need to accept argument, it's not a property
    @property
    def is_wishlist(self): #product.wishlist
        wishlistItems = self.wishlist_set.all()

        return wishlistItems
    
    def remove_stock(self,quantity):
       self.stock = self.stock - quantity
       return self.stock
    
    def restore_stock(self,quantity):
        self.stock = self.stock + quantity
        return self.stock
    
    @property
    def set_final_star(self):
        stars = self.products_review_set.all()
        stars = list(stars)
        total_stars = 0
        count = 0
        for i in stars:
            count += 1
            total_stars += i.star
        if count != 0:
            total_stars = total_stars / count
        return total_stars
    
    @property
    def set_final_star_len(self):
        stars = self.products_review_set.all()
        stars = list(stars)
        total_stars = 0
        count = 0
        for i in stars:
            count += 1
            total_stars += i.star
        if count != 0:
            total_stars = total_stars / count
        return count


    def __str__(self):
        return self.name


# Haven't make the feature where a user can make a review on 1 product once. Add the feature manually in the templates
class Products_review(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, null=True)
    star = models.FloatField(null=True,blank=True) 
    text = models.CharField(null=True, blank=True, max_length=200)
    date = models.DateField(auto_now_add=True)
    helpful = models.IntegerField(null=True,blank=True)
    unhelpful = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return str(self.star)
        
class Products_img(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    img = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.name
    
class Products_offer(models.Model):
    product = models.OneToOneField(Products, on_delete=models.CASCADE,primary_key=True,)
    name = models.CharField(max_length=200)
    date_start = models.DateField()
    date_end = models.DateField()
    final_price = models.IntegerField(null=True,blank=True) 

    def __str__(self):
        return self.name

class OrderStatus(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# Customer ordering data
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,null=True)
    status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True, blank=True)
    # When we delete the customer, we don't want to delete the order. We just want to set the customer to null.
    date_ordered = models.DateField(auto_now_add=True) # Not like that
    complete = models.BooleanField(default=False) # payment complete
    current = models.BooleanField(default=True) # if true, we can continue adding to cart. and displayed in the checkout page
    cancel = models.BooleanField(default=False) 
    #status = models.CharField(max_length=200, default="false") #false, placed, paid
    payment_method = models.CharField(max_length=200, null=True)
    transaction_id = models.CharField(max_length=200, null=True)
    terms = models.BooleanField(default=False)
    shipping_cost = models.IntegerField(default=0) 
    delivery_time = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        if self.cancel == True:
            return str(self.id)+"_cancelled"
        return str(self.id)
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems]) #The total quantity of the cart (all OrderItems)
        return total

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_item_total for item in orderitems]) #The total price of the cart (all OrderItems)
        return total

    @property
    def calculate_subtotal(self):
        return self.get_cart_total + self.shipping_cost 
    

class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    payment_method = models.CharField(max_length=200, null=True)
    payment_timestamp = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    payment_evidence = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return str(self.order)+"_"+str(self.customer)+"_"+str(self.payment_method)+"_"+str(self.complete)

# The item within our cart
class OrderItem(models.Model):
    product= models.ForeignKey(Products, on_delete=models.SET_NULL, blank=True, null=True) #When the customer is deleted, the OrderItem remains exist. However, the customer key is null
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)    

    def __str__(self):
        return str(self.order)+"_"+str(self.product)
    
    @property
    def get_item_total(self):
        product = self.product
        if product.offer == False:
            product_price = product.price
        else: 
            product_price = product.products_offer.final_price
            
        total = product_price * self.quantity

        return total
    
    
class ShippingAddress(models.Model):
    customer = models.OneToOneField(Customer,on_delete=models.SET_NULL, blank=True, null=True)
    # order = models.OneToOneField(Order,on_delete=models.SET_NULL, blank=True, null=True)
    address= models.CharField(max_length=200, null=True)
    district = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    #province = models.CharField(choices=provinceChoiceField(), max_length=200, null=True)
    province = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    service = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.address

class Province(models.Model):
    name = models.CharField(max_length=200)
    identifier = models.IntegerField()

    def __str__(self):
        return self.name
    
class City(models.Model):
    name = models.CharField(max_length=200)
    identifier = models.IntegerField()
    province = models.ForeignKey(Province,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Wishlist(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Products,on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.product)
    
class Testimony(models.Model):
    name = models.CharField(max_length=200)
    img = models.ImageField(null=True, blank=True, upload_to="images/")
    status = models.CharField(max_length=200)
    ig_link = models.CharField(max_length=200)
    fb_link = models.CharField(max_length=200)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class FAQs(models.Model):
    subject = models.CharField(max_length=200)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.subject
    
class Identity(models.Model):
    heading = models.CharField(max_length=200)
    text = models.CharField(max_length=200)
    img = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.heading
    
class MeetTheTeam(models.Model):
    name = models.CharField(max_length=200)
    img = models.ImageField(null=True, blank=True, upload_to="images/")
    division = models.CharField(max_length=200, null=True, blank=True,)
    job_desc = models.CharField(max_length=200, null=True, blank=True,)

    def __str__(self):
        return self.name

