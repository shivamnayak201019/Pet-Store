from django.db import models
from django.db.models import Manager


class custommanger(models.Manager):
    def getdata(self,a):
        return super().get_queryset().filter(species=a)
    


class pet(models.Model):
    gender=(("Male","male"),("Female","female"))
    image=models.ImageField(upload_to="media")
    name=models.CharField(max_length=200)
    species=models.CharField(max_length=200)
    breed=models.CharField(max_length=200)
    age=models.IntegerField()
    gender=models.CharField(max_length=200,choices=gender)
    description=models.CharField(max_length=200)
    price=models.FloatField()


    cpetobj = custommanger()
    objects = Manager()

   
    






    class Meta:
        db_table="pet"


class customer1(models.Model):
    name=models.CharField(max_length=20)
    email=models.EmailField()
    contact=models.BigIntegerField()
    password=models.CharField(max_length=200)

    class Meta:
        db_table='customer1'


class cart(models.Model):
    cid=models.ForeignKey(customer1,on_delete=models.CASCADE)
    Pid=models.ForeignKey(pet,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    totalamount=models.FloatField()

    class Meta:
        db_table='cart'

class order(models.Model):
    ordernumber=models.CharField(max_length=100)
    orderdate=models.DateField(max_length=100)
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    phoneno=models.BigIntegerField()
    address=models.CharField(max_length=200)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    pincode=models.BigIntegerField(max_length=100)
    orderstatus=models.CharField(max_length=100)


    class Meta:
        db_table='order'

class payment(models.Model):
    customerid=models.ForeignKey(customer1,on_delete=models.CASCADE)
    oid=models.ForeignKey(order,on_delete=models.CASCADE)
    paymentstatus=models.CharField(max_length=100,default='pending')
    transactionid=models.CharField(max_length=200)
    paymentmode=models.CharField(max_length=100,default='paypal')

    class Meta:
        db_table='payment'

class orderdetail(models.Model):
    ordernumber=models.CharField(max_length=100)
    customerid=models.ForeignKey(customer1,on_delete=models.CASCADE)
    productid=models.ForeignKey(pet,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    totalprice=models.IntegerField()
    paymentid=models.ForeignKey(payment,on_delete=models.CASCADE,null=True)
    created_at=models.DateField(auto_now=True)
    updated_at=models.DateField(auto_now=True)

    class Meta:
        db_table='orderdetail'


