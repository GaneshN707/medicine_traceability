from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
from app.auth import authentication, generate_qr_code
from app.models import firm_info
from app.models import medicine
from cryptography.fernet import Fernet
import json
import qrcode 
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
import cv2
import time
from django.http import JsonResponse
import hashlib
import os
from django.http import HttpResponseNotFound
from django.template import TemplateDoesNotExist
# Create your views here.
def base(request):
    return render(request , 'base.html')

def index(request):
    return render(request , 'index.html')

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def Show_data(request):
     # Assuming firm_info is the model associated with user medicine data
    Medicines = medicine.objects.filter(first_name = request.user.first_name)
    print(Medicines)
    user_firm = firm_info.objects.get(user=request.user)
    context = {
        'fname': request.user.first_name,
        'medicines' : Medicines,
        'user_type' : user_firm.user_type,
    }

    return render(request, 'Show_data.html', context)




def registration(request, user_type):
    context = {
        'user_type' : user_type,
    }
    if request.method == "POST":
        first_name = request.POST['fname']
        username = request.POST['username']
        password = request.POST['password']
        password1 = request.POST['repassword']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        postal_code = request.POST['postal_code']
        user_type = request.POST['user_type']
        # print(first_name, contact_no, ussername)

        verify = authentication(first_name, password, password1)
        if verify == "success":
            user = User.objects.create_user(username, password, password1)          #create_user
            profile = firm_info(user = user, address = address, city = city, state = state, country = country, postal_code = postal_code, user_type = user_type)
            user.first_name = first_name
            user.save()
            profile.save()
            messages.success(request, "Your Account has been Created.")
            return redirect("log_in")
            
        else:
            messages.error(request, verify)
            return redirect("registration", user_type=user_type)
    
    return render(request, 'registration.html', context)   


def log_in(request):
    if request.method == "POST":
        # return HttpResponse("This is Home page")  
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, "Log In Successful...!")
            return redirect("sidebar")
        else:
            messages.error(request, "Invalid User...!")
            return redirect("log_in")
    return render(request, 'log_in.html')


@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def log_out(request):
    logout(request)
    messages.success(request, "Log out Successfuly...!")
    return redirect("/")

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def sidebar(request):
    user_firm = firm_info.objects.get(user=request.user)
    context = {
        'fname': request.user.first_name,
        'user_type' : user_firm.user_type
    }
    return render(request , 'sidebar.html', context)

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)

def admedicine(request):
    try:
        user_firm = firm_info.objects.get(user=request.user)
        context = {
            'fname': request.user.first_name,
            'city': user_firm.city,
            'address': user_firm.address,
            'state' : user_firm.state,
            'postal_code': user_firm.postal_code,
            'user_type' : user_firm.user_type
        }
        if request.method == "POST":
            medicine_id = request.POST['medicine_id']
            medicine_name = request.POST['medicine_name']
            batch_no = request.POST['batch_no']
            Medicine_Used = request.POST['Medicine_Used']
            manifacture_date = request.POST['manifacture_date']
            expire_date = request.POST['expire_date']
            medice_mrp = request.POST['medice_mrp']


            qr_dict = {"medicine_id" : medicine_id, 'medicine_name': medicine_name, 'batch_no' : batch_no,'Medicine_Used':Medicine_Used, 'manifacture_date': str(manifacture_date),'expire_date':str(expire_date), 'medice_mrp': medice_mrp}
            # Generate a key
            key = Fernet.generate_key()

            # Create a Fernet cipher using the key
            cipher_suite = Fernet(key)

            # Convert dictionary to bytes
            data_bytes = json.dumps(qr_dict).encode()

            # Encrypt the data
            encrypted_data = cipher_suite.encrypt(data_bytes)

            # Combine cipher suite and encrypted data into a single string
            qr_value = key.decode() + "#*#" + encrypted_data.decode()
            # print(qr_value)
            qr_image = generate_qr_code(qr_value, medicine_id, batch_no, str(manifacture_date))

            # Check if chain/chain.json exists
            if os.path.exists('chain/chain.json'):
                # Try to load existing data from chain/chain.json
                with open('chain/chain.json', 'r') as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        # If file is empty or not valid JSON, initialize data as an empty dictionary
                        data = {}
            else:
                # If chain/chain.json doesn't exist, initialize data as an empty dictionary
                data = {}

            # Check if qr_value already exists in data
            if qr_value in data:
                # If qr_value already exists, display a message and return
                messages.warning(request, "Medicine already exists!")
                return render(request, 'admedicine.html', context)

            # Store qr_value as a key with an empty list as its value in data
            data[qr_value] = []

            # Write data back to chain/chain.json
            with open('chain/chain.json', 'w') as f:
                json.dump(data, f, indent=4)

            med = medicine(Medicine_id = medicine_id, Medicine_Name = medicine_name, Batch_No = batch_no, Medicine_Used = Medicine_Used, Manifacture_Date = manifacture_date, Expiring_Date = expire_date, Maximum_Retail_prise = medice_mrp, first_name = request.user.first_name , city = user_firm.city, state = user_firm.state, country = user_firm.country, postal_code = user_firm.postal_code, qr_code_image=qr_image)
            
            med.save()
            messages.success(request, "Medicine Added Successfuly!!!")

            context['med'] = med


    except firm_info.DoesNotExist:
        context = {
            'fname': request.user.first_name,
            'city': '',
            'address': '',
            'state': '',
            'postal_code':'',
        }

    return render(request, 'admedicine.html', context)

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def scan_qr(request):
    user_firm = firm_info.objects.get(user=request.user)
    context = {
        'user_type' : user_firm.user_type
    }
    
    return render(request , 'scan_qr.html', context)

