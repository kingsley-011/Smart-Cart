from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from firebase import firebase
from .utils import *
from .models import Referrar, Payment_detail, Items
import joblib

firebase = firebase.FirebaseApplication('https://smartcart-c354c-default-rtdb.europe-west1.firebasedatabase.app/')

# Create your views here.
def home(request):
    return render(request, 'home.html')



def user_register(request):
    if request.method == "POST":
        mobile = request.POST['mobile']
        email = request.POST['email']
        photo = request.POST['photo']
        print(photo)
        user = User.objects.create_user(username=mobile, email=email, password="smartcart###1234")
        user.save()
        user_slug = gerenrate_url(user.id)
        ref_ins = Referrar.objects.create(user=user, refer_url=user_slug)
        ref_ins.save()
        login(request, user)
        return redirect('home')
    return render(request, 'user_register.html')




def refer_and_earn(request):
    context = {}
    if request.user.is_authenticated:
        user = request.user
        ref_ins = Referrar.objects.get(user = user)
        context['refer_url'] = ref_ins.refer_url
        referred_users = ref_ins.referred_user.all()
        refer_data = []
        for data in referred_users:
            mobile_ = data.username
            email_ = data.email
            refer_data.append([mobile_, email_])
        context['refer_data'] = refer_data
        return render(request, 'refer_and_earn.html', context=context)
    return render(request, 'error_handle.html')




def cart1_page(request):
    context = {}
    add_cart1_data_from_firebase = firebase.get('/cart1/add', None)
    remove_cart1_data_from_firebase = firebase.get('/cart1/remove', None)
    # print(add_cart1_data_from_firebase, remove_cart1_data_from_firebase)
    # print(len(add_cart1_data_from_firebase), len(remove_cart1_data_from_firebase))
    product_details = []
    final_invoice = get_invoice(add_cart1_data_from_firebase, remove_cart1_data_from_firebase)
    for _name, _count in final_invoice.items():
        if _count != 0:
            product_details.append((_name, _count,(random.randint(10, 40))*_count))
    total_price = sum([float(i) for _ , _ , i in product_details])
    context['total_price'] = total_price
    context['product_details'] = product_details
    return render(request, 'cart1.html', context=context)





def cart2_page(request):
    context = {}
    add_cart1_data_from_firebase = firebase.get('/cart2/add', None)
    remove_cart1_data_from_firebase = firebase.get('/cart2/remove', None)
    # print(add_cart1_data_from_firebase, remove_cart1_data_from_firebase)
    # print(len(add_cart1_data_from_firebase), len(remove_cart1_data_from_firebase))
    product_details = []
    final_invoice = get_invoice(add_cart1_data_from_firebase, remove_cart1_data_from_firebase)
    for _name, _count in final_invoice.items():
        if _count != 0:
            product_details.append((_name, _count,(random.randint(10, 40))*_count))
    total_price = sum([float(i) for _ , _ , i in product_details])
    context['total_price'] = total_price
    context['product_details'] = product_details
    return render(request, 'cart1.html', context=context)

def user_login(request):
    if request.method == "POST":
        mobile = request.POST['mobile']
        user_ins = User.objects.get(username=mobile)
        next = request.POST['next']
        login(request, user_ins)
        return HttpResponseRedirect(next)
    return render(request, 'user_login.html')

def payment(request):
    context = {}
    def convert_ipaddress(x : str) -> int:
            res = ''
            for i in x:
                if i.isdigit():
                    res += i
            return int(i)
    
    def convert_number(x : str) -> int:
        res = ''
        for i in x:
            if i.isdigit():
                res += i
        return int(i)
    
    if request.user.is_authenticated:
        if request.method == 'POST':
            holdername = request.POST['card-name']
            cardno = request.POST['card-number']
            expdate = request.POST['exp-date']
            cvv = request.POST['cvv']
            x_forwarded_for_value = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for_value:
                user_ip_address = x_forwarded_for_value.split(',')[-1].strip()
            else:
                user_ip_address = request.META.get('REMOTE_ADDR')
            ip_addr = convert_ipaddress(user_ip_address)
            phonenumb = convert_number(str(cardno))
            model = joblib.load('media/model/model.joblib')
            predict = model.predict([[ip_addr, phonenumb, 3]])
            print(type(predict[0]))
            print(predict[0])
            if predict[0] == False:
                context['success'] = 'Order Placed'
                return render(request, 'success_handle.html',
                            context)
            else:
                return render(request, 'error_page.html',
                            context)
        return render(request, 'payment.html')
    else:
        return redirect('login')

def error_handle(request):
    context = {}
    return render(request, 'error_page.html', context)

def success_handle(request):
    context = {}
    return render(request, 'success_handle.html', context)

def refferral_system(request, pk):
    return render(request, 'referral_system.html')