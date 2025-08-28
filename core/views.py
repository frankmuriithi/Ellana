from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Count, Avg
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import models
from django.core.exceptions import ValidationError



from .models import Profile, Category, Outfit, OutfitImage, Order, OrderItem, Review, Notification, Message, Cart, Wishlist, Compare, Review
from .forms import SignUpForm, ProfileForm, OutfitForm, OutfitImageForm, CategoryForm, ReviewForm, MessageForm, ReviewForm


# -------------------------
# AUTH
# -------------------------
def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # No manual Profile creation — signal will handle it
            user.profile.is_seller = False
            user.profile.save()
            
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect('outfit_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful.")
            # redirect to homepage (outfit_list)
            return redirect('outfit_list')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})


def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('login')


# -------------------------
# PROFILE
# -------------------------
class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProfileForm(instance=request.user.profile)
        return render(request, 'core/profile.html', {'form': form})

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
        return render(request, 'core/profile.html', {'form': form})


# OUTFIT
# -------------------------
class OutfitListView(ListView):
    model = Outfit
    template_name = 'core/outfit_list.html'
    context_object_name = 'outfits'

    def get_queryset(self):
        return Outfit.objects.filter(is_active=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .models import Category   # import here or at the top
        context['categories'] = Category.objects.all()  # pass categories to template
        return context


  


class OutfitDetailView(DetailView):
    model = Outfit
    template_name = 'core/outfit_detail.html'
    context_object_name = 'outfit'
    


@method_decorator(login_required, name='dispatch')
class OutfitCreateView(UserPassesTestMixin, CreateView):
    model = Outfit
    form_class = OutfitForm
    template_name = 'core/add_outfit.html'
    success_url = reverse_lazy('outfit_list')

    def form_valid(self, form):
        # Assign the logged-in superuser's profile as the designer
        form.instance.designer = self.request.user.profile
        messages.success(self.request, "Outfit created successfully.")
        return super().form_valid(form)

    def test_func(self):
        # Only allow the superuser to create outfits
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "Only the seller can add outfits.")
        return redirect('outfit_list')

class OutfitUpdateView(UserPassesTestMixin, UpdateView):
    model = Outfit
    form_class = OutfitForm
    template_name = 'core/add_outfit.html'
    success_url = reverse_lazy('outfit_list')

    def test_func(self):
        outfit = self.get_object()
        # only the designer (seller) can edit
        return outfit.designer == getattr(self.request.user, 'profile', None)

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to edit this outfit.")
        return redirect('outfit_list')


class OutfitDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Outfit
    template_name = 'core/outfit_confirm_delete.html'
    success_url = reverse_lazy('outfit_list')

    def test_func(self):
        return self.request.user.is_superuser  # Only the seller (superuser) can delete outfits

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Outfit deleted successfully.")
        return super().delete(request, *args, **kwargs)


class CategoryListView(ListView):
    model = Category
    template_name = 'core/category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return Category.objects.all().prefetch_related('outfit_set')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_categories'] = Category.objects.filter(featured=True)[:3]
        return context

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'core/category_detail.html'
    context_object_name = 'category'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object
        outfits = Outfit.objects.filter(
            category=category, 
            is_active=True
        ).select_related('designer')
        
        # Add sorting functionality
        sort = self.request.GET.get('sort', 'newest')
        if sort == 'price_low':
            outfits = outfits.order_by('price')
        elif sort == 'price_high':
            outfits = outfits.order_by('-price')
        elif sort == 'popular':
            outfits = outfits.annotate(
                num_orders=Count('orderitem')
            ).order_by('-num_orders')
        else:  # newest
            outfits = outfits.order_by('-created_at')
            
        context['outfits'] = outfits
        context['sort'] = sort
        return context
    

# CART & ORDER
@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)  # Fetch items for logged-in user
    total = sum(item.total_price for item in cart_items)

    return render(request, 'core/cart.html', {
        'items': cart_items,
        'total': total
    })