@login_required(login_url="log_in")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def scaned_qr(request, qr_value):
    try:
        # Retrieve firm_info associated with the current user
        user_firm = firm_info.objects.get(user=request.user)
    except firm_info.DoesNotExist:
        messages.error(request, "Invalid Qr Code!!")
        return HttpResponseNotFound("Invalid Qr Code!!")

    context = {
        'user_type': user_firm.user_type
    }

    try:
        # Load the contents of chain.json
        with open('chain/chain.json', 'r') as f:
            chain_data = json.load(f)
    except FileNotFoundError:
        # If chain.json file does not exist, create an empty dictionary
        chain_data = {}


    # Check if qr_value is present in the keys of chain_data
    if qr_value in chain_data:
        associated_value = chain_data[qr_value]
        if isinstance(associated_value, list):
            # Encrypt the current user's data using SHA256
            data = f"{request.user.username}#{user_firm.user_type}#{user_firm.city}#{user_firm.state}#{user_firm.country}"
            encrypted_data = {user_firm.user_type : hashlib.sha256(data.encode()).hexdigest()}
            if encrypted_data in associated_value:
                messages.info(request, "Medicine Already Present")
            else:
                # Append the encrypted data to the list associated with the QR code value
                chain_data[qr_value].append(encrypted_data)
                with open('chain/chain.json', 'w') as f:
                    json.dump(chain_data, f)
                messages.success(request, "Data Appended Successfully!!")
        else:
            messages.error(request, "Invalid Data Format for QR Code")
    else:
        # If qr_value is not present, redirect to scan_qr page
        messages.info(request, "Invalid QR Code!!")
        return redirect('scan_qr')


    try:
        return render(request, 'scan_qr.html', context)
    except TemplateDoesNotExist:
        messages.error(request, "Template 'scan_qr.html' does not exist.")
        return redirect('scan_qr')

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def tracemedicine(request):
    user_firm = firm_info.objects.get(user=request.user)
    context = {
        'user_type' : user_firm.user_type
    }
    
    return render(request , 'tracemedicine.html', context)

def trace_qr(request, qr_value):
    
    try:
        # Load the contents of chain.json
        with open('chain/chain.json', 'r') as f:
            chain_data = json.load(f)
    except FileNotFoundError:
        # If chain.json file does not exist, return None
        return None

    # Check if qr_value is present in the keys of chain_data
    if qr_value in chain_data:
        associated_value = chain_data[qr_value]
        user_firm = firm_info.objects.get(user=request.user)
        context = {
            'user_type' : user_firm.user_type,
            'chain' : associated_value
        }
        if isinstance(associated_value, list):
            # Decrypt the data associated with the QR code value
            # Assuming qr_value contains the encryption key followed by the encrypted data
            key_str, encrypted_data_str = qr_value.split("#*#")

            # Convert the key string back to bytes
            key = key_str.encode()

            # Create a Fernet cipher using the key
            cipher_suite = Fernet(key)

            # Decrypt the encrypted data
            decrypted_data = cipher_suite.decrypt(encrypted_data_str.encode())

            # Convert the decrypted bytes back to a dictionary
            decrypted_dict = json.loads(decrypted_data.decode())

            print(decrypted_dict)
            context['decrypted_dict'] = decrypted_dict
            messages.success(request, "Authorized Medicine")
            return render(request, "trace_qr.html",context)
        else:
            # Invalid data format for QR code
            return None
    else:
        # QR code value not found
        messages.error(request, "Unauthorized Qr Code")
        user_firm = firm_info.objects.get(user=request.user)
        context = {
            'user_type' : user_firm.user_type
        }
    
        return render(request , 'tracemedicine.html', context)    

# def pages(request, *args, **kwargs):
#     messages.error(request, "Invalid QR Code!!!")
#     return render(request, '404.html', status=404)