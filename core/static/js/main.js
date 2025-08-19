document.addEventListener('DOMContentLoaded', function() {
  // Mobile menu toggle
  const menuToggle = document.querySelector('.mobile-menu-toggle');
  const mainNav = document.querySelector('.main-nav');
  
  menuToggle.addEventListener('click', function() {
    mainNav.classList.toggle('active');
  });
  
  // Close notifications
  const closeButtons = document.querySelectorAll('.close-notification');
  closeButtons.forEach(button => {
    button.addEventListener('click', function() {
      this.parentElement.style.display = 'none';
    });
  });
  
  // Navbar scroll effect
  window.addEventListener('scroll', function() {
    const header = document.querySelector('.main-header');
    if (window.scrollY > 50) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  });
  
  // Close mobile menu when clicking a link
  const navLinks = document.querySelectorAll('.nav-link');
  navLinks.forEach(link => {
    link.addEventListener('click', function() {
      if (mainNav.classList.contains('active')) {
        mainNav.classList.remove('active');
      }
    });
  });
});

// Mobile dropdown toggle
document.querySelector('.dropdown-toggle').addEventListener('click', function() {
  this.parentElement.classList.toggle('active');
});

// Animate on scroll
function animateOnScroll() {
  const elements = document.querySelectorAll('.animate-on-scroll');
  elements.forEach(element => {
    const elementPosition = element.getBoundingClientRect().top;
    const screenPosition = window.innerHeight / 1.2;
    
    if(elementPosition < screenPosition) {
      element.classList.add('animated');
    }
  });
}

window.addEventListener('scroll', animateOnScroll);
animateOnScroll(); // Run once on page load

// For dynamic loading of reviews
document.addEventListener('DOMContentLoaded', function() {
  // You can fetch reviews from an API here
  // fetch('/api/reviews')
  //   .then(response => response.json())
  //   .then(data => populateReviews(data));
  
  // Example of review carousel functionality
  const reviewCards = document.querySelectorAll('.review-card');
  
  reviewCards.forEach(card => {
    card.addEventListener('mouseenter', () => {
      card.style.transform = 'translateY(-5px)';
    });
    
    card.addEventListener('mouseleave', () => {
      card.style.transform = 'translateY(0)';
    });
  });
});

// Add this JavaScript for enhanced interactions
document.addEventListener('DOMContentLoaded', function() {
  const select = document.querySelector('.modern-select');
  const selectWrapper = document.querySelector('.select-wrapper');
  
  // Add ripple effect on click
  select.addEventListener('click', function(e) {
    const rect = select.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    const ripple = document.createElement('span');
    ripple.classList.add('ripple-effect');
    ripple.style.left = `${x}px`;
    ripple.style.top = `${y}px`;
    selectWrapper.appendChild(ripple);
    
    setTimeout(() => {
      ripple.remove();
    }, 600);
  });
  
  // Add focus/blur effects
  select.addEventListener('focus', function() {
    selectWrapper.style.transform = 'translateY(-3px)';
  });
  
  select.addEventListener('blur', function() {
    selectWrapper.style.transform = 'translateY(0)';
  });
});

document.addEventListener('DOMContentLoaded', function() {
  // Avatar preview functionality
  const avatarInput = document.getElementById('id_avatar');
  const avatarPreview = document.getElementById('avatar-preview');
  
  if (avatarInput && avatarPreview) {
    avatarInput.addEventListener('change', function(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
          if (avatarPreview.tagName === 'IMG') {
            avatarPreview.src = e.target.result;
          } else {
            // Replace placeholder with image
            const newAvatar = document.createElement('img');
            newAvatar.src = e.target.result;
            newAvatar.className = 'profile-avatar';
            newAvatar.id = 'avatar-preview';
            avatarPreview.parentNode.replaceChild(newAvatar, avatarPreview);
          }
        }
        reader.readAsDataURL(file);
      }
    });
  }

  // Add focus effects to form inputs
  const inputs = document.querySelectorAll('.form-group input, .form-group textarea, .form-group select');
  inputs.forEach(input => {
    input.addEventListener('focus', function() {
      this.parentNode.querySelector('label').style.color = '#6366f1';
    });
    
    input.addEventListener('blur', function() {
      this.parentNode.querySelector('label').style.color = '#4b5563';
    });
  });
});

document.addEventListener('DOMContentLoaded', function() {
  // Quantity controls
  document.querySelectorAll('.quantity-btn').forEach(button => {
    button.addEventListener('click', function() {
      const action = this.getAttribute('data-action');
      const itemElement = this.closest('.cart-item');
      const quantityElement = itemElement.querySelector('.quantity');
      let quantity = parseInt(quantityElement.textContent);
      
      if (action === 'increase') {
        quantity += 1;
      } else if (action === 'decrease' && quantity > 1) {
        quantity -= 1;
      }
      
      // Update UI immediately
      quantityElement.textContent = quantity;
      
      // Here you would typically make an AJAX call to update the server
      // updateCartItem(itemElement.dataset.itemId, quantity);
    });
  });
  
  // Remove item functionality
  document.querySelectorAll('.remove-item').forEach(button => {
    button.addEventListener('click', function() {
      const itemElement = this.closest('.cart-item');
      itemElement.classList.add('removing');
      
      // Wait for animation to complete before removing
      setTimeout(() => {
        // Here you would typically make an AJAX call to remove from server
        // removeCartItem(itemElement.dataset.itemId);
        
        itemElement.remove();
        updateCartCount();
      }, 300);
    });
  });
  
  function updateCartCount() {
    const countElement = document.querySelector('.cart-count');
    if (countElement) {
      const currentCount = parseInt(countElement.textContent.split(' ')[0]);
      const newCount = currentCount - 1;
      countElement.textContent = newCount + (newCount === 1 ? ' item' : ' items');
    }
  }
  
  // Add ripple effect to checkout button
  const checkoutBtn = document.querySelector('.checkout-btn');
  if (checkoutBtn) {
    checkoutBtn.addEventListener('click', function(e) {
      e.preventDefault();
      
      // Create ripple element
      const ripple = document.createElement('span');
      ripple.classList.add('ripple-effect');
      
      // Position ripple
      const rect = this.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      ripple.style.left = `${x}px`;
      ripple.style.top = `${y}px`;
      
      this.appendChild(ripple);
      
      // Remove ripple after animation
      setTimeout(() => {
        ripple.remove();
        // Proceed to checkout after animation
        window.location.href = this.href;
      }, 600);
    });
  }
});

// Form Validation
document.getElementById('contactForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Get form values
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;
    
    // Simple validation
    if (name === '' || email === '' || message === '') {
        alert('Please fill in all fields');
        return;
    }
    
    // Submit form (replace with AJAX in production)
    alert('Thank you for your message! We will get back to you soon.');
    this.reset();
});

// Animation on scroll
AOS.init({
    duration: 800,
    easing: 'ease-in-out',
    once: true
});