@require_POST
@login_required
def add_to_cart(request, outfit_id=None):
    """
    Universal Add to Cart view:
    - Supports outfit_id from URL or POST data
    - Works for all 'Add to Cart' buttons in the project
    """
    # Get outfit_id (from URL param OR POST body)
    if outfit_id is None:
        outfit_id = request.POST.get('outfit_id')

    # Ensure we have a valid id
    if not outfit_id:
        return JsonResponse({'success': False, 'message': 'No outfit ID provided'}, status=400)

    # Get quantity, default = 1
    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        return JsonResponse({'success': False, 'message': 'Invalid quantity'}, status=400)

    if quantity < 1:
        return JsonResponse({'success': False, 'message': 'Quantity must be at least 1'}, status=400)

    # Try fetching outfit and updating cart
    try:
        outfit = Outfit.objects.get(id=outfit_id)
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            outfit=outfit,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        # total cart items (sum of quantities)
        cart_count = Cart.objects.filter(user=request.user).aggregate(
            total=models.Sum('quantity')
        )['total'] or 0

        return redirect('view_cart')

    except Outfit.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Outfit not found'}, status=404)



def remove_cart_item(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(Cart, id=item_id)
        item.delete()
        return JsonResponse({"success": True, "item_id": item_id})
    return JsonResponse({"success": False}, status=400)


@login_required
def increase_cart_item(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(Cart, id=item_id, user=request.user)
        try:
            # Optional: Add stock check if Outfit has 'stock' field
            if hasattr(item.outfit, 'stock') and item.quantity + 1 > item.outfit.stock:
                return JsonResponse({"success": False, "error": f"Only {item.outfit.stock} in stock."}, status=400)
            item.quantity += 1
            item.save()
            cart_total = sum(i.total_price for i in Cart.objects.filter(user=request.user))
            return JsonResponse({
                "success": True,
                "quantity": item.quantity,
                "subtotal": str(item.total_price),  # Fixed: Use total_price
                "cart_total": str(cart_total)
            })
        except ValidationError as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

@login_required
def decrease_cart_item(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(Cart, id=item_id, user=request.user)
        try:
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                # Optional: Delete if quantity would be 0
                item.delete()
                return JsonResponse({
                    "success": True,
                    "quantity": 0,
                    "subtotal": "0.00",
                    "cart_total": str(sum(i.total_price for i in Cart.objects.filter(user=request.user)))
                })
            cart_total = sum(i.total_price for i in Cart.objects.filter(user=request.user))
            return JsonResponse({
                "success": True,
                "quantity": item.quantity,
                "subtotal": str(item.total_price),  # Fixed: Use total_price
                "cart_total": str(cart_total)
            })
        except ValidationError as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


@require_POST
@login_required
def toggle_wishlist(request):
    outfit_id = request.POST.get('outfit_id')
    
    try:
        outfit = Outfit.objects.get(id=outfit_id)
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            outfit=outfit
        )
        
        if not created:
            wishlist_item.delete()
            return JsonResponse({
                'success': True,
                'on_wishlist': False
            })
            
        return JsonResponse({
            'success': True,
            'on_wishlist': True
        })
    except Outfit.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Outfit not found'}, status=404)


@login_required
def remove_from_wishlist(request, outfit_id):
    outfit = get_object_or_404(Outfit, id=outfit_id)
    Wishlist.objects.filter(user=request.user, outfit=outfit).delete()
    return JsonResponse({"success": True})


@require_POST
@login_required
def add_to_compare(request):
    outfit_id = request.POST.get('outfit_id')
    max_compare_items = 4

    try:
        outfit = Outfit.objects.get(id=outfit_id)
        compare_qs = Compare.objects.filter(user=request.user)
        compare_count = compare_qs.count()

        if compare_qs.filter(outfit=outfit).exists():
            compare_qs.filter(outfit=outfit).delete()
            return JsonResponse({
                'success': True,
                'message': 'Removed from compare',
                'compare_count': compare_count - 1
            })

        if compare_count >= max_compare_items:
            return JsonResponse({
                'success': False,
                'message': f'You can compare maximum {max_compare_items} items',
                'compare_count': compare_count
            })

        Compare.objects.create(user=request.user, outfit=outfit)
        return JsonResponse({
            'success': True,
            'message': 'Added to compare',
            'compare_count': compare_count + 1
        })
    except Outfit.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Outfit not found'}, status=404)



def remove_from_compare(request):
    if request.method == "POST":
        outfit_id = request.POST.get("outfit_id")
        compare_item = get_object_or_404(Compare, outfit__id=outfit_id, user=request.user)
        compare_item.delete()
        return JsonResponse({"success": True, "outfit_id": outfit_id})
    return JsonResponse({"success": False}, status=400)



def Compare_page(request):
    items = Compare.objects.filter(user=request.user)
    return render(request, 'core/compare.html', {'compare_items': items})

def Wishlist_page(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'core/wishlist.html', {'wishlist_items': items})


@login_required
def checkout(request):
    user = request.user  
    cart_items = Cart.objects.filter(user=user)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("cart_detail")

    # Calculate total
    total_amount = sum(item.outfit.price * item.quantity for item in cart_items)

    # Create order
    order = Order.objects.create(
        customer=user.profile,
        total_amount=total_amount,
        payment_method="mpesa"  # later you can let user choose
    )

    # Create OrderItems
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            outfit=item.outfit,
            quantity=item.quantity,
            price=item.outfit.price
        )

    # Clear cart
    cart_items.delete()

    messages.success(request, f"Order #{order.pk} has been placed successfully!")
    return redirect("order_detail", order_id=order.id)  # take them to order summary


@login_required
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id, customer=request.user.profile)
    return render(request, "core/order_detail.html", {"order": order})


