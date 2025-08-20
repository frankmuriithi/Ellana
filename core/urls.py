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
    path('order/place/', views.place_order, name='place_order'),
    path('orders/', views.OrderHistoryView.as_view(), name='order_history'),
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('toggle-wishlist/', views.toggle_wishlist, name='toggle_wishlist'),
    path('add-to-compare/', views.add_to_compare, name='add_to_compare'),
    path('compare/', views.Compare_page, name='compare'),
    path('wishlist/', views.Wishlist_page, name='wishlist'),
    path("compare/add/<int:outfit_id>/", views.add_to_compare, name="add_to_compare"),



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

]


