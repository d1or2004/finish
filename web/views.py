from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import UserMadel, Product, RecentBlogModel, Testimonial, TeamModel, ContactModel, Subscribe, Cart
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout


class RegisterView(View):
    def get(self, request):
        return render(request, 'auth/register.html')

    def post(self, request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password_1 = request.POST['password_1']
        password_2 = request.POST['password_2']
        if password_1 == password_2:
            user = User(first_name=first_name, last_name=last_name, email=email, username=username)
            user.set_password(password_1)
            user.save()
            return redirect('login')
        else:
            return render(request, 'auth/register.html')


class LoginView(View):
    def get(self, request):
        form = UserMadel()
        context = {'form': form}
        return render(request, 'auth/login.html', context)

    def post(self, request):
        username = request.POST['username']
        password_1 = request.POST['password_1']

        data = {
            'username': username,
            'password': password_1
        }

        login_form = AuthenticationForm(data=data)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('home')

        else:
            form = UserMadel()
            context = {'form': form}
            return render(request, 'auth/login.html', context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class HomeView(View):
    def get(self, request):
        products = Product.objects.all()
        recents = RecentBlogModel.objects.all()
        testimonials = Testimonial.objects.all()
        context = {
            "products": products,
            "recents": recents,
            "testimonials": testimonials
        }
        return render(request, "web/index.html", context)

    def post(self, request):
        a = request.POST['cart']
        if a == 'card':
            name = request.POST['name']
            email = request.POST['email']
            subscribe = Subscribe(name=name, email=email)
            subscribe.save()
            return redirect('home')
        else:
            title = request.POST['product_name']
            user = request.POST['username']
            product = Product.objects.get(product_name=title)
            user = User.objects.get(username=user)
            corzina = Cart.objects.create(title=product, user=user)
            corzina.save()
            return redirect('card')


class ShopView(View):
    def get(self, request):
        search = request.GET.get('search')
        if not search:
            products = Product.objects.all()
            context = {'products': products}
            print(products)
            return render(request, 'web/shop.html', context)
        else:
            products = Product.objects.filter(product_name__icontains=search)
            if products:
                context = {'products': products}
                print("________________________________")
                print(products)
                return render(request, 'web/shop.html', context)
            else:
                context = {'products': products}
                return render(request, 'web/shop.html', context)

    def post(self, request):
        name = request.POST['name']
        email = request.POST['email']
        subscribe = Subscribe(name=name, email=email)
        subscribe.save()
        return redirect('shop')


class AboutView(View):
    def get(self, request):
        testimonials = Testimonial.objects.all()
        teams = TeamModel.objects.all()
        context = {
            "teams": teams,
            "testimonials": testimonials
        }
        return render(request, "web/about.html", context)

    def post(self, request):
        name = request.POST['name']
        email = request.POST['email']
        subscribe = Subscribe(name=name, email=email)
        subscribe.save()
        return redirect('about')


class ServiceView(View):
    def get(self, request):
        testimonials = Testimonial.objects.all()
        products = Product.objects.all()
        context = {
            "products": products,
            "testimonials": testimonials
        }
        return render(request, "web/services.html", context)

    def post(self, request):
        name = request.POST['name']
        email = request.POST['email']
        subscribe = Subscribe(name=name, email=email)
        subscribe.save()
        return redirect('service')


class BlogView(View):
    def get(self, request):
        testimonials = Testimonial.objects.all()
        recents = RecentBlogModel.objects.all()
        context = {
            "recents": recents,
            "testimonials": testimonials
        }
        return render(request, "web/blog.html", context)

    def post(self, request):
        name = request.POST['name']
        email = request.POST['email']
        subscribe = Subscribe(name=name, email=email)
        subscribe.save()
        return redirect('blog')


class ContactView(View):
    def get(self, request):
        return render(request, "web/contact.html")

    def post(self, request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        message = request.POST['message']
        contact = ContactModel(first_name=first_name, last_name=last_name, email=email, message=message)
        contact.save()
        return redirect('contact')


class ShopInsert(View):
    def get(self, request):
        return render(request, "web/shop_insert.html")

    def post(self, request):
        product_name = request.POST['product_name']
        image = request.POST['image']
        price = request.POST['price']
        description = request.POST['description']
        category_code = request.POST['category_code']
        category_name = request.POST['category_name']
        subcategory_code = request.POST['subcategory_code']
        subcategory_name = request.POST['subcategory_name']
        new_product = Product(product_name=product_name, image=f"media/product/{image}", price=price,
                              description=description,
                              category_code=category_code, category_name=category_name,
                              subcategory_code=subcategory_code, subcategory_name=subcategory_name
                              )
        new_product.save()
        return redirect('shop')


class PruductDetailView(View):
    def get(self, request, id):
        product = Product.objects.get(id=id)
        return render(request, "web/product_detail.html", context={"product": product})


class ProductUpdateView(View):
    def get(self, request, id):
        product = Product.objects.get(id=id)
        return render(request, "web/product_update.html", context={"product": product})

    def post(self, request, id):
        product = Product.objects.get(id=id)
        name = request.POST['product_name']
        new_image = request.POST['image']
        new_price = request.POST['price']
        new_description = request.POST['description']
        new_category_code = request.POST['category_code']
        new_category_name = request.POST['category_name']
        new_subcategory_code = request.POST['subcategory_code']
        new_subcategory_name = request.POST['subcategory_name']

        product.product_name = name
        product.image = new_image
        product.price = new_price
        product.description = new_description
        product.category_code = new_category_code
        product.category_name = new_category_name
        product.subcategory_code = new_subcategory_code
        product.subcategory_name = new_subcategory_name
        product.save()
        return redirect("shop")


class DeleteProductView(View):
    def get(self, request, id):
        product = Product.objects.get(id=id)
        product.delete()
        return redirect('shop')


class CardDeleteView(LoginRequiredMixin, View):
    def get(self, request, id):
        card_item = get_object_or_404(Cart, id=id, user=request.user)
        card_item.delete()
        return redirect('card')


class CardDeleteFullView(LoginRequiredMixin, View):
    def get(self, request):
        Cart.objects.filter(user=request.user).delete()
        return redirect('card')


class CardView(LoginRequiredMixin, View):
    def get(self, request):
        username = request.user.username
        user = User.objects.get(username=username)
        user_card = Cart.objects.filter(user=user)
        total_price = 0
        for i in user_card:
            if i.title.price:
                total_price += i.title.price
        context = {
            "user_card": user_card,
            "total_price": total_price
        }
        return render(request, "web/cart.html", context)


class ChekOutPageView(LoginRequiredMixin, View):
    def get(self, request):
        username = request.user.username
        user = User.objects.get(username=username)
        user_cart = Cart.objects.filter(user=user)

        # obshiy narxni korish uchun
        total_price = 0
        for item in user_cart:
            total_price += item.title.price

        context = {
            "user_cart": user_cart,
            'total_price': total_price,
        }
        return render(request, 'web/checkout.html', context)


class ThankYouPageview(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'web/thankyou.html')
