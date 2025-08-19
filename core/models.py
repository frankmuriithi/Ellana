from django.conf import settings
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator

User = settings.AUTH_USER_MODEL  # 'auth.User' by default


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    is_seller = models.BooleanField(default=False)  # single seller flag
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    color = models.CharField(max_length=20, default='blue')  # for category color coding
    featured = models.BooleanField(default=False)  # for featured categories

    def __str__(self):
        return self.name


class Outfit(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    designer = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='outfits')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # optional thumbnail
    image = models.ImageField(upload_to='outfits/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    #Comparison-related fields
    brand = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    size = models.CharField(max_length=20, blank=True, null=True)
    material = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('outfit_detail', args=[str(self.pk)])


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    outfit = models.ForeignKey('Outfit', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'outfit')  # Prevents duplicate items
        verbose_name = "Shopping Cart Item"
        verbose_name_plural = "Shopping Cart Items"

    def __str__(self):
        return f"{self.quantity}x {self.outfit.name} in {self.user}'s cart"

    @property
    def total_price(self):
        return self.outfit.price * self.quantity

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    outfit = models.ForeignKey('Outfit', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'outfit')  # Prevents duplicates
        verbose_name = "Wishlist Item"
        verbose_name_plural = "Wishlist Items"

    def __str__(self):
        return f"{self.outfit.name} in {self.user}'s wishlist"

class Compare(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    outfit = models.ForeignKey('Outfit', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'outfit')  # Prevents duplicates
        verbose_name = "Comparison Item"
        verbose_name_plural = "Comparison Items"

    def __str__(self):
        return f"{self.outfit.name} in {self.user}'s compare list"

    @classmethod
    def get_count_for_user(cls, user):
        return cls.objects.filter(user=user).count()

class OutfitImage(models.Model):
    outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='outfits/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.outfit.name} image"


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    customer = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=50, default='mpesa')

    def __str__(self):
        return f"Order #{self.pk} - {self.customer.user.username if self.customer else 'Unknown'}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    outfit = models.ForeignKey(Outfit, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # price at time of order

    def __str__(self):
        return f"{self.outfit} x {self.quantity}"


class Review(models.Model):
    outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.outfit} by {self.reviewer.user.username if self.reviewer else 'Anon'}"


class Notification(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notif to {self.user.user.username}: {self.message}"


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='sent_messages')
    receiver = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='received_messages')
    subject = models.CharField(max_length=200, blank=True)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.user.username if self.sender else 'Unknown'} to {self.receiver.user.username if self.receiver else 'Unknown'}"
