from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, Func, Value, ExpressionWrapper, DecimalField
from django.db.models.aggregates import Count, Max, Min, Avg
from django.db.models.functions import Concat

from store.models import Collection, Product, OrderItem, Order, Customer


# Create your views here.


def hello_world(request):
    query_set = Product.objects.all()
    # Note data is not actually in query_set
    # query_set is only populated after iterating over it or accessing it in some way
    # this is useful so we can build more complex queries and then
    # run the final query by iterating/accessing the query_set
    for product in query_set:
        print(product)

    # the query below applies two filters in succesion then orders by...
    # to access the final data just iterate over or access it like query_set[0]
    query_set.filter().filter().order_by()

    # if the query is something like the aggregate count then a queryset is not
    # returned but the value itself is returned

    # the below returns an object
    # pk stands for primary key
    try:
        product = Product.objects.get(pk=1)
    except ObjectDoesNotExist:
        pass

    # A BETTER TRY...CATC?
    # this retuns None if row does not exists instead of triggering an error
    product1 = Product.objects.filter(pk=0).first()
    productExists = Product.objects.filter(pk=0).exists()
    # return HttpResponse("Hello World!")

    # MULTIPLE FILTERS
    # inventory < 10 AND price < 20
    queryset = Product.objects.filter(inventory__lt=10, unit_price__lt=30)
    queryset = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=30)
    queryset = Product.objects.filter(unit_price__range=(20,30))
    # Filter across relationships
    # find all products in collection #1
    queryset = Product.objects.filter(collection__id=1)
    queryset = Product.objects.filter(collection__id__gt=1)
    queryset = Product.objects.filter(collection__id__range=(1,2,3))
    queryset = Product.objects.filter(title__contains="coffee")
    queryset = Product.objects.filter(title__icontains="coffee") #case insensative

    queryset = Product.objects.filter(title__startswith="coffee") 

    # filter - dates
    # find all products updated in 2021
    queryset = Product.objects.filter(last_update__year=2021) 

    queryset = Product.objects.filter(description__isnull=True) 
    

    # USING THE Q OBJECT to filter with 'OR'
    # Q is short for Query, and with this class we can represent a query expression
    # inventory < 10 OR price < 20
    queryset = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))

    # same as aboove where we past kewargs directly to filter but using Q is more verbose
    queryset = Product.objects.filter(Q(inventory__lt=10) & Q(unit_price__lt=20))

    queryset = Product.objects.filter(Q(inventory__lt=10) & ~Q(unit_price__lt=20))

    # USING F class to reference fields in a query
    # eg. find products where inventory = price ... this is not relistic just an example, roll with it
    queryset = Product.objects.filter(inventory=F("unit_price"))
    # We can even access fields in a different table. Below "collection" is the table being referenced
    queryset = Product.objects.filter(inventory=F("collection__id"))

    # SORTING
    queryset = Product.objects.order_by('title')
    # sort decending by adding a minus
    queryset = Product.objects.order_by('-title')
    # sort by multiple fields
    queryset = Product.objects.order_by('unit_price', '-title')
    # sort products and pick first product
    product = Product.objects.order_by('unit_price')[0] # returns an object not a queryset
    product = Product.objects.earliest('unit_price') # sorts ascending then returns first item 
    product = Product.objects.latest('unit_price') # sorsts descending then returns first item

    # LIMITING
    queryset = Product.objects.all()[:5]
    queryset = Product.objects.all()[5:10]

    # PICK FIELDS TO BE RETURNED
    queryset = Product.objects.values('id', 'title')
    queryset = Product.objects.values('id', 'title','collection__title')

    # we can use values list to return an array of tuples instead of an array of dicts
    queryset = Product.objects.values_list('id', 'title','collection__title')

    # exercise
    # Select products that have been ordered and sort by title
    # this returns an array of dicts
    queryset = Product.objects.filter(id__in=OrderItem.objects.values('product__id').distinct().order_by('product__title')).order_by('title')

    # Get the last 5 orders with their customer and items (incl product)
    queryset = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
     

    # Aggregation
    result = Product.objects.aggregate(Count('id'), Min('unit_price'))
    # rename fieldnams with kwargs
    result = Product.objects.aggregate(count=Count('id'), min_price=Min('unit_price'), max_price=Max('unit_price'), avg_price=Avg('unit_price'))
  

    # ANNOTATIONS (i.e adding a computed field to each row)
    queryset = Customer.objects.annotate(is_new=Value(True))
    queryset = Customer.objects.annotate(new_id=F('id'))
    queryset = Customer.objects.annotate(new_id=F('id')+1) # can perform computations
    # calling built in DB functions
    queryset = Customer.objects.annotate(full_name=Func(F('first_name'), Value(' '), F('last_name'),function='CONCAT'))
    # short cut method of above by using imported Concat class
    queryset = Customer.objects.annotate(full_name=Concat('first_name', Value(' '), 'last_name'))
    # View orders each customer placed
    queryset = Customer.objects.annotate(orders_count=Count('order'))  
    # ExpressionWrapper
    discounted_price = ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField())
    queryset = Product.objects.annotate(discounted_price=discounted_price)

    # quering generic relations

    from django.contrib.contenttypes.models import ContentType
    from tags.models import TaggedItem
    # eg. find tags for a given product
    content_type = ContentType.objects.get_for_model(Product)
    # content_type is now a row from the ContentType table. Specifically the row that represents the Product model
    queryset = TaggedItem.objects. \
        select_related('tag') \
        .filter(content_type=content_type,object_id=1)
    

    # custom managers
    # create the manager next to the model in the models.py
    # in this examaple we will used Tags app
    # Instead of having noisy code as in the above when querying a generic relationship
    # we will encapsulate this in a custom manager.
    # So copy above code into its own class method in models.py
    # Then configure the TaggedItem model with this manager by 
    # adding an objects attribute and assingig it to an instance of this class
    # now use the manager to simplyfy the code above. 
    queryset = TaggedItem.objects.get_tags_for(Product,  1)

    # INSERT DATA (CREATTING OBJECTS)
    # create a collection
    collection = Collection()
    collection.title = "Video Games"
    # set featured product
    collection.featured_product = Product(pk=1)
    collection.save() # save to database

    # UPDATE the collection above. It's ID is 12
    try:
        collection = Collection.objects.get(pk=12)
        collection.title = "Games"
        collection.featured_product = None
        collection.save() # save to database
    except  ObjectDoesNotExist:
        pass

    # DELETE a row/object
    try:
        collection = Collection.objects.get(pk=12)
        collection.delete()  # delete collection with primary key =12
    except  ObjectDoesNotExist:
        pass

    # filter then delete
    Collection.objects.filter(id__gt=15).delete()

    # TRANSACTIONS
    # create an order and add an item.
    from django.db import transaction

    with transaction.atomic():
        order = Order()
        order.customer = Customer(pk=1)
        order.save()
        item = OrderItem()
        item.order = order
        item.product = Product(pk=1)
        item.quantity = 1
        item.unit_price = 10
        item.save()

    # RAW SQL QUERIES
    raw_queryset = Product.objects.raw('SELECT * FROM store_product')
    # note this queryset is not of the same type as above querysets. This is a raw queryset
    # it will not have methods like filter etc, since we are doing everything directly with sql


    # WE CAN EVEN GO FULL MONTY BY BYPASSING OUR MODELS
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM store_product')
        # cursor.callproc('get customers', [1,2,'a']) # call a stored proc



    return render(
        request, "hello_world.html", {"name": "Janus", "results": list(queryset), "raw_results": list(raw_queryset)}
    )
