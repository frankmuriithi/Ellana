from django.urls import path
from . import views
from .views import CategoryListView, CategoryDetailView, add_to_cart, toggle_wishlist, add_to_compare, ReviewCreateView, OutfitReviewsView


urlpatterns = [
    # Home / Outfit
    path('', views.OutfitListView.as_view(), name='outfit_list'),
    path('outfit/<int:pk>/', views.OutfitDetailView.as_view(), name='outfit_detail'),
    path('outfit/add/', views.OutfitCreateView.as_view(), name='add_outfit'),
    path('outfit/<int:pk>/edit/', views.OutfitUpdateView.as_view(), name='edit_outfit'),
    path('outfit/<int:pk>/delete/', views.OutfitDeleteView.as_view(), name='delete_outfit'),

    # Auth
    path('login/', views.user_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('signup/', views.user_signup, name='signup'),

    # Profile
    path('profile/', views.ProfileView.as_view(), name='profile'),

    # Categories
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),

    # Cart & Orders
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:outfit_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='cart_detail'),   # Your cart page
    path('checkout/', views.checkout, name='checkout'),     # Checkout logic
    path("order/<int:order_id>/", views.order_detail, name="order_detail"),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),


    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path("cart/remove/<int:item_id>/", views.remove_cart_item, name="remove_cart_item"),
    path("cart/increase/<int:item_id>/", views.increase_cart_item, name="increase_cart_item"),
    path("cart/decrease/<int:item_id>/", views.decrease_cart_item, name="decrease_cart_item"),
    path('toggle-wishlist/', views.toggle_wishlist, name='toggle_wishlist'),
    path('add-to-compare/', views.add_to_compare, name='add_to_compare'),
    path('compare/', views.Compare_page, name='compare'),
    path('wishlist/', views.Wishlist_page, name='wishlist'),
    path("compare/add/<int:outfit_id>/", views.add_to_compare, name="add_to_compare"),
    path("wishlist/remove/<int:outfit_id>/", views.remove_from_wishlist, name="remove_from_wishlist"),
    path("remove-from-compare/", views.remove_from_compare, name="remove_from_compare"),




    # Reviews
    path('outfit/<int:outfit_id>/reviews/', views.OutfitReviewsView.as_view(), 
         name='outfit_reviews'),
    path('outfit/<int:outfit_id>/review/create/', views.ReviewCreateView.as_view(), 
         name='create_review'),
         
         
    # Notifications
    path('notifications/', views.NotificationListView.as_view(), name='notifications'),

    # Messages
    path('messages/new/', views.MessageCreateView.as_view(), name='send_message'),
    path('messages/inbox/', views.InboxView.as_view(), name='inbox'),

     # About Us
     path('about/', views.about_view, name='about'),

     # Contact Us
     path('contact/', views.contact_view, name='contact'),

     # FAQs
     path('faqs/', views.faqs, name='faqs'),

     #Shipping policy
     path('shipping/', views.shipping, name='shipping'),

     #Returns policy
     path('returns/', views.returns, name='returns'),

     #Terms and Conditions
     path('terms/', views.terms, name='terms'),
     #Privacy Policy
     path('privacy/', views.privacy, name='privacy'),

]


