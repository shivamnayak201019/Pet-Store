from django.shortcuts import render,redirect
from .models import pet,customer1,cart,order,payment,orderdetail
from django.views.generic import DetailView,ListView,CreateView,UpdateView,DeleteView
from django.db.models import Q
from django.contrib.auth.hashers import make_password,check_password
from datetime import date
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
class petview(ListView):
    model=pet
    template_name='petview.html'
    context_object_name='petobj'

    def get_context_data(self,**kwargs):
        data=self.request.session['sessionvalue']
        context=super().get_context_data(**kwargs)
        context['session']=data
        return context

def petviewcmfun(request,data):
    
    petdetails = pet.cpetobj.getdata(data)
    print(petdetails)
    return render(request,'PetView.html',{'petobj':petdetails})  


class login(ListView):
    model=pet
    template_name='login.html'

def search(request):
    if request.method=="POST":

        searchdata=request.POST.get('searchquery')
        petobj=pet.objects.filter(Q(name__icontains=searchdata)|Q(breed__icontains=searchdata)|Q(species__icontains=searchdata))
        return render(request,'petview.html',{'petobj':petobj})

def register(request):
    if request.method=="GET":
        return render(request,'registration.html')
    elif request.method=="POST":
        firstname=request.POST.get('fn')
        email1=request.POST.get('email')
        phoneno=request.POST.get('pn')
        password1=request.POST.get('pass')
        epassword=make_password(password1)
        custobj=customer1(name=firstname,contact=phoneno,password=epassword,email=email1)
        custobj.save()
        return redirect('../login/')


def login(request):
    if request.method=="GET":
        return render(request,'login.html')
    if request.method=='POST':
        password=request.POST.get('lpass')
        username=request.POST.get('lemail')
        print(password)
        print(username)
        cust=customer1.objects.filter(email=username)
        print(cust)
        if cust:
            custobj1=customer1.objects.get(email=username)
            print(custobj1.email)
            flag=check_password(password,custobj1.password)
            print("flag",flag)
            if flag:
                request.session['sessionvalue']=custobj1.email
                print("inside flag")
                return redirect('../petview')
            else:
                return render(request,'login.html',{'msg':'incorrect email or passward'})
        else:
            return render(request,'login.html',{'msg':'incorrect email or passward'})
            



class detailtask(DetailView):
    model=pet
    template_name='taskdetail.html'
    context_object_name='i'


def addtocart(request):
    productid=request.POST.get('productid')
    print(productid)
    custsession=request.session['sessionvalue']
    custobj=customer1.objects.get(email=custsession)
    pobj=pet.objects.get(id=productid)

    flag=cart.objects.filter(cid=custobj.id,Pid=pobj.id)
    if flag:
        cartobj=cart.objects.get(cid=custobj.id,Pid=pobj.id)
        cartobj.quantity=cartobj.quantity+1
        cartobj.totalamount=pobj.price*cartobj.quantity
        cartobj.save()
    else:
        cartobj=cart(cid=custobj,Pid=pobj,quantity=1,totalamount=pobj.price*1)
        cartobj.save()

    return redirect('../petview')

def viewcart(request):
    custsession=request.session['sessionvalue']
    custobj=customer1.objects.get(email=custsession)
    cartobj=cart.objects.filter(cid=custobj.id)
    return render(request,'cart.html',{'cartobj':cartobj})

def cq(request):
    cemail=request.session['sessionvalue']
    pid=request.POST.get('pid')
    custobj=customer1.objects.get(email=cemail)
    pobj=pet.objects.get(id=pid)    
    cartobj=cart.objects.get(cid=custobj.id,Pid=pobj.id)

    if request.POST.get('cqbtn')=="+":
        cartobj.quantity=cartobj.quantity+1
        cartobj.totalamount=cartobj.quantity*pobj.price
        cartobj.save()
    elif request.POST.get('cqbtn')=="-":
        if cartobj.quantity==1:
            cartobj.delete()
        else:
            cartobj.quantity=cartobj.quantity-1
            cartobj.totalamount=cartobj.quantity*pobj.price
            print(cartobj.totalamount)
            cartobj.save()

    return redirect('../viewcart')


def summary(request):
    cemail=request.session['sessionvalue']
    custobj=customer1.objects.get(email=cemail)
    cartobj=cart.objects.filter(cid=custobj.id)
    totalbill=0
    totaldogs=0
    
    for i in cartobj:
        totalbill+=i.totalamount
        totaldogs+=i.quantity
    return render(request,"summary.html",{'cartobj':cartobj,'totalbill':totalbill,'totaldogs':totaldogs})

    
def placeorder(request):
    fn=request.POST.get('fn')
    ln=request.POST.get('ln')
    address=request.POST.get('address')
    city=request.POST.get('city')
    state=request.POST.get('state')
    pincode=request.POST.get('pincode')
    phoneno=request.POST.get('phoneno')

    datetimev=date.today()
    orderobj=order(firstname=fn,lastname=ln,address=address,city=city,state=state,pincode=pincode,phoneno=phoneno,orderdate=datetimev,orderstatus="pending")
    orderobj.save()

    ono=str(orderobj.id)+str(datetimev).replace('-','')
    orderobj.ordernumber=ono
    orderobj.save()
    custsession=request.session['sessionvalue']
    custobj=customer1.objects.get(email=custsession)
    cartobj=cart.objects.filter(cid=custobj.id)
    totalbill=0

    # ==================================razor pay================
    for i in cartobj:
        totalbill+=i.totalamount
    razorpay_client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
 
 

    currency = 'INR'
    amount = 20000  # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = '../petview'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZORPAY_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url

    # ============================================end===========================

    from django.core.mail import EmailMessage

    sm=EmailMessage('order places','order placed from petstore application. total bill for your order is'+str(totalbill),to=['nayakshivam1@gmail.com'])
    sm.send()
    return render(request,"payment.html",{'orderobj':orderobj,'session':custsession,'cartobj':cartobj,'totalbill':totalbill,'context':context})

def paymentsuccess(request):
        odata= request.GET.get('order_id')
        print(odata)
        data = request.GET.get('payment_id')
        print(data)
        print(request.GET.get('session'))
        request.session['sessionvalue']=request.GET.get('session')
        em=request.session['sessionvalue']
        # em=request.GET.get('sessionname')
        custobj=customer1.objects.get(email=em)
        cartobj=cart.objects.filter(cid=custobj.id)
        orderobj=order.objects.get(ordernumber=odata)
        paymentobj=payment(customerid=custobj,oid=orderobj,paymentstatus="paid",transactionid=data,paymentmode='paypal')
        paymentobj.save()
        for i in cartobj:
            orderdetailobj=orderdetail(ordernumber=odata,customerid=custobj,productid=i.Pid,quantity=i.quantity,totalprice=i.totalamount,paymentid=paymentobj)
            orderdetailobj.save()
            i.delete()
        

        return render(request,'paymentsuccess.html',{'em':em,'paymentobj':paymentobj})

def logout(request):
    del request.session['sessionvalue']
    return redirect('../login/')

        




    




    