def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "core/order_confirmation.html", {"order": order})


# -------------------------
# REVIEWS
# -------------------------
class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'core/review_form.html'

    def form_valid(self, form):
        form.instance.reviewer = self.request.user.profile
        return super().form_valid(form)


# -------------------------
# NOTIFICATIONS
# -------------------------
class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'core/notifications.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user.profile).order_by('-created_at')


# -------------------------
# MESSAGING
# -------------------------
class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'core/message_form.html'
    success_url = reverse_lazy('inbox')

    def form_valid(self, form):
        form.instance.sender = self.request.user.profile
        form.instance.sent_at = timezone.now()
        return super().form_valid(form)


class InboxView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'core/inbox.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user.profile).order_by('-sent_at')



class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'core/review_form.html'

    def form_valid(self, form):
        outfit = get_object_or_404(Outfit, pk=self.kwargs['outfit_id'])
        form.instance.reviewer = self.request.user.profile
        form.instance.outfit = outfit
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['outfit'] = get_object_or_404(Outfit, pk=self.kwargs['outfit_id'])
        return context

    def get_success_url(self):
        return reverse_lazy('outfit_detail', kwargs={'pk': self.kwargs['outfit_id']})


class OutfitReviewsView(ListView):
    model = Review
    template_name = 'core/reviews_list.html'
    context_object_name = 'reviews'
    paginate_by = 10

    def get_queryset(self):
        return Review.objects.filter(
            outfit_id=self.kwargs['outfit_id']
        ).select_related(
            'reviewer__user',
            'outfit'
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        outfit = get_object_or_404(Outfit, pk=self.kwargs['outfit_id'])
        
        reviews = self.get_queryset()
        rating_stats = reviews.aggregate(
            avg_rating=Avg('rating'),
            count=Count('id')
        )
        
        context.update({
            'outfit': outfit,
            'average_rating': rating_stats['avg_rating'] or 0,
            'review_count': rating_stats['count'],
            'rating_distribution': reviews.values('rating').annotate(count=Count('id'))
        })
        return context

def about_view(request):
    return render(request, 'core/about.html')

def contact_view(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user.profile
            message.sent_at = timezone.now()
            message.save()
            messages.success(request, "Message sent successfully.")
            return redirect('contact')
    else:
        form = MessageForm()
    return render(request, 'core/contact.html', {'form': form})    

@login_required
def faqs(request):
    return render(request, 'core/faqs.html')

@login_required
def shipping(request):
    return render(request, 'core/shipping.html')

@login_required
def returns(request):
    return render(request, 'core/returns.html')

@login_required
def terms(request):
    return render(request, 'core/terms.html')

@login_required
def privacy(request):
    return render(request, 'core/privacy.html')