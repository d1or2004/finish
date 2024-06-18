from django.urls import path
from .views import RegisterView, LoginView, LogoutView, HomeView, ShopView, AboutView, ServiceView, BlogView, \
    ContactView, ShopInsert, PruductDetailView, ProductUpdateView, DeleteProductView, CardView, ChekOutPageView, \
    ThankYouPageview, CardDeleteView, CardDeleteFullView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', HomeView.as_view(), name='home'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('about/', AboutView.as_view(), name='about'),
    path('service/', ServiceView.as_view(), name='service'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('shop_insert/', ShopInsert.as_view(), name='shop-insert'),
    path('product_datail/<int:id>/', PruductDetailView.as_view(), name='product-detail'),
    path('productupdate/<int:id>/', ProductUpdateView.as_view(), name='product-update'),
    path('productdelete/<int:id>/', DeleteProductView.as_view(), name='product-delete'),
    path('card/delete/<int:id>/', CardDeleteView.as_view(), name='card-delete'),
    path('card/', CardView.as_view(), name='card'),
    path('check/', ChekOutPageView.as_view(), name='check'),
    path('card/delete/', CardDeleteFullView.as_view(), name='card-full-delete'),
    path('thnk/', ThankYouPageview.as_view(), name='thankyou'),

]
