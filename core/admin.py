from django.contrib import admin
from .models import (
    Profile, Category, Outfit, OutfitImage,
    Order, OrderItem, Review, Notification, Message, Cart, Wishlist, Compare
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_seller')
    list_filter = ('is_seller',)
    actions = ['make_single_seller']

    def make_single_seller(self, request, queryset):
        # ensure only one seller: if selecting more than 1, require single selection
        if queryset.count() != 1:
            self.message_user(request, "Select exactly one profile to set as the single seller.")
            return
        Profile.objects.update(is_seller=False)
        profile = queryset.first()
        profile.is_seller = True
        profile.save()
        self.message_user(request, f"{profile.user.username} is now set as the seller.")
    make_single_seller.short_description = "Set selected profile as the single seller"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Outfit)
class OutfitAdmin(admin.ModelAdmin):
    list_display = ('name', 'designer', 'price', 'is_active')
    list_filter = ('is_active', 'category')
    search_fields = ('name', 'description')



@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'outfit', 'quantity', 'added_at')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'outfit', 'added_at')

@admin.register(Compare)
class CompareAdmin(admin.ModelAdmin):
    list_display = ('user', 'outfit', 'added_at')    


admin.site.register(OutfitImage)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)
admin.site.register(Notification)
admin.site.register(Message)
