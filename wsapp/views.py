from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from wsapp.models import Article, Product, Type, Subtype, DetailOrder, Order, Review


def nav():
    list_types = []
    types = Type.objects.all().prefetch_related('subtype_set')
    for type in types:
        object_type = {}
        object_type['id'] = type.id
        object_type['title_t'] = type.title_t

        object_type['list_subtypes'] = type.subtype_set.all().values('id', 'title_subt')

        list_types.append(object_type)
    return list_types


def index(request):
    if request.method == 'POST':
        if 'product' in request.POST.keys():
            id_product = request.POST['product']
            person = auth.get_user(request)
            add_to_cart(person, id_product)
    template = 'index.html'
    list_articles = []
    articles = Article.objects.all().prefetch_related('products').order_by('-published_at')#.values()
    for article in articles:
        object_article = {}
        object_article['title_a'] = article.title_a
        object_article['description_a'] = article.description_a

        object_article['products'] = article.products.all().order_by('-amount_pr').values('id', 'title_pr', 'description_pr', 'amount_pr', 'image')

        list_articles.append(object_article)
    context = {
        'list_articles': list_articles,
        'list_types': nav()
    }

    return render(request, template, context)


def cart(request):
    template = 'cart.html'
    person = auth.get_user(request)
    if request.method == 'POST':
        new_order = Order.objects.create(status='оформлен')
        DetailOrder.objects.filter(person=person, order__isnull=True).update(order=new_order)

    products_in_cart = DetailOrder.objects.filter(person=person, order__isnull=True).prefetch_related('product').values('amount_do', 'product__id', 'product__title_pr', 'product__description_pr', 'product__amount_pr', 'product__image')

    context = {
        'products_in_cart': products_in_cart,
        'count': products_in_cart.count(),
        'list_types': nav()
    }
    return render(request, template, context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return redirect('index')
    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return render(request, 'index.html')


def add_to_cart(person, id_product):
    prod = Product.objects.get(id=id_product)
    count_products_in_cart = DetailOrder.objects.filter(product=prod, person=person, order__isnull=True).count()
    if count_products_in_cart == 0:
        DetailOrder.objects.create(amount_do=1, product=prod, person=person)


def add_feedback(person, id_product, mark, description):
    print(id_product)
    prod = Product.objects.get(id=id_product)
    print(person)
    product_has_order = DetailOrder.objects.filter(product=prod, person=person, order__isnull=False).count()
    if product_has_order != 0:
        Review.objects.create(mark=int(mark), review=description, product=prod, person=person)


def product(request, id_product):
    person = auth.get_user(request)
    if request.method == 'POST':
        if 'feedback' in request.POST.keys() and 'mark' in request.POST.keys():
            id_product = request.POST['feedback']
            mark = request.POST['mark']
            description = request.POST['description']
            add_feedback(person, id_product, mark, description)
        if 'product' in request.POST.keys():
            id_product = request.POST['product']
            add_to_cart(person, id_product)

    template = 'product_det.html'
    prod = Product.objects.get(id=id_product)
    reviews = Review.objects.filter(product=prod).select_related('person').values('mark', 'review', 'person__username')
    context = {
        'product': prod,
        'reviews': reviews,
        'list_types': nav()
    }
    return render(request, template, context)


def products(request, id_type, id_subtype):
    if request.method == 'POST':
        if 'product' in request.POST.keys():
            id_product = request.POST['product']
            person = auth.get_user(request)
            add_to_cart(person, id_product)

    template = 'products.html'
    type = get_object_or_404(Type, id=id_type)
    if id_subtype != 0:
        subtype = get_object_or_404(Subtype, id=id_subtype)
        prods = Product.objects.filter(subtype=id_subtype).values('id', 'title_pr', 'description_pr', 'amount_pr', 'image')
        title = subtype.title_subt
    else:
        prods = Product.objects.filter(type=id_type).values('id', 'title_pr', 'description_pr', 'amount_pr', 'image')
        title = type.title_t

    context = {
        'products': prods,
        'title': title,
        'list_types': nav()
    }
    return render(request, template, context)

