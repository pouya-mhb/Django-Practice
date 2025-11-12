from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category, Order, OrderItem
from .cart import Cart


def home(request):
    return render(request, "shop/home.html")


def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(
        request,
        "shop/product_list.html",
        {"products": products, "categories": categories},
    )


def product_detail(request, slug):
    product = get_object_or_404(
        Product,
        slug=slug,
    )
    return render(request, "shop/product_detail.html", {"product": product})


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    # Check stock before adding
    if product.stock <= 0:
        messages.error(request, f"Sorry, {product.name} is out of stock.")
        return redirect("shop:product_detail", slug=product.slug)

    # Add product to cart
    cart.add(product=product, quantity=1)

    # Decrease stock
    product.stock -= 1
    product.save()

    messages.success(request, f"Added {product.name} to your cart.")
    return redirect("shop:cart_detail")


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    # Before removing, find how many of this product are in cart
    quantity_in_cart = cart.cart.get(str(product_id), {}).get("quantity", 0)

    # Remove item from cart
    cart.remove(product)

    # Increase stock back
    if quantity_in_cart > 0:
        product.stock += quantity_in_cart
        product.save()

    messages.warning(request, f"Removed {product.name} from your cart.")
    return redirect("shop:cart_detail")


def cart_detail(request):
    cart = Cart(request)
    return render(request, "shop/cart_detail.html", {"cart": cart})


@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.error(request, "Your cart is empty.")
        return redirect("shop:product_list")

    order = Order.objects.create(user=request.user)
    for item in cart:
        OrderItem.objects.create(
            order=order,
            product=item["product"],
            price=item["price"],
            quantity=item["quantity"],
        )
    cart.clear()
    messages.success(request, f"Order #{order.id} placed successfully!")
    return redirect("dashboard")


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.all()
    total_price = order.get_total_price()

    context = {
        "order": order,
        "items": items,
        "total_price": total_price,
    }
    return render(request, "shop/order_detail.html", context)


def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == "POST":
        if "success" in request.POST:
            order.paid = True
            order.save()
            messages.success(request, f"Payment successful for Order #{order.id}")
            return redirect("dashboard")
        elif "fail" in request.POST:
            order.paid = False
            order.save()
            messages.error(request, f"Payment failed for Order #{order.id}")
            return redirect("dashboard")

    return render(request, "shop/payment.html", {"order": order})
