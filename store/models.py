from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Customer(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        if self.first_name:
            return self.first_name
        else:
            return 'no_first_name'  


class Category(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_name = models.CharField(max_length=100, null=True, blank=True)
    product_category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to='product_images', default='product.jpg')
    product_price = models.DecimalField(max_digits=7, decimal_places=2)
    product_description = models.TextField()

    def __str__(self):
        return self.product_name

    @property
    def imageURL(self):
        try:
            url = self.product_image.url
        except:
            url = ''
        return url


STATUS = (
    ('pending', 'pending'),
    ('delivered', 'delivered')
)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(choices=STATUS, max_length=10)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return total

    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, blank=True)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        price = self.quantity * self.product.product_price
        return price


class Shipping(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    zipcode = models.CharField(max_length=100, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


class Wishlist(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.customer.first_name

    @property
    def get_wishlist_total(self):
        return self.products.all().count()

    @property
    def get_wishlist_products(self):
        return self.products.all()        
    
    def check_if_product_in_wishlist(self, product):
        products = self.get_wishlist_products
        if product in products:
            return True
        else: 
            return False    

