from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.utils.text import capfirst
from django.contrib.auth.models import User,auth
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.views import View
from .forms import EmailForm
from django.http import JsonResponse
from datetime import datetime,date, timedelta
from xhtml2pdf import pisa
from django.template.loader import get_template
from bs4 import BeautifulSoup
import io
import os
import json
from django.template import Context, Template
import tempfile
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.http import FileResponse
from django.urls import reverse
from django.db.models import Sum
from itertools import groupby
from django.core import serializers
from django.shortcuts import get_object_or_404, redirect
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from django.template.response import TemplateResponse
import calendar
from calendar import HTMLCalendar
from django.template import loader
from .models import customer  # Import your Customer model


def index(request):

    return render(request,'landpage.html')

def register(request):
    if request.method=='POST':

        first_name=capfirst(request.POST['fname'])
        last_name=capfirst(request.POST['lname'])
        username=request.POST['uname']
        password=request.POST['password']
        cpassword=request.POST['cpassword']
        email=request.POST['email1']
        phone = request.POST['phone']

      
        if password==cpassword:  #  password matching......
            if User.objects.filter(username=username).exists(): #check Username Already Exists..
                messages.info(request, 'This username already exists!!!!!!')
                return redirect('register')
            else:
                user=User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    password=password,
                    email=email)
                
                user.save()
                u = User.objects.get(id = user.id)

                company_details(contact_number = phone, user = u).save()
        else:
            messages.info(request, 'Password doesnt match!!!!!!!')
            print("Password is not Matching.. ") 
            return redirect('register')   
        return redirect('register')

    return render(request,'register.html',{'msg' : messages})

def login(request):
        
    if request.method == 'POST':
        
        email_or_username = request.POST['emailorusername']
        password = request.POST['password']
        print(password)
        user = authenticate(request, username=email_or_username, password=password)
        print(user)
        if user is not None:
            auth.login(request,user)
            # .........................................................
            user=request.user        
            account_info = [{"user": user, "account_type": "Accounts Payable","account_name":"Accounts Payable","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"This is an account of all the money which you owe to others like a pending bill payment to a vendor,etc.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Accounts Receivable","account_name":"Accounts Receivable","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"The money that customers owe you becomes the accounts receivable. A good example of this is a payment expected from an invoice sent to your customer.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Advertising and Marketing","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Your expenses on promotional, marketing and advertising activities like banners, web-adds, trade shows, etc. are recorded in advertising and marketing account.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Current Assets","account_name":"Advance Tax","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Any tax which is paid in advance is recorded into the advance tax account. This advance tax payment could be a quarterly, half yearly or yearly payment","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Automobile Expense","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Transportation related expenses like fuel charges and maintenance charges for automobiles, are included to the automobile expense account.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Bad Debt","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Any amount which is lost and is unrecoverable is recorded into the bad debt account.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Bank Fees and Charges","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":" Any bank fees levied is recorded into the bank fees and charges account. A bank account maintenance fee, transaction charges, a late payment fee are some examples.","watchlist":"","create_status":"default","status":"active"},
            
            {"user": user, "account_type": "Expense","account_name":"Consultant Expense","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Charges for availing the services of a consultant is recorded as a consultant expenses. The fees paid to a soft skills consultant to impart personality development training for your employees is a good example.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Cost Of Goods Sold","account_name":"Cost of Goods Sold","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"An expense account which tracks the value of the goods sold.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Credit Card Charges","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":" Service fees for transactions , balance transfer fees, annual credit fees and other charges levied on a credit card are recorded into the credit card account.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Depreciation Expense","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Any depreciation in value of your assets can be captured as a depreciation expense.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Depreciation Expense","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Any depreciation in value of your assets can be captured as a depreciation expense.","watchlist":"","create_status":"default","status":"active"},

            {"user": user, "account_type": "Income","account_name":"Discount","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Any reduction on your selling price as a discount can be recorded into the discount account.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Equity","account_name":"Drawings","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"The money withdrawn from a business by its owner can be tracked with this account.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Current Assets","account_name":"Employee Advance","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Money paid out to an employee in advance can be tracked here till it's repaid or shown to be spent for company purposes","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Current Liability","account_name":"Employee Reimbursements","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"This account can be used to track the reimbursements that are due to be paid out to employees.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Expense","account_name":"Exchange Gain or Loss","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Changing the conversion rate can result in a gain or a loss. You can record this into the exchange gain or loss account.","watchlist":"","create_status":"default","status":"active"},

            {"user": user, "account_type": "Fixed Asset","account_name":"Furniture and Equipment","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Purchases of furniture and equipment for your office that can be used for a long period of time usually exceeding one year can be tracked with this account.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Income","account_name":"General Income","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"A general category of account where you can record any income which cannot be recorded into any other category","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Income","account_name":"Interest Income","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"A percentage of your balances and deposits are given as interest to you by your banks and financial institutions. This interest is recorded into the interest income account.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Stock","account_name":"Inventory Asset","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"An account which tracks the value of goods in your inventory.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"IT and Internet Expenses","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Money spent on your IT infrastructure and usage like internet connection, purchasing computer equipment etc is recorded as an IT and Computer Expense","watchlist":"","create_status":"default","status":"active"},

            {"user": user, "account_type": "Expense","account_name":"Janitorial Expense","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"All your janitorial and cleaning expenses are recorded into the janitorial expenses account.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Income","account_name":"Late Fee Income","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Any late fee income is recorded into the late fee income account. The late fee is levied when the payment for an invoice is not received by the due date","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Lodging","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Any expense related to putting up at motels etc while on business travel can be entered here.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Meals and Entertainment","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Expenses on food and entertainment are recorded into this account.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Office Supplies","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"All expenses on purchasing office supplies like stationery are recorded into the office supplies account.","watchlist":"","create_status":"default","status":"active"},

            {"user": user, "account_type": "Other Current Liability","account_name":"Opening Balance Adjustments","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"This account will hold the difference in the debits and credits entered during the opening balance.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Equity","account_name":"Opening Balance Offset","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"This is an account where you can record the balance from your previous years earning or the amount set aside for some activities. It is like a buffer account for your funds.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Income","account_name":"Other Charges","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Miscellaneous charges like adjustments made to the invoice can be recorded in this account.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Other Expenses","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":" Any minor expense on activities unrelated to primary business operations is recorded under the other expense account.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Equity","account_name":"Owner's Equity","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"The owners rights to the assets of a company can be quantified in the owner's equity account.","watchlist":"","create_status":"default","status":"active"},

            {"user": user, "account_type": "Cash","account_name":"Petty Cash","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"It is a small amount of cash that is used to pay your minor or casual expenses rather than writing a check.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Postage","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Your expenses on ground mails, shipping and air mails can be recorded under the postage account.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Current Assets","account_name":"Prepaid Expenses","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"An asset account that reports amounts paid in advance while purchasing goods or services from a vendor.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Printing and Stationery","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":" Expenses incurred by the organization towards printing and stationery.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Rent Expense","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"The rent paid for your office or any space related to your business can be recorded as a rental expense.","watchlist":"","create_status":"default","status":"active"},

            {"user": user, "account_type": "Expense","account_name":"Repairs and Maintenance","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"The costs involved in maintenance and repair of assets is recorded under this account.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Equity","account_name":"Retained Earnings","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"The earnings of your company which are not distributed among the share holders is accounted as retained earnings.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Salaries and Employee Wages","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Salaries for your employees and the wages paid to workers are recorded under the salaries and wages account.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Income","account_name":"Sales","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":" The income from the sales in your business is recorded under the sales account.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Income","account_name":"Shipping Charge","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Shipping charges made to the invoice will be recorded in this account.","watchlist":"","create_status":"default","status":"active"},

            {"user": user, "account_type": "Other Liability","account_name":"Tag Adjustments","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":" This adjustment account tracks the transfers between different reporting tags.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Current Liability","account_name":"Tax Payable","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"The amount of money which you owe to your tax authority is recorded under the tax payable account. This amount is a sum of your outstanding in taxes and the tax charged on sales.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Telephone Expense","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"The expenses on your telephone, mobile and fax usage are accounted as telephone expenses.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Travel Expense","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":" Expenses on business travels like hotel bookings, flight charges, etc. are recorded as travel expenses.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Uncategorized","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"This account can be used to temporarily track expenses that are yet to be identified and classified into a particular category.","watchlist":"","create_status":"default","status":"active"},

            {"user": user, "account_type": "Cash","account_name":"Undeposited Funds","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"Record funds received by your company yet to be deposited in a bank as undeposited funds and group them as a current asset in your balance sheet.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Current Liability","account_name":"Unearned Revenue","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"A liability account that reports amounts received in advance of providing goods or services. When the goods or services are provided, this account balance is decreased and a revenue account is increased.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Equity","account_name":"Capital Stock","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":" An equity account that tracks the capital introduced when a business is operated through a company or corporation.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Long Term Liability","account_name":"Construction Loans","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"An expense account that tracks the amount you repay for construction loans.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Contract Assets","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"An asset account to track the amount that you receive from your customers while you're yet to complete rendering the services.","watchlist":"","create_status":"default","status":"active"},

            {"user": user, "account_type": "Expense","account_name":"Depreciation And Amortisation","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"An expense account that is used to track the depreciation of tangible assets and intangible assets, which is amortization.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Equity","account_name":"Distributions","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"An equity account that tracks the payment of stock, cash or physical products to its shareholders.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Equity","account_name":"Dividends Paid","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"An equity account to track the dividends paid when a corporation declares dividend on its common stock.","watchlist":"","create_status":"default","status":"active"},

            {"user": user, "account_type": "Other Current Liability","account_name":"GST Payable","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Current Liability","account_name":"Output CGST","credit_no":"","sub_account":"on","parent_account":"GST Payable","bank_account_no":"","currency":"","account_code":"","description":"","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Current Liability","account_name":"Output IGST","credit_no":"","sub_account":"on","parent_account":"GST Payable","bank_account_no":"","currency":"","account_code":"","description":"","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Current Liability","account_name":"Output SGST","credit_no":"","sub_account":"on","parent_account":"GST Payable","bank_account_no":"","currency":"","account_code":"","description":"","watchlist":"","create_status":"default","status":"active"},

            {"user": user, "account_type": "Equity","account_name":"Investments","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"An equity account used to track the amount that you invest.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Cost Of Goods Sold","account_name":"Job Costing","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"An expense account to track the costs that you incur in performing a job or a task.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Cost Of Goods Sold","account_name":"Labor","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"An expense account that tracks the amount that you pay as labor.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Cost Of Goods Sold","account_name":"Materials","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"An expense account that tracks the amount you use in purchasing materials.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Merchandise","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"An expense account to track the amount spent on purchasing merchandise.","watchlist":"","create_status":"default","status":"active"},

            {"user": user, "account_type": "Long Term Liability","account_name":"Mortgages","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"An expense account that tracks the amounts you pay for the mortgage loan.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Raw Materials And Consumables","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"An expense account to track the amount spent on purchasing raw materials and consumables.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Current Assets","account_name":"Reverse Charge Tax Input but not due","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"The amount of tax payable for your reverse charge purchases can be tracked here.","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Current Assets","account_name":"Sales to Customers (Cash)","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Cost Of Goods Sold","account_name":"Subcontractor","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":" An expense account to track the amount that you pay subcontractors who provide service to you.","watchlist":"","create_status":"default","status":"active"},

            {"user": user, "account_type": "Other Current Assets","account_name":"GST TCS Receivable","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Current Assets","account_name":"GST TDS Receivable","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"","watchlist":"","create_status":"default","status":"active"},

            {"user": user, "account_type": "Other Current Assets","account_name":"Input Tax Credits","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Current Assets","account_name":"Input CGST","credit_no":"","sub_account":"on","parent_account":"Input Tax Credits","bank_account_no":"","currency":"","account_code":"","description":"","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Current Assets","account_name":"Input IGST","credit_no":"","sub_account":"on","parent_account":"Input Tax Credits","bank_account_no":"","currency":"","account_code":"","description":"","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Current Assets","account_name":"Input SGST","credit_no":"","sub_account":"on","parent_account":"Input Tax Credits","bank_account_no":"","currency":"","account_code":"","description":"","watchlist":"","create_status":"default","status":"active"},

            {"user": user, "account_type": "Other Current Liability","account_name":"TDS Payable","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Other Current Assets","account_name":"TDS Receivable","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"","watchlist":"","create_status":"default","status":"active"},
            {"user": user, "account_type": "Expense","account_name":"Transportation Expense","credit_no":"","sub_account":"","parent_account":"","bank_account_no":"","currency":"","account_code":"","description":"An expense account to track the amount spent on transporting goods or providing services.","watchlist":"","create_status":"default","status":"active"},




            ]
            print(account_info[0])
            print(account_info[1])

            for account in account_info:
                print(account)
                if not Chart_of_Account.objects.filter(account_name=account['account_name']).exists():
                    new_account = Chart_of_Account(user=account['user'],account_name=account['account_name'],account_type=account['account_type'],credit_no=account['credit_no'],sub_account=account['sub_account'],parent_account=account['parent_account'],bank_account_no=account['bank_account_no'],currency=account['currency'],account_code=account['account_code'],description=account['description'],watchlist=account['watchlist'],create_status=account['create_status'],status=account['status'])
                    new_account.save()
            
            if not setting_list.objects.filter(user=request.user.id).exists():
                user_id=User.objects.get(id=request.user.id)
                settings_row=setting_list(user=user_id,items='yes',pricelist='yes',offline_banking='yes',banking='yes',customers='yes',
                estimates='yes',retainer_invoices='yes',sales_orders='yes',delivery_challans='yes',invoices='yes',
                credit_notes='yes',recurring_invoices='yes',vendors='yes',vendor_credits='yes',expenses='yes',recurring_expenses='yes',
                purchase_orders='yes',payment_made='yes',bills='yes',recurring_bills='yes',projects='yes',chart_of_accounts='yes',
                employees='yes',employees_loan='yes',pdf='yes',slip='yes',print_opt='yes')
                settings_row.save()
            return redirect('dashboard')
        else:
            return redirect('/')
        

    return render(request, 'register.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('/')

def forgotpassword(request):
     return render(request,'setpassword.html')

def setnewpassword(request):

    if request.method=='POST':
        email_or_username = request.POST['emailorusername']
        password=request.POST['password']
        cpassword=request.POST['cpassword']
        if password==cpassword:

            c = User.objects.filter(Q(username = email_or_username)|Q(email = email_or_username)).first()
            c.set_password(password)
            c.save()

        return redirect('register' )
        
    else:
        return render(request, 'setpassword.html')

@login_required(login_url='login')
def base(request):
   
       
    if not Unit.objects.filter(unit='BOX').exists():
            Unit(unit='BOX').save()
    if not Unit.objects.filter(unit='UNIT').exists():
            Unit(unit='UNIT').save()
    if not Unit.objects.filter(unit='LITRE').exists():
            Unit(unit='LITRE').save()

    if not Sales.objects.filter(Account_name='General Income').exists():
            Sales(Account_type='INCOME',Account_name='General Income',Account_desc='salesincome').save()
    if not Sales.objects.filter(Account_name='Intrest Income').exists():
            Sales(Account_type='INCOME',Account_name='Intrest Income',Account_desc='salesincome').save()
    if not Sales.objects.filter(Account_name='Late fee Income').exists():
            Sales(Account_type='INCOME',Account_name='Late fee Income',Account_desc='salesincome').save()
    if not Sales.objects.filter(Account_name='Discount Income').exists():
            Sales(Account_type='INCOME',Account_name='Discount Income',Account_desc='salesincome').save()
    if not Sales.objects.filter(Account_name='Other Charges').exists():
            Sales(Account_type='INCOME',Account_name='Other Charges',Account_desc='salesincome').save()
    if not Sales.objects.filter(Account_name='Shipping Charge').exists():
            Sales(Account_type='INCOME',Account_name='Shipping Charge',Account_desc='salesincome').save()
    



    if not  Purchase.objects.filter(Account_name='Advertising & Marketing').exists():
            Purchase(Account_type='EXPENCES',Account_name='Advertising & Markting',Account_desc='Advertsing Exp').save()
    if not Purchase.objects.filter(Account_name='Debit Charge').exists():
            Purchase(Account_type='EXPENCES',Account_name='Debit Charge',Account_desc='Debited Exp').save()
    if not Purchase.objects.filter(Account_name='Labour Charge').exists():
            Purchase(Account_type='EXPENCES',Account_name='Labour Charge',Account_desc='Labour Exp').save()
    if not Purchase.objects.filter(Account_name='Raw Meterials').exists():
            Purchase(Account_type='EXPENCES',Account_name='Raw Meterials',Account_desc='Raw Meterials Exp').save()
    if not Purchase.objects.filter(Account_name='Automobile Expense').exists():
            Purchase(Account_type='EXPENCES',Account_name='Automobile Expense',Account_desc='Automobile Expense').save()
    if not Purchase.objects.filter(Account_name='Bad Debt').exists():
            Purchase(Account_type='EXPENCES',Account_name='Bad Debt',Account_desc='Bad Debt').save()
    if not Purchase.objects.filter(Account_name='Bank Fees and Charges').exists():
            Purchase(Account_type='EXPENCES',Account_name='Bank Fees and Charges',Account_desc='Bank Fees and Charges').save()
    if not Purchase.objects.filter(Account_name='Consultant Expense').exists():
            Purchase(Account_type='EXPENCES',Account_name='Consultant Expense',Account_desc='Consultant Expense').save()
    if not Purchase.objects.filter(Account_name='Credit card Charges').exists():
            Purchase(Account_type='EXPENCES',Account_name='Credit card Charges',Account_desc='Credit card Charges').save()
    if not Purchase.objects.filter(Account_name='Depreciation Charges').exists():
            Purchase(Account_type='EXPENCES',Account_name='Depreciation Charges',Account_desc='Depreciation Charges').save()
    if not Purchase.objects.filter(Account_name='IT and Internet Expense').exists():
            Purchase(Account_type='EXPENCES',Account_name='IT and Internet Expense',Account_desc='IT and Internet Expense').save()
    if not Purchase.objects.filter(Account_name='Janitorial Expense').exists():
            Purchase(Account_type='EXPENCES',Account_name='Janitorial Expense',Account_desc='Janitorial Expense').save()
    if not Purchase.objects.filter(Account_name='Lodging').exists():
            Purchase(Account_type='EXPENCES',Account_name='Lodging',Account_desc='Lodging').save()
    if not Purchase.objects.filter(Account_name='Meals and Entertinment').exists():
            Purchase(Account_type='EXPENCES',Account_name='Meals and Entertinment',Account_desc='Meals and Entertinment').save()
    if not Purchase.objects.filter(Account_name='Office Supplies').exists():
            Purchase(Account_type='EXPENCES',Account_name='Office Supplies',Account_desc='Office Supplies').save()
    if not Purchase.objects.filter(Account_name='Other Expenses').exists():
            Purchase(Account_type='EXPENCES',Account_name='Other Expenses',Account_desc='Other Expenses').save()
    if not Purchase.objects.filter(Account_name='Postage').exists():
            Purchase(Account_type='EXPENCES',Account_name='Printing and sationary',Account_desc='Postage').save()
    if not Purchase.objects.filter(Account_name='Postage').exists():
            Purchase(Account_type='EXPENCES',Account_name='Printing and sationary',Account_desc='Printing and sationary').save()
    if not Purchase.objects.filter(Account_name='Rent Expenses').exists():
            Purchase(Account_type='EXPENCES',Account_name='Rent Expenses',Account_desc='Rent Expenses').save()
    if not Purchase.objects.filter(Account_name='Repair and maintenance').exists():
            Purchase(Account_type='EXPENCES',Account_name='Repair and maintenance',Account_desc='Repair and maintenance').save()
    if not Purchase.objects.filter(Account_name='Salaries and Employee wages').exists():
            Purchase(Account_type='EXPENCES',Account_name='Salaries and Employee wages',Account_desc='Salaries and Employee wages').save()
    if not Purchase.objects.filter(Account_name='Telephonic Expenses').exists():
            Purchase(Account_type='EXPENCES',Account_name='Telephonic Expenses',Account_desc='Telephonic Expenses').save()
    if not Purchase.objects.filter(Account_name='Travel Expenses').exists():
            Purchase(Account_type='EXPENCES',Account_name='Travel Expenses',Account_desc='Travel Expenses').save()
    if not Purchase.objects.filter(Account_name='Uncategorized').exists():
            Purchase(Account_type='EXPENCES',Account_name='Uncategorized',Account_desc='Uncategorized').save()
    if not Purchase.objects.filter(Account_name='Contract Assets').exists():
            Purchase(Account_type='EXPENCES',Account_name='Contract Assets',Account_desc='Contract Assets').save()
    if not Purchase.objects.filter(Account_name='Depreciation and Amoritisation').exists():
            Purchase(Account_type='EXPENCES',Account_name='Depreciation and Amoritisation',Account_desc='Depreciation and Amoritisation').save()
    if not Purchase.objects.filter(Account_name='Merchandise').exists():
            Purchase(Account_type='EXPENCES',Account_name='Merchandise',Account_desc='Merchandise').save()
    if not Purchase.objects.filter(Account_name='Raw material and Consumables').exists():
            Purchase(Account_type='EXPENCES',Account_name='Raw material and Consumables',Account_desc='Raw material and Consumables').save()
    if not Purchase.objects.filter(Account_name='Transportation Expenses').exists():
            Purchase(Account_type='EXPENCES',Account_name='Transportation Expenses',Account_desc='Transportation Expenses').save()
    if not Purchase.objects.filter(Account_name='Transportation Expenses').exists():
            Purchase(Account_type='EXPENCES',Account_name='Transportation Expenses',Account_desc='Transportation Expenses').save()
    if not Purchase.objects.filter(Account_name='Cost Of Goods Sold').exists():
            Purchase(Account_type='Cost Of Goods Sold',Account_name='Cost Of Goods Sold',Account_desc='Cost Of Goods Sold').save()
    if not Purchase.objects.filter(Account_name='Job Costing').exists():
            Purchase(Account_type='Cost Of Goods Sold',Account_name='Job Costing',Account_desc='Job Costing').save()
    if not Purchase.objects.filter(Account_name='Labour').exists():
            Purchase(Account_type='Cost Of Goods Sold',Account_name='Labour',Account_desc='Labour').save()
    if not Purchase.objects.filter(Account_name='Materials').exists():
            Purchase(Account_type='Cost Of Goods Sold',Account_name='Materials',Account_desc='Materials').save()
    if not Purchase.objects.filter(Account_name='Subcontractor').exists():
            Purchase(Account_type='Cost Of Goods Sold',Account_name='Subcontractor',Account_desc='Subcontractor').save()
    if not Purchase.objects.filter(Account_name='Furniture and Equipment').exists():
            Purchase(Account_type='Fixed Asset',Account_name='Furniture and Equipment',Account_desc='Furniture and Equipment').save() 

    if not Account.objects.filter(accountName='Advance Tax').exists():
        Account(accountType='Other Current Asset',accountName='Advance Tax',description='Advance Tax').save()
    if not Account.objects.filter(accountName='Employee Advance').exists():
        Account(accountType='Other Current Asset',accountName='Employee Advance',description='Employee Advance').save()
    if not Account.objects.filter(accountName='Furniture and Equipment').exists():
            Account(accountType='Fixed Asset',accountName='Furniture and Equipment',description='Furniture and Equipment').save()
    if not Account.objects.filter(accountName='Employee Reimbursement').exists():
        Account(accountType='Other Current Liability',accountName='Employee Reimbursement',description='Employee Reimbursement').save()
    if not Account.objects.filter(accountName='Advertising & Marketing').exists():
        Account(accountType='Expenses',accountName='Advertising & Marketing',description='Advertising & Marketing').save()
    if not Account.objects.filter(accountName='Automobile Expense').exists():
        Account(accountType='Expenses',accountName='Automobile Expense',description='Automobile Expense').save()
    if not payment_terms.objects.filter(Terms='NET 30').exists():
        payment_terms(Terms='NET 30').save()
    if not payment_terms.objects.filter(Terms='NET 60').exists():
        payment_terms(Terms='NET 60').save()
    if not payment_terms.objects.filter(Terms='NET 45').exists():
        payment_terms(Terms='NET 45').save()
    if not payment_terms.objects.filter(Terms='Due on Receipt').exists():
        payment_terms(Terms='Due on Receipt').save()
    


   

    company = company_details.objects.get(user = request.user)
    context = {
                'company' : company
            }
    return render(request,'loginhome.html',context)




@login_required(login_url='login')
def view_profile(request):

    company = company_details.objects.get(user = request.user)
    context = {
                'company' : company
            }
    return render(request,'profile.html',context)

@login_required(login_url='login')
def edit_profile(request,pk):

    company = company_details.objects.get(id = pk)
    user1 = User.objects.get(id = company.user_id)

    if request.method == "POST":

        user1.first_name = capfirst(request.POST.get('f_name'))
        user1.last_name  = capfirst(request.POST.get('l_name'))
        user1.email = request.POST.get('email')
        company.contact_number = request.POST.get('cnum')
        company.address = request.POST.get('ards')
        company.company_name = request.POST.get('comp_name')
        company.company_email = request.POST.get('comp_email')
        company.city = request.POST.get('city')
        company.state = request.POST.get('state')
        company.country = request.POST.get('country')
        company.pincode = request.POST.get('pinc')
        company.gst_num = request.POST.get('gst')
        company.pan_num = request.POST.get('pan')
        company.business_name = request.POST.get('bname')
        company.company_type = request.POST.get('comp_type')
        company.industry_type = request.POST.get('indu_type')
        if len(request.FILES)!=0 :
            company.profile_pic = request.FILES.get('file')

        company.save()
        user1.save()
        return redirect('view_profile')

    context = {
        'company' : company,
        'user1' : user1,
    }
    
    return render(request,'edit_profile.html',context)

@login_required(login_url='login')
def itemview(request):
    company = company_details.objects.get(user = request.user)
    viewitem=AddItem.objects.all()
    return render(request,'item_view.html',{'view':viewitem,'company':company})


@login_required(login_url='login')
def additem(request):
    company=company_details.objects.get(user=request.user)
    unit=Unit.objects.all()
    sale=Sales.objects.all()
    purchase=Purchase.objects.all()
    accounts = Purchase.objects.all()
    account_types = set(Purchase.objects.values_list('Account_type', flat=True))

    
    account = Sales.objects.all()
    account_type = set(Sales.objects.values_list('Account_type', flat=True))
    
    

    return render(request,'additem.html',{'unit':unit,'sale':sale,'purchase':purchase,'company':company,
               
                            "account":account,"account_type":account_type,"accounts":accounts,"account_types":account_types,
                            
                            })

@login_required(login_url='login')
def add_account(request):
    if request.method=='POST':
        Account_type  =request.POST.get('acc_type')
        if Account_type is not None:
            Account_name =request.POST['acc_name']
            Account_desc =request.POST['acc_desc']
        
            acc=Purchase(Account_type=Account_type,Account_name=Account_name,Account_desc=Account_desc)
            acc.save() 
            account_id=acc.id 
                           
            return JsonResponse({"Account_type":Account_type,"Account_name":Account_name,"Account_desc":Account_desc,'account_id':account_id})
        
    return render(request,'additem.html')


@login_required(login_url='login')
def add(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            radio=request.POST.get('radio')
           
            
            if radio =='taxable':
                print('tax section')
                
    
                
                inter=request.POST['inter']
                intra=request.POST['intra']
                type=request.POST.get('type')
                name=request.POST['name']
                unit=request.POST['unit']
                hsn=request.POST['hsn']
                status=request.POST.get('status')
                sel_price=request.POST.get('sel_price')
                sel_acc=request.POST.get('sel_acc')
                s_desc=request.POST.get('sel_desc')
                cost_price=request.POST.get('cost_price')
                cost_acc=request.POST.get('cost_acc')      
                p_desc=request.POST.get('cost_desc')
                min_stock=request.POST.get('minimum_stock')
                tax=request.POST.get('radio')
                u=request.user.id
                us=request.user
                history="Created by" + str(us)
                user=User.objects.get(id=u)
                unit=Unit.objects.get(id=unit)
                sel=Sales.objects.get(id=sel_acc)
                cost=Purchase.objects.get(id=cost_acc)
                invacc=request.POST.get('invacc')
                stock=request.POST.get('openstock')
                stock_per_unit = request.POST.get('inventoryaccntperunit')
           
                print('satus')
                
                ad_item=AddItem(type=type,
                                Name=name,
                                p_desc=p_desc,
                                s_desc=s_desc,
                                minimum_stock=min_stock,
                                s_price=sel_price,
                                p_price=cost_price,
                                tax=tax,
                                hsn=hsn,
                                unit=unit,
                                sales=sel,
                                purchase=cost,
                                satus=status,
                                user=user,
                                creat=history,
                                interstate=inter,
                                intrastate=intra,
                                invacc=invacc,
                                stock=stock,
                                rate=stock_per_unit
                                )
                ad_item.save()
                
            else:
                print('nontaxsection')
                                                  
                type=request.POST.get('type')
                name=request.POST['name']
                unit=request.POST['unit']
                hsn=request.POST['hsn']
                sel_price=request.POST.get('sel_price')
                sel_acc=request.POST.get('sel_acc')
                s_desc=request.POST.get('sel_desc')
                cost_price=request.POST.get('cost_price')
                cost_acc=request.POST.get('cost_acc')      
                p_desc=request.POST.get('cost_desc')
                min_stock=request.POST.get('minimum_stock')
                tax=request.POST.get('radio')
                status=request.POST.get('status')
                u=request.user.id
                us=request.user
                history="Created by" + str(us)
                user=User.objects.get(id=u)
                unit=Unit.objects.get(id=unit)
                sel=Sales.objects.get(id=sel_acc)
                cost=Purchase.objects.get(id=cost_acc)
                istock = request.POST['openstock']
                invacc=request.POST.get('invacc')
                stock_per_unit = request.POST.get('inventoryaccntperunit')

                ad_item=AddItem(type=type,
                                Name=name,
                                hsn=hsn,
                                p_desc=p_desc,
                                s_desc=s_desc,
                                minimum_stock=min_stock,
                                s_price=sel_price,
                                p_price=cost_price,
                                unit=unit,
                                sales=sel,
                                tax=tax,
                                purchase=cost,
                                satus = status,
                                user=user,
                                creat=history,
                                interstate='none',
                                intrastate='none',
                                invacc=invacc,
                                stock=istock,
                                rate=stock_per_unit
                            
                               
                                )
                
                ad_item.save()
           
           
            return redirect("itemview")
    return render(request,'additem.html')


@login_required(login_url='login')
def edititem(request,id):
    item=AddItem.objects.all
    pedit=AddItem.objects.get(id=id)
    p=Purchase.objects.all()
    s=Sales.objects.all()
    u=Unit.objects.all()
    company=company_details.objects.get(user=request.user)
    accounts = Purchase.objects.all()
    account_types = set(Purchase.objects.values_list('Account_type', flat=True))
    

    
    account = Sales.objects.all()
    account_type = set(Sales.objects.values_list('Account_type', flat=True))
    
    return render(request,'edititem.html',{"account":account,"account_type":account_type,'e':pedit,'p':p,'s':s,'u':u,"accounts":accounts,"account_types":account_types,'item':item, "company":company})




@login_required(login_url='login')
def edit_db(request,id):
        if request.method=='POST':
            radio=request.POST.get('radio')
            edit=AddItem.objects.get(id=id)

            if radio =='taxable':
                edit.interstate=request.POST['inter']
                edit.intrastate=request.POST['intra']
                edit.type=request.POST.get('type')
                edit.Name=request.POST['name']
                unit=request.POST.get('unit')  
                edit.s_price=request.POST['sel_price']
                sel_acc=request.POST['sel_acc']
                edit.s_desc=request.POST['sel_desc']
                edit.p_price=request.POST['cost_price']
                cost_acc=request.POST['cost_acc']        
                edit.p_desc=request.POST['cost_desc']
                edit.hsn=request.POST['hsn']
                edit.stock=request.POST['openstock']
                edit.satus=request.POST.get('status')
                edit.invacc=request.POST.get('invacc')
                edit.tax=request.POST.get('radio')
                edit.rate=request.POST.get('inventoryaccntperunit')
                edit.status_stock=request.POST.get('satus')
                edit.unit=Unit.objects.get(unit=unit)
                edit.sales=Sales.objects.get(id=sel_acc)
                edit.purchase=Purchase.objects.get(id=cost_acc)
                edit.minimum_stock=request.POST.get('minimum_stock')
                edit.save()
            
            else:
                edit.type=request.POST.get('type')
                edit.Name=request.POST['name']
                unit=request.POST.get('unit')
                edit.s_price=request.POST['sel_price']
                sel_acc=request.POST['sel_acc']
                edit.s_desc=request.POST['sel_desc']
                edit.p_price=request.POST['cost_price']
                cost_acc=request.POST['cost_acc']        
                edit.p_desc=request.POST['cost_desc']
                edit.hsn=request.POST['hsn']
                edit.stock=request.POST['openstock']
                edit.satus=request.POST.get('status')
                edit.invacc=request.POST.get('invacc')
                edit.tax=request.POST.get('radio')
                edit.rate=request.POST.get('inventoryaccntperunit')
                edit.status_stock=request.POST.get('satus')
                edit.minimum_stock=request.POST.get('minimum_stock')
                edit.unit=Unit.objects.get(unit=unit)
                edit.sales=Sales.objects.get(id=sel_acc)
                edit.purchase=Purchase.objects.get(id=cost_acc)
                edit.save()




            
            
            return redirect('detail', id=edit.id)


        return render(request,'edititem.html')




@login_required(login_url='login')
def detail(request,id):
    company=company_details.objects.get(user=request.user)
    user_id=request.user
    items=AddItem.objects.all()
    product=AddItem.objects.get(id=id)
    history=History.objects.filter(p_id=product.id)
    comments = Comments_item.objects.filter(item=id).order_by('-id')
    print(product.id)
    
    quantity = int(product.stock)
    price = int(product.p_price)
    stock = (quantity * price)
    
    
    context={
       "allproduct":items,
       "product":product,
       "history":history,
       'company':  company, 
       "comments":comments,
       'stock': stock,
    }
    
    return render(request,'demo.html',context)


@login_required(login_url='login')
def Action(request,id):
    user=request.user.id
    user=User.objects.get(id=user)
    viewitem=AddItem.objects.all()
    event=AddItem.objects.get(id=id)
    

    print(user)
    if request.method=='POST':
        action=request.POST['action']
        event.satus=action
        event.save()
        if action == 'active':
            History(user=user,message="Item marked as Active ",p=event).save()
        else:
            History(user=user,message="Item marked as inActive",p=event).save()
    return render(request,'item_view.html',{'view':viewitem})

@login_required(login_url='login')
def cleer(request,id):
    dl=AddItem.objects.get(id=id)
    dl.delete()
    return redirect('itemview')


@login_required(login_url='login')
def add_unit(request):
    if request.method == 'POST':
        unit_name = request.POST['unit_name']
        unit = Unit(unit=unit_name)  
        unit.save()  
        unit_id = unit.id  
        return JsonResponse({"unit_name": unit_name, "unit_id": unit_id})
    return render(request, "additem.html")



@login_required(login_url='login')
def add_sales(request):
    if request.method=='POST':
        Account_type  =request.POST['acc_type']
        Account_name =request.POST['acc_name']
        Acount_code =request.POST['acc_code']
        Account_desc =request.POST['acc_desc']        
        acc=Sales(Account_type=Account_type,Account_name=Account_name,Acount_code=Acount_code,Account_desc=Account_desc)
        acc.save()
        return redirect('additem')
    return render(request,'additem.html')

def sort_product_name(request,id):
   

    company=company_details.objects.get(user=request.user)
    user_id=request.user
    items=AddItem.objects.all().order_by('Name')
    product=AddItem.objects.get(id=id)
    history=History.objects.filter(p_id=product.id)
    comments = Comments_item.objects.filter(item=id).order_by('-id')
    print(product.id)
    
    quantity = int(product.stock)
    price = int(product.p_price)
    stock = (quantity * price)
    
    
    context={
       "allproduct":items,
       "product":product,
       "history":history,
       'company':  company, 
       "comments":comments,
       'stock': stock,
       
       
    }
    
    return render(request,'demo.html',context)
    
def sort_product_hsn(request,id):

    company=company_details.objects.get(user=request.user)
    user_id=request.user
    items=AddItem.objects.all().order_by('hsn')
    product=AddItem.objects.get(id=id)
    history=History.objects.filter(p_id=product.id)
    comments = Comments_item.objects.filter(item=id).order_by('-id')
    print(product.id)
    
    quantity = int(product.stock)
    price = int(product.p_price)
    stock = (quantity * price)
    
    
    context={
       "allproduct":items,
       "product":product,
       "history":history,
       'company':  company, 
       "comments":comments,
       'stock': stock,
       
       
    }
    
    return render(request,'demo.html',context)
    
def commentproduct(request, product_id):
    if request.method == 'POST':
        user = request.user
        product = AddItem.objects.get(id=product_id)
        new_comment = request.POST.get('comment')
        
        # Save the new comment to the database
        cmt=Comments_item.objects.create(item=product, user=user, content=new_comment)
        cmt.save()


        company=company_details.objects.get(user=request.user)
        user_id=request.user
        items=AddItem.objects.all()
        product=AddItem.objects.get(id=product_id)
        history=History.objects.filter(p_id=product.id)
        comments = Comments_item.objects.filter(item=product_id).order_by('-id')
        print(product.id)
    
        quantity = int(product.stock)
        price = int(product.p_price)
        stock = (quantity * price)
    
    
        context={
       "allproduct":items,
       "product":product,
       "history":history,
       'company':  company, 
       "comments":comments,
       'stock': stock,
       
       
        }
    
        return render(request,'demo.html',context)  

    # # Retrieve all the comments for the product
    # comments = Comments_item.objects.filter(item=product_id).values_list('content', flat=True)

    # response_data = {'comments': list(comments)}
    # return JsonResponse(response_data)
    
@login_required(login_url='login')
def vendor(request):
    company=company_details.objects.get(user=request.user)
    return render(request,'create_vendor.html',{'company':company})


@login_required(login_url='login')
def add_vendor(request):
    if request.method=="POST":
        vendor_data=vendor_table()
        vendor_data.salutation = request.POST.get('salutation')
        vendor_data.first_name=request.POST['first_name']
        vendor_data.last_name=request.POST['last_name']
        vendor_data.company_name=request.POST['company_name']
        vendor_data.vendor_display_name=request.POST['v_display_name']
        vendor_data.vendor_email=request.POST['vendor_email']
        vendor_data.vendor_wphone=request.POST['w_phone']
        vendor_data.vendor_mphone=request.POST['m_phone']
        vendor_data.skype_number=request.POST['skype_number']
        vendor_data.designation=request.POST['designation']
        vendor_data.department=request.POST['department']
        vendor_data.website=request.POST['website']
        vendor_data.gst_treatment=request.POST['gst']
        vendor_data.status="Active"

        x=request.POST['gst']
        if x=="Unregistered Business-not Registered under GST":
            vendor_data.pan_number=request.POST['pan_number']
            vendor_data.gst_number="null"
        else:
            vendor_data.gst_number=request.POST['gst_number']
            vendor_data.pan_number=request.POST['pan_number']

        vendor_data.source_supply=request.POST['source_supply']
        vendor_data.currency=request.POST['currency']
        vendor_data.opening_bal=request.POST['opening_bal']
        vendor_data.payment_terms=request.POST['payment_terms']

        user_id=request.user.id
        udata=User.objects.get(id=user_id)
        vendor_data.user=udata
        vendor_data.battention=request.POST['battention']
        vendor_data.bcountry=request.POST['bcountry']
        vendor_data.baddress=request.POST['baddress']
        vendor_data.bcity=request.POST['bcity']
        vendor_data.bstate=request.POST['bstate']
        vendor_data.bzip=request.POST['bzip']
        vendor_data.bphone=request.POST['bphone']
        vendor_data.bfax=request.POST['bfax']

        vendor_data.sattention=request.POST['sattention']
        vendor_data.scountry=request.POST['scountry']
        vendor_data.saddress=request.POST['saddress']
        vendor_data.scity=request.POST['scity']
        vendor_data.sstate=request.POST['sstate']
        vendor_data.szip=request.POST['szip']
        vendor_data.sphone=request.POST['sphone']
        vendor_data.sfax=request.POST['sfax']
        vendor_data.save()
# .......................................................adding to remaks table.....................
        vdata=vendor_table.objects.get(id=vendor_data.id)
        vendor=vdata
        rdata=remarks_table()
        rdata.remarks=request.POST['remark']
        rdata.user=udata
        rdata.vendor=vdata
        rdata.save()


#  ...........................adding multiple rows of table to model  ........................................................  
     
        salutation =request.POST.getlist('salutation[]')
        first_name =request.POST.getlist('first_name[]')
        last_name =request.POST.getlist('last_name[]')
        email =request.POST.getlist('email[]')
        work_phone =request.POST.getlist('wphone[]')
        mobile =request.POST.getlist('mobile[]')
        skype_number =request.POST.getlist('skype[]')
        designation =request.POST.getlist('designation[]')
        department =request.POST.getlist('department[]') 
        vdata=vendor_table.objects.get(id=vendor_data.id)
        vendor=vdata
        print("hi")
        print(salutation)
        if salutation != ['Select']:
            if len(salutation)==len(first_name)==len(last_name)==len(email)==len(work_phone)==len(mobile)==len(skype_number)==len(designation)==len(department):
                mapped2=zip(salutation,first_name,last_name,email,work_phone,mobile,skype_number,designation,department)
                mapped2=list(mapped2)
                print(mapped2)
                for ele in mapped2:
                    created = contact_person_table.objects.get_or_create(salutation=ele[0],first_name=ele[1],last_name=ele[2],email=ele[3],
                            work_phone=ele[4],mobile=ele[5],skype_number=ele[6],designation=ele[7],department=ele[8],user=udata,vendor=vendor)
            
       
                 
        return redirect('view_vendor_list')
        

def sample(request):
    print("hello")
    return redirect('base')

def view_vendor_list(request):
    company=company_details.objects.get(user=request.user)
    user_id=request.user.id
    udata=User.objects.get(id=user_id)
    data=vendor_table.objects.filter(user=udata)
    return render(request,'vendor_list.html',{'data':data,'company':company})

def view_vendor_details(request,pk):
    company=company_details.objects.get(user=request.user)
    user_id=request.user.id
    udata=User.objects.get(id=user_id)
    vdata1=vendor_table.objects.filter(user=udata)
    vdata2=vendor_table.objects.get(id=pk)
    mdata=mail_table.objects.filter(vendor=vdata2)
    ddata=doc_upload_table.objects.filter(user=udata,vendor=vdata2)
    cmt_data=comments_table.objects.filter(user=udata,vendor=vdata2)
    contact_persons = contact_person_table.objects.filter(user=udata,vendor=vdata2)

    fname = vdata2.first_name
    lname = vdata2.last_name
    fullname = fname + ' ' + lname
    v_email = vdata2.vendor_email
    name_and_id = fullname +' '+ str(vdata2.id) 
    id_and_name = str(vdata2.id) +' '+ fullname  

    print(fname)
    print(lname)
    print(fullname)
    print(v_email)
    print(name_and_id)

    vendor_credits = Vendor_Credits_Bills.objects.filter(user = udata,vendor_name = name_and_id)
    expence = ExpenseE.objects.filter(user = udata,vendor_id = pk)
    recurring_expense = Expense.objects.filter(vendor_id = pk)
    purchase_ordr = Purchase_Order.objects.filter(user = udata,vendor_name = name_and_id)
    paymnt_made = payment_made.objects.filter(user = udata,vendor_id = pk)
    purchase_bill = PurchaseBills.objects.filter(user = udata,vendor_name = fullname,vendor_email = v_email)
    recurring_bill = recurring_bills.objects.filter(user = udata,vendor_name = id_and_name)

    context = {
        'company':company,
        'vdata':vdata1,
        'vdata2':vdata2,
        'mdata':mdata,
        'ddata':ddata,
        'cmt_data':cmt_data,
        'contact_persons':contact_persons,
        'vendor_credits':vendor_credits,
        'expence':expence,
        'recurring_expense':recurring_expense,
        'purchase_ordr':purchase_ordr,
        'paymnt_made':paymnt_made,
        'purchase_bill':purchase_bill,
        'recurring_bill':recurring_bill,

    }

    return render(request,'vendor_details.html',context)

def add_comment(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    
    if request.method == 'POST':
        comment_text = request.POST.get('comment', '')
        Expense.objects.create(expense=expense, comment=comment_text)

    return redirect('show_recurring', expense_id=expense_id)

def sendmail(request):
    if request.method=='POST':
       subject=request.POST['subject']
       messag=request.POST['messag']
       sendto=request.POST['sendto']
       send_mail(subject,messag,settings.EMAIL_HOST_USER,
                 [sendto],fail_silently=False)
       return redirect('view_customr')



def edit_vendor(request,pk):
    company=company_details.objects.get(user=request.user)
    vdata=vendor_table.objects.get(id=pk)
    if remarks_table.objects.filter(vendor=vdata).exists() or contact_person_table.objects.filter(vendor=vdata).exists():
        if remarks_table.objects.filter(vendor=vdata).exists() and contact_person_table.objects.filter(vendor=vdata).exists():
            rdata=remarks_table.objects.get(vendor=vdata)
            pdata=contact_person_table.objects.filter(vendor=vdata)
            return render(request,'edit_vendor.html',{'vdata':vdata,'rdata':rdata,'pdata':pdata})
        else:
            if remarks_table.objects.filter(vendor=vdata).exists():
                rdata=remarks_table.objects.get(vendor=vdata)
                return render(request,'edit_vendor.html',{'vdata':vdata,'rdata':rdata})
            if contact_person_table.objects.filter(vendor=vdata).exists():
                pdata=contact_person_table.objects.filter(vendor=vdata)
                return render(request,'edit_vendor.html',{'vdata':vdata,'pdata':pdata})      
        
    else:
        return render(request,'edit_vendor.html',{'vdata':vdata,"company":company})


def edit_vendor_details(request,pk):
    if request.method=='POST':
        vdata=vendor_table.objects.get(id=pk)
        vdata.salutation=request.POST['salutation']
        vdata.first_name=request.POST['first_name']
        vdata.last_name=request.POST['last_name']
        vdata.company_name=request.POST['company_name']
        vdata.vendor_display_name=request.POST['v_display_name']
        vdata.vendor_email=request.POST['vendor_email']
        vdata.vendor_wphone=request.POST['w_phone']
        vdata.vendor_mphone=request.POST['m_phone']
        vdata.skype_number=request.POST['skype_number']
        vdata.designation=request.POST['designation']
        vdata.department=request.POST['department']
        vdata.website=request.POST['website']
        vdata.gst_treatment=request.POST['gst']
        if vdata.gst_treatment=="Unregistered Business-not Registered under GST":
            vdata.pan_number=request.POST['pan_number']
            vdata.gst_number="null"
        else:
            vdata.gst_number=request.POST['gst_number']
            vdata.pan_number=request.POST['pan_number']

        vdata.source_supply=request.POST['source_supply']
        vdata.currency=request.POST['currency']
        vdata.opening_bal=request.POST['opening_bal']
        vdata.payment_terms=request.POST['payment_terms']

        vdata.battention=request.POST['battention']
        vdata.bcountry=request.POST['bcountry']
        vdata.baddress=request.POST['baddress']
        vdata.bcity=request.POST['bcity']
        vdata.bstate=request.POST['bstate']
        vdata.bzip=request.POST['bzip']
        vdata.bphone=request.POST['bphone']
        vdata.bfax=request.POST['bfax']

        vdata.sattention=request.POST['sattention']
        vdata.scountry=request.POST['scountry']
        vdata.saddress=request.POST['saddress']
        vdata.scity=request.POST['scity']
        vdata.sstate=request.POST['sstate']
        vdata.szip=request.POST['szip']
        vdata.sphone=request.POST['sphone']
        vdata.sfax=request.POST['sfax']

        vdata.save()
             # .................................edit remarks_table ..........................
        vendor=vdata
        user_id=request.user.id
        udata=User.objects.get(id=user_id)
        if remarks_table.objects.filter(vendor=vdata).exists():
            rdata=remarks_table.objects.get(vendor=vdata)
            rdata.remarks=request.POST['remark']
            rdata.save()
        else:
            rdata=remarks_table()
            rdata.remarks=request.POST["remark"]
            rdata.vendor=vendor
            rdata.user=udata
            rdata.save()

            # .......................contact_person_table................ deleting existing entries and inserting  ...............

        pdata=contact_person_table.objects.filter(vendor=vdata)
        salutation =request.POST.getlist('salutation[]')
        first_name =request.POST.getlist('first_name[]')
        last_name =request.POST.getlist('last_name[]')
        email =request.POST.getlist('email[]')
        work_phone =request.POST.getlist('wphone[]')
        mobile =request.POST.getlist('mobile[]')
        skype_number =request.POST.getlist('skype[]')
        designation =request.POST.getlist('designation[]')
        department =request.POST.getlist('department[]') 

        vdata=vendor_table.objects.get(id=vdata.id)
        vendor=vdata
        user_id=request.user.id
        udata=User.objects.get(id=user_id)

        # .....  deleting existing rows......
        pdata.delete()
        if len(salutation)==len(first_name)==len(last_name)==len(email)==len(work_phone)==len(mobile)==len(skype_number)==len(designation)==len(department):
            mapped2=zip(salutation,first_name,last_name,email,work_phone,mobile,skype_number,designation,department)
            mapped2=list(mapped2)
            print(mapped2)
            for ele in mapped2:
                created = contact_person_table.objects.get_or_create(salutation=ele[0],first_name=ele[1],last_name=ele[2],email=ele[3],
                         work_phone=ele[4],mobile=ele[5],skype_number=ele[6],designation=ele[7],department=ele[8],user=udata,vendor=vendor)
        



        return redirect("view_vendor_list")

def upload_document(request,pk):
    if request.method=='POST':
        user_id=request.user.id
        udata=User.objects.get(id=user_id)
        vdata=vendor_table.objects.get(id=pk)
        title=request.POST['title']
        document=request.FILES.get('file')
        doc_data=doc_upload_table(user=udata,vendor=vdata,title=title,document=document)
        doc_data.save()
        return redirect("view_vendor_list")

def download_doc(request,pk):
    document=get_object_or_404(doc_upload_table,id=pk)
    response=HttpResponse(document.document,content_type='application/pdf')
    response['Content-Disposition']=f'attachment; filename="{document.document.name}"'
    return response

def cancel_vendor(request):
    return redirect("vendor")

def delete_vendor(request,pk):
    if comments_table.objects.filter(vendor=pk).exists():
        user2=comments_table.objects.filter(vendor=pk)
        user2.delete()
    if mail_table.objects.filter(vendor=pk).exists():
        user3=mail_table.objects.filter(vendor=pk)
        user3.delete()
    if doc_upload_table.objects.filter(vendor=pk).exists():
        user4=doc_upload_table.objects.filter(vendor=pk)
        user4.delete()
    if contact_person_table.objects.filter(vendor=pk).exists():
        user5=contact_person_table.objects.filter(vendor=pk)
        user5.delete()
    if remarks_table.objects.filter(vendor=pk).exists():
        user6=remarks_table.objects.filter(vendor=pk)
        user6.delete()
    
    user1=vendor_table.objects.get(id=pk)
    user1.delete()
    return redirect("view_vendor_list")
    
    

# view functions for retainer invoice

@login_required(login_url='login')
def add_customer(request):
    sb=payment_terms.objects.all()
    return render(request,'customer.html',{'sb':sb})


@login_required(login_url='login')
def retainer_invoice(request):
    company=company_details.objects.get(user=request.user)
    invoices=RetainerInvoice.objects.all().order_by('-id')
    context={'invoices':invoices,'company':company}
    return render(request,'retainer_invoice.html',context)


@login_required(login_url='login')
def add_invoice(request):
    company=company_details.objects.get(user_id=request.user)
    unit=Unit.objects.all()
    payments=payment_terms.objects.all()
    bank=Bankcreation.objects.all()
    customer1=customer.objects.all()   
    last_record = RetainerInvoice.objects.last()
    sales=Sales.objects.all()
    itm=AddItem.objects.all()

    purchase=Purchase.objects.all()
    if last_record ==None:
        reford = '01'
        reference = 'RET-01'
        remaining_characters='RET-'
    else:
        reference = 'RET-01'
        lastSalesNo = last_record.retainer_invoice_number
        last_two_numbers = int(lastSalesNo[-2:])+1
        remaining_characters = lastSalesNo[:-2]  
        if last_two_numbers < 10:
            reference = remaining_characters+'0'+str(last_two_numbers)
        else:
            reference = remaining_characters+str(last_two_numbers)
        if last_record.id+1 < 10:
            reford = '0'+ str(int(last_record.id)+1)
        else:
            reford = str(int(last_record.id)+1)

    context={'customer1':customer1,'pay':payments,'company':company,'bank':bank,'unit':unit,'reford':reford,'reference':reference,'remaining_characters':remaining_characters,'itm':itm,'sales':sales,'purchase':purchase}    
    return render(request,'add_invoice.html',context)

@login_required(login_url='login')
def create_invoice_draft(request):
    
    if request.method=='POST':
        user=request.user
        select=request.POST['customer_id']
        customer_name=customer.objects.get(id=select)
        customer_name11=customer_name.customerName
        customer_name1=customer_name11.upper()
        customer_mailid=request.POST['cx_mail']
        customer_placesupply=request.POST['cus_place1']
        retainer_invoice_number=request.POST['retainer-invoice-number']
        references=request.POST['references']
        retainer_invoice_date=request.POST['invoicedate']
        total_amount=request.POST.get('total')
        bal_amount=request.POST['balance']
        customer_notes=request.POST['customer_notes']
        terms_and_conditions=request.POST['terms']
        pay_opt1=request.POST['pay_method']
        acc_no = request.POST.get('acc_no', '')
        cheque_no = request.POST.get('chq_no', '')
        upi_id = request.POST.get('upi_id', '')
        if pay_opt1 != '':
            if pay_opt1 == 'cash':
                bankid="null"
            elif pay_opt1 == 'upi':
                bankid="null"
            elif pay_opt1 == 'cheque':
                bankid="null"
            else:
                bankid=pay_opt1.split(" ")[0]
                bank_id=Bankcreation.objects.filter(name=bankid,ac_no=acc_no)
                for i in bank_id:
                    bankname=i.name
                    b_id=i.id
                    bank=Bankcreation.objects.get(id=b_id)
       
        retainer_invoice=RetainerInvoice(
            user=user,customer_name=customer_name,customer_name1=customer_name1,customer_mailid=customer_mailid,customer_placesupply=customer_placesupply,retainer_invoice_number=retainer_invoice_number,refrences=references,retainer_invoice_date=retainer_invoice_date,total_amount=total_amount,balance=bal_amount,customer_notes=customer_notes,terms_and_conditions=terms_and_conditions)
    
        retainer_invoice.save()

        if pay_opt1 != '':
            if pay_opt1 == 'cash':
                ret_payment=retainer_payment_details(user=user,retainer=retainer_invoice,payment_opt=pay_opt1,acc_no=acc_no,cheque_no=cheque_no,upi_id=upi_id)
                ret_payment.save()
            elif pay_opt1 == 'cheque':
                ret_payment=retainer_payment_details(user=user,retainer=retainer_invoice,payment_opt=pay_opt1,acc_no=acc_no,cheque_no=cheque_no,upi_id=upi_id)
                ret_payment.save()
            elif pay_opt1 == 'upi':
                ret_payment=retainer_payment_details(user=user,retainer=retainer_invoice,payment_opt=pay_opt1,acc_no=acc_no,cheque_no=cheque_no,upi_id=upi_id)
                ret_payment.save()
            else:
                ret_payment=retainer_payment_details(user=user,retainer=retainer_invoice,payment_opt=bankname,acc_no=acc_no,bank=bank,cheque_no=cheque_no,upi_id=upi_id)
                ret_payment.save()

        description = request.POST.getlist('description[]')
        amount =request.POST.getlist('amount[]')
        itm=request.POST.getlist('item[]')
        qty=request.POST.getlist('quantity[]')
        if len(description)==len(amount)==len(itm)==len(qty):
            mapped = zip(description,amount,itm,qty)
            mapped=list(mapped)
            for ele in mapped:
                created = Retaineritems.objects.create(description=ele[0],amount=ele[1],itemname=ele[2],quantity=ele[3] ,retainer=retainer_invoice)
        else:
            pass

        return redirect('retainer_invoice')
        

         
@login_required(login_url='login')
def create_invoice_send(request):
    if request.method=='POST':
        user=request.user
        select=request.POST['customer_id']
        customer_name=customer.objects.get(id=select)
        customer_name11=customer_name.customerName
        customer_name1=customer_name11.upper()
        customer_mailid=request.POST['cx_mail']
        customer_placesupply=request.POST['cus_place1']
        retainer_invoice_number=request.POST['retainer-invoice-number']
        references=request.POST['references']
        retainer_invoice_date=request.POST['invoicedate']
        total_amount=request.POST.get('total')
        bal_amount=request.POST['balance']
        customer_notes=request.POST['customer_notes']
        terms_and_conditions=request.POST['terms']
        pay_opt1=request.POST['pay_method']
        tot_in_string = str(total_amount)

        acc_no=request.POST['acc_no']
        cheque_no=request.POST['chq_no']
        upi_id=request.POST['upi_id']


        if pay_opt1 != '':
            if pay_opt1 == 'cash':
                bankid="null"
            elif pay_opt1 == 'upi':
                bankid="null"
            elif pay_opt1 == 'cheque':
                bankid="null"
                bank_name1=0
            else:
                bankid=pay_opt1.split(" ")[0]
                bank_id=Bankcreation.objects.filter(name=bankid,ac_no=acc_no)
                for i in bank_id:
                    bankname=i.name
                    b_id=i.id
                    bank=Bankcreation.objects.get(id=b_id)

        retainer_invoice=RetainerInvoice(
        user=user,customer_name=customer_name,customer_name1=customer_name1,customer_mailid=customer_mailid,customer_placesupply=customer_placesupply,retainer_invoice_number=retainer_invoice_number,refrences=references,retainer_invoice_date=retainer_invoice_date,
        total_amount=total_amount,balance=bal_amount,customer_notes=customer_notes,terms_and_conditions=terms_and_conditions,is_draft=False,is_sent=True)
        retainer_invoice.save()

        if pay_opt1 != '':
            if pay_opt1 == 'cash':
                ret_payment=retainer_payment_details(user=user,retainer=retainer_invoice,payment_opt=pay_opt1,acc_no=acc_no,cheque_no=cheque_no,upi_id=upi_id)
                ret_payment.save()
            elif pay_opt1 == 'cheque':
                ret_payment=retainer_payment_details(user=user,retainer=retainer_invoice,payment_opt=pay_opt1,acc_no=acc_no,cheque_no=cheque_no,upi_id=upi_id)
                ret_payment.save()
            elif pay_opt1 == 'upi':
                ret_payment=retainer_payment_details(user=user,retainer=retainer_invoice,payment_opt=pay_opt1,acc_no=acc_no,cheque_no=cheque_no,upi_id=upi_id)
                ret_payment.save()
            else:
                ret_payment=retainer_payment_details(user=user,retainer=retainer_invoice,payment_opt=bankname,acc_no=acc_no,bank=bank,cheque_no=cheque_no,upi_id=upi_id)
                ret_payment.save()

        description = request.POST.getlist('description[]')
        amount =request.POST.getlist('amount[]')
        itm=request.POST.getlist('item[]')
        qty=request.POST.getlist('quantity[]')
        if len(description)==len(amount)==len(itm)==len(qty):
            mapped = zip(description,amount,itm,qty)
            mapped=list(mapped)
            for ele in mapped:
                created = Retaineritems.objects.create(description=ele[0],amount=ele[1],itemname=ele[2],quantity=ele[3] ,retainer=retainer_invoice)
        else:
            pass
        # return redirect('invoice_view',pk=retainer_invoice.id)
        cust_email = customer.objects.get(
            user=user, customerName=customer_name1).customerEmail
        print(cust_email)
        subject = 'Retainer Invoice'
        message = 'Dear Customer,\n Your Retainer Invoice has been Saved for a total amount of: ' + tot_in_string
        recipient = cust_email
        send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])
        return redirect('retainer_invoice')



@login_required(login_url='login')
def invoice_view(request,pk):
    user=request.user
    company=company_details.objects.get(user=user)
    invoices=RetainerInvoice.objects.all()
    invoice=RetainerInvoice.objects.get(id=pk)
    item=Retaineritems.objects.filter(retainer=pk)
    ret_comments=retainer_invoice_comments.objects.filter(retainer=invoice.id,user=user)

    if retainer_payment_details.objects.filter(retainer=invoice.id,user=user).exists():
        ret_payments=retainer_payment_details.objects.get(retainer=invoice.id)
        context={'invoices':invoices,'invoice':invoice,'item':item,'company':company,'ret_comments':ret_comments,'ret_payments':ret_payments}
    else:
        context={'invoices':invoices,'invoice':invoice,'item':item,'company':company,'ret_comments':ret_comments}

    return render(request,'invoice_view.html',context)



@login_required(login_url='login')
def retainer_template(request,pk):
    invoice=RetainerInvoice.objects.get(id=pk)
    return render(request,'template.html',{'invoice':invoice})

@login_required(login_url='login')
def retainer_edit_page(request,pk):
    company=company_details.objects.get(user_id=request.user)
    invoice=RetainerInvoice.objects.get(id=pk)
   
    payments=payment_terms.objects.all()
    cust_id=customer.objects.get(id=invoice.customer_name.id)
    custo_id=cust_id.id
    customer1=customer.objects.all()
    cust_gst_treat=invoice.customer_name.GSTTreatment
    cust_gstno=invoice.customer_name.GSTIN
    cust_placeofsupply=invoice.customer_placesupply
    items=Retaineritems.objects.filter(retainer=pk)
    banks=Bankcreation.objects.all()
    if retainer_payment_details.objects.filter(retainer=invoice.id).exists():
        pay_details=retainer_payment_details.objects.get(retainer=invoice.id) 
        # if Bankcreation.objects.filter(id=pay_details.bank.id).exists():
        #     bnk=Bankcreation.objects.get(id=pay_details.bank.id)
            # bnkid=bnk.id
        context={'invoice':invoice, 'customer1':customer1,'pay_detail':pay_details,'cust_gst_treat':cust_gst_treat,'cust_gstno':cust_gstno,'cust_placeofsupply':cust_placeofsupply,'items':items,'custo_id':custo_id,'payments':payments,'company':company,'banks':banks}
    else:
        context={'invoice':invoice, 'customer1':customer1,'cust_gst_treat':cust_gst_treat,'cust_gstno':cust_gstno,'cust_placeofsupply':cust_placeofsupply,'items':items,'custo_id':custo_id,'payments':payments,'company':company,'banks':banks}


    return render(request,'retainer_invoice_edit.html',context)



@login_required(login_url='login')
def retainer_update(request,pk):

    if request.method=='POST':
        retainer_invoice=RetainerInvoice.objects.get(id=pk)
        select=request.POST['customer_id']
        retainer_invoice.customer_name=customer.objects.get(id=select)
        retainer_invoice.customer_mailid=request.POST['cx_mail']
        retainer_invoice.customer_placesupply=request.POST['cus_place1']
        retainer_invoice.retainer_invoice_number=request.POST['retainer-invoice-number']
        retainer_invoice.refrences=request.POST['references']
        retainer_invoice.retainer_invoice_date=request.POST['invoicedate']
        retainer_invoice.total_amount=request.POST.get('total')
        retainer_invoice.balance=request.POST['balance']
        retainer_invoice.customer_notes=request.POST['customer_notes']
        retainer_invoice.terms_and_conditions=request.POST['terms']
    
        retainer_invoice.save()

        payment_opt=request.POST['pay_method']
        if payment_opt != '':
            pay_opt1=payment_opt.split(" ")[1]
            pay_opt2=payment_opt.split()[1:]
            if pay_opt1 == 'Cash':
                bankid="null"
            elif pay_opt1 == 'UPI':
                bankid="null"
            elif pay_opt1 == 'Cheque':
                bankid="null"
                bank_name1=0
            else:
                bnkid=payment_opt.split(" ")[0]
                # bankna=payment_opt.split()[1:]
                bank_name1=Bankcreation.objects.get(id=bnkid)
                bankname=bank_name1.name

            acc_no=request.POST['acc_no']
            cheque_no=request.POST['chq_no']
            upi_id=request.POST['upi_id']
        if payment_opt != '':
            if retainer_payment_details.objects.filter(retainer=retainer_invoice.id).exists():
                if pay_opt1 == 'Cash':
                    retainer_payment=retainer_payment_details.objects.get(retainer=retainer_invoice.id)
                    retainer_payment.payment_opt=pay_opt1
                    retainer_payment.acc_no=acc_no
                    retainer_payment.upi_id=upi_id
                    retainer_payment.cheque_no=cheque_no
                    retainer_payment.save()
                elif pay_opt1 == 'Cheque':
                    retainer_payment=retainer_payment_details.objects.get(retainer=retainer_invoice.id)
                    retainer_payment.payment_opt=pay_opt1
                    retainer_payment.acc_no=acc_no
                    retainer_payment.upi_id=upi_id
                    retainer_payment.cheque_no=cheque_no
                    retainer_payment.save()
                elif pay_opt1 == 'UPI':
                    retainer_payment=retainer_payment_details.objects.get(retainer=retainer_invoice.id)
                    retainer_payment.payment_opt=pay_opt1
                    retainer_payment.acc_no=acc_no
                    retainer_payment.upi_id=upi_id
                    retainer_payment.cheque_no=cheque_no
                    retainer_payment.save()
                else:
                    retainer_payment=retainer_payment_details.objects.get(retainer=retainer_invoice.id)
                    retainer_payment.payment_opt=bankname
                    retainer_payment.bank=bank_name1
                    retainer_payment.acc_no=acc_no
                    retainer_payment.upi_id=upi_id
                    retainer_payment.cheque_no=cheque_no
                    retainer_payment.save()
            else:
                if pay_opt1 != "UPI" or pay_opt1 != "Cash" or pay_opt1 != "Cheque":
                    bankid=payment_opt.split(" ")[0]
                    bank_name1=Bankcreation.objects.get(id=bankid)
                    bankname=bank_name1.name
                    bank_id=bank_name1.id
                    retainer_payment=retainer_payment_details(user=request.user,retainer=retainer_invoice,payment_opt=bankname,
                    bank=bank_name1,acc_no=acc_no,upi_id=upi_id,cheque_no=cheque_no)
                    retainer_payment.save()
                else:
                    retainer_payment=retainer_payment_details(user=request.user,retainer=retainer_invoice,payment_opt=pay_opt1,
                    acc_no=acc_no,upi_id=upi_id,cheque_no=cheque_no)
                    retainer_payment.save()



        objects_to_delete = Retaineritems.objects.filter(retainer=retainer_invoice.id)
        objects_to_delete.delete()

        description=request.POST.getlist('description[]')
        amount=request.POST.getlist('amount[]')

        if len(description) == len(amount):
              mapped = zip(description,amount)
              mapped = list(mapped)
              for element in mapped:
                created = Retaineritems.objects.create(
                    retainer=retainer_invoice, description=element[0], amount=element[1])

        
        # descriptions=request.POST.getlist('description[]')
        # amounts=request.POST.getlist('amount[]')
        



        # for i in range(len(descriptions)):
        #     description=descriptions[i]
        #     amount=amounts[i]
        #     obj,created=Retaineritems.objects.update_or_create(retainer=retainer_invoice,description=description,defaults={'amount':amount})
        #     obj.save()





        return redirect('invoice_view',retainer_invoice.id)

@login_required(login_url='login')
def mail_send(request,pk):

    if request.method=='POST':
        # comments=request.POST.getlist('mailcomments')
        # print(comments)
        files=request.FILES.getlist('files')
        email_to='nikhilaajayan76@gmail.com'
        subject='Retainer Invoice'
        message1=f'Please keep the attached\nretainer invoice for future use.\n\n'
        # message2='' 

        # for comment in comments:
        #     message2 += comment + '\n'

        messages=message1
        # +message2 

  

        email=EmailMessage(
            subject=subject,
            body=messages,
            to=[email_to]
        )
        
        for file in files:
            email.attach(file.name, file.read(), file.content_type)

        email.send() 
        print('bottom') 
        retainer_invoice=RetainerInvoice.objects.get(id=pk)
        retainer_invoice.is_draft=False
        retainer_invoice.is_sent=True
        retainer_invoice.save()  
        return redirect('retainer_invoice')
    
    return redirect('retainer_invoice')

@login_required(login_url='login')
def retaineritem_delete(request,pk):
    cur_user = request.user
    user1 = User.objects.get(id=cur_user.id)
    item = get_object_or_404(Retaineritems, id=pk)
    item.delete()
    return redirect('retainer_edit_page' ,pk=item.retainer.id)
    
@login_required(login_url='login')
def retainer_delete(request,pk):
    cur_user = request.user
    user1 = User.objects.get(id=cur_user.id)
    items=Retaineritems.objects.filter(retainer=pk)
    items.delete()
    retainer=RetainerInvoice.objects.get(id=pk)
    retainer.delete()
    return redirect('retainer_invoice')
        
            
def allestimates(request):
    user = request.user
    estimates = Estimates.objects.filter(user=user).order_by('-id')
    company = company_details.objects.get(user=user)
    context = {
        'estimates': estimates,
        'company': company,
    }
    # for i in estimates:
    #     print(i)

    return render(request, 'all_estimates.html', context)





def newestimate(request):
    user = request.user
    # print(user_id)
    
    company = company_details.objects.get(user=user)
    items = AddItem.objects.filter(user_id=user.id)
    customers = customer.objects.filter(user_id=user.id)
    # item=AddItem.objects.all()
    unit=Unit.objects.all()
    sales=Sales.objects.all()
    purchase=Purchase.objects.all()
    payments = payment_terms.objects.all()
    if Estimates.objects.all().exists():
        estimates_count = Estimates.objects.last().id
        next_count = estimates_count+1
    else:
        next_count=1 
    # estimates_count = Estimates.objects.last().id
    # next_count = estimates_count+1
    context = {'company': company,
               'items': items,
               'customers': customers,
               'count': next_count,
               'units':unit,
               'sales':sales,
               'purchase':purchase,
               'payments':payments,
               }

    return render(request,'new_estimate.html',context)


def itemdata_est(request):
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)
    company = company_details.objects.get(user=user)
    # print(company.state)
    id = request.GET.get('id')
    cust = request.GET.get('cust')
    print(id)
    print(cust)
    item = AddItem.objects.get(Name=id, user=user)
    rate = item.p_price
    place = company.state
    gst = item.intrastate
    igst = item.interstate
    place_of_supply = customer.objects.get(
        customerName=cust, user=user).placeofsupply
    return JsonResponse({"status": " not", 'place': place, 'rate': rate, 'pos': place_of_supply, 'gst': gst, 'igst': igst})
    return redirect('/')


def createestimate(request):
    print('hi1')
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)
    if request.method == 'POST':
        x=request.POST["hidden_state"]
        y=request.POST["hidden_cus_place"]

        cust_idd = request.POST['customer_name'].split(" ")[0]
        cust_name2=customer.objects.get(id=cust_idd)
        cust_name1=cust_name2.customerName
        cust_name=cust_name1.upper()
        customer_id=request.POST['customer_id']
        customer_id1=customer.objects.get(id=customer_id)
        customer_mailid=request.POST['customer_mail']
        customer_placesupply=request.POST['cus_place1']
        est_number = request.POST['estimate_number']
        reference = request.POST['reference']
        est_date = request.POST['estimate_date']
        exp_date = request.POST['expiry_date']

        if x == y:

          item = request.POST.getlist('item[]')
          hsn=request.POST.getlist('hsn[]')
          quantity = request.POST.getlist('quantity[]')
          rate = request.POST.getlist('rate[]')
          discount = request.POST.getlist('discount[]')
          tax = request.POST.getlist('tax[]')
          amount = request.POST.getlist('amount[]')
        
        else:
          itemm = request.POST.getlist('itemm[]')
          hsnn=request.POST.getlist('hsnn[]')
          quantityy = request.POST.getlist('quantityy[]')
          ratee = request.POST.getlist('ratee[]')
          discountt = request.POST.getlist('discountt[]')
          taxx = request.POST.getlist('taxx[]')
          amountt = request.POST.getlist('amountt[]')
        

        cust_note = request.POST['customer_note']
        sub_total = request.POST['subtotal']
        igst = request.POST['igst']
        sgst = request.POST['sgst']
        cgst = request.POST['cgst']
        tax_amnt = request.POST['total_taxamount']
        shipping = request.POST['shipping_charge']
        adjustment = request.POST['adjustment_charge']
        total = request.POST['total']
        tearms_conditions = request.POST['terms_conditions']
        attachment = request.FILES.get('file')
        status = 'Draft'
        convert_invoice='not_converted'
        convert_sales='not_converted'
        

        estimate = Estimates(user=user,customer=customer_id1,customer_name=cust_name,customer_mailid=customer_mailid,customer_placesupply=customer_placesupply,estimate_no=est_number, reference=reference, estimate_date=est_date, 
                             expiry_date=exp_date, sub_total=sub_total,igst=igst,sgst=sgst,cgst=cgst,tax_amount=tax_amnt, shipping_charge=shipping,
                             adjustment=adjustment, total=total, status=status, customer_notes=cust_note, terms_conditions=tearms_conditions, 
                             attachment=attachment,convert_invoice=convert_invoice,convert_sales=convert_sales)
        estimate.save()

        if x == y:

           if len(item) == len(hsn) == len(quantity) == len(rate) == len(discount) == len(tax) == len(amount):
             mapped = zip(item,hsn,quantity, rate, discount, tax, amount)
             mapped = list(mapped)
             for element in mapped:
                created = EstimateItems.objects.create(
                    estimate=estimate, item_name=element[0],hsn=element[1],quantity=element[2], rate=element[3], discount=element[4], tax_percentage=element[5], amount=element[6])
        else:
            if len(itemm) == len(hsnn) == len(quantityy) == len(ratee) == len(discountt) == len(taxx) == len(amountt):
             mapped = zip(itemm,hsnn,quantityy, ratee, discountt, taxx, amountt )
             mapped = list(mapped)
             for element in mapped:
                created = EstimateItems.objects.create(
                    estimate=estimate, item_name=element[0],hsn=element[1], quantity=element[2], rate=element[3], discount=element[4], tax_percentage=element[5], amount=element[6])

    return redirect('allestimates')


def create_and_send_estimate(request):
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)
    print("hello")
    if request.method == 'POST':
        x=request.POST["hidden_state"]
        y=request.POST["hidden_cus_place"]

        cust_idd = request.POST['customer_name'].split(" ")[0]
        cust_name2=customer.objects.get(id=cust_idd)
        cust_name1=cust_name2.customerName
        cust_name=cust_name1.upper()
        customer_id=request.POST['customer_id']
        customer_id1=customer.objects.get(id=customer_id)
        customer_mailid=request.POST['customer_mail']
        customer_placesupply=request.POST['cus_place1']
        est_number = request.POST['estimate_number']
        reference = request.POST['reference']
        est_date = request.POST['estimate_date']
        exp_date = request.POST['expiry_date']

        if x == y:

            item = request.POST.getlist('item[]')
            hsn=request.POST.getlist('hsn[]')
            quantity1 = request.POST.getlist('quantity[]')
            quantity = [float(x) for x in quantity1]
            rate1 = request.POST.getlist('rate[]')
            rate = [float(x) for x in rate1]
            discount1 = request.POST.getlist('discount[]')
            discount = [float(x) for x in discount1]
            tax1 = request.POST.getlist('tax[]')
            tax = [float(x) for x in tax1]
            amount1 = request.POST.getlist('amount[]')
            amount = [float(x) for x in amount1]
        else:
            itemm = request.POST.getlist('itemm[]')
            hsnn=request.POST.getlist('hsnn[]')
            quantityy1 = request.POST.getlist('quantityy[]')
            quantityy = [float(x) for x in quantityy1]
            ratee1 = request.POST.getlist('ratee[]')
            ratee = [float(x) for x in ratee1]
            discountt1 = request.POST.getlist('discountt[]')
            discountt = [float(x) for x in discountt1]
            taxx1 = request.POST.getlist('taxx[]')
            taxx = [float(x) for x in taxx1]
            amountt1 = request.POST.getlist('amountt[]')
            amountt = [float(x) for x in amountt1]
        

        cust_note = request.POST['customer_note']
        sub_total = float(request.POST['subtotal'])
        igst = float(request.POST.get('igst'))
        sgst = float(request.POST['sgst'])
        cgst = float(request.POST['cgst'])
        tax_amnt = float(request.POST['total_taxamount'])
        shipping = float(request.POST['shipping_charge'])
        adjustment = float(request.POST['adjustment_charge'])
        total = float(request.POST['total'])
        tearms_conditions = request.POST['terms_conditions']
        attachment = request.FILES.get('file')
        status = 'Sent'
        convert_invoice='not_converted'
        convert_sales='not_converted'
        tot_in_string = str(total)
        estimate = Estimates(user=user,customer=customer_id1,customer_name=cust_name,customer_mailid=customer_mailid,customer_placesupply=customer_placesupply,estimate_no=est_number, reference=reference, estimate_date=est_date, 
                             expiry_date=exp_date, sub_total=sub_total,igst=igst,sgst=sgst,cgst=cgst,tax_amount=tax_amnt, shipping_charge=shipping,
                             adjustment=adjustment, total=total, status=status, customer_notes=cust_note, terms_conditions=tearms_conditions, 
                             attachment=attachment,convert_invoice=convert_invoice,convert_sales=convert_sales)
        estimate.save()

        if x == y:
            if len(item)== len(hsn) == len(quantity) == len(rate) == len(discount) == len(tax) == len(amount):
              mapped = zip(item,hsn,quantity, rate, discount, tax, amount)
              mapped = list(mapped)
              for element in mapped:
                    created = EstimateItems.objects.create(
                    estimate=estimate,item_name=element[0],hsn=element[1],quantity=element[2], rate=element[3], discount=element[4], tax_percentage=element[5], amount=element[6])
        
        else:
            if len(itemm)== len(hsnn) == len(quantityy) == len(ratee) == len(discountt) == len(taxx) == len(amountt):
              mapped = zip(itemm,hsnn,quantityy,ratee,discountt,taxx,amountt)
              mapped = list(mapped)
              for element in mapped:
                    created = EstimateItems.objects.create(
                    estimate=estimate,item_name=element[0],hsn=element[1],quantity=element[2], rate=element[3], discount=element[4], tax_percentage=element[5], amount=element[6])

        cust_email = customer.objects.get(
            user=user, customerName=cust_name).customerEmail
        print(cust_email)
        subject = 'Estimate'
        message = 'Dear Customer,\n Your Estimate has been Saved for a total amount of: ' + tot_in_string
        recipient = cust_email
        send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])

    return redirect('allestimates')

def estimateslip(request, est_id):
    user = request.user
    company = company_details.objects.get(user=user)
    all_estimates = Estimates.objects.filter(user=user)
    estimate = Estimates.objects.get(id=est_id)
    
    items = EstimateItems.objects.filter(estimate=estimate)
    est_comments=estimate_comments.objects.filter(estimate=estimate.id,user=user)
    context = {
        'company': company,
        'all_estimates':all_estimates,
        'estimate': estimate,
        'items': items,
        'est_comments':est_comments,
    }
    return render(request, 'estimate_slip.html', context)




def editestimate(request,est_id):
    user = request.user
    company = company_details.objects.get(user=user)
    comp=company.state
    customers = customer.objects.filter(user_id=user.id)
    items = AddItem.objects.filter(user_id=user.id)
    estimate = Estimates.objects.get(id=est_id)
    
    cust=estimate.customer_placesupply
    cust_email=estimate.customer.customerEmail
    cust_id=estimate.customer.id
    cust_gst_treat=estimate.customer.GSTTreatment
    cust_gstno=estimate.customer.GSTIN
    unit=Unit.objects.all()
    sales=Sales.objects.all()
    purchase=Purchase.objects.all()
    payments = payment_terms.objects.all()

    est_items = EstimateItems.objects.filter(estimate=estimate)
    context = {
        'company': company,
        'estimate': estimate,
        'customers': customers,
        'items': items,
        'est_items': est_items,
        'comp':comp,
        'cust':cust,
        'cust_id':cust_id,
        'units':unit,
        'sales':sales,
        'purchase':purchase,
        'cust_email':cust_email,
        'payments':payments,
        'cust_gst_treat':cust_gst_treat,
        'cust_gstno':cust_gstno,
    }
    return render(request,'edit_estimate.html', context)

def updateestimate(request,pk):
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)

    if request.method == 'POST':
        x=request.POST["hidden_state"]
        y=request.POST["hidden_cus_place"]

        estimate = Estimates.objects.get(id=pk)
        
        convert_inv=estimate.convert_invoice
        convert_sal=estimate.convert_sales
        estimate.user = user
        cust_idd = request.POST['customer_name'].split(" ")[0]
        cust_name2=customer.objects.get(id=cust_idd)
        cust_name1=cust_name2.customerName
        cust_name=cust_name1.upper()
        estimate.customer_name=cust_name
        
        custr=request.POST['customer_id']
        customer_id=customer.objects.get(id=custr)
        estimate.customer=customer_id
        estimate.customer_mailid=request.POST['customer_mail']
        estimate.customer_placesupply=request.POST['cus_place1']
        estimate.estimate_no = request.POST['estimate_number']
        estimate.reference = request.POST['reference']
        estimate.estimate_date = request.POST['estimate_date']
        estimate.expiry_date = request.POST['expiry_date']

        estimate.customer_notes = request.POST['customer_note']
        estimate.sub_total = float(request.POST['subtotal'])
        estimate.igst = float(request.POST['igst'])
        estimate.sgst = float(request.POST['sgst'])
        estimate.cgst = float(request.POST['cgst'])
        estimate.tax_amount = float(request.POST['total_taxamount'])
        estimate.shipping_charge = float(request.POST['shipping_charge'])
        estimate.adjustment = float(request.POST['adjustment_charge'])
        estimate.total = float(request.POST['total'])
        estimate.terms_conditions = request.POST['terms_conditions']
        estimate.status = 'Draft'
        estimate.convert_invoice=convert_inv
        estimate.convert_sales=convert_sal

        old=estimate.attachment
        new=request.FILES.get('file')
        if old != None and new == None:
            estimate.attachment = old
        else:
            estimate.attachment = new

        estimate.save()

        if x == y:
          item = request.POST.getlist('item[]')
          hsn=request.POST.getlist('hsn[]')
          quantity1 = request.POST.getlist('quantity[]')
          quantity = [float(x) for x in quantity1]
          rate1 = request.POST.getlist('rate[]')
          rate = [float(x) for x in rate1]
          discount1 = request.POST.getlist('discount[]')
          discount = [float(x) for x in discount1]
          tax1 = request.POST.getlist('tax[]')
          tax = [float(x) for x in tax1]
          amount1 = request.POST.getlist('amount[]')
          amount = [float(x) for x in amount1]
        else:
          itemm = request.POST.getlist('itemm[]')
          hsnn=request.POST.getlist('hsnn[]')
          quantityy1 = request.POST.getlist('quantityy[]')
          quantityy = [float(x) for x in quantityy1]
          ratee1 = request.POST.getlist('ratee[]')
          ratee = [float(x) for x in ratee1]
          discountt1 = request.POST.getlist('discountt[]')
          discountt = [float(x) for x in discountt1]
          taxx1 = request.POST.getlist('taxx[]')
          taxx = [float(x) for x in taxx1]
          amountt1 = request.POST.getlist('amountt[]')
          amountt = [float(x) for x in amountt1]

        objects_to_delete = EstimateItems.objects.filter(estimate_id=estimate.id)
        objects_to_delete.delete()

        if x == y:
           if len(item)== len(hsn)== len(quantity) == len(rate) == len(discount) == len(tax) == len(amount):
              mapped = zip(item,hsn,quantity,rate,discount,tax,amount)
              mapped = list(mapped)
              for element in mapped:
                created = EstimateItems.objects.create(
                    estimate=estimate,item_name=element[0],hsn=element[1],quantity=element[2], rate=element[3], discount=element[4], tax_percentage=element[5], amount=element[6])
        else:
           if len(itemm)==len(hsnn)==len(quantityy)==len(ratee)==len(discountt)==len(taxx)==len(amountt):
              mapped = zip(itemm,hsnn,quantityy, ratee, discountt, taxx, amountt)
              mapped = list(mapped)
              for element in mapped:
                created = EstimateItems.objects.create(
                    estimate=estimate,item_name=element[0],hsn=element[1],quantity=element[2], rate=element[3], discount=element[4], tax_percentage=element[5], amount=element[6])
        
        if SalesOrder.objects.filter(estimate=pk).exists():
            sal=SalesOrder.objects.get(estimate=pk)
            # sal_item=sales_item.objects.filter(sale=sal.id)
            sal.customer_id=estimate.customer.id
            sal.reference=estimate.reference
            sal.sales_date=estimate.estimate_date
            sal.cxnote=estimate.customer_notes
            sal.subtotal=estimate.sub_total
            sal.igst=estimate.igst
            sal.cgst=estimate.cgst
            sal.sgst=estimate.sgst
            sal.t_tax=estimate.tax_amount
            sal.grandtotal=estimate.total
            sal.status=estimate.status
            sal.terms_condition=estimate.terms_conditions
            sal.file=estimate.attachment
            sal.sos=estimate.customer.placeofsupply
            sal.sh_charge=estimate.shipping_charge
            sal.save()

            objects_to_delete = sales_item.objects.filter(sale=sal.id)
            objects_to_delete.delete()

            items = EstimateItems.objects.filter(estimate=estimate.id)
            saleid = SalesOrder.objects.get(id=sal.id)
            for item in items:
                itemss = sales_item(product=item.item_name,quantity=item.quantity,hsn=item.hsn,tax=item.tax_percentage,
                                    total=item.amount,desc=item.discount,rate=item.rate,sale=saleid)
                itemss.save()
        
# .......................................................................................................        
        if invoice.objects.filter(estimate=pk).exists():
            invo=invoice.objects.get(estimate=pk)
            custt=estimate.customer.id
            custt_id=customer.objects.get(id=custt)
            invo.customer=custt_id
            invo.inv_date=estimate.estimate_date
            invo.due_date=estimate.expiry_date
            invo.cxnote=estimate.customer_notes
            invo.subtotal=estimate.sub_total
            invo.igst=estimate.igst
            invo.cgst=estimate.cgst
            invo.sgst=estimate.sgst
            invo.t_tax=estimate.tax_amount
            invo.subtotal=estimate.sub_total
            invo.grandtotal=estimate.total
            invo.status=estimate.status
            invo.terms_condition=estimate.terms_conditions
            invo.file=estimate.attachment
            invo.shipping_charge=estimate.shipping_charge
            invo.adjustment=estimate.adjustment
            invo.save()

            objects_to_delete = invoice_item.objects.filter(inv=invo.id)
            objects_to_delete.delete()

            items = EstimateItems.objects.filter(estimate=estimate.id)
            invid = invoice.objects.get(id=invo.id)
            for item in items:
                itemss = invoice_item(product=item.item_name,quantity=item.quantity,hsn=item.hsn,tax=item.tax_percentage,
                                    total=item.amount,discount=item.discount,rate=item.rate,inv=invid)
                itemss.save()





    return redirect('estimateslip',estimate.id)

def converttoinvoice(request,pk):
    user1 = request.user.id
    user=User.objects.get(id=user1)
    company = company_details.objects.get(user=user)
    estimate = Estimates.objects.get(id=pk)
    sale_status=estimate.convert_invoice
    if sale_status=='not_converted':
        new_status="converted"
    else:
        new_status="converted"
    items = EstimateItems.objects.filter(estimate=estimate.id)
    cust = customer.objects.get(customerName=estimate.customer_name,user=user)
    # invoice_count = invoice.objects.count()
    # next_no = invoice_count+1 
    if invoice.objects.all().exists():
        invoice_count = invoice.objects.last().id
        count=invoice_count+1
        inv_string="INV-"
        next_no=inv_string+str(count)
    else:
        count=1 
        inv_string="INV-"
        next_no=inv_string+str(count)

    inv = invoice(customer=cust,invoice_no=next_no,order_no=0,
                      inv_date=estimate.estimate_date,due_date=estimate.expiry_date,igst=estimate.igst,cgst=estimate.cgst,
                      sgst=estimate.sgst,t_tax=estimate.tax_amount,subtotal=estimate.sub_total,grandtotal=estimate.total,
                      cxnote=estimate.customer_notes,file=estimate.attachment,terms_condition=estimate.terms_conditions,
                      status=estimate.status,estimate=estimate.id,user=user)
    inv.save()
    inv = invoice.objects.get(invoice_no=next_no,customer=cust)
    for item in items:
        items = invoice_item(product=item.item_name,quantity=item.quantity,hsn=item.hsn,tax=item.tax_percentage,
                             total=item.amount,discount=item.discount,rate=item.rate,inv=inv)
        items.save()
    estimate.convert_invoice=new_status
    estimate.save()
    
    return redirect('allestimates')




def add_customer_for_estimate(request):
    sb=payment_terms.objects.all()
    return render(request,'customer_est.html',{'sb':sb})
    
def entr_custmr_for_estimate(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            type=request.POST.get('type')
            txtFullName=request.POST['txtFullName']
            cpname=request.POST['cpname']
           
            email=request.POST['email']            
            wphone=request.POST['fname']
            mobile=request.POST.get('lname')
            skname=request.POST.get('skname')
            desg=request.POST.get('desg')      
            dept=request.POST.get('dept')
            wbsite=request.POST.get('wbsite')

            gstt=request.POST.get('gstt')
            posply=request.POST.get('posply')
            tax1=request.POST.get('tax1')
            crncy=request.POST.get('crncy')
            obal=request.POST.get('obal')

            select=request.POST.get('pterms')
            pterms=payment_terms.objects.get(id=select)
            pterms=request.POST.get('pterms')

            plst=request.POST.get('plst')
            plang=request.POST.get('plang')
            fbk=request.POST.get('fbk')
            twtr=request.POST.get('twtr')
        
            atn=request.POST.get('atn')
            ctry=request.POST.get('ctry')
            
            addrs=request.POST.get('addrs')
            addrs1=request.POST.get('addrs1')
            bct=request.POST.get('bct')
            bst=request.POST.get('bst')
            bzip=request.POST.get('bzip')
            bpon=request.POST.get('bpon')
            bfx=request.POST.get('bfx')

            sal=request.POST.get('sal')
            ftname=request.POST.get('ftname')
            ltname=request.POST.get('ltname')
            mail=request.POST.get('mail')
            bworkpn=request.POST.get('bworkpn')
            bmobile=request.POST.get('bmobile')

            bskype=request.POST.get('bskype')
            bdesg=request.POST.get('bdesg')
            bdept=request.POST.get('bdept')
            u = User.objects.get(id = request.user.id)

          
            ctmr=customer(customerName=txtFullName,customerType=type,
                        companyName=cpname,customerEmail=email,customerWorkPhone=wphone,
                         customerMobile=mobile,skype=skname,designation=desg,department=dept,
                           website=wbsite,GSTTreatment=gstt,placeofsupply=posply, Taxpreference=tax1,
                             currency=crncy,OpeningBalance=obal,PaymentTerms=pterms,
                                PriceList=plst,PortalLanguage=plang,Facebook=fbk,Twitter=twtr,
                                 Attention=atn,country=ctry,Address1=addrs,Address2=addrs1,
                                  city=bct,state=bst,zipcode=bzip,phone1=bpon,
                                   fax=bfx,CPsalutation=sal,Firstname=ftname,
                                    Lastname=ltname,CPemail=mail,CPphone=bworkpn,
                                    CPmobile= bmobile,CPskype=bskype,CPdesignation=bdesg,
                                     CPdepartment=bdept,user=u )
            ctmr.save()  
            
            return redirect("newestimate")
        return redirect("newestimate")
    
def payment_term_for_estimate(request):
    if request.method=='POST':
        term=request.POST.get('term')
        day=request.POST.get('day')
        ptr=payment_terms(Terms=term,Days=day)
        ptr.save()
        return redirect("add_customer_for_estimate")

    
@login_required(login_url='login')
def payment_term(request):
    if request.method=='POST':
        term=request.POST.get('term')
        day=request.POST.get('day')
        ptr=payment_terms(Terms=term,Days=day)
        ptr.save()
        return redirect("add_customer")

@login_required(login_url='login')
def invoiceview(request):
    user=request.user
    company=company_details.objects.get(user=request.user)
    invoicev=invoice.objects.filter(user=user)
    
    if not payment_terms.objects.filter(Terms='net 15').exists(): 
       payment_terms(Terms='net 15',Days=15).save()
    if not payment_terms.objects.filter(Terms='due end of month').exists():
        payment_terms(Terms='due end of month',Days=60).save()
    elif not  payment_terms.objects.filter(Terms='net 30').exists():
        payment_terms(Terms='net 30',Days=30).save() 
    
    
    context={
        'invoice':invoicev,
        'company':company,
        
    }
    return render(request,'invoiceview.html',context)

@login_required(login_url='login')
def detailedview(request,id):
    user=request.user
    inv_dat=invoice.objects.filter(user=user)
    inv_master=invoice.objects.get(id=id)
    invoiceitem=invoice_item.objects.filter(inv_id=id)
    company=company_details.objects.get(user_id=request.user.id)
    inv_comments=invoice_comments.objects.filter(user=user,invoice=id)
    
    
    context={
        'inv_dat':inv_dat,
        'invoiceitem':invoiceitem,
        'company':company,
        'invoice':inv_master,
        'inv_comments':inv_comments,
    }
    return render(request,'invoice_det.html',context)

@login_required(login_url='login')

def dele(request,pk):
    d=invoice.objects.get(id=pk)
    d.delete()
    return redirect('invoiceview')

@login_required(login_url='login')

def addinvoice(request):
    c=customer.objects.all()
    p=AddItem.objects.all()
    i=invoice.objects.all()
    pay=payment.objects.all()
    if not payment.objects.filter(term='net 15').exists(): 
       payment(term='net 15',days=15).save()
    if not payment.objects.filter(term='due end of month').exists():
        payment(term='due end of month',days=60).save()
    elif not  payment.objects.filter(term='net 30').exists():
        payment(term='net 30',days=30).save() 
    


    
            
            
            
            
    context={
        'c':c,
        'p':p,
        'i':i,
        'pay':pay,
        
    }
       
    return render(request,'createinvoice.html',context)


@login_required(login_url='login')
def add_prod(request):     #updation
    c = customer.objects.all()
    company = company_details.objects.get(user=request.user.id)
    p = AddItem.objects.all()
    i = invoice.objects.all()
    payments = payment_terms.objects.all()
    sales = Sales.objects.all()
    purchase = Purchase.objects.all()
    unit = Unit.objects.all()
    banks = Bankcreation.objects.all()
    if invoice.objects.all().exists():
        invoice_count = invoice.objects.last().id
        count = invoice_count
    else:
        count = 1
    # invoice_count = invoice.objects.last().id
    # count=invoice_count+1
    if not payment_terms.objects.filter(Terms='net 15').exists():
       payment_terms(Terms='net 15', Days=15).save()
    if not payment_terms.objects.filter(Terms='due end of month').exists():
        payment_terms(Terms='due end of month', Days=60).save()
    elif not payment_terms.objects.filter(Terms='net 30').exists():
        payment_terms(Terms='net 30', Days=30).save()

    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            x = request.POST["hidden_state"]
            y = request.POST["hidden_cus_place"]
            print("Value of x:", x)
            print("Value of y:", y)
            c = request.POST['cx_name']
            print(c)
            cus = customer.objects.get(id=c)
            print(cus.id)
            custo = cus
            invoice_no = request.POST['inv_no']
            terms = request.POST['term']
            # term=payment_terms.objects.get(id=terms)
            order_no = request.POST['ord_no']
            cheque_number = ''
            upi_id = ''
            payment_method = request.POST['payment_method']
            if payment_method == 'cash':
                pass
                # Handle cash related operations here
            elif payment_method == 'cheque':
                cheque_number = request.POST.get('cheque_number', '')
                # Handle cheque related operations here
            elif payment_method == 'upi':
                upi_id = request.POST.get('upi_id', '')
                # Handle UPI related operations here
            elif payment_method == 'bank':
                bank_id = request.POST.get('bank_name')
                cheque_number = request.POST.get('cheque_number', '')
                upi_id = request.POST.get('upi_id', '')
                
            else:
                
                pass

            
            inv_date_str = request.POST['inv_date']  # Retrieve the invoice date as a string
            due_date_str = request.POST['due_date']  # Retrieve the due date as a string
            
            inv_date_str = request.POST.get('inv_date', "")
            due_date_str = request.POST.get('due_date', "")

            inv_date = None
            due_date = None

            if inv_date_str and due_date_str:
                try:
                    inv_date = datetime.strptime(inv_date_str, '%Y-%m-%d')
                    due_date = datetime.strptime(due_date_str, '%Y-%m-%d')

                    cxnote = request.POST.get('customer_note', "")
                    subtotal = request.POST.get('subtotal', "")
                    igst = request.POST.get('igst', "")
                    cgst = request.POST.get('cgst', "")
                    sgst = request.POST.get('sgst', "")
                    totaltax = request.POST.get('totaltax', "")
                    t_total = request.POST.get('t_total', "")
                    file = request.FILES.get('file', None)
                    tc = request.POST.get('ter_cond', "")
                    status = request.POST.get('sd', "")
                    shipping_charge = request.POST.get('shipping_charge', "")
                    adjustment_charge = request.POST.get('adjustment_charge', "")
                    paid_amount = request.POST.get('paid_amount', "")
                    balance = request.POST.get('balance', "")

                    # Code for different scenarios based on x and y values
                    
    # Save the invoice_payment instance to persist the changes in the database
    

                        
                    

                    inv = invoice(user=user, customer=custo, invoice_no=invoice_no, terms=terms, order_no=order_no, 
                                  inv_date=inv_date, due_date=due_date, cxnote=cxnote, subtotal=subtotal, 
                                  igst=igst, cgst=cgst, sgst=sgst, t_tax=totaltax, grandtotal=t_total, 
                                  status=status, terms_condition=tc, file=file, adjustment=adjustment_charge, shipping_charge=shipping_charge, paid_amount=paid_amount, balance=balance)
                    inv.save()
                    
                    invoice_payment = InvoicePayment(
                                        invoice=inv,
                                        payment_method=payment_method,
                                        cheque_number=cheque_number,
                                        upi_id=upi_id,
                                    )
                    if payment_method == 'bank' and bank_id:
                        bank_instance = Bankcreation.objects.get(id=bank_id)
                        invoice_payment.bank = bank_instance
                    invoice_payment.save()

                    # Additional code for creating invoice items

                except ValueError as e:
                    print(f"Value Error: {e}")

           

            if x == y:
                item = request.POST.getlist("item[]")
                print("Item List:", item) 

                hsn = request.POST.getlist("hsn[]")
                quantity = request.POST.getlist("quantity[]")
                rate = request.POST.getlist("rate[]")
                discount = request.POST.getlist("discount[]")
                tax = request.POST.getlist("tax[]")
                amount = request.POST.getlist("amount[]")
                print('amount:', amount)
                for i in range(len(item)):
                    print(f"Item: {item[i]}, HSN: {hsn[i]}, Quantity: {quantity[i]}, Rate: {rate[i]}, Discount: {discount[i]}, Tax: {tax[i]}, Amount: {amount[i]}")

                    
                # term=payment_terms.objects.get(id=term.id)
            else:
                itemm = request.POST.getlist('itemm[]')
                hsnn = request.POST.getlist('hsnn[]')
                quantityy = request.POST.getlist('quantityy[]')
                ratee = request.POST.getlist('ratee[]')
                discountt = request.POST.getlist('discountt[]')
                taxx = request.POST.getlist('taxx[]')
                amountt = request.POST.getlist('amountt[]')
                for i in range(len(itemm)):
                    print(f"Item: {itemm[i]}, HSN: {hsnn[i]}, Quantity: {quantityy[i]}, Rate: {ratee[i]}, Discount: {discountt[i]}, Tax: {taxx[i]}, Amount: {amountt[i]}")

                # term=payment_terms.objects.get(id=term.id)

            
            
               
            if x == y:
                print("Length of invoiceitem.item: ", len(item))
                print("Length of invoiceitem.hsn: ", len(hsn))
                print("Length of invoiceitem.quantity: ", len(quantity))
                print("Length of invoiceitem.desc: ", len(discount))
                print("Length of invoiceitem.tax: ", len(tax))
                print("Length of invoiceitem.amount: ", len(amount))
                print("Length of invoiceitem.rate: ", len(rate))
                print("Value of x: ", x)
                print("Value of y: ", y)
                
                inv_id = invoice.objects.get(id=inv.id)
                if len(item) == len(hsn) == len(quantity) == len(discount) == len(tax) == len(amount) == len(rate):
                    mapped = list(zip(item, hsn, quantity, discount, tax, amount, rate))
                    print(mapped)
                    created_objects = [
                        invoice_item(
                            inv=inv_id,
                            product=element[0],
                            hsn=element[1],
                            quantity=element[2],
                            discount=element[3],
                            tax=element[4],
                            total=element[5],
                            rate=element[6],
                        )
                        for element in mapped
                    ]
                    invoice_item.objects.bulk_create(created_objects)
                    return redirect('invoiceview')     

            else:
                inv_id = invoice.objects.get(id=inv.id)
                if len(itemm) == len(hsnn) == len(quantityy) == len(discountt) == len(taxx) == len(amountt) == len(ratee):
                    mapped = list(zip(itemm, hsnn, quantityy, discountt, taxx, amountt, ratee))
                    created_objects = [
                        invoice_item(
                            inv=inv_id,
                            product=element[0],
                            hsn=element[1],
                            quantity=element[2],
                            discount=element[3],
                            tax=element[4],
                            total=element[5],
                            rate=element[6],
                        )
                        for element in mapped
                    ]
                    invoice_item.objects.bulk_create(created_objects)
                    return redirect('invoiceview')   


            

    context = {
        'c': c,
        'p': p,
        'i': i,
        'company': company,
        'sales': sales,
        'purchase': purchase,
        'units': unit,
        'count': count,
        'payments': payments,
        'banks' : banks
    }
    return render(request, 'createinvoice.html', context)


@login_required(login_url='login')

def add_payment(request):
    if request.method=='POST':
            terms=request.POST.get()
    return redirect('add_prod')


@login_required(login_url='login')

def add_cx(request):
    if request.user.is_authenticated:
        if request.method=='POST':
                user=request.user.id
                user=User.objects.get(id=user)
                print(user)
                name=request.POST.get('name')
                email=request.POST.get('email')
                pos=request.POST.get('position')
                state=request.POST.get('state')
                com_name=request.POST.get('company')
                customer(customerName=name,customerEmail=email,placeofsupply=pos,state=state,companyName=com_name,user_id=user.id).save()
        return redirect('add_prod')




@login_required(login_url='login')
def edited_prod(request, id):
    print(id)
    user = request.user
    c = customer.objects.all()
    p = AddItem.objects.all()
    invoiceitem = invoice_item.objects.filter(inv_id=id)
    invoic = invoice.objects.get(id=id)
    cust = invoic.customer.placeofsupply
    cust_id = invoic.customer.id
    pay = payment_terms.objects.all()
    sales = Sales.objects.all()
    purchase = Purchase.objects.all()
    invpay = InvoicePayment.objects.filter(invoice_id=id)

    invp = invpay[0] if invpay else None
    banks = Bankcreation.objects.all()
    unit = Unit.objects.all()
    
    company = company_details.objects.get(user=request.user.id)
    comp = company.state
    

    if request.method == 'POST':
        x = request.POST["hidden_state"]
        y = request.POST["hidden_cus_place"]
        print("Value of x:", x)
        print("Value of y:", y)
        u = request.user.id
        u2 = User.objects.get(id=u)
        c = request.POST['cx_name']
        cus = customer.objects.get(id=c)

        invoic.customer = cus
        invoic.user = u2
        invoic.terms = request.POST.get('term', "")
        invoic.inv_date = request.POST.get('inv_date', "")
        invoic.due_date = request.POST.get('due_date', "")
        invoic.cxnote = request.POST.get('customer_note', "")
        invoic.subtotal = request.POST.get('subtotal', "")
        invoic.igst = request.POST.get('igst', "")
        invoic.cgst = request.POST.get('cgst', "")
        invoic.sgst = request.POST.get('sgst', "")
        invoic.t_tax = request.POST.get('totaltax', "")
        invoic.grandtotal = request.POST.get('t_total', "")
        invoic.paid_amount = request.POST.get('paid_amount', "")
        invoic.balance = request.POST.get('balance', "")

        old = invoic.file
        new = request.FILES.get('file')
        if old and not new:
            invoic.file = old
        else:
            invoic.file = new

        invoic.terms_condition = request.POST.get('ter_cond')

        status = request.POST['sd']
        if status == 'draft':
            invoic.status = status
        else:
            invoic.status = status

        invoic.save()
        
        if invp:
            invp.payment_method = request.POST.get('payment_method', "")
            if invp.payment_method == 'cash':
                pass
            elif invp.payment_method == 'cheque':
                invp.cheque_number = request.POST.get('cheque_number', '')
            elif invp.payment_method == 'upi':
                invp.upi_id = request.POST.get('upi_id', '')
            elif invp.payment_method == 'bank':
                invp.bank_id = request.POST.get('bank_name', "")

            invp.save()

        print("/////////////////////////////////////////////////////////")
        if x == y:
            invoiceitem.item = request.POST.getlist('item[]')
            invoiceitem.hsn = request.POST.getlist('hsn[]')
            invoiceitem.quantity = request.POST.getlist('quantity[]')
            invoiceitem.rate = request.POST.getlist('rate[]')
            invoiceitem.desc = request.POST.getlist('desc[]')
            invoiceitem.tax = request.POST.getlist('tax[]')
            invoiceitem.amount = request.POST.getlist('amount[]')
            
            print("hai")
            
        else:
            invoiceitem.itemm = request.POST.getlist('itemm[]')
            invoiceitem.hsnn = request.POST.getlist('hsnn[]')
            invoiceitem.quantityy = request.POST.getlist('quantityy[]')
            invoiceitem.ratee = request.POST.getlist('ratee[]')
            invoiceitem.descc = request.POST.getlist('descc[]')
            invoiceitem.taxx = request.POST.getlist('taxx[]')
            invoiceitem.amountt = request.POST.getlist('amountt[]')
            
            
        if x == y:
            print("manage")
            print("Length of invoiceitem.item: ", len(invoiceitem.item))
            print("Length of invoiceitem.hsn: ", len(invoiceitem.hsn))
            print("Length of invoiceitem.quantity: ", len(invoiceitem.quantity))
            print("Length of invoiceitem.desc: ", len(invoiceitem.desc))
            print("Length of invoiceitem.tax: ", len(invoiceitem.tax))
            print("Length of invoiceitem.amount: ", len(invoiceitem.amount))
            print("Length of invoiceitem.rate: ", len(invoiceitem.rate))
            print("Value of x: ", x)
            print("Value of y: ", y)
            if len(invoiceitem.item) == len(invoiceitem.hsn) == len(invoiceitem.quantity) == len(invoiceitem.desc) == len(invoiceitem.tax) == len(invoiceitem.amount) == len(invoiceitem.rate):
                print("11")
                mapped = zip(invoiceitem.item, invoiceitem.hsn, invoiceitem.quantity, invoiceitem.desc, invoiceitem.tax, invoiceitem.amount, invoiceitem.rate)
                mapped = list(mapped)
                for element in mapped:
                    created = invoice_item.objects.get_or_create(inv=invoic, product=element[0], hsn=element[1],
                                                                 quantity=element[2], discount=element[3], tax=element[4],
                                                                 total=element[5], rate=element[6])
                    print("moveon")

                return redirect('invoice_overview', id)

        else:
            if len(invoiceitem.itemm) == len(invoiceitem.hsnn) == len(invoiceitem.quantityy) == len(invoiceitem.descc) == len(invoiceitem.taxx) == len(invoiceitem.amountt) == len(invoiceitem.ratee):
                mapped = zip(invoiceitem.itemm, invoiceitem.hsnn, invoiceitem.quantityy, invoiceitem.descc, invoiceitem.taxx, invoiceitem.amountt, invoiceitem.ratee)
                mapped = list(mapped)
                for element in mapped:
                    created = invoice_item.objects.get_or_create(inv=invoic, product=element[0], hsn=element[1],
                                                                 quantity=element[2], discount=element[3], tax=element[4],
                                                                 total=element[5], rate=element[6])

                return redirect('invoice_overview', id)

    context = {
        'user': user,
        'c': c,
        'p': p,
        'inv': invoiceitem,
        'i': invoic,
        'pay': pay,
        'sales': sales,
        'purchase': purchase,
        'units': unit,
        'company': company,
        'cust': cust,
        'comp': comp,
        'custo_id': cust_id,
        'invpay': invpay,
        'banks': banks,
        'invp':invp,
    }

    return render(request, 'invoiceedit.html', context)

@login_required(login_url='login')

def edited(request,id):
    c=customer.objects.all()
    p=AddItem.objects.all()
    invoiceitem=invoice_item.objects.filter(inv_id=id)
    inv=invoice.objects.get(id=id)
    context={
        'c':c,
        'p':p,
        'inv':invoiceitem,
        'inv':inv,
        
    }
    
    return render(request,'editinvoice.html')



@login_required(login_url='login')
def itemdata(request):
    cur_user = request.user.id
    user = User.objects.get(id=cur_user)
    company = company_details.objects.get(user = user)
    id = request.GET.get('id')
    cust = request.GET.get('cust')
    cus=customer.objects.get(id=cust)

    try:
        item = AddItem.objects.get(Name=id)
        rate = item.s_price
        place=company.state
        gst = item.intrastate
        igst = item.interstate
        desc=item.s_desc
        mail=cus.customerEmail
        stock=item.stock
        hsn=item.hsn

        place_of_supply = customer.objects.get(id=cust).placeofsupply
        return JsonResponse({"status":" not",'mail':mail,'desc':desc,'place':place,'rate':rate,'pos':place_of_supply,'gst':gst,'igst':igst,
                            'stock':stock,'hsn':hsn})
    except AddItem.DoesNotExist:
        rate = 0
        place=''
        gst = 0
        igst = 0
        desc=0
        mail=''
        stock=0
        hsn=0
        place_of_supply = customer.objects.get(id=cust).placeofsupply
        return JsonResponse({"status":" not",'mail':mail,'desc':desc,'place':place,'rate':rate,'pos':place_of_supply,'gst':gst,'igst':igst,
                            'stock':stock,'hsn':hsn})

@login_required(login_url='login')
def itemdata_ri(request):
    cur_user = request.user.id
    user = User.objects.get(id=cur_user)
    company = company_details.objects.get(user = user)
    id = request.GET.get('id')

    try:
        item = AddItem.objects.get(Name=id)
        rate = item.s_price
        place=company.state
        gst = item.intrastate
        igst = item.interstate
        desc=item.s_desc
        stock=item.stock
        hsn=item.hsn

        return JsonResponse({"status":" not",'desc':desc,'place':place,'rate':rate,'gst':gst,'igst':igst,
                            'stock':stock,'hsn':hsn})
    except AddItem.DoesNotExist:
        rate = 0
        place=''
        gst = 0
        igst = 0
        desc=0
        mail=''
        stock=0
        hsn=0
        return JsonResponse({"status":" not",'desc':desc,'place':place,'rate':rate,'gst':gst,'igst':igst,
                            'stock':stock,'hsn':hsn})

def convert_to_invoice(request,pk):
    sale = SalesOrder.objects.get(id=pk)
    inv_id = invoice.objects.last()
    user = User.objects.get(id = request.user.id)
    custo = customer.objects.get(id=sale.customer.id)

    if inv_id == None:
        invoice_no = "INV-01"
        order_no = 1
    else:
        if (inv_id.id<10):
            invoice_no = "INV-0"+str(inv_id.id+1)
            order_no = str(inv_id.id+1)
        else:
            invoice_no = "INV-"+str(inv_id.id+1)
            order_no = str(inv_id.id+1)

    terms = sale.terms.id
    inv_date = sale.sales_date
    due_date = sale.ship_date
    cxnote = sale.cxnote
    subtotal = sale.subtotal
    igst = sale.igst
    cgst = sale.cgst
    sgst = sale.sgst
    totaltax = sale.t_tax
    t_total = sale.grandtotal
    status = sale.status
    tc = sale.terms_condition
    file = sale.file

    inv=invoice(user=user,customer=custo,invoice_no=invoice_no,terms=terms,order_no=order_no,inv_date=inv_date,due_date=due_date,
                cxnote=cxnote,subtotal=subtotal,igst=igst,cgst=cgst,sgst=sgst,t_tax=totaltax,grandtotal=t_total,status=status,
                terms_condition=tc,file=file)
    inv.save()
    invitem_id = invoice.objects.last()


    sale.complete_status = 1
    sale.save()
    item =sales_item.objects.filter(sale_id=sale)
    for i in item:
        invitem=invoice_item(product=i.product,quantity=i.quantity,hsn=i.hsn,tax=i.tax,total=i.total,discount=i.desc,rate=i.rate,inv_id=invitem_id.id)
        invitem.save()

    return redirect('view_sales_order')

def convert_to_recinvoice(request,pk):
    sale = SalesOrder.objects.get(id=pk)
    recinv_id = Recurring_invoice.objects.last()
    user = User.objects.get(id = request.user.id)
    custo = customer.objects.get(id=sale.customer.id)

    if recinv_id == None:
        reinvoiceno = "REC-01"
        order_num = 1
    else:
        if (recinv_id.id<10):
            reinvoiceno = "REC-0"+str(recinv_id.id+1)
            order_num = str(recinv_id.id+1)
        else:
            reinvoiceno = "REC-"+str(recinv_id.id+1)
            order_num = str(recinv_id.id+1)

    customer_name = sale.customer.customerName
    customer_email = sale.customer.customerEmail
    customer_address = sale.customer.Address1
    gst_treatment = sale.customer.GSTTreatment
    gst_number = sale.customer.GSTIN
    place_of_supply = sale.sos
    entry_type = sale.customer.Taxpreference
    inv_date = sale.sales_date
    due_date = sale.ship_date
    terms = sale.terms.id
    cxnote = sale.cxnote
    terms_conditions = sale.terms_condition
    file = sale.file
    status = sale.status
    subtotal = sale.subtotal
    igst = sale.igst
    sgst = sale.sgst
    cgst = sale.cgst
    totaltax = sale.t_tax
    sh_charge =sale.sh_charge
    adjust = sale.adjust
    t_total = sale.grandtotal
    advance = sale.advance
    balance = sale.balance
    pay_method = sale.pay_method
   

    recinv=Recurring_invoice(cname=customer_name,cemail=customer_email,cadrs=customer_address,gsttr=gst_treatment,gstnum=gst_number,p_supply=place_of_supply,entry_type=entry_type,reinvoiceno=reinvoiceno,order_num=order_num,start=inv_date,end=due_date,terms=terms,cust_note=cxnote,conditions=terms_conditions,attachment=file,status=status,sub_total=subtotal,igst=igst,sgst=sgst,cgst=cgst,tax_amount=totaltax,shipping_charge=sh_charge,adjustment=adjust,total=t_total,paid=advance,balance=balance,payment_method=pay_method,cust_name=custo,user=user)
    recinv.save()
    recitem_id = Recurring_invoice.objects.last()


    sale.complete_status = -1
    sale.save()
    item =sales_item.objects.filter(sale_id=sale)
    for i in item:
        recitem =recur_itemtable(iname=i.product,hsncode=i.hsn,quantity=i.quantity,rate=i.rate,discount=i.desc,tax=i.tax,amt=i.total,ri_id=recitem_id.id)
       
        recitem.save()


    return redirect('view_sales_order')


    
def convert_view(request,pk):
    sale=SalesOrder.objects.get(id=pk)
    sale.status = "approved"
    sale.save()
    return redirect('sales_order_det',pk)

def deleteestimate(request,est_id):
    user = request.user
    company = company_details.objects.get(user=user)
    estimate = Estimates.objects.get(id=est_id)
    items = EstimateItems.objects.filter(estimate=estimate)
    items.delete()
    estimate.delete()
    return redirect('allestimates')
    

@login_required(login_url='login')
def additem_page_est(request):
    unit=Unit.objects.all()
    sale=Sales.objects.all()
    purchase=Purchase.objects.all()
    accounts = Purchase.objects.all()
    account_types = set(Purchase.objects.values_list('Account_type', flat=True))

    
    account = Sales.objects.all()
    account_type = set(Sales.objects.values_list('Account_type', flat=True))
    
    

    return render(request,'additem_est.html',{'unit':unit,'sale':sale,'purchase':purchase,
               
                            "account":account,"account_type":account_type,"accounts":accounts,"account_types":account_types,
                            
                            })

def additem_est(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            radio=request.POST.get('radio')
            if radio=='tax':
    
                
                inter=request.POST['inter']
                intra=request.POST['intra']
                type=request.POST.get('type')
                name=request.POST['name']
                unit=request.POST['unit']
                sel_price=request.POST.get('sel_price')
                sel_acc=request.POST.get('sel_acc')
                s_desc=request.POST.get('sel_desc')
                cost_price=request.POST.get('cost_price')
                cost_acc=request.POST.get('cost_acc')      
                p_desc=request.POST.get('cost_desc')
                u=request.user.id
                us=request.user
                history="Created by" + str(us)
                user=User.objects.get(id=u)
                unit=Unit.objects.get(id=unit)
                sel=Sales.objects.get(id=sel_acc)
                cost=Purchase.objects.get(id=cost_acc)
                ad_item=AddItem(type=type,Name=name,p_desc=p_desc,s_desc=s_desc,s_price=sel_price,p_price=cost_price,unit=unit,
                            sales=sel,purchase=cost,user=user,creat=history,interstate=inter,intrastate=intra
                                )
                
            else:
                                                  
                type=request.POST.get('type')
                name=request.POST['name']
                unit=request.POST['unit']
                sel_price=request.POST.get('sel_price')
                sel_acc=request.POST.get('sel_acc')
                s_desc=request.POST.get('sel_desc')
                cost_price=request.POST.get('cost_price')
                cost_acc=request.POST.get('cost_acc')      
                p_desc=request.POST.get('cost_desc')
                u=request.user.id
                us=request.user
                history="Created by" + str(us)
                user=User.objects.get(id=u)
                unit=Unit.objects.get(id=unit)
                sel=Sales.objects.get(id=sel_acc)
                cost=Purchase.objects.get(id=cost_acc)
                ad_item=AddItem(type=type,Name=name,p_desc=p_desc,s_desc=s_desc,s_price=sel_price,p_price=cost_price,unit=unit,
                            sales=sel,purchase=cost,user=user,creat=history,interstate='none',intrastate='none'
                                )
                ad_item.save()
            ad_item.save()
           
            return redirect("newestimate")
    return render(request,'additem_est.html')

@login_required(login_url='login')
def add_unit_est(request):
    if request.method=='POST':
        unit_name=request.POST['unit_name']
        Unit(unit=unit_name).save()
        return redirect('additem_est')
    return redirect("additem_est")
    
#-------------new view functions to add

@login_required(login_url='login')
def add_sales_est(request):
    if request.method=='POST':
        Account_type  =request.POST['acc_type']
        Account_name =request.POST['acc_name']
        Acount_code =request.POST['acc_code']
        Account_desc =request.POST['acc_desc']        
        acc=Sales(Account_type=Account_type,Account_name=Account_name,Acount_code=Acount_code,Account_desc=Account_desc)
        acc.save()
        return redirect('additem_est')
    return redirect("additem_est")

@login_required(login_url='login')
def add_account_est(request):
    if request.method=='POST':
        Account_type  =request.POST['acc_type']
        Account_name =request.POST['acc_name']
        Acount_code =request.POST['acc_code']
        Account_desc =request.POST['acc_desc']
       
        acc=Purchase(Account_type=Account_type,Account_name=Account_name,Acount_code=Acount_code,Account_desc=Account_desc)
        acc.save()                 
        return redirect("additem_est")
        
    return redirect("additem_est")
    
def customerdata(request):
    customer_id = request.GET.get('id')
    cust = customer.objects.get(id=customer_id)
    data7 = {'email': cust.customerEmail,'gstno':cust.GSTIN,'place':cust.placeofsupply,'gsttreat':cust.GSTTreatment,'billingAddress':cust.Address1}
    return JsonResponse(data7)

def termdata(request):
    term_id = request.GET.get('id')
    term = payment_terms.objects.get(id=term_id)
    data = {'days': term.Days}
    return JsonResponse(data)
    
    
def bankdata(request):
    bank_id = request.GET.get('id')
    term = Bankcreation.objects.get(name=bank_id)
    data = {'bank': term.ac_no}
    return JsonResponse(data)
    
def add_customer_for_invoice(request):
    pt=payment_terms.objects.all()
    if request.user.is_authenticated:
        if request.method=='POST':
            type=request.POST.get('type')
            txtFullName=request.POST['txtFullName']
            cpname=request.POST['cpname']
           
            email=request.POST.get('myEmail')
            wphone=request.POST.get('wphone')
            mobile=request.POST.get('mobile')
            skname=request.POST.get('skname')
            desg=request.POST.get('desg')      
            dept=request.POST.get('dept')
            wbsite=request.POST.get('wbsite')

            gstt=request.POST.get('gstt')
            posply=request.POST.get('posply')
            tax1=request.POST.get('tax1')
            crncy=request.POST.get('crncy')
            obal=request.POST.get('obal')

            select=request.POST.get('pterms')
            pterms=payment_terms.objects.get(id=select)
            pterms=request.POST.get('pterms')

            plst=request.POST.get('plst')
            plang=request.POST.get('plang')
            fbk=request.POST.get('fbk')
            twtr=request.POST.get('twtr')
        
            atn=request.POST.get('atn')
            ctry=request.POST.get('ctry')
            
            addrs=request.POST.get('addrs')
            addrs1=request.POST.get('addrs1')
            bct=request.POST.get('bct')
            bst=request.POST.get('bst')
            bzip=request.POST.get('bzip')
            bpon=request.POST.get('bpon')
            bfx=request.POST.get('bfx')

            sal=request.POST.get('sal')
            ftname=request.POST.get('ftname')
            ltname=request.POST.get('ltname')
            mail=request.POST.get('mail')
            bworkpn=request.POST.get('bworkpn')
            bmobile=request.POST.get('bmobile')

            bskype=request.POST.get('bskype')
            bdesg=request.POST.get('bdesg')
            bdept=request.POST.get('bdept')
            u = User.objects.get(id = request.user.id)

          
            ctmr=customer(customerName=txtFullName,customerType=type,
                        companyName=cpname,customerEmail=email,customerWorkPhone=wphone,
                         customerMobile=mobile,skype=skname,designation=desg,department=dept,
                           website=wbsite,GSTTreatment=gstt,placeofsupply=posply, Taxpreference=tax1,
                             currency=crncy,OpeningBalance=obal,PaymentTerms=pterms,
                                PriceList=plst,PortalLanguage=plang,Facebook=fbk,Twitter=twtr,
                                 Attention=atn,country=ctry,Address1=addrs,Address2=addrs1,
                                  city=bct,state=bst,zipcode=bzip,phone1=bpon,
                                   fax=bfx,CPsalutation=sal,Firstname=ftname,
                                    Lastname=ltname,CPemail=mail,CPphone=bworkpn,
                                    CPmobile= bmobile,CPskype=bskype,CPdesignation=bdesg,
                                     CPdepartment=bdept,user=u )
            ctmr.save()  
            
            return redirect("add_prod")
        return render(request,"createinvoice.html",)
        
        
def payment_term_for_invoice(request):
    if request.method=='POST':
        term=request.POST.get('term')
        day=request.POST.get('day')
        ptr=payment_terms(Terms=term,Days=day)
        ptr.save()
        return redirect("add_prod")
        
        
def addprice(request):
    company=company_details.objects.get(user=request.user)
    add=AddItem.objects.all()
    return render(request,'addprice_list.html',{'add':add,'company':company})
    
    
def addpl(request):
    print('hi')
    if request.method == "POST":
        

        
        name = request.POST.get('name')
        print(name)
        types = request.POST.get('type')
        print(types)
        taxes=request.POST.get('rate')
        desc = request.POST.get('desc')
        cur = request.POST.get('currency')
        print(cur)
        mark = request.POST.get('mark')
        print(mark)
        perc = request.POST.get('per')
        print(perc)
        rounds = request.POST.get('round')
        print(rounds)
        u = request.user.id
        user = User.objects.get(id=u)
            
        ad_item = Pricelist(
                name=name,
                types=types,
                tax=taxes,
                currency=cur,
                description=desc,
                mark=mark,
                percentage=perc,
                roundoff=rounds,
                user=user,
            )
            
        ad_item.save()
        item_name = request.POST.getlist('iname[]') 
        print(item_name)
        price = request.POST.getlist('iprice[]')
        rate = request.POST.getlist('custom[]') 
        if len(item_name) == len(price) == len(rate):
            mapped2 = zip(item_name, price, rate)
            mapped2 = list(mapped2)
         
            for ele in mapped2:
                created = Sample_table.objects.get_or_create(item_name=ele[0], price=ele[1], cust_rate=ele[2], pl=ad_item)

        return redirect("viewpricelist")
    else:
        # Handle the case when the request method is not POST
        return render(request, 'addprice_list.html')
    # return render(request, 'addprice_list.html')
    
def createpl(request):
    return render(request,'addprice_list.html')
    
def active_status(request,id):
    p=Pricelist.objects.get(id=id)
    if p.status == 'active':
        p.status = 'inactive'
    else:
        p.status = 'active'
    p.save()
    return redirect('viewlist',id=id)

def viewpricelist(request):
    company = company_details.objects.get(user = request.user)
    view=Pricelist.objects.all() 
                                                                                                                                                                                                                                                                                                                          
    return render(request,'view_price_list.html',{'view':view,'company':company})
    
def viewlist(request,id):
    company = company_details.objects.get(user = request.user)
    items=Pricelist.objects.all()
    product=Pricelist.objects.get(id=id)
    print(product.id)
    
    
    context={
       "allproduct":items,
       "product":product,
       'company':company,
      
    }
    
    return render(request,'list.html',context)

def editlist(request,id):
    company = company_details.objects.get(user = request.user)
    editpl=Pricelist.objects.get(id=id)
    sam=Sample_table.objects.filter(pl=id)
    return render(request,'edit_pricelist.html',{'editpl':editpl,'sam':sam,"company":company})
    
def editpage(request,id):
    if request.method=='POST':
        edit=Pricelist.objects.get(id=id)
        edit.name=request.POST['name']
        edit.description=request.POST['desc']
        edit.mark=request.POST['mark']
        edit.percentage=request.POST['per']
        print(request.POST['per'])
        edit.tax=request.POST['types']
        
        edit.roundoff=request.POST['round']
        print(edit.roundoff)
        item_name = request.POST.getlist('iname[]') 
        print(item_name)
        price = request.POST.getlist('iprice[]')
        rate = request.POST.getlist('custom[]') 
        sam=Sample_table.objects.filter(pl=id).delete()

        if len(item_name) == len(price) == len(rate):
            mapped2 = zip(item_name, price, rate)
            mapped2 = list(mapped2)
         
            for ele in mapped2:
                created = Sample_table.objects.get_or_create(item_name=ele[0], price=ele[1], cust_rate=ele[2],pl=edit)
        edit.save()

        return redirect('viewpricelist')
def delete_item(request,id):
    dl=Pricelist.objects.get(id=id)
    dl.delete()
    return redirect('viewpricelist')


def banking_home(request):
    company = company_details.objects.get(user = request.user)
    viewitem=banking.objects.filter(user=request.user)
    return render(request,'banking.html',{'view':viewitem,"company":company})       
    
def create_banking(request):
    company = company_details.objects.get(user = request.user)
    print(company.company_name)
    banks = bank.objects.filter(user=request.user, acc_type="bank")
    return render(request,'create_banking.html',{"bank":banks,"company":company})    

def save_banking(request):
    if request.method == "POST":
        a=banking()
        a.name = request.POST.get('main_name',None)
        a.alias = request.POST.get('main_alias',None)
        a.acc_type = request.POST.get('main_type',None)
        a.ac_holder = request.POST.get('ac_holder',None)
        a.ac_no = request.POST.get('ac_number',None)
        a.ifsc = request.POST.get('ifsc',None)
        a.swift_code = request.POST.get('sw_code',None)
        a.bnk_name = request.POST.get('bnk_nm',None)
        a.bnk_branch = request.POST.get('br_name',None)
        a.chq_book = request.POST.get('alter_chq',None)
        a.chq_print = request.POST.get('en_chq',None)
        a.chq_config = request.POST.get('chq_prnt',None)
        a.mail_name = request.POST.get('name',None)
        a.mail_addr = request.POST.get('address',None)
        a.mail_country = request.POST.get('country',None)
        a.mail_state = request.POST.get('state',None)
        a.mail_pin = request.POST.get('pin',None)
        a.bd_bnk_det = request.POST.get('bnk_det',None)
        a.bd_pan_no = request.POST.get('pan',None)
        a.bd_reg_typ = request.POST.get('register_type',None)
        a.bd_gst_no = request.POST.get('gstin',None)
        a.bd_gst_det = request.POST.get('gst_det',None)
        a.opening_blnc_type = request.POST.get('opening_blnc_type',None)
        a.user=request.user
        a.opening_bal = request.POST.get('balance',None)
        a.save()
        return redirect("banking_home")
    return redirect("create_banking")

def view_bank(request,id):
    viewitem=banking.objects.filter(user=request.user)
    bnk=banking.objects.get(id=id,user=request.user)
    company = company_details.objects.get(user = request.user)
    context={
        'view':viewitem,
        'bnk':bnk,
        "company":company
    }
    return render(request,"view_bank.html",context)

def banking_edit(request,id):
    bnk=banking.objects.get(id=id,user=request.user)
    banks = bank.objects.filter(user=request.user, acc_type="bank")
    company = company_details.objects.get(user = request.user)
    context={
        'bnk':bnk,
        "bank":banks,
        "company":company
    }
    return render(request,"edit_banking.html",context)

def save_edit_bnk(request,id):
    if request.method == "POST":
        a=banking.objects.get(id=id,user=request.user)
        a.name = request.POST.get('main_name',None)
        a.alias = request.POST.get('main_alias',None)
        a.acc_type = request.POST.get('main_type',None)
        a.ac_holder = request.POST.get('ac_holder',None)
        a.ac_no = request.POST.get('ac_number',None)
        a.ifsc = request.POST.get('ifsc',None)
        a.swift_code = request.POST.get('sw_code',None)
        a.bnk_name = request.POST.get('bnk_nm',None)
        a.bnk_branch = request.POST.get('br_name',None)
        a.chq_book = request.POST.get('alter_chq',None)
        a.chq_print = request.POST.get('en_chq',None)
        a.chq_config = request.POST.get('chq_prnt',None)
        a.mail_name = request.POST.get('name',None)
        a.mail_addr = request.POST.get('address',None)
        a.mail_country = request.POST.get('country',None)
        a.mail_state = request.POST.get('state',None)
        a.mail_pin = request.POST.get('pin',None)
        a.bd_bnk_det = request.POST.get('bnk_det',None)
        a.bd_pan_no = request.POST.get('pan',None)
        a.bd_reg_typ = request.POST.get('register_type',None)
        a.bd_gst_no = request.POST.get('gstin',None)
        a.bd_gst_det = request.POST.get('gst_det',None)
        a.opening_bal = request.POST.get('balance',None)
        a.opening_blnc_type = request.POST.get('opening_blnc_type',None)
        a.save()
        return redirect("banking_home")
    return redirect("create_banking")

def save_bank(request):
    if request.method == "POST":
        a=bank()
        a.acc_type = request.POST.get('type',None)
        a.bank_name = request.POST.get('bank',None)
        a.user = request.user
        a.save()
        return redirect("create_banking")
    return redirect("create_banking")
def save_banking_edit(request,id):
    if request.method == "POST":
        a=bank()
        a.acc_type = request.POST.get('type',None)
        a.bank_name = request.POST.get('bank',None)
        a.user = request.user
        a.save()
        return redirect("banking_edit", id)
    return redirect("banking_edit", id)
    
def basenav(request):
    company = company_details.objects.get(user = request.user)
    print(company.company_name)
    context = {
                'company' : company
            }
    return render(request,'base.html',context)

def banking_delete(request,id):
    bnk=banking.objects.get(id=id)
    bnk.delete()
    return redirect("banking_home")
    
@login_required(login_url='login')
def recurringhome(request):
    user_id=request.user.id 
       
    selected_vendor_id = request.GET.get('vendor')
    vendors = vendor_table.objects.filter(user=user_id)
    accounts = Account.objects.all()
    account_types = set(Account.objects.values_list('accountType', flat=True))
    repeat_list = repeat_every.objects.all()
    bank=Bankcreation.objects.all()
    # repeat=repeat_every.objects.values_list('Terms', flat=True).distinct()
   
    selected_vendor = vendor_table.objects.filter(id=selected_vendor_id).first()
    gst_treatment = selected_vendor.gst_treatment if selected_vendor else ''
    customers=customer.objects.filter(user=user_id)
    payments=payment_terms.objects.filter(user=user_id)
    company = company_details.objects.get(user = request.user)
    last_id = Expense.objects.filter(user=user_id).order_by('-id').values('id').first()
    if last_id:
        last_id = last_id['id']
        next_no = last_id+1
    else:
        next_no = 1
    
    return render(request, 'recurring_home.html', {
        'vendors': vendors,
        'selected_vendor_id': selected_vendor_id,
        
        'accounts': accounts,
        'account_types': account_types,
        'gst_treatment':gst_treatment,
        'customers':customers,
        'payments':payments,
        'company':company,
        'repeat_list':repeat_list,
        'bank':bank,
        'num':next_no
    })


from django.shortcuts import get_object_or_404
from .models import Expense, vendor_table

@login_required(login_url='login')
def add_expense(request):
    if request.method == 'POST':
        
        # Retrieve form data
        userId=request.user.id
        profile_name = request.POST['profile_name']
        repeatevery = request.POST['repeat_every']
        repeat=repeat_every.objects.filter(id=repeatevery).first()
        start_date = request.POST['start_date']
        expense_account_id  = request.POST['expense_account']
        expense_account = Account.objects.filter(pk=expense_account_id).first()

        refrenc=request.POST['refrnsid']

        expense_type = request.POST['expense_type']
          
        hsn = request.POST['goods_label']
        sac = request.POST['services_label']
        amount = request.POST['amount']
        currency = request.POST['currency']
        paidthrough = request.POST['paidthrough']
        cheque_id = request.POST.get('chequeId')
        upi_number = request.POST.get('upiNumber')
        bank_account = request.POST.get('bankAccount')
        vendor_id = request.POST['vendor']
        vendor = get_object_or_404(vendor_table, pk=vendor_id)
        gst_treatment=request.POST['gst_trt_inp']
        gst = request.POST.get('gstin_inp')
        vmail=request.POST['vmail']
        vdestination = request.POST['destination']
        tax = request.POST['tax[]']
        notes = request.POST['notes']
        customer_id = request.POST['customername']
        customer_obj = get_object_or_404(customer, pk=customer_id)
        cust_gsttreatmnt=request.POST['cu_gst_trt']
        custemail=request.POST.get('mail')
        cust_pos=request.POST['c_destination']
        # Handle the ends_on field
        file=request.FILES.get('file')
       
        udata=User.objects.get(id=userId)
       
        # Create and save the Expense instance
        expense = Expense(
            profile_name=profile_name,
            repeatevery=repeat,
            start_date=start_date,
           
            expense_account=expense_account,
            refrenceid=refrenc,
            expense_type=expense_type,
            hsn=hsn,
            sac=sac,
            amount=amount,
            currency=currency,
            paidthrough=paidthrough,
            cheque_id=cheque_id, 
            upi_number=upi_number,
            bank_account=bank_account,
            vendor=vendor,
            gst_treatment=gst_treatment,
            gst=gst,
            vendor_destination=vdestination,
            tax=tax,
            notes=notes,
            customer= customer_obj,
            customeremail=custemail,
            cust_gsttreatment=cust_gsttreatmnt,
            cust_placeofsupply=cust_pos,
            vendormail= vmail,
            document=file,
            activation_tag="Active", # Set the activation_tag to "active"
            status='Save',
           
            user=udata,
            
        )
        expense.save()

        return redirect('recurringbase')
    else:
       
        return render(request, 'recurring_home.html')


@login_required(login_url='login')
def recurringbase(request):
    userId=request.user.id
    expenses = Expense.objects.filter(user=userId)
    company = company_details.objects.get(user = request.user)
    
    return render(request, 'recurring_base.html',{'expenses': expenses,'company':company})

@login_required(login_url='login')
def show_recurring(request, expense_id):
    userid=request.user.id
    expense = get_object_or_404(Expense, id=expense_id)
    expenses = Expense.objects.filter(user=userid)
    company = company_details.objects.get(user=request.user)
    accounts = Account.objects.all()
    account_types = set(Account.objects.values_list('accountType', flat=True))
   
    search_query = request.GET.get('search_query')
    search_date = request.GET.get('search_date')

    if search_query:
        expenses = expenses.filter(
            Q(profile_name__icontains=search_query) | Q(customername__icontains=search_query)
        )

    if search_date:
        expenses = expenses.filter(start_date=search_date)

    

    comments = Comment.objects.filter(profile_name=expense.profile_name, expense=expense)
    vendor = vendor_table.objects.get(id=expense.vendor_id)
    customers = customer.objects.get(id=expense.customer_id)
    vendors = vendor_table.objects.all()
  
    everyrepeat=repeat_every.objects.get(id=expense.repeatevery.id)
   

    return render(request, 'show_recurring.html', {'expense': expense,'expense.id':expense_id, 'expenses': expenses, 'comments': comments, 'company': company, 'vendor': vendor, 'customer': customers,'account':accounts,'account_types':account_types,'vendors':vendors,'repeat':everyrepeat})


def expense_details(request, pk):
    user = request.user
    expense = ExpenseE.objects.filter(user=user)
    company = company_details.objects.get(user = request.user)
    expense_account=ExpenseE.objects.get(id=pk)
    context = {
        'expenses': expense,
        'expense': expense_account,
        'company':company
    }
    return render(request, 'expenseview.html', context)
    
def edit_expense(request, expense_id):
    
    user_id=request.user.id 

    expense = Expense.objects.get(id=expense_id)
    
    vendors = vendor_table.objects.filter(user=user_id)
    customers = customer.objects.filter(user=user_id)
    accounts = Account.objects.all()
    account_types = Account.objects.values_list('accountType', flat=True).distinct()
    selected_account = expense.expense_account
    payments=payment_terms.objects.all()
    company = company_details.objects.get(user = request.user)
    repeat_list = repeat_every.objects.all()
    
    
    
    if request.method == 'POST':
       
        expense.profile_name = request.POST.get('profile_name')
        repeatevery_id= request.POST.get('repeat_every')
        repeat_id=repeat_every.objects.get(id=repeatevery_id)
        expense.repeatevery=repeat_id
        expense.start_date = request.POST.get('start_date')
        
        account_id = request.POST.get('expense_account')
        
        selected_account = Account.objects.get(id=account_id)
        expense.expense_account=selected_account
        expense.expense_type = request.POST.get('expense_type')
        expense.hsn = request.POST['goods_label']
        expense.sac = request.POST['services_label']
        expense.amount = request.POST.get('amount')
        expense.currency = request.POST.get('currency')
        expense.paidthrough = request.POST.get('paidthrough')
        expense.cheque_id=request.POST.get('chequeId')
        expense.upi_number=request.POST.get('upiNumber')
        expense.bank_account = request.POST.get('bankAccount')
        expense.vendor_id = request.POST.get('vendor')
        expense.expense_type = request.POST.get('expense_type')
        expense.gst_treatment= request.POST.get('gst_trt_inp')
        if expense.gst_treatment=='unregistered Business':
            expense.gst='None'
        else:
            expense.gst=request.POST.get('gstin_inp')
        expense.vendormail=request.POST.get('vmail')
        expense.destination = request.POST.get('destination')
        expense.tax = request.POST.get('tax[]')
        expense.notes = request.POST.get('notes')
        customer_id= request.POST.get('customername')  # Get the customer ID from POST data
        customer_obj = get_object_or_404(customer, pk=customer_id)  # Fetch the customer object
        expense.customer = customer_obj
        expense.customeremail=request.POST.get('mail')
        
        
        

        expense.save()
        
        return redirect('show_recurring',expense_id=expense_id)
    
    else:
        
        return render(request, 'edit_expense.html', {'expense': expense, 'vendors': vendors, 'customers': customers,'accounts': accounts,'selected_account': selected_account,'items':  account_types,'payments':payments,'company':company,'repeat_list':repeat_list})
        
@login_required(login_url='login')
def newexp(request):
    return render(request,'create_expense.html')

@login_required(login_url='login')
def save_data(request):
    if request.method == 'POST':
        account_type = request.POST.get('accountType')
        account_name = request.POST.get('accountName')
        account_code = request.POST.get('accountCode')
        description = request.POST.get('description')

        account = Account(accountType=account_type, accountName=account_name,  description=description)
        account.save()
        acc_id = account.id

        return JsonResponse({
            "account_type": account_type,
            "account_name": account_name,
            "account_code": account_code,
            "description": description,
            "acc_id": acc_id
        })

    return render(request, 'recurring_home.html')@login_required(login_url='login')
  
    
from django.http import JsonResponse
from .models import Account

def get_account_names(request):
    account_names = Account.objects.values_list('accountName', flat=True)
    return JsonResponse(list(account_names), safe=False)
    
@login_required(login_url='login')
def profileshow(request,expense_id):
    expenses = Expense.objects.all()
    expense = get_object_or_404(Expense, id=expense_id)

    return render(request, 'show_recurring.html', {'expenses': expenses,'expense':expense})    
    
@login_required(login_url='login')   
def entr_custmr(request):
  if request.user.is_authenticated:
        if request.method=='POST':
            print('customer is entered')
           
            type=request.POST.get('type')
            Name=request.POST.get('ctitle')
            print(Name)
            fname=request.POST.get('cfirstname')
            print(fname)
            lname=request.POST.get('clastname')
            company=request.POST.get('ccompany_name')
            email=request.POST.get('cemail')
            wphone=request.POST.get('cw_mobile')
            mobile=request.POST.get('cp_mobile')
            facebook=request.POST.get('facebook')
            twitter=request.POST.get('twitter')
            wbsite=request.POST.get('website')
            skname=request.POST.get('cskype')
            desg=request.POST.get('c_desg')      
            dept=request.POST.get('c_dpt')
            print(dept)

            gstt=request.POST.get('c_gsttype')
            gstin=request.POST.get('v_gstin')
            posply=request.POST.get('placesupply')
            tax1=request.POST.get('radioCust1')
            crncy=request.POST.get('c_curn')
            obal=request.POST.get('c_open')

            select=request.POST.get('c_terms')
            pterms=payment_terms.objects.get(id=select)
            
            print(pterms)

           
            baddrs1=request.POST.get('cstreet1')
            baddrs2=request.POST.get('cstreet2')
            bcity=request.POST.get('ccity')
            bstate=request.POST.get('cstate')
            bcountry=request.POST.get('ccountry')
            bpincode=request.POST.get('cpincode')
            bphone=request.POST.get('cphone')
            bfax=request.POST.get('cfax')
            saddrs1=request.POST.get('csstreet1')
            saddrs2=request.POST.get('csstreet2')
            scity=request.POST.get('cscity')
            sstate=request.POST.get('csstate')
            scountry=request.POST.get('cscountry')
            spincode=request.POST.get('cspincode')
            sphone=request.POST.get('csphone')
            sfax=request.POST.get('csfax')
            print(sfax)

            u = User.objects.get(id = request.user.id)
          

          
            ctmr=customer(customerType=type,Name=Name,
                        companyName=company,customerEmail=email,customerWorkPhone=wphone,
                         customerMobile=mobile,skype=skname,designation=desg,department=dept,
                           website=wbsite,GSTTreatment=gstt,placeofsupply=posply, Taxpreference=tax1,
                             currency=crncy,OpeningBalance=obal,PaymentTerms=pterms,
                                Facebook=facebook,Twitter=twitter,GSTIN= gstin,
                                 country=bcountry,bAddress1=baddrs1,bAddress2=baddrs2,
                                  bcity=bcity,state=bstate,zipcode= bpincode,phone1=bphone,
                                   fax=bfax,Firstname=fname,sAddress1=saddrs1,sAddress2=saddrs2,scity= scity,sstate=sstate,
                                     scountry= scountry, szipcode=spincode,sphone1=sphone,sfax=sfax,Lastname=lname,user=u )
           
            ctmr.save()  
            print(ctmr)
            
            new_customer_data = {
            'id': ctmr.id,
            'name': ctmr.Firstname + ' ' + ctmr.Lastname,
            'email':ctmr.customerEmail,
            

            # Add other fields as needed
        }
            return JsonResponse(new_customer_data)
        payments=payment_terms.objects.all()
        return render(request,'recurring_home.html',{'payments':payments})  
        
from django.http import JsonResponse

@login_required(login_url='login')
def get_customer_names(request):
    customers = customer.objects.all()
    customer_names = [{'id': c.id, 'name':f'{c.Firstname} {c.Lastname}'} for c in customers]
    return JsonResponse(customer_names, safe=False)  
    
@login_required(login_url='login')   
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    expense.delete()
    return redirect('recurringbase')


def get_profile_details(request, profile_id):
    expense = get_object_or_404(Expense, id=profile_id)
    vendor = expense.vendor 
    data = {
        'id': expense.id,
        'profile_name': expense.profile_name,
        'repeat_every': expense.repeat_every,
        'start_date': expense.start_date,
        'ends_on': expense.ends_on,
        'expense_account': expense.expense_account,
        'expense_type': expense.expense_type,
        'amount': expense.amount,
        'paidthrough': expense.paidthrough,
        'vendor': vendor.vendor_display_name,  
        'gst': expense.gst,
        'destination': expense.destination,
        'tax': expense.tax,
        'notes': expense.notes,
        'customername': expense.customername,
        'activation_tag': expense.activation_tag
    }
    return JsonResponse(data)
    
    
    
@login_required(login_url='login')
def view_sales_order(request):
    sales=SalesOrder.objects.all()
    user = request.user
    company = company_details.objects.get(user=user)
    return render(request,'view_sales_order.html',{"sale":sales,"company":company})      

    
@login_required(login_url='login')
def create_sales_order(request):
    user = request.user
    unit=Unit.objects.all()
    sales=Sales.objects.all()
    company = company_details.objects.get(user=user)
    cust=customer.objects.all()
    pay=payment_terms.objects.all()
    itm=AddItem.objects.all()
    purchase=Purchase.objects.all()
    last_record = SalesOrder.objects.last()
    bank = Bankcreation.objects.all()

    if last_record ==None:
        reford = '01'
        reference = 'SO-01'
        remaining_characters='SO-'
    else:
        reference = 'SO-01'
        lastSalesNo = last_record.sales_no
        last_two_numbers = int(lastSalesNo[-2:])+1
        remaining_characters = lastSalesNo[:-2]  
        if last_two_numbers < 10:
            reference = remaining_characters+'0'+str(last_two_numbers)
        else:
            reference = remaining_characters+str(last_two_numbers)
        if last_record.id+1 < 10:
            reford = '0'+ str(int(last_record.id)+1)
        else:
            reford = str(int(last_record.id)+1)
    
    context={
        "c":cust,
        "pay":pay,
        "itm":itm,
        "company":company,
        "unit":unit, 
        "sales":sales,
        "purchase":purchase,
        "reford":reford,
        "reference":reference,
        "remaining_characters":remaining_characters,
        "bank":bank
    }
    return render(request,'create_sales_order.html',context)

    
@login_required(login_url='login')
def add_customer_for_sorder(request):
        if request.method=='POST':
            tax=request.POST.get('tax')
            type=request.POST.get('title')
            first=request.POST['firstname']
            last=request.POST['lastname']
            txtFullName= request.POST['display_name']
            
            itemtype=request.POST.get('itemtype')
            cpname=request.POST['company_name']
            
            email=request.POST.get('email')
            wphone=request.POST.get('work_mobile')
            mobile=request.POST.get('pers_mobile')
            skname=request.POST.get('skype')
            desg=request.POST.get('desg')      
            dept=request.POST.get('dpt')
            wbsite=request.POST.get('website')

            gstt=request.POST.get('gsttype')
            gstin=request.POST.get('gstin')
            panno=request.POST.get('panno')


            posply=request.POST.get('placesupply')
            crncy=request.POST.get('currency')
            obal=request.POST.get('openingbalance')

           
            pterms=request.POST.get('paymentterms')

           
          
            fbk=request.POST.get('facebook')
            twtr=request.POST.get('twitter')
          
            ctry=request.POST.get('country')
            
            street=request.POST.get('street')
            shipstate=request.POST.get('shipstate')
            shipcity=request.POST.get('shipcity')
            bzip=request.POST.get('shippincode')
            shipfax=request.POST.get('shipfax')

            sal=request.POST.get('title')
            addres=street +','+ shipcity+',' + shipstate+',' + bzip
            adress2=addres
            u = User.objects.get(id = request.user.id)

            print(tax)
            ctmr=customer(customerName=txtFullName,customerType=itemtype,
                        companyName=cpname,customerEmail=email,customerWorkPhone=wphone,
                         customerMobile=mobile,skype=skname,designation=desg,department=dept,
                           website=wbsite,GSTTreatment=gstt,placeofsupply=posply, Taxpreference=tax,
                             currency=crncy,OpeningBalance=obal,PaymentTerms=pterms,
                               Facebook=fbk,Twitter=twtr
                                 ,country=ctry,Address1=addres,Address2=adress2,
                                  city=shipcity,state=shipstate,zipcode=bzip,phone1=wphone,
                                   fax=shipfax,
                                  user=u ,GSTIN=gstin,pan_no=panno)
            ctmr.save()
 
            
            return HttpResponse({"message": "success"})

    
@login_required(login_url='login')        
def payment_term_for_sorder(request):
    if request.method=='POST':
        term=request.POST.get('term')
        day=request.POST.get('day')
        ptr=payment_terms(Terms=term,Days=day)
        ptr.save()
        return redirect("create_sales_order")
        
        
@login_required(login_url='login')
def add_sales_order(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            c=request.POST['cx_name']
            cus=customer.objects.get(id=c)   
            custo=cus.id
            sales_no=request.POST['sale_no']

            if len(sales_no) == 4:
                sales_no = sales_no[:3] + '0' +sales_no[-1]

            sale_list = list(SalesOrder.objects.values_list('sales_no'))
            sale_list_update = [item[0] for item in sale_list]
            
            if sales_no in sale_list_update:
                messages.error(request,'Sale Order number is already in use')
                return redirect('create_sales_order')

            terms=request.POST['term']
            term=payment_terms.objects.get(id=terms)
            reference=request.POST['ord_no']
            sa_date=request.POST['sa_date']
            sh_date=request.POST['sh_date']
            sos=request.POST['srcofsupply']
            sh_charge=request.POST['shipping_charge']
            cxnote=request.POST['customer_note']
            subtotal=request.POST['subtotal']
            igst=request.POST['igst']
            cgst=request.POST['cgst']
            sgst=request.POST['sgst']
            totaltax=request.POST['totaltax']
            t_total=request.POST['t_total']
            balance=request.POST['balance']
            advance=request.POST['advance']
            cheque_id=request.POST['cheque_id']
            upi_id=request.POST['upi_id']
            pay_method=request.POST['method']

            if request.FILES.get('file') is not None:
                file=request.FILES['file']
            else:
                file="/static/images/alt.jpg"

            tc=request.POST['ter_cond']
            product=tuple(request.POST.getlist('item[]'))
            hsn=tuple(request.POST.getlist('hsn[]'))
            quantity=tuple(request.POST.getlist('quantity[]'))
            rate=tuple(request.POST.getlist('rate[]'))
            desc=tuple(request.POST.getlist('desc[]'))
            tax=tuple(request.POST.getlist('tax[]'))
            total=tuple(request.POST.getlist('amount[]'))
            adjust=(request.POST.getlist('adjust'))
            adjust = float(adjust[0])

            if 'Draft' in request.POST:
                status="draft"
            if "Save" in request.POST:
                status = "approved"
            
            sales=SalesOrder(customer_id=custo,sales_no=sales_no,terms=term,reference=reference, sales_date=sa_date,ship_date=sh_date,
                             balance=balance,cxnote=cxnote,subtotal=subtotal,igst=igst,cgst=cgst,sgst=sgst,t_tax=totaltax,
                             cheque_id=cheque_id,upi_id=upi_id,pay_method=pay_method,grandtotal=t_total,status=status,terms_condition=tc,
                             file=file,sos=sos,sh_charge=sh_charge,adjust=adjust,advance=advance)
            sales.save()
            sale_id=SalesOrder.objects.get(id=sales.id)
          
            if len(product)==len(quantity)==len(tax)==len(total)==len(rate)==len(hsn):
                mapped = zip(hsn,product,quantity,tax,total,rate,desc)
                mapped = list(mapped)
                for element in mapped:
                    created =sales_item(sale=sale_id,hsn=element[0],product=element[1],quantity=element[2],tax=element[3],total=element[4],
                                        rate=element[5],desc=element[6])
                    created.save()

            return redirect('view_sales_order')       
    
@login_required(login_url='login')
def sales_order_det(request,id):
    sales=SalesOrder.objects.get(id=id)
    saleitem=sales_item.objects.filter(sale_id=id)
    sale_order=SalesOrder.objects.all()
    company=company_details.objects.get(user_id=request.user.id)

    bank=''
    if sales.pay_method != 'cash':
        if sales.pay_method != 'upi':
            if sales.pay_method != 'cheque':
                bank = Bankcreation.objects.get(name=sales.pay_method)
    
    context={'sale':sales,'saleitem':saleitem,'sale_order':sale_order,'company':company,'bank':bank}
    
    return render(request,'sales_order_det.html',context)


    
@login_required(login_url='login')
def delet_sales(request,id):
    d=SalesOrder.objects.get(id=id)
    d.delete()
    return redirect('view_sales_order')
    
    
@login_required(login_url='login')
def edit_sales_order(request,id):
    user = request.user
    company = company_details.objects.get(user=user)
    c = customer.objects.all()
    itm = AddItem.objects.all()
    salesitem = sales_item.objects.filter(sale_id=id)
    sales = SalesOrder.objects.get(id=id)
    sales_id = SalesOrder.objects.get(id=id)
    pay=payment_terms.objects.all()
    bank = Bankcreation.objects.all()
    unit=Unit.objects.all()
    last_record = SalesOrder.objects.last()
    sale=Sales.objects.all()
    purchase=Purchase.objects.all()

    if request.method == 'POST':
        u=request.user.id
        c=request.POST['cx_name']
        
        cust=customer.objects.get(id=c) 
        sales.customer=cust
        term=request.POST['term']
        
        sales_no=request.POST['sale_no']

        if len(sales_no) == 4:
            sales_no = sales_no[:3] + '0' +sales_no[-1]

        sale_list = list(SalesOrder.objects.values_list('sales_no'))
        sale_list_update = [item[0] for item in sale_list]

        if sales_no in sale_list_update:
            if sales_no != sales_id.sales_no:
                messages.error(request,'Sale Order number is already in use')
                return redirect('edit_sales_order',id)
        
        sales.sales_no=request.POST['sale_no']

        term=request.POST['term']
        sales.terms = payment_terms.objects.get(id=term)
        sales.sales_date = request.POST['sa_date']
        sales.ship_date=request.POST['sh_date']
        sales.cxnote = request.POST['customer_note']
        sales.igst = request.POST['igst']
        sales.cgst = request.POST['cgst']
        sales.sgst = request.POST['sgst']
        sales.t_tax = request.POST['totaltax']
        sales.grandtotal = request.POST['t_total']
        sales.sos=request.POST['srcofsupply']
        sales.sh_charge=request.POST['shipping_charge']
        if request.FILES.get('file') is not None:
            sales.file = request.FILES['file']
        else:
            sales.file = "/static/images/alt.jpg"

            sales.terms_condition = request.POST.get('ter_cond')

        sales.balance=request.POST['balance']
        sales.advance=request.POST['advance']
        sales.cheque_id=request.POST['cheque_id']
        sales.upi_id=request.POST['upi_id']
        sales.pay_method=request.POST['method']
        adjust=request.POST.getlist('adjust')
        adjust = float(adjust[0])
        sales.adjust=adjust
        
        sales.save()
        hsn=tuple(request.POST.getlist('hsn[]'))
        product=tuple(request.POST.getlist('item[]'))
        quantity=tuple(request.POST.getlist('quantity[]'))
        rate=tuple(request.POST.getlist('rate[]'))
        tax=tuple(request.POST.getlist('tax[]'))
        total=tuple(request.POST.getlist('amount[]'))
        desc=tuple(request.POST.getlist('desc[]'))
        obj_dele=sales_item.objects.filter(sale_id=sales.id)
        obj_dele.delete()
       
        if len(product)==len(quantity)==len(tax)==len(total)==len(rate):

            mapped = zip(hsn,product,quantity,tax,total,rate,desc)
            mapped = list(mapped)
        
            for element in mapped:
                created =sales_item(sale=sales,hsn=element[0],product=element[1],quantity=element[2],tax=element[3],total=element[4],
                                        rate=element[5],desc=element[6])
                created.save()
                    
               
            return redirect('sales_order_det',id)
                
    context={
        "c":c,
        "itm":itm,
        "saleitm":salesitem,
        "sale":sales,
        "pay":pay,
        "company":company,
        "bank":bank,
        "unit":unit,
        "reford":(last_record.id)+1,
        "sales":sale,
        "purchase":purchase,
        "rowcount":len(salesitem)

    }
    return render(request,'edit_sale_page.html',context)
    
    
def create_delivery_chellan(request):
    user = request.user
    # print(user_id)
    company = company_details.objects.get(user=user)
    items = AddItem.objects.filter(user_id=user.id)
    customers = customer.objects.filter(user_id=user.id)
    dates=date.today()
    # estimates_count = DeliveryChellan.objects.filter(user_id=user.id).count()
    # estimates_count = DeliveryChellan.objects.last().id
    if  DeliveryChellan.objects.all().exists():
        chellan_count = RetainerInvoice.objects.last().id
        count=chellan_count+1 
    else:
        count=1 
    # print(estimates_count)
    # next_count = estimates_count+1

    unit=Unit.objects.all()
    sale=Sales.objects.all()
    purchase=Purchase.objects.all()
    accounts = Purchase.objects.all()
    account_types = set(Purchase.objects.values_list('Account_type', flat=True))

    
    account = Sales.objects.all()
    account_type = set(Sales.objects.values_list('Account_type', flat=True))
    payments=payment_terms.objects.all()

    context = {'company': company,
               'items': items,
               'customers': customers,
               'count': count,
               'date':dates,
               'unit':unit,
               'sale':sale,
               'purchase':purchase,
                "account":account,
                "account_type":account_type,
                "accounts":accounts,
                "account_types":account_types,
                'payments':payments,
               }

    return render(request, 'create_delivery_chellan.html', context)


def delivery_chellan_home(request):
    company = company_details.objects.get(user = request.user)
    viewitem=DeliveryChellan.objects.filter(user=request.user)
    
    return render(request,'delivery_chellan.html',{'view':viewitem,"company":company})  
    
    
def create_challan_draft(request):
    if request.method == 'POST':
        try:
            x = request.POST["hidden_state"]
            y = request.POST["hidden_cus_place"]
            c = request.POST['customer_id']
            cus = customer.objects.get(id=c)
            
            # Retrieve the current user
            cur_user = request.user
            user = User.objects.get(id=cur_user.id)
            
            custo = cus
            cust_name = cus.customerName
            chellan_no = request.POST['chellan_number']
            reference = request.POST['reference']
            chellan_date = request.POST['chellan_date']
            customer_mailid = request.POST['customer_mail']
            chellan_type = request.POST['chellan_type']

            if x == y:
                item = request.POST.getlist('item[]')
                hsn = request.POST.getlist('hsn[]')
                quantity1 = request.POST.getlist('quantity[]')
                quantity = [float(x) for x in quantity1]
                rate1 = request.POST.getlist('rate[]')
                rate = [float(x) for x in rate1]
                discount1 = request.POST.getlist('discount[]')
                discount = [float(x) for x in discount1]
                tax1 = request.POST.getlist('tax[]')
                tax = [float(x) for x in tax1]
                amount1 = request.POST.getlist('amount[]')
                amount = [float(x) for x in amount1]
            else:
                item = request.POST.getlist('itemm[]')
                hsn = request.POST.getlist('hsnn[]')
                quantity1 = request.POST.getlist('quantityy[]')
                quantity = [float(x) for x in quantity1]
                rate1 = request.POST.getlist('ratee[]')
                rate = [float(x) for x in rate1]
                discount1 = request.POST.getlist('discountt[]')
                discount = [float(x) for x in discount1]
                tax1 = request.POST.getlist('taxx[]')
                tax = [float(x) for x in tax1]
                amount1 = request.POST.getlist('amountt[]')
                amount = [float(x) for x in amount1]

            cust_note = request.POST['customer_note']
            sub_total = float(request.POST['subtotal'])
            igst = float(request.POST['igst'])
            sgst = float(request.POST['sgst'])
            cgst = float(request.POST['cgst'])
            tax_amnt = float(request.POST['total_taxamount'])
            shipping = float(request.POST['shipping_charge'])
            adjustment = float(request.POST['adjustment_charge'])
            total = float(request.POST['total'])
            tearms_conditions = request.POST['tearms_conditions']
            attachment = request.FILES.get('file')
            status = "Draft"
            tot_in_string = str(total)

            challan = DeliveryChellan(
                user=user,
                cu=custo,  # Assign the customer to the 'cu' field
                customer_name=cust_name,
                chellan_no=chellan_no,
                reference=reference,
                chellan_date=chellan_date,
                customer_mailid=customer_mailid,
                # Set other fields as needed
                sub_total=sub_total,
                igst=igst,
                sgst=sgst,
                cgst=cgst,
                tax_amount=tax_amnt,
                chellan_type=chellan_type,
                shipping_charge=shipping,
                adjustment=adjustment,
                total=total,
                status=status,
                customer_notes=cust_note,
                terms_conditions=tearms_conditions,
                attachment=attachment
            )
            challan.save()


            # Handle dynamic items
            for i in range(len(item)):
                item_data = ChallanItems(
                    chellan=challan,
                    item_name=item[i],
                    hsn=hsn[i],
                    quantity=quantity[i],
                    rate=rate[i],
                    discount=discount[i],
                    tax_percentage=tax[i],
                    amount=amount[i]
                )
                item_data.save()

            cust_email = custo.customerEmail

            subject = 'Delivery Challan'
            message = f'Dear Customer,\n Your Delivery Challan has been saved for a total amount of: {tot_in_string}'
            recipient = cust_email
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])

            return redirect('delivery_chellan_home')

        except Exception as e:
            # Handle exceptions or errors here
            # You can log the error or display an error message
            return HttpResponseServerError(f"An error occurred: {str(e)}")

    return render(request, 'create_challan.html')  # Render the create_challan template when it's a GET request

def create_and_send_challan(request):
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)
    
    if request.method == 'POST':
        x = request.POST["hidden_state"]
        y = request.POST["hidden_cus_place"]
        c = request.POST['customer_id']
        cus = customer.objects.get(id=c)
        custo = cus.id
        cust_name = cus.customerName
        chellan_no = request.POST['chellan_number']
        reference = request.POST['reference']
        chellan_date = request.POST['chellan_date']
        customer_mailid = request.POST['customer_mail']
        chellan_type = request.POST['chellan_type']
        
        if x == y:
            item = request.POST.getlist('item[]')
            hsn = request.POST.getlist('hsn[]')
            quantity1 = request.POST.getlist('quantity[]')
            quantity = [float(x) for x in quantity1]
            rate1 = request.POST.getlist('rate[]')
            rate = [float(x) for x in rate1]
            discount1 = request.POST.getlist('discount[]')
            discount = [float(x) for x in discount1]
            tax1 = request.POST.getlist('tax[]')
            tax = [float(x) for x in tax1]
            amount1 = request.POST.getlist('amount[]')
            amount = [float(x) for x in amount1]
        else:
            itemm = request.POST.getlist('itemm[]')
            hsnn = request.POST.getlist('hsnn[]')
            quantityy1 = request.POST.getlist('quantityy[]')
            quantityy = [float(x) for x in quantityy1]
            ratee1 = request.POST.getlist('ratee[]')
            ratee = [float(x) for x in ratee1]
            discountt1 = request.POST.getlist('discountt[]')
            discountt = [float(x) for x in discountt1]
            taxx1 = request.POST.getlist('taxx[]')
            taxx = [float(x) for x in taxx1]
            amountt1 = request.POST.getlist('amountt[]')
            amountt = [float(x) for x in amountt1]

        cust_note = request.POST['customer_note']
        sub_total = float(request.POST['subtotal'])
        igst = float(request.POST['igst'])
        sgst = float(request.POST['sgst'])
        cgst = float(request.POST['cgst'])
        tax_amnt = float(request.POST['total_taxamount'])
        shipping = float(request.POST['shipping_charge'])
        adjustment = float(request.POST['adjustment_charge'])
        total = float(request.POST['total'])
        tearms_conditions = request.POST['tearms_conditions']
        attachment = request.FILES.get('file')
        status = 'Send'
        tot_in_string = str(total)

        challan = DeliveryChellan(
            user=user,
            cu=cus,
            customer_name=cust_name,
            chellan_no=chellan_no,
            reference=reference,
            chellan_date=chellan_date,
            customer_mailid=customer_mailid,
            sub_total=sub_total,
            igst=igst,
            sgst=sgst,
            cgst=cgst,
            tax_amount=tax_amnt,
            chellan_type=chellan_type,
            shipping_charge=shipping,
            adjustment=adjustment,
            total=total,
            status=status,
            customer_notes=cust_note,
            terms_conditions=tearms_conditions,
            attachment=attachment
        )
        challan.save()

        if x == y:
            if len(item) == len(hsn) == len(quantity) == len(rate) == len(discount) == len(tax) == len(amount):
                mapped = zip(item, hsn, quantity, rate, discount, tax, amount)
                mapped = list(mapped)
                for element in mapped:
                    created = ChallanItems.objects.create(
                        chellan=challan, item_name=element[0], hsn=element[1], quantity=element[2], rate=element[3], discount=element[4], tax_percentage=element[5], amount=element[6])
        else:
            if len(itemm) == len(quantityy) == len(ratee) == len(discountt) == len(taxx) == len(amountt):
                mapped = zip(itemm, hsnn, quantityy, ratee, discountt, taxx, amountt)
                mapped = list(mapped)
                for element in mapped:
                    created = ChallanItems.objects.create(
                        chellan=challan, item_name=element[0], hsn=element[1], quantity=element[2], rate=element[3], discount=element[4], tax_percentage=element[5], amount=element[6])

        cust_email = customer.objects.get(user=user, customerName=cust_name).customerEmail
      
        subject = 'Delivery Challan'
        message = 'Dear Customer,\n Your Delivery Challan has been Saved for a total amount of: ' + tot_in_string
        recipient = cust_email
        send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])

    return redirect('delivery_chellan_home')


def add_customer_for_challan(request):
   
    return render(request,'create_cust_challan.html')
    
def payment_term_challan(request):
    if request.method=='POST':
        term=request.POST.get('term')
        day=request.POST.get('day')
        ptr=payment_terms(Terms=term,Days=day)
        ptr.save()
        return redirect("add_customer_for_challan")

def entr_custmr_for_challan(request):
    print("sdfdsfsds")
    type=request.GET.get('types')
    txtFullName=request.GET.get('txtFullNames')
    cpname=request.GET.get('cpnames')
    email=request.GET.get('email_ids')
    mobile=request.GET.get('mobiles')
    wbsite=request.GET.get('wbsites')
    gstt=request.GET.get('gstts')
    posply=request.GET.get('posplys')
    tax1=request.GET.get('tax1s')
    crncy=request.GET.get('crncys')
    obal=request.GET.get('obals')
    select=request.GET.get('ptermss')
    pterms=request.GET.get('ptermss')
    plst=request.GET.get('plsts')
    plang=request.GET.get('plangs')
    fbk=request.GET.get('fbks')
    twtr=request.GET.get('twtrs')
    atn=request.GET.get('atns')
    ctry=request.GET.get('ctrys')
    addrs=request.GET.get('addrss')
    addrs1=request.GET.get('addrs1s')
    bct=request.GET.get('bcts')
    bst=request.GET.get('bsts')
    bzip=request.GET.get('bzips')
    bpon=request.GET.get('bpons')
    bfx=request.GET.get('bfxs')
    sal=request.GET.get('sals')
    ftname=request.GET.get('ftnames')
    ltname=request.GET.get('ltnames')
    mail=request.GET.get('mails')
    bworkpn=request.GET.get('bworkpns')
    bmobile=request.GET.get('bmobiles')

    bskype=request.GET.get('bskypes')
    bdesg=request.GET.get('bdesgs')
    bdept=request.GET.get('bdepts')
    u = User.objects.get(id = request.user.id)


    ctmr=customer(customerName=txtFullName,customerType=type,
                companyName=cpname,customerEmail=email,
                    customerMobile=mobile,
                    website=wbsite,GSTTreatment=gstt,placeofsupply=posply, Taxpreference=tax1,
                        currency=crncy,OpeningBalance=obal,PaymentTerms=pterms,
                        PriceList=plst,PortalLanguage=plang,Facebook=fbk,Twitter=twtr,
                            Attention=atn,country=ctry,Address1=addrs,Address2=addrs1,
                            city=bct,state=bst,zipcode=bzip,phone1=bpon,
                            fax=bfx,CPsalutation=sal,Firstname=ftname,
                            Lastname=ltname,CPemail=mail,CPphone=bworkpn,
                            CPmobile= bmobile,CPskype=bskype,CPdesignation=bdesg,
                                CPdepartment=bdept,user=u )
    ctmr.save() 
    print(txtFullName)
    return JsonResponse({"status": " not", 'customer': txtFullName, "plos":posply})
        
@login_required(login_url='login')
def additem_page_challan(request):
    unit=Unit.objects.all()
    sale=Sales.objects.all()
    purchase=Purchase.objects.all()
    accounts = Purchase.objects.all()
    account_types = set(Purchase.objects.values_list('Account_type', flat=True))

    
    account = Sales.objects.all()
    account_type = set(Sales.objects.values_list('Account_type', flat=True))
    
    

    return render(request,'additem_challan.html',{'unit':unit,'sale':sale,'purchase':purchase,
               
                            "account":account,"account_type":account_type,"accounts":accounts,"account_types":account_types,
                            
                            })

def additem_challan(request):
    
    radio=request.GET.get('radios')
    inter=request.GET.get('inters')
    intra=request.GET.get('intras')
    type=request.GET.get('types')
    name=request.GET.get('names')
    hsn=request.GET.get('hsn')
    print(hsn)
    unit=request.GET.get('units')
    sel_price=request.GET.get('sel_prices')
    sel_acc=request.GET.get('sel_accs')
    s_desc=request.GET.get('s_descs')
    cost_price=request.GET.get('cost_prices')
    cost_acc=request.GET.get('cost_accs')      
    p_desc=request.GET.get('p_descs')
    u=request.user.id
    us=request.user
    history="Created by" + str(us)
    user=User.objects.get(id=u)
    unit=Unit.objects.get(id=unit)
    sel=Sales.objects.get(id=sel_acc)
    cost=Purchase.objects.get(id=cost_acc)
    ad_item=AddItem(type=type,Name=name,hsn=hsn,p_desc=p_desc,s_desc=s_desc,s_price=sel_price,p_price=cost_price,unit=unit,
                sales=sel,purchase=cost,user=user,creat=history,interstate=inter,intrastate=intra
                    )
    ad_item.save()

    return JsonResponse({"status": " not", 'name': name})

def delivery_challan_view(request, id):
    user = request.user
    company = company_details.objects.get(user=user)
    all_estimates = DeliveryChellan.objects.filter(user=user)
    estimate = DeliveryChellan.objects.get(id=id)
    items = ChallanItems.objects.filter(chellan=estimate)
    chellan_comments=delivery_chellan_comments.objects.filter(chellan=estimate.id,user=user)
    print(items)
    context = {
        'company': company,
        'all_estimates':all_estimates,
        'estimate': estimate,
        'items': items,
        'comments':chellan_comments,
    }
    return render(request, 'delivery_challan_view.html', context)


# delivery_challan_edit.html

def delivery_challan_edit(request,id):
    user = request.user
    company = company_details.objects.get(user=user)
    customers = customer.objects.filter(user_id=user.id)
    items = AddItem.objects.filter(user_id=user.id)
    estimate = DeliveryChellan.objects.get(id=id)
    cust=estimate.customer.placeofsupply
    cust_id=estimate.customer.id
    payments=payment_terms.objects.all()
    
    pls= customer.objects.get(customerName=estimate.customer_name)
    
    est_items = ChallanItems.objects.filter(chellan=estimate)

    unit=Unit.objects.all()
    sale=Sales.objects.all()
    purchase=Purchase.objects.all()
    accounts = Purchase.objects.all()
    account_types = set(Purchase.objects.values_list('Account_type', flat=True))

    
    account = Sales.objects.all()
    account_type = set(Sales.objects.values_list('Account_type', flat=True))

    

    context = {
        'company': company,
        'estimate': estimate,
        'customers': customers,
        'items': items,
        'est_items': est_items,
        'unit':unit,
        'sale':sale,
        'purchase':purchase,
        "account":account,
        "account_type":account_type,
        "accounts":accounts,
        "account_types":account_types,
        "pls":pls,
        'payments':payments,
        'cust':cust,
        'custo_id':cust_id,
    }
    return render(request, 'delivery_challan_edit.html', context)

def update_challan(request,id):
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)

    if request.method == "POST":
        x=request.POST["hidden_state"]
        y=request.POST["hidden_cus_place"]
        c=request.POST['customer_id']
        cus=customer.objects.get(id=c) 
        custo=cus
        cust_name =cus.customerName
        estimate = DeliveryChellan.objects.get(id=id)
        # estimate.customer_name = request.POST['customer_name']
        estimate.customer_name = cust_name
        estimate.customer=custo
        estimate.chellan_no = request.POST['chellan_number']
        estimate.reference = request.POST['reference']
        estimate.chellan_date = request.POST['challan_date']
        estimate.customer_mailid = request.POST['customer_mail']
        estimate.chellan_type = request.POST['chellan_type']
    

        estimate.customer_notes = request.POST['customer_note']
        estimate.sub_total = float(request.POST['subtotal'])
        estimate.tax_amount = float(request.POST['total_taxamount'])
        estimate.shipping_charge = float(request.POST['shipping_charge'])
        estimate.adjustment = float(request.POST['adjustment_charge'])
        estimate.total = float(request.POST['total'])
        estimate.terms_conditions = request.POST['tearms_conditions']
        estimate.status = 'Draft'

        old=estimate.attachment
        new=request.FILES.get('file')
        if old != None and new == None:
            estimate.attachment = old
        else:
            estimate.attachment = new

        estimate.save()

        if x==y:

            item = request.POST.getlist('item[]')
            hsn = request.POST.getlist('hsn[]')
            quantity1 = request.POST.getlist('quantity[]')
            quantity = [float(x) for x in quantity1]
            rate1 = request.POST.getlist('rate[]')
            rate = [float(x) for x in rate1]
            discount1 = request.POST.getlist('discount[]')
            discount = [float(x) for x in discount1]
            tax1 = request.POST.getlist('tax[]')
            tax = [float(x) for x in tax1]
            amount1 = request.POST.getlist('amount[]')
            amount = [float(x) for x in amount1]
        
        else:

            itemm = request.POST.getlist('itemm[]')
            hsnn = request.POST.getlist('hsnn[]')
            quantityy1 = request.POST.getlist('quantityy[]')
            quantityy = [float(x) for x in quantityy1]
            ratee1 = request.POST.getlist('ratee[]')
            ratee = [float(x) for x in ratee1]
            discountt1 = request.POST.getlist('discountt[]')
            discountt = [float(x) for x in discountt1]
            taxx1 = request.POST.getlist('taxx[]')
            taxx = [float(x) for x in taxx1]
            amountt1 = request.POST.getlist('amountt[]')
            amountt = [float(x) for x in amountt1]
       

        

        if x==y:
            if len(item) == len(hsn) ==  len(quantity) == len(rate) == len(discount) == len(tax) == len(amount):
                mapped = zip(item,hsn, quantity, rate, discount, tax, amount)
                mapped = list(mapped)
                for element in mapped:
                    created = ChallanItems.objects.get_or_create(
                        chellan=estimate, item_name=element[0], hsn=element[1], quantity=element[2], rate=element[3], discount=element[4], tax_percentage=element[5], amount=element[6])
            return redirect('delivery_chellan_home')

        else:
            if len(itemm) == len(hsnn) == len(quantityy) == len(ratee) == len(discountt) == len(taxx) == len(amountt):
                mapped = zip(itemm, hsnn, quantityy, ratee, discountt, taxx, amountt)
                mapped = list(mapped)
                for element in mapped:
                    created = ChallanItems.objects.create(
                        chellan=estimate, item_name=element[0],  hsn=element[1], quantity=element[2], rate=element[3], discount=element[4], tax_percentage=element[5], amount=element[6])
            return redirect('delivery_chellan_home')

    return redirect('delivery_chellan_home')

def get_cust_mail(request):
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)
    company = company_details.objects.get(user=user)
    # print(company.state)
  
    cust = request.GET.get('cust')
    print(cust)


    item = customer.objects.get(customerName=cust, user=user)

    
    email = item.customerEmail
    
    cust_place_supply=item.placeofsupply

    ads=item.Address1
   

    mob=item.customerMobile
    gstt=item.GSTTreatment
    gstno=item.GSTIN

    if gstt=="Unregistered Business-not Registered under GST":
        gstno="null"
    cust_id=item.id

    
    return JsonResponse({"status": " not", 'email': email,'ads':ads,'mob':mob,'cust_id':cust_id,'cust_place_supply':cust_place_supply,'gstt':gstt,'gstno':gstno})
    return redirect('/')
    
def add_customer_edit_challan(request):
   
    return render(request,'create_cust_challan_edit.html')



def payment_term_challan_edit(request):
    if request.method=='POST':
        term=request.POST.get('term')
        day=request.POST.get('day')
        ptr=payment_terms(Terms=term,Days=day)
        ptr.save()
        return redirect("add_customer_edit_challan")

def sv_cust_edit_challan(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            type=request.POST.get('type')
            txtFullName=request.POST['txtFullName']
            cpname=request.POST['cpname']
           
            email=request.POST.get('myEmail')
            wphone=request.POST.get('wphone')
            mobile=request.POST.get('mobile')
            skname=request.POST.get('skname')
            desg=request.POST.get('desg')      
            dept=request.POST.get('dept')
            wbsite=request.POST.get('wbsite')

            gstt=request.POST.get('gstt')
            posply=request.POST.get('posply')
            tax1=request.POST.get('tax1')
            crncy=request.POST.get('crncy')
            obal=request.POST.get('obal')

            select=request.POST.get('pterms')
           
            pterms=request.POST.get('pterms')

            plst=request.POST.get('plst')
            plang=request.POST.get('plang')
            fbk=request.POST.get('fbk')
            twtr=request.POST.get('twtr')
        
            atn=request.POST.get('atn')
            ctry=request.POST.get('ctry')
            
            addrs=request.POST.get('addrs')
            addrs1=request.POST.get('addrs1')
            bct=request.POST.get('bct')
            bst=request.POST.get('bst')
            bzip=request.POST.get('bzip')
            bpon=request.POST.get('bpon')
            bfx=request.POST.get('bfx')

            sal=request.POST.get('sal')
            ftname=request.POST.get('ftname')
            ltname=request.POST.get('ltname')
            mail=request.POST.get('mail')
            bworkpn=request.POST.get('bworkpn')
            bmobile=request.POST.get('bmobile')

            bskype=request.POST.get('bskype')
            bdesg=request.POST.get('bdesg')
            bdept=request.POST.get('bdept')
            u = User.objects.get(id = request.user.id)

          
            ctmr=customer(customerName=txtFullName,customerType=type,
                        companyName=cpname,customerEmail=email,customerWorkPhone=wphone,
                         customerMobile=mobile,skype=skname,designation=desg,department=dept,
                           website=wbsite,GSTTreatment=gstt,placeofsupply=posply, Taxpreference=tax1,
                             currency=crncy,OpeningBalance=obal,PaymentTerms=pterms,
                                PriceList=plst,PortalLanguage=plang,Facebook=fbk,Twitter=twtr,
                                 Attention=atn,country=ctry,Address1=addrs,Address2=addrs1,
                                  city=bct,state=bst,zipcode=bzip,phone1=bpon,
                                   fax=bfx,CPsalutation=sal,Firstname=ftname,
                                    Lastname=ltname,CPemail=mail,CPphone=bworkpn,
                                    CPmobile= bmobile,CPskype=bskype,CPdesignation=bdesg,
                                     CPdepartment=bdept,user=u )
            ctmr.save()  
            
            return redirect("delivery_chellan_home")
        return redirect("delivery_chellan_home")

@login_required(login_url='login')
def additem_edit_challan(request):
    unit=Unit.objects.all()
    sale=Sales.objects.all()
    purchase=Purchase.objects.all()
    accounts = Purchase.objects.all()
    account_types = set(Purchase.objects.values_list('Account_type', flat=True))

    
    account = Sales.objects.all()
    account_type = set(Sales.objects.values_list('Account_type', flat=True))
    
    

    return render(request,'additem_challanedit.html',{'unit':unit,'sale':sale,'purchase':purchase,
               
                            "account":account,"account_type":account_type,"accounts":accounts,"account_types":account_types,
                            
                            })

def additem_challan_edit(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            radio=request.POST.get('radio')
            if radio=='tax':
    
                
                inter=request.POST['inter']
                intra=request.POST['intra']
                type=request.POST.get('type')
                name=request.POST['name']
                unit=request.POST['unit']
                sel_price=request.POST.get('sel_price')
                sel_acc=request.POST.get('sel_acc')
                s_desc=request.POST.get('sel_desc')
                cost_price=request.POST.get('cost_price')
                cost_acc=request.POST.get('cost_acc')      
                p_desc=request.POST.get('cost_desc')
                u=request.user.id
                us=request.user
                history="Created by" + str(us)
                user=User.objects.get(id=u)
                unit=Unit.objects.get(id=unit)
                sel=Sales.objects.get(id=sel_acc)
                cost=Purchase.objects.get(id=cost_acc)
                ad_item=AddItem(type=type,Name=name,p_desc=p_desc,s_desc=s_desc,s_price=sel_price,p_price=cost_price,unit=unit,
                            sales=sel,purchase=cost,user=user,creat=history,interstate=inter,intrastate=intra
                                )
                
            else:
                                                  
                type=request.POST.get('type')
                name=request.POST['name']
                unit=request.POST['unit']
                sel_price=request.POST.get('sel_price')
                sel_acc=request.POST.get('sel_acc')
                s_desc=request.POST.get('sel_desc')
                cost_price=request.POST.get('cost_price')
                cost_acc=request.POST.get('cost_acc')      
                p_desc=request.POST.get('cost_desc')
                u=request.user.id
                us=request.user
                history="Created by" + str(us)
                user=User.objects.get(id=u)
                unit=Unit.objects.get(id=unit)
                sel=Sales.objects.get(id=sel_acc)
                cost=Purchase.objects.get(id=cost_acc)
                ad_item=AddItem(type=type,Name=name,p_desc=p_desc,s_desc=s_desc,s_price=sel_price,p_price=cost_price,unit=unit,
                            sales=sel,purchase=cost,user=user,creat=history,interstate='none',intrastate='none'
                                )
                ad_item.save()
            ad_item.save()
           
            return redirect("delivery_chellan_home")
    return redirect("additem_edit_challan")

@login_required(login_url='login')
def add_account_challan_edit(request):
    print("haii")
    if request.method=='POST':
        Account_type  =request.POST['acc_type']
        Account_name =request.POST['acc_name']
        Acount_code =request.POST['acc_code']
        Account_desc =request.POST['acc_desc']
       
        acc=Purchase(Account_type=Account_type,Account_name=Account_name,Acount_code=Acount_code,Account_desc=Account_desc)
        acc.save()                 
        return redirect("additem_edit_challan")
        
    return redirect("additem_edit_challan")

@login_required(login_url='login')
def add_unit_edit_challan(request):
    if request.method=='POST':
        unit_name=request.POST['unit_name']
        Unit(unit=unit_name).save()
        return redirect('additem_edit_challan')
    return redirect("additem_edit_challan")

@login_required(login_url='login')
def add_sales_edit_challan(request):
    if request.method=='POST':
        Account_type  =request.POST['acc_type']
        Account_name =request.POST['acc_name']
        Acount_code =request.POST['acc_code']
        Account_desc =request.POST['acc_desc']        
        acc=Sales(Account_type=Account_type,Account_name=Account_name,Acount_code=Acount_code,Account_desc=Account_desc)
        acc.save()
        return redirect('additem_edit_challan')
    return redirect("additem_edit_challan")

@login_required(login_url='login')
def add_account_challan(request):
    if request.method=='POST':
        Account_type  =request.POST['acc_type']
        Account_name =request.POST['acc_name']
        Acount_code =request.POST['acc_code']
        Account_desc =request.POST['acc_desc']
       
        acc=Purchase(Account_type=Account_type,Account_name=Account_name,Acount_code=Acount_code,Account_desc=Account_desc)
        acc.save()                 
        return redirect("additem_page_challan")
        
    return redirect("additem_page_challan")

@login_required(login_url='login')
def add_unit_challan(request):
    if request.method=='POST':
        unit_name=request.POST['unit_name']
        Unit(unit=unit_name).save()
        return redirect('additem_page_challan')
    return redirect("additem_page_challan")

@login_required(login_url='login')
def add_sales_challan(request):
    if request.method=='POST':
        Account_type  =request.POST['acc_type']
        Account_name =request.POST['acc_name']
        Acount_code =request.POST['acc_code']
        Account_desc =request.POST['acc_desc']        
        acc=Sales(Account_type=Account_type,Account_name=Account_name,Acount_code=Acount_code,Account_desc=Account_desc)
        acc.save()
        return redirect('additem_page_challan')
    return redirect("additem_page_challan")



def render_challan_pdf(request,id):

    user = request.user
    company = company_details.objects.get(user=user)
    challn_on = DeliveryChellan.objects.filter(user=user)
    challan = DeliveryChellan.objects.get(id=id)
    items = ChallanItems.objects.filter(chellan=challan)
    print(challan.customer_name) 
    print(challan.customer_mailid)
    customers = customer.objects.get(user=user,customerName=challan.customer_name,customerEmail=challan.customer_mailid)



    print(items)
    

    total = challan.total

    template_path = 'delivery_challan_pdf.html'
    context = {
        'company': company,
        'challn_on':challn_on,
        'challan': challan,
        'items': items,
        'customers':customers
    }
    fname=challan.chellan_no
   
    # Create a Django response object, and specify content_type as pdftemp_creditnote
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'
    response['Content-Disposition'] =f'attachment; filename= {fname}.pdf'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    


    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def deletechallan(request,id):
    user = request.user
    company = company_details.objects.get(user=user)
    estimate = DeliveryChellan.objects.get(id=id,user=user)
    items = ChallanItems.objects.filter(chellan=id)
    items.delete()
    estimate.delete()
    return redirect('delivery_chellan_home')
    
def filter_chellan(request):
    if request.method=='POST':
        flter_drop  =request.POST['flter_drop']
        company = company_details.objects.get(user = request.user)
        if flter_drop == "Draft":
            viewitem=DeliveryChellan.objects.filter(user=request.user, status="Draft") 
        elif flter_drop == "Send":
            viewitem=DeliveryChellan.objects.filter(user=request.user, status="Send")
        else:
            viewitem=DeliveryChellan.objects.filter(user=request.user)
        return render(request,'delivery_chellan.html',{'view':viewitem,"company":company})  
    return redirect("delivery_chellan_home") 
    
def filter_chellan_type(request):
    if request.method=='POST':
        flter_drop  =request.POST['flter_tp']
        usr_in  =request.POST['usr_in']
        company = company_details.objects.get(user = request.user)
        if flter_drop == "Customer":
            viewitem=DeliveryChellan.objects.filter(user=request.user, customer_name=usr_in) 
        elif flter_drop == "Date":
            fromdate=datetime.strptime(usr_in, "%d-%m-%Y").date()
            print(fromdate)

            viewitem=DeliveryChellan.objects.filter(user=request.user, chellan_date=fromdate)
        elif flter_drop == "Amount":
            viewitem=DeliveryChellan.objects.filter(user=request.user, total=usr_in)
        else:
            viewitem=DeliveryChellan.objects.filter(user=request.user)
        return render(request,'delivery_chellan.html',{'view':viewitem,"company":company})  
    return redirect("delivery_chellan_home") 
    
    
def itemdata_challan(request):
    cur_user = request.user
    user = cur_user.id
    try:
        id = request.GET.get('id')

        try:
            item = AddItem.objects.get(Name=id, user=user)
            name = item.Name
            rate = item.p_price
            # Assuming `company_name` is a field in the `company_details` model
            place = company_details.objects.get(user=cur_user).company_name
            return JsonResponse({"status": "not", 'place': place, 'rate': rate})
        except AddItem.DoesNotExist:
            return JsonResponse({"status": "error", 'message': "Item not found"})
    except Exception as e:
        return JsonResponse({"status": "error", 'message': str(e)})
    

def payment_term_for_sales(request):
    
    if request.method == 'POST':
        terms = json.loads(request.POST.get('terms', '[]'))
        days = json.loads(request.POST.get('days', '[]'))
        pay_term=terms[0]
        if len(terms) == len(days):
            for term, day in zip(terms, days):
                
                created = payment_terms.objects.get_or_create(Terms=term, Days=day)
            return JsonResponse({"message": "success","pay_term":pay_term})
        print(pay_term)
    return JsonResponse({"message": "success",})    
    
    
def report_page(request):
    return render(request,'reports.html')

def report_recurring_invoice(request):
    return render(request,'report_recurring_invoice.html')
    
def payment_recur(request):
    if request.method=='POST':
        print('hi')
        terms=request.POST.get('name')
        print(terms)
        day=request.POST.get('days')
        print(day)
        ptr=payments_recur(Terms=terms,Days=day)
        ptr.save()
        response_data={
            "message":"success",
            "terms":terms,
        }
        return JsonResponse(response_data)

def create_recur(request):
    user = request.user

    
    company = company_details.objects.get(user=user)
    # custo=customer.objects.get(cust_name=cust)
    item=AddItem.objects.all()
    sb=payment.objects.all()
    cus=customer.objects.filter(user=user)
    pay=payments_recur.objects.all()
    every=repeat_everyterms.objects.all()
    banks=Bankcreation.objects.filter(user=user)
    unit=Unit.objects.all()
    sales=Sales.objects.all()
    purchase=Purchase.objects.all()
    return render(request,'samrecurpage.html',{'item':item,'sb':sb,'cus':cus,'pay':pay,'company':company,'every':every,'banks':banks,'unit':unit,'sales':sales,'purchase':purchase,})

def new_recur(request):

    if request.method=='POST':
        
        custname=request.POST.get('customer')
        cus=customer.objects.get(customerName=custname)   
        custo=cus.id 
        cusemail=request.POST.get('mails')
        cusadd=request.POST.get('addr')
        gsttr=request.POST.get('gst')
        gstn=request.POST.get('gstnum')
        pos=request.POST.get('supply')
        e_type=request.POST.get('type')
        profile=request.POST.get('name')
        invoice=request.POST.get('recurno')
        onumber=request.POST.get('order')
        repeat=request.POST.get('every')
        pay_method=request.POST.get('method')
        sdate=request.POST.get('start')
        edate=request.POST.get('end')
        pay=request.POST.get('terms')
        pay_term_type =request.POST.get('terms_data_source')
        print(pay_term_type)
        notes=request.POST.get('customer_note')
        terms=request.POST.get('ter_cond')
        attach=request.POST.get('file')
        sub=request.POST.get('subtotal')
        i=request.POST.get('igst')
        c=request.POST.get('cgst')
        s=request.POST.get('sgst')
        taxamt=request.POST.get('total_taxamount')
        ship=request.POST.get('shipping_charge')
        adj=request.POST.get('adjustment_charge')
        tot=request.POST.get('total')
        paid=request.POST.get('paids')
        balance=request.POST.get('balance')
        status='Save'
       
        recur=Recurring_invoice(
            cname=custname,
            cemail=cusemail,
            cadrs=cusadd,
            gsttr=gsttr,
            gstnum=gstn,
            reinvoiceno=invoice,
            p_supply=pos,
            entry_type=e_type,
            name=profile,
            order_num=onumber,
            every=repeat,
            payment_method=pay_method,
            start=sdate,
            end=edate,
            terms=pay,
            payment_type=pay_term_type,
            attachment=attach,
            cust_note=notes,
            conditions=terms,
            sub_total=sub,
            igst=i,
            cgst=c,
            sgst=s,
            tax_amount=taxamt,
            shipping_charge=ship,
            adjustment=adj,
            total=tot,
            paid=paid,
            balance=balance,
            status=status,
            user = request.user,
            cust_name_id=custo,
            # cust_name=cus,

            # custname=request.cust_name

        )
        recur.save()
        items=request.POST.getlist('item[]')
        print(items)
        quantity1 = request.POST.getlist('quantity[]')
        quantity = [float(x) for x in quantity1]
        print(quantity)
        hsnc1 = request.POST.getlist('hsn[]')
        hsnc = [float(x) for x in hsnc1]
        rate1 = request.POST.getlist('rate[]')
        rate = [float(x) for x in rate1]
        print(rate)
        discount1 = request.POST.getlist('discount[]')
        discount = [float(x) for x in discount1]
        print(discount)
        tax1 = request.POST.getlist('tax[]')
        tax = [float(x) for x in tax1]
        print(tax)
        amount1 = request.POST.getlist('amount[]')
        amount = [float(x) for x in amount1]
        print(amount)
        
        if len(items)==len(quantity)==len(hsnc)==len(rate)==len(discount)==len(tax)==len(amount):
            print('testing')
            print(items)
            print(quantity)
            print(rate)
            print(discount)
            print(tax)
            print(amount)
            mapped1 = zip(items,quantity,hsnc,rate,discount,tax,amount)
            mapped = list(mapped1)
            for element in mapped:
                created =recur_itemtable.objects.get_or_create(
                    iname=element[0], quantity=element[1],hsncode=element[2], rate=element[3], discount=element[4], tax=element[5],amt=element[6],ri=recur)
        
                
        return redirect('view_recurpage')
    else:
        return render(request,'samrecurpage.html')


def view_recurpage(request):
    recur=Recurring_invoice.objects.all()
    company=company_details.objects.get(user_id=request.user.id)

    return render(request,'recurringonvoice.html',{'recur':recur,'company':company})

def viewrecur(request,id):    
    user = request.user

    cust = customer.objects.filter(user_id=request.user.id)
    company=company_details.objects.get(user_id=request.user.id)
    items=Recurring_invoice.objects.filter(user=user)
    product=Recurring_invoice.objects.get(id=id)
    table=recur_itemtable.objects.filter(ri=id)
    print(product.id)
    return render(request,'recur_invoice.html',{'customer':cust,'allproduct':items,'product':product,'itemstable':table,'company':company})


def edit_recur(request,id):
    banks=Bankcreation.objects.all()

    item=AddItem.objects.all()
    cus=customer.objects.all()
    pay=payments_recur.objects.all()
    banks=Bankcreation.objects.all()
    unit=Unit.objects.all()
    sales=Sales.objects.all()
    purchase=Purchase.objects.all()
    every=repeat_everyterms.objects.all()
    editr=Recurring_invoice.objects.get(id=id)
    tab=recur_itemtable.objects.filter(ri=id)
    company=company_details.objects.get(user_id=request.user.id)
    # print(type(editr.payment_type))

    return render(request,'edit_recur.html',{'editr':editr,'banks':banks,'cus':cus,'tab':tab,'item':item,'pay':pay,'every':every,'company':company,'unit':unit,'sales':sales,'purchase':purchase})  
   

def editrecurpage(request,id):
    print('edit view')
    if request.method=='POST':
        edit=Recurring_invoice.objects.get(id=id)
        edit.cname=request.POST['customer']
        edit.cemail=request.POST['mails']
        edit.cadrs=request.POST['addr']
        edit.gsttr=request.POST['gst']
        edit.gstnum=request.POST['gstnum']
        edit.p_supply=request.POST['supply']
        edit.entry_type=request.POST['type']
        edit.name=request.POST['name']
        edit.reinvoiceno=request.POST['recurno']
        edit.order_num=request.POST['order']
        edit.every=request.POST['every']
        edit.payment_method=request.POST['method']
        edit.start=request.POST['start']
        edit.end=request.POST['end']
        edit.terms=request.POST['terms']
        edit.cust_note=request.POST['customer_note']
        edit.conditions=request.POST['ter_cond']
        edit.adjustment=request.POST['adjustment_charge']
        edit.shipping_charge=request.POST['shipping_charge']
        edit.paid=request.POST['paids']
        edit.balance = float(request.POST['balance'])
        edit.sub_total = float(request.POST['subtotal'])
        edit.tax_amount = float(request.POST['total_taxamount'])
        edit.total = float(request.POST['total'])
        edit.cgst = float(request.POST['cgst'])
        edit.sgst = float(request.POST['sgst'])
        edit.igst = float(request.POST['igst'])
        items=request.POST.getlist('item[]')
        print(items)
        quantity1 = request.POST.getlist('quantity[]')
        quantity = [float(x) for x in quantity1]
        print(quantity)
        hsnc1 = request.POST.getlist('hsn[]')
        hsnc = [float(x) for x in hsnc1]
        rate1 = request.POST.getlist('rate[]')
        rate = [float(x) for x in rate1]
        print(rate)
        discount1 = request.POST.getlist('discount[]')
        discount = [float(x) for x in discount1]
        print(discount)
        tax1 = request.POST.getlist('tax[]')
        tax = [float(x) for x in tax1]
        print(tax)
        amount1 = request.POST.getlist('amount[]')
        amount = [float(x) for x in amount1]
        print(amount)
        objects_to_delete = recur_itemtable.objects.filter(ri_id=edit.id)
        objects_to_delete.delete()
        # sam=recur_itemtable.objects.filter(ri=id).delete()
        if len(items)==len(quantity)==len(hsnc)==len(rate)==len(discount)==len(tax)==len(amount):
            
            mapped1 = zip(items,quantity,hsnc,rate,discount,tax,amount)
            mapped = list(mapped1)
            for element in mapped:
                created =recur_itemtable.objects.create(
                    iname=element[0], quantity=element[1],hsncode=element[2], rate=element[3], discount=element[4], tax=element[5], amt=element[6],ri=edit)
        edit.save()
        return redirect('view_recurpage')



def del_recur(request,del_id):
    user = request.user
    company = company_details.objects.get(user=user)
    estimate =Recurring_invoice.objects.get(id=del_id)
    items =recur_itemtable.objects.filter(ri=estimate)
    items.delete()
    estimate.delete()
    # d=recurring_invoice.objects.get(id=id)
    # # d1=recur_itemtable.objects.get(id=id)
    # d.delete()
    # # d1.delete()
    return redirect('view_recurpage')


    
def itemdata_recur(request):
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)
    company = company_details.objects.get(user=user)
    print(company.state)
    id = request.GET.get('id')
    cust = request.GET.get('cust')
    print(id)
    print(cust)

    item = AddItem.objects.get(Name=id, user=user)

    rate = item.s_price
    place = company.state
    gst = item.intrastate
    igst = item.interstate
    hsncode=item.hsn
    place_of_supply = customer.objects.get(
        customerName=cust, user=user).placeofsupply
    return JsonResponse({"status": " not", 'place': place, 'rate': rate, 'pos': place_of_supply, 'gst': gst, 'igst': igst,'hsncode':hsncode})
    return redirect('/')


    
@login_required(login_url='login')
def recurring_bill(request):

    company = company_details.objects.get(user = request.user)
    recur = recurring_bills.objects.filter(user = request.user.id).values()
    pickup_records = []

    for r in recur:
        vn = r['vendor_name'].split()[1:]
        r['vend_name'] = " ".join(vn)
        cn = r['customer_name'].split()[2:]
        r['cust_name'] = " ".join(cn)
        record = {"start_date":str(r['start_date']),"bill_no":str(r['bill_no']),"profile_name":r['profile_name'],"vend_name":str(r['vend_name']),"cust_name":r['cust_name'],"grand_total":r['grand_total'],"balance":str(r['balance']),"id":r['id']}
        pickup_records.append(record)


    context = {
                'company' : company,
                'recur_bill' : pickup_records
            }
    return render(request,'recurring_bills.html',context)

# filter

@login_required(login_url='login')
def recur_custasc(request):

    company = company_details.objects.get(user = request.user)
    recur = recurring_bills.objects.filter(user = request.user.id).values()
    for r in recur:
        vn = r['vendor_name'].split()[1:]
        r['vend_name'] = " ".join(vn)
        cn = r['customer_name'].split()[2:]
        r['cust_name'] = " ".join(cn)

    sorted_recur = sorted(recur, key=lambda r: r['cust_name'])    

    context = {
                'company' : company,
                'recur_bill' : sorted_recur
            }
    return render(request,'recurring_bills.html',context)

@login_required(login_url='login')
def recur_custdesc(request):
    company = company_details.objects.get(user = request.user)
    recur = recurring_bills.objects.filter(user = request.user.id).values()
    for r in recur:
        vn = r['vendor_name'].split()[1:]
        r['vend_name'] = " ".join(vn)
        cn = r['customer_name'].split()[2:]
        r['cust_name'] = " ".join(cn)

    sorted_recur = sorted(recur, key=lambda r: r['cust_name'],reverse=True)    

    context = {
                'company' : company,
                'recur_bill' : sorted_recur
            }
    return render(request,'recurring_bills.html',context)

@login_required(login_url='login')
def recur_vendorasc(request):

    company = company_details.objects.get(user = request.user)
    recur = recurring_bills.objects.filter(user = request.user.id).values()
    for r in recur:
        vn = r['vendor_name'].split()[1:]
        r['vend_name'] = " ".join(vn)
        cn = r['customer_name'].split()[2:]
        r['cust_name'] = " ".join(cn)

    sorted_recur = sorted(recur, key=lambda r: r['vend_name'])    

    context = {
                'company' : company,
                'recur_bill' : sorted_recur
            }
    return render(request,'recurring_bills.html',context)

@login_required(login_url='login')
def recur_vendordesc(request):

    company = company_details.objects.get(user = request.user)
    recur = recurring_bills.objects.filter(user = request.user.id).values()
    for r in recur:
        vn = r['vendor_name'].split()[1:]
        r['vend_name'] = " ".join(vn)
        cn = r['customer_name'].split()[2:]
        r['cust_name'] = " ".join(cn)

        sorted_recur = sorted(recur, key=lambda r: r['vend_name'],reverse=True)    

    context = {
                'company' : company,
                'recur_bill' : sorted_recur
            }
    return render(request,'recurring_bills.html',context)

@login_required(login_url='login')
def recur_profileasc(request):

    company = company_details.objects.get(user = request.user)
    recur = recurring_bills.objects.filter(user = request.user.id).values()
    for r in recur:
        vn = r['vendor_name'].split()[1:]
        r['vend_name'] = " ".join(vn)
        cn = r['customer_name'].split()[2:]
        r['cust_name'] = " ".join(cn)

    sorted_recur = sorted(recur, key=lambda r: r['profile_name'],reverse=False) 

    context = {
                'company' : company,
                'recur_bill' : sorted_recur
            }
    return render(request,'recurring_bills.html',context)

@login_required(login_url='login')
def recur_profiledesc(request):

    company = company_details.objects.get(user = request.user)
    recur = recurring_bills.objects.filter(user = request.user.id).values()
    for r in recur:
        vn = r['vendor_name'].split()[1:]
        r['vend_name'] = " ".join(vn)
        cn = r['customer_name'].split()[2:]
        r['cust_name'] = " ".join(cn)

    sorted_recur = sorted(recur, key=lambda r: r['profile_name'],reverse=True) 

    context = {
                'company' : company,
                'recur_bill' : sorted_recur
            }
    return render(request,'recurring_bills.html',context)

@login_required(login_url='login')
def add_recurring_bills(request):

    company = company_details.objects.get(user=request.user)
    vendor = vendor_table.objects.filter(user=request.user)
    acnt_name = Chart_of_Account.objects.filter(user=request.user)
    acnt_type = Chart_of_Account.objects.filter(user=request.user).values('account_type').distinct()
    cust = customer.objects.filter(user=request.user)
    item = AddItem.objects.filter(user=request.user)
    payments = payment_terms.objects.exclude(Days__isnull=True).filter(user_id=request.user.id)
    units = Unit.objects.all()
    sales = Sales.objects.all()
    purchase = Purchase.objects.all()
    sales_type = set(Sales.objects.values_list('Account_type', flat=True))
    purchase_type = set(Purchase.objects.values_list('Account_type', flat=True))
    bank=Bankcreation.objects.all()
    last_id = recurring_bills.objects.filter(user_id=request.user.id).order_by('-id').values('id').first()
    print(last_id)
    if last_id !=  None:
        if request.user.is_authenticated:
            last_id = last_id['id']
            next_no = last_id + 1
        else:
            next_no = 1
    else:
         next_no = 1

    context = {
        'company': company,
        'vendor': vendor,
        'account': acnt_name,
        'account_type': acnt_type,
        'customer': cust,
        'item': item,
        'payments': payments,
        'units': units,
        'sales': sales,
        'purchase': purchase,
        'sales_type': sales_type,
        'purchase_type': purchase_type,
        'b_no': next_no,
        'bank':bank,

    }

    return render(request, 'add_recurring_bills.html', context)


@login_required(login_url='login')
def create_recurring_bills(request):

    company = company_details.objects.get(user = request.user)
    print(request.POST.get('customer').split(" ")[0])
    cust = customer.objects.get(id=request.POST.get('customer').split(" ")[0],user = request.user)

    if request.method == 'POST':
        # vname = request.POST.get('vendor').rsplit(' ', 1)
        # cname = request.POST.get('customer').split(" ")[1:]
        vname  = request.POST.get('vendor')
        cname = request.POST.get('customer')
        #cus=customer.objects.get(customerName=cname)   
        custo=cust.id 
        # cname = " ".join(cname)
        v_gst_no=request.POST.get('gstin_inp')   # haripriya add
        src_supply = request.POST.get('srcofsupply')
        prof = request.POST['prof_name']
        repeat = request.POST['repeats']
        start = request.POST.get('start_date')
        end = None if request.POST.get('end_date') == "" else  request.POST.get('end_date')
        pay_term =request.POST['terms']
        payment_method =request.POST['paymentmethod']
        amt_paid =request.POST['amtPaid']

        
        bill_no =  request.POST.get('bills')
        sub_total =request.POST['subtotal']
        adjustment =request.POST['add_round_off']

        sgst=None if request.POST.get('sgst') == "" else  request.POST.get('sgst')
        cgst=None if request.POST.get('cgst') == "" else  request.POST.get('cgst')
        igst= None if request.POST.get('igst') == "" else  request.POST.get('igst')

        status = 'Save'
        taxamount =request.POST['total_taxamount']

        shipping_charge=0 if request.POST['addcharge'] == "" else request.POST['addcharge']
        grand_total=request.POST['grand_total']
        note=request.POST.get('note')
        balance = float(grand_total) - float(amt_paid)
        u = User.objects.get(id = request.user.id)

        bills = recurring_bills(vendor_name=vname,profile_name=prof,customer_name = cname,vendor_gst_number=v_gst_no,
                    source_supply=src_supply,repeat_every = repeat,start_date = start,end_date = end,
                    payment_terms =pay_term,sub_total=sub_total,sgst=sgst,cgst=cgst,igst=igst,
                    tax_amount=taxamount, shipping_charge = shipping_charge,
                    grand_total=grand_total,note=note,company=company,user = u,cname_recur_id=custo,bill_no = bill_no,status = status,payment_method=payment_method, amt_paid=amt_paid,
                    adjustment = adjustment,balance = balance)
        bills.save()

        r_bill = recurring_bills.objects.get(id=bills.id)

        if len(request.FILES) != 0:
            r_bill.document=request.FILES['file'] 
            r_bill.save()

        items = request.POST.getlist("item[]")
        
        quantity = request.POST.getlist("qty[]")
        rate = request.POST.getlist("rate[]")
        
        if (src_supply.split("-")[1]) == company.state:
            tax = request.POST.getlist("tax1[]")
        else:
            tax = request.POST.getlist("tax2[]")

        discount = request.POST.getlist("discount[]") 
        amount = request.POST.getlist("amount[]")
        hsn = request.POST.getlist('HSN[]')

        print(items)
        print(quantity) 
        print(rate)
        print(tax) 
        print(discount) 
        print(amount) 
        print(hsn) 

        if len(items)==len(amount) == len(quantity) == len(rate)==len(tax) == len(discount) == len(hsn) and items and  quantity and rate and tax and discount and amount and hsn:
                
                mapped=zip(items,quantity,rate,tax,discount,amount,hsn)
                mapped=list(mapped)

                for ele in mapped:

                    it = AddItem.objects.get(user = request.user, id = ele[0]).Name
                        
                    created = recurring_bills_items.objects.create(item = it,quantity=ele[1],rate=ele[2],
                    tax=ele[3],discount = ele[4],amount=ele[5],hsn=ele[6], user = u,company = company, recur_bills = r_bill)
                
        return redirect('recurring_bill')
    
    return redirect('recurring_bill')


@login_required(login_url='login')
def edit_recurring_bills(request,id):

    company = company_details.objects.get(user = request.user)
    vendor = vendor_table.objects.filter(user = request.user)
    acnt = Chart_of_Account.objects.filter(user = request.user)
    acnt_type = Chart_of_Account.objects.filter(user = request.user).values('account_type').distinct()
    cust = customer.objects.filter(user = request.user)
    item = AddItem.objects.filter(user = request.user)
    payments = payment_terms.objects.exclude(Days__isnull=True).filter(user_id=request.user.id)
    units = Unit.objects.all()
    sales=Sales.objects.all()
    purchase=Purchase.objects.all()
    
    sales_type = set(Sales.objects.values_list('Account_type', flat=True))
    purchase_type = set(Purchase.objects.values_list('Account_type', flat=True))
    recur_bills = recurring_bills.objects.get(user = request.user,id=id)
    recur_item = recurring_bills_items.objects.filter(user = request.user,recur_bills = id) 
    c = customer.objects.filter(user = request.user).get(id = recur_bills.customer_name.split(' ')[0])
    v = vendor_table.objects.filter(user = request.user).get(id = recur_bills.vendor_name.split(" ")[0])
    bank=Bankcreation.objects.all()

    
    context = {
        'company' : company,
        'vendor' : vendor,
        'account': acnt,
        'account_type' : acnt_type,
        'customer' : cust,
        'item' : item,
        'payments' :payments,
        'units' :units,
        'sales' :sales,
        'purchase':purchase,
        'sales_type':sales_type,
        'purchase_type':purchase_type,
        'recur_bills': recur_bills,
        'recur_items' : recur_item,
        'cust':c,
        'vend' : v,
        'id': id,
        'vend_name' : " ".join(recur_bills.vendor_name.split(" ")[1:]),
        'cust_name' : " ".join(recur_bills.customer_name.split(" ")[2:]),
        'bank':bank,
        
    }

    return render(request,'edit_recurring_bills.html',context)



def change_recurring_bills(request,id):
            
    company = company_details.objects.get(user = request.user)
    # cust = customer.objects.get(customerName=request.POST.get('customer').strip(" "),user = request.user)
    r_bill=recurring_bills.objects.get(user = request.user,id=id)
    cust = customer.objects.get(id=request.POST.get('customer').split(" ")[0],user = request.user)

    if request.method == 'POST':
        
        r_bill.vendor_name = request.POST.get('vendor')
        r_bill.customer_name= request.POST.get('customer')
        r_bill.profile_name = request.POST['prof_name']
        r_bill.source_supply=request.POST['srcofsupply']
        r_bill.repeat_every=request.POST['repeats']
        r_bill.start_date=request.POST['start_date']
        r_bill.end_date=None if request.POST.get('end_date') == "" else  request.POST.get('end_date')
        r_bill.payment_terms=request.POST['terms']
        r_bill.note=request.POST['note']
        r_bill.sub_total=None if request.POST.get('subtotal') == "" else  request.POST.get('subtotal')
        r_bill.igst=None if request.POST.get('igst') == "" else  request.POST.get('igst')
        r_bill.cgst=None if request.POST.get('cgst') == "" else  request.POST.get('cgst')
        r_bill.sgst=None if request.POST.get('sgst') == "" else  request.POST.get('sgst')
        r_bill.shipping_charge=request.POST['addcharge']
        r_bill.grand_total=request.POST.get('grand_total')
        r_bill.payment_method =request.POST['paymentmethod']
        r_bill.amt_paid =request.POST['amtPaid']
        
        r_bill.bill_no =  request.POST.get('bills')
        r_bill.adjustment =request.POST['add_round_off']
        r_bill.status = 'Save'
        r_bill.tax_amount = request.POST['total_taxamount']
        r_bill.grand_total = request.POST.get('grand_total')
        r_bill.amt_paid = request.POST['amtPaid']
        grand_total = request.POST.get('grand_total')
        amt_paid = request.POST['amtPaid']
        r_bill.balance = float(grand_total) - float(amt_paid)

        r_bill.cname_recur_id = cust.id

        if len(request.FILES) != 0:
             
            r_bill.document = request.FILES['file']
            

        r_bill.save()          

        items = request.POST.getlist("item[]")
        
        quantity = request.POST.getlist("qty[]")
        rate = request.POST.getlist("rate[]")

        if (request.POST['srcofsupply'].split("-")[1]) == company.state:
            tax = request.POST.getlist("tax1[]")
        else:
            tax = request.POST.getlist("tax2[]")

        discount = request.POST.getlist("discount[]") 
        amount = request.POST.getlist("amount[]")
        hsn = request.POST.getlist('HSN[]')
        
        if len(items)==len(amount) == len(quantity) == len(rate)==len(tax) == len(discount) == len(hsn) and items and quantity and rate and tax and discount and amount and hsn:
                
            mapped=zip(items,quantity,rate,tax,discount,amount,hsn)
            mapped=list(mapped)

            objects_to_delete = recurring_bills_items.objects.filter(recur_bills=r_bill.id)
            objects_to_delete.delete()
            for ele in mapped: 
                     
                    it = ele[0]
                    if isNum(ele[0]):
                        it = AddItem.objects.get(user = request.user, id = ele[0]).Name

                    created = recurring_bills_items.objects.create(item = it,quantity=ele[1],rate=ele[2],
                    tax=ele[3],discount = ele[4],amount=ele[5],hsn=ele[6], user = request.user,company = company, recur_bills = r_bill)
            # count = recurring_bills_items.objects.filter(recur_bills=r_bill.id).count()
            
            # for ele in mapped:
            #     print('hellogioh')
            #     if int(len(items))>int(count):

            #         pbillss=recurring_bills.objects.get(id=id)
            #         company = company_details.objects.get(user = request.user)
            #         it = AddItem.objects.get(user = request.user, id = ele[0]).Name
            #         it = AddItem.objects.get(user = request.user, id = ele[0]).Name
            #         created = recurring_bills_items.objects.get_or_create(item = it,quantity=ele[1],rate=ele[2],
            #          tax=ele[3],discount = ele[4],amount=ele[5],hsn=ele[6],recur_bills=r_bill.id,company=company,user = request.user)

            #     else:
            #         print('hello')
            #         dbs=recurring_bills_items.objects.get(recur_bills =r_bill.id,item = ele[0])
            #         created = recurring_bills_items.objects.filter(recur_bills =dbs.recur_bills,item = ele[0]).update(item = ele[0],
            #             quantity=ele[1],rate=ele[2], tax=ele[3],discount=ele[4],amount= ele[5],hsn=ele[6])
 

        return redirect('view_recurring_bills',id)
    return redirect('recurring_bill')



@login_required(login_url='login')
def delete_recurring_bills(request, id):

    company = company_details.objects.get(user = request.user)
    rbill=recurring_bills.objects.get(user = request.user, id= id)
    billitem = recurring_bills_items.objects.filter(user = request.user,recur_bills=id)

    rbill.delete() 
    billitem.delete() 
     
    return redirect('recurring_bill')


@login_required(login_url='login')
def view_recurring_bills(request,id):
   
    company = company_details.objects.get(user = request.user)
    bills = recurring_bills.objects.filter(user = request.user)
    rbill=recurring_bills.objects.get(user = request.user, id= id)
    billitem = recurring_bills_items.objects.filter(user = request.user,recur_bills=id) 
    comment = rec_comments.objects.filter(recur_bills_id=rbill) 
    cust = customer.objects.get(id = rbill.customer_name.split(" ")[0])
    vend = vendor_table.objects.get(id = rbill.vendor_name.split(" ")[0])
    print(cust.state)
    print(company.state)
    gst_or_igst = "GST" if company.state.lower() == cust.state.lower() else "IGST"
    tax_total = [] 
    for b in billitem:
        if b.tax not in tax_total: 
            tax_total.append(b.tax)
    
    cust_name = cust.customerName
    vend_name = vend.salutation+ " " +vend.first_name + " " +vend.last_name
    context = {
                'company' : company,
                'recur_bills' : bills,
                'recur_bill' : rbill,
                'bill_item' : billitem,
                'tax' : tax_total,
                "gst_or_igst" : gst_or_igst,
                'customer' : cust,
                'vendor' : vend,
                'customer_name' : cust_name,
                'vendor_name' : vend_name,
                'comments':comment
            }

    return render(request, 'view_recurring_bills.html',context)



@login_required(login_url='login')
def view_custasc(request,id):
    company = company_details.objects.get(user = request.user)
    bills =recurring_bills.objects.filter(user = request.user).order_by('customer_name')

    rbill=recurring_bills.objects.get(user = request.user, id= id)
    billitem = recurring_bills_items.objects.filter(user = request.user,recur_bills=id)

    comp_state = company.state
    cust = customer.objects.get(customerName = rbill.customer_name)

    gst_or_igst = "GST" if comp_state == rbill.source_supply else "IGST"


    comp_state = company.state
    cust = customer.objects.get(id = rbill.customer_name.split(" ")[0])
    vend = vendor_table.objects.get(id = rbill.vendor_name.split(" ")[0])
    gst_or_igst = "GST" if comp_state == rbill.source_supply else "IGST"


    tax_total = 0 
    for b in billitem:
        tax_total += b.tax

    context = {
                'company' : company,
                'recur_bills' : bills,
                'recur_bill' : rbill,
                'bill_item' : billitem,
                'tax' : tax_total,
                "gst_or_igst" : gst_or_igst,
                'customer' : cust,
                'vendor' : vend,
            }
    return render(request,'view_recurring_bills.html',context)


@login_required(login_url='login')
def view_custdesc(request,id):
    company = company_details.objects.get(user = request.user)
    bills =recurring_bills.objects.filter(user = request.user).order_by('-customer_name')

    rbill=recurring_bills.objects.get(user = request.user, id= id)
    billitem = recurring_bills_items.objects.filter(user = request.user,recur_bills=id)

    comp_state = company.state
    cust = customer.objects.get(id = rbill.customer_name.split(" ")[0])
    vend = vendor_table.objects.get(id = rbill.vendor_name.split(" ")[0])
    gst_or_igst = "GST" if comp_state == rbill.source_supply else "IGST"


    tax_total = 0 
    for b in billitem:
        tax_total += b.tax

    context = {
                'company' : company,
                'recur_bills' : bills,
                'recur_bill' : rbill,
                'bill_item' : billitem,
                'tax' : tax_total,
                "gst_or_igst" : gst_or_igst,
                'customer' : cust,
                'vendor' : vend,
            }
    return render(request,'view_recurring_bills.html',context)

@login_required(login_url='login')
def view_vendorasc(request,id):
    company = company_details.objects.get(user = request.user)
    bills =recurring_bills.objects.filter(user = request.user).order_by('vendor_name')

    rbill=recurring_bills.objects.get(user = request.user, id= id)
    billitem = recurring_bills_items.objects.filter(user = request.user,recur_bills=id)

    comp_state = company.state
    cust = customer.objects.get(id = rbill.customer_name.split(" ")[0])
    vend = vendor_table.objects.get(id = rbill.vendor_name.split(" ")[0])
    gst_or_igst = "GST" if comp_state == rbill.source_supply else "IGST"


    tax_total = 0 
    for b in billitem:
        tax_total += b.tax

    context = {
                'company' : company,
                'recur_bills' : bills,
                'recur_bill' : rbill,
                'bill_item' : billitem,
                'tax' : tax_total,
                "gst_or_igst" : gst_or_igst,
                'customer' : cust,
                'vendor' : vend,
            }
    return render(request,'view_recurring_bills.html',context)

@login_required(login_url='login')
def view_vendordesc(request,id):
    company = company_details.objects.get(user = request.user)
    bills =recurring_bills.objects.filter(user = request.user).order_by('-vendor_name')

    rbill=recurring_bills.objects.get(user = request.user, id= id)
    billitem = recurring_bills_items.objects.filter(user = request.user,recur_bills=id)

    comp_state = company.state
    cust = customer.objects.get(id = rbill.customer_name.split(" ")[0])
    vend = vendor_table.objects.get(id = rbill.vendor_name.split(" ")[0])
    gst_or_igst = "GST" if comp_state == rbill.source_supply else "IGST"


    tax_total = 0 
    for b in billitem:
        tax_total += b.tax

    context = {
                'company' : company,
                'recur_bills' : bills,
                'recur_bill' : rbill,
                'bill_item' : billitem,
                'tax' : tax_total,
                "gst_or_igst" : gst_or_igst,
                'customer' : cust,
                'vendor' : vend,
            }
    return render(request,'view_recurring_bills.html',context)

@login_required(login_url='login')
def view_profileasc(request,id):
    company = company_details.objects.get(user = request.user)
    bills =recurring_bills.objects.filter(user = request.user).order_by('profile_name')

    rbill=recurring_bills.objects.get(user = request.user, id= id)
    billitem = recurring_bills_items.objects.filter(user = request.user,recur_bills=id)

    comp_state = company.state
    cust = customer.objects.get(id = rbill.customer_name.split(" ")[0])
    vend = vendor_table.objects.get(id = rbill.vendor_name.split(" ")[0])
    gst_or_igst = "GST" if comp_state == rbill.source_supply else "IGST"


    tax_total = 0 
    for b in billitem:
        tax_total += b.tax

    context = {
                'company' : company,
                'recur_bills' : bills,
                'recur_bill' : rbill,
                'bill_item' : billitem,
                'tax' : tax_total,
                "gst_or_igst" : gst_or_igst,
                'customer' : cust,
                'vendor' : vend,
            }
    return render(request,'view_recurring_bills.html',context)

@login_required(login_url='login')
def view_profiledesc(request,id):

    company = company_details.objects.get(user = request.user)
    bills =recurring_bills.objects.filter(user = request.user).order_by('-profile_name')

    rbill=recurring_bills.objects.get(user = request.user, id= id)
    billitem = recurring_bills_items.objects.filter(user = request.user,recur_bills=id)

    comp_state = company.state
    cust = customer.objects.get(customerName = rbill.customer_name)

    gst_or_igst = "GST" if comp_state == rbill.source_supplysupply else "IGST"


    tax_total = 0 
    for b in billitem:
        tax_total += b.tax

    context = {
                'company' : company,
                'recur_bills' : bills,
                'recur_bill' : rbill,
                'bill_item' : billitem,
                'tax' : tax_total,
                "gst_or_igst" : gst_or_igst,
                'customer' : cust,
            }
    return render(request,'view_recurring_bills.html',context)


@login_required(login_url='login')
def get_vendordet(request):

    company= company_details.objects.get(user = request.user)

    # fname = request.POST.get('fname')
    # lname = request.POST.get('lname')
    id = request.POST.get('id')
    vdr = vendor_table.objects.get(user=company.user_id, id=id)
    vemail = vdr.vendor_email
    gstnum = vdr.gst_number
    gsttr = vdr.gst_treatment
    source_supply = vdr.source_supply

    return JsonResponse({'vendor_email' :vemail, 'gst_number' : gstnum,'gst_treatment':gsttr,'source_supply':source_supply},safe=False)


@login_required(login_url='login')
def get_customerdet(request):
    company= company_details.objects.get(user = request.user)
    name = request.POST.get('name')
    id = request.POST.get('id')
    cust = customer.objects.get(user=company.user_id,id=id)
    email = cust.customerEmail
    cust_id=id
    cust_address=cust.Address1
    cust_place_supply=cust.placeofsupply
    gstin = cust.GSTIN
    gsttr = cust.GSTTreatment
    cstate = cust.placeofsupply.split("] ")[1:]
    print(email)
    print(gstin)
    print(id)
    state = 'Not Specified' if cstate == "" else cstate
    return JsonResponse({'customer_email' :email, 'gst_treatment':gsttr, 'gstin': gstin , 'state' : state,'cust_id':cust_id,'cust_place_supply':cust_place_supply,'cust_address':cust_address},safe=False)


@login_required(login_url='login')
def recurbills_vendor(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        title=request.POST.get('title')
        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')
        comp=request.POST.get('company_name')
        dispn = request.POST.get('display_name')
        email=request.POST.get('email')
        website=request.POST.get('website')
        w_mobile=request.POST.get('work_mobile')
        p_mobile=request.POST.get('pers_mobile')
        skype = request.POST.get('skype')
        desg = request.POST.get('desg')
        dpt = request.POST.get('dpt')
        gsttype=request.POST.get('gsttype')
        gstin=request.POST.get('gstin')
        panno=request.POST.get('panno')
        supply=request.POST.get('sourceofsupply')
        currency=request.POST.get('currency')
        balance=request.POST.get('openingbalance')
        payment=request.POST.get('paymentterms')
        street=request.POST.get('street')
        city=request.POST.get('city')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
        country=request.POST.get('country')
        fax=request.POST.get('fax')
        phone=request.POST.get('phone')
        shipstreet=request.POST.get('shipstreet')
        shipcity=request.POST.get('shipcity')
        shipstate=request.POST.get('shipstate')
        shippincode=request.POST.get('shippincode')
        shipcountry=request.POST.get('shipcountry')
        shipfax=request.POST.get('shipfax')
        shipphone=request.POST.get('shipphone')

        u = User.objects.get(id = request.user.id)

        vndr = vendor_table(salutation=title, first_name=first_name, last_name=last_name,vendor_display_name = dispn, company_name= comp, gst_treatment=gsttype, gst_number=gstin, 
                    pan_number=panno,vendor_wphone = w_mobile,vendor_mphone = p_mobile, vendor_email=email,skype_number = skype,
                    source_supply=supply,currency=currency, website=website, designation = desg, department = dpt,
                    opening_bal=balance,baddress=street, bcity=city, bstate=state, payment_terms=payment,bzip=pincode, 
                    bcountry=country, saddress=shipstreet, scity=shipcity, sstate=shipstate,szip=shippincode, scountry=shipcountry,
                    bfax = fax, sfax = shipfax, bphone = phone, sphone = shipphone,user = u)
        vndr.save()

        return HttpResponse({"message": "success"})
        
@login_required(login_url='login')
def vendor_dropdown(request):
    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = vendor_table.objects.filter(user = user)
    for option in option_objects:
        
        options[option.id] = [option.salutation, option.first_name, option.last_name, option.id]
    return JsonResponse(options)



@login_required(login_url='login')
def recurbills_pay(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        name=request.POST.get('name')
        days=request.POST.get('days')
        
        u = User.objects.get(id = request.user.id)

        pay = payment_terms(Terms=name, Days=days, user = u)
        pay.save()

        return HttpResponse({"message": "success"})
        
@login_required(login_url='login')
def pay_dropdown(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = payment_terms.objects.filter(user = user)
    for option in option_objects:
        options[option.id] = [option.Terms,option.Days]

    return JsonResponse(options)


@login_required(login_url='login')
def recurbills_unit(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        unit =request.POST.get('unit')
        
        u = User.objects.get(id = request.user.id)

        unit = Unit(unit= unit)
        unit.save()

        return HttpResponse({"message": "success"})
        
@login_required(login_url='login')
def unit_dropdown(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = Unit.objects.all()
    for option in option_objects:
        options[option.id] = [option.unit,option.id]

    return JsonResponse(options)

@login_required(login_url='login')
def recurbills_item(request):    #updation

    company = company_details.objects.get(user = request.user)

    if request.method=='POST':
        
        type=request.POST.get('type')
        name=request.POST.get('name')
       
        ut=request.POST.get('unit')
        inter=request.POST.get('inter')
        intra=request.POST.get('intra')
        sell_price=request.POST.get('sell_price')
        sell_acc=request.POST.get('sell_acc')
        sell_desc=request.POST.get('sell_desc')
        cost_price=request.POST.get('cost_price')
        cost_acc=request.POST.get('cost_acc')      
        cost_desc=request.POST.get('cost_desc')
        hsn_number = request.POST.get('hsn_number')
        
        
        units=Unit.objects.get(id=ut)
        sel=Sales.objects.get(id=sell_acc)
        cost=Purchase.objects.get(id=cost_acc)

        history="Created by " + str(request.user)

        u  = User.objects.get(id = request.user.id)

        item=AddItem(type=type,Name=name,p_desc=cost_desc,s_desc=sell_desc,s_price=sell_price,p_price=cost_price,
                     user=u ,creat=history,interstate=inter,intrastate=intra,unit = units,sales = sel, purchase = cost, hsn=hsn_number)

        item.save()

        return HttpResponse({"message": "success"})
    
    return HttpResponse("Invalid request method.")

        
@login_required(login_url='login')
def item_dropdown(request):
    user = User.objects.get(id=request.user.id)
    options = {}
    option_objects = AddItem.objects.filter(user=request.user)
    for option in option_objects:
        display_name = option.Name
        options[option.id] = [display_name, option.hsn, f"{display_name} - {option.hsn}"]

    return JsonResponse(options)


@login_required(login_url='login')
def recurbills_account(request):

    company = company_details.objects.get(user = request.user)


    if request.method=='POST':
        type=request.POST.get('actype')
        name=request.POST['acname']
        u = User.objects.get(id = request.user.id)
        
        acnt=Account(accountType=type,accountName=name,user = u)

        acnt.save()

        return HttpResponse({"message": "success"})
        
@login_required(login_url='login')
def account_dropdown(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = Chart_of_Account.objects.filter(user = user)
    for option in option_objects:
        options[option.id] = [option.account_name,option.id]

    return JsonResponse(options)


@login_required(login_url='login')
def get_rate(request):

    user = User.objects.get(id=request.user.id)
    if request.method=='POST':
        id=request.POST.get('id')

        item = AddItem.objects.get( id = id, user = user)
         
        rate = 0 if item.s_price == "" else item.s_price
        hsn = 0 if item.hsn == "" else item.hsn

        return JsonResponse({"rate": rate,"hsn":hsn},safe=False)
    
@login_required(login_url='login')
def get_cust_state(request):

    user = User.objects.get(id=request.user.id)
    if request.method=='POST':

        id=request.POST.get('id')
        cust = customer.objects.get(id = id, user = user)
        cstate = cust.placeofsupply.split("] ")[1]
        state = 'Not Specified' if cstate == "" else cstate

        return JsonResponse({"state": state},safe=False)
    
@login_required(login_url='login')
def export_pdf(request, id):
    company = company_details.objects.get(user=request.user)
    bills = recurring_bills.objects.filter(user=request.user)
    rbill = recurring_bills.objects.get(user=request.user, id=id)
    billitem = recurring_bills_items.objects.filter(user=request.user, recur_bills=id)

    comp_state = company.state
    cust = customer.objects.get(customerName=" ".join(rbill.customer_name.split(" ")[1:]))

    gst_or_igst = "GST" if comp_state == rbill.source_supply else "IGST"

    tax_total = 0
    for b in billitem:
        tax_total += b.tax

    template_path = 'view_recurring_bills.html'
    context = {
        'company': company,
        'recur_bills': bills,
        'recur_bill': rbill,
        'bill_item': billitem,
        'tax': tax_total,
        "gst_or_igst": gst_or_igst,
        'customer': cust,
    }
     
    fname= rbill.profile_name
   
    # Create a Django response object, and specify content_type as pdftemp_creditnote
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'
    response['Content-Disposition'] =f'attachment; filename= {fname}.pdf'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF( html, dest=response)
 
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



@login_required(login_url='login')
def recurbill_comment(request):

    company = company_details.objects.get(user = request.user)

    if request.method=='POST':
        id =request.POST.get('id')
        cmnt =request.POST.get('comment')
        
        u = User.objects.get(id = request.user.id)
        r_bill = recurring_bills.objects.get(user = request.user, id = id)
        r_bill.comments = cmnt
        r_bill.save()

        return HttpResponse({"message": "success"})

@login_required(login_url='login')
def recurbill_add_file(request,id):

    company = company_details.objects.get(user = request.user)
    bill = recurring_bills.objects.get(user = request.user,id=id)
    print(bill)

    if request.method == 'POST':

        bill.document=request.POST.get('file')

        if len(request.FILES) != 0:
             
            bill.document = request.FILES['file']

        bill.save()
        return redirect('view_recurring_bills',id)
    

@require_POST
def recurbill_email(request,id):

    company = company_details.objects.get(user = request.user)
    bill = recurring_bills.objects.get(user = request.user,id=id)

    if request.method == 'POST':

        recipient =request.POST.get('recipient')
        sender =request.POST.get('sender')
        sub =request.POST.get('subject')
        message =request.POST.get('message')

    script_directory = os.path.dirname(os.path.abspath(__file__))
    template_filename = 'view_recurring_bills.html'
    template_path = os.path.join(script_directory, 'templates', template_filename)

    with open(template_path, 'r') as file:
        html_content = file.read()
        

    soup = BeautifulSoup(html_content, 'html.parser')
    section = soup.find('div', class_='print-only')
    section_html = section.prettify()
    template = Template(section_html)

    if template:
        prntonly_content = str(template)

    # print(prntonly_content)
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as temp_file:
        temp_file.write(prntonly_content.encode('utf-8'))

    with open(temp_file.name, 'rb') as attachment_file:
        attachment_content = attachment_file.read()

    email = EmailMessage(
        subject=sub,
        body=message,
        from_email=sender,
        to=[recipient],
    )
    email.attach('Recurring Bill',attachment_content , 'text/html')

    email.send()
     
    return HttpResponse(status=200)
    
    
def get_comments(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    comments = Expense.objects.filter(expense=expense).values_list('comment', flat=True)
    return JsonResponse(list(comments), safe=False)
    

def every_terms(request):
    if request.method=='POST':
        print('hi')
        terms=request.POST.get('name')
        print(terms)
        ptr=repeat_everyterms(Terms=terms)
        ptr.save()
        response_data={
            "message":"success",
            "terms":terms,
        }
        return JsonResponse(response_data)
        
        
def cust_create(request):
    sb=payment_terms.objects.all()
    return render(request,'customer_cr.html',{'sb':sb})
    
def customer_me(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            type=request.POST.get('type')
            txtFullName=request.POST['txtFullName']
            cpname=request.POST['cpname']
           
            email=request.POST.get('email')
            wphone=request.POST.get('fname')
            mobile=request.POST.get('lname')
            skname=request.POST.get('skype')
            desg=request.POST.get('des')      
            dept=request.POST.get('dept')
            wbsite=request.POST.get('wbsite')

            gstt=request.POST.get('gstt')
            posply=request.POST.get('posply')
            tax1=request.POST.get('tax1')
            crncy=request.POST.get('crncy')
            obal=request.POST.get('obal')

            select=request.POST.get('pterms')
            pterms=payment_terms.objects.get(id=select)
            pterms=request.POST.get('pterms')

            plst=request.POST.get('plst')
            plang=request.POST.get('plang')
            fbk=request.POST.get('fbk')
            twtr=request.POST.get('twtr')
        
            atn=request.POST.get('atn')
            ctry=request.POST.get('ctry')
            
            addrs=request.POST.get('addrs')
            addrs1=request.POST.get('addrs1')
            bct=request.POST.get('bct')
            bst=request.POST.get('bst')
            bzip=request.POST.get('bzip')
            bpon=request.POST.get('bpon')
            bfx=request.POST.get('bfx')

            sal=request.POST.get('sal')
            ftname=request.POST.get('ftname')
            ltname=request.POST.get('ltname')
            mail=request.POST.get('mail')
            bworkpn=request.POST.get('bworkpn')
            bmobile=request.POST.get('bmobile')

            bskype=request.POST.get('bskype')
            bdesg=request.POST.get('bdesg')
            bdept=request.POST.get('bdept')
            u = User.objects.get(id = request.user.id)

          
            ctmr=customer(customerName=txtFullName,customerType=type,
                        companyName=cpname,customerEmail=email,customerWorkPhone=wphone,
                         customerMobile=mobile,skype=skname,designation=desg,department=dept,
                           website=wbsite,GSTTreatment=gstt,placeofsupply=posply, Taxpreference=tax1,
                             currency=crncy,OpeningBalance=obal,PaymentTerms=pterms,
                                PriceList=plst,PortalLanguage=plang,Facebook=fbk,Twitter=twtr,
                                 Attention=atn,country=ctry,Address1=addrs,Address2=addrs1,
                                  city=bct,state=bst,zipcode=bzip,phone1=bpon,
                                   fax=bfx,CPsalutation=sal,Firstname=ftname,
                                    Lastname=ltname,CPemail=mail,CPphone=bworkpn,
                                    CPmobile= bmobile,CPskype=bskype,CPdesignation=bdesg,
                                     CPdepartment=bdept,user=u )
            ctmr.save()  
            
            return redirect("create_recur")
        return redirect("/")
        
        
@login_required(login_url='login')
def recurbills_customer(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        # title=request.POST.get('title')
        # first_name=request.POST.get('firstname')
        # last_name=request.POST.get('lastname')
        # comp=request.POST.get('company_name')
        cust_type = request.POST.get('customer_type')
        name = request.POST.get('display_name')
        comp_name = request.POST.get('company_name')
        email=request.POST.get('email')
        website=request.POST.get('website')
        w_mobile=request.POST.get('work_mobile')
        p_mobile=request.POST.get('pers_mobile')
        fb = request.POST.get('facebook')
        twitter = request.POST.get('twitter')
        skype = request.POST.get('skype')
        desg = request.POST.get('desg')
        dpt = request.POST.get('dpt')
        
        gsttype=request.POST.get('gsttype')
        gst_num = request.POST.get('gst_num')
        pan_number = request.POST.get('pan_number')
        # gstin=request.POST.get('gstin')
        # panno=request.POST.get('panno')
        supply=request.POST.get('placeofsupply')
        tax = request.POST.get('tax_preference')
        currency=request.POST.get('currency')
        balance=request.POST.get('openingbalance')
        payment=request.POST.get('paymentterms')
        street1=request.POST.get('street1')
        street2=request.POST.get('street2')
        city=request.POST.get('city')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
        country=request.POST.get('country')
        fax=request.POST.get('fax')
        phone=request.POST.get('phone')
        # shipstreet1=request.POST.get('shipstreet1')
        # shipstreet2=request.POST.get('shipstreet2')
        # shipcity=request.POST.get('shipcity')
        # shipstate=request.POST.get('shipstate')
        # shippincode=request.POST.get('shippincode')
        # shipcountry=request.POST.get('shipcountry')
        # shipfax=request.POST.get('shipfax')
        # shipphone=request.POST.get('shipphone')

        u = User.objects.get(id = request.user.id)

        cust = customer(customerName = name,customerType = cust_type, companyName= comp_name, GSTTreatment=gsttype, GSTIN=gst_num, pan_no=pan_number,
                        customerWorkPhone = w_mobile,customerMobile = p_mobile, customerEmail=email,skype = skype,Facebook = fb, 
                        Twitter = twitter,placeofsupply=supply,Taxpreference = tax,currency=currency, website=website, 
                        designation = desg, department = dpt,OpeningBalance=balance,Address1=street1,Address2=street2, city=city, 
                        state=state, PaymentTerms=payment,zipcode=pincode,country=country,  fax = fax,  phone1 = phone,user = u)
        cust.save()

        return HttpResponse({"message": "success"})
        
        
@login_required(login_url='login')
def customer_dropdown(request):
    user = User.objects.get(id=request.user.id)
    options = {}
    option_objects = customer.objects.all()
    for option in option_objects:
        options[option.id] = {
            'customerName': option.customerName,
            'customerEmail': option.customerEmail,
            'GSTTreatment': option.GSTTreatment,
            'GSTIN': option.GSTIN,
            'placeofsupply': option.placeofsupply,
        }
    return JsonResponse(options)
    
    
def entr_custmrA(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            cr_data=customer()
            print('hii')
            print(cr_data)
            type=request.POST.get('type')
            fname=request.POST.get('fName')
            print(fname)
            lname=request.POST.get('lName')
            print(lname)
            txtFullName=request.POST.get('txtFullName')
            cpname=request.POST.get('cpname')           
            email=request.POST.get('email')
            wphone=request.POST.get('wphone')
            mobile=request.POST.get('mobile')
            skname=request.POST.get('skname')
            desg=request.POST.get('desg')      
            dept=request.POST.get('dept')
            wbsite=request.POST.get('wbsite')

            gstt=request.POST.get('v_gsttype')
            
            x=request.POST.get('v_gsttype')
            if x=="Unregistered Business-not Registered under GST":
                pan=request.POST.get('pan_number')
                gstin="null"
            else:
                gstin=request.POST.get('v_gstin')
                pan=request.POST.get('pan_number')
           
            posply=request.POST.get('posply')
            tax1=request.POST.get('tax1')
            crncy=request.POST.get('crncy')

            # select=request.POST.get('pterms')
            
            pterms=request.POST.get('terms')

            plst=request.POST.get('plst')
            plang=request.POST.get('plang')
            fbk=request.POST.get('fbk')
            twtr=request.POST.get('twtr')
        
            atn=request.POST.get('atn')
            ctry=request.POST.get('ctry')
            
            addrs=request.POST.get('addrs')
            addrs1=request.POST.get('addrs1')
            bct=request.POST.get('bct')
            bst=request.POST.get('bst')
            bzip=request.POST.get('bzip')
            bpon=request.POST.get('bpon')
            bfx=request.POST.get('bfx')
            remark=request.POST.get('remark')
            obal= float(request.POST.get('obal', 0.0))
            crdr=request.POST.get('bal')
            status='Active'
            u = User.objects.get(id = request.user.id)
            if crdr == 'credit':
                obal = -obal
            else:
                obal = obal
          
            ctmr=customer(customerName=txtFullName,
                          Fname=fname,Lname=lname,
                          customerType=type,
                        companyName=cpname,
                        customerEmail=email,
                        customerWorkPhone=wphone,
                         customerMobile=mobile,skype=skname,
                         designation=desg,department=dept,
                           website=wbsite
                           ,GSTTreatment=gstt,
                           GSTIN=gstin,pan_no=pan,
                           placeofsupply=posply, Taxpreference=tax1,
                             currency=crncy,OpeningBalance=obal,
                             PaymentTerms=pterms,
                                PriceList=plst,PortalLanguage=plang,
                                Facebook=fbk,
                                Twitter=twtr,
                                 Attention=atn,country=ctry,Address1=addrs,Address2=addrs1,
                                  city=bct,state=bst,zipcode=bzip,phone1=bpon,
                                   fax=bfx,
                                     remark=remark,cr_dr=crdr,status=status,user=u )
            ctmr.save() 
 
            #  ...........................adding multiple rows of table to model  ........................................................       
            CPsalutation =request.POST.getlist('sal[]')
            Firstname=request.POST.getlist('ftname[]')
            Lastname =request.POST.getlist('ltname[]')
            CPemail =request.POST.getlist('mail[]')
            CPphone=request.POST.getlist('bworkpn[]')
            CPmobile=request.POST.getlist('bmobile[]')
            CPskype=request.POST.getlist('bskype[]')
            CPdesignation=request.POST.getlist('bdesg[]')
            CPdepartment=request.POST.getlist('bdept[]') 
            
            cdata=customer.objects.get(id=ctmr.id)
            Customr=cdata 
            
            if len(CPsalutation)==len(Firstname)==len(Lastname)==len(CPemail)==len(CPphone)==len(CPmobile)==len(CPskype)==len(CPdesignation)==len(CPdepartment):
                mapped2=zip(CPsalutation,Firstname,Lastname,CPemail,CPphone,CPmobile,CPskype,CPdesignation,CPdepartment)
                mapped2=list(mapped2)
                print(mapped2)
                for ele in mapped2:
                    created = customer_contact_person_table.objects.get_or_create(CPsalutation=ele[0],Firstname=ele[1],Lastname=ele[2],CPemail=ele[3],
                            CPphone=ele[4],CPmobile=ele[5],CPskype=ele[6],CPdesignation=ele[7],CPdepartment=ele[8],user=u,Customr=Customr)
            
            return redirect("view_customr")
        return render(request,'view_customer.html') 
        
        
def payment_termA(request):
    if request.method=='POST':
        term=request.POST.get('term')
        day=request.POST.get('day')
        ptr=payment_terms(Terms=term,Days=day)
        ptr.save()
        return HttpResponse( {"message":"success"})
        
        
def dashboard(request):
    if not Unit.objects.filter(unit='BOX').exists():
            Unit(unit='BOX').save()
    if not Unit.objects.filter(unit='UNIT').exists():
            Unit(unit='UNIT').save()
    if not Unit.objects.filter(unit='LITRE').exists():
            Unit(unit='LITRE').save()

    if not Sales.objects.filter(Account_name='General Income').exists():
            Sales(Account_type='INCOME',Account_name='General Income',Account_desc='salesincome').save()
    if not Sales.objects.filter(Account_name='Intrest Income').exists():
            Sales(Account_type='INCOME',Account_name='Intrest Income',Account_desc='salesincome').save()
    if not Sales.objects.filter(Account_name='Late fee Income').exists():
            Sales(Account_type='INCOME',Account_name='Late fee Income',Account_desc='salesincome').save()
    if not Sales.objects.filter(Account_name='Discount Income').exists():
            Sales(Account_type='INCOME',Account_name='Discount Income',Account_desc='salesincome').save()
    if not Sales.objects.filter(Account_name='Other Charges').exists():
            Sales(Account_type='INCOME',Account_name='Other Charges',Account_desc='salesincome').save()
    if not Sales.objects.filter(Account_name='Shipping Charge').exists():
            Sales(Account_type='INCOME',Account_name='Shipping Charge',Account_desc='salesincome').save()

    



    if not  Purchase.objects.filter(Account_name='Advertising & Marketing').exists():
            Purchase(Account_type='EXPENCES',Account_name='Advertising & Markting',Account_desc='Advertsing Exp').save()
    if not Purchase.objects.filter(Account_name='Debit Charge').exists():
            Purchase(Account_type='EXPENCES',Account_name='Debit Charge',Account_desc='Debited Exp').save()
    if not Purchase.objects.filter(Account_name='Labour Charge').exists():
            Purchase(Account_type='EXPENCES',Account_name='Labour Charge',Account_desc='Labour Exp').save()
    if not Purchase.objects.filter(Account_name='Raw Meterials').exists():
            Purchase(Account_type='EXPENCES',Account_name='Raw Meterials',Account_desc='Raw Meterials Exp').save()
    if not Purchase.objects.filter(Account_name='Automobile Expense').exists():
            Purchase(Account_type='EXPENCES',Account_name='Automobile Expense',Account_desc='Automobile Expense').save()
    if not Purchase.objects.filter(Account_name='Bad Debt').exists():
            Purchase(Account_type='EXPENCES',Account_name='Bad Debt',Account_desc='Bad Debt').save()
    if not Purchase.objects.filter(Account_name='Bank Fees and Charges').exists():
            Purchase(Account_type='EXPENCES',Account_name='Bank Fees and Charges',Account_desc='Bank Fees and Charges').save()
    if not Purchase.objects.filter(Account_name='Consultant Expense').exists():
            Purchase(Account_type='EXPENCES',Account_name='Consultant Expense',Account_desc='Consultant Expense').save()
    if not Purchase.objects.filter(Account_name='Credit card Charges').exists():
            Purchase(Account_type='EXPENCES',Account_name='Credit card Charges',Account_desc='Credit card Charges').save()
    if not Purchase.objects.filter(Account_name='Depreciation Charges').exists():
            Purchase(Account_type='EXPENCES',Account_name='Depreciation Charges',Account_desc='Depreciation Charges').save()
    if not Purchase.objects.filter(Account_name='IT and Internet Expense').exists():
            Purchase(Account_type='EXPENCES',Account_name='IT and Internet Expense',Account_desc='IT and Internet Expense').save()
    if not Purchase.objects.filter(Account_name='Janitorial Expense').exists():
            Purchase(Account_type='EXPENCES',Account_name='Janitorial Expense',Account_desc='Janitorial Expense').save()
    if not Purchase.objects.filter(Account_name='Lodging').exists():
            Purchase(Account_type='EXPENCES',Account_name='Lodging',Account_desc='Lodging').save()
    if not Purchase.objects.filter(Account_name='Meals and Entertinment').exists():
            Purchase(Account_type='EXPENCES',Account_name='Meals and Entertinment',Account_desc='Meals and Entertinment').save()
    if not Purchase.objects.filter(Account_name='Office Supplies').exists():
            Purchase(Account_type='EXPENCES',Account_name='Office Supplies',Account_desc='Office Supplies').save()
    if not Purchase.objects.filter(Account_name='Other Expenses').exists():
            Purchase(Account_type='EXPENCES',Account_name='Other Expenses',Account_desc='Other Expenses').save()
    if not Purchase.objects.filter(Account_name='Postage').exists():
            Purchase(Account_type='EXPENCES',Account_name='Printing and sationary',Account_desc='Postage').save()
    if not Purchase.objects.filter(Account_name='Postage').exists():
            Purchase(Account_type='EXPENCES',Account_name='Printing and sationary',Account_desc='Printing and sationary').save()
    if not Purchase.objects.filter(Account_name='Rent Expenses').exists():
            Purchase(Account_type='EXPENCES',Account_name='Rent Expenses',Account_desc='Rent Expenses').save()
    if not Purchase.objects.filter(Account_name='Repair and maintenance').exists():
            Purchase(Account_type='EXPENCES',Account_name='Repair and maintenance',Account_desc='Repair and maintenance').save()
    if not Purchase.objects.filter(Account_name='Salaries and Employee wages').exists():
            Purchase(Account_type='EXPENCES',Account_name='Salaries and Employee wages',Account_desc='Salaries and Employee wages').save()
    if not Purchase.objects.filter(Account_name='Telephonic Expenses').exists():
            Purchase(Account_type='EXPENCES',Account_name='Telephonic Expenses',Account_desc='Telephonic Expenses').save()
    if not Purchase.objects.filter(Account_name='Travel Expenses').exists():
            Purchase(Account_type='EXPENCES',Account_name='Travel Expenses',Account_desc='Travel Expenses').save()
    if not Purchase.objects.filter(Account_name='Uncategorized').exists():
            Purchase(Account_type='EXPENCES',Account_name='Uncategorized',Account_desc='Uncategorized').save()
    if not Purchase.objects.filter(Account_name='Contract Assets').exists():
            Purchase(Account_type='EXPENCES',Account_name='Contract Assets',Account_desc='Contract Assets').save()
    if not Purchase.objects.filter(Account_name='Depreciation and Amoritisation').exists():
            Purchase(Account_type='EXPENCES',Account_name='Depreciation and Amoritisation',Account_desc='Depreciation and Amoritisation').save()
    if not Purchase.objects.filter(Account_name='Merchandise').exists():
            Purchase(Account_type='EXPENCES',Account_name='Merchandise',Account_desc='Merchandise').save()
    if not Purchase.objects.filter(Account_name='Raw material and Consumables').exists():
            Purchase(Account_type='EXPENCES',Account_name='Raw material and Consumables',Account_desc='Raw material and Consumables').save()
    if not Purchase.objects.filter(Account_name='Transportation Expenses').exists():
            Purchase(Account_type='EXPENCES',Account_name='Transportation Expenses',Account_desc='Transportation Expenses').save()
    if not Purchase.objects.filter(Account_name='Transportation Expenses').exists():
            Purchase(Account_type='EXPENCES',Account_name='Transportation Expenses',Account_desc='Transportation Expenses').save()
    if not Purchase.objects.filter(Account_name='Cost Of Goods Sold').exists():
            Purchase(Account_type='Cost Of Goods Sold',Account_name='Cost Of Goods Sold',Account_desc='Cost Of Goods Sold').save()
    if not Purchase.objects.filter(Account_name='Job Costing').exists():
            Purchase(Account_type='Cost Of Goods Sold',Account_name='Job Costing',Account_desc='Job Costing').save()
    if not Purchase.objects.filter(Account_name='Labour').exists():
            Purchase(Account_type='Cost Of Goods Sold',Account_name='Labour',Account_desc='Labour').save()
    if not Purchase.objects.filter(Account_name='Materials').exists():
            Purchase(Account_type='Cost Of Goods Sold',Account_name='Materials',Account_desc='Materials').save()
    if not Purchase.objects.filter(Account_name='Subcontractor').exists():
            Purchase(Account_type='Cost Of Goods Sold',Account_name='Subcontractor',Account_desc='Subcontractor').save()
    if not Purchase.objects.filter(Account_name='Furniture and Equipment').exists():
            Purchase(Account_type='Fixed Asset',Account_name='Furniture and Equipment',Account_desc='Furniture and Equipment').save() 

    if not Account.objects.filter(accountName='Advance Tax').exists():
        Account(accountType='Other Current Asset',accountName='Advance Tax',description='Advance Tax').save()
    if not Account.objects.filter(accountName='Employee Advance').exists():
        Account(accountType='Other Current Asset',accountName='Employee Advance',description='Employee Advance').save()
    if not Account.objects.filter(accountName='Furniture and Equipment').exists():
            Account(accountType='Fixed Asset',accountName='Furniture and Equipment',description='Furniture and Equipment').save()
    if not Account.objects.filter(accountName='Employee Reimbursement').exists():
        Account(accountType='Other Current Liability',accountName='Employee Reimbursement',description='Employee Reimbursement').save()
    if not Account.objects.filter(accountName='Advertising & Marketing').exists():
        Account(accountType='Expenses',accountName='Advertising & Marketing',description='Advertising & Marketing').save()
    if not Account.objects.filter(accountName='Automobile Expense').exists():
        Account(accountType='Expenses',accountName='Automobile Expense',description='Automobile Expense').save()

    userId=User.objects.get(id=request.user.id)
    if not payment_terms.objects.filter(Terms='NET 30',user=userId).exists():
        payment_terms(Terms='NET 30',user=userId).save()
    if not payment_terms.objects.filter(Terms='NET 60',user=userId).exists():
        payment_terms(Terms='NET 60',user=userId).save()
    if not payment_terms.objects.filter(Terms='NET 45',user=userId).exists():
        payment_terms(Terms='NET 45',user=userId).save()
    if not payment_terms.objects.filter(Terms='Due on Receipt',user=userId).exists():
        payment_terms(Terms='Due on Receipt',user=userId).save()

    if not repeat_every.objects.filter(Terms='Week').exists():
        repeat_every(Terms='Week').save()
    if not repeat_every.objects.filter(Terms='Month').exists():
        repeat_every(Terms='Month').save()
    
    if not repeat_every.objects.filter(Terms='Year').exists():
        repeat_every(Terms='Year').save()
    
    company=company_details.objects.get(user=request.user)
    return render(request,'Dashboard.html',{'company':company})
    
    
def delete_customr(request,id):
    if customer_comments_table.objects.filter(customr=id).exists():
        us2=customer_comments_table.objects.filter(customr=id)
        us2.delete()
    if customer_mail_table.objects.filter(customr=id).exists():
        us3=customer_mail_table.objects.filter(customr=id)
        us3.delete()
    if customer_doc_upload_table.objects.filter(customr=id).exists():

        us5=customer_doc_upload_table.objects.filter(customr=id)
        us5.delete()
    if customer_contact_person_table.objects.filter(Customr=id).exists():
        us4=customer_contact_person_table.objects.filter(Customr=id)
        us4.delete()
    cs=customer.objects.get(id=id)
    cs.delete()
    return redirect('view_customr')
    
def view_customr(request):
    company=company_details.objects.get(user=request.user)
    vc=customer.objects.all()
    return render(request,'view_customer.html',{'vc':vc,'company':company})
    
def view_customr_sname(request):
    company=company_details.objects.get(user=request.user)
    vc=customer.objects.order_by('customerName')
    return render(request,'view_customer.html',{'vc':vc,'company':company})
    
def view_customr_scpname(request):
    company=company_details.objects.get(user=request.user)
    vc=customer.objects.order_by('companyName')
    return render(request,'view_customer.html',{'vc':vc,'company':company})
    
def view_one_customer(request,id):
    company=company_details.objects.get(user=request.user)
    user_id=request.user.id
    udata=User.objects.get(id=user_id)
    # cus=customer.objects.filter(user=udata)
    cu=customer.objects.get(id=id)
    vc=customer.objects.all()
    em=customer_mail_table.objects.all()

    estimatecus=Estimates.objects.filter(customer_name=cu.customerName)
    retainer=RetainerInvoice.objects.filter(user=udata,customer_name_id=id)
    # sales=SalesOrder.objects.filter(user=udata,customer_id=id)
    delivery=DeliveryChellan.objects.filter(customer_name=cu.customerName)
    # inv=invoice.objects.filter(user=udata,customer_id=id)
    # credit=Creditnote.objects.filter(user=udata,customer_id=id)
    recur=Recurring_invoice.objects.filter(cname=cu.customerName)
    purchase=Purchase_Order.objects.filter(customer_name=cu.customerName)
    bills=PurchaseBills.objects.filter(customer_name=cu.customerName)
    recurbills=recurring_bills.objects.filter(user=udata,cname_recur_id=id)

    return render(request,'view_one_customer.html',{'vc':vc,'cu':cu,"company":company,'em':em,'estimatecus':estimatecus,'retainer':retainer,'recur':recur,'purchase':purchase,
                    'bills':bills,'recurbills':recurbills,'delivery':delivery,})
    
def editcustomer(request,id):
    company=company_details.objects.get(user=request.user)
    cu=customer.objects.get(id=id)
    pt=payment_terms.objects.all()
    prc=Pricelist.objects.all()
    if customer_contact_person_table.objects.filter(Customr=cu).exists():
        pdata=customer_contact_person_table.objects.filter(Customr=cu)
        return render(request,'edit_customer.html',{'cu':cu,'pt':pt,'prc':prc,'pdata':pdata})      

    else:
        return render(request,'edit_customer.html',{'cu':cu,'pt':pt,'prc':prc,'company':company})
    
    
def editEnter_customer(request,id):
        if request.method=='POST':
            edit=customer.objects.get(id=id)

            edit.customerType=request.POST.get('type')
            edit.Fname=request.POST.get('first_name')
            edit.Lname=request.POST.get('last_name')
            edit.customerName=request.POST.get('txtFullName')
            edit.companyName=request.POST.get('cpname')

            edit.customerEmail=request.POST.get('email')
            edit.customerWorkPhone=request.POST.get('wphone')
            edit.customerMobile=request.POST.get('mobile')
            edit.skype=request.POST.get('skname')
            edit.designation=request.POST.get('desg')
            edit.department=request.POST.get('dept')
            edit.website=request.POST.get('wbsite')
            edit.GSTTreatment=request.POST.get('gst')
            if edit.GSTTreatment=="Unregistered Business-not Registered under GST":
                edit.pan_no=request.POST.get('pan_number')
                edit.GSTIN=request.POST.get('gst_number')
            else:
                edit.GSTIN=request.POST.get('gst_number')
                edit.pan_no=request.POST.get('pan_number')
            
            edit.placeofsupply=request.POST.get('posply')
            edit.Taxpreference=request.POST.get('tax1')
            
            edit.PaymentTerms=request.POST.get('terms')
            
            edit.PriceList=request.POST.get('plst')
            edit.PortalLanguage=request.POST.get('plang')
            edit.Facebook=request.POST.get('fbk')
            edit.Twitter=request.POST.get('twtr')
            edit.Attention=request.POST.get('atn')
            edit.country=request.POST.get('ctry')

            edit.Address1=request.POST.get('addrs')
            edit.Address2=request.POST.get('addrs1')
            edit.city=request.POST.get('bct')
            edit.state=request.POST.get('bst')
            edit.zipcode=request.POST.get('bzip')
            edit.phone1=request.POST.get('bpon')
            edit.fax=request.POST.get('bfx')
            edit.remark=request.POST.get('remark')
            edit.OpeningBalance=float(request.POST.get('obal'))
            edit.cr_dr=request.POST.get('bal')
            if edit.cr_dr == 'credit':
                edit.OpeningBalance = -float(edit.OpeningBalance)
            else:
                edit.OpeningBalance = edit.OpeningBalance
            
           
            edit.save()

            
            # .......................contact_person_table................ deleting existing entries and inserting  ...............

            pdata=customer_contact_person_table.objects.filter(Customr=edit)
            CPsalutation =request.POST.getlist('sal[]')
            Firstname =request.POST.getlist('ftname[]')
            Lastname =request.POST.getlist('ltname[]')
            CPemail =request.POST.getlist('mail[]')
            CPphone =request.POST.getlist('bworkpn[]')
            CPmobile =request.POST.getlist('bmobile[]')
            CPskype =request.POST.getlist('bskype[]')
            CPdesignation =request.POST.getlist('bdesg[]')
            CPdepartment =request.POST.getlist('bdept[]') 

            cdata=customer.objects.get(id=edit.id)
            Customr=cdata 
            
            user_id=request.user.id
            u=User.objects.get(id=user_id)

            # .....  deleting existing rows......
            pdata.delete()
            if len(CPsalutation)==len(Firstname)==len(Lastname)==len(CPemail)==len(CPphone)==len(CPmobile)==len(CPskype)==len(CPdesignation)==len(CPdepartment):
                mapped2=zip(CPsalutation,Firstname,Lastname,CPemail,CPphone,CPmobile,CPskype,CPdesignation,CPdepartment)
                mapped2=list(mapped2)
                print(mapped2)
                for ele in mapped2:
                    created = customer_contact_person_table.objects.get_or_create(CPsalutation=ele[0],Firstname=ele[1],Lastname=ele[2],CPemail=ele[3],
                            CPphone=ele[4],CPmobile=ele[5],CPskype=ele[6],CPdesignation=ele[7],CPdepartment=ele[8],user=u,Customr=Customr)
            

            return redirect('view_customr')

        return render(request,'view_customer.html')  
        
def add_email_customer(request,id):
    cu=customer.objects.get(id=id)
    return render(request,'emailcustomer.html',{'cu':cu})
    
    
@login_required(login_url='login')    
def paymentmethod(request):
    id = request.user
    print(id)
    user = User.objects.get(id=request.user.id)
    company=company_details.objects.get(user=user)
    paymnt = payment_made.objects.filter(user=user)
    vendor = vendor_table.objects.all()
    banks = banking.objects.all()
    option = method.objects.all()
    context = {'paymnt':paymnt,'vendor':vendor,'banks':banks,'option':option,'company':company,}
    return render (request,'payment_method.html',context)

def paymentadd_method(request):
    company=company_details.objects.get(user=request.user)
    vendors = vendor_table.objects.filter(user=request.user)
    bank =  banking.objects.filter(user=request.user)
    option = method.objects.all()
    context = {'vendors':vendors,'bank':bank,'option':option,'company':company}
    return render(request,'payment_method_add.html',context)

def payment_add_details(request):
    if request.method == 'POST':
        select = request.POST['select']
        vendor = vendor_table.objects.get(id=select)
        payment_method = request.POST['payment_method']
        option = method.objects.get(id=payment_method)
        reference = request.POST['reference']
        date = request.POST['date']
        paid_through = request.POST['paid_through']
        amount = request.POST['amount']
        email = request.POST['email']
        balance = request.POST['balance']
        gst_treatment = request.POST['gst']
        gst_no = request.POST['gst_number']
        difference = request.POST['difference']
        
        # Determine whether it's "In-Hand Cash" or a bank name
        if paid_through == 'cash':
            cash_value = 'In-Hand Cash'
        else:
            bank_name = request.POST.get('bank_name_select', '')  # Adjust name if needed
            cash_value = bank_name
        user = User.objects.get(id=request.user.id)
        data = payment_made(
            reference=reference,
            payment=option,
            date=date,
            cash=cash_value,
            amount=amount,
            vendor=vendor,
            email=email,
            balance=balance,
            current_balance=difference,
            gst=gst_treatment,
            gst_number=gst_no,
            user=user
        )
        data.save()
        return redirect('paymentmethod')


    
def payment_details_view(request, pk):
    payment = get_object_or_404(payment_made, id=pk)
    vendors = vendor_table.objects.all()
    # Retrieve the queryset of payment_made_items objects you want to display in the template
    # For example, if you want to display all payment_made_items objects, you can do:
    payment_items = payment_made.objects.all()
    bank = banking.objects.all()  
    option = method.objects.all()
    company=company_details.objects.get(user=request.user)
    return render(request, 'payment_details.html', {'payment': payment, 'vendors': vendors, 'payment_items': payment_items,'bank':bank,'option':option,'company':company})




def payment_edit(request):
    payment_id = request.GET.get('payment_id')
    payment = get_object_or_404(payment_made,id=payment_id)
    vendor = vendor_table.objects.all()
    bank = banking.objects.all()
    option = method.objects.all()
    company=company_details.objects.get(user=request.user)
    return render(request,'payment_details_edit.html',{'payment':payment,'vendor':vendor,'bank':bank,'option':option,'company':company})


def payment_edit_view(request,pk):
    if request.method == 'POST':
        payment = payment_made.objects.get(id=pk)
        payments = request.POST.get('payment')
        option = method.objects.get(id=payments)
        payment.payment = option
        payment.reference = request.POST.get('reference')
        select = request.POST.get('select')
        vendor = vendor_table.objects.get(id=select)
        payment.vendor = vendor
        paid_through = request.POST['paid_through']
        
        print(f'paid_through: {paid_through}')  # Debugging output
        if paid_through == 'In-Hand Cash':
            cash_value = 'In-Hand Cash'
        else:
            bank_name = request.POST.get('bank_name_select', '')  # Debugging output
            cash_value = bank_name
        print(f'cash_value: {cash_value}')  # Debugging output
        payment.cash = cash_value

        payment.date = request.POST.get('date')
        payment.email = request.POST.get('email')
        payment.amount = request.POST.get('ammount')
        payment.balance = request.POST.get('balance')
        payment.current_balance = request.POST.get('current_balance')
        payment.gst = request.POST.get('gst')
        payment.gst_number = request.POST.get('gst_number')
        payment.save()
        return redirect('paymentmethod')
    return render(request, 'payment_details_edit.html',{'payment': payment})
    
def purchase_order(request):
    company=company_details.objects.get(user=request.user)
    vendor=vendor_table.objects.filter(user=request.user)
    cust=customer.objects.filter(user = request.user)
    payment=payment_terms.objects.all()
    item=AddItem.objects.all()
    account=Account.objects.all()
    unit=Unit.objects.all()
    sales=Sales.objects.all()
    purchase=Purchase.objects.all()
    context={
        'vendor':vendor,
        'customer':cust,
        'payment':payment,
        'item':item,
        'account':account,
        'units':unit,
        'sales':sales,
        'purchase':purchase,
        'company':company,
        
    }
        
    return render(request,'create_purchase_order.html',context)



def purchaseView(request):
    purchase_table=Purchase_Order.objects.all()
    purchase_order_table=Purchase_Order_items.objects.all()
    company=company_details.objects.get(id=request.user.id)
    context={
        'pt':purchase_table,
        'po_t':purchase_order_table,
        'company':company,
        }
    return render(request,'purchase_order.html',context)

@login_required(login_url='login')
def purchase_vendor(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        title=request.POST.get('title')
        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')
        comp=request.POST.get('company_name')
        dispn = request.POST.get('display_name')
        email=request.POST.get('email')
        website=request.POST.get('website')
        w_mobile=request.POST.get('work_mobile')
        p_mobile=request.POST.get('pers_mobile')
        skype = request.POST.get('skype')
        desg = request.POST.get('desg')
        dpt = request.POST.get('dpt')
        gsttype=request.POST.get('gsttype')
        gstin=request.POST.get('gstin')
        panno=request.POST.get('panno')
        supply=request.POST.get('sourceofsupply')
        currency=request.POST.get('currency')
        balance=request.POST.get('openingbalance')
        payment=request.POST.get('paymentterms')
        street=request.POST.get('street')
        city=request.POST.get('city')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
        country=request.POST.get('country')
        fax=request.POST.get('fax')
        phone=request.POST.get('phone')
        shipstreet=request.POST.get('shipstreet')
        shipcity=request.POST.get('shipcity')
        shipstate=request.POST.get('shipstate')
        shippincode=request.POST.get('shippincode')
        shipcountry=request.POST.get('shipcountry')
        shipfax=request.POST.get('shipfax')
        shipphone=request.POST.get('shipphone')

        u = User.objects.get(id = request.user.id)

        vndr = vendor_table(salutation=title, first_name=first_name, last_name=last_name,vendor_display_name = dispn, company_name= comp, gst_treatment=gsttype, gst_number=gstin, 
                    pan_number=panno,vendor_wphone = w_mobile,vendor_mphone = p_mobile, vendor_email=email,skype_number = skype,
                    source_supply=supply,currency=currency, website=website, designation = desg, department = dpt,
                    opening_bal=balance,baddress=street, bcity=city, bstate=state, payment_terms=payment,bzip=pincode, 
                    bcountry=country, saddress=shipstreet, scity=shipcity, sstate=shipstate,szip=shippincode, scountry=shipcountry,
                    bfax = fax, sfax = shipfax, bphone = phone, sphone = shipphone,user = u)
        vndr.save()

        return HttpResponse({"message": "success"})
        
@login_required(login_url='login')
def purchase_customer(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            tax=request.POST.get('tax')
            type=request.POST.get('title')
            first=request.POST['firstname']
            last=request.POST['lastname']
            txtFullName= request.POST['display_name']
            
            itemtype=request.POST.get('itemtype')
            cpname=request.POST['company_name']
            
            email=request.POST.get('email')
            wphone=request.POST.get('work_mobile')
            mobile=request.POST.get('pers_mobile')
            skname=request.POST.get('skype')
            desg=request.POST.get('desg')      
            dept=request.POST.get('dpt')
            wbsite=request.POST.get('website')

            gstt=request.POST.get('gsttype')
            posply=request.POST.get('placesupply')
            crncy=request.POST.get('currency')
            obal=request.POST.get('openingbalance')

           
            pterms=request.POST.get('paymentterms')

            plst=request.POST.get('plst')
            plang=request.POST.get('plang')
            fbk=request.POST.get('facebook')
            twtr=request.POST.get('twitter')
        
            ctry=request.POST.get('country')
            
            street=request.POST.get('street')
            shipstate=request.POST.get('shipstate')
            shipcity=request.POST.get('shipcity')
            bzip=request.POST.get('shippincode')
            shipfax=request.POST.get('shipfax')

            sal=request.POST.get('title')
            addres=street +','+ shipcity+',' + shipstate+',' + bzip
            adress2=addres
            u = User.objects.get(id = request.user.id)

            print(tax)
            ctmr=customer(customerName=txtFullName,customerType=itemtype,
                        companyName=cpname,customerEmail=email,customerWorkPhone=wphone,
                         customerMobile=mobile,skype=skname,designation=desg,department=dept,
                           website=wbsite,GSTTreatment=gstt,placeofsupply=posply, Taxpreference=tax,
                             currency=crncy,OpeningBalance=obal,PaymentTerms=pterms,
                                PriceList=plst,PortalLanguage=plang,Facebook=fbk,Twitter=twtr
                                 ,country=ctry,Address1=addres,Address2=adress2,
                                  city=shipcity,state=shipstate,zipcode=bzip,phone1=wphone,
                                   fax=shipfax,CPsalutation=sal,Firstname=first,
                                    Lastname=last,CPemail=email,CPphone=mobile,
                                    CPmobile= wphone,CPskype=skname,CPdesignation=desg,
                                     CPdepartment=dept,user=u )
            ctmr.save()

        return HttpResponse({"message": "success"})

@login_required(login_url='login')
def purchase_pay(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        name=request.POST.get('name')
        days=request.POST.get('days')
        
        u = User.objects.get(id = request.user.id)

        pay = payment_terms(Terms=name, Days=days, user = u)
        pay.save()

        return HttpResponse({"message": "success"})
        
@login_required(login_url='login')
def payment_dropdown(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = payment_terms.objects.filter(user = user)
    for option in option_objects:
        options[option.id] = option.Terms + str(option.Days)

    return JsonResponse(options)

@login_required(login_url='login')
def customer_det(request):

    company= company_details.objects.get(user = request.user)
    st=company.state
    name = request.POST.get('name')
    print(name)

    vdr = customer.objects.get(user=company.user_id,customerName=name)
    email = vdr.customerEmail
    gstin = 0
    gsttr = vdr.GSTTreatment
    adres=vdr.Address2
    streat=vdr.Address1
    city=vdr.city
    state=vdr.state
    print(email)
    return JsonResponse({'customer_email' :email, 'gst_treatment':gsttr, 'gstin': gstin,'adres':adres,'st':st,'streat':streat,'city':city,'state':state},safe=False)

    
@login_required(login_url='login')    
def vendor_det(request):

    company= company_details.objects.get(user = request.user)

    fname = request.POST.get('fname')
    lname = request.POST.get('lname')
    id = request.POST.get('id')
    vdr = vendor_table.objects.get(user=company.user_id,first_name = fname,last_name = lname,id=id)
    vemail = vdr.vendor_email
    gstnum = vdr.gst_number
    gsttr = vdr.gst_treatment
    address=vdr.baddress  + '' + vdr.bcity + ''+vdr.bstate +''+vdr.bzip+''+vdr.bcountry
    print(address)
    return JsonResponse({'vendor_email' :vemail, 'gst_number' : gstnum,'gst_treatment':gsttr,'address':address},safe=False)

    
@login_required(login_url='login')
def purchase_unit(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        unit =request.POST.get('unit')
        
        u = User.objects.get(id = request.user.id)

        unit = Unit(unit= unit)
        unit.save()

        return HttpResponse({"message": "success"})
        
@login_required(login_url='login')        
def purchase_unit_dropdown(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = Unit.objects.all()
    for option in option_objects:
        options[option.id] = option.unit

    return JsonResponse(options)

@login_required(login_url='login')
def purchase_item(request):
    if request.method=='POST':
        type=request.POST.get('type')
        name=request.POST['name']
        ut=request.POST['unit']
        hsn=request.POST['hsn']
        inter=request.POST['inter']
        intra=request.POST['intra']
        sell_price=request.POST.get('sell_price')
        sell_acc=request.POST.get('sell_acc')
        sell_desc=request.POST.get('sell_desc')
        cost_price=request.POST.get('cost_price')
        cost_acc=request.POST.get('cost_acc')      
        cost_desc=request.POST.get('cost_desc')
        invasset=request.POST.get('invasset')
        opening_stock=request.POST.get('opening_stock')
        opening_stock_unit=request.POST.get('opening_stock_unit')
        active_type=request.POST.get('active_type')
        units=Unit.objects.get(id=ut)
        sel=Sales.objects.get(id=sell_acc)
        cost=Purchase.objects.get(id=cost_acc)

        history="Created by " + str(request.user)
        user = User.objects.get(id = request.user.id)

        item=AddItem(type=type,hsn=hsn,unit=units,sales=sel,purchase=cost,Name=name,p_desc=cost_desc,s_desc=sell_desc,s_price=sell_price,
                    p_price=cost_price,user=user,creat=history,interstate=inter,intrastate=intra,invacc=invasset,stock=opening_stock,
                    rate=opening_stock_unit,satus=active_type,status_stock=active_type)

        item.save()
        return HttpResponse({"message": "success"})
        
@login_required(login_url='login')        
def purchase_item_dropdown(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = AddItem.objects.all()
    for option in option_objects:
        options[option.id] = option.Name

    return JsonResponse(options)
    
@login_required(login_url='login')    
def purchase_account(request):

    company = company_details.objects.get(user = request.user)


    if request.method=='POST':
        type=request.POST.get('actype')
        name=request.POST['acname']
        u = User.objects.get(id = request.user.id)

        acnt=Account(accountType=type,accountName=name,user = u)

        acnt.save()

        return HttpResponse({"message": "success"})
        

@login_required(login_url='login')
def purchase_account_dropdown(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = Account.objects.filter(user = user)
    for option in option_objects:
        options[option.id] = option.accountName

    return JsonResponse(options)


@login_required(login_url='login')
def create_Purchase_order(request):

    company = company_details.objects.get(user = request.user)
    if request.method == 'POST':
        typ=request.POST.get('option')
        vname = request.POST.get('vendor')
        vmail = request.POST.get('email_inp')
        vgst_t = request.POST.get('gst_trt_inp')
        vgst_n = request.POST.get('gstin_inp')
            
        orgname = request.POST.get('orgName')
        org_gst = request.POST.get('gstNumber')
        org_address = request.POST.get('orgAddress')
        org_street = request.POST.get('orgstreet')
        org_city = request.POST.get('orgcity')
        org_state = request.POST.get('orgstate')
            
        cname = request.POST.get('custom')
        cus=customer.objects.get(customerName=cname)   
        custo=cus.id 
        cmail = request.POST.get('custMail')
        caddress = request.POST.get('custAddress')
        cstreet = request.POST.get('custStreet')
        ccity = request.POST.get('custcity')
        cstate = request.POST.get('custstate')

        src_supply = request.POST.get('srcofsupply')
        po = request.POST['pur_ord']
        ref = request.POST['ref']
        terms = request.POST['terms']
        start = request.POST.get('start_date')
        end =  request.POST.get('end_date')
        sub_total =request.POST['subtotal']
        sgst=request.POST['sgst']
        cgst=request.POST['cgst']
        igst=request.POST['igst']
        tax = request.POST['total_taxamount']
        shipping_charge= request.POST['shipping_charge']
        grand_total=request.POST['grandtotal']
        note=request.POST['customer_note']
        payment_type=request.POST['ptype']
        terms_con = request.POST['tearms_conditions']
        orgMail=request.POST.get('orgMail')
        u = User.objects.get(id = request.user.id)
        print('yes')
        print(typ)
        if typ=='Organization':
           

            purchase = Purchase_Order(vendor_name=vname,
                                    vendor_mail=vmail,
                                    vendor_gst_traet=vgst_t,
                                    vendor_gst_no=vgst_n,
                                    Org_name=orgname,
                                    Org_address=org_address,
                                    Org_gst=org_gst,
                                    Org_street=org_street,
                                    Org_city=org_city,
                                    Org_state=org_state,
                                    Org_mail=orgMail,
                                    Pur_no=po,
                                    ref=ref,
                                    customer_name = '',
                                    customer_mail='',
                                    customer_address='',
                                    customer_street='',
                                    customer_city='',
                                    customer_state='',
                                    source_supply=src_supply,
                                    payment_terms = terms,
                                    Ord_date = start,
                                    exp_date = end,
                                    sub_total=sub_total,
                                    sgst=sgst,
                                    cgst=cgst,
                                    igst=igst,
                                    tax_amount=tax,
                                    shipping_charge = shipping_charge,
                                    grand_total=grand_total,
                                    note=note,
                                    
                                    term=terms_con,
                                    company=company,
                                    custo_id=custo,
                                    user = u,typ=typ  )
            purchase.save()

            p_bill = Purchase_Order.objects.get(id=purchase.id)

            if len(request.FILES) != 0:
                p_bill.document=request.FILES['file'] 
                p_bill.save()
                print('save')
        else:
            purchase = Purchase_Order(vendor_name=vname,
                                    vendor_mail=vmail,
                                    vendor_gst_traet=vgst_t,
                                    vendor_gst_no=vgst_n,
                                    customer_name = cname,
                                    customer_mail=cmail,
                                    customer_street=cstreet,
                                    customer_city=ccity,
                                    customer_state=cstate,
                                    Pur_no=po,
                                    ref=ref,
                                    Org_name='',
                                    Org_address='',
                                    Org_gst='',
                                    Org_street='',
                                    Org_city='',
                                    Org_state='',
                                    Org_mail='',
                                    customer_address=caddress,
                                    source_supply=src_supply,
                                    payment_terms = terms,
                                    Ord_date = start,
                                    exp_date = end,
                                    sub_total=sub_total,
                                    sgst=sgst,
                                    cgst=cgst,
                                    igst=igst,
                                    tax_amount=tax,
                                    shipping_charge = shipping_charge,
                                    grand_total=grand_total,
                                    note=note,
                                    
                                    term=terms_con,
                                    company=company,
                                    user = u,typ=typ)
            purchase.save()

            p_bill = Purchase_Order.objects.get(id=purchase.id)

    
            if len(request.FILES) != 0:
                p_bill.document=request.FILES['file'] 
                p_bill.save()
                print('save')
            item = request.POST.getlist("item[]")
            # accounts = request.POST.getlist("account[]")
            quantity = request.POST.getlist("quantity[]")
            rate = request.POST.getlist("rate[]")
            tax = request.POST.getlist("tax[]")
            discount = request.POST.getlist("discount[]")
            amount = request.POST.getlist("amount[]")
            if len(item) == len(quantity) == len(rate) == len(discount) == len(tax) == len(amount):
                for i in range(len(item)):
                    created = Purchase_Order_items.objects.create(
                        item=item[i],
                        quantity=quantity[i],
                        rate=rate[i],
                        tax=tax[i],
                        discount=discount[i],
                        amount=amount[i],
                        user=u,
                        company=company,
                        PO=p_bill
                    )
                print('Done')

        return redirect('purchaseView')
    return render(request,'create_purchase_order.html')

def purchase_delet(request,id):
    po=Purchase_Order.objects.get(id=id)
    po.delete()
    return redirect('purchaseView')

    
def purchase_bill_view(request,id):
    po=Purchase_Order.objects.all()
    po_t=Purchase_Order_items.objects.filter(PO=id)
    po_table=Purchase_Order.objects.get(id=id)
    company=company_details.objects.get(user_id=request.user.id)
    po_item=Purchase_Order.objects.get(id=id)
    context={
        'po':po,
        'pot':po_t,
        'company':company,
        'po_table':po_table,
        'po_item':po_item,
    }
    return render(request, 'purchase_bill_view.html',context)
    
    
def EmailAttachementView_purchase(request):

        if request.method == 'POST':
                
            subject =request.POST['subject']
            message = request.POST['message']
            email = request.POST['email']
            files = request.FILES.getlist('attach')

            try:
                mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email])
                for f in files:
                    mail.attach(f.name, f.read(), f.content_type)
                mail.send()
                return render(request, 'purchasemail.html')
            except:
               return render(request, 'purchasemail.html')

        return render(request, 'purchasemail.html')
        
        
def export_purchase_pdf(request,id):

    user = request.user
    company = company_details.objects.get(user=user)
    challn_on = Purchase_Order.objects.filter(user=user)
    challan = Purchase_Order.objects.get(id=id)
    items = Purchase_Order_items.objects.filter(PO=challan)
    print(challan.customer_name) 
    print(challan.customer_name)
    total = challan.grand_total

    template_path = 'pdfchallan.html'
    context = {
        'company': company,
        'pot':challn_on,
        'po_item': challan,
        'po_table': items, 
    }
    fname=challan.Pur_no
   
    # Create a Django response object, and specify content_type as pdftemp_creditnote
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'
    response['Content-Disposition'] =f'attachment; filename= {fname}.pdf'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    


    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def edit(request,pk):
    company = company_details.objects.get(user = request.user)
    vendor=vendor_table.objects.all()
    cust=customer.objects.filter(user = request.user)
    payment=payment_terms.objects.all()
    item=AddItem.objects.all()
    account=Account.objects.all()
    unit=Unit.objects.all()
    sales=Sales.objects.all()
    purchase=Purchase.objects.all()
    po=Purchase_Order.objects.get(id=pk)
    po_tabl=Purchase_Order_items.objects.filter(PO=pk)
    context={
        'vendor':vendor,
        'customer':cust,
        'payment':payment,
        'item':item,
        'account':account,
        'units':unit,
        'sales':sales,
        'purchase':purchase,
        'po':po,        
        'po_table':po_tabl,
        'company':company
    }
    return render(request,'edit_purchase_order.html',context)
    
    
def edit_Purchase_order(request,id):

    company = company_details.objects.get(user = request.user)
    po_id=Purchase_Order.objects.get(id=id)
    if request.method == 'POST':
        typ=request.POST['typ']
        print('yes')
        print(typ)
        if typ=='Organization':
            po_id.vendor_name = request.POST.get('vendor')
            po_id.vendor_mail = request.POST.get('email_inp')
            po_id.vendor_gst_traet = request.POST.get('gst_trt_inp')
            po_id.vendor_gst_no = request.POST.get('gstin_inp')
            po_id.typ=typ
            po_id.Org_name = request.POST.get('orgName')
            po_id.Org_address = request.POST.get('gstNumber')
            po_id.Org_gst = request.POST.get('orgAddress')

            po_id.Org_street=request.POST.get('orgstreet')
            po_id.Org_city=request.POST.get('orgcity')
            po_id.Org_state=request.POST.get('orgstate')
            po_id.Org_mail=request.POST.get('orgMail')

            po_id.customer_name = ''
            po_id.customer_mail = ''
            po_id.customer_address = ''
            po_id.customer_street = ''
            po_id.customer_city = ''
            po_id.customer_state = ''
            

            po_id.source_supply = request.POST.get('srcofsupply')
            po_id.Pur_no = request.POST['pur_ord']
            po_id.ref = request.POST['ref']
            po_id.payment_terms = request.POST['terms']
            po_id.Ord_date = request.POST.get('start_date')
            po_id.exp_date =  request.POST.get('end_date')
            po_id.sub_total =request.POST['subtotal']
            po_id.sgst=request.POST['sgst']
            po_id.cgst=request.POST['cgst']
            po_id.igst=request.POST['igst']
            po_id.tax_amount = request.POST['total_taxamount']
            po_id.shipping_charge= request.POST['shipping_charge']
            po_id.grand_total=request.POST['grandtotal']
            po_id.note=request.POST['customer_note']
            po_id.term = request.POST['tearms_conditions']
            u = User.objects.get(id = request.user.id)

            
            po_id.save()

            p_bill = Purchase_Order.objects.get(id=po_id.id)

            if len(request.FILES) != 0:
                p_bill.document=request.FILES['file'] 
                p_bill.save()
                print('save')
        else:
            po_id.vendor_name = request.POST.get('vendor')
            po_id.vendor_mail = request.POST.get('email_inp')
            po_id.vendor_gst_traet = request.POST.get('gst_trt_inp')
            po_id.vendor_gst_no = request.POST.get('gstin_inp')
            po_id.typ=typ
            
            po_id.Org_name = ''
            po_id.Org_address = ''
            po_id.Org_gst = ''
            po_id.Org_street=''
            po_id.Org_city=''
            po_id.Org_state=''
            po_id.Org_mail=''
            po_id.customer_name = request.POST.get('custom')
            po_id.customer_mail = request.POST.get('custMail')
            po_id.customer_address = request.POST.get('custAddress')
            po_id.customer_street = request.POST.get('custstreet')
            po_id.customer_city = request.POST.get('custcity')
            po_id.customer_state = request.POST.get('custstate')

            po_id.source_supply = request.POST.get('srcofsupply')
            po_id.Pur_no = request.POST['pur_ord']
            po_id.ref = request.POST['ref']
            po_id.payment_terms = request.POST['terms']
            po_id.Ord_date = request.POST.get('start_date')
            po_id.exp_date =  request.POST.get('end_date')
            po_id.sub_total =request.POST['subtotal']
            po_id.sgst=request.POST['sgst']
            po_id.cgst=request.POST['cgst']
            po_id.igst=request.POST['igst']
            po_id.tax_amount = request.POST['total_taxamount']
            po_id.shipping_charge= request.POST['shipping_charge']
            po_id.grand_total=request.POST['grandtotal']
            po_id.note=request.POST['customer_note']
            po_id.term = request.POST['tearms_conditions']
            
            u = User.objects.get(id = request.user.id)

            
            po_id.save()

            p_bill = Purchase_Order.objects.get(id=po_id.id)

        if request.FILES.get('file') is not None:
            po_id.file = request.FILES['file']
        else:
            po_id.file = "/static/images/default.jpg"
        po_id.save()
        item = request.POST.getlist("item[]")
        accounts = request.POST.getlist("account[]")
        quantity = request.POST.getlist("quantity[]")
        rate = request.POST.getlist("rate[]")
        tax = request.POST.getlist("tax[]")
        discount = request.POST.getlist("discount[]")
        amount = request.POST.getlist("amount[]")

        obj_dele = Purchase_Order_items.objects.filter(PO=p_bill.id)
        obj_dele.delete()

        if len(item) == len(accounts) == len(quantity) == len(rate) == len(discount) == len(tax) == len(amount):
            for i in range(len(item)):
                created = Purchase_Order_items.objects.create(
                    item=item[i],
                    account=accounts[i],
                    quantity=quantity[i],
                    rate=rate[i],
                    tax=tax[i],
                    discount=discount[i],
                    amount=amount[i],
                    user=u,
                    company=company,
                    PO=p_bill
                )

                print('Done')

            return redirect('purchase_bill_view',id)
    return redirect('purchaseView')


def change_status(request, id):
    chellan = DeliveryChellan.objects.get(id=id)
    chellan.status = 'Send'
    chellan.save()
    return redirect('delivery_challan_view', id=id)
    
def change_status_draft(request,pk):
    pur=Purchase_Order.objects.get(id=pk)
    pur.status='Draft'
    pur.save()
    return redirect('purchase_bill_view',pk)
    
def draft(request,id):
    company = company_details.objects.get(user = request.user)
    po_table=Purchase_Order.objects.all()
    po=Purchase_Order.objects.filter(status='Draft')
    company=company_details.objects.get(user_id=request.user.id)
    po_item=Purchase_Order.objects.get(id=id)
    context={
        'po':po,
        'company':company,
        'po_table':po_table,
        'po_item':po_item,
        'company':company,
    }
    return render(request,"purchase_bill_view.html",context)
    
    
def Approved(request,id):
    company = company_details.objects.get(user = request.user)
    po_table=Purchase_Order.objects.all()
    po=Purchase_Order.objects.filter(status='Approved')
    company=company_details.objects.get(user_id=request.user.id)
    po_item=Purchase_Order.objects.get(id=id)
    context={
        'po':po,
        'company':company,
        'po_table':po_table,
        'po_item':po_item,
        'company':company,
    }
    return render(request,"purchase_bill_view.html",context)
    
    
###################################################################### CHART OF ACCOUNT


def chartofaccount_home(request):
    company=company_details.objects.get(user=request.user)
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)
    # view=Chart_of_Account.objects.filter(user=user)
    view=Chart_of_Account.objects.all()
    return render(request,"chartofaccount_home.html", {'view':view,'company':company})

def create_account(request):
    if request.method=='POST':
        a=Chart_of_Account()
        cur_user = request.user
        user = User.objects.get(id=cur_user.id)
        a.user = user
        a.account_type = request.POST.get("account_type",None)
        a.account_name = request.POST.get("account_name",None)
        a.account_code = request.POST.get("account_code",None)
        a.description = request.POST.get("description",None)
        a.watchlist = request.POST.get("watchlist",None)
        a.status="active"
        if a.account_type=="Other Current Assets":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account",None)
            a.parent_account = request.POST.get("parent_account",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)

        if a.account_type=="Cash":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account22",None)
            a.parent_account = request.POST.get("parent_account22",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)

        if a.account_type=="Fixed Assets":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account33",None)
            a.parent_account = request.POST.get("parent_account33",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Stock":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account44",None)
            a.parent_account = request.POST.get("parent_account44",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Other Current Liability":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account55",None)
            a.parent_account = request.POST.get("parent_account55",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Long Term Liability":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account66",None)
            a.parent_account = request.POST.get("parent_account66",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Other Liability":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account77",None)
            a.parent_account = request.POST.get("parent_account77",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Equity":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account88",None)
            a.parent_account = request.POST.get("parent_account88",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Income":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account99",None)
            a.parent_account = request.POST.get("parent_account99",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Expense":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account100",None)
            a.parent_account = request.POST.get("parent_account100",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Cost Of Goods Sold":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account111",None)
            a.parent_account = request.POST.get("parent_account111",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Other Expense":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account222",None)
            a.parent_account = request.POST.get("parent_account222",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)

        a.save()
        return redirect('chartofaccount_home')
    return redirect('chartofaccount_home')



def chartofaccount_view(request,id):
    company=company_details.objects.get(user=request.user)
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)
    # view=Chart_of_Account.objects.filter(user=user)
    # ind=Chart_of_Account.objects.get(user=user,id=id)
    view=Chart_of_Account.objects.all()
    ind=Chart_of_Account.objects.get(id=id)

    doc=Chart_of_Account_Upload.objects.filter(account=ind)
    print(view)
    return render(request,"chartofaccount_view.html", {'view':view,'ind':ind,'doc':doc,'company':company})  

def create_account_view(request):
    if request.method=='POST':
        a=Chart_of_Account()
        cur_user = request.user
        user = User.objects.get(id=cur_user.id)
        a.user = user
        a.account_type = request.POST.get("account_type",None)
        a.account_name = request.POST.get("account_name",None)
        a.account_code = request.POST.get("account_code",None)
        a.description = request.POST.get("description",None)
        a.watchlist = request.POST.get("watchlist",None)
        a.status="active"
        if a.account_type=="Other Current Assets":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account",None)
            a.parent_account = request.POST.get("parent_account",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)

        if a.account_type=="Cash":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account22",None)
            a.parent_account = request.POST.get("parent_account22",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)

        if a.account_type=="Fixed Assets":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account33",None)
            a.parent_account = request.POST.get("parent_account33",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Stock":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account44",None)
            a.parent_account = request.POST.get("parent_account44",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Other Current Liability":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account55",None)
            a.parent_account = request.POST.get("parent_account55",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Long Term Liability":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account66",None)
            a.parent_account = request.POST.get("parent_account66",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Other Liability":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account77",None)
            a.parent_account = request.POST.get("parent_account77",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Equity":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account88",None)
            a.parent_account = request.POST.get("parent_account88",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Income":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account99",None)
            a.parent_account = request.POST.get("parent_account99",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Expense":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account100",None)
            a.parent_account = request.POST.get("parent_account100",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Cost Of Goods Sold":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account111",None)
            a.parent_account = request.POST.get("parent_account111",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Other Expense":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account222",None)
            a.parent_account = request.POST.get("parent_account222",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)

        a.save()
        return redirect('chartofaccount_home')
    return redirect('chartofaccount_home')



def edit_chart_of_account(request,pk):
    if request.method=='POST':
        a=Chart_of_Account.objects.get(id=pk)
        cur_user = request.user
        user = User.objects.get(id=cur_user.id)
        a.user = user
        a.account_type = request.POST.get("account_type1",None)
        a.account_name = request.POST.get("account_name1",None)
        a.account_code = request.POST.get("account_code",None)
        a.description = request.POST.get("description",None)
        a.watchlist = request.POST.get("watchlist",None)
        a.status=request.POST.get("radiobutton",None)

        if a.account_type=="Other Current Assets":        
            a.sub_account = request.POST.get("sub_account1",None)
            if a.sub_account=='on':
               a.parent_account = request.POST.get("parent_account1",None)
            else:
               a.parent_account = "null"
            a.bank_account_no = "null"
            a.currency = "null"

        if a.account_type=="Cash":        
            a.sub_account = request.POST.get("sub_account2",None)
            if a.sub_account=='on':
               a.parent_account = request.POST.get("parent_account2",None)
            else:
               a.parent_account = "null"
            a.bank_account_no = "null"
            a.currency = "null"

        if a.account_type=="Fixed Asset":        
            a.sub_account = request.POST.get("sub_account3",None)
            if a.sub_account=='on':
               a.parent_account = request.POST.get("parent_account3",None)
            else:
               a.parent_account = "null"           
            a.bank_account_no = "null"
            a.currency = "null"
        
        if a.account_type=="Stock":        
            a.sub_account = request.POST.get("sub_account4",None)
            if a.sub_account=='on':
               a.parent_account = request.POST.get("parent_account4",None)
            else:
               a.parent_account = "null"
            a.bank_account_no = "null"
            a.currency = "null"
        
        if a.account_type=="Other Current Liability":        
            a.sub_account = request.POST.get("sub_account5",None)
            if a.sub_account=='on':
               a.parent_account = request.POST.get("parent_account5",None)
            else:
               a.parent_account = "null"
            a.bank_account_no = "null"
            a.currency = "null"
        
        if a.account_type=="Long Term Liability":        
            a.sub_account = request.POST.get("sub_account6",None)
            if a.sub_account=='on':
               a.parent_account = request.POST.get("parent_account6",None)
            else:
               a.parent_account = "null"
            a.bank_account_no = "null"
            a.currency = "null"
        
        if a.account_type=="Other Liability":        
            a.sub_account = request.POST.get("sub_account7",None)
            if a.sub_account=='on':
               a.parent_account = request.POST.get("parent_account7",None)
            else:
               a.parent_account = "null"
            a.bank_account_no = "null"
            a.currency = "null"
        
        if a.account_type=="Equity":        
            a.sub_account = request.POST.get("sub_account8",None)
            if a.sub_account=='on':
               a.parent_account = request.POST.get("parent_account8",None)
            else:
               a.parent_account = "null"
            a.bank_account_no = "null"
            a.currency = "null"
        
        if a.account_type=="Income":        
            a.sub_account = request.POST.get("sub_account9",None)
            if a.sub_account=='on':
               a.parent_account = request.POST.get("parent_account9",None)
            else:
               a.parent_account = "null"
            a.bank_account_no = "null"
            a.currency = "null"

        if a.account_type=="Expense":        
            a.sub_account = request.POST.get("sub_account10",None)
            if a.sub_account=='on':
               a.parent_account = request.POST.get("parent_account10",None)
            else:
               a.parent_account = "null"
            a.bank_account_no = "null"
            a.currency = "null"

        if a.account_type=="Cost Of Goods Sold":        
            a.sub_account = request.POST.get("sub_account11",None)
            if a.sub_account=='on':
               a.parent_account = request.POST.get("parent_account11",None)
            else:
               a.parent_account = "null"
            a.bank_account_no = "null"
            a.currency = "null"
        
        if a.account_type=="Other Expense":        
            a.sub_account = request.POST.get("sub_account12",None)
            if a.sub_account=='on':
               a.parent_account = request.POST.get("parent_account12",None)
            else:
               a.parent_account = "null"
            a.bank_account_no = "null"
            a.currency = "null"
        
        if a.account_type=="Bank":        
            a.sub_account ="null"         
            a.parent_account = "null"
            a.bank_account_no = request.POST.get("account_number")
            a.currency = request.POST.get("parent_account22")

        if a.account_type=="Credit Card":        
            a.sub_account ="null"         
            a.parent_account = "null"
            a.bank_account_no = "null"
            a.currency = request.POST.get("parent_account32")
        
        a.save()
        return redirect('chartofaccount_home')
    return redirect('chartofaccount_home')



def upload_chart_of_account(request,pk):
    if request.method=='POST':
        cur_user = request.user
        user = User.objects.get(id=cur_user.id)
        account=Chart_of_Account.objects.get(id=pk)
        account_type=account.account_type
        account_name=account.account_name
        title=request.POST['file_title']
        description=request.POST['description']
        document=request.FILES.get('file')
        doc_upload=Chart_of_Account_Upload(user=user,account=account,account_type=account_type,account_name=account_name,title=title,description=description,document=document)
        doc_upload.save()
        return redirect('chartofaccount_home')
    return redirect('chartofaccount_home')

def download_chart_of_account(request,pk):
    document=get_object_or_404(Chart_of_Account_Upload,id=pk)
    response=HttpResponse(document.document,content_type='application/pdf')
    response['Content-Disposition']=f'attachment; filename="{document.document.name}"'
    return response

def proj(request):
    user_id=request.user.id
    udata=User.objects.get(id=user_id)
    data=customer.objects.filter(user=request.user)
    print("Hello")
    print(data)
    u=User.objects.all()
    tasks=task.objects.all()
    uz=usernamez.objects.all()
    uc=usercreate.objects.all()
    emp=Payroll.objects.filter()
    company=company_details.objects.get(user=request.user)
    return render(request,'proj.html',{'data':data,'u':u,'tasks':tasks,'uz':uz,'uc':uc,'company':company,'emp':emp})
    
def vproj(request):
   
    proj=project1.objects.filter(user=request.user)
    
    active=Project.objects.all()
    company=company_details.objects.get(user=request.user)
    for i in proj:
        tsk=task.objects.filter(proj=i)
        usr=usernamez.objects.filter(projn=i)
        
        for j in usr:
            emp=Payroll.objects.get(id=j.usernamez)
            i.uname=emp.first_name
        for j in tsk:
            i.status= j.billable
            i.rate= j.taskrph
    return render(request,'projlist.html',{'proj':proj,'active':active,'company':company})
    
    
def addproj(request):
    if request.method == 'POST':
        user_id=request.user.id
        user=User.objects.get(id=user_id)
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        c_name = request.POST.get('c_name')
        billing = request.POST.get('billing')
        rateperhour = request.POST.get('rateperhour')
        budget = request.POST.get('budget')
        start = request.POST.get('start')
        end = request.POST.get('end')
        #comment=request.POST.get('comment')

        taskname1 = request.POST.getlist('taskname[]')
        print(taskname1)
        taskdes1 = request.POST.getlist('taskdes[]')
        print(taskdes1)
        taskrph1 = request.POST.getlist('taskrph[]')
        print(taskrph1)
        billable1 = request.POST.getlist('billable[]')
        billdate = request.POST.getlist('billdate[]')
        print(billable1)
        user_select1 = request.POST.getlist('user_select[]')
        print(user_select1)
        email1 = request.POST.getlist('email[]')
        print(email1)

# Ensure all lists have the same length
        max_length = max(len(taskname1), len(taskdes1), len(taskrph1), len(billable1),len(billdate))
        taskname1.extend([''] * (max_length - len(taskname1)))
        taskdes1.extend([''] * (max_length - len(taskdes1)))
        taskrph1.extend([''] * (max_length - len(taskrph1)))
        billable1.extend(['Not Billed'] * (max_length - len(billable1)))
        billdate.extend([''] * (max_length - len(billdate)))
        

        cat = customer.objects.get(id=c_name)
        proj = project1(name=name, desc=desc, c_name=cat, billing=billing, rateperhour=rateperhour, budget=budget,user=user,start=start,end=end)
        proj.save()

        mapped_tasks = zip(taskname1, taskdes1, taskrph1, billable1,billdate)
        mapped_tasks = list(mapped_tasks)
        for ele in mapped_tasks:
            billable = 'Billed' if ele[3] == 'on' else 'Not Billed'
            if ele[3] == 'on' :
                tasks, created = task.objects.get_or_create(
                taskname=ele[0],
                taskdes=ele[1],
                taskrph=ele[2],
                proj=proj,
                billable=billable,
                billdate=ele[4],
                )
            else:
                tasks, created = task.objects.get_or_create(
                taskname=ele[0],
                taskdes=ele[1],
                taskrph=ele[2],
                proj=proj,
                billable=billable,
                )



        mapped_users = zip(user_select1, email1)
        mapped_users = list(mapped_users)
        for elez in mapped_users:
            usrz, varez = usernamez.objects.get_or_create(
                usernamez=elez[0], emailz=elez[1], projn=proj
            )
        
    return redirect('vproj')



def overview(request,id):
   
    proje=project1.objects.filter(user=request.user)
    for p in proje:
        tsk=task.objects.get(proj=p)
        p.billable = tsk.billable
    
   
    company=company_details.objects.get(user=request.user)
    project = get_object_or_404(project1, id=id)
    taskz=task.objects.get(proj=project)
    usern=usernamez.objects.filter(projn=project)
    attach=projectfiles.objects.filter(proj=project)
    print(attach)
    for i in usern:
        emp= Payroll.objects.get(id=i.usernamez)
        fname= emp.first_name
        lname = emp.last_name
        i.name = fname+ " "+lname
    cmt=projectcomment.objects.filter(proj=id)
     # Save the project object with the updated comment


    return render(request,'overview.html',{'usern':usern,'taskz':taskz,'proje':proje,'project':project,'company':company,'cmt':cmt,'attach':attach})

# def comment(request, product_id):
#     if request.method == 'POST':
#         user = request.user
#         product = AddItem.objects.get(id=product_id)
#         new_comment = request.POST.get('comment')
        
#         # Save the new comment to the database
#         Comments_item.objects.create(item=product, user=user, content=new_comment)

#     # Retrieve all the comments for the product
#     comments = Comments_item.objects.filter(item=product_id).values_list('content', flat=True)

#     response_data = {'comments': list(comments)}
#     return JsonResponse(response_data)

    
    
def commentdb(request, pk):
    if request.method == 'POST':     
        c_user_id=request.user.id  
        c_data=User.objects.get(id=c_user_id)
        c_comment=request.POST['comment']
        c_data3=Vendor_Credits.objects.all()
        c_data2=Vendor_Credits.objects.get(id=pk)
        comments= Credits_comments_table(user=c_data,vendor=c_data2,comment=c_comment)
        Credits_comments_table.objects.filter(vendor=pk).order_by('id')
        comments.save()
        
        context = {
            "allproduct": c_data3,
            "c_data2": c_data2,
            "comments": comments,
        }
        return redirect("show_credits",pk=pk)


 

def editproj(request,id):
    proj=project1.objects.get(id=id)
    proje=project1.objects.filter(user=request.user)
    data=customer.objects.filter(user=request.user)
    uc=usercreate.objects.all()
    usern=usernamez.objects.filter(projn=proj)
    taskz=task.objects.filter(proj=id)
    company=company_details.objects.get(user=request.user)
    for i in usern:
        emp= Payroll.objects.get(id=i.usernamez)
        fname= emp.first_name
        lname = emp.last_name
        i.name = fname+ " "+lname
    emp= Payroll.objects.all()
    return render(request,'editoverview.html',{'data':data,'proj':proj,'proje':proje,'uc':uc,'usern':usern,'taskz':taskz,'company':company,'emp':emp})
    
    
    
def editprojdb(request,id):
  if request.method == 'POST':
        proj=project1.objects.get(id=id)
        proj.name = request.POST.get('name')
        proj.desc = request.POST.get('desc')
        proj.c_name_id = request.POST.get('c_name')
        proj.billing = request.POST.get('billing')
        proj.rateperhour = request.POST.get('rateperhour')
        proj.budget = request.POST.get('budget')
        proj.start = request.POST.get('start')
        proj.end = request.POST.get('end')

        # taskname1 = request.POST.getlist('taskname[]')
        # print(taskname1)
        # taskdes1 = request.POST.getlist('taskdes[]')
        # print(taskdes1)
        # taskrph1 = request.POST.getlist('taskrph[]')
        # print(taskrph1)
        # billable1 = request.POST.getlist('billable[]')
        # billdate = request.POST.getlist('billdate[]')
        # print(billable1)
        # user_select1 = request.POST.getlist('user_select[]')
        # print(user_select1)
        # email1 = request.POST.getlist('email[]')
        # print(email1)
       
        
        proj.save()

        tsk = task.objects.get(proj=proj)
        tsk.taskname =request.POST.get('taskname')
        tsk.taskdes=request.POST.get('taskdes')
        tsk.taskrph=request.POST.get('taskrph')
        billable = request.POST.get("billable")
        if billable == 'on' :
            tsk.billable = 'Billed'
            tsk.billdate= request.POST.get('billdate')
        else:
            tsk.billable = 'Not Billed'
            tsk.billdate = None
        print("saved")
        tsk.save()

        usr = usernamez.objects.get(projn=proj)
        usr.usernamez =request.POST.get('user_select')
        usr.emailz =request.POST.get('email')
        print("user")
        usr.save()
        # Delete existing usernamez objects for the project
        # usernamez.objects.filter(projn=proj).delete()


        # objects_to_delete = task.objects.filter(proj_id=proj.id)
        # objects_to_delete.delete()

        
        # mapped_tasks = zip(taskname1, taskdes1, taskrph1, billable1,billdate)
        # mapped_tasks = list(mapped_tasks)
        # for ele in mapped_tasks:
        #     billable = 'Billed' if ele[3] == 'on' else 'Not Billed'
        #     if ele[3] == 'on' :
        #         tasks, created = task.objects.get_or_create(
        #         taskname=ele[0],
        #         taskdes=ele[1],
        #         taskrph=ele[2],
        #         proj=proj,
        #         billable=billable,
        #         billdate=ele[4],
        #         )
        #     else:
        #         tasks, created = task.objects.get_or_create(
        #         taskname=ele[0],
        #         taskdes=ele[1],
        #         taskrph=ele[2],
        #         proj=proj,
        #         billable=billable,
        #         )



        # mapped_users = zip(user_select1, email1)
        # mapped_users = list(mapped_users)
        # for elez in mapped_users:
        #     usrz, varez = usernamez.objects.get_or_create(
        #         usernamez=elez[0], emailz=elez[1], projn=proj
        #     )

        
        return redirect('overview',id)
  
def delproj(request,id):
    projd=project1.objects.get(id=id)
    projd.delete()
    return redirect('vproj')
    
    
def itemdata2(request):
    cur_user = request.user.id
    user = User.objects.get(id=cur_user)
    company = company_details.objects.get(user = user)
    print(company.state)
    id = request.GET.get('id')
    cust = request.GET.get('cust')
    
        
    item = AddItem.objects.get(Name=id)
    cus=Vendor_Credits.objects.get(company_name=cust)
    rate = item.s_price
    place=company.state
    gst = item.intrastate
    igst = item.interstate
    desc=item.s_desc
    print(place)
    mail=cus.vendor_email
    
    place_of_supply = Vendor_Credits.objects.get(company_name=cust).source_supply
    print(place_of_supply)
    return JsonResponse({"status":" not",'mail':mail,'desc':desc,'place':place,'rate':rate,'pos':place_of_supply,'gst':gst,'igst':igst})
    return redirect('/')
    
    
def createuser(request):
    if request.method == 'POST':
        usernamezz = request.POST.get('usernamezz')
        emailzz = request.POST.get('emailzz')
        
        # Check if a user with the same username already exists
        existing_user = usercreate.objects.filter(usernamezz=usernamezz).first()
        
        if existing_user:
            return JsonResponse({"status": "error", "message": "User already exists"})
        else:
            proj = usercreate(usernamezz=usernamezz, emailzz=emailzz)
            proj.save()
            return JsonResponse({"status": "success", "username": usernamezz, "email": emailzz})
    
    return render(request, "proj.html")
            
            
def toggle_status(request, project_id):
    project = get_object_or_404(project1, id=project_id)
    project.active = not project.active
    project.save()
    return JsonResponse({'status': project.active})
    
    
def itemdata_challan_save(request):
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)
    company = company_details.objects.get(user=user)
    print(company.state)
    id = request.GET.get('id')
    

    

    item = AddItem.objects.get(Name=id, user=user)
    name=item.Name
    rate = item.p_price
    place = company.state

    return JsonResponse({"status": " not", 'place': place, 'rate': rate})
    return redirect('/')


def apr(request):
    company = company_details.objects.get(user=request.user)
    pt=Purchase_Order.objects.filter(status='Approved')
    return render(request,'purchase_order.html',{'pt':pt,"company":company})


def drf(request):
    company = company_details.objects.get(user=request.user)
    pt=Purchase_Order.objects.filter(status='Draft')
    return render(request,'purchase_order.html',{'pt':pt,"company":company})


def add_customers(request):
    
    company = company_details.objects.get(user=request.user)
    sb=payment.objects.all()
    hi=Pricelist.objects.all()
    return render(request,'customer.html',{'hi':hi,'sb':sb,'company':company})
    
def profileasc(request):
    company = company_details.objects.get(user=request.user)
    cmp1 = company_details.objects.get(user=request.user)
    user = request.user
    rec_bill = Recurring_invoice.objects.filter(status='Save',user=user)
    context = {
        'recur': rec_bill,
        'cmp1': cmp1,
        "company":company,
    }
    return render(request, 'recurringonvoice.html', context)
    
    
def profiledesc(request):
    company = company_details.objects.get(user=request.user)
    cmp1 = company_details.objects.get(user = request.user)
    user = request.user
    rec_bill = Recurring_invoice.objects.filter(status='Draft',user=user)
    context = {
            'recur':rec_bill,
            "company":company,
            'cmp1': cmp1,

            }
    return render(request, 'recurringonvoice.html', context)
    
    
def payment_lists(request,payment_id):
    payment = get_object_or_404(payment_made, id=payment_id)
    vendor = vendor_table.objects.all()
    bank = banking.objects.all()
    option = method.objects.all()
    company=company_details.objects.get(user=request.user)
    return render(request,'payment_list.html',{'payment':payment,'vendor':vendor,'bank':bank,'option':option,'company':company})
    

def payment_template(request,payment_id):
    payment = get_object_or_404(payment_made,id=payment_id)
    vendor = vendor_table.objects.all()
    bank = banking.objects.all()
    option = method.objects.all()
    company=company_details.objects.get(user=request.user)    
    context = {'payment':payment,'vendor':vendor,'bank':bank,'option':option,'company':company}
    return render(request,'payment_template.html',context)
    
def delete_payment(request, payment_id):
   payment = payment_made.objects.filter(id=payment_id)
   payment.delete()
   return redirect('paymentmethod')
   
   
def payment_delete_details(request):
    payment_id = request.GET.get('payment_id')
    payment = get_object_or_404(payment_made,id=payment_id)
    payment.delete()
    return redirect('paymentmethod')
    
def payment_details(request, payment_id):
    payment = get_object_or_404(payment_made, id=payment_id)
    vendor = vendor_table.objects.all()  # Fetch all vendor data
    bank = banking.objects.all()
    option = method.objects.all()
    company = company_details.objects.get(user=request.user)
    return render(request, 'payment_details_edit.html', {'payment': payment ,'vendor': vendor,'bank':bank,'option':option,'company':company})
    
    
def add_option(request):
    if request.method == "POST":
        option_name = request.POST.get('option')

        # Save the new option to the database
        new_option = method(option=option_name)
        new_option.save()
        print(option_name)

        response_data = {
            "message": "success",
            "option": option_name,
        }

        return JsonResponse(response_data)
    
    
def options(request):
    
    if not method.objects.filter(option='BOX').exists():
            method(option='BOX').save()
    if not method.objects.filter(option='UNIT').exists():
            method(option='UNIT').save()
    if not method.objects.filter(option='LITRE').exists():
            method(option='LITRE').save()
    return render(request,'payment_method_add.html')
    
    
def add_options(request):
    if request.method=='POST':
        option_name=request.POST['option']
        method(option=option_name).save()
        return redirect('payment_edit')
    return render(request,"payment_details_edit.html")
    
    
def marks(request):
    
    if not method.objects.filter(unit='Online').exists():
        method_instance = method(unit='Online')
        method_instance.save()
        
    if not method.objects.filter(unit='Cheque').exists():
        method_instance = method(unit='Cheque')
        method_instance.save()
        
    if not method.objects.filter(unit='UPI').exists():
        method_instance = method(unit='UPI')
        method_instance.save()
    return render(request,'sucess.html')
    
    
def payment_banking(request):
    company = company_details.objects.get(user = request.user)
    print(company.company_name)
    banks = bank.objects.filter(user=request.user, acc_type="bank")
    return render(request,'payment_banking_add.html',{"bank":banks,"company":company})    
    
def option_dropdown(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = method.objects.all()
    for option in option_objects:
        options[option.id] = option.option
    print(options)    

    return JsonResponse(options)
    
def banking_dropdown(request):

    user = User.objects.get(id=request.user.id)

    banks = {}
    bank_objects = banking.objects.all()
    for bank in bank_objects:
        banks[bank.id] = bank.bnk_name

    return JsonResponse(banks)


# def banking_dropdown(request):
#     user = User.objects.get(id=request.user.id)

#     options = {}
#     option_objects = banking.objects.filter(user = user)
#     for option in option_objects:
        
#         options[option.id] = [ option.bnk_name, option.id]
#     return JsonResponse(options)


def added_banking(request):
  
    if request.method == "POST":
        main_name = request.POST.get('main_name')
        alias = request.POST.get('main_alias')
        acunt_type = request.POST.get('main_type')
        ac_holder = request.POST.get('ac_holder')
        ac_number = request.POST.get('ac_number')
        ifsc = request.POST.get('ifsc')
        sw_code = request.POST.get('sw_code')
        bnk_name = request.POST.get('bnk_name')
        br_name = request.POST.get('br_name')
        chqrng = request.POST.get('alter_chq')
        chqprnt = request.POST.get('en_chq')
        chqprnty = request.POST.get('chq_prnt')
        name = request.POST.get('name')
        address = request.POST.get('address')
        country = request.POST.get('country')
        state = request.POST.get('state')
        pin = request.POST.get('pin')
        bnk_det = request.POST.get('bnk_det')
        pan = request.POST.get('pan')
        regtype = request.POST.get('register_type')
        gstin = request.POST.get('gstin')
        gst_det = request.POST.get('gst_det')
        balance = request.POST.get('balance')

        
        u = User.objects.get(id = request.user.id)

       
        data = banking(
            name=main_name,
            alias=alias,
            acc_type=acunt_type,
            ac_holder=ac_holder,
            ac_no=ac_number,
            ifsc=ifsc,
            swift_code=sw_code,
            bnk_name=bnk_name,
            bnk_branch=br_name,
            chq_book=chqrng,
            chq_print=chqprnt,
            chq_config=chqprnty,
            mail_name=name,
            mail_addr=address,
            mail_country=country,
            mail_state=state,
            mail_pin=pin,
            bd_bnk_det=bnk_det,
            bd_pan_no=pan,
            bd_reg_typ=regtype,
            bd_gst_no=gstin,
            bd_gst_det=gst_det,
            opening_bal=balance,
            user=u
        )
        data.save()
        response_data = {
            "message": "success",
            "bnk_nm":bnk_name,
            
        }

        return JsonResponse(response_data)
    
    
def payment_banking_edit(request):
    company = company_details.objects.get(user = request.user)
    print(company.company_name)
    banks = bank.objects.filter(user=request.user, acc_type="bank")
    return render(request,'payment_banking_edit.html',{"bank":banks,"company":company})
    
    
def added_banking_edit(request):
    if request.method == "POST":
        a=banking()
        a.name = request.POST.get('main_name',None)
        a.alias = request.POST.get('main_alias',None)
        a.acc_type = request.POST.get('main_type',None)
        a.ac_holder = request.POST.get('ac_holder',None)
        a.ac_no = request.POST.get('ac_number',None)
        a.ifsc = request.POST.get('ifsc',None)
        a.swift_code = request.POST.get('sw_code',None)
        a.bnk_name = request.POST.get('bnk_nm',None)
        a.bnk_branch = request.POST.get('br_name',None)
        a.chq_book = request.POST.get('alter_chq',None)
        a.chq_print = request.POST.get('en_chq',None)
        a.chq_config = request.POST.get('chq_prnt',None)
        a.mail_name = request.POST.get('name',None)
        a.mail_addr = request.POST.get('address',None)
        a.mail_country = request.POST.get('country',None)
        a.mail_state = request.POST.get('state',None)
        a.mail_pin = request.POST.get('pin',None)
        a.bd_bnk_det = request.POST.get('bnk_det',None)
        a.bd_pan_no = request.POST.get('pan',None)
        a.bd_reg_typ = request.POST.get('register_type',None)
        a.bd_gst_no = request.POST.get('gstin',None)
        a.bd_gst_det = request.POST.get('gst_det',None)
        a.user=request.user
        a.opening_bal = request.POST.get('balance',None)
        a.save()
        return redirect("payment_edit") 
    
    
@login_required(login_url='login')
def delete_comment(request, product_id, comment_id):
    try:
        comment = Comments_item.objects.get(id=comment_id, item_id=product_id, user=request.user)
        comment.delete()
    except Comments_item.DoesNotExist:
        pass

    return redirect('detail', product_id)
    
    
def save_bank_payment(request):
    if request.method == "POST":
        a=bank()
        a.acc_type = request.POST.get('type',None)
        a.bank_name = request.POST.get('bank',None)
        a.user = request.user
        a.save()
        return redirect('paymentadd_method')
        
        
def payroll_create(request):
    company=company_details.objects.get(user=request.user)
    return render(request,'payroll_create.html',{'company':company})
    
    
def editpayroll(request,id):
    p=Payroll.objects.get(id=id)
    
    if request.method=='POST':
        p.title=request.POST['title']
        p.first_name=request.POST['fname']
        p.last_name=request.POST['lname']
        p.alias=request.POST['alias']
        p.joindate=request.POST['joindate']
        p.salary=request.POST['salary']   
        # p.image=request.FILES.get('file')
        new=request.FILES.get('file')
        old= p.image
        if old!=None and new==None:
            p.image=old
        else:
            p.image=new
        p.emp_number = request.POST['empnum']
        p.designation = request.POST['designation']
        p.location=request.POST['location']
        p.gender=request.POST['gender']
        p.dob=request.POST['dob']
        p.blood=request.POST['blood']
        p.parent=request.POST['fm_name']
        p.spouse_name=request.POST['s_name']  
        add1=request.POST['address']
        add2=request.POST['address2']
        address=add1+" "+add2
        padd1=request.POST['paddress'] 
        padd2=request.POST['paddress2'] 
        paddress= padd1+" "+padd2      
        p.address=address 
        p.permanent_address=paddress 
        p.Phone=request.POST['phone']
        ephone=request.POST['ephone']
        if ephone =="":
            p.emergency_phone=None
        else:
            p.emergency_phone=request.POST['ephone']
        p.email=request.POST['email']
        p.ITN=request.POST['itn']
        p.Aadhar=request.POST['an']
        p.UAN=request.POST['uan']
        p.PFN=request.POST['pfn']
        p.PRAN=request.POST['pran']
        istds=request.POST['istds']
        if istds == '1':
            p.isTDS=request.POST['pora']
            p.TDS=request.POST['tds']
        else:
            p.isTDS='No'
            p.TDS=0
        p.save()
        
        if Bankdetails.objects.filter(payroll=p).exists():
            b=Bankdetails.objects.get(payroll=p)
            b.acc_no=request.POST['acc_no']  
            b.IFSC=request.POST['ifsc']
            b.bank_name=request.POST['b_name']
            b.branch=request.POST['branch']
            b.transaction_type=request.POST['ttype']
            b.save()
        else:
            bank=request.POST['bank']
            if(bank == '1'):
                accno=request.POST['acc_no']       
                ifsc=request.POST['ifsc']       
                bname=request.POST['b_name']       
                branch=request.POST['branch']
                ttype=request.POST['ttype']
                b=Bankdetails(payroll=p,acc_no=accno,IFSC=ifsc,bank_name=bname,branch=branch,transaction_type=ttype)
                b.save()
        
    else:
        return redirect('payroll_view',id=id)
    return redirect('payroll_view',id=id)

def createpayroll(request):
    if request.method=='POST':
        title=request.POST['title']
        fname=request.POST['fname']
        lname=request.POST['lname']
        alias=request.POST['alias']
        joindate=request.POST['joindate']
        saltype=request.POST['saltype']
        if (saltype == 'Fixed'):
            salary=request.POST['fsalary']
        else:
            salary=request.POST['vsalary']
        image=request.FILES.get('file')
        if image == None:
            image="image/img.png"
        empnum=request.POST['empnum']
        designation = request.POST['designation']
        location=request.POST['location']
        gender=request.POST['gender']
        dob=request.POST['dob']
        blood=request.POST['blood']
        fmname=request.POST['fm_name']
        sname=request.POST['s_name']        
        add1=request.POST['address']
        add2=request.POST['address2']
        address=add1+" "+add2
        padd1=request.POST['paddress'] 
        padd2=request.POST['paddress2'] 
        paddress= padd1+padd2
        phone=request.POST['phone']
        ephn=request.POST['ephone']
        if ephn=="":
            ephone=None
        else:
            ephone=request.POST['ephone']
        email=request.POST['email']
        isdts=request.POST['tds']
        if isdts == '1':
            istdsval=request.POST['pora']
            if istdsval == 'Percentage':
                tds=request.POST['pcnt']
            elif istdsval == 'Amount':
                tds=request.POST['amnt']
        else:
            istdsval='No'
            tds = 0
        itn=request.POST['itn']
        an=request.POST['an']        
        uan=request.POST['uan'] 
        pfn=request.POST['pfn']
        pran=request.POST['pran']
        payroll= Payroll(title=title,first_name=fname,last_name=lname,alias=alias,image=image,joindate=joindate,salary_type=saltype,salary=salary,emp_number=empnum,designation=designation,location=location,
                         gender=gender,dob=dob,blood=blood,parent=fmname,spouse_name=sname,address=address,permanent_address=paddress ,Phone=phone,emergency_phone=ephone,
                         email=email,ITN=itn,Aadhar=an,UAN=uan,PFN=pfn,PRAN=pran,isTDS=istdsval,TDS=tds)
        payroll.save()

        bank=request.POST['bank']
        if(bank == '1'):
            accno=request.POST['acc_no']       
            ifsc=request.POST['ifsc']       
            bname=request.POST['b_name']       
            branch=request.POST['branch']
            ttype=request.POST['ttype']
            b=Bankdetails(payroll=payroll,acc_no=accno,IFSC=ifsc,bank_name=bname,branch=branch,transaction_type=ttype)
            b.save()
        attach=request.FILES.get('attach')       
        if(attach):
            att=Payrollfiles(attachment=attach,payroll=payroll)
        # messages.success(request,'Saved succefully !')
        print(bank)
        return redirect('payroll_list')
    else:
        return redirect('payroll_create')
        
        
def payroll_list(request):
    company=company_details.objects.get(user=request.user)
    p=Payroll.objects.all()
    return render(request,'payroll_list.html',{'pay':p,'company':company})
    
    
def payroll_delete(request,pid):
    p=Payroll.objects.get(id=pid)
    p.delete()
    return redirect('payroll_list')
    
    
def payroll_view(request,id):
    payroll=Payroll.objects.all()
    p=Payroll.objects.get(id=id)
    com=Commentmodel.objects.filter(payroll=p)
    b=Bankdetails.objects.filter(payroll=p)
    attach=Payrollfiles.objects.filter(payroll=p)
    company=company_details.objects.get(user=request.user)
    print(p)
    print(attach)
    return render(request,'payroll_view.html',{'pay':payroll,'p':p,'b':b,'com':com,'attach':attach,'company':company})

def payroll_active(request,id):
    p=Payroll.objects.get(id=id)
    if p.status == 'Active':
        p.status = 'Inactive'
    else:
        p.status = 'Active'
    p.save()
    return redirect('payroll_view',id=id)

def payroll_file(request,id):
    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]
        pay=Payroll.objects.get(id=id)
        p=Payrollfiles(attachment=uploaded_file,payroll=pay)
        p.save()
        print("hellooooooooooooooooo")
        return redirect('payroll_view',id)
    else:
        return redirect('payroll_view',id)
    # 

def img_download(request,id):
    p=Payroll.objects.get(id=id)
    image_file = p.image

    response = FileResponse(image_file)
    response['Content-Disposition'] = f'attachment; filename="{image_file.name}"'
    # return redirect('payroll_view',id=id)
    return response
    
    
def file_download(request,aid):
    att= Payrollfiles.objects.get(id=aid)
    file = att.attachment
    response = FileResponse(file)
    response['Content-Disposition'] = f'attachment; filename="{file.name}"'
    return response
    
    
def payroll_edit(request,pid):  
    p=Payroll.objects.get(id=pid)
    company=company_details.objects.get(user=request.user)
    address=p.address
    paddress=p.permanent_address
    add1, add2 = split_paragraph(address)
    padd1, padd2 = split_paragraph(paddress)
    b=Bankdetails.objects.filter(payroll=p)
    print(b)
    context = {
                'add1' : add1,
                'add2' : add2, 'padd1' : padd1, 'padd2': padd2,
                'pay':p,'b':b,'company':company
            }
    return render(request,'payroll_edit.html',context)

def add_payrollcomment(request,pid):
    p=Payroll.objects.get(id=pid)
    if request.method== 'POST':
        comment=request.POST['comments']
        c= Commentmodel(comment=comment,payroll=p)
        c.save()
    return redirect('payroll_view',id=pid)
    
    
def delete_payrollcomment(request,cid):
    
    try:
        comment = Commentmodel.objects.get(id=cid)
        p=comment.payroll
        print("================================")
        comment.delete()
        return redirect('payroll_view', p.id)
    except:
        return redirect('payroll_view', p.id)
        
        
def projcomment(request,id):
    proj = project1.objects.get(id=id)
    proje=project1.objects.filter(user=request.user)
    return render(request,'comment.html',{'proj':proj,'proje':proje})
    
    
def projcommentdb(request, id):
    projc = get_object_or_404(project1, id=id)

    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        if comment_text:
            if projc.comment:
                projc.comment += "\n" + comment_text  # Add new comment to existing comments
            else:
                projc.comment = comment_text  # If no comments exist, set it as the first comment
            projc.save()

    return redirect('overview', id=id)
    
    
    
def entr_custmrA1(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            type=request.POST.get('type')
            txtFullName=request.POST['txtFullName']
            cpname=request.POST['cpname']
           
            email=request.POST.get('email')
            wphone=request.POST.get('wphone')
            mobile=request.POST.get('mobile')
            skname=request.POST.get('skname')
            desg=request.POST.get('desg')      
            dept=request.POST.get('dept')
            wbsite=request.POST.get('wbsite')

            gstt=request.POST.get('v_gsttype')
            gstin=request.POST.get('v_gstin')
            posply=request.POST.get('posply')
            tax1=request.POST.get('tax1')
            crncy=request.POST.get('crncy')
            obal=request.POST.get('obal')

            select=request.POST.get('pterms')
            pterms=payment_terms.objects.get(id=select)
            pterms=request.POST.get('pterms')

            plst=request.POST.get('plst')
            plang=request.POST.get('plang')
            fbk=request.POST.get('fbk')
            twtr=request.POST.get('twtr')
        
            atn=request.POST.get('atn')
            ctry=request.POST.get('ctry')
            
            addrs=request.POST.get('addrs')
            addrs1=request.POST.get('addrs1')
            bct=request.POST.get('bct')
            bst=request.POST.get('bst')
            bzip=request.POST.get('bzip')
            bpon=request.POST.get('bpon')
            bfx=request.POST.get('bfx')

            sal=request.POST.get('sal')
            ftname=request.POST.get('ftname')
            ltname=request.POST.get('ltname')
            mail=request.POST.get('mail')
            bworkpn=request.POST.get('bworkpn')
            bmobile=request.POST.get('bmobile')

            bskype=request.POST.get('bskype')
            bdesg=request.POST.get('bdesg')
            bdept=request.POST.get('bdept')
            u = User.objects.get(id = request.user.id)

          
            ctmr=customer(customerName=txtFullName,
                          customerType=type,
                        companyName=cpname,
                        customerEmail=email,
                        customerWorkPhone=wphone,
                         customerMobile=mobile,skype=skname,
                         designation=desg,department=dept,
                           website=wbsite
                           ,GSTTreatment=gstt,
                           GSTIN=gstin,
                           placeofsupply=posply, Taxpreference=tax1,
                             currency=crncy,OpeningBalance=obal,
                             PaymentTerms=pterms,
                                PriceList=plst,PortalLanguage=plang,
                                Facebook=fbk,
                                Twitter=twtr,
                                 Attention=atn,country=ctry,Address1=addrs,Address2=addrs1,
                                  city=bct,state=bst,zipcode=bzip,phone1=bpon,
                                   fax=bfx,CPsalutation=sal,Firstname=ftname,
                                    Lastname=ltname,CPemail=mail,CPphone=bworkpn,
                                    CPmobile= bmobile,CPskype=bskype,CPdesignation=bdesg,
                                     CPdepartment=bdept,user=u )
            ctmr.save()  
            
            return redirect("proj")
        return render(request,'customerzz.html')
        
        
def payment_termA1(request):
    if request.method=='POST':
        term=request.POST.get('term')
        day=request.POST.get('day')
        ptr=payment_terms(Terms=term,Days=day)
        ptr.save()
        return HttpResponse( {"message":"success"})
        
        
def add_customers1(request):
    sb=payment_terms.objects.all()
    hi=Pricelist.objects.all()
    return render(request,'customerzz.html',{'sb':sb,'hi':hi})
    
    
#####################expense##############################################################
    
def expensepage(request):
    company = company_details.objects.get(user = request.user)
    expenses = ExpenseE.objects.filter(user=request.user)
    context = {
        'expenses': expenses,
        'company':company
       }
    return render(request,'expense.html',context)

def save_expense(request):
    company = company_details.objects.get(user = request.user)
    if request.user.is_authenticated:
        if request.method == 'POST':
           
            date = request.POST.get('date')
            
           
            expense_account = request.POST.get('expense_account')
            amount = request.POST.get('amount')
            currency = request.POST.get('currency')
            expense_type = request.POST.get('expense_type')
            paid = request.POST.get('paid')

            notes = request.POST.get('notes')
            if request.POST.get('expense_type') == 'goods':
                hsn_code = request.POST.get('sac')
                sac = request.POST.get('hsn_code')
            else:
                hsn_code = request.POST.get('hsn_code')
                sac = request.POST.get('sac')
    
            gst_treatment = request.POST.get('gst_treatment')
            gstin=request.POST.get('gstin',None)
            destination_of_supply = request.POST.get('destination_of_supply')
            reverse_charge = request.POST.get('reverse_charge')
            tax = request.POST.get('tax')
            invoice = request.POST.get('invoice')
            c = request.POST.get('customer')
            customere = customer.objects.get(id=c)
            v= request.POST.get('vendor')
            vendor=vendor_table.objects.get(id=v)

          
            taxamt = request.POST.get('taxamt',False)
           
            image = request.FILES.get('image')


            expense = ExpenseE.objects.create(
                user=request.user,
                date=date,
                image=image,
                expense_account=expense_account,
                amount=amount,
                currency=currency,
                taxamt=taxamt,
                sac=sac,
                expense_type=expense_type,
                paid=paid,
                notes=notes,
                hsn_code=hsn_code,
                gst_treatment=gst_treatment,
                gstin=gstin,
                destination_of_supply=destination_of_supply,
                reverse_charge=reverse_charge,
                tax=tax,
                invoice=invoice,
                customer_name= customere,
                vendor=vendor,
                company=company
            )

            expense.save()

            return redirect('expensepage')
        else:
          
            c = customer.objects.filter(user=request.user)
            v = vendor_table.objects.filter(user=request.user)
            accounts = AccountE.objects.filter(user=request.user)
            account_types = set(AccountE.objects.filter(user=request.user).values_list('account_type', flat=True))
            p = payment_termsE.objects.filter(user=request.user)
            cp= company_details.objects.get(user = request.user)
            return render(request, 'addexpense.html', {'company':cp,'vendor':v,'customer': c,'payments':p,'accounts': accounts, 'account_types': account_types,
            })
   
def upload_documents(request, expense_id):
    if request.method == 'POST':
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        expense = ExpenseE.objects.get(id=expense_id)
        attachment_file = request.FILES.get('attachment')

        doc_data = AttachE.objects.create(user=user, expense=expense, attachment=attachment_file)
        doc_data.save()

        return redirect("expense_details", pk=expense.pk)
   
def upload_documents(request, expense_id):
    if request.method == 'POST':
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        expense = ExpenseE.objects.get(id=expense_id)
        attachment_file = request.FILES.get('attachment')

        doc_data = AttachE.objects.create(user=user, expense=expense, attachment=attachment_file)
        doc_data.save()

        return redirect("expense_details", pk=expense.pk)

def add_accountE(request):
    accounts = AccountE.objects.filter(user=request.user)
    account_types = set(AccountE.objects.filter(user=request.user).values_list('account_type', flat=True))
    if request.method=='POST':
        a=AccountE()
        cur_user = request.user
        user = User.objects.get(id=cur_user.id)
        a.user = user
        a.account_type = request.POST.get("account_type",None)
        a.account_name = request.POST.get("account_name",None)
        a.account_code = request.POST.get("account_code",None)
        a.description = request.POST.get("description",None)
        a.watchlist = request.POST.get("watchlist",None)
        a.status="active"
        if a.account_type=="Other Current Assets":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account",None)
            a.parent_account = request.POST.get("parent_account",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)

        if a.account_type=="Cash":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account22",None)
            a.parent_account = request.POST.get("parent_account22",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)

        if a.account_type=="Fixed Assets":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account33",None)
            a.parent_account = request.POST.get("parent_account33",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Stock":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account44",None)
            a.parent_account = request.POST.get("parent_account44",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Other Current Liability":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account55",None)
            a.parent_account = request.POST.get("parent_account55",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Long Term Liability":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account66",None)
            a.parent_account = request.POST.get("parent_account66",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Other Liability":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account77",None)
            a.parent_account = request.POST.get("parent_account77",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Equity":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account88",None)
            a.parent_account = request.POST.get("parent_account88",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Income":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account99",None)
            a.parent_account = request.POST.get("parent_account99",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Expense":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account100",None)
            a.parent_account = request.POST.get("parent_account100",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Cost Of Goods Sold":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account111",None)
            a.parent_account = request.POST.get("parent_account111",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
        
        if a.account_type=="Other Expense":
            a.credit_no = request.POST.get("credit_number",None)
            a.sub_account = request.POST.get("sub_account222",None)
            a.parent_account = request.POST.get("parent_account222",None)
            a.bank_account_no = request.POST.get("account_number",None)
            a.currency = request.POST.get("currency",None)
       
        a.save()
       
        
    return HttpResponse('Account saved successfully')
    return render(request, 'addexpense.html', {
        'accounts': accounts,
        'account_types': account_types,
    })

def account_dropdownE(request):
    user = User.objects.get(id=request.user.id)

    options = {}
    account_objects = AccountE.objects.filter(user=user)
    for account in account_objects:
        
        options[account.id] = {
            'account_name': account.account_name,
            'account_type': account.account_type
        }

    return JsonResponse(options)  
       



def add_custmr(request):
    
    # company = ExpenseE.objects.get(user = request.user)
    if request.method=='POST':

        # title=request.POST.get('title')
        # first_name=request.POST.get('firstname')
        # last_name=request.POST.get('lastname')
        # comp=request.POST.get('company_name')
        cust_type = request.POST.get('customer_type')
        name = request.POST.get('display_name')
        comp_name = request.POST.get('company_name')
        email=request.POST.get('email')
        website=request.POST.get('website')
        w_mobile=request.POST.get('work_mobile')
        p_mobile=request.POST.get('pers_mobile')
        fb = request.POST.get('facebook')
        twitter = request.POST.get('twitter')
        skype = request.POST.get('skype')
        desg = request.POST.get('desg')
        dpt = request.POST.get('dpt')
        gsttype=request.POST.get('gsttype')
        # gstin=request.POST.get('gstin')
        # panno=request.POST.get('panno')
        supply=request.POST.get('placeofsupply')
        tax = request.POST.get('tax_preference')
        currency=request.POST.get('currency')
        balance=request.POST.get('openingbalance')
        payment=request.POST.get('paymentterms')
        street1=request.POST.get('street1')
        street2=request.POST.get('street2')
        city=request.POST.get('city')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
        country=request.POST.get('country')
        fax=request.POST.get('fax')
        phone=request.POST.get('phone')
        # shipstreet1=request.POST.get('shipstreet1')
        # shipstreet2=request.POST.get('shipstreet2')
        # shipcity=request.POST.get('shipcity')
        # shipstate=request.POST.get('shipstate')
        # shippincode=request.POST.get('shippincode')
        # shipcountry=request.POST.get('shipcountry')
        # shipfax=request.POST.get('shipfax')
        # shipphone=request.POST.get('shipphone')

        u = User.objects.get(id = request.user.id)
        if balance == '':
           balance = None

        cust = customer(customerName = name,customerType = cust_type, companyName= comp_name, GSTTreatment=gsttype, 
                        customerWorkPhone = w_mobile,customerMobile = p_mobile, customerEmail=email,skype = skype,Facebook = fb, 
                        Twitter = twitter,placeofsupply=supply,Taxpreference = tax,currency=currency, website=website, 
                        designation = desg, department = dpt,OpeningBalance=balance,Address1=street1,Address2=street2, city=city, 
                        state=state, PaymentTerms=payment,zipcode=pincode,country=country, fax = fax, phone1 = phone,user = u)
        cust.save()

        return HttpResponse({"message": "success"})
        
        
def customer_dropdownE(request):
    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = customer.objects.filter(user=user)
    for option in option_objects:
        display_name = option.customerName
        options[option.id] = [display_name, f"{display_name}"]
        
    return JsonResponse(options)

        
# def customer_dropdownE(request):
#     user = User.objects.get(id=request.user.id)

#     options = {}
#     option_objects = addcustomerE.objects.filter(user = user)
#     for option in option_objects:
#         options[option.id] = [option.customer_name]


#     return JsonResponse(options)        
        
        
def edit_expensee(request,expense_id):
    company = company_details.objects.get(user = request.user)
    if request.user.is_authenticated:
        expense = ExpenseE.objects.get(id=expense_id)

        if request.method == 'POST':
            date = request.POST.get('date')
            expense_account = request.POST.get('expense_account')
            amount = request.POST.get('amount')
            currency = request.POST.get('currency')
            expense_type = request.POST.get('expense_type')
            paid = request.POST.get('paid')
            notes = request.POST.get('notes')
            if request.POST.get('expense_type') == 'goods':
                hsn_code = request.POST.get('sac')
                sac = request.POST.get('hsn_code')
            else:
                hsn_code = request.POST.get('hsn_code')
                sac = request.POST.get('sac')
            gst_treatment = request.POST.get('gst_treatment')
            destination_of_supply = request.POST.get('destination_of_supply')
           
            tax = request.POST.get('tax')
            invoice = request.POST.get('invoice')
            c = request.POST.get('customer')
            customere = customer.objects.get(id=c)
            v = request.POST.get('vendor')
            vendor = vendor_table.objects.get(id=v)
            reporting_tags = request.POST.get('reporting_tags')
            taxamt = request.POST.get('taxamt', False)
           
            reverse_charge = request.POST.get('reverse_charge')
            if reverse_charge == 'True':
                expense.reverse_charge = True
            else:
                expense.reverse_charge = False

            gstin = request.POST.get('gstin', None)
            if gstin is not None:
                expense.gstin = gstin
            else:
                expense.gstin = None

            if request.FILES.get('image'):
                image = request.FILES['image']
            elif expense.image:
                image = expense.image
            else:
                image = None

            expense.date = date
            expense.expense_account = expense_account
            expense.amount = amount
            expense.currency = currency
            expense.taxamt = taxamt
            expense.sac = sac
            expense.expense_type = expense_type
            expense.paid = paid
            expense.notes = notes
            expense.hsn_code = hsn_code
            expense.gst_treatment = gst_treatment
            expense.gstin=gstin
            expense.destination_of_supply = destination_of_supply
            expense.reverse_charge = reverse_charge
            expense.tax = tax
            expense.invoice = invoice
            expense.customer_name = customere
            expense.reporting_tags = reporting_tags
            expense.vendor = vendor
            expense.image=image
            
            expense.company=company
            expense.save()

            return redirect('expense_details',pk=expense.pk)
        else:
           
            c = customer.objects.filter(user=request.user)
            v = vendor_table.objects.filter(user=request.user)
            accounts = AccountE.objects.filter(user=request.user)
            account_types = set(AccountE.objects.filter(user=request.user).values_list('account_type', flat=True))
            p = payment_termsE.objects.filter(user=request.user)
            cp= company_details.objects.get(user = request.user)
            return render(request, 'editexpense.html', {'company':cp ,'vendor': v, 'customer': c, 'accounts': accounts, 'account_types': account_types, 'expense': expense})

def delet(request,id):
    items=ExpenseE.objects.filter(id=id)
    items.delete()
    
    return redirect('expensepage')



    
def add_vendore(request):
    
    if request.method=='POST':

        title=request.POST.get('title')
        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')
        comp=request.POST.get('company_name')
        dispn = request.POST.get('display_name')
        email=request.POST.get('email',None)
        website=request.POST.get('website',None)
        w_mobile=request.POST.get('work_mobile',None)
        p_mobile=request.POST.get('pers_mobile',None)
        skype = request.POST.get('skype',None)
        desg = request.POST.get('desg',None)
        dpt = request.POST.get('dpt',None)
        gsttype=request.POST.get('gsttype',None)
        gstin=request.POST.get('gstin',None)
        panno=request.POST.get('panno',None)
        supply=request.POST.get('sourceofsupply',None)
        currency=request.POST.get('currency',None)
        balance=request.POST.get('openingbalance',None)
        payment=request.POST.get('paymentterms',None)
        street=request.POST.get('street',None)
        city=request.POST.get('city',None)
        state=request.POST.get('state',None)
        pincode=request.POST.get('pincode',None)
        country=request.POST.get('country',None)
        fax=request.POST.get('fax',None)
        phone=request.POST.get('phone',None)
        shipstreet=request.POST.get('shipstreet',None)
        shipcity=request.POST.get('shipcity',None)
        shipstate=request.POST.get('shipstate',None)
        shippincode=request.POST.get('shippincode',None)
        shipcountry=request.POST.get('shipcountry',None)
        shipfax=request.POST.get('shipfax',None)
        shipphone=request.POST.get('shipphone',None)
        
        u = User.objects.get(id = request.user.id)
        vndr = vendor_table(salutation=title, first_name=first_name, last_name=last_name,vendor_display_name = dispn, company_name= comp, gst_treatment=gsttype, gst_number=gstin, 
                    pan_number=panno,vendor_wphone = w_mobile,vendor_mphone = p_mobile, vendor_email=email,skype_number = skype,
                    source_supply=supply,currency=currency, website=website, designation = desg, department = dpt,
                    opening_bal=balance,baddress=street, bcity=city, bstate=state, payment_terms=payment,bzip=pincode, 
                    bcountry=country, saddress=shipstreet, scity=shipcity, sstate=shipstate,szip=shippincode, scountry=shipcountry,
                    bfax = fax, sfax = shipfax, bphone = phone, sphone = shipphone,user = u)
        vndr.save()

        return HttpResponse("success")

# def vendor_dropdownE(request):
#     user = User.objects.get(id=request.user.id)

#     options = {}
#     option_objects = vendor_tableE.objects.filter(user=user)
#     for option in option_objects:
#         # options[option.id] = [option.first_name + " " + option.last_name, option.first_name + " " + option.last_name + " " + str(option.id)]
#         display_name = f"{option.salutation} {option.first_name} {option.last_name}"
#         options[option.id] = [display_name, display_name + " " + str(option.id)]
#         # options[option.id] = display_name
#     return JsonResponse(options)

def vendor_dropdownE(request):
    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = vendor_table.objects.filter(user=user)
    for option in option_objects:
        display_name = f"{option.salutation} {option.first_name} {option.last_name}"
        options[option.id] = [display_name, display_name]
    return JsonResponse(options)
    
    
def deletefile(request,aid):
    att=Payrollfiles.objects.get(id=aid)
    p=att.payroll
    att.delete()
    return redirect('payroll_view',p.id)
    
    
def project_customer(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        # title=request.POST.get('title')
        # first_name=request.POST.get('firstname')
        # last_name=request.POST.get('lastname')
        # comp=request.POST.get('company_name')
        cust_type = request.POST.get('customer_type')
        name = request.POST.get('display_name')
        comp_name = request.POST.get('company_name')
        email=request.POST.get('email')
        website=request.POST.get('website')
        w_mobile=request.POST.get('work_mobile')
        p_mobile=request.POST.get('pers_mobile')
        fb = request.POST.get('facebook')
        twitter = request.POST.get('twitter')
        skype = request.POST.get('skype')
        desg = request.POST.get('desg')
        dpt = request.POST.get('dpt')
        gsttype=request.POST.get('gsttype')
        # gstin=request.POST.get('gstin')
        # panno=request.POST.get('panno')
        supply=request.POST.get('placeofsupply')
        tax = request.POST.get('tax_preference')
        currency=request.POST.get('currency')
        balance=request.POST.get('openingbalance')
        payment=request.POST.get('paymentterms')
        street1=request.POST.get('street1')
        street2=request.POST.get('street2')
        city=request.POST.get('city')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
        country=request.POST.get('country')
        fax=request.POST.get('fax')
        phone=request.POST.get('phone')
        # shipstreet1=request.POST.get('shipstreet1')
        # shipstreet2=request.POST.get('shipstreet2')
        # shipcity=request.POST.get('shipcity')
        # shipstate=request.POST.get('shipstate')
        # shippincode=request.POST.get('shippincode')
        # shipcountry=request.POST.get('shipcountry')
        # shipfax=request.POST.get('shipfax')
        # shipphone=request.POST.get('shipphone')

        u = User.objects.get(id = request.user.id)

        cust = customer(customerName = name,customerType = cust_type, companyName= comp_name, GSTTreatment=gsttype, 
                        customerWorkPhone = w_mobile,customerMobile = p_mobile, customerEmail=email,skype = skype,Facebook = fb, 
                        Twitter = twitter,placeofsupply=supply,Taxpreference = tax,currency=currency, website=website, 
                        designation = desg, department = dpt,OpeningBalance=balance,Address1=street1,Address2=street2, city=city, 
                        state=state, PaymentTerms=payment,zipcode=pincode,country=country,  fax = fax,  phone1 = phone,user = u)
        cust.save()

        return HttpResponse({"message": "success"})
        
        
@login_required(login_url='login')
def customer_dropdown_proj(request):
    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = customer.objects.filter(user = user)
    for option in option_objects:
        options[option.id] = [option.id , option.customerName]

    return JsonResponse(options) 
    
    
def recurbills_payzzz(request):
    if request.method == 'POST':
        # Extract the data from the POST request
        name = request.POST.get('name')
        days = request.POST.get('days')

        # Create a new payment_terms object and save it to the database
        payment_term = payment_terms(Terms=name, Days=days)
        payment_term.save()

        # Return a JSON response indicating success
        return JsonResponse({"message": "success"})
        
        
def split_paragraph(paragraph):
    if paragraph is None:
        return '',''
    else:
        words = paragraph.split()
        total_words = len(words)
        midpoint = None
        for i in range(total_words):
            if i > total_words // 2 and words[i].isalpha():
                midpoint = i
                break
        if midpoint is None:
            # If no suitable midpoint found, split at the actual midpoint
            midpoint = total_words // 2
    
        first_half = ' '.join(words[:midpoint])
        second_half = ' '.join(words[midpoint:])
        return first_half, second_half
    
    
def filter_by_draft(request):
    user = request.user
    estimates=Estimates.objects.filter(status='draft',user=user)
    return render(request, 'all_estimates.html', {'estimates':estimates})
    
    
def filter_by_sent(request):
    user = request.user
    estimates=Estimates.objects.filter(status='sent',user=user)
    return render(request, 'all_estimates.html', {'estimates':estimates})
    
    
def filter_by_draft_estimate_view(request,pk):
    user = request.user
    company = company_details.objects.get(user=user)
    all_estimates = Estimates.objects.filter(user=user,status='draft')
    estimate = Estimates.objects.get(id=pk)
    items = EstimateItems.objects.filter(estimate=estimate)
    context = {
        'company': company,
        'all_estimates':all_estimates,
        'estimate': estimate,
        'items': items,
    }
    return render(request, 'estimate_slip.html', context)
    
    
def filter_by_sent_estimate_view(request,pk):
    user = request.user
    company = company_details.objects.get(user=user)
    all_estimates = Estimates.objects.filter(user=user,status='sent')
    estimate = Estimates.objects.get(id=pk)
    items = EstimateItems.objects.filter(estimate=estimate)
    context = {
        'company': company,
        'all_estimates':all_estimates,
        'estimate': estimate,
        'items': items,
    }
    return render(request, 'estimate_slip.html', context)
    
    
def add_est_comment(request,pk):
    if request.method=="POST":
        user=request.user      
        estimate=Estimates.objects.get(id=pk)
       
        comment=estimate_comments()
        comment.user=user
        comment.estimate=estimate
        comment.comments=request.POST.get('comments')
       
        comment.save()
    return redirect('estimateslip',estimate.id)
    
    
###########Report############
def report_inventory_view(request):
    company = company_details.objects.get(user=request.user)
    return render(request,'reports_inventory.html',{'company':company})
    
    
def report_view(request):
    company = company_details.objects.get(user=request.user)
    return render(request,'reports.html',{'company':company})

def inventory_summary(request):
    company = company_details.objects.get(user=request.user)
    sales = sales_item.objects.all()
    item=AddItem.objects.all()
    return render(request,'inventory_summary.html',{'company':company,'item':item,'sales':sales})


def custom_repot(request):
    company = company_details.objects.get(user=request.user)
    item = AddItem.objects.all()
    return render(request,'custom_report_inventory.html',{'company':company,'items':item})

def inventory_Valuation_summary(request):
    company = company_details.objects.get(user=request.user)
    item = AddItem.objects.all()
    return render(request,'inventory-valuation.html',{'company':company,'item':item})


def custom_valuation_repot(request):
    company = company_details.objects.get(user=request.user)
    item = AddItem.objects.all()
    return render(request,'custom-valuation-report.html',{'company':company,'items':item})


def show_hide(request):
    company = company_details.objects.get(user=request.user)
    return render(request,'show_hide.html',{'company':company})

def general(request):
    company = company_details.objects.get(user=request.user)
    return render(request,'custom-valuation-report.html',{'company':company})
    
    
#Abin - Vendor Credits

@login_required(login_url='login')
def vendor_credits_home(request):

    company = company_details.objects.get(user = request.user)
    recur = Vendor_Credits_Bills.objects.filter(user = request.user.id).values()
    for r in recur:
        vn = r['vendor_name'].split()[1:]
        r['vend_name'] = " ".join(vn)
        

    sorted_recur = sorted(recur, key=lambda r: r['vendor_name'],reverse=True) 

    context = {
                'company' : company,
                'recur_bill' : sorted_recur
            }
    return render(request,'vendor_credits_home.html',context)
    
    

def getitems2(request):
    cmp1 = request.user
    id=request.GET.get('id')
    print(id)
    data=AddItem.objects.get(Name=id,user_id=cmp1)
    print(data)
    price=data.s_price
    return JsonResponse({"price":price})
    
    
def vendor_credits(request):
    c = customer.objects.all()
    p = AddItem.objects.all()
    i = invoice.objects.all()
    pay = payment_terms.objects.all()

    if request.user.is_authenticated:
        vendors = vendor_table.objects.all()
        if request.method == 'POST':
            # c=request.POST['cx_name']
            # cus=customer.objects.get(customerName=c) 
            # print(cus.id)  
            # custo=cus.id
            company_name = request.POST.get('sel')
            vendor_email = request.POST.get('email')
            baddress = request.POST.get('address')
            gst_treatment = request.POST.get('gst')
            source_supply = request.POST.get('placeofsupply')
            credit_note = request.POST.get('credit_note')
            order_no = request.POST.get('order_number')
            vendor_date = request.POST.get('credit_date')
            cxnote = request.POST['customer_note']
            subtotal = request.POST['subtotal']
            igst = request.POST['igst']
            cgst = request.POST['cgst']
            sgst = request.POST['sgst']
            adjustment = request.POST['adjustment_charge']
            totaltax = request.POST['totaltax']
            t_total = request.POST['t_total']

            file = request.FILES['file'] if 'file' in request.FILES else "/static/images/alt.jpg"
            # tc = request.POST['ter_cond']
            status = request.POST['sd']
            if status == 'draft':
                print(status)
            else:
                print(status)

            product = request.POST.getlist('item[]')
            hsn = request.POST.getlist('hsn[]')           
            quantity = request.POST.getlist('quantity[]')          
            rate = request.POST.getlist('rate[]')           
            discount = request.POST.getlist('desc[]')           
            tax = request.POST.getlist('tax[]')     
                 
            total = request.POST.getlist('amount[]')
            print(total)

            inv = Vendor_Credits.objects.create(
                
                user=request.user,
                # customer_id=custo,
                company_name=company_name,
                vendor_email=vendor_email,
                baddress=baddress,
                credit_note=credit_note,
                gst_treatment=gst_treatment,
                source_supply=source_supply,
                order_no=order_no,
                vendor_date=vendor_date,
                cgst=cgst,
                sgst=sgst,
                adjustment=adjustment,
                cxnote=cxnote,
                subtotal=subtotal,
                igst=igst,
                t_tax=totaltax,
                grandtotal=t_total,
                status=status,
                file=file
            )
            inv.save()
            inv_id=Vendor_Credits.objects.get(id=inv.id)

            if len(product) == len(hsn) == len(quantity) == len(discount) == len(tax) == len(total) == len(rate):
                
                mapped = zip(product, hsn, quantity, discount, tax, total, rate)
                mapped = list(mapped)
            
                for element in mapped:
                    created = Vendor_invoice_item.objects.create(
                        inv=inv_id,
                        product=element[0],
                        hsn=element[1],
                        quantity=element[2],
                        discount=element[3],
                        tax=element[4],
                        total=element[5],
                        rate=element[6]
                    )
                    created.save()
            return redirect('vendor_credits_home')

    context = {
        'c': c,
        'p': p,
        'i': i,
        'pay': pay,
        'vendors': vendors,
    }

    return render(request, 'vendor_credits.html', context)
    
    
def show_credits(request, pk):
    user_id=request.user.id
    udata=User.objects.get(id=user_id)
    vdata1=Vendor_Credits.objects.filter(user=udata)
    vcredit=Vendor_Credits.objects.get(id=pk)
    mdata=Credits_mail_table.objects.filter(vendor=pk)
    ddata=Credits_doc_upload_table.objects.filter(user=udata,vendor=vcredit)

    cdata = Credits_comments_table.objects.filter(vendor=vcredit).order_by('-id')
    # comment = Credits_comments_table.objects.filter(vendor=pk).order_by('id')
    return render(request,'show_credit.html',{'vdata':vdata1,'vcredit':vcredit,'mdata':mdata,'ddata':ddata,'cdata':cdata})
    
    
@login_required(login_url='login')
def delete_comment_credit(request, pk,vid):
    comment = Credits_comments_table.objects.get(id=pk)
    comment.delete()

    return redirect('show_credits',pk=vid)
    
    
def credit_sendmail(request,pk):
    if request.method=='POST':
        user_id=request.user.id
        udata=User.objects.get(id=user_id)
        vdata2=Vendor_Credits.objects.get(id=pk)
        mail_from=settings.EMAIL_HOST_USER
        mail_to=request.POST['email']
        subject=request.POST['subject']
        content=request.POST['content']
        mail_data=Credits_mail_table(user=udata,vendor=vdata2,mail_from=mail_from,mail_to=mail_to,subject=subject,content=content)
        mail_data.save()

        subject = request.POST['subject']
        message = request.POST['content']
        recipient = request.POST['email']     #  recipient =request.POST["inputTagName"]
        send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])

        return redirect("vendor_credits_home")
        
        
def credit_upload_document(request,pk):
    if request.method=='POST':
        user_id=request.user.id
        udata=User.objects.get(id=user_id)
        vdata=Vendor_Credits.objects.get(id=pk)
        title=request.POST['title']
        document=request.FILES.get('file')
        doc_data=Credits_doc_upload_table(user=udata,vendor=vdata,title=title,document=document)
        doc_data.save()
        return redirect("vendor_credits_home")
        
        
def credit_download_doc(request,pk):
    document=get_object_or_404(Credits_doc_upload_table,id=pk)
    response=HttpResponse(document.document,content_type='application/pdf')
    response['Content-Disposition']=f'attachment; filename="{document.document.name}"'
    return response
    
    
def credit_delete_vendor(request,pk):
    if Credits_comments_table.objects.filter(vendor=pk).exists():
        user2=Credits_comments_table.objects.filter(vendor=pk)
        user2.delete()
    if Credits_mail_table.objects.filter(vendor=pk).exists():
        user3=Credits_mail_table.objects.filter(vendor=pk)
        user3.delete()
    if Credits_doc_upload_table.objects.filter(vendor=pk).exists():
        user4=Credits_doc_upload_table.objects.filter(vendor=pk)
        user4.delete()

    
    user1=Vendor_Credits.objects.get(id=pk)
    user1.delete()
    return redirect("vendor_credits_home")
    
    
def edit_vendor_credits(request,id):
    company = company_details.objects.get(user = request.user)
    vendor=vendor_table.objects.all()
    cust=customer.objects.filter(user = request.user)
    payment=payment_terms.objects.all()
    item=AddItem.objects.all()
    account=Account.objects.all()
    unit=Unit.objects.all()
    sales=Sales.objects.all()
    purchase=Purchase.objects.all()
    po=Vendor_Credits_Bills.objects.get(id=id)
    po_tabl=Vendor_Credits_Bills_items_bills.objects.filter(recur_bills=id)
    context={
        'company' : company,
        'vendor':vendor,
        'customer':cust,
        'payment':payment,
        'item':item,
        'account':account,
        'units':unit,
        'sales':sales,
        'purchase':purchase,
        'po':po,        
        'po_table':po_tabl,
    }
    return render(request,'edit_vendor_credits.html',context)
    
    
def credits_statement(request,id):
    sales=Vendor_Credits.objects.get(id=id)
    saleitem=Vendor_invoice_item.objects.filter(inv_id=id)
    sale_order=Vendor_Credits.objects.all()
    company=company_details.objects.get(user_id=request.user.id)
    
    
    context={
        'sale':sales,
        'saleitem':saleitem,
        'sale_order':sale_order,
        'comp':company,
        'vendor':vendor,
        
        
                    }
    return render(request,'vender_credit_state.html',context)
    
    
def add_customer_for_vcredit(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            
            salutation=request.POST['salutation']
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            company_name=request.POST['company_name']
            vendor_display_name=request.POST['v_display_name']
            vendor_email=request.POST['vendor_email']
            vendor_wphone=request.POST['w_phone']
            vendor_mphone=request.POST['m_phone']
            skype_number=request.POST['skype_number']
            designation=request.POST['designation']
            department=request.POST['department']
            website=request.POST['website']
            gst_treatment=request.POST['gst']
            
            gst_number=request.POST['gst_number']
            pan_number=request.POST['pan_number']
            
            source_supply=request.POST['source_supply']
            currency=request.POST['currency']
            opening_bal=request.POST['opening_bal']
            payment_terms=request.POST['payment_terms']
            
            battention=request.POST['battention']
            bcountry=request.POST['bcountry']
            baddress=request.POST['baddress']
            bcity=request.POST['bcity']
            bstate=request.POST['bstate']
            bzip=request.POST['bzip']
            bphone=request.POST['bphone']
            bfax=request.POST['bfax']
        

          
           
            u = User.objects.get(id = request.user.id)

          
            ctmr=vendor_table(salutation=salutation,first_name=first_name,
                        last_name=last_name,company_name=company_name,vendor_display_name=vendor_display_name,
                         vendor_email=vendor_email,vendor_wphone=vendor_wphone,vendor_mphone=vendor_mphone,
                           skype_number=skype_number,designation=designation,department=department, website=website,
                             gst_treatment=gst_treatment,gst_number=gst_number,pan_number=pan_number,
                                source_supply=source_supply,currency=currency,opening_bal=opening_bal,payment_terms=payment_terms,baddress=baddress,
                                 battention=battention,bcountry=bcountry,bcity=bcity,bstate=bstate,
                                  bzip=bzip,bphone=bphone,bfax=bfax,user=u )
            ctmr.save()  
            
            return redirect("vendor_credits")
        return render(request,"add_vendor_vcredits.html",)
        
        
def additem_vendor_page(request):
    unit=Unit.objects.all()
    sale=Sales.objects.all()
    purchase=Purchase.objects.all()
    accounts = Purchase.objects.all()
    account_types = set(Purchase.objects.values_list('Account_type', flat=True))

    
    account = Sales.objects.all()
    account_type = set(Sales.objects.values_list('Account_type', flat=True))
    
    

    return render(request,'add_vendor_credit_items.html',{'unit':unit,'sale':sale,'purchase':purchase,
               
                            "account":account,"account_type":account_type,"accounts":accounts,"account_types":account_types,
                            
                            })
                            
                            
                            
def additem_vendor_credit(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            radio=request.POST.get('radio')
            if radio=='tax':
    
                
                inter=request.POST['inter']
                intra=request.POST['intra']
                type=request.POST.get('type')
                name=request.POST['name']
                unit=request.POST['unit']
                sel_price=request.POST.get('sel_price')
                sel_acc=request.POST.get('sel_acc')
                s_desc=request.POST.get('sel_desc')
                cost_price=request.POST.get('cost_price')
                cost_acc=request.POST.get('cost_acc')      
                p_desc=request.POST.get('cost_desc')
                u=request.user.id
                us=request.user
                history="Created by" + str(us)
                user=User.objects.get(id=u)
                unit=Unit.objects.get(id=unit)
                sel=Sales.objects.get(id=sel_acc)
                cost=Purchase.objects.get(id=cost_acc)
                ad_item=AddItem(type=type,Name=name,p_desc=p_desc,s_desc=s_desc,s_price=sel_price,p_price=cost_price,unit=unit,
                            sales=sel,purchase=cost,user=user,creat=history,interstate=inter,intrastate=intra
                                )
                
            else:
                                                  
                type=request.POST.get('type')
                name=request.POST['name']
                unit=request.POST['unit']
                sel_price=request.POST.get('sel_price')
                sel_acc=request.POST.get('sel_acc')
                s_desc=request.POST.get('sel_desc')
                cost_price=request.POST.get('cost_price')
                cost_acc=request.POST.get('cost_acc')      
                p_desc=request.POST.get('cost_desc')
                u=request.user.id
                us=request.user
                history="Created by" + str(us)
                user=User.objects.get(id=u)
                unit=Unit.objects.get(id=unit)
                sel=Sales.objects.get(id=sel_acc)
                cost=Purchase.objects.get(id=cost_acc)
                ad_item=AddItem(type=type,Name=name,p_desc=p_desc,s_desc=s_desc,s_price=sel_price,p_price=cost_price,unit=unit,
                            sales=sel,purchase=cost,user=user,creat=history,interstate='none',intrastate='none'
                                )
                ad_item.save()
            ad_item.save()
           
            return redirect("vendor_credits")
    return render(request,'add_vendor_credit_items.html')
    
def poject_itemz(request):
    user_id = request.GET.get('id')
    user = get_object_or_404(usercreate, usernamezz=user_id)
    email = user.emailzz
    return JsonResponse({'email': email})
    
def report(request):
  return render(request, 'reports.html')

def fifo_cost(request):
    company = company_details.objects.get(user = request.user)
    return render(request, 'fifo_cost.html', {'company': company})

def product_sales(request):
    company = company_details.objects.get(user = request.user)
    return render(request, 'product_sales.html', {'company': company})

def show_customize_product(request):
    general = "url1"
    show = "url2"
    
    company = company_details.objects.get(user = request.user)
    
    context = {
        'url1' : general,
        'url2' : show,
        'company': company,
    }
    return render(request, 'customize_show_product.html', context)

def product_customize(request):
    general = "url1"
    show = "url2"
    
    items = AddItem.objects.all()
    company = company_details.objects.get(user = request.user)
    
    context = {
        'url1' : general,
        'url2' : show,
        'item' : items,
        'company': company,
    }
    return render(request, 'customize_product.html', context)

def customize_fifo(request):
    items = AddItem.objects.all()
    company = company_details.objects.get(user = request.user)
    context = {
        'item': items,
        'company': company,
        }
    return render(request, 'customize_fifo.html', context)
    
    
    
#-----------bills-----sumayya------------------------------------------------------------------------------------------------

def view_bills(request):
    user = request.user
    bills = PurchaseBills.objects.filter(user=user).order_by('-id')
    company = company_details.objects.get(user=user)
    pickup_records = []
    for bill in bills:
        record = {"bill_date":str(bill.bill_date),"bill_no":str(bill.bill_no),"customer_name":bill.customer_name,"vendor_name":bill.vendor_name,"status":bill.status,"total":bill.total,"id":bill.id,"balance":str(bill.balance)}
        pickup_records.append(record)

    context = {
        'bills': pickup_records,
        'company': company,
    }

    return render(request, 'viewbills.html', context)


def new_bill(request):
    user = request.user
    company = company_details.objects.get(user_id=user.id)
    items = AddItem.objects.filter(user_id=user.id)
    vendors = vendor_table.objects.filter(user_id=user.id)
    customers = customer.objects.filter(user_id=user.id)
    terms = payment_terms.objects.exclude(Days__isnull=True).filter(user_id=user.id)
    units = Unit.objects.all()
    account = Chart_of_Account.objects.all()
    account_types = Chart_of_Account.objects.values_list('account_type', flat=True).distinct()
    sales_acc = Sales.objects.all()
    pur_acc = Purchase.objects.all()
    bank=Bankcreation.objects.all()
    last_id = PurchaseBills.objects.filter(user_id=user.id).order_by('-id').values('id').first()
    if last_id:
        last_id = last_id['id']
        next_no = last_id+1
    else:
        next_no = 1
    context = {'company': company,
               'items': items,
               'vendors': vendors,
               'customers': customers,
               'terms': terms,
               'units': units,
               'b_no': next_no,
               'acc': account,
               'acc_types':account_types,
               's_acc': sales_acc,
               'p_acc': pur_acc,
               'bank':bank,
               }

    return render(request, 'newbill.html',context)


def get_customer_data_bill(request):
    user = request.user
    name = request.GET.get('id') 
    custobject = customer.objects.get(customerName=name, user=user)
    email = custobject.customerEmail
    pos = custobject.placeofsupply 
    gst_treatment = custobject.GSTTreatment
    gst_number = custobject.GSTIN
    return JsonResponse({"status": " not", 'email': email, 'pos': pos, 'gst_treatment' : gst_treatment, 'gst_number' : gst_number }) 

def get_vendor_data_bill(request):
    user = request.user
    name = request.GET.get('id')
    first_name, last_name = name.split(' ') 
    vendorobject = vendor_table.objects.get(first_name=first_name, last_name=last_name)
    email = vendorobject.vendor_email
    sos = vendorobject.source_supply
    gst_treatment = vendorobject.gst_treatment
    gst_number = vendorobject.gst_number  
    return JsonResponse({"status": " not", 'email': email, 'sos': sos,'gst_number': gst_number,'gst_treatment': gst_treatment})

@login_required(login_url='login')
def add_vendor_bills(request):
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        title=request.POST.get('title')
        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')
        fullname = request.POST.get('display_name')
        comp_name = request.POST.get('company_name')
        email=request.POST.get('email')
        website=request.POST.get('website')
        w_mobile=request.POST.get('work_mobile')
        p_mobile=request.POST.get('pers_mobile')
        skype = request.POST.get('skype')
        desg = request.POST.get('desg')
        dpt = request.POST.get('dpt')
        gsttype=request.POST.get('gsttype')
        gstin=request.POST.get('gstin')
        panno=request.POST.get('panno')
        s_supply=request.POST.get('sourceofsupply')
        currency=request.POST.get('currency')
        balance=request.POST.get('openingbalance')
        payment=request.POST.get('paymentterms')
        street=request.POST.get('street')
        city=request.POST.get('city')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
        country=request.POST.get('country')
        fax=request.POST.get('fax')
        phone=request.POST.get('phone')
        shipstreet=request.POST.get('shipstreet')
        shipcity=request.POST.get('shipcity')
        shipstate=request.POST.get('shipstate')
        shippincode=request.POST.get('shippincode')
        shipcountry=request.POST.get('shipcountry')
        shipfax=request.POST.get('shipfax')
        shipphone=request.POST.get('shipphone')

        u = User.objects.get(id = request.user.id)

        vend = vendor_table(user = u,salutation=title,first_name=first_name,last_name=last_name,company_name=comp_name,vendor_display_name=fullname,
                            vendor_email=email,vendor_wphone=w_mobile,vendor_mphone=p_mobile,skype_number=skype,designation=desg,
                            department=dpt,website=website,gst_treatment=gsttype,gst_number=gstin,pan_number=panno,source_supply=s_supply,
                            currency=currency,opening_bal=balance,payment_terms=payment,bcountry=country,baddress=street,bcity=city,
                            bstate=state,bphone=phone,bfax=fax,scountry=shipcountry,saddress=shipstreet,scity=shipcity,
                            sstate=shipstate,sphone=shipphone,sfax=shipfax)
        vend.save()

        response_data = {
            "message": "success",
            "fullname":fullname,
            "email": email,
            "sos": s_supply,
            "gstin": gstin
        }

        return JsonResponse(response_data)

@login_required(login_url='login')
def entr_custmr_for_bills(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        # title=request.POST.get('title')
        # first_name=request.POST.get('firstname')
        # last_name=request.POST.get('lastname')
        # comp=request.POST.get('company_name')
        cust_type = request.POST.get('customer_type')
        name = request.POST.get('display_name')
        comp_name = request.POST.get('company_name')
        email=request.POST.get('email')
        website=request.POST.get('website')
        w_mobile=request.POST.get('work_mobile')
        p_mobile=request.POST.get('pers_mobile')
        fb = request.POST.get('facebook')
        twitter = request.POST.get('twitter')
        skype = request.POST.get('skype')
        desg = request.POST.get('desg')
        dpt = request.POST.get('dpt')
        gsttype=request.POST.get('gsttype')
        # gstin=request.POST.get('gstin')
        # panno=request.POST.get('panno')
        supply=request.POST.get('placeofsupply')
        tax = request.POST.get('tax_preference')
        currency=request.POST.get('currency')
        balance=request.POST.get('openingbalance')
        payment=request.POST.get('paymentterms')
        street1=request.POST.get('street1')
        street2=request.POST.get('street2')
        city=request.POST.get('city')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
        country=request.POST.get('country')
        fax=request.POST.get('fax')
        phone=request.POST.get('phone')
        # shipstreet1=request.POST.get('shipstreet1')
        # shipstreet2=request.POST.get('shipstreet2')
        # shipcity=request.POST.get('shipcity')
        # shipstate=request.POST.get('shipstate')
        # shippincode=request.POST.get('shippincode')
        # shipcountry=request.POST.get('shipcountry')
        # shipfax=request.POST.get('shipfax')
        # shipphone=request.POST.get('shipphone')

        u = User.objects.get(id = request.user.id)

        cust = customer(customerName = name,customerType = cust_type, companyName= comp_name, GSTTreatment=gsttype, 
                        customerWorkPhone = w_mobile,customerMobile = p_mobile, customerEmail=email,skype = skype,Facebook = fb, 
                        Twitter = twitter,placeofsupply=supply,Taxpreference = tax,currency=currency, website=website, 
                        designation = desg, department = dpt,OpeningBalance=balance,Address1=street1,Address2=street2, city=city, 
                        state=state, PaymentTerms=payment,zipcode=pincode,country=country,  fax = fax,  phone1 = phone,user = u)
        cust.save()

        response_data = {
            "message": "success",
            "name":name,
            "email": email,
            "pos": supply
        }

        return JsonResponse(response_data)

@login_required(login_url='login')
def create_account_bills(request):
    u = User.objects.get(id = request.user.id)
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        type=request.POST.get('type')
        name=request.POST.get('name')

        u = User.objects.get(id = request.user.id)

        acc = Chart_of_Account(account_type=type,account_name=name,user = u)
        acc.save()

        response_data = {
            "message": "success",
            "name":name,
        }

        return JsonResponse(response_data)

@login_required(login_url='login')
def create_payment_terms_bills(request):
    u = User.objects.get(id = request.user.id)
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        t_name=request.POST.get('name')
        t_days=request.POST.get('days')

        u = User.objects.get(id = request.user.id)

        term = payment_terms(Terms=t_name,Days=t_days)
        term.save()

        response_data = {
            "message": "success",
            "t_name":t_name,
        }

        return JsonResponse(response_data)
    
def additem_bills(request):
    
    radio=request.GET.get('radios')
    inter=request.GET.get('inters')
    intra=request.GET.get('intras')
    type=request.GET.get('types')
    name=request.GET.get('names')
    unit=request.GET.get('units')
    sel_price=request.GET.get('sel_prices')
    sel_acc=request.GET.get('sel_accs')
    s_desc=request.GET.get('s_descs')
    cost_price=request.GET.get('cost_prices')
    cost_acc=request.GET.get('cost_accs')      
    p_desc=request.GET.get('p_descs')
    hsn=request.GET.get('hsn')
    u=request.user.id
    us=request.user
    history="Created by" + str(us)
    user=User.objects.get(id=u)
    unit=Unit.objects.get(id=unit)
    sel=Sales.objects.get(id=sel_acc)
    cost=Purchase.objects.get(id=cost_acc)
    ad_item=AddItem(type=type,Name=name,p_desc=p_desc,s_desc=s_desc,s_price=sel_price,p_price=cost_price,unit=unit,
                sales=sel,purchase=cost,user=user,creat=history,interstate=inter,intrastate=intra, hsn = hsn
                    )
    ad_item.save()

    return JsonResponse({"status": " not", 'name': name})

def itemdata_bills(request):
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)
    company = company_details.objects.get(user=user)
    # print(company.state)
    id = request.GET.get('id')
    cust = request.GET.get('cust') 

    item = AddItem.objects.get(Name=id, user=user)

    rate = item.p_price
    hsn = item.hsn
    return JsonResponse({"status": " not", 'rate': rate, 'hsn' : hsn})
    return redirect('/')

def create_purchase_bill(request):
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)
    if request.method == 'POST':
        vendor_name = request.POST['vendor_name']
        vendor_email = request.POST['vendor_email']
        vendor_gst = request.POST['gstin_inp']
        sos = request.POST['sos']
        cust_name = request.POST['customer_name']
        cus=customer.objects.get(customerName=cust_name)   
        custo=cus.id 
        cust_email = request.POST['customer_email']
        pos = request.POST['pos']
        bill_number = request.POST['bill_number']
        order_number = request.POST['order_number']
        bill_date = request.POST['bill_date']
        due_date = request.POST['due_date']
        terms = request.POST['p_terms']
        repeat_every = request.POST['repeats']
        payment_method = request.POST['paymentmethod']
        amt_paid = request.POST['amtPaid']
        adjustment = request.POST['add_round_off']
        
       
        

        item = request.POST.getlist('item[]')
        account = request.POST.getlist('account[]')
        quantity = request.POST.getlist('quantity[]')
        rate = request.POST.getlist('rate[]')
        tax = request.POST.getlist('tax[]')
        amount = request.POST.getlist('amount[]')
        hsn = request.POST.getlist('HSN[]')
        discount = request.POST.getlist('discount[]')
        # print(item)
        # print(quantity)
        # print(rate)
        # print(discount)
        # print(tax)
        # print(amount)

        # cust_note = request.POST['customer_note']
        sub_total = request.POST['subtotal']
        igst = request.POST['igst']
        sgst = request.POST['sgst']
        cgst = request.POST['cgst']
        tax_amnt = request.POST['total_taxamount']
        shipping = request.POST['shipping_charge']
        
        total = request.POST['total']
        # tearms_conditions = request.POST['tearms_conditions']
        attachment = request.FILES.get('file')
        status = 'Draft'
        terms = request.POST['p_terms']
        balance = float(total) - float(amt_paid)
        bill = PurchaseBills(user=user,cusname_id=custo, customer_name=cust_name,customer_email= cust_email,place_of_supply=pos,vendor_name=vendor_name,
                             vendor_email=vendor_email,vendor_gst_no = vendor_gst,source_of_supply=sos,bill_no=bill_number, order_number=order_number, bill_date=bill_date, 
                             due_date=due_date,payment_terms=terms, sub_total=sub_total,igst=igst,sgst=sgst,cgst=cgst,tax_amount=tax_amnt, 
                             shipping_charge=shipping,total=total, status=status,attachment=attachment,repeat_every=repeat_every,
                             payment_method=payment_method,amt_paid=amt_paid,balance=balance, adjustment= adjustment)
        bill.save()
        
        if len(item) == len(quantity) == len(rate) == len(account) == len(tax) == len(amount) == len(hsn) == len(discount):
            mapped = zip(item, quantity, rate, account, tax, amount, hsn, discount)
            mapped = list(mapped)
            for element in mapped:
                created = PurchaseBillItems.objects.create(
                    purchase_bill=bill, item_name=element[0], quantity=element[1], rate=element[2], account=element[3], tax_percentage=element[4], amount=element[5], hsn=element[6], discount=element[7])
    return redirect('view_bills')


def create_purchase_bill1(request):
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)
    if request.method == 'POST':
        vendor_name = request.POST['vendor_name']
        vendor_email = request.POST['vendor_email']
        vendor_gst = request.POST['gstin_inp']
        sos = request.POST['sos']
        cust_name = request.POST['customer_name']
        cust_email = request.POST['customer_email']
        pos = request.POST['pos']
        bill_number = request.POST['bill_number']
        order_number = request.POST['order_number']
        bill_date = request.POST['bill_date']
        due_date = None if request.POST.get('due_date') == "" else  request.POST.get('due_date')
        terms = request.POST['p_terms']
        repeat_every = request.POST['repeats']
        payment_method = request.POST['paymentmethod']
        adjustment = request.POST['add_round_off']
        amt_paid = request.POST['amtPaid']
        

        item = request.POST.getlist('item[]')
        # account = request.POST.getlist('account[]')
        quantity = request.POST.getlist('quantity[]')
        rate = request.POST.getlist('rate[]')
        tax = request.POST.getlist('tax[]')
        amount = request.POST.getlist('amount[]')
        hsn = request.POST.getlist('HSN[]')
        discount = request.POST.getlist('discount[]')

        # cust_note = request.POST['customer_note']
        sub_total = request.POST['subtotal']
        igst = request.POST['igst']
        sgst = request.POST['sgst']
        cgst = request.POST['cgst']
        tax_amnt = request.POST['total_taxamount']
        shipping = request.POST['shipping_charge']
       
        total = request.POST['total']
        # tearms_conditions = request.POST['tearms_conditions']
        attachment = request.FILES.get('file')
        status = 'Save'
        balance = float(total) - float(amt_paid)
       
        bill = PurchaseBills(user=user, customer_name=cust_name,customer_email= cust_email,place_of_supply=pos,vendor_name=vendor_name,
                             vendor_email=vendor_email,vendor_gst_no=vendor_gst,source_of_supply=sos,bill_no=bill_number, order_number=order_number, bill_date=bill_date, 
                             due_date=due_date,payment_terms=terms, sub_total=sub_total,igst=igst,sgst=sgst,cgst=cgst,tax_amount=tax_amnt, 
                             shipping_charge=shipping,total=total, status=status,attachment=attachment,repeat_every=repeat_every,
                             payment_method=payment_method,amt_paid=amt_paid,balance=balance,adjustment=adjustment)
        bill.save()
       

        if len(item) == len(quantity) == len(rate) == len(tax) == len(amount) == len(hsn) == len(discount):
            mapped = zip(item, quantity, rate,tax, amount, hsn, discount)
            mapped = list(mapped)
            for element in mapped:
                created = PurchaseBillItems.objects.create(
                    purchase_bill=bill, item_name=element[0], quantity=element[1], rate=element[2], tax_percentage=element[3], amount=element[4], hsn=element[5], discount=element[6])
    return redirect('view_bills')




def bill_view(request, b_id):
    user = request.user
    company = company_details.objects.get(user=user)
    bills = PurchaseBills.objects.filter(user=user)
    bill = PurchaseBills.objects.get(id=b_id)
    items = PurchaseBillItems.objects.filter(purchase_bill=bill)
    comment = purchase_comments.objects.filter(purchase_bill=b_id)
    context = {
        'company': company,
        'bills': bills,
        'bill': bill,
        'items': items,
        'comments':comment,
    }
    return render(request, 'bill_slip.html', context)

def add_comment_bills(request,bill_id):
    if request.method == 'POST':
        bill = PurchaseBills.objects.get(id=bill_id) 
        bill.comments = request.POST['comment']
        bill.save()
        return redirect('bill_view',b_id = bill_id)
    

def edit_bill(request,bill_id):
    user = request.user
    company = company_details.objects.get(user=user)
    customers = customer.objects.filter(user_id=user.id)
    vendors = vendor_table.objects.filter(user_id=user.id)
    items = AddItem.objects.filter(user_id=user.id)
    bill = PurchaseBills.objects.get(id=bill_id)
    bill_items = PurchaseBillItems.objects.filter(purchase_bill=bill)
    units = Unit.objects.all()
    terms = payment_terms.objects.exclude(Days__isnull=True).filter(user_id=user.id)
    account = Chart_of_Account.objects.all()
    account_types = Chart_of_Account.objects.values_list('account_type', flat=True).distinct()
    sales_acc = Sales.objects.all()
    pur_acc = Purchase.objects.all()
    bank=Bankcreation.objects.all()

    last_id = PurchaseBills.objects.filter(user_id=user.id).order_by('-id').values('id').first()
    if last_id:
        last_id = last_id['id']
        next_no = last_id+1
    else:
        next_no = 1
    print(bill_items)
    context = {
        'company': company,
        'bill': bill,
        'customers': customers,
        'items': items,
        'bill_items': bill_items,
        'vendors': vendors,
        'terms': terms,
        'acc': account,
        'acc_types':account_types,
        's_acc': sales_acc,
        'p_acc': pur_acc,
        'units': units,
        'id': bill_id,
        'bank':bank,
        
    }
    return render(request, 'edit_bill.html', context)


def update_bills(request,pk):
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)

    if request.method == 'POST':
        bill = PurchaseBills.objects.get(id=pk)
        bill.user = user
        bill.vendor_name = request.POST['vendor_name']
        bill.vendor_email = request.POST['vendor_email']
        bill.vendor_gst = request.POST['gstin_inp']
        bill.source_of_supply = request.POST['sos']
        bill.customer_name = request.POST['customer_name']
        bill.customer_email = request.POST['customer_email']
        bill.place_of_supply = request.POST['pos']
        bill.bill_no = request.POST['bill_number']
        bill.order_number = request.POST['order_number']
        bill.bill_date = request.POST['bill_date']
        bill.due_date = None if request.POST.get('due_date') == "" else  request.POST.get('due_date')
        bill.payment_terms = request.POST['p_terms']
        bill.repeat_every = request.POST['repeats']
        bill.payment_method = request.POST['paymentmethod']
        bill.adjustment = request.POST['add_round_off']
        bill.amt_paid = request.POST['amtPaid']
        

        bill.sub_total = request.POST['subtotal']
        bill.igst = request.POST['igst']
        bill.sgst = request.POST['sgst']
        bill.cgst = request.POST['cgst']
        bill.tax_amount = request.POST['total_taxamount']
        bill.shipping_charge = request.POST['shipping_charge'] 
        bill.total = request.POST['total']
        bill.status = 'Draft'
        total = request.POST['total']
        amt_paid = request.POST['amtPaid']
        bill.balance = float(total) - float(amt_paid)
        
       
        old=bill.attachment
        new=request.FILES.get('file')
        if old != None and new == None:
            bill.attachment = old
        else:
            bill.attachment = new

        bill.save()

        item = request.POST.getlist('item[]')
        
        quantity = request.POST.getlist('quantity[]')
        rate = request.POST.getlist('rate[]')
        tax = request.POST.getlist('tax[]')
        amount = request.POST.getlist('amount[]')
        hsn = request.POST.getlist('HSN[]')
        discount = request.POST.getlist('discount[]')
       
        # print(item)
        # print(quantity)
        # print(rate)
        # print(discount)
        # print(tax)
        # print(amount)

        objects_to_delete = PurchaseBillItems.objects.filter(purchase_bill_id=bill.id)
        objects_to_delete.delete()
 
        if len(item) == len(quantity) == len(rate) == len(tax) == len(amount) == len(hsn) == len(discount) and item and quantity and rate and  tax and amount and hsn and discount:
            mapped = zip(item, quantity, rate, tax, amount, hsn, discount)
            mapped = list(mapped)
            for element in mapped:
                created = PurchaseBillItems.objects.create(
                    purchase_bill=bill, item_name=element[0], quantity=element[1], rate=element[2], tax_percentage=element[3], amount=element[4], hsn=element[5], discount=element[6])
    return redirect('bill_view',b_id = bill.id)


def upload_file_bills(request,bill_id):
    if request.method == 'POST':
        bill = PurchaseBills.objects.get(id=bill_id) 
        bill.attachment = request.FILES.get('file')
        bill.save()
        return redirect('bill_view',b_id = bill_id)

def delete_bill(request,bill_id):
    bill = PurchaseBills.objects.get(id = bill_id)
    bill.delete()
    return redirect('view_bills')

def search_bill(request):
    if request.method == "POST":
        user = request.user
        company = company_details.objects.get(user=user)
        search = request.POST['search']
        cloumn = request.POST['type']

        if cloumn == '1' or search  == '':
            return redirect('view_bills')    

        else :
            if cloumn == '2':
                bills = PurchaseBills.objects.filter(user=user,customer_name=search).all()

                context = {
                    'bills': bills,
                    'company': company,
                }

                return render(request, 'viewbills.html', context)

            else:
                if cloumn == '3':
                    bills = PurchaseBills.objects.filter(user=user,bill_no=search).all()

                    context = {
                        'bills': bills,
                        'company': company,
                    }

                    return render(request, 'viewbills.html', context)       
   
    
    return redirect('view_bills')
    
    
@login_required(login_url='login')    
def expense_pay(request):
    
    if request.method=='POST':

        name=request.POST.get('name')
        days=request.POST.get('days')
        
        u = User.objects.get(id = request.user.id)

        pay = payment_termsE(Terms=name, Days=days, user = u)
        pay.save()

        return HttpResponse({"message": "success"})
        
        
@login_required(login_url='login')
def pay_dropdownE(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = payment_termsE.objects.filter(user = user)
    for option in option_objects:
        options[option.id] = [option.Terms]

    return JsonResponse(options)   
    
    
# def get_vendor_gst_treatment(request):
#     v_user = request.user
#     user = User.objects.get(id=v_user.id)
  
#     vendor = request.GET.get('vendor')
#     vendor = vendor_tableE.objects.get(vendor_display_name=vendor, user=user)
#     gst_treatment = vendor.gst_treatment
   
#     return JsonResponse({'gst_treatment':gst_treatment})
# def get_vendor_gst_treatment(request):
#     v_user = request.user
#     user = User.objects.get(id=v_user.id)

#     vendor_name = request.GET.get('vendor') 
#     try:
#         vendor = vendor_tableE.objects.get(vendor_display_name=vendor_name, user=user)
#         gst_treatment = vendor.gst_treatment
#     except vendor_tableE.DoesNotExist:
#         gst_treatment = None

#     print(f"Vendor Name: {vendor_name}, GST Treatment: {gst_treatment}")

#     return JsonResponse({'gst_treatment': gst_treatment})


def get_vendor_gst_treatment(request):
    v_user = request.user
    user = User.objects.get(id=v_user.id)

    vendor_name = request.GET.get('vendor') 
    if vendor_name: 
        try:
            vendor = vendor_table.objects.get(id=vendor_name, user=user)
            gst_treatment = vendor.gst_treatment
            gstin = vendor.gst_number  
        except vendor_table.DoesNotExist:
            gst_treatment = None
            gstin = None

        print(f"Vendor Name: {vendor_name}, GST Treatment: {gst_treatment}, GSTIN: {gstin}")

        return JsonResponse({'gst_treatment': gst_treatment, 'gstin': gstin})
    else:
     
        return JsonResponse({'gst_treatment': None, 'gstin': None})
    
    
def get_company_state(request):
    user = request.user
    try:
        company = company_details.objects.get(user=user)
        state = company.state
    except company_details.DoesNotExist:
        state = None
    print("Fetched State:", state)
    return JsonResponse({"state": state})
    
def reports(request):
    return render(request,'reports.html') 
    
    
def salesby_customer(request):
    customer1 = customer.objects.all()
    company_data = company_details.objects.get(user=request.user)
    return render(request, 'salesby_customer.html', {'cust': customer1, 'company_data': company_data})
    
    
def customize_report(request):
    company_data = company_details.objects.get(user=request.user)

    return render(request, 'customize_report.html',{'company_data': company_data})

    return render(request, 'customize_report.html',{'company_data': company_data})
    
def general_customize(request):
    return render(request,'general_customize.html') 
    
def salesby_item(request):
    items = invoice_item.objects.all()
    items2 =recur_itemtable.objects.all()
 
    company_data = company_details.objects.get(user=request.user)
    return render(request, 'salesby_item.html', {'items': items,'items2': items2, 'company_data': company_data})        
    
def customize_report1(request):
    company_data = company_details.objects.get(user=request.user)
    items = AddItem.objects.all()
    customers = customer.objects.all()
    available_columns = ["Sales(FCY)", "Sales with Tax", "Company Name", "First Name", "Last Name", "Website",
                         "Customer Email", "Mobile Phone", "WorkPhone", "Department", "Designation"]
    
    context = {
        "available_columns": available_columns,
    }
    return render(request, 'customize_report1.html', {'items': items, 'customers': customers,'company_data': company_data})
    
def salesby_item_filter(request):
    company_data = company_details.objects.get(user=request.user)
    item = sales_item.objects.all()
    items2 =recur_itemtable.objects.all()
    if request.method == 'POST':
        s=request.POST['d1']
        start=str(s)
        e=request.POST['d2']
        end=str(e)
        items = invoice_item.objects.filter(inv__due_date__range=[start,end])
        items2 = recur_itemtable.objects.filter(ri__start__range=[start,end])
        return render(request, 'salesby_item.html', {'items': items,'items2': items2, 'company_data': company_data})  

    

    return render(request, 'salesby_item.html', {'items': item, 'company_data': company_data})  

def salesgraph(request,product):
    company=company_details.objects.get(user=request.user)
    user_id=request.user
    item=invoice_item.objects.filter(product=product)
    items2 =recur_itemtable.objects.filter(iname=product)
    print(items2)

    # print(items)
    # labels = [items.name for item in items]
    # values = [item.value for item in items]
    products=AddItem.objects.all()
    n=AddItem.objects.get(Name=product)
    name=product
    print(name)
 
    context={

       "allproduct":item,
       "items2":items2,
       
       'name':name,
       "product":products,
        "n":n,
    #    "history":history,
       'company':  company, 
    #    "comments":comments,
    #    'stock': stock,
        'label': 'Line Chart',
        # 'labels': labels,
        # 'values': values,
        'chart_type': 'bar'
        
    }
    print('1')
    return render(request,'salesgraph.html',context)  

def salesby_item_graph_filter(request,product):
    company=company_details.objects.get(user=request.user)
    user_id=request.user
    item=invoice_item.objects.filter(product=product)
    n=AddItem.objects.get(Name=product)

    products=AddItem.objects.all()
    name=product
    print(name)
    if request.method == 'POST':
        s=request.POST['d1']
        start=str(s)
        e=request.POST['d2']
        end=str(e)
        items =  invoice_item.objects.filter(product=product,inv__due_date__range=[start,end])
        items2 =recur_itemtable.objects.filter(iname=product,ri__start__range=[start,end])
        products=AddItem.objects.all()
        n=AddItem.objects.get(Name=product)
        context={

       "allproduct":items,
       'items2':items2,
       
       'name':name,
       "n":n,
       "product":products,
    #    "history":history,
       'company':  company, 
    #    "comments":comments,
    #    'stock': stock,
        'label': 'Line Chart',
        # 'labels': labels,
        # 'values': values,
        'chart_type': 'bar'
        }
        return render(request, 'salesgraph.html',context)  

    
    context={

       "allproduct":item,
       
       'name':name,
       "n":n,
       "product":products,
    #    "history":history,
       'company':  company, 
    #    "comments":comments,
    #    'stock': stock,
        'label': 'Line Chart',
        # 'labels': labels,
        # 'values': values,
        'chart_type': 'bar'
    }
    return render(request, 'salesgraph.html', context)            
    
def customerAtoZ_bills(request):
    user = request.user
    bills = PurchaseBills.objects.filter(user=user).order_by('customer_name')
    company = company_details.objects.get(user=user)
    context = {
        'bills': bills,
        'company': company,
    }

    return render(request, 'viewbills.html', context)
    
def vendorAtoZ_bills(request):
    user = request.user
    bills = PurchaseBills.objects.filter(user=user).order_by('vendor_name')
    company = company_details.objects.get(user=user)
    context = {
        'bills': bills,
        'company': company,
    }

    return render(request, 'viewbills.html', context)
    
    
def sendmails(request,id):
    if request.method=='POST':
       user_id=request.user.id
       udata=User.objects.get(id=user_id)
       cdata2=customer.objects.get(id=id)
       mail_from=settings.EMAIL_HOST_USER
       mail_to=request.POST['sendto']
       subject=request.POST['subject']
       content=request.POST['messag']
       mail_data=customer_mail_table(user=udata,customr=cdata2,mail_from=mail_from,mail_to=mail_to,subject=subject,content=content)
       mail_data.save()
       #----------------------------------------------
       subject=request.POST['subject']
       messag=request.POST['messag']
       sendto=request.POST['sendto']
       send_mail(subject,messag,settings.EMAIL_HOST_USER,
                 [sendto],fail_silently=False)
       return redirect('view_customr')
       
       
def cust_comments(request,id):
    if request.method=='POST':
       user_id=request.user.id
       udata=User.objects.get(id=user_id)
       cdata2=customer.objects.get(id=id)
       comment=request.POST['comments']
       cmts=customer_comments_table(user=udata,customr=cdata2,comment=comment)
       cmts.save()
       return redirect('view_customr')
       
def cust_Attach_files(request,id):
    if request.method=='POST':
        user_id=request.user.id
        udata=User.objects.get(id=user_id)
        cdata2=customer.objects.get(id=id)
        title=request.POST['title']
        document=request.FILES.get('file')
        doc_data=customer_doc_upload_table(user=udata,customr=cdata2,title=title,document=document)
        doc_data.save()
        return redirect('view_customr')
        
def sales_order(request):
    company = company_details.objects.get(user = request.user)
    data = SalesOrder.objects.all()
    cust = customer.objects.all()
    name_list =[]
    for item in cust :
        if item.customerName[3:] not in name_list:
            name_list.append(item.customerName[3:])
    return render(request, 'sales_order.html',{'data':data, 'company': company,'name_list':name_list})
    
    
def sales_summery(request):
    company = company_details.objects.get(user = request.user)
    data = AddItem.objects.all()
    
    return render(request, 'sales_summery.html', {'data':data, 'company': company})
    
    
def transaction(request, pk):
    product = AddItem.objects.get(id = pk)
    company = company_details.objects.get(user = request.user)
    
    items=AddItem.objects.all()
    
    estimate = EstimateItems.objects.filter(item_name = product.Name)
    sales_order = sales_item.objects.filter(product = product.Name)
    recurring_invoice = recur_itemtable.objects.filter(iname = product.Name)
    purchase_order = Purchase_Order_items.objects.filter(item = product.Name)
    recurring_bills = recurring_bills_items.objects.filter(item = product.Name)
    invoice = invoice_item.objects.filter(product = product.Name)
    deliveryChellan = ChallanItems.objects.filter(item_name = product.Name)
    bills = PurchaseBillItems.objects.filter(item_name = product.Name)
    expense = Expense.objects.filter(goods_label = product.Name)
    
    quantity = int(product.stock)
    price = int(product.p_price)
    stock = (quantity * price)
    
    
    
    context = {
        'allproduct': items,
        'product': product,
        'company': company,
        
        'estimate': estimate,
        'sales_order': sales_order,
        'recurring_invoice': recurring_invoice,
        'purchase_order': purchase_order,
        'recurring_bills': recurring_bills,
        'invoice': invoice,
        'deliveryChellan': deliveryChellan,
        'bills': bills,
        'expense': expense,
        'stock': stock,
    }
    
    return render(request, 'transactions.html',context)
    
    
login_required(login_url='login')
def view_sales_order_all(request):
    sales=SalesOrder.objects.all()
    return render(request,'view_sales_order.html',{"sale":sales})   
    
login_required(login_url='login')
def view_sales_order_Draft(request):
    sales=SalesOrder.objects.filter(status="draft")
    return render(request,'view_sales_order.html',{"sale":sales}) 
    
login_required(login_url='login')
def view_sales_order_approved(request):
    sales=SalesOrder.objects.filter(status="approved")
    return render(request,'view_sales_order.html',{"sale":sales}) 

@login_required(login_url='login')
def customer_dropdown_sales(request):
    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = customer.objects.filter(user = user)
    for option in option_objects:
        options[option.id] = [option.customerName]

    return JsonResponse(options)
    
    
def gstr2_load(request):
    company = company_details.objects.get(user=request.user)
    purchase= PurchaseBills.objects.all()
    purchaseItem=PurchaseBillItems.objects.all()
    recur_bills=recurring_bills.objects.all()
    recur_add_bills=recurring_bills_items.objects.all()
  
   
    context={'company':company,'purchase':purchase,'purchases':purchaseItem,'recur_bills':recur_bills,'recur_add_bills':recur_add_bills}
    return render(request,'GSTR_2.html',context)
    
def sales_by_hsn_load(request):
     company = company_details.objects.get(user=request.user)
    #  item = AddItem.objects.all()
     invoices=invoice.objects.all()
     invoice_items = invoice_item.objects.all()
 
     return render(request,'sales_by_hsn.html',{'company':company,'invoice':invoices,'invoice_item':invoice_items})
     
     
def export_sales_pdf(request,id):

    user = request.user
    company = company_details.objects.get(user=user)
    sales = SalesOrder.objects.get(id=id)
    items = sales_item.objects.filter(sale_id=id)
    

    template_path = 'pdfsales.html'
    context = {
        'company': company,
        'sale':sales,
        'item':items,
        
    }
    fname=sales.sales_no
   
    # Create a Django response object, and specify content_type as pdftemp_creditnote
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'
    response['Content-Disposition'] =f'attachment; filename= {fname}.pdf'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    


    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
    
    
#---------------------shamreena---GSTR1 & GSTR_3B

def GSTR_3Bpage(request):
    company = company_details.objects.get(user=request.user)
    context={
       
        'company':company
    }
    return render(request,'GSTR_3B2.html',context)
    
def GSTR_1page(request):
    company = company_details.objects.get(user=request.user)
    data=invoice.objects.all()
    invoices=recurring_invoice.objects.all()
    reinv=RetainerInvoice.objects.all()
    context={
        'invoices':invoices,
        'data':data,
        'reinv':reinv,
        'company':company
    }
    return render(request,'gstr1_s2.html', context)
    
    
def change_vendor_status(request,pk):
    company=company_details.objects.get(user=request.user)
    user_id=request.user.id
    vdata=vendor_table.objects.get(id=pk)
    if vdata.status == 'Active':
        vdata.status = 'Inactive'
        vdata.save()
    else:
        vdata.status = 'Active'
        vdata.save()
    return redirect('view_vendor_details',pk=vdata.id)
    
    
#Reshna-banking

def bank_home(request):
    cp= company_details.objects.get(user = request.user)
    banks= Bankcreation.objects.filter(user=request.user)
    bank_balances = []
    for bank in banks:
        bank_transactions = transactions.objects.filter(user=request.user, bank=bank)
        bank_balance = sum([transaction.amount for transaction in bank_transactions])
        bank_balances.append((bank, bank_balance))
   
    
    return render(request, 'bank_home.html', {'company': cp,'bank_balances': bank_balances})

def create_bank(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
           
            date = request.POST.get('date')
            name = request.POST.get('name')
            opn_bal = float(request.POST.get('opn_bal', 0.0))
            bal_type=request.POST.get('bal_type')
            branch= request.POST.get('branch')
            ac_no= request.POST.get('ac_no')
            ifsc=request.POST.get('ifsc')
            if bal_type == 'Credit':
                opn_bal = -opn_bal
            else:
                opn_bal = opn_bal


            bank = Bankcreation.objects.create(
                user=request.user,
                name=name,
                opn_bal=opn_bal,
                bal_type=bal_type,
                branch=branch,
                ac_no=ac_no,
                ifsc=ifsc,
                date=date
              
            )

            bank.save()
            banka = Bankcreation.objects.get(id=bank.id)

            if len(request.FILES) != 0:
                banka.document=request.FILES['file'] 
                banka.save()

            return redirect('bank_home')
        else:
          
          
            cp= company_details.objects.get(user = request.user)
            return render(request, 'addbank.html', {'company':cp})

def edit_bank(request,bank_id):
    if request.user.is_authenticated:
        bank = Bankcreation.objects.get(id=bank_id,user=request.user)
        if request.method == 'POST':
            bank.name = request.POST.get('name')
            bank.opn_bal = float(request.POST.get('opn_bal', 0.0))
            bank.bal_type = request.POST.get('bal_type')
            if bank.bal_type == 'Credit':
                bank.opn_bal = -bank.opn_bal
            else: 
                bank.opn_bal = bank.opn_bal
            
           
            bank.date = request.POST.get('date')
            print(type(bank.date))
            bank.branch = request.POST.get('branch')
            bank.ac_no = request.POST.get('ac_no')
            bank.ifsc = request.POST.get('ifsc')
            bank.save()
            return redirect('bank_listout',id=bank_id)
        else:
          
          
            cp= company_details.objects.get(user = request.user)
            return render(request, 'editbank.html', {'company':cp,'bank': bank})

def delete_bank(request, bank_id):
    if request.user.is_authenticated:
        bank = Bankcreation.objects.get(id=bank_id, user=request.user)
        bank.delete()
    return redirect('bank_home')  

# def bank_listout(request,id):
#     cp= company_details.objects.get(user = request.user)
#     bank= Bankcreation.objects.filter(user=request.user)
#     banks =get_object_or_404(Bankcreation, id=id)      
#     bankc=transactions.objects.filter(user=request.user,bank=banks)
#     bank_balance = sum([transaction.amount for transaction in bankc])
#     bank_balances = []
#     for bank in bank:
#         transactions_for_bank = transactions.objects.filter(user=request.user, bank=bank)
#         balance = sum([transaction.amount for transaction in transactions_for_bank])
#         bank_balances.append((bank, balance))

#     return render(request,'banklistout.html', {'company':cp, 'bank':bank ,'banks':banks,'bankc':bankc,'bank_balance':bank_balance,'bank_balances': bank_balances})   

def bank_listout(request, id):
    cp = company_details.objects.get(user=request.user)
    banks_list = Bankcreation.objects.filter(user=request.user)

    selected_bank = get_object_or_404(Bankcreation, id=id)
    transactions_for_selected_bank = transactions.objects.filter(user=request.user, bank=selected_bank)
    print(transactions_for_selected_bank)
    bank_balance = sum([transaction.amount for transaction in transactions_for_selected_bank])

    for transaction in transactions_for_selected_bank:
            if transaction.type == 'Bank To Bank Transfer':
                if transaction.amount > 0:
                    transaction.display_text = f'From: {transaction.fromB}'
                else:
                    transaction.display_text = f'To: {transaction.toB}'
            else:
                transaction.display_text = '' 

    bank_balances = []
    for bank in banks_list:
        transactions_for_bank = transactions.objects.filter(user=request.user, bank=bank)
        balance = sum([transaction.amount for transaction in transactions_for_bank])
        bank_balances.append((bank, balance))

    return render(request, 'banklistout.html', {'company': cp, 'banks_list': banks_list, 'selected_bank': selected_bank, 'bank_balance': bank_balance, 'bank_balances': bank_balances ,'transactions_for_selected_bank':transactions_for_selected_bank})


def banktocash(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            date = request.POST.get('date')
            fromB = request.POST.get('fromB')
            toB = request.POST.get('toB')
            amount = float(request.POST.get('amount', 0.0))
            description = request.POST.get('description')
            type = request.POST.get('type')
            adjtype = request.POST.get('adjtype') 
            adjacname = request.POST.get('adjacname')
            bank = Bankcreation.objects.get(id=id)

            if type == 'Cash To Bank Transfer':
                to_bank = Bankcreation.objects.get(id=toB)
                cash_to_banktransaction = transactions.objects.create(
                    user=request.user,
                    fromB=fromB,
                    toB=toB,
                    amount=amount,
                    description=description,
                    date=date,
                    type=type,
                    bank=to_bank
                )
               
                cash_to_banktransaction.save()

            if type == 'Adjust Bank Balance':
                if adjtype == 'Reduce Balance':
                    amount = -amount
                else:
                    amount=amount
                ad_bank = Bankcreation.objects.get(id=adjacname)
                adj_transaction = transactions.objects.create(
                    user=request.user,
                    fromB=fromB,
                    adjacname=adjacname,
                    description=description,
                    date=date,
                    adjtype=adjtype,
                    type=type,
                    bank=ad_bank,
                    amount=amount
                )
                
                
                adj_transaction.save()

            if type == 'Bank To Cash Transfer':
                from_bankB = Bankcreation.objects.get(id=fromB)
                bank_to_cash_transaction = transactions.objects.create(
                    user=request.user,
                    fromB=fromB,
                    toB=toB,
                    amount=-amount,
                    description=description,
                    date=date,
                    type=type,
                    bank=from_bankB
                )
               
                bank_to_cash_transaction.save()
                
            if type == 'Bank To Bank Transfer':
                from_bank = Bankcreation.objects.get(id=fromB)
                to_bank = Bankcreation.objects.get(id=toB)
                from_bank_transaction = transactions.objects.create(
                    user=request.user,
                    fromB=from_bank.name,
                    toB=to_bank.name,
                    amount=-amount,
                    description=description,
                    date=date,
                    type=type,
                    bank=from_bank
                )
                
                from_bank_transaction.save()

               
                to_bank_transaction = transactions.objects.create(
                    user=request.user,
                    fromB=from_bank.name,
                    toB=to_bank.name,
                    amount=amount,
                    description=description,
                    date=date,
                    type=type,
                    bank=to_bank
                )
               
                to_bank_transaction.save()

            return redirect('bank_listout', id=id)
        else:
            b = Bankcreation.objects.filter(user=request.user)
            cp = company_details.objects.get(user=request.user)
            return render(request, 'banklistout.html', {'company': cp, 'bank': b})


def bank_attachfile(request,id):

    company = company_details.objects.get(user = request.user)
    bank = Bankcreation.objects.get(user = request.user,id=id)
    print(bank)

    if request.method == 'POST':

        bank.document=request.POST.get('file')

        if len(request.FILES) != 0:
             
            bank.document = request.FILES['file']

        bank.save()
        return redirect('bank_listout',id=id)

def nameasc(request):
    cp = company_details.objects.get(user = request.user)
    bank =Bankcreation.objects.filter(user = request.user).order_by('name')
    print(bank)
    bank_balances = []
    for bank in bank:
        bank_transactions = transactions.objects.filter(user=request.user, bank=bank)
        bank_balance = sum([transaction.amount for transaction in bank_transactions])
        bank_balances.append((bank, bank_balance))
    return render(request, 'bank_home.html', {'company': cp, 'bank_balances': bank_balances})

def namedes(request):
    cp = company_details.objects.get(user = request.user)
    bank =Bankcreation.objects.filter(user = request.user).order_by('-name')
    print(bank)
    bank_balances = []
    for bank in bank:
        bank_transactions = transactions.objects.filter(user=request.user, bank=bank)
        bank_balance = sum([transaction.amount for transaction in bank_transactions])
        bank_balances.append((bank, bank_balance))
    return render(request, 'bank_home.html', {'company': cp, 'bank_balances': bank_balances})

def view_nameasc(request,id):
    cp = company_details.objects.get(user = request.user)
    banks_list =Bankcreation.objects.filter(user = request.user).order_by('name')
    print(banks_list)
    selected_bank = get_object_or_404(Bankcreation, id=id)
    transactions_for_selected_bank = transactions.objects.filter(user=request.user, bank=selected_bank)
    print(transactions_for_selected_bank)
    bank_balance = sum([transaction.amount for transaction in transactions_for_selected_bank])

    bank_balances = []
    for bank in banks_list:
        transactions_for_bank = transactions.objects.filter(user=request.user, bank=bank)
        balance = sum([transaction.amount for transaction in transactions_for_bank])
        bank_balances.append((bank, balance))
    for transaction in transactions_for_selected_bank:
            if transaction.type == 'Bank To Bank Transfer':
                if transaction.amount > 0:
                    transaction.display_text = f'From: {transaction.fromB}'
                else:
                    transaction.display_text = f'To: {transaction.toB}'
            else:
                transaction.display_text = '' 

    return render(request, 'banklistout.html', {'company': cp, 'banks_list': banks_list, 'selected_bank': selected_bank, 'bank_balance': bank_balance, 'bank_balances': bank_balances ,'transactions_for_selected_bank':transactions_for_selected_bank})

def view_namedes(request,id):
    cp = company_details.objects.get(user = request.user)
    banks_list =Bankcreation.objects.filter(user = request.user).order_by('-name')
    print(banks_list)
    selected_bank = get_object_or_404(Bankcreation, id=id)
    transactions_for_selected_bank = transactions.objects.filter(user=request.user, bank=selected_bank)
    print(transactions_for_selected_bank)
    bank_balance = sum([transaction.amount for transaction in transactions_for_selected_bank])

    bank_balances = []
    for bank in banks_list:
        transactions_for_bank = transactions.objects.filter(user=request.user, bank=bank)
        balance = sum([transaction.amount for transaction in transactions_for_bank])
        bank_balances.append((bank, balance))
    for transaction in transactions_for_selected_bank:
            if transaction.type == 'Bank To Bank Transfer':
                if transaction.amount > 0:
                    transaction.display_text = f'From: {transaction.fromB}'
                else:
                    transaction.display_text = f'To: {transaction.toB}'
            else:
                transaction.display_text = '' 

    return render(request, 'banklistout.html', {'bankcompany': cp,'company': cp, 'banks_list': banks_list, 'selected_bank': selected_bank, 'bank_balance': bank_balance, 'bank_balances': bank_balances ,'transactions_for_selected_bank':transactions_for_selected_bank,})

def bank_status(request, id):
    cp = company_details.objects.get(user=request.user)
    banks_list = Bankcreation.objects.filter(user=request.user)

    selected_bank = get_object_or_404(Bankcreation, id=id)
    transactions_for_selected_bank = transactions.objects.filter(user=request.user, bank=selected_bank)
    print(transactions_for_selected_bank)
    bank_balance = sum([transaction.amount for transaction in transactions_for_selected_bank])

    for transaction in transactions_for_selected_bank:
            if transaction.type == 'Bank To Bank Transfer':
                if transaction.amount > 0:
                    transaction.display_text = f'From: {transaction.fromB}'
                else:
                    transaction.display_text = f'To: {transaction.toB}'
            else:
                transaction.display_text = '' 

    bank_balances = []
    for bank in banks_list:
        transactions_for_bank = transactions.objects.filter(user=request.user, bank=bank)
        balance = sum([transaction.amount for transaction in transactions_for_bank])
        bank_balances.append((bank, balance))
    # if request.method == 'POST':
        selected_bank = get_object_or_404(Bankcreation, id=id)
        # new_status = request.POST.get('action')
        # selected_bank.status = new_status
        if selected_bank.status == 'Active':
            selected_bank.status = 'Inactive'
        else:
            selected_bank.status = 'Active'
        selected_bank.save()
        # selected_bank.save()

        # return JsonResponse({'message': 'Status updated successfully'})
    
    return render(request, 'banklistout.html', {'company': cp, 'banks_list': banks_list, 'selected_bank': selected_bank, 'bank_balance': bank_balance, 'bank_balances': bank_balances ,'transactions_for_selected_bank':transactions_for_selected_bank})

def bank_pdf(request, id):
    cp = company_details.objects.get(user=request.user)
    banks_list = Bankcreation.objects.filter(user=request.user)
    selected_bank = get_object_or_404(Bankcreation, id=id)
    transactions_for_selected_bank = transactions.objects.filter(user=request.user, bank=selected_bank)
    print(transactions_for_selected_bank)
    bank_balance = sum([transaction.amount for transaction in transactions_for_selected_bank])

    bank_balances = []
    for bank in banks_list:
        transactions_for_bank = transactions.objects.filter(user=request.user, bank=bank)
        balance = sum([transaction.amount for transaction in transactions_for_bank])
        bank_balances.append((bank, balance))
    for transaction in transactions_for_selected_bank:
            if transaction.type == 'Bank To Bank Transfer':
                if transaction.amount > 0:
                    transaction.display_text = f'From: {transaction.fromB}'
                else:
                    transaction.display_text = f'To: {transaction.toB}'
            else:
                transaction.display_text = '' 

    script_directory = os.path.dirname(os.path.abspath(__file__))
    template_filename = 'banklistout.html'
    template_path = os.path.join(script_directory, 'templates', template_filename)

    with open(template_path, 'r') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    section = soup.find('div', class_='print-only')
    section_html = section.prettify()
    template = Template(section_html)

    context = {
    'company': cp, 'banks_list': banks_list, 'selected_bank': selected_bank, 
    'bank_balance': bank_balance, 'bank_balances': bank_balances ,
    'transactions_for_selected_bank':transactions_for_selected_bank
    }
    html = template.render(Context(context))

    fname = selected_bank.name
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={fname}.pdf'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    
    return response
        
        
@login_required(login_url='login')
def vendor_credit_dropdown(request):
    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = vendor_table.objects.filter(user = user)
    for option in option_objects:
        
        options[option.id] = [option.salutation, option.first_name, option.last_name, option.id]
    return JsonResponse(options)
    
    
@login_required(login_url='login')
def vendor_credit_item(request):

    company = company_details.objects.get(user = request.user)

    if request.method=='POST':
        type=request.POST.get('type')
        name=request.POST['name']
        hsn=request.POST['hsn']
        ut=request.POST['unit']
        inter=request.POST['inter']
        intra=request.POST['intra']
        sell_price=request.POST.get('sell_price')
        sell_acc=request.POST.get('sell_acc')
        sell_desc=request.POST.get('sell_desc')
        cost_price=request.POST.get('cost_price')
        cost_acc=request.POST.get('cost_acc')      
        cost_desc=request.POST.get('cost_desc')
        units=Unit.objects.get(id=ut)
        sel=Sales.objects.get(id=sell_acc)
        cost=Purchase.objects.get(id=cost_acc)

        history="Created by " + str(request.user)
        user = User.objects.get(id = request.user.id)

        item=AddItem(type=type,unit=units,sales=sel,purchase=cost,Name=name,hsn=hsn,p_desc=cost_desc,s_desc=sell_desc,s_price=sell_price,p_price=cost_price,
                    user=user,creat=history,interstate=inter,intrastate=intra)

        item.save()


        return HttpResponse({"message": "success"})
    
@login_required(login_url='login')
def vendor_credit_item_dropdown(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = AddItem.objects.all()
    for option in option_objects:
        options[option.id] = option.Name

    return JsonResponse(options)
    
    
@login_required(login_url='login')
def get_vendor_credit_det(request):

    company= company_details.objects.get(user = request.user)

    # fname = request.POST.get('fname')
    # lname = request.POST.get('lname')
    id = request.POST.get('id')
    vdr = vendor_table.objects.get(user=company.user_id, id=id)
    vemail = vdr.vendor_email
    gstnum = vdr.gst_number
    gsttr = vdr.gst_treatment
    baddress = vdr.baddress

    return JsonResponse({'vendor_email' :vemail, 'gst_number' : gstnum,'gst_treatment':gsttr, 'baddress' : baddress},safe=False)
    
    
@login_required(login_url='login')
def get_vendor_credit_det1(request):

    company= company_details.objects.get(user = request.user)

    # fname = request.POST.get('fname')
    # lname = request.POST.get('lname')
    # name = request.POST.get('id')
    full_name = request.POST.get('id')
    first_name, last_name = full_name.split() if full_name else ('', '')
    print(first_name)
    print(last_name)


    vdr = vendor_table.objects.get(user=company.user_id, first_name=first_name,last_name=last_name)
    
    vemail = vdr.vendor_email
    gstnum = vdr.gst_number
    gsttr = vdr.gst_treatment
    baddress = vdr.baddress

    return JsonResponse({'vendor_email' :vemail, 'gst_number' : gstnum,'gst_treatment':gsttr, 'vendor_name' : baddress},safe=False)
    
@login_required(login_url='login')
def view_vendor_credits(request,id):

    company = company_details.objects.get(user = request.user)
    bills = Vendor_Credits_Bills.objects.filter(user = request.user)
    rbill=Vendor_Credits_Bills.objects.get(user = request.user, id= id)
    billitem = Vendor_Credits_Bills_items_bills.objects.filter(user = request.user,recur_bills=id)
    
    #cust = customer.objects.get(id = rbill.customer_name.split(" ")[0])
    # vend = vendor_table.objects.get(id = rbill.company_name.split(" ")[0])
    gst_or_igst = "GST" if company.state == (" ".join(rbill.source_supply.split(" ")[1:])) else "IGST"
    tax_total = [] 
    for b in billitem:
        if b.tax not in tax_total: 
            tax_total.append(b.tax)
    
    #cust_name = cust.customerName
    # vend_name = vend.salutation+ " " +vend.first_name + " " +vend.last_name
    context = {
                'company' : company,
                'recur_bills' : bills,
                'recur_bill' : rbill,
                'bill_item' : billitem,
                'tax' : tax_total,
                "gst_or_igst" : gst_or_igst,
                #'customer' : cust,
                # 'vendor' : vend,
                #'customer_name' : cust_name,
                # 'vendor_name' : vend_name,
            }

    return render(request, 'view_vendor_credits.html',context)
    
@login_required(login_url='login')
def vendor_credit_comment(request):

    company = company_details.objects.get(user = request.user)

    if request.method=='POST':
        id =request.POST.get('id')
        cmnt =request.POST.get('comment')
        
        u = User.objects.get(id = request.user.id)
        r_bill = Vendor_Credits_Bills.objects.get(user = request.user, id = id)
        r_bill.comments = cmnt
        r_bill.save()

        return redirect('vendor_credits_home',id)
    return redirect('vendor_credits_home')
    
@login_required(login_url='login')
def vendor_credit_add_file(request,id):

    company = company_details.objects.get(user = request.user)
    bill = recurring_bills.objects.get(user = request.user,id=id)
    print(bill)

    if request.method == 'POST':

        bill.document=request.POST.get('file')

        if len(request.FILES) != 0:
             
            bill.document = request.FILES['file']

        bill.save()
        return redirect('view_recurring_bills',id)
        
        
def vendor_credit_email(request,id):

    company = company_details.objects.get(user = request.user)
    bill = Vendor_Credits_Bills.objects.get(user = request.user,id=id)

    if request.method == 'POST':

        recipient =request.POST.get('recipient')
        sender =request.POST.get('sender')
        sub =request.POST.get('subject')
        message =request.POST.get('message')

    script_directory = os.path.dirname(os.path.abspath(__file__))
    template_filename = 'view_vendor_credits.html'
    template_path = os.path.join(script_directory, 'templates', template_filename)

    with open(template_path, 'r') as file:
        html_content = file.read()
        

    soup = BeautifulSoup(html_content, 'html.parser')
    section = soup.find('div', class_='print-only')
    section_html = section.prettify()
    template = Template(section_html)

    if template:
        prntonly_content = str(template)

    # print(prntonly_content)
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as temp_file:
        temp_file.write(prntonly_content.encode('utf-8'))

    with open(temp_file.name, 'rb') as attachment_file:
        attachment_content = attachment_file.read()

    email = EmailMessage(
        subject=sub,
        body=message,
        from_email=sender,
        to=[recipient],
    )
    email.attach('Recurring Bill',attachment_content , 'text/html')

    email.send()
     
    return HttpResponse(status=200)
    
@login_required(login_url='login')
def vc_view_vendorasc(request,id):
    company = company_details.objects.get(user = request.user)
    bills =Vendor_Credits_Bills.objects.filter(user = request.user).order_by('company_name')

    rbill=Vendor_Credits_Bills.objects.get(user = request.user, id= id)
    billitem = Vendor_Credits_Bills_items_bills.objects.filter(user = request.user,recur_bills=id)

    comp_state = company.state
    # cust = customer.objects.get(id = rbill.customer_name.split(" ")[0])
    vend = vendor_table.objects.get(id = rbill.company_name.split(" ")[0])
    gst_or_igst = "GST" if comp_state == rbill.source_supply else "IGST"


    tax_total = 0 
    for b in billitem:
        tax_total += b.tax

    context = {
                'company' : company,
                'recur_bills' : bills,
                'recur_bill' : rbill,
                'bill_item' : billitem,
                'tax' : tax_total,
                "gst_or_igst" : gst_or_igst,
                # 'customer' : cust,
                'vendor' : vend,
            }
    return render(request,'view_vendor_credits.html',context)
    
    
@login_required(login_url='login')
def vc_view_vendordesc(request,id):
    company = company_details.objects.get(user = request.user)
    bills =Vendor_Credits_Bills.objects.filter(user = request.user).order_by('-vendor_name')

    rbill=Vendor_Credits_Bills.objects.get(user = request.user, id= id)
    billitem = Vendor_Credits_Bills_items_bills.objects.filter(user = request.user,recur_bills=id)

    comp_state = company.state
    # cust = customer.objects.get(id = rbill.customer_name.split(" ")[0])
    vend = vendor_table.objects.get(id = rbill.company_name.split(" ")[0])
    gst_or_igst = "GST" if comp_state == rbill.source_supply else "IGST"


    tax_total = 0 
    for b in billitem:
        tax_total += b.tax

    context = {
                'company' : company,
                'recur_bills' : bills,
                'recur_bill' : rbill,
                'bill_item' : billitem,
                'tax' : tax_total,
                "gst_or_igst" : gst_or_igst,
                # 'customer' : cust,
                'vendor' : vend,
            }
    return render(request,'view_vendor_credits.html',context)
    
    
@login_required(login_url='login')
def delete_vendor_credits(request, id):

    company = company_details.objects.get(user = request.user)
    rbill=Vendor_Credits_Bills.objects.get(user = request.user, id= id)
    billitem = Vendor_Credits_Bills_items_bills.objects.filter(user = request.user,recur_bills=id)

    rbill.delete() 
    billitem.delete() 
     
    return redirect('vendor_credits_home')
    
def add_vendor_credits(request):
    company = company_details.objects.get(user = request.user)
    vendor=vendor_table.objects.all()
    cust=customer.objects.filter(user = request.user)
    payment=payment_terms.objects.all()
    item=AddItem.objects.all()
    account=Account.objects.all()
    unit=Unit.objects.all()
    sales=Sales.objects.all()
    purchase=Purchase.objects.all()
    context={
        'company' : company,
        'vendor':vendor,
        'customer':cust,
        'payment':payment,
        'item':item,
        'account':account,
        'units':unit,
        'sales':sales,
        'purchase':purchase,
        
    }
        
    return render(request,'create_vendor_credits.html',context)
    
    
@login_required(login_url='login')
def create_vendor_credit(request):

    company = company_details.objects.get(user = request.user)
    if request.method == 'POST':
        typ=request.POST.get('option')
        vname = request.POST.get('vendor')
        vmail = request.POST.get('email_inp')
        vgst_t = request.POST.get('gst_trt_inp')
        vgst_n = request.POST.get('gstin_inp')
        vaddress = request.POST.get('address_inp')
        
        credit_note = request.POST.get('credit_note')
        order_no = request.POST.get('order_number')
        vendor_date = request.POST.get('credit_date')

        src_supply = request.POST.get('srcofsupply')
     
        sub_total =request.POST['subtotal']
        sgst=request.POST['sgst']
        cgst=request.POST['cgst']
        igst=request.POST['igst']
        tax = request.POST['total_taxamount']
        adjustment= request.POST['shipping_charge']
        # adjustment=request.POST['adjustment_charge']
        grand_total=request.POST['grandtotal']
        note=request.POST['customer_note']
      
        u = User.objects.get(id = request.user.id)
        print('yes')
        print(typ)
        if typ=='Organization':
           

            purchase = Vendor_Credits_Bills(vendor_name=vname,
                                    vendor_email=vmail,
                                    gst_treatment=vgst_t,
                                    gst_number=vgst_n,
                                    address=vaddress,
                                        
                                    vendor_date=vendor_date,
                                    order_no=order_no,
                                    credit_note=credit_note,
                             
                                    source_supply=src_supply,
                                      
                                    sub_total=sub_total,
                                    sgst=sgst,
                                    cgst=cgst,
                                    igst=igst,
                                    tax_amount=tax,
                                     
                                    adjustment=adjustment,
                                    grand_total=grand_total,
                                    note=note,
                                   
                                    company=company,
                                    user = u )
            purchase.save()

            p_bill = Vendor_Credits_Bills.objects.get(id=purchase.id)

            if len(request.FILES) != 0:
                p_bill.document=request.FILES['file'] 
                p_bill.save()
                print('save')
        else:
            purchase = Vendor_Credits_Bills(vendor_name=vname,
                                    vendor_email=vmail,
                                    gst_treatment=vgst_t,
                                    gst_number=vgst_n,
                                    address=vaddress,
                                        
                                    vendor_date=vendor_date,
                                    order_no=order_no,
                                    credit_note=credit_note,
                              
                                    source_supply=src_supply,
                                  
                                    sub_total=sub_total,
                                    sgst=sgst,
                                    cgst=cgst,
                                    igst=igst,
                                    tax_amount=tax,
                                    
                                    adjustment=adjustment,
                                    grand_total=grand_total,
                                    note=note,
                                        # term=terms_con,
                                    company=company,
                                    user = u)
            purchase.save()

            p_bill = Vendor_Credits_Bills.objects.get(id=purchase.id)

        
            if len(request.FILES) != 0:
                p_bill.document=request.FILES['file'] 
                p_bill.save()
                print('save')
            item = request.POST.getlist("item[]")
            accounts = request.POST.getlist("account[]")
            hsn = request.POST.getlist("hsn[]")
            quantity = request.POST.getlist("quantity[]")
            rate = request.POST.getlist("rate[]")
            tax = request.POST.getlist("tax[]")
            discount = request.POST.getlist("discount[]")
            amount = request.POST.getlist("amount[]")
            if len(item) == len(accounts) == len(hsn) == len(quantity) == len(rate) == len(discount) == len(tax) == len(amount):
                for i in range(len(item)):
                    created = Vendor_Credits_Bills_items_bills.objects.create(
                        item=item[i],
                        account=accounts[i],
                        
                        hsn=hsn[i],
                        quantity=quantity[i],
                        rate=rate[i],
                        tax=tax[i],
                        discount=discount[i],
                        amount=amount[i],
                        user=u,
                        company=company,
                        recur_bills=p_bill
                    )
                print('Done')

        return redirect('vendor_credits_home')
    return render(request,'create_vendor_credits.html')
    
    
def change_vendor_credits(request,id):

    company = company_details.objects.get(user = request.user)
    po_id=Vendor_Credits_Bills.objects.get(id=id)
    if request.method == 'POST':
    
        po_id.vendor_name = request.POST.get('vendor')
        po_id.vendor_mail = request.POST.get('email_inp')
        po_id.vendor_gst_traet = request.POST.get('gst_trt_inp')
        po_id.vendor_gst_no = request.POST.get('gstin_inp')
            
        po_id.vaddress = request.POST.get('address_inp')       
        po_id.credit_note = request.POST.get('credit_note')
        po_id.order_no = request.POST.get('order_number')
        po_id.vendor_date = request.POST.get('credit_date')

        po_id.source_supply = request.POST.get('srcofsupply')

        po_id.sub_total =request.POST['subtotal']
        po_id.sgst=request.POST['sgst']
        po_id.cgst=request.POST['cgst']
        po_id.igst=request.POST['igst']
        po_id.tax_amount = request.POST['total_taxamount']
        po_id.grand_total=request.POST['grandtotal']
        po_id.note=request.POST['customer_note']
        # po_id.adjustment=request.POST['add_round_off']
        po_id.adjustment=request.POST['shipping_charge']
        
        u = User.objects.get(id = request.user.id)

            
        po_id.save()

        p_bill = Vendor_Credits_Bills.objects.get(id=po_id.id)

        if len(request.FILES) != 0:
            p_bill.document=request.FILES['file'] 
            p_bill.save()
            print('save')
    else:
        po_id.vendor_name = request.POST.get('vendor')
        po_id.vendor_mail = request.POST.get('email_inp')
        po_id.vendor_gst_traet = request.POST.get('gst_trt_inp')
        po_id.vendor_gst_no = request.POST.get('gstin_inp')
            
        po_id.vaddress = request.POST.get('address_inp')       
        po_id.credit_note = request.POST.get('credit_note')
        po_id.order_no = request.POST.get('order_number')
        po_id.vendor_date = request.POST.get('credit_date')
        po_id.source_supply = request.POST.get('srcofsupply')
        po_id.sub_total =request.POST['subtotal']
        po_id.sgst=request.POST['sgst']
        po_id.cgst=request.POST['cgst']
        po_id.igst=request.POST['igst']
        po_id.tax_amount = request.POST['total_taxamount']
        po_id.grand_total=request.POST['grandtotal']
        po_id.note=request.POST['customer_note']
        # po_id.adjustment=request.POST['add_round_off']
        po_id.adjustment=request.POST['shipping_charge']
            
        u = User.objects.get(id = request.user.id)

            
        po_id.save()

        p_bill = Vendor_Credits_Bills.objects.get(id=po_id.id)

    if request.FILES.get('file') is not None:
        po_id.file = request.FILES['file']
    else:
        po_id.file = "/static/images/default.jpg"
    po_id.save()
    item = request.POST.getlist("item[]")
    accounts = request.POST.getlist("account[]")
    hsn = request.POST.getlist("hsn[]")
    quantity = request.POST.getlist("quantity[]")
    rate = request.POST.getlist("rate[]")
    tax = request.POST.getlist("tax[]")
    discount = request.POST.getlist("discount[]")
    amount = request.POST.getlist("amount[]")

    obj_dele = Vendor_Credits_Bills_items_bills.objects.filter(recur_bills=p_bill.id)
    obj_dele.delete()

    if len(item) == len(accounts) == len(hsn) == len(quantity) == len(rate) == len(discount) == len(tax) == len(amount):
        for i in range(len(item)):
            created = Vendor_Credits_Bills_items_bills.objects.create(
                item=item[i],
                account=accounts[i],
                hsn=hsn[i],
                quantity=quantity[i],
                rate=rate[i],
                tax=tax[i],
                discount=discount[i],
                amount=amount[i],
                user=u,
                company=company,
                recur_bills=p_bill
            )

            print('Done')

        return redirect('view_vendor_credits',id)
    return redirect('vendor_credits_home')
    
    
@login_required(login_url='login')
def vendor_credits_pay(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        name=request.POST.get('name')
        days=request.POST.get('days')
        
        u = User.objects.get(id = request.user.id)

        pay = payment_terms(Terms=name, Days=days, user = u)
        pay.save()

        return HttpResponse({"message": "success"})
    
@login_required(login_url='login')
def vendor_credits_pay_dropdown(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = payment_terms.objects.filter(user = user)
    for option in option_objects:
        options[option.id] = option.Terms + str(option.Days)

    return JsonResponse(options)

@login_required(login_url='login')
def vendor_credits_unit(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        unit =request.POST.get('unit')
        
        u = User.objects.get(id = request.user.id)

        unit = Unit(unit= unit)
        unit.save()

        return HttpResponse({"message": "success"})
        
@login_required(login_url='login')        
def vendor_credits_unit_dropdown(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = Unit.objects.all()
    for option in option_objects:
        options[option.id] = option.unit

    return JsonResponse(options)

@login_required(login_url='login')    
def vendor_credits_account(request):

    company = company_details.objects.get(user = request.user)


    if request.method=='POST':
        type=request.POST.get('actype')
        name=request.POST['acname']
        u = User.objects.get(id = request.user.id)

        acnt=Account(accountType=type,accountName=name,user = u)

        acnt.save()

        return HttpResponse({"message": "success"})
        

@login_required(login_url='login')
def vendor_credits_account_dropdown(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = Account.objects.filter(user = user)
    for option in option_objects:
        options[option.id] = option.accountName

    return JsonResponse(options)

def export_vendor_credit_pdf(request,id):

    user = request.user
    company = company_details.objects.get(user=user)
    challn_on = Vendor_Credits_Bills.objects.filter(user=user)
    challan = Vendor_Credits_Bills.objects.get(id=id)
    items = Vendor_Credits_Bills_items_bills.objects.filter(PO=challan)
    print(challan.customer_name) 
    print(challan.customer_name)
    total = challan.grand_total

    template_path = 'pdfchallan.html'
    context = {
        'company': company,
        'pot':challn_on,
        'po_item': challan,
        'po_table': items, 
    }
    fname=challan.Pur_no
   
    # Create a Django response object, and specify content_type as pdftemp_creditnote
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'
    response['Content-Disposition'] =f'attachment; filename= {fname}.pdf'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    


    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
    
def itemdata_vendor_credit(request):
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)
    company = company_details.objects.get(user=user)
    print(company.state)
    id = request.GET.get('id')
    

    

    item = AddItem.objects.get(Name=id, user=user)
    name=item.Name
    rate = item.p_price
    hsn = item.hsn
    place = company.state

    return JsonResponse({"status": " not", 'place': place, 'rate': rate, 'hsn': hsn})
    return redirect('/')
    
    
@login_required(login_url='login')
def vendor_credit_vendor(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        title=request.POST.get('title')
        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')
        comp=request.POST.get('company_name')
        dispn = request.POST.get('display_name')
        email=request.POST.get('email')
        website=request.POST.get('website')
        w_mobile=request.POST.get('work_mobile')
        p_mobile=request.POST.get('pers_mobile')
        skype = request.POST.get('skype')
        desg = request.POST.get('desg')
        dpt = request.POST.get('dpt')
        gsttype=request.POST.get('gsttype')
        gstin=request.POST.get('gstin')
        panno=request.POST.get('panno')
        supply=request.POST.get('sourceofsupply')
        currency=request.POST.get('currency')
        balance=request.POST.get('openingbalance')
        payment=request.POST.get('paymentterms')
        street=request.POST.get('street')
        city=request.POST.get('city')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
        country=request.POST.get('country')
        fax=request.POST.get('fax')
        phone=request.POST.get('phone')
        shipstreet=request.POST.get('shipstreet')
        shipcity=request.POST.get('shipcity')
        shipstate=request.POST.get('shipstate')
        shippincode=request.POST.get('shippincode')
        shipcountry=request.POST.get('shipcountry')
        shipfax=request.POST.get('shipfax')
        shipphone=request.POST.get('shipphone')

        u = User.objects.get(id = request.user.id)

        vndr = vendor_table(salutation=title, first_name=first_name, last_name=last_name,vendor_display_name = dispn, company_name= comp, gst_treatment=gsttype, gst_number=gstin, 
                    pan_number=panno,vendor_wphone = w_mobile,vendor_mphone = p_mobile, vendor_email=email,skype_number = skype,
                    source_supply=supply,currency=currency, website=website, designation = desg, department = dpt,
                    opening_bal=balance,baddress=street, bcity=city, bstate=state, payment_terms=payment,bzip=pincode, 
                    bcountry=country, saddress=shipstreet, scity=shipcity, sstate=shipstate,szip=shippincode, scountry=shipcountry,
                    bfax = fax, sfax = shipfax, bphone = phone, sphone = shipphone,user = u)
        vndr.save()

        return HttpResponse({"message": "success"})
        
        
############### BALANCE SHEET ################## 
def load_balance_sheet(request):
    company = company_details.objects.get(user = request.user.id)
    return render(request,'balance_sheet.html', {"company":company})
    
def load_customize_report_bs(request):
    company = company_details.objects.get(user = request.user.id)
    return render(request,'customize_report_bs.html', {"range":range(2,24),"company":company})
    
def update_balancesheet(request):
    if request.method=='POST':
        newdate= request.POST.get('newdate', False)
        company = company_details.objects.get(user = request.user.id)
        return render(request,'balance_sheet.html', {"company":company,"newdate":newdate,"valid":1})
    
############### HORIZONTAL BALANCE SHEET ################## 
def load_horizontal_balance_sheet(request):
    company = company_details.objects.get(user = request.user.id)
    return render(request,'horizontal_balance_sheet.html', {"company":company})
    
def load_customize_report_hbs(request):
    company = company_details.objects.get(user = request.user.id)
    return render(request,'customize_report_hbs.html',{"company":company})
    
def update_hbalancesheet(request):
    if request.method=='POST':
        newdate= request.POST.get('newdate', False)
        company = company_details.objects.get(user = request.user.id)
        return render(request,'horizontal_balance_sheet.html', {"company":company,"newdate":newdate})
    
def party_statement(request):
    cust=customer.objects.all()
    company = company_details.objects.get(user=request.user)
    vendor=vendor_table.objects.all()
    context={
        "customer":cust,
        "company":company,
        "vendor":vendor

    }
    return render(request,"party_statement.html",context)

def get_transactions(request):
    party = request.GET.get('party')
    st_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    st_date = datetime.strptime(st_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    estimates = Estimates.objects.filter(customer__customerName=party,estimate_date__range=(st_date, end_date))
    estimates_list = [ {'date': estimate.estimate_date,'transaction': "Estimate",'reference': estimate.reference,}
        for estimate in estimates
    ]
    re_invoice=RetainerInvoice.objects.filter(customer_name__customerName=party,retainer_invoice_date__range=(st_date, end_date))
    re_inv_list = [ {'date': re_invo.retainer_invoice_date,'transaction': "Retainer Invoice",'reference': re_invo.refrences,"total":re_invo.total_amount}
        for re_invo in re_invoice
    ]
    sales_order=SalesOrder.objects.filter(customer__customerName=party,sales_date__range=(st_date, end_date))
    sales_list = [ {'date': sale.sales_date,'transaction': "Sales order",'reference': sale.reference,"total":sale.grandtotal}
        for sale in sales_order
    ]
    del_chel=DeliveryChellan.objects.filter(customer_name=party,chellan_date__range=(st_date, end_date))
    del_chel_list=[ {'date': chel.chellan_date,'transaction': "Delivery Chellan",'reference': chel.reference,"total":chel.total}
        for chel in del_chel
    ]
    invo=invoice.objects.filter(customer__customerName=party,inv_date__range=(st_date, end_date))
    inv_list=[ {'date': inv.inv_date,'transaction': "Invoice",'reference': "","total":inv.grandtotal}
        for inv in invo
    ]
    rec_inv=recurring_invoice.objects.filter(cname=party,start__range=(st_date, end_date))
    recinv_list=[ {'date': recinv.start,'transaction': "Recurring Invoice",'reference':"", "total":recinv.total,}
        for recinv in rec_inv
    ]
    sale_lists=re_inv_list+sales_list+del_chel_list+inv_list+recinv_list
    sale_total=0.0
    for i in sale_lists:
        sale_total=sale_total+float(i["total"])    

    expense=ExpenseE.objects.filter(Q(vendor__vendor_display_name=party) |Q(customer_name__customerName=party),date__range=(st_date, end_date))
    expense_list=[ {'date': exp.date,'transaction': "Expense",'reference': "",}
        for exp in expense
    ]
    
    re_expense=Expense.objects.filter(Q(vendor__vendor_display_name=party) |Q(customername=party),start_date__range=(st_date, end_date))
    reexpense_list=[ {'date': exp.start_date,'transaction': "Reccuring Expense",'reference': "",}
        for exp in re_expense
    ]
   
    pur_order=Purchase_Order.objects.filter(Q(vendor_name__icontains=party)|Q(customer_name=party),Ord_date__range=(st_date, end_date))
    pur_list=[ {'date':pur.Ord_date,'transaction': "Purchase Order",'reference': pur.ref,"total":pur.grand_total}
        for pur in pur_order
    ]
    pay_made=payment_made.objects.filter(vendor__vendor_display_name=party,date__range=(st_date, end_date))
    pay_list=[ {'date':pay.date,'transaction': "payment made",'reference': pay.reference,"total":pay.amount}
        for pay in pay_made
    ]
    pur_bills=PurchaseBills.objects.filter( Q(vendor_name=party) | Q(customer_name=party),
    bill_date__range=(st_date, end_date))
    pur_bill_list=[ {'date':bill.bill_date,'transaction': "Bill",'reference': "","total":bill.total}
        for bill in pur_bills
    ]
    re_pur_bill=recurring_bills.objects.filter(Q(vendor_name__icontains=party) | Q(customer_name__icontains=party),start_date__range=(st_date, end_date))
    re_pur_bill_list=[ {'date':re_bill.start_date,'transaction': "Recurring Bill",'reference': " ","total":re_bill.grand_total}
        for re_bill in re_pur_bill
    ]

    vend_credits=Vendor_Credits_Bills.objects.filter(vendor_name__icontains=" ".join(party.split()[1:]),vendor_date__range=(st_date, end_date))
    vend_credit_list=[ {'date':vend.vendor_date,'transaction': "Vendor Credits",'reference': " ","total":vend.grand_total}
        for vend in vend_credits
    ]
    purchase_list=pur_list+pay_list+pur_bill_list+re_pur_bill_list
    pur_total=0.0
    for i in purchase_list:
        pur_total+=float(i["total"])   
    return JsonResponse({"transactions": re_inv_list+estimates_list+sales_list+
                         del_chel_list+inv_list+recinv_list+expense_list+pur_list+pay_list
                         +pur_bill_list+re_pur_bill_list+reexpense_list+vend_credit_list,
                         "sale_total":sale_total,"pur_total":pur_total})


def all_parties(request):
    custom=customer.objects.all()
    vend=vendor_table.objects.all()
    company = company_details.objects.get(user=request.user)
    return render(request,'all_parties.html',{"cust":custom,"vendor":vend, "company":company,})
    
def purchasebyitem(request):
    user=request.user
    customer1 = customer.objects.filter(user=user)
    company_data = company_details.objects.get(user=request.user)
    bills = PurchaseBillItems.objects.all()
    return render(request,'purchases_by_item.html',{'cust': customer1, 'company': company_data,'bills':bills})

def customize_report_purchasebyitem(request):
    user=request.user
    vendor=vendor_table.objects.all()
    company_data = company_details.objects.get(user=request.user)
    bills = PurchaseBillItems.objects.all()
    return render(request,'customize_report_purchasebyitem.html',{'vendors':vendor,'company': company_data,'bills':bills})
   
def purchasebyvendor(request):
    customer1 = customer.objects.all()
    company_data = company_details.objects.get(user=request.user)
    vendor=vendor_table.objects.all()
    return render(request,'purchases_by_vendor.html',{'cust': customer1, 'company': company_data,'vendors':vendor})


def customize_vendor_report(request):
    vendor=vendor_table.objects.all()
    company_data = company_details.objects.get(user=request.user)
    return render(request,'customize_report_vendor.html',{'vendors':vendor,'company': company_data})
    
def ewaylistout(request):
     proj=EWayBill.objects.filter(user=request.user)
     custom=customer.objects.all()
     company=company_details.objects.get(user=request.user)
     return render(request,'ewaylistout.html',{'proj':proj,'custom':custom,'company':company})
     
def ewaycreate(request):
     user_id=request.user.id
     udata=User.objects.get(id=user_id)
     user=request.user
     data=customer.objects.filter(user_id=user.id)
     payments=payment_terms.objects.all()
     trans=Transportation.objects.all()
     units = Unit.objects.all()
     sales=Sales.objects.all()
     purchase=Purchase.objects.all()
     sales_type = set(Sales.objects.values_list('Account_type', flat=True))
     purchase_type = set(Purchase.objects.values_list('Account_type', flat=True))
     item = AddItem.objects.filter(user = request.user)
     company=company_details.objects.get(user=request.user)
     return render(request,'ewaycreate.html',{'data':data,'payments':payments,'trans':trans,'units':units,'sales':sales,'purchase':purchase,'sales_type':sales_type,'purchase_type':purchase_type,'item':item,'company':company})
     
def ewayb_customer(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        # title=request.POST.get('title')
        # first_name=request.POST.get('firstname')
        # last_name=request.POST.get('lastname')
        # comp=request.POST.get('company_name')
        cust_type = request.POST.get('customer_type')
        name = request.POST.get('display_name')
        comp_name = request.POST.get('company_name')
        email=request.POST.get('email')
        website=request.POST.get('website')
        w_mobile=request.POST.get('work_mobile')
        p_mobile=request.POST.get('pers_mobile')
        fb = request.POST.get('facebook')
        twitter = request.POST.get('twitter')
        skype = request.POST.get('skype')
        desg = request.POST.get('desg')
        dpt = request.POST.get('dpt')
        gsttype=request.POST.get('gsttype')
        # gstin=request.POST.get('gstin')
        # panno=request.POST.get('panno')
        supply=request.POST.get('placeofsupply')
        tax = request.POST.get('tax_preference')
        currency=request.POST.get('currency')
        balance=request.POST.get('openingbalance')
        payment=request.POST.get('paymentterms')
        street1=request.POST.get('street1')
        street2=request.POST.get('street2')
        city=request.POST.get('city')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
        country=request.POST.get('country')
        fax=request.POST.get('fax')
        phone=request.POST.get('phone')
        # shipstreet1=request.POST.get('shipstreet1')
        # shipstreet2=request.POST.get('shipstreet2')
        # shipcity=request.POST.get('shipcity')
        # shipstate=request.POST.get('shipstate')
        # shippincode=request.POST.get('shippincode')
        # shipcountry=request.POST.get('shipcountry')
        # shipfax=request.POST.get('shipfax')
        # shipphone=request.POST.get('shipphone')

        u = User.objects.get(id = request.user.id)

        cust = customer(customerName = name,customerType = cust_type, companyName= comp_name, GSTTreatment=gsttype, 
                        customerWorkPhone = w_mobile,customerMobile = p_mobile, customerEmail=email,skype = skype,Facebook = fb, 
                        Twitter = twitter,placeofsupply=supply,Taxpreference = tax,currency=currency, website=website, 
                        designation = desg, department = dpt,OpeningBalance=balance,Address1=street1,Address2=street2, city=city, 
                        state=state, PaymentTerms=payment,zipcode=pincode,country=country,  fax = fax,  phone1 = phone,user = u)
        cust.save()

        return HttpResponse({"message": "success"})
        
def customer_dropdown_ewayb(request):
    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = customer.objects.filter(user = user)
    for option in option_objects:
        options[option.id] = [option.id , option.customerName]

    return JsonResponse(options) 
    
def recurbills_pay_eway(request):
    if request.method == 'POST':
        # Extract the data from the POST request
        name = request.POST.get('name')
        days = request.POST.get('days')

        # Create a new payment_terms object and save it to the database
        payment_term = payment_terms(Terms=name, Days=days)
        payment_term.save()

        # Return a JSON response indicating success
        return JsonResponse({"message": "success"})
        
def add_transportation(request):
    if request.method == 'POST':
        transportation_method = request.POST.get('method')
        if transportation_method:
            transportation = Transportation(method=transportation_method)
            transportation.save()
            return JsonResponse({'message': 'Transportation added successfully.'})
        else:
            return JsonResponse({'message': 'Transportation method is required.'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=405) 
        
        
def ewaybills_item(request):

    company = company_details.objects.get(user = request.user)

    if request.method=='POST':
        
        type=request.POST.get('type')
        name=request.POST.get('name')
        ut=request.POST.get('unit')
        inter=request.POST.get('inter')
        intra=request.POST.get('intra')
        sell_price=request.POST.get('sell_price')
        sell_acc=request.POST.get('sell_acc')
        sell_desc=request.POST.get('sell_desc')
        cost_price=request.POST.get('cost_price')
        cost_acc=request.POST.get('cost_acc')      
        cost_desc=request.POST.get('cost_desc')
        
        units=Unit.objects.get(id=ut)
        sel=Sales.objects.get(id=sell_acc)
        cost=Purchase.objects.get(id=cost_acc)

        history="Created by " + str(request.user)

        u  = User.objects.get(id = request.user.id)

        item=AddItem(type=type,Name=name,p_desc=cost_desc,s_desc=sell_desc,s_price=sell_price,p_price=cost_price,
                     user=u ,creat=history,interstate=inter,intrastate=intra,unit = units,sales = sel, purchase = cost)

        item.save()

        return HttpResponse({"message": "success"})
    
    return HttpResponse("Invalid request method.")
    
    
def eway_item_dropdown(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = AddItem.objects.filter(user = request.user)
    for option in option_objects:
        options[option.id] = [option.Name,option.id]

    return JsonResponse(options)
    
    
def eway_unit(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        unit =request.POST.get('unit')
        
        u = User.objects.get(id = request.user.id)

        unit = Unit(unit= unit)
        unit.save()

        return HttpResponse({"message": "success"})
        
def eway_unit_dropdown(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = Unit.objects.all()
    for option in option_objects:
        options[option.id] = [option.unit,option.id]

    return JsonResponse(options)
    
    
def unit_get_rate(request):

    user = User.objects.get(id=request.user.id)
    if request.method=='POST':
        id=request.POST.get('id')

        item = AddItem.objects.get( id = id, user = user)
         
        rate = 0 if item.s_price == "" else item.s_price

        return JsonResponse({"rate": rate},safe=False)  
        
        
def create_ewaybillz(request):
    
    
    if request.method == 'POST':
        user_id=request.user.id
        user=User.objects.get(id=user_id)

        doc = request.POST.get('doc')
        transsub = request.POST.get('transsub')
        customerzz = request.POST.get('customerzz')
        cemail= request.POST.get('cemail')
        cgst_trt_inp = request.POST.get('cgst_trt_inp')
        cgstin_inp = request.POST.get('cgstin_inp')
        invoiceno = request.POST.get('invoiceno')
        date = request.POST.get('date')
        trans = request.POST.get('trans')
        adda = request.POST.get('adda')
        addb = request.POST.get('addb')
        srcofsupply = request.POST.get('srcofsupply')
        transportation = request.POST.get('transportation')
        km = request.POST.get('km')
        vno = request.POST.get('vno')
        
        sub_total =request.POST['subtotal']
        sgst=request.POST['sgst']
        cgst=request.POST['cgst']
        igst=request.POST['igst']
        tax = request.POST['total_taxamount']
        shipping_charge= request.POST['shipping_charge']
        adj= request.POST['adj']
        grand_total=request.POST['grandtotal']
        note=request.POST['note']
        cat = customer.objects.get(id=customerzz)
        eway_bill = EWayBill.objects.create(
            
            doc=doc,
            transsub=transsub,
            customerzz=customerzz,
            cemail=cemail,
            cgst_trt_inp=cgst_trt_inp,
            cgstin_inp=cgstin_inp,
            invoiceno=invoiceno,
            date=date,
            trans=trans,
            adda=adda,
            addb=addb,
            srcofsupply=srcofsupply,
            transportation=transportation,
            km=km,
            vno=vno,
            note=note,
            grand_total=grand_total,
            adj=adj,
            shipping_charge=shipping_charge,
            tax=tax,
            igst=igst,
            cgst=cgst,
            sgst=sgst,
            sub_total=sub_total,
            user=user,
            cust=cat,
        )

        items = request.POST.getlist("item[]")
        quantities = request.POST.getlist("quantity[]")
        rates = request.POST.getlist("rate[]")
        taxes = request.POST.getlist("tax[]")
        discounts = request.POST.getlist("discount[]")
        amounts = request.POST.getlist("amount[]")
        
        if len(items) == len(quantities) == len(rates) == len(discounts) == len(taxes) == len(amounts):
            for i in range(len(items)):
                EWayBillItem.objects.create(
                    eway_bill=eway_bill,
                    item=items[i],
                    quantity=quantities[i],
                    rate=rates[i],
                    tax=taxes[i],
                    discount=discounts[i],
                    amount=amounts[i],
                )

            return redirect('ewaylistout')
    
    return render(request, 'ewaycreate.html')
    
def ewayoverview(request,id):
    eway=EWayBill.objects.filter(user=request.user)
    ewayi=EWayBill.objects.filter(id=id)
    company=company_details.objects.get(user=request.user)
    ewayb = EWayBillItem.objects.filter(eway_bill_id=id)  # Fetch items related to the EWayBill id
    projc = get_object_or_404(EWayBill, id=id)
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        if comment_text:
            projc.comment = comment_text  # Set the comment field of the specific project object
            projc.save()  # Save the project object with the updated comment
    return render(request, 'ewayoverview.html',{'eway':eway,"ewayi":ewayi,'ewayb':ewayb,'projc':projc,'company':company})
    
    
def delete_ewaybills(request, id):

    
    ebill=EWayBill.objects.get(user = request.user, id= id)
    billway = EWayBill.objects.filter(user = request.user,id=id)

    ebill.delete() 
    billway.delete() 
     
    return redirect('ewaylistout')
    
def ewayedit(request,id):
     user_id=request.user.id
     udata=User.objects.get(id=user_id)
     user = request.user
     data = customer.objects.filter(user_id=user.id)
     payments=payment_terms.objects.all()
     trans=Transportation.objects.all()
     units = Unit.objects.all()
     sales=Sales.objects.all()
     purchase=Purchase.objects.all()
     sales_type = set(Sales.objects.values_list('Account_type', flat=True))
     purchase_type = set(Purchase.objects.values_list('Account_type', flat=True))
     item = AddItem.objects.filter(user = request.user)
     eway=EWayBill.objects.get(id=id)
     ewayi=EWayBill.objects.filter(id=id)
     ewayb=EWayBillItem.objects.filter(eway_bill_id=id)
     company=company_details.objects.get(user=request.user)
     return render(request,'ewayedit.html',{'data':data,'payments':payments,'trans':trans,'units':units,'sales':sales,'purchase':purchase,'sales_type':sales_type,'purchase_type':purchase_type,'item':item,'eway':eway,'ewayb':ewayb,'ewayi':ewayi,'company':company})
     

def ewaybill_comment(request):

    company = company_details.objects.get(user = request.user)

    if request.method=='POST':
        id =request.POST.get('id')
        cmnt =request.POST.get('comment')
        
        u = User.objects.get(id = request.user.id)
        e_bill = EWayBill.objects.get(user = request.user, id = id)
        e_bill.comments = cmnt
        e_bill.save()

        return HttpResponse({"message": "success"})
        
        
def ewayeditdb(request, id):
    eway = get_object_or_404(EWayBill, id=id)

    if request.method == 'POST':
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        # Update EWayBill fields
        eway.doc = request.POST.get('doc')
        eway.transsub = request.POST.get('transsub')
        customerzz = request.POST.get('customerzz')
        custz=customer.objects.get(id=customerzz)
        eway.customerzz=custz.customerName
        eway.cust=custz
        print(request.POST.get('customerzz'))
        eway.cemail = request.POST.get('cemail')
        eway.cgst_trt_inp = request.POST.get('cgst_trt_inp')
        eway.cgstin_inp = request.POST.get('cgstin_inp')
        eway.invoiceno = request.POST.get('invoiceno')
        eway.date = request.POST.get('date')
        eway.trans = request.POST.get('trans')
        eway.adda = request.POST.get('adda')
        eway.addb = request.POST.get('addb')
        eway.srcofsupply = request.POST.get('srcofsupply')
        eway.transportation = request.POST.get('transportation')
        eway.km = request.POST.get('km')
        eway.vno = request.POST.get('vno')
        eway.sub_total = request.POST['subtotal']
        eway.sgst = request.POST['sgst']
        eway.cgst = request.POST['cgst']
        eway.igst = request.POST['igst']
        eway.tax = request.POST['total_taxamount']
        eway.shipping_charge = request.POST['shipping_charge']
        eway.adj = request.POST['adj']
        eway.grand_total = request.POST['grandtotal']
        eway.note = request.POST['note']
        eway.save()
        print("test")
        # Delete existing EWayBillItems associated with this EWayBill
        EWayBillItem.objects.filter(eway_bill=eway).delete()

        # Update EWayBillItems
        items = request.POST.getlist("item[]")
        quantities = request.POST.getlist("quantity[]")
        rates = request.POST.getlist("rate[]")
        taxes = request.POST.getlist("tax[]")
        discounts = request.POST.getlist("discount[]")
        amounts = request.POST.getlist("amount[]")

        if len(items) == len(quantities) == len(rates) == len(discounts) == len(taxes) == len(amounts):
            for i in range(len(items)):
                EWayBillItem.objects.create(
                    eway_bill=eway,
                    item=items[i],
                    quantity=quantities[i],
                    rate=rates[i],
                    tax=taxes[i],
                    discount=discounts[i],
                    amount=amounts[i],
                )

            return redirect('ewayoverview' ,id=id)

    return render(request, 'ewayedit.html', {'eway': eway})
    
def ewaycommentdb(request, id):
    projc = get_object_or_404(EWayBill, id=id)

    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        if comment_text:
            if projc.comment:
                projc.comment += "\n" + comment_text  # Add new comment to existing comments
            else:
                projc.comment = comment_text  # If no comments exist, set it as the first comment
            projc.save()

    return redirect('ewayoverview', id=id)
    
def get_transportation_options(request):
    transportation_options = Transportation.objects.all().values_list('method', flat=True)
    options_list = list(transportation_options)
    return JsonResponse({'options': options_list})
    
def filter_invoice_draft(request):
    user = request.user
    invo=invoice.objects.filter(status='draft',user=user)
    return render(request, 'invoiceview.html', {'invoice':invo})
    
def filter_invoice_sent(request):
    user = request.user
    invo=invoice.objects.filter(status='send',user=user)
    return render(request, 'invoiceview.html', {'invoice':invo})
    
def add_invoice_comment(request,pk):
    if request.method=="POST":
        user=request.user      
        inv=invoice.objects.get(id=pk)
       
        comment=invoice_comments()
        comment.user=user
        comment.invoice=inv
        comment.comments=request.POST.get('comments')
        comment.save()
    return redirect('detailedview',inv.id)
    
def filter_inv_det_send(request,id):
    user=request.user
    inv_dat=invoice.objects.filter(user=user,status="send")
    inv_master=invoice.objects.get(id=id)
    invoiceitem=invoice_item.objects.filter(inv_id=id)
    company=company_details.objects.get(user_id=request.user.id)
    
    
    context={
        'inv_dat':inv_dat,
        'invoiceitem':invoiceitem,
        'comp':company,
        'invoice':inv_master,
    }
    return render(request,'invoice_det.html',context)
    
def filter_inv_det_draft(request,id):
    user=request.user
    inv_dat=invoice.objects.filter(user=user,status="draft")
    inv_master=invoice.objects.get(id=id)
    invoiceitem=invoice_item.objects.filter(inv_id=id)
    company=company_details.objects.get(user_id=request.user.id)
    
    
    context={
        'inv_dat':inv_dat,
        'invoiceitem':invoiceitem,
        'comp':company,
        'invoice':inv_master,
    }
    return render(request,'invoice_det.html',context)
    
def filter_retainer_draft(request):
    user = request.user
    invoices=RetainerInvoice.objects.filter(is_draft=1)
    return render(request, 'retainer_invoice.html', {'invoices':invoices})
    
def filter_retainer_sent(request):
    user = request.user
    invoices=RetainerInvoice.objects.filter(is_draft=0,is_sent=1)
    return render(request, 'retainer_invoice.html', {'invoices':invoices})
    
def filter_retainer_view_draft(request,pk):
    invoices=RetainerInvoice.objects.filter(is_draft=1)
    invoice=RetainerInvoice.objects.get(id=pk)
    item=Retaineritems.objects.filter(retainer=pk)

    context={'invoices':invoices,'invoice':invoice,'item':item}
    return render(request,'invoice_view.html',context)
    
def filter_retainer_view_sent(request,pk):
    invoices=RetainerInvoice.objects.filter(is_sent=1)
    invoice=RetainerInvoice.objects.get(id=pk)
    item=Retaineritems.objects.filter(retainer=pk)

    context={'invoices':invoices,'invoice':invoice,'item':item}
    return render(request,'invoice_view.html',context)
    
def add_ret_invoice_comment(request,pk):
    if request.method=="POST":
        user=request.user      
        invoice=RetainerInvoice.objects.get(id=pk)
       
        comment=retainer_invoice_comments()
        comment.user=user
        comment.retainer=invoice
        comment.comments=request.POST.get('comments')
       
        comment.save()
    return redirect('invoice_view',invoice.id)


def filter_delivery_draft(request):
    user = request.user
    view=DeliveryChellan.objects.filter(status='draft',user=user)
    return render(request,'delivery_chellan.html',{'view':view})
    
def filter_delivery_sent(request):
    user = request.user
    view=DeliveryChellan.objects.filter(status='send',user=user)
    return render(request,'delivery_chellan.html',{'view':view})
    
def filter_by_draft_chellan_view(request,pk):
    user = request.user
    company = company_details.objects.get(user=user)
    all_estimates = DeliveryChellan.objects.filter(user=user,status='draft')
    estimate = DeliveryChellan.objects.get(id=pk)
    items = ChallanItems.objects.filter(chellan=estimate)
    context = {
        'company': company,
        'all_estimates':all_estimates,
        'estimate': estimate,
        'items': items,
    }
    return render(request, 'delivery_challan_view.html', context)
    
def filter_by_sent_chellan_view(request,pk):
    user = request.user
    company = company_details.objects.get(user=user)
    all_estimates = DeliveryChellan.objects.filter(user=user,status='send')
    estimate = DeliveryChellan.objects.get(id=pk)
    items = ChallanItems.objects.filter(chellan=estimate)
    context = {
        'company': company,
        'all_estimates':all_estimates,
        'estimate': estimate,
        'items': items,
    }
    return render(request, 'delivery_challan_view.html', context)

def add_delivery_chellan_comment(request,pk):
    if request.method=="POST":
        user=request.user      
        chellan=DeliveryChellan.objects.get(id=pk)
       
        comment=delivery_chellan_comments()
        comment.user=user
        comment.chellan=chellan
        comment.comments=request.POST.get('comments')
       
        comment.save()
    return redirect('delivery_challan_view',chellan.id)
    
    
def purchase_customer_eway(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            tax=request.POST.get('tax')
            type=request.POST.get('title')
            first=request.POST['firstname']
            last=request.POST['lastname']
            txtFullName= request.POST['display_name']
            
            itemtype=request.POST.get('itemtype')
            cpname=request.POST['company_name']
            
            email=request.POST.get('email')
            wphone=request.POST.get('work_mobile')
            mobile=request.POST.get('pers_mobile')
            skname=request.POST.get('skype')
            desg=request.POST.get('desg')      
            dept=request.POST.get('dpt')
            wbsite=request.POST.get('website')

            gstt=request.POST.get('gsttype')
            gstn=request.POST.get('gstin')
            posply=request.POST.get('placesupply')
            crncy=request.POST.get('currency')
            obal=request.POST.get('openingbalance')

           
            pterms=request.POST.get('paymentterms')

            plst=request.POST.get('plst')
            plang=request.POST.get('plang')
            fbk=request.POST.get('facebook')
            twtr=request.POST.get('twitter')
        
            ctry=request.POST.get('country')
            
            street=request.POST.get('street')
            shipstate=request.POST.get('shipstate')
            shipcity=request.POST.get('shipcity')
            bzip=request.POST.get('shippincode')
            shipfax=request.POST.get('shipfax')

            sal=request.POST.get('title')
            addres=street +','+ shipcity+',' + shipstate+',' + bzip
            adress2=addres
            u = User.objects.get(id = request.user.id)

            print(tax)
            ctmr=customer(customerName=txtFullName,customerType=itemtype,
                        companyName=cpname,customerEmail=email,customerWorkPhone=wphone,
                         customerMobile=mobile,skype=skname,designation=desg,department=dept,
                           website=wbsite,GSTTreatment=gstt,GSTIN=gstn,placeofsupply=posply, Taxpreference=tax,
                             currency=crncy,OpeningBalance=obal,PaymentTerms=pterms,
                                PriceList=plst,PortalLanguage=plang,Facebook=fbk,Twitter=twtr
                                 ,country=ctry,Address1=addres,Address2=adress2,
                                  city=shipcity,state=shipstate,zipcode=bzip,phone1=wphone,
                                   fax=shipfax,CPsalutation=sal,Firstname=first,
                                    Lastname=last,CPemail=email,CPphone=mobile,
                                    CPmobile= wphone,CPskype=skname,CPdesignation=desg,
                                     CPdepartment=dept,user=u )
            ctmr.save()

        return HttpResponse({"message": "success"})
        
        
@login_required(login_url='login')
def get_vendor_list(request):
    user = User.objects.get(id=request.user.id)

    options = []
    option_objects = vendor_table.objects.filter(user=user)
    for option in option_objects:
        vendor_info = {
            'id': option.id,
            'name': f"{option.salutation} {option.first_name} {option.last_name}",
            'gstTreatment': option.gst_treatment,
            'gstnumber':option.gst_number,
        }
        options.append(vendor_info)

    return JsonResponse(options, safe=False)
 # Set safe to False when returning a list
 
def get_vendor_data(request):
    vendor_id = request.GET.get('vendor')
    try:
        vendor = vendor_table.objects.get(id=vendor_id)
        vendor_data = {'gst_treatment': vendor.gst_treatment}
    except vendor_table.DoesNotExist:
        vendor_data = {'error': 'Vendor not found'}
    return JsonResponse(vendor_data)
    
def toggle_expense_status(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    expense.activation_tag = "inactive" if expense.activation_tag == "active" else "active"
    expense.save()
    return JsonResponse({'status': expense.activation_tag})
    
    
@login_required(login_url='login')
def expense_comment(request,expense_id):
   
    expense = get_object_or_404(Expense, id=expense_id) 
    

    if request.method == 'POST':
      
        comment_text = request.POST['comment']

        comment = Comment()
        comment.profile_name = expense.profile_name  # Set profile_name from the related Expense
        comment.expense = expense  # Set the ForeignKey to the related Expense
        comment.comment = comment_text
        comment.save()
        comments = Comment.objects.filter(profile_name=expense.profile_name, expense=expense)

        # Redirect to the 'show_recurring' view or an appropriate page
        return redirect('show_recurring', expense_id=expense_id)

    company = company_details.objects.get(user=request.user)

    context = {
        'expense': expense,
        'company': company,
        'comments':comments,
    }

    return render(request, 'show_recurring.html', context)
    
    
def get_vendor_gst(request, vendor_id):
    
    vendor = vendor_table.objects.get(pk=vendor_id)
    
    return JsonResponse({'gst_treatment': vendor.gst_treatment,'gst_number':vendor.gst_number,'email':vendor.vendor_email,})
        
@login_required(login_url='login')
def delete_expense_comment(request, expense_id, comment_id):
    
        try:
            comment = get_object_or_404(Comment, id=comment_id, expense__id=expense_id)
            
            # Retrieve the corresponding expense object for the comment
            expense = comment.expense

            # Check if the profile_name in the expense matches the user's profile name
            if expense.profile_name == comment.profile_name:
                comment.delete()
        except Comment.DoesNotExist:
            pass  # Comment does not exist, no need to delete

        return redirect('show_recurring', expense_id=expense_id)
        
@login_required(login_url='login')
def get_customer_email(request):
   
    if request.method == 'GET':
        customer_id = request.GET.get('customername')
        try:
            custmer = customer.objects.get(id=customer_id)
            email = custmer.customerEmail
           
            return JsonResponse({'email': email})
        except customer.DoesNotExist:  # Corrected exception name
            # Handle the case where the customer does not exist
            return JsonResponse({'error': 'Customer not found'}, status=404)
    else:
        # Handle other HTTP methods if necessary
        return JsonResponse({'error': 'Invalid request method'}, status=400)
        
        
@login_required(login_url='login')
def custmr_payment(request):

    if request.method == 'POST':
        print('enter payment terms')
        user = request.user
        name = request.POST.get('term_name')
        days = request.POST.get('term_days')
        
        
        payment = payment_terms(Terms=name, Days=days, user=user)
        payment.save()
        
        return JsonResponse({'success': True, 'term_name': name, 'term_id': payment.id})
    else:
        return JsonResponse({'success': False})
        
        
def creditnotes(request):
    user = request.user
    credit_notes = Creditnote.objects.all()
    company = company_details.objects.get(user=user)
    context = {'credit_notes': credit_notes , 'company':company}
    return render(request, 'creditnotes.html', context)
   

def newcredit(request):
    item=AddItem.objects.all()
    user = request.user
    unit=Unit.objects.all()
    sales=Sales.objects.all()
    company = company_details.objects.get(user=user)
    cust=customer.objects.all()
    pay=payment_terms.objects.all()
    itm=sales_item.objects.all()
    purchase=Purchase.objects.all()
    
   
    return render(request,'newcredit.html',{"c":cust, "pay":pay, "itm":itm,"company":company,"unit":unit, "sales":sales,"purchase":purchase,'item':item })


def creditnote_view(request,creditnote_id):
    user = request.user
    item=AddItem.objects.all()
    cust=customer.objects.all()
    company = company_details.objects.get(user=user)
    creditnote = get_object_or_404(Creditnote, id=creditnote_id)
    credititems = Credititem.objects.filter(creditnote=creditnote)
    creditnote_customers = customer.objects.filter(creditnote=creditnote)
    creditnotes = Creditnote.objects.all()  # Fetch all Creditnote objects
    print(creditnote)
    return render(request,'creditnote_view.html',{'company':company, 'cust': creditnote_customers,'creditnote':creditnote,'cust':cust ,'credititems': credititems,'item':item,'creditnotes': creditnotes})    

def add_creditnotes(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        customer_id = request.POST.get('cx_name')
        invoice_number = request.POST.get('sale_no')
        credit_note = request.POST.get('credit_note')
        reference = request.POST.get('ord_no')
        creditnote_date = request.POST.get('cr_date')
        customer_notes = request.POST.get('customer_note')
        subtotal = request.POST.get('subtotal')
        igst = request.POST.get('igst')
        cgst = request.POST.get('cgst')
        sgst = request.POST.get('sgst')
        total_tax = request.POST.get('tax_total')
        shipping_charge = request.POST.get('shipping_charge')
        adjustment = request.POST.get('adjustment')
        total = request.POST.get('t_total')
        terms_and_conditions = request.POST.get('ter_cond')
        attached_file = request.FILES.get('file')

        # Create the Creditnote instance
        credit_note_instance = Creditnote(
            user=request.user,
            customer_id=customer_id,
            invoice_number=invoice_number,
            credit_note=credit_note,
            reference=reference,
            creditnote_date=creditnote_date,
            customer_notes=customer_notes,
            subtotal=subtotal,
            igst=igst,
            cgst=cgst,
            sgst=sgst,
            total_tax=total_tax,
            shipping_charge=shipping_charge,
            total=total,
            terms_and_conditions=terms_and_conditions,
            attached_file=attached_file,
            adjustment=adjustment,
            active=True
        )

        # Save the Creditnote instance
        credit_note_instance.save()

        # Handle Credititem data
        items = request.POST.getlist('item_name[]')
        hsns = request.POST.getlist('hsn[]')
        quantities = request.POST.getlist('quantity[]')
        rates = request.POST.getlist('rate[]')
        taxes = request.POST.getlist('tax[]')
        discounts = request.POST.getlist('discount[]')
        amounts = request.POST.getlist('amount[]')

        if len(items) == len(hsns) == len(quantities) == len(rates) == len(discounts) == len(taxes) == len(amounts):
            for i in range(len(items)):
                add_item_instance = get_object_or_404(AddItem, pk=items[i])
                add_item_instance.save()

                item = Credititem(
                    creditnote=credit_note_instance,
                    item_name=add_item_instance,
                    hsn=hsns[i],
                    quantity=quantities[i],
                    rate=rates[i],
                    tax=taxes[i],
                    discount=discounts[i],
                    amount=amounts[i],
                )
                item.save()

            return redirect('creditnotes')

    return render(request, 'creditnotes.html', {'c': [credit_note_instance]})

def edit_creditnote(request, pk):
    user = request.user
    company = company_details.objects.get(user=user)
    cust=customer.objects.all()
    creditnote = get_object_or_404(Creditnote, id=pk)
    credititems = Credititem.objects.filter(creditnote=creditnote)
    itm = AddItem.objects.all()
    print(credititems)  
    
    return render(request, 'edit_creditnote.html', {'creditnote': creditnote, 'credititems': credititems,'cust':cust,'itm':itm,'company':company})       
      

def editdb(request, pk):
    creditnote = get_object_or_404(Creditnote, id=pk)
    cust = customer.objects.all()
    itm = AddItem.objects.all()

    if request.method == 'POST':
        # Retrieve customer_id from the form
        customer_id = request.POST.get('customer', None)
        email=request.POST.get('email')
        placeofsupply=request.POST.get('place_of_supply')
        gsttreatment=request.POST.get('gst_treatment')
        gstin=request.POST.get('gstin')
        baddress=request.POST.get('billing_address')
     
        invoice_number = request.POST.get('sale_no')
        credit_note = request.POST.get('credit_note')
        reference = request.POST.get('ord_no')
        creditnote_date = request.POST.get('cr_date')
        customer_notes = request.POST.get('customer_note')
        subtotal = request.POST.get('subtotal')
        igst = request.POST.get('igst')
        cgst = request.POST.get('cgst')
        sgst = request.POST.get('sgst')
        total_tax = request.POST.get('tax_total')
        shipping_charge = request.POST.get('shipping_charge')
        total = request.POST.get('t_total')
        terms_and_conditions = request.POST.get('ter_cond')
        attached_file = request.FILES.get('file')
        adjustment = request.POST.get('adjustment')

        # Ensure that customer_id is a valid integer
        try:
            customer_id = int(customer_id)
        except (ValueError, TypeError):
            customer_id = None

        # Update the fields of the existing Creditnote object
       
        
        creditnote.invoice_number = invoice_number
        creditnote.credit_note = credit_note
        creditnote.reference = reference
        creditnote.creditnote_date = creditnote_date
        creditnote.customer_notes = customer_notes
        creditnote.subtotal = subtotal
        creditnote.igst = igst
        creditnote.cgst = cgst
        creditnote.sgst = sgst
        creditnote.total_tax = total_tax
        creditnote.shipping_charge = shipping_charge
        creditnote.total = total
        creditnote.terms_and_conditions = terms_and_conditions
        creditnote.adjustment = adjustment

        # Set the customer_id field
        if customer_id is not None:
            creditnote.customer_id = customer_id

        # Save the updated Creditnote object
        creditnote.save()
        # Update credit item records
        item_ids = request.POST.getlist('item_id[]')
        item_names = request.POST.getlist('item_name[]')
        hsns = request.POST.getlist('hsn')
        quantities = request.POST.getlist('quantity[]')
        rates = request.POST.getlist('rate[]')
        taxes = request.POST.getlist('tax[]')
        discounts = request.POST.getlist('discount[]')
        amounts = request.POST.getlist('amount[]')

        for item_id, item_name, hsn, quantity, rate, tax, discount, amount in zip(item_ids, item_names, hsns, quantities, rates, taxes, discounts, amounts):
            credititem = Credititem.objects.get(id=item_id)
            credititem.item_name = item_name
            credititem.hsn = hsn
            credititem.quantity = quantity
            credititem.rate = rate
            credititem.tax = tax
            credititem.discount = discount
            credititem.amount = amount
          
            credititem.save()

        return redirect('creditnote_view', creditnote_id=creditnote.pk)

    return render(request, 'creditnote_view.html', {'creditnote': creditnote, 'cust': cust, 'itm': itm})


def load_initial_items(request):
    # Retrieve the initial items
    initial_items = AddItem.objects.all()

    # Serialize the items to JSON
    items_json = serializers.serialize('json', initial_items)

    # Return the serialized items as a JSON response
    return JsonResponse(items_json, safe=False)


def credit_template(request):
    return render(request,'credit_template.html')    




def file_download1(request,aid):
    att= Creditnote.objects.get(id=aid)
    file = att.attachment
    response = FileResponse(file)
    response['Content-Disposition'] = f'attachment; filename="{file.name}"'
    return response     

def deletefile1(request,aid):
    att=Payrollfiles.objects.get(id=aid)
    p=att.payroll
    att.delete()
    return redirect('payroll_view',p.id)


def purchase_item_dropdown1(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = AddItem.objects.all()
    for option in option_objects:
        options.append({
            'id': option.id,
            'Name': option.Name,
            'hsn': option.hsn,  # Include HSN field in the response
            'rate': option.rate,  # Include rate field in the response
        })


    return JsonResponse(options)

def fetch_customers_from_creditnotes(request):
    # Retrieve all CreditNote objects
    creditnotes = Creditnote.objects.all()

    # Initialize an empty list to store customer data
    customer_data = []

    # Iterate through credit notes and get associated customers
    for creditnote in creditnotes:
        customer = creditnote.customer  # Assuming there's a ForeignKey from CreditNote to Customer
        if customer:
            customer_data.append({
                'customerName': customer.customerName,
                'creditNoteNumber': creditnote.credit_note,
                'amount': creditnote.total,  # Assuming you want to display the total amount
            })

    # Return the customer data as JSON response
    return JsonResponse(customer_data, safe=False)

def delete_creditnote(request, pk):
    
    creditnote = get_object_or_404(Creditnote, pk=pk)

    
    creditnote_items = Credititem.objects.filter(creditnote=creditnote)

   
    creditnote_items.delete()

    creditnote.delete()

    
    return redirect('creditnotes')




def add_comment_creditnotes(request, creditnote_id):
    creditnote = get_object_or_404(Creditnote, pk=creditnote_id)

    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        user = request.user  # Assuming you're using Django's authentication

        # Create a new comment instance and save it
        comment = creditnote_comments(user=user, creditnote=creditnote, comment=comment_text)
        comment.save()

    return redirect('creditnote_view', creditnote_id=creditnote_id)


def creditnote_add_file(request, pk):
    creditnote = get_object_or_404(Creditnote, user=request.user, pk=pk)

    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')

        if uploaded_file:
           
            creditnote_doc_upload = Creditnote_doc_upload(
                user=request.user,
                creditnote=creditnote,
                title="Attachment",  # Set an appropriate title
                document=uploaded_file
            )
            creditnote_doc_upload.save()

    return redirect('creditnote_view', pk=pk)    
    
    
def customer_balances(request):
    user = request.user
    company = company_details.objects.get(user=user)
    vc=customer.objects.all()
    return render(request,'customer_balances.html',{'vc':vc,'company':company})
    return render(request,'customer_balances.html')


def delivery_challan(request):
    
    user = request.user
    company = company_details.objects.get(user=user)
    view=DeliveryChellan.objects.all()
    
   
    return render(request,'delivery_challan.html',{'view':view,'company':company})

def show_customize_challan(request):
    user = request.user
    company1 = company_details.objects.get(user = user)
    return render(request, 'customize_show_challan.html', {'company':company1})

def custom_report(request):
    user = request.user
    customer1 = customer.objects.all()
    company = company_details.objects.get(user=user)
    return render(request,'custom_report.html',{'customer':customer1,'company':company})

def challan_customize(request):
    user = request.user
    company = company_details.objects.get(user=user)
    general = "url4"
    show = "url3"
    
    context = {
        'url4' : general,
        'url3' : show,
        'company' : company,
    }
    return render(request, 'customize_challan.html',context)
    
    
#Rijin

def create_loan(request):
    error_message = None

    if request.method == 'POST':
        print("Received a POST request")
        # Process form submission
        employee_id = request.POST.get('employee')
        issue_date = request.POST.get('loan_issue_date')
        expiry_date = request.POST.get('loan_expiry_date')
        loan_amount = request.POST.get('loan_amount')
        cutting_type = request.POST.get('payment_method')

        try:
            if cutting_type == 'percentage_wise':
                cutting_percentage = request.POST.get('percentage')
                # Fetch the payroll object based on the selected employee
                payroll = Payroll.objects.get(id=employee_id)
                # Calculate monthly cutting amount as a percentage of salary
                cutting_amount = (float(cutting_percentage) / 100) * float(payroll.salary)
            else:
                cutting_amount = request.POST.get('monthly_cutting_amount')
                cutting_percentage = 0  # Initialize as None

            # Fetch the payroll object based on the selected employee
            payroll = Payroll.objects.get(id=employee_id)
            
            # Check if monthly cutting amount is greater than salary
            if float(cutting_amount) > float(payroll.salary):
                raise ValueError("Monthly cutting amount cannot exceed employee's salary")

            loan = Loan(
                payroll=payroll,
                date_issue=issue_date,
                date_expiry=expiry_date,
                loan_amount=loan_amount,
                monthly_cutting_type=cutting_type,
                monthly_cutting_percentage=cutting_percentage,
                monthly_cutting_amount=cutting_amount
            )
            
            loan.save()

            # Debugging: Print information to the console
            print(f"Employee ID: {employee_id}")
            print(f"Issue Date: {issue_date}")
            print(f"Expiry Date: {expiry_date}")
            print(f"Loan Amount: {loan_amount}")
            print(f"Cutting Type: {cutting_type}")
            print(f"Cutting Percentage: {cutting_percentage}")
            print(f"Cutting Amount: {cutting_amount}")
            print(f"Payroll: {payroll}")
            print(f"Loan: {loan}")

            return redirect('employee_list')  # Redirect to the employee list page
        except (ValueError, Payroll.DoesNotExist, ValidationError) as e:
            # Handle validation errors (e.g., percentage > 100%, amount >= salary, employee not found)
            error_message = str(e)

    # For GET requests or when the form is not submitted, retrieve a list of all payrolls
    payrolls = Payroll.objects.all()
    company = company_details.objects.get(user=request.user)
    context = {
        'payrolls': payrolls,
        'error_message': error_message,
        'company': company,
    }
    return render(request, 'create_loan.html', context)
    
    
def employee_list(request):
    employees_with_loans = Payroll.objects.filter(loan__isnull=False)
    company=company_details.objects.get(user=request.user)
    for employee in employees_with_loans:
        employee.loan_info = Loan.objects.get(payroll=employee)
    
    context = {
        'employees': employees_with_loans,
        'company': company,
    }
    return render(request, 'employee_list.html', context)
    
    
def delete_loan(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    loan.delete()
    return redirect('employee_list') 
    
def edit_loan(request, loan_id): 
    print("Entering edit_loan view")
    
    loan = get_object_or_404(Loan, id=loan_id)
    payrolls = Payroll.objects.all()

    if request.method == 'POST':
        print("Processing form submission")
        
        employee_id = request.POST.get('employee')
        issue_date = request.POST.get('date_issue')
        expiry_date = request.POST.get('date_expiry')
        loan_amount = request.POST.get('loan_amount')
        
        cutting_type = request.POST.get('payment_method')

        # Check if 'cutting_type' is "percentage_wise" and calculate cutting_amount
        if cutting_type == 'amount_wise':
            cutting_percentage = 0
            cutting_amount = request.POST.get('monthly_cutting_amount')
        else:
            # 'cutting_type' is "amount_wise" or not provided, set cutting_percentage and cutting_amount to existing values
            cutting_percentage = request.POST.get('percentage')
            cutting_amount = (float(cutting_percentage) / 100) * float(loan.payroll.salary)

        # Check if any values have changed before updating
        if (issue_date != loan.date_issue or
            expiry_date != loan.date_expiry or
            loan_amount != loan.loan_amount or
            cutting_percentage != loan.monthly_cutting_percentage or
            cutting_amount != loan.monthly_cutting_amount):
            
            # Fetch the payroll object based on the selected employee
            payroll = Payroll.objects.get(id=employee_id)
            
            # Check if monthly cutting amount is greater than salary
            if float(cutting_amount) > float(payroll.salary):
                error_message = "Monthly cutting amount cannot exceed salary"
                context = {
                    'loan': loan, 
                    'payrolls': payrolls,
                    'error_message': error_message,
                }
                return render(request, 'edit_loan.html', context)
            
            # Update loan details
            loan.payroll = payroll
            loan.date_issue = issue_date
            loan.date_expiry = expiry_date
            loan.loan_amount = loan_amount
            loan.monthly_cutting_type = cutting_type
            loan.monthly_cutting_percentage = cutting_percentage
            loan.monthly_cutting_amount = cutting_amount
            loan.save()

            return redirect(reverse('employee_loan_details', args=[loan.payroll.id]))
    
    company = company_details.objects.get(user=request.user)
    
    context = {
        'loan': loan, 
        'company': company, 
        'payrolls': payrolls,
    }
    print("Returning from edit_loan view")
    return render(request, 'edit_loan.html', context)
    
    
def employee_loan_details(request, payroll_id):
    status = request.GET.get('status', 'all')

    if status == 'active':
        loans = Loan.objects.filter(payroll_id=payroll_id, active=True)
    elif status == 'inactive':
        loans = Loan.objects.filter(payroll_id=payroll_id, active=False)
    else:
        loans = Loan.objects.filter(payroll_id=payroll_id)

    payroll = get_object_or_404(Payroll, id=payroll_id)
    loans = Loan.objects.filter(payroll=payroll)
    l=Loan.objects.all()
    comments = LoanComment.objects.filter(payroll=payroll)
    attach = LoanAttach.objects.filter(payroll=payroll)
    ''' if request.method == 'POST':
        comment_text = request.POST.get('comment', '')  # Get the comment from the form
        loan_id = request.POST.get('loan_id', '')  # Get the associated loan ID from the form
        
        if comment_text and loan_id:
            loan = get_object_or_404(Loan, id=loan_id)
            comment = LoanComment(comment=comment_text, loan=loan)
            comment.save()
            # Redirect to the same page after saving the comment
            return redirect('employee_loan_details', payroll_id=payroll_id)'''
    company=company_details.objects.get(user=request.user)
    context = {
        'p': payroll,
        'loans': loans,
        'l' : l,
        'comments': comments,
        'attach' : attach,
        'company': company,
    }
    for loan in loans:
        print(f"Loan ID: {loan.id}")

    return render(request, 'employee_loan_details.html', context)
    
    
def activate_loan(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    loan.is_active = True
    loan.save()
    # Optionally, you can add a success message using Django's messages framework.
    # messages.success(request, 'Loan has been activated.')
    return redirect('employee_loan_details', payroll_id=loan.payroll.id)
    
def deactivate_loan(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    loan.is_active = False
    loan.save()
    # Optionally, you can add a success message using Django's messages framework.
    # messages.success(request, 'Loan has been deactivated.')
    return redirect('employee_loan_details', payroll_id=loan.payroll.id)
    
    
def toggle_loan_active(request, loan_id):
    loan = Loan.objects.get(pk=loan_id)
    loan.active = not loan.active  # Toggle the active status
    loan.save()
    
    return JsonResponse({'active': loan.active})
    
def employee_loan_template(request, payroll_id):
    status = request.GET.get('status', 'all')

    if status == 'active':
        loans = Loan.objects.filter(payroll_id=payroll_id, active=True)
    elif status == 'inactive':
        loans = Loan.objects.filter(payroll_id=payroll_id, active=False)
    else:
        loans = Loan.objects.filter(payroll_id=payroll_id)
    
    company = company_details.objects.get(user = request.user)
    payroll = get_object_or_404(Payroll, id=payroll_id)
    loans = Loan.objects.filter(payroll=payroll)
    l=Loan.objects.all()
    comments = LoanComment.objects.filter(payroll=payroll)
    attach = LoanAttach.objects.filter(payroll=payroll)

    context = {
        'company': company,
        'p': payroll,
        
        
     
        'loans': loans,
        'l' : l,
        
        'comments': comments,
        'attach' : attach
    }
    for loan in loans:
        print(f"Loan ID: {loan.id}")

    return render(request, 'employee_loan_template.html', context)
    
def add_loan_comment(request,payroll_id):
    
    payroll = get_object_or_404(Payroll, id=payroll_id)
    
    if request.method== 'POST':
        comments=request.POST['comment']
        c= LoanComment(comment=comments,payroll=payroll)
        c.save()
    return redirect('employee_loan_details',payroll_id=payroll_id)
    
    
def add_loan_comment_template(request,payroll_id):
    
    payroll = get_object_or_404(Payroll, id=payroll_id)
    
    if request.method== 'POST':
        comments=request.POST['comment']
        c= LoanComment(comment=comments,payroll=payroll)
        c.save()
    return redirect('employee_loan_template',payroll_id=payroll_id)
    
def delete_loan_comment(request, comment_id):
    try:
        # Get the loan comment using the provided comment_id
        comment = get_object_or_404(LoanComment, id=comment_id)
        
        # Get the associated payroll for redirection
        payroll = comment.payroll
        
        # Delete the comment
        comment.delete()
        
        # Redirect to the appropriate view (e.g., 'employee_loan_details')
        return redirect('employee_loan_details', payroll_id=payroll.id)
    except LoanComment.DoesNotExist:
        # Handle the case where the comment does not exist
        return redirect('employee_loan_details', payroll_id=payroll.id)
        
def delete_loan_comment_template(request, comment_id):
    try:
        # Get the loan comment using the provided comment_id
        comment = get_object_or_404(LoanComment, id=comment_id)
        
        # Get the associated payroll for redirection
        payroll = comment.payroll
        
        # Delete the comment
        comment.delete()
        
        # Redirect to the appropriate view (e.g., 'employee_loan_details')
        return redirect('employee_loan_template', payroll_id=payroll.id)
    except LoanComment.DoesNotExist:
        # Handle the case where the comment does not exist
        return redirect('employee_loan_template', payroll_id=payroll.id)
        
def add_loan_attach(request, payroll_id):
    if request.method == "POST" and request.FILES.get("file"):
        files = request.FILES["file"]
        payroll = get_object_or_404(Payroll, id=payroll_id)
        a = LoanAttach(attach=files, payroll=payroll)
        a.save()

        # Return a JSON response indicating success
        response_data = {
    'message': 'The file was uploaded successfully.Please reload the page to download it.'
}

        return JsonResponse(response_data)

    

        
        
    else:
        return redirect('employee_loan_details', payroll_id=payroll_id)
        
def add_loan_attach_template(request, payroll_id):
    if request.method == "POST" and request.FILES.get("file"):
        files = request.FILES["file"]
        payroll = get_object_or_404(Payroll, id=payroll_id)
        a = LoanAttach(attach=files, payroll=payroll)
        a.save()

        # Return a JSON response indicating success
        response_data = {'message': 'The file was uploaded successfully. Please reload the page to download it'}
        return JsonResponse(response_data)  
    else:
        return redirect('employee_loan_template', payroll_id=payroll_id)
        
        
def download_loan_attach(request, payroll_id, attachment_id):
    # Retrieve the LoanAttach object based on the attach_id
    payroll = get_object_or_404(Payroll, id=payroll_id)
    loan_attach = get_object_or_404(LoanAttach,id=attachment_id, payroll=payroll)

    # Get the file to be downloaded
    attachment_file = loan_attach.attach

    # Create a FileResponse and set content disposition for download
    response = FileResponse(attachment_file)
    response['Content-Disposition'] = f'attachment; filename="{attachment_file.name}"'

    return response
    
    
def delete_loan_attach(request, attach_id):
    try:
        # Get the loan comment using the provided comment_id
        attach = get_object_or_404(LoanAttach, id=attach_id)
        
        # Get the associated payroll for redirection
        payroll = attach.payroll
        
        # Delete the comment
        attach.delete()
        
        # Redirect to the appropriate view (e.g., 'employee_loan_details')
        return redirect('employee_loan_details', payroll_id=payroll.id)
    except LoanAttach.DoesNotExist:
        # Handle the case where the comment does not exist
        # Redirect to an appropriate view or return an error response
        return redirect('employee_loan_details', payroll_id=payroll.id)  # You may want to change this behavior if needed
        
def delete_loan_attach_template(request, attach_id):
    try:
        # Get the loan comment using the provided comment_id
        attach = get_object_or_404(LoanAttach, id=attach_id)
        
        # Get the associated payroll for redirection
        payroll = attach.payroll
        
        # Delete the comment
        attach.delete()
        
        # Redirect to the appropriate view (e.g., 'employee_loan_details')
        return redirect('employee_loan_template', payroll_id=payroll.id)
    except LoanAttach.DoesNotExist:
        # Handle the case where the comment does not exist
        # Redirect to an appropriate view or return an error response
        return redirect('employee_loan_template', payroll_id=payroll.id)
        
        
def loan_active(request, loan_id):
  
    l = get_object_or_404(Loan, id=loan_id)

    # Activate the bank account
    l.active = True
    l.save()

    # Redirect to a success page
    return redirect('employee_loan_details' ,payroll_id=loan_id)
    
def loan_deactive(request, loan_id):
  
    l = get_object_or_404(Loan, id=loan_id)

    # Activate the bank account
    l.active = False
    l.save()

    # Redirect to a success page
    return redirect('employee_loan_details' ,payroll_id=loan_id)
    
    
def createpayroll2(request):
    if request.method=='POST':
        title=request.POST['title']
        fname=request.POST['fname']
        lname=request.POST['lname']
        alias=request.POST['alias']
        joindate=request.POST['joindate2']
        saltype=request.POST['saltype']
        if (saltype == 'Fixed'):
            salary=request.POST['fsalary']
        else:
            salary=request.POST['vsalary']
        image=request.FILES.get('file')
        if image == None:
            image="image/img.png"
        empnum=request.POST['empnum']
        designation = request.POST['designation']
        location=request.POST['location']
        gender=request.POST['gender']
        dob=request.POST['dob']
        blood=request.POST['blood']
        fmname=request.POST['fm_name']
        sname=request.POST['s_name']
        email=request.POST['email2']        
        add1=request.POST['address']
        add2=request.POST['address2']
        address=add1+" "+add2
        padd1=request.POST['paddress'] 
        padd2=request.POST['paddress2'] 
        paddress= padd1+padd2
        phone=request.POST['phone']
        ephn=request.POST['ephone']
        if ephn=="":
            ephone=None
        else:
            ephone=request.POST['ephone']
        
        isdts=request.POST['tds']
        if isdts == '1':
            istdsval=request.POST['pora']
            if istdsval == 'Percentage':
                tds=request.POST['pcnt']
            elif istdsval == 'Amount':
                tds=request.POST['amnt']
        else:
            istdsval='No'
            tds = 0
        itn=request.POST['itn']
        an=request.POST['an']        
        uan=request.POST['uan'] 
        pfn=request.POST['pfn']
        pran=request.POST['pran']
        payroll= Payroll(title=title,first_name=fname,last_name=lname,alias=alias,image=image,joindate=joindate,salary_type=saltype,salary=salary,emp_number=empnum,designation=designation,location=location,
                         gender=gender,dob=dob,blood=blood,parent=fmname,spouse_name=sname,address=address,permanent_address=paddress ,Phone=phone,emergency_phone=ephone,
                         email=email,ITN=itn,Aadhar=an,UAN=uan,PFN=pfn,PRAN=pran,isTDS=istdsval,TDS=tds)
        payroll.save()

        bank=request.POST['bank']
        if(bank == '1'):
            accno=request.POST['acc_no']       
            ifsc=request.POST['ifsc']       
            bname=request.POST['b_name']       
            branch=request.POST['branch']
            ttype=request.POST['ttype']
            b=Bankdetails(payroll=payroll,acc_no=accno,IFSC=ifsc,bank_name=bname,branch=branch,transaction_type=ttype)
            b.save()
        attach=request.FILES.get('attach')       
        if(attach):
            att=Payrollfiles(attachment=attach,payroll=payroll)
        # messages.success(request,'Saved succefully !')
        print(bank)
        return redirect('create_loan')
    else:
        return redirect('create_loan')
        
        
def loan_dropdown(request):
    options = {}
    option_objects = Payroll.objects.all()  
    for option in option_objects:
        options[option.id] = {
            'employee_name': option.first_name + ' ' + option.last_name,
            'email': option.email,
            'salary': option.salary,
            'employee': option.emp_number,
            'join_date': option.joindate.strftime('%Y-%m-%d'),  
        }
    return JsonResponse(options)
    
    
def loan_dropwithoutreload(request, employee_id):
    
    employee = get_object_or_404(Payroll, id=employee_id)

    
    employee_details = {
        'email': employee.email,
        'emp_number': employee.emp_number,
        'salary': employee.salary,
        'joindate': employee.joindate.strftime('%Y-%m-%d'),
        
    }

    return JsonResponse(employee_details)
    
    
#Noel
def get_customerdet_eway(request):
    company= company_details.objects.get(user = request.user)
    name = request.POST.get('name')
    id = request.POST.get('id')
    cust = customer.objects.get(user=company.user_id,id=id)
    email = cust.customerEmail
    cust_id=id
    cust_place_supply=cust.placeofsupply
    gstin = cust.GSTIN
    gsttr = cust.GSTTreatment
    # cstate = cust.placeofsupply.split("] ")[1:]
    print(email)
    print(gstin)
    print(id)
    # state = 'Not Specified' if cstate == "" else cstate
    return JsonResponse({'customer_email' :email, 'gst_treatment':gsttr, 'gstin': gstin , 'cust_id':cust_id,'cust_place_supply':cust_place_supply},safe=False)
@login_required(login_url='login')
def purchase_item_eway(request):

    company = company_details.objects.get(user = request.user)

    if request.method=='POST':
        type=request.POST.get('type')
        name=request.POST['name']
        ut=request.POST['unit']
        inter=request.POST['inter']
        intra=request.POST['intra']
        sell_price=request.POST.get('sell_price')
        sell_acc=request.POST.get('sell_acc')
        sell_desc=request.POST.get('sell_desc')
        cost_price=request.POST.get('cost_price')
        cost_acc=request.POST.get('cost_acc')      
        cost_desc=request.POST.get('cost_desc')
        units=Unit.objects.get(id=ut)
        sel=Sales.objects.get(id=sell_acc)
        cost=Purchase.objects.get(id=cost_acc)

        history="Created by " + str(request.user)
        user = User.objects.get(id = request.user.id)

        item=AddItem(type=type,unit=units,sales=sel,purchase=cost,Name=name,p_desc=cost_desc,s_desc=sell_desc,s_price=sell_price,p_price=cost_price,
                    user=user,creat=history,interstate=inter,intrastate=intra)

        item.save() 
        print("function")
        return JsonResponse({"message": "success"})
        
@login_required(login_url='login')        
def purchase_item_dropdown_eway(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = AddItem.objects.all()
    for option in option_objects:
        options[option.id] = option.Name

    return JsonResponse(options)
@login_required(login_url='login')
def purchase_unit_eway(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        unit =request.POST.get('unit')
        
        u = User.objects.get(id = request.user.id)

        unit = Unit(unit= unit)
        unit.save()
     
        return JsonResponse({"message": "success"})
        
@login_required(login_url='login')        
def purchase_unit_dropdown_eway(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = Unit.objects.all()
    for option in option_objects:
        options[option.id] = option.unit
    
    return JsonResponse(options)
    
    
def vendorbal_customer(request):
    sum=0 
    sum1=0
    company=company_details.objects.get(user=request.user)
    customer1 = customer.objects.all()
    purchasebill=PurchaseBills.objects.filter(user=request.user)
    for p in purchasebill:
        sum=sum+p.total
    recurringbill=recurring_bills.objects.filter(user=request.user)
    for s in recurringbill:
        sum1=sum1+s.grand_total
    grand=sum+sum1
    return render(request, 'vendor_customer.html', {'cust': customer1, 'company':company,'purchasebill':purchasebill, 'sum': sum,'recurringbill':recurringbill,'sum1':sum1,'grand':grand})

def bill_details(request):
    print(request.user)
    company=company_details.objects.get(user=request.user)
    purchasebill=PurchaseBills.objects.filter(user=request.user)
    recurringbill=recurring_bills.objects.filter(user=request.user)
    vendors_balance = {}
    payments = payment_made.objects.filter(user=request.user)
    
    payments_all = payment_made.objects.all()
    for payment in payments: 
        vendor_name = payment.vendor.first_name
        currentbaln=payment.current_balance
        print(currentbaln)
        if vendor_name not in vendors_balance:
            vendors_balance[vendor_name] = currentbaln
        else:
            vendors_balance[vendor_name] += currentbaln
    for bill in purchasebill:
        vendor_name = bill.vendor_name
        print(vendor_name)
       
    print(vendors_balance)
    return render(request, 'bill_details.html', {'company':company,'purchasebill':purchasebill,'recurringbill':recurringbill,'vendors_balance':vendors_balance})

def vendor_customize_report(request):
    company_data = company_details.objects.get(user=request.user)
    purchasebill=PurchaseBills.objects.all()
    print(purchasebill)
    return render(request, 'vendor_customize_report.html',{'company': company_data,'purchasebill':purchasebill})

def bill_customize_report(request):
    company_data = company_details.objects.get(user=request.user)
    return render(request, 'bill_customize_report.html',{'company': company_data})
    
    
def daybook(request):
    company = company_details.objects.get(user=request.user)
    cus=customer.objects.all()
    esti=Estimates.objects.all()
    cred=Creditnote.objects.all()
    inv=invoice.objects.all()
    dc=DeliveryChellan.objects.all()
    retain=RetainerInvoice.objects.all()
    sales=SalesOrder.objects.all()
    payment=payment_made.objects.all()
    recbill=recurring_bills.objects.all()
    exp=Expense.objects.all()
    purchase=Purchase_Order.objects.all()
    pbill=PurchaseBills.objects.all()
    ebill=EWayBill.objects.all()
    loan=Loan.objects.all()
    vcr=Vendor_Credits_Bills.objects.all()
    emp=Payroll.objects.all()
    offbank=Bankdetails.objects.all()
    bdetails=Bankcreation.objects.all()
    item=AddItem.objects.all()
    price=Pricelist.objects.all()

    



    context={
            'company': company,'cus':cus,
            'cred':cred,'inv':inv,
            'dc':dc,'esti':esti,'retain':retain,'sales':sales,'payment':payment,
            'recbill':recbill,'exp':exp,'purchase':purchase,'pbill':pbill,'ebill':ebill,
            'loan':loan,'vcr':vcr,'emp':emp,'offbank':offbank,'bdetails':bdetails,'item':item,'price':price,
    }
    return render(request,'daybook.html',context)


def creditnote_details(request):
    company= company_details.objects.get(user=request.user)
    credit= Creditnote.objects.all()  
    return render(request,'creditnote_details.html',{'company': company,'credit':credit})
    
@login_required(login_url='login')
def save_recurring_data(request):
    if request.method == 'POST':
        account_type = request.POST.get('accountType')
        account_name = request.POST.get('accountName')
        account_code = request.POST.get('accountCode')
        description = request.POST.get('description')

        account = Account(accountType=account_type, accountName=account_name,  description=description)
        account.save()
        acc_id = account.id

        return JsonResponse({
            "account_type": account_type,
            "account_name": account_name,
            "account_code": account_code,
            "description": description,
            "acc_id": acc_id
        })

    return render(request, 'recurring_home.html')
    
@login_required(login_url='login')
def entr_recurring_custmr(request):
    if request.method == 'POST':
       

        type = request.POST.get('radioCust')
        sal=request.POST.get('ctitle')
        fname= request.POST.get('cfirstname')
        lname=request.POST.get('clastname')
        # fullname=request.POST.get('cdisplayname')
        fullname = sal + ' ' + fname + ' ' + lname if fname and lname else (fname or lname)
        
        company = request.POST.get('ccompany_name')
        email = request.POST.get('cemail')
        wphone = request.POST.get('cw_mobile')
        mobile = request.POST.get('cp_mobile')
        facebook = request.POST.get('facebook')
        twitter = request.POST.get('twitter')
        wbsite = request.POST.get('website')
        skname = request.POST.get('cskype')
        desg = request.POST.get('c_desg')
        dept = request.POST.get('c_dpt')
        gstt = request.POST.get('c_gsttype')
        gstin = request.POST.get('c_gstin')
        pan=request.POST.get('c_pan')
        posply = request.POST.get('placesupply')
        tax1 = request.POST.get('radioCust1')
        crncy = request.POST.get('c_curn')
        obal = request.POST.get('c_open')
        
        selected_payment_label =int(request.POST.get('c_terms'))
       
        pterms = payment_terms.objects.get(id=selected_payment_label)
        
        
        baddrs1 = request.POST.get('cstreet1')
        baddrs2 = request.POST.get('cstreet2')
        bcity = request.POST.get('ccity')
        bstate = request.POST.get('cstate')
        bcountry = request.POST.get('ccountry')
        bpincode = request.POST.get('cpincode')
        bphone = request.POST.get('cphone')
        bfax = request.POST.get('cfax')
        saddrs1 = request.POST.get('csstreet1')
        saddrs2 = request.POST.get('csstreet2')
        scity = request.POST.get('cscity')
        sstate = request.POST.get('csstate')
        scountry = request.POST.get('cscountry')
        spincode = request.POST.get('cspincode')
        sphone = request.POST.get('csphone')
        sfax = request.POST.get('csfax')

        u = User.objects.get(id=request.user.id)

        ctmr = customer(customerType=type, customerName=fullname,
                        companyName=company, customerEmail=email, customerWorkPhone=wphone,
                        customerMobile=mobile, skype=skname, designation=desg, department=dept,
                        website=wbsite, GSTTreatment=gstt, placeofsupply=posply, Taxpreference=tax1,
                        currency=crncy, OpeningBalance=obal,PaymentTerms=pterms,    
                        Facebook=facebook, Twitter=twitter, GSTIN=gstin,Fname=fname,Lname=lname,
                        country=bcountry, Address1=baddrs1, Address2=baddrs2,pan_no=pan,
                        city=bcity, state=bstate, zipcode=bpincode, phone1=bphone,
                        fax=bfax, sAddress1=saddrs1, sAddress2=saddrs2, scity=scity, sstate=sstate,
                        scountry=scountry, szipcode=spincode, sphone1=sphone, sfax=sfax, user=u)

        ctmr.save()
        print(ctmr)

        new_customer_data = {
            'id': ctmr.id,
            'name': ctmr.customerName,
            'email': ctmr.customerEmail,
            # Add other fields as needed
        }
        return JsonResponse(new_customer_data)

    payments = payment_terms.objects.all()
    return render(request, 'recurring_home.html', {'payments': payments})
    
    
@login_required(login_url='login')
def get_customer_namess(request):
    user_id=request.user.id
    customers = customer.objects.filter(user=user_id)
    customer_names = [{'id': c.id, 'name':c.customerName} for c in customers]
    return JsonResponse(customer_names, safe=False)    
    
    
@login_required(login_url='login')
def payment_view(request):
    user = request.user

    payment_terms_queryset = payment_terms.objects.filter(user=user)
  
    options = {option.id: [option.id, option.Terms] for option in payment_terms_queryset}

    return JsonResponse(options, safe=False)
    
    
@login_required(login_url='login')
def add_recurring_vendor(request):
    
    if request.method=="POST":
       
        salutation=request.POST['title']
        
        first_name=request.POST['firstname']
        
        last_name=request.POST['lastname']
        company_name=request.POST['vcompany_name']
        vendor_email=request.POST['vemail']
        vendor_wphone=request.POST['vw_mobile']
        vendor_mphone=request.POST['vp_mobile']
        website=request.POST['website']
        skype_number=request.POST['vskype']
        designation=request.POST['v_desg']
        department=request.POST['v_dpt']
        gst_treatment=request.POST['v_gsttype']
        gst_number=request.POST['v_gstin']
        pan_number=request.POST['v_pan']
            
        source_supply=request.POST['v_sourceofsupply']
        currency=request.POST['currency']
        opening_bal=request.POST['v_open']
        payment_terms=request.POST['v_terms']
        bstreet=request.POST['vstreet']
        bcity=request.POST['vcity']
            

            
        bstate=request.POST['vstate']
        bcountry=request.POST['vcountry']
        bpin=request.POST['vpincode']
        bphone=request.POST['vphone']
        bfax=request.POST['vfax']
        sstreet=request.POST['vsstreet']
        scity=request.POST['vscity']
        sstate=request.POST['vsstate']

        scountry=request.POST['vscountry']

        spin=request.POST['vspincode']
        sphone=request.POST['vsphone']
        sfax=request.POST['vsfax']
        vendor_data=vendor_table(salutation=salutation,
                                 first_name=first_name,
                                 last_name=last_name,
                                 company_name=company_name,
                                 vendor_email=vendor_email,
                                 vendor_wphone=vendor_wphone,
                                 vendor_mphone=vendor_mphone,
                                 website=website, 
                                 skype_number= skype_number,
                                 designation=designation,
                                 department=department,
                                 gst_treatment=gst_treatment,
                                 pan_number=pan_number,
                                 gst_number=gst_number,
                                 source_supply=source_supply,
                                 currency=currency,
                                 opening_bal=opening_bal,
                                 payment_terms=payment_terms,
                                 bstreet=bstreet,
                                 bcity=bcity,
                                 bstate=bstate,
                                 bcountry=bcountry,
                                 bpin= bpin,
                                 bphone=bphone,
                                 bfax=bfax,
                                 sstreet=sstreet,
                                 scity=scity,
                                 sstate=sstate,
                                 scountry=scountry,
                                 spin=spin,
                                 sphone=sphone,
                                 sfax=sfax)
        
        vendor_data.save()
        user_id=request.user.id

        udata=User.objects.get(id=user_id)
        vendor_data.user=udata
        vendor_data.save()
       
        vendorname=f"{vendor_data.first_name} {vendor_data.last_name}"
       
        
        
       
        
        response_data = {
        'success': True,  # Indicate success
        'vendorId': vendor_data.id,
        'gstTreatment': gst_treatment, 
        'gstnum':gst_number,
        'vendorName':vendorname,
    }
        return JsonResponse(response_data)
    return render(request, 'recurring_home.html')
    
    
#............................................mirna.................manual journal................................

def manual_journal_home(request):
    query = request.GET.get('query')
    filter_type = request.GET.get('filter')

    journals = Journal.objects.all()

    if query:
        journals = journals.filter(
            Q(date__icontains=query) |
            Q(journal_no__icontains=query) |
            Q(reference_no__icontains=query) |
            Q(status__icontains=query) |
            Q(notes__icontains=query) |
            Q(total_debit__icontains=query)
        )

    if filter_type == 'draft':
        journals = journals.filter(status='draft')
    elif filter_type == 'published':
        journals = journals.filter(status='published')

    try:
        company = company_details.objects.get(user=request.user)
        company_name = company.company_name
        address = company.address
    except company_details.DoesNotExist:
        company_name = ''
        address = ''

    context = {
        'journal': journals,
        'query': query,
        'filter_type': filter_type,
        'company_name': company_name,
        'address': address,
        'company' : company,
    }
    return render(request, 'manual_journal.html', context)

def add_journal(request):
    accounts = Chart_of_Account.objects.all()
    vendors = vendor_table.objects.all()
    customers = customer.objects.all()

    try:
        company = company_details.objects.get(user=request.user)
        company_name = company.company_name
        address = company.address
    except company_details.DoesNotExist:
        company_name = ''
        address = ''

    if request.method == 'POST':
        user = request.user
        date = request.POST.get('date')
        journal_no = request.POST.get('journal_no')
        reference_no = request.POST.get('reference_no')
        notes = request.POST.get('notes')
        currency = request.POST.get('currency')
        cash_journal = request.POST.get('cash_journal') == 'True'

        attachment = request.FILES.get('attachment')  

        journal = Journal(
            user=user,
            date=date,
            journal_no=journal_no,
            reference_no=reference_no,
            notes=notes,
            currency=currency,
            cash_journal=cash_journal,
            attachment=attachment  
        )
        journal.save()

        account_list = request.POST.getlist('account')
        description_list = request.POST.getlist('description')
        contact_list = request.POST.getlist('contact')
        debits_list = request.POST.getlist('debits')
        credits_list = request.POST.getlist('credits')

        total_debit = 0
        total_credit = 0

        for i in range(len(account_list)):
            account = account_list[i]
            description = description_list[i]
            contact = contact_list[i]
            debits = debits_list[i]
            credits = credits_list[i]

            journal_entry = JournalEntry(
                journal=journal,
                account=account,
                description=description,
                contact=contact,
                debits=debits,
                credits=credits
            )
            journal_entry.save()

            total_debit += float(debits) if debits else 0
            total_credit += float(credits) if credits else 0

        difference = total_debit - total_credit

        journal.total_debit = total_debit
        journal.total_credit = total_credit
        journal.difference = difference
        journal.save()

        return redirect('manual_journal_home')

    return render(request, 'add_journal.html', {'accounts': accounts, 'vendors': vendors,'customers': customers, 'company_name': company_name,'address': address,'company' : company})
    
@login_required(login_url='login')
def journal_account_dropdown(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = Chart_of_Account.objects.filter(user = user)
    for option in option_objects:
        options[option.id] = [option.account_name,option.id]

    return JsonResponse(options)

@login_required(login_url='login')
def create_account_jrnl(request):
    u = User.objects.get(id = request.user.id)
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        type=request.POST.get('type')
        name=request.POST.get('name')

        u = User.objects.get(id = request.user.id)

        acc = Chart_of_Account(account_type=type,account_name=name,user = u)
        acc.save()

        response_data = {
            "message": "success",
            "name":name,
        }

        return JsonResponse(response_data)

def journal_list(request):
    query = request.GET.get('query')
    filter_param = request.GET.get('filter')

    journals = Journal.objects.all()

    if query:
        journals = journals.filter(
            Q(date__icontains=query) |
            Q(journal_no__icontains=query) |
            Q(reference_no__icontains=query) |
            Q(status__icontains=query) |
            Q(notes__icontains=query) |
            Q(total_debit__icontains=query)
        )

    if filter_param:
        if filter_param == 'draft':
            journals = journals.filter(status='draft')
        elif filter_param == 'published':
            journals = journals.filter(status='published')

    journal_id = request.GET.get('journal_id')
    selected_journal = None
    journal_entries = None

    if journal_id:
        selected_journal = get_object_or_404(Journal, id=journal_id)
        journal_entries = JournalEntry.objects.filter(journal=selected_journal)

    try:
        company = company_details.objects.get(user=request.user)
        company_name = company.company_name
        address = company.address
    except company_details.DoesNotExist:
        company_name = ''
        address = ''

    context = {
        'journals': journals,
        'selected_journal': selected_journal,
        'journal_entries': journal_entries,
        'company_name': company_name,
        'address': address,
        'company':company,
    }

    return render(request, 'journal_list.html', context)

def get_journal_details(request, journal_id):
    try:
        selected_journal = Journal.objects.get(id=journal_id)
        journal_entries = JournalEntry.objects.filter(journal=selected_journal)

        try:
            company = company_details.objects.get(user=request.user)
            company_name = company.company_name
            address = company.address
        except company_details.DoesNotExist:
            company_name = ''
            address = ''

        data = {
            'company_name': company_name,
            'address': address,
            'selected_journal': {
                'notes': selected_journal.notes,
                'reference_no': selected_journal.reference_no,
                'journal_no': selected_journal.journal_no,
                'date': selected_journal.date,
                'total_credit': selected_journal.total_credit,
                'total_debit': selected_journal.total_debit,
                'difference': selected_journal.difference,
            },
            'journal_entries': [
                {
                    'account': entry.account,
                    'description': entry.description,
                    'contact': entry.contact,
                    'debits': entry.debits,
                    'credits': entry.credits,
                }
                for entry in journal_entries
            ],
        }

        return JsonResponse(data)
    except Journal.DoesNotExist:
        return JsonResponse({'error': 'Journal not found'}, status=404)
    
def get_journal_details_for_overview(request, journal_id):
    try:
        selected_journal = Journal.objects.get(id=journal_id)
        journal_entries = JournalEntry.objects.filter(journal=selected_journal)

        try:
            company = company_details.objects.get(user=request.user)
            company_name = company.company_name
            address = company.address
        except company_details.DoesNotExist:
            company_name = ''
            address = ''

        data = {
            'company_name': company_name,
            'address': address,
            'selected_journal': {
                'notes': selected_journal.notes,
                'reference_no': selected_journal.reference_no,
                'journal_no': selected_journal.journal_no,
                'status': selected_journal.status,
                'date': selected_journal.date,
                'total_credit': selected_journal.total_credit,
                'total_debit': selected_journal.total_debit,
                'difference': selected_journal.difference,
            },
            'journal_entries': [
                {
                    'account': entry.account,
                    'description': entry.description,
                    'contact': entry.contact,
                    'debits': entry.debits,
                    'credits': entry.credits,
                }
                for entry in journal_entries
            ],
        }

        return JsonResponse(data)
    except Journal.DoesNotExist:
        return JsonResponse({'error': 'Journal not found'}, status=404)

def update_journal_status(request, journal_id):
    if request.method == 'POST':
        try:
            selected_journal = Journal.objects.get(id=journal_id)
            selected_journal.status = 'published'
            selected_journal.save()

            return JsonResponse({'message': 'Journal status updated successfully.'})
        except Journal.DoesNotExist:
            return JsonResponse({'error': 'Journal not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
def get_journal_comments(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)
    comments = journal.comments.all()
    is_current_user_comment = False
    if request.user.is_authenticated:
        is_current_user_comment = comments.filter(user=request.user).exists()

    comments_data = [{
        'id': comment.id,
        'text': comment.text,
        'user': comment.user.username,
        'date_time': comment.date_time.strftime('%Y-%m-%d %H:%M:%S'),
    } for comment in comments]

    return JsonResponse({
        'comments': comments_data,
        'is_current_user_comment': is_current_user_comment,
    })

def save_journal_comment(request, journal_id):
    if request.method == 'POST':
        journal = get_object_or_404(Journal, id=journal_id)
        comment_text = request.POST.get('text')
        
        if comment_text:
            JournalComment.objects.create(
                journal=journal,
                user=request.user,
                text=comment_text,
            )
            
            return JsonResponse({'message': 'Comment saved successfully.'})
    
    return JsonResponse({'error': 'Invalid request.'}, status=400)

def delete_journal_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(JournalComment, id=comment_id)
        if request.user == comment.user:
            comment.delete()
            return JsonResponse({'message': 'Comment deleted successfully.'})
        else:
            return JsonResponse({'error': 'Permission denied.'}, status=403)
    
    return JsonResponse({'error': 'Invalid request.'}, status=400)

def get_journal_attachment(request, journal_id):
    try:
        selected_journal = Journal.objects.get(id=journal_id)

        if selected_journal.attachment:
            attachment_url = selected_journal.attachment.url
            return JsonResponse({'attachment_url': attachment_url})
        else:
            return JsonResponse({'attachment_url': None})
    except Journal.DoesNotExist:
        return JsonResponse({'error': 'Journal not found'}, status=404)

@require_POST
def delete_journal(request, journal_id):
    try:
        journal = Journal.objects.get(id=journal_id)
        journal_entries = JournalEntry.objects.filter(journal=journal)
        journal_entries.delete()
        journal.delete()
        return JsonResponse({'message': 'Journal deleted successfully.'})
    except Journal.DoesNotExist:
        return JsonResponse({'message': 'Journal not found.'})
    
def edit_journal(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)
    accounts = Chart_of_Account.objects.all()
    vendors = vendor_table.objects.all()
    customers = customer.objects.all()

    try:
        company = company_details.objects.get(user=request.user)
        company_name = company.company_name
        address = company.address
    except company_details.DoesNotExist:
        company_name = ''
        address = ''

    if request.method == 'POST':
        date = request.POST.get('date')
        journal_no = request.POST.get('journal_no')
        reference_no = request.POST.get('reference_no')
        notes = request.POST.get('notes')
        currency = request.POST.get('currency')
        cash_journal = request.POST.get('cash_journal') == 'True'

        journal.date = date
        journal.journal_no = journal_no
        journal.reference_no = reference_no
        journal.notes = notes
        journal.currency = currency
        journal.cash_journal = cash_journal       
        journal.user = request.user
        old=journal.attachment
        new = request.FILES.get('attachment')
        if old !=None and new==None:
            journal.attachment=old
        else:
            journal.attachment=new            
        journal.save()

        account_list = request.POST.getlist('account')
        description_list = request.POST.getlist('description')
        contact_list = request.POST.getlist('contact')
        debits_list = request.POST.getlist('debits')
        credits_list = request.POST.getlist('credits')

        total_debit = 0
        total_credit = 0

        JournalEntry.objects.filter(journal=journal).delete()

        for i in range(len(account_list)):
            account = account_list[i]
            description = description_list[i]
            contact = contact_list[i]
            debits = debits_list[i]
            credits = credits_list[i]

            journal_entry = JournalEntry(
                journal=journal,
                account=account,
                description=description,
                contact=contact,
                debits=debits,
                credits=credits
            )
            journal_entry.save()

            total_debit += float(debits) if debits else 0
            total_credit += float(credits) if credits else 0

        difference = total_debit - total_credit

        journal.total_debit = total_debit
        journal.total_credit = total_credit
        journal.difference = difference
        journal.save()

        return redirect('journal_list')

    return render(request, 'edit_journal.html', {'journal': journal, 'accounts': accounts, 'vendors': vendors, 'customers': customers, 'company_name': company_name,'address': address,'company' : company})

def save_pdf(request):
    if request.method == 'POST':
        pdf_data = request.POST.get('pdf_data')
        decoded_pdf_data = base64.b64decode(pdf_data)

        with open('/path/to/your/journal.pdf', 'wb') as f:
            f.write(decoded_pdf_data)

        with open('/path/to/your/journal.pdf', 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="journal.pdf"'
            return response

    return HttpResponse('Invalid request method')
    
    
#----------------------------shamreena---Inventory Details

def inven_details(request):
    company = company_details.objects.get(user=request.user)
    item=AddItem.objects.all()
    inv=invoice_item.objects.all()
    recur=recur_itemtable.objects.all()
    reta=RetainerInvoice.objects.all()
    pars=Purchase_Order_items.objects.all()
    estim=EstimateItems.objects.all()
    sale=sales_item.objects.all()
    challan=ChallanItems.objects.all()
    credit=Credititem.objects.all()
    vencredit=Vendor_invoice_item.objects.all()
    bills=PurchaseBillItems.objects.all()
    recubills=recurring_bills_items.objects.all()
    vendorbill=Vendor_Credits_Bills_items_bills.objects.all()
    context={
        'item':item,
        'recur':recur,
        'inv':inv,
        'reta':reta,
        'pars':pars,
        'company':company,
        'estim':estim,
        'sale':sale,
        'challan':challan,
        'credit':credit,
        'vencredit':vencredit,
        'bills':bills,
        'recubills':recubills,
        'vendorbill':vendorbill
    }
    return render(request,'inventorydetails.html', context)
    
def inventorysalegraph(request):
    company = company_details.objects.get(user=request.user)
    item=AddItem.objects.all()
    inv = invoice_item.objects.all()
    cnote =Credititem.objects.all()
    rinv = recur_itemtable.objects.all()
    context = {'company':company,"inv":inv,"cnote":cnote,"rinv":rinv,'item':item}
    return render(request, 'inventory sale graph.html', context)

def invengraph(request,product):
    company=company_details.objects.get(user=request.user)
    user_id=request.user
    item=invoice_item.objects.filter(product=product)
    items2 =recur_itemtable.objects.filter(iname=product)
    print(items2)

    # print(items)
    # labels = [items.name for item in items]
    # values = [item.value for item in items]
    products=AddItem.objects.all()
    n=AddItem.objects.get(Name=product)
    name=product
    print(name)
 
    context={

       "allproduct":item,
       "items2":items2,
      
       
       'name':name,
       "product":products,
        "n":n,
    #    "history":history,
       'company':  company, 
    #    "comments":comments,
    #    'stock': stock,
        'label': 'Line Chart',
        # 'labels': labels,
        # 'values': values,
        'chart_type': 'bar'
        
    }
    print('1')
    return render(request,'inventorygraph.html',context)      

def invenitem_graph_filter(request,product):
    company=company_details.objects.get(user=request.user)
    user_id=request.user
    item=invoice_item.objects.filter(product=product)
    n=AddItem.objects.get(Name=product)

    products=AddItem.objects.all()
    name=product
    print(name)
    if request.method == 'POST':
        s=request.POST['d1']
        start=str(s)
        e=request.POST['d2']
        end=str(e)
        items =  invoice_item.objects.filter(product=product,inv__due_date__range=[start,end])
        items2 =recur_itemtable.objects.filter(iname=product,ri__start__range=[start,end])
        products=AddItem.objects.all()
        n=AddItem.objects.get(Name=product)
        context={

       "allproduct":items,
       'items2':items2,
       
       'name':name,
       "n":n,
       "product":products,

       'company':  company, 
   
        'label': 'Line Chart',
    
        'chart_type': 'bar'
        }
        return render(request, 'inventorygraph.html', context)   

    
    context={

       "allproduct":item,
       
       'name':name,
       "n":n,
       "product":products,
 
       'company':  company, 

        'label': 'Line Chart',
       
        'chart_type': 'bar'
    }
    return render(request, 'inventorygraph.html', context)          
    
    
def credit_customer(request):
    
    company = company_details.objects.get(user = request.user)

    if request.user.is_authenticated:
        if request.method=='POST':
            tax=request.POST.get('tax')
            type=request.POST.get('title')
            first=request.POST['firstname']
            last=request.POST['lastname']
            txtFullName= request.POST['display_name']
            
            itemtype=request.POST.get('itemtype')
            cpname=request.POST['company_name']
            
            email=request.POST.get('email')
            wphone=request.POST.get('work_mobile')
            mobile=request.POST.get('pers_mobile')
            skname=request.POST.get('skype')
            desg=request.POST.get('desg')      
            dept=request.POST.get('dpt')
            wbsite=request.POST.get('website')

            gstt=request.POST.get('gsttype')
            gstin=request.POST.get('gstin')
            panno=request.POST.get('panno')


            posply=request.POST.get('placesupply')
            crncy=request.POST.get('currency')
            obal=request.POST.get('openingbalance')

           
            pterms=request.POST.get('paymentterms')

           
          
            fbk=request.POST.get('facebook')
            twtr=request.POST.get('twitter')
          
            ctry=request.POST.get('country')
            
            street=request.POST.get('street')
            shipstate=request.POST.get('shipstate')
            shipcity=request.POST.get('shipcity')
            bzip=request.POST.get('shippincode')
            shipfax=request.POST.get('shipfax')

            sal=request.POST.get('title')
            addres=street +','+ shipcity+',' + shipstate+',' + bzip
            adress2=addres
            u = User.objects.get(id = request.user.id)

            print(tax)
            ctmr=customer(customerName=txtFullName,customerType=itemtype,
                        companyName=cpname,customerEmail=email,customerWorkPhone=wphone,
                         customerMobile=mobile,skype=skname,designation=desg,department=dept,
                           website=wbsite,GSTTreatment=gstt,placeofsupply=posply, Taxpreference=tax,
                             currency=crncy,OpeningBalance=obal,PaymentTerms=pterms,
                               Facebook=fbk,Twitter=twtr
                                 ,country=ctry,Address1=addres,Address2=adress2,
                                  city=shipcity,state=shipstate,zipcode=bzip,phone1=wphone,
                                   fax=shipfax,
                                  user=u ,GSTIN=gstin,pan_no=panno)
            ctmr.save()
 
            
            return HttpResponse({"message": "success"})
        
        
def customer_dropdown_credit(request):
    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = customer.objects.filter(user = user)
    for option in option_objects:
        options[option.id] = [option.customerName]

    return JsonResponse(options)
    
def update_creditnote_status(request, creditnote_id):
    try:
        # Get the Creditnote object by ID
        creditnote = get_object_or_404(Creditnote, id=creditnote_id)

        # Update the status
        creditnote.active = not creditnote.active
        creditnote.save()

        # Determine the new status
        new_status = "Active" if creditnote.active else "Inactive"

        return JsonResponse({"success": True, "newStatus": new_status})

    except Exception as e:
        print(str(e))
        return JsonResponse({"success": False})
        
        
def add_comment_cust(request,id):
    if request.method == 'POST':
        bill = customer.objects.get(id=id) 
        bill.comments = request.POST['comment']
        bill.save()
        return redirect('view_one_customer',id=id)
        
def amtcus(request):
    company=company_details.objects.get(user=request.user)
    vc= customer.objects.filter(user=request.user).order_by('OpeningBalance')
    context = {
        'vc': vc,
        "company":company,
    }
    return render(request, 'view_customer.html', context)
    
    
def payment_terms_cust(request):        #update
    if request.method == 'POST':
        terms = request.POST.get('name')
        day = request.POST.get('days')
        ptr = payment_terms(Terms=terms, Days=day)
        ptr.save()
        response_data = {
            "message": "success",
            "terms": terms,
        }
        return JsonResponse(response_data)
        
        
def customer_active(request,id):
    p=customer.objects.get(id=id)
    if p.status == 'Active':
        p.status = 'Inactive'
    else:
        p.status = 'Active'
    p.save()
    return redirect('view_one_customer',id=id)
    
    
def active_cust(request):
    company=company_details.objects.get(user=request.user)
    user = request.user
    vc= customer.objects.filter(status='Active',user=user)
    context = {
        'vc': vc,
        "company":company,
    }
    return render(request, 'view_customer.html', context)
    

def inactive_cust(request):
    company=company_details.objects.get(user=request.user)
    user = request.user
    vc= customer.objects.filter(status='Inactive',user=user)   
    context = {
        'vc': vc,
        "company":company,
    }
    return render(request, 'view_customer.html', context)
    
    
def cust_sname(request,id):
    company = company_details.objects.get(user=request.user)
    cmp1 = company_details.objects.get(user=request.user)
    cu=customer.objects.get(id=id)
    vc = customer.objects.filter(user=request.user).order_by('customerName')
    context = {
        'cu':cu,
        'vc':vc,
        'cmp1': cmp1,
        "company":company,
    }
    return render(request, 'view_one_customer.html', context)
    
    
def cust_amt(request,id):
    company = company_details.objects.get(user=request.user)
    cmp1 = company_details.objects.get(user=request.user)
    cu=customer.objects.get(id=id)
    vc = customer.objects.filter(user=request.user).order_by('OpeningBalance')
    context = {
        'cu':cu,
        'vc':vc,
        'cmp1': cmp1,
        "company":company,
    }
    return render(request, 'view_one_customer.html', context)
    
    
def emailattachment_cust(request):

        if request.method == 'POST':
                
            subject =request.POST['subject']
            message = request.POST['messege']
            email = request.POST['email']
            files = request.FILES.getlist('attach')

            try:
                mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email])
                for f in files:
                    mail.attach(f.name, f.read(), f.content_type)
                mail.send()
                return render(request, 'customermail.html')
            except:
               return render(request, 'customermail.html')

        return render(request, 'customermail.html')
        
        
def new_recur1(request):
    if request.method=='POST':
        
        custname=request.POST.get('customer')
        cus=customer.objects.get(customerName=custname)   
        custo=cus.id
        cusemail=request.POST.get('mails')
        cusadd=request.POST.get('addr')
        gsttr=request.POST.get('gst')
        gstn=request.POST.get('gstnum')
        pos=request.POST.get('supply')
        e_type=request.POST.get('type')
        profile=request.POST.get('name')
        invoice=request.POST.get('recurno')
        onumber=request.POST.get('order')
        repeat=request.POST.get('every')
        pay_method=request.POST.get('method')
        sdate=request.POST.get('start')
        edate=request.POST.get('end')
        pay=request.POST.get('terms')
        pay_term_type =request.POST.get('terms_data_source')
        print(pay_term_type)
        notes=request.POST.get('customer_note')
        terms=request.POST.get('ter_cond')
        attach=request.POST.get('file')
        sub=request.POST.get('subtotal')
        i=request.POST.get('igst')
        c=request.POST.get('cgst')
        s=request.POST.get('sgst')
        taxamt=request.POST.get('total_taxamount')
        ship=request.POST.get('shipping_charge')
        adj=request.POST.get('adjustment_charge')
        tot=request.POST.get('total')
        paid=request.POST.get('paids')
        balance=request.POST.get('balance')
        status='Draft'
       
        recur=Recurring_invoice(
            cname=custname,
            cemail=cusemail,
            cadrs=cusadd,
            gsttr=gsttr,
            gstnum=gstn,
            reinvoiceno=invoice,
            p_supply=pos,
            entry_type=e_type,
            name=profile,
            order_num=onumber,
            every=repeat,
            payment_method=pay_method,
            start=sdate,
            end=edate,
            terms=pay,
            payment_type=pay_term_type,
            attachment=attach,
            cust_note=notes,
            conditions=terms,
            sub_total=sub,
            igst=i,
            cgst=c,
            sgst=s,
            tax_amount=taxamt,
            shipping_charge=ship,
            adjustment=adj,
            total=tot,
            paid=paid,
            status=status,
            balance=balance,
            user = request.user,
            cust_name_id=custo,

        )
        recur.save()
        items=request.POST.getlist('item[]')
        print(items)
        quantity1 = request.POST.getlist('quantity[]')
        quantity = [float(x) for x in quantity1]
        print(quantity)
        hsnc1 = request.POST.getlist('hsn[]')
        hsnc = [float(x) for x in hsnc1]
        rate1 = request.POST.getlist('rate[]')
        rate = [float(x) for x in rate1]
        print(rate)
        discount1 = request.POST.getlist('discount[]')
        discount = [float(x) for x in discount1]
        print(discount)
        tax1 = request.POST.getlist('tax[]')
        tax = [float(x) for x in tax1]
        print(tax)
        amount1 = request.POST.getlist('amount[]')
        amount = [float(x) for x in amount1]
        print(amount)
        
        if len(items)==len(quantity)==len(hsnc)==len(rate)==len(discount)==len(tax)==len(amount):
            print('testing')
            print(items)
            print(quantity)
            print(rate)
            print(discount)
            print(tax)
            print(amount)
            mapped1 = zip(items,quantity,hsnc,rate,discount,tax,amount)
            mapped = list(mapped1)
            for element in mapped:
                created =recur_itemtable.objects.get_or_create(
                    iname=element[0], quantity=element[1],hsncode=element[2], rate=element[3], discount=element[4], tax=element[5],amt=element[6],ri=recur)
        
                
        return redirect('view_recurpage')
    else:
        return render(request,'samrecurpage.html')
        
        
def add_comment_recur(request,id):
    if request.method == 'POST':
        bill = Recurring_invoice.objects.get(id=id) 
        bill.comments = request.POST['comment']
        bill.save()
        return redirect('viewrecur',id = id)
        
        
def profilename(request):
    company = company_details.objects.get(user=request.user)
    cmp1 = company_details.objects.get(user=request.user)
    rec_bill = Recurring_invoice.objects.filter(user=request.user).order_by('name')
    context = {
        'recur': rec_bill,
        'cmp1': cmp1,
        "company":company,
    }
    return render(request, 'recurringonvoice.html', context)
    
    
def customerasc(request):
    company = company_details.objects.get(user=request.user)
    cmp1 = company_details.objects.get(user=request.user)
    rec_bill = Recurring_invoice.objects.filter(user=request.user).order_by('cname')
    context = {
        'recur': rec_bill,
        'cmp1': cmp1,
        "company":company,
    }
    return render(request, 'recurringonvoice.html', context)
    
    
def amtasc(request):
    company = company_details.objects.get(user=request.user)
    cmp1 = company_details.objects.get(user=request.user)
    rec_bill = Recurring_invoice.objects.filter(user=request.user).order_by('total')
    context = {
        'recur': rec_bill,
        'cmp1': cmp1,
        "company":company,
    }
    return render(request, 'recurringonvoice.html', context)      
    
    
def recurname(request,id):
    company = company_details.objects.get(user=request.user)
    cmp1 = company_details.objects.get(user=request.user)
    product=Recurring_invoice.objects.get(id=id)

    rec_bill = Recurring_invoice.objects.filter(user=request.user).order_by('cname')
    context = {
        'allproduct': rec_bill,
        'cmp1': cmp1,
        "company":company,
        "product":product,
    }
    return render(request, 'recur_invoice.html', context)
    
    
def recuramt(request,id):
    company = company_details.objects.get(user=request.user)
    cmp1 = company_details.objects.get(user=request.user)
    product=Recurring_invoice.objects.get(id=id)
    rec_bill = Recurring_invoice.objects.filter(user=request.user).order_by('total')
    context = {
        'allproduct': rec_bill,
        'cmp1': cmp1,
        "company":company,
        "product":product,
    }
    return render(request, 'recur_invoice.html', context)
    
    
def draft_to_save(request,id):
    drf=Recurring_invoice.objects.get(id=id)
    drf.status='Save'
    drf.save()
    return redirect('viewrecur',id)
    
    
def delete_customer(request,id):
    user=request.user
    company = company_details.objects.get(user=user)
    customers=customer.objects.get(id=id)
    personal=customer_contact_person_table.objects.filter(Customr=customers)
    customers.delete()
    personal.delete()
    
    
def get_repeat_every(request):
    if request.method == 'POST':
        every = request.POST.get('repeatname')
        repeat_item = repeat_every(Terms=every)
        repeat_item.save()

        # Get all items from the database
        repeat_list = repeat_every.objects.all()
        
        options = {option.id: [option.id, option.Terms] for option in repeat_list}
        

    return JsonResponse(options, safe=False)
    
    
@login_required(login_url='login')
def inventory_adjustment(request):
    user=request.user.id
    company_data = company_details.objects.get(user=request.user)
    adjustment=Adjustment.objects.filter(user_id=user)
    return render(request,'inventory_adjustment.html',{'company': company_data,'adjustment':adjustment})

@login_required(login_url='login')
def new_adjustment(request):
    user = request.user
    accounts=Chart_of_Account.objects.all()
    company_data = company_details.objects.get(user=request.user)
    items = AddItem.objects.filter(user_id=user.id)
    sales=Sales.objects.all()
    purchase=Purchase.objects.all()
    unit=Unit.objects.all()
    reason=Reason.objects.all()
    return render(request,'new_adjustment.html',{'company': company_data,'accounts':accounts,'items':items,'sales':sales,'purchase':purchase,'units':unit,'reason':reason})


@login_required(login_url='login')
def newreasons(request):
    if request.method == 'POST':
        newreason= request.POST.get('reasonlist')
        print(newreason,'reason')
        reasons=Reason(reason=newreason)
        reasons.save()
        return JsonResponse({"message": "success"})


def newreasonslist(request):
    print('hello')
    rson={}
    reasons=Reason.objects.all()
    for r in reasons:
        rson[r.id]= r.reason
    return JsonResponse(rson)


def save_adjustment(request):
     if request.method=='POST':
         typeof_adjustment=request.POST.get('type','')
         ref_no=request.POST['refno']
         date=request.POST['date']
         account=request.POST['account']
         reason=request.POST['reason']

         print(f"reason: {reason}")

         description = request.POST['description']
         user_id = request.user.id 
         account_instance = Chart_of_Account.objects.get(id=account)
         user_instance = User.objects.get(id=user_id) 
         reason_instance = Reason.objects.get(reason=reason)
         reason_id = reason_instance.id
         company = company_details.objects.get(user=request.user)

         adjustment = Adjustment.objects.create(
            user=user_instance,
            type=typeof_adjustment,
            adjustment_type=typeof_adjustment,
            reference_number=ref_no,
            date=date,
            account=account_instance,
            reason=reason_instance,
            description=description,
            company=company
                  
            
        )
         adjustment.save()

         if typeof_adjustment == 'Quantity':
             item_names = request.POST.getlist('item[]')
             qty_available = request.POST.getlist('qtyav[]')
             new_qty_on_hand = request.POST.getlist('newqty[]')

             print(new_qty_on_hand,"new_qty_on_hand is")
             qty_adjusted = request.POST.getlist('qtyadj[]')

             if len(item_names) == len(qty_available) == len(new_qty_on_hand) == len(qty_adjusted):
                for i in range(len(item_names)):

                    item_instance = AddItem.objects.get(Name=item_names[i])
                    item_instance.stock += int(new_qty_on_hand[i])
                    item_instance.save()

                    items1 = ItemAdjustment.objects.create(
                        item=item_names[i],
                        quantity_available=qty_available[i],
                        new_quantity_on_hand=new_qty_on_hand[i],
                        adjusted_quantity=qty_adjusted[i],
                        adjustment_type=typeof_adjustment,
                        adjustment=adjustment,
                        user=user_instance,
                    )
                    items1.save()

         elif typeof_adjustment == 'Value':
             items_names = request.POST.getlist('item2[]')
             current_value = request.POST.getlist('cuval[]')
             changed_value = request.POST.getlist('chval[]')
             value_adjusted = request.POST.getlist('adjval[]')

             if len(items_names) == len(current_value) == len(changed_value) == len(value_adjusted):
                for j in range(len(items_names)):
                    items2 = ItemAdjustment.objects.create(
                        item=items_names[j],
                        current_value=current_value[j],
                        changed_value=changed_value[j],
                        adjusted_value=value_adjusted[j],
                        adjustment_type=typeof_adjustment,
                        adjustment=adjustment,
                        user=user_instance,       
                    )
                    items2.save()

         if 'save_draft' in request.POST:
            adjustment.status = "Draft"

         elif 'convert_adjusted' in request.POST:
             adjustment.status = "Adjusted"

         adjustment.save()   
     return redirect("inventory_adjustment")
             
             
             
   
def inv_overview(request,id):
    users1=request.user.id
    user=request.user
    alladj=Adjustment.objects.filter(user=user)
    adj=Adjustment.objects.get(id=id)
    adjItems=ItemAdjustment.objects.filter(adjustment=adj)
    company_data = company_details.objects.get(user=users1)
    inv_comments=Inventory_adj_comments.objects.filter(adjustment=adj.id,user=user)
    return render(request,'inventory_overview.html',{'alladj':alladj,'company':company_data,'adj':adj,'adjItems':adjItems,'inv_comments':inv_comments})
        


def add_inv_comment(request,id):
    if request.method=='POST':
        user=request.user
        adj=Adjustment.objects.get(id=id)
        comment=Inventory_adj_comments()
        comment.user=user
        comment.adjustment=adj
        comment.comments=request.POST.get('comments')
        comment.save()
        return redirect('inv_overview',adj.id)



def change_inventory_status(request,id):
    adj=Adjustment.objects.get(id=id)
    if adj.status == 'Draft':
        adj.status = 'Adjusted'
        adj.save()
    else:
        adj.status = 'Adjusted'
        adj.save()
    return redirect(inv_overview,adj.id)

def delete_inventory(request,id):
    adj=Adjustment.objects.get(id=id)
    adjItems=ItemAdjustment.objects.filter(adjustment=adj)
    adjItems.delete()
    adj.delete()
    return redirect('inventory_adjustment')

    
def filterby_draft(request,id):
    user=request.user
    alladj=Adjustment.objects.filter(user=user,status='Draft')
    adj=Adjustment.objects.get(id=id)
    adjItems=ItemAdjustment.objects.filter(adjustment=adj)
    company = company_details.objects.get(user=request.user)
    return render(request,'inventory_overview.html',{'alladj':alladj,'adj':adj,'adjItems':adjItems,'company':company})


  
def filterby_adjusted(request,id):
    user=request.user
    alladj=Adjustment.objects.filter(user=user,status='Adjusted')
    adj=Adjustment.objects.get(id=id)
    adjItems=ItemAdjustment.objects.filter(adjustment=adj)
    company = company_details.objects.get(user=request.user)
    return render(request,'inventory_overview.html',{'alladj':alladj,'adj':adj,'adjItems':adjItems,'company':company})




def edit_inventory(request,id):
    user=request.user
    company=company_details.objects.get(user=user)
    items = AddItem.objects.filter(user_id=user.id)
    adj=Adjustment.objects.get(id=id)
    print(adj.description,'date')
    items = AddItem.objects.filter(user_id=user.id)
    accounts=Chart_of_Account.objects.all()
    adj_items=ItemAdjustment.objects.filter(adjustment=adj)
    reason=Reason.objects.all()
    unit=Unit.objects.all()
    sales=Sales.objects.all()
    purchase=Purchase.objects.all()
    value =[]
    for adjustment in adj_items:
        print(adjustment.adjustment_type, 'item type')
        value=adjustment.adjustment_type
        val=adjustment.current_value
        print(val,'val')
    print(value,'value is ')
    return render(request,'edit_adjustment.html',{'company':company,'adj':adj,'accounts':accounts,'items':items,'adj_items':adj_items,'value':value,'reason':reason,'units':unit,'sales':sales,'purchase':purchase})
  

    
def update_adjustment(request,id):
    user=request.user
    user_id=request.user.id
    user_instance = User.objects.get(id=user_id)
    if request.method=='POST':
        adjustment=Adjustment.objects.get(id=id)
        adjustment.user=user_instance
        adjustment.type=request.POST.get('type','')
        adjustment.adjustment_type=request.POST.get('type','')
        adjustment.reference_number=request.POST['refno']
        adjustment.date=request.POST['date']
        account=request.POST['account']
        account_instance = Chart_of_Account.objects.get(id=account)
        adjustment.account=account_instance
        reason=request.POST['reason']
        reason_instance=Reason.objects.get(reason=reason)
        adjustment.reason=reason_instance
        adjustment.description=request.POST['description']
        company = company_details.objects.get(user=user)
        adjustment.company=company
        adjustment.save()
        itemadjustment = ItemAdjustment.objects.filter(adjustment_id=adjustment.id)
        itemadjustment.delete()
        
        if adjustment.adjustment_type == 'Quantity':
             item_names = request.POST.getlist('item[]')
             qty_available = request.POST.getlist('qtyav[]')
             new_qty_on_hand = request.POST.getlist('newqty[]')
             qty_adjusted = request.POST.getlist('qtyadj[]')

             if len(item_names) == len(qty_available) == len(new_qty_on_hand) == len(qty_adjusted):
                for i in range(len(item_names)):
                    item_instance = AddItem.objects.get(Name=item_names[i])
                    item_instance.stock += int(float(new_qty_on_hand[i]))
                    item_instance.save()
                    items1 = ItemAdjustment.objects.create(
                        item=item_names[i],
                        quantity_available=qty_available[i],
                        new_quantity_on_hand=new_qty_on_hand[i],
                        adjusted_quantity=qty_adjusted[i],
                        adjustment_type=adjustment.adjustment_type,
                        adjustment=adjustment,
                        user=user_instance,
                    )

                    items1.save()
        elif adjustment.adjustment_type == 'Value':
             items_names = request.POST.getlist('item2[]')
             current_value = request.POST.getlist('cuval[]')
             changed_value = request.POST.getlist('chval[]')
             value_adjusted = request.POST.getlist('adjval[]')
             if len(items_names) == len(current_value) == len(changed_value) == len(value_adjusted):
                for j in range(len(items_names)):
                    items2 = ItemAdjustment.objects.create(
                        item=items_names[j],
                        current_value=current_value[j],
                        changed_value=changed_value[j],
                        adjusted_value=value_adjusted[j],
                        adjustment_type=adjustment.adjustment_type,
                        adjustment=adjustment,
                        user=user_instance,       
                    )
                    items2.save()
        if 'save_draft' in request.POST:
            adjustment.status = "Draft"

        elif 'convert_adjusted' in request.POST:
             adjustment.status = "Adjusted"

        adjustment.save()
    return redirect("inv_overview",id)
    
    
#------------------------------reports-Profit and Loss & Profit and Loss (schedule lll)-------Merlin------------------------#
def profit_and_loss(request):
    customer1 = customer.objects.all()
    company = company_details.objects.get(user=request.user)
    print(range(2,24))
    return render(request, 'profit_and_loss.html', {'cust': customer1, 'company': company})


def profit_and_loss_customize_report(request):
    customer1 = customer.objects.all()
    company = company_details.objects.get(user=request.user)
    return render(request, 'profit_and_loss_customize_report.html', {'cust': customer1, 'company': company,"range":range(2,24)},)

def prft_and_ls_custmz_rprt_shw_hide(request):
    customer1 = customer.objects.all()
    company= company_details.objects.get(user=request.user)
    return render(request, 'prft_n_lss_custmz_rprt_shw_hide.html', {'cust': customer1, 'company': company},)
    
def profit_and_loss_schedule_III(request):
    customer1 = customer.objects.all()
    company= company_details.objects.get(user=request.user)
    return render(request, 'profit_and_loss_schedule_iii.html', {'cust': customer1, 'company': company},)

def profit_and_loss_scedule_iii_customize_report(request):
    customer1 = customer.objects.all()
    company = company_details.objects.get(user=request.user)
    return render(request, 'profit_and_loss_scedule_iii_customize_report.html', {'cust': customer1, 'company': company},)

def profit_and_loss_pdf(request):
    customer1 = customer.objects.all()
    company= company_details.objects.get(user=request.user)
    
    template_path = 'profit_and_loss_pdf.html'
    context = {
        'customer':customer1,
        'company': company,
    }
    # Create a Django response object, and specify content_type as pdftemp_creditnote
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="profit_and_loss_report.pdf"'
    #response['Content-Disposition'] =f'attachment; filename= {fname}.pdf'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response   

def profit_and_loss_schedule_III_pdf(request):
    customer1 = customer.objects.all()
    company= company_details.objects.get(user=request.user)
    
    template_path = 'profit_and_loss_schedule_III_pdf.html'
    context = {
        'customer':customer1,
        'company': company,
    }
    # Create a Django response object, and specify content_type as pdftemp_creditnote
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="profit_and_loss_schedule_iii_report.pdf"'
    #response['Content-Disposition'] =f'attachment; filename= {fname}.pdf'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


#--End--

def recurinvoice_customer(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':
        cust_type = request.POST.get('customer_type')
        fname=request.POST.get('firstname')
        lname=request.POST.get('lastname')

        name = request.POST.get('display_name')
        comp_name = request.POST.get('company_name')
        email=request.POST.get('email')
        website=request.POST.get('website')
        w_mobile=request.POST.get('work_mobile')
        p_mobile=request.POST.get('pers_mobile')
        fb = request.POST.get('facebook')
        twitter = request.POST.get('twitter')
        skype = request.POST.get('skype')
        desg = request.POST.get('desg')
        dpt = request.POST.get('dpt')
        gsttype=request.POST.get('gsttype')
        gstnm=request.POST.get('gstin')
        print(gstnm)
        pan=request.POST.get('panno')
        print(pan)
        supply=request.POST.get('placesupply')
        print('table',supply)
        tax = request.POST.get('tax_preference')
        currency=request.POST.get('currency')
        payment=request.POST.get('paymentterms')
        street1=request.POST.get('street')
        street2=request.POST.get('street')
        city=request.POST.get('city')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
        country=request.POST.get('country')
        fax=request.POST.get('fax')
        phone=request.POST.get('phone')
        status='Active'
        balance= float(request.POST.get('openingbalance', 0.0))
        baltype=request.POST.get('crdb')
        if baltype=='credit':
            balance = -balance
        else:
            balance=balance

        u = User.objects.get(id = request.user.id)

        cust = customer(customerName = name,customerType = cust_type, Fname=fname,Lname=lname,companyName= comp_name, GSTTreatment=gsttype, 
                        customerWorkPhone = w_mobile,customerMobile = p_mobile, customerEmail=email,skype = skype,Facebook = fb, 
                        Twitter = twitter,placeofsupply=supply,Taxpreference = tax,currency=currency, website=website, 
                        designation = desg, department = dpt,OpeningBalance=balance,cr_dr=baltype,GSTIN=gstnm,pan_no=pan,Address1=street1,Address2=street2, city=city, 
                        state=state, PaymentTerms=payment,zipcode=pincode,country=country,  fax = fax,  phone1 = phone,status = status,user = u)
        cust.save()

        return HttpResponse({"message": "success"})
        
        
#____________________horizontal profit and loss___________________
def horizontal_profit_and_loss(request):
    company = company_details.objects.get(user = request.user.id)
    return render(request,'horizontal_profit&loss.html',{'company':company})

def customize_report_hpl(request):
    company = company_details.objects.get(user = request.user.id)
    return render(request,'customize_report_hpl.html',{"company":company})

#_______________________balance sheet (schedule 3)______________________

def balance_sheet_sthree(request):
    company = company_details.objects.get(user = request.user.id)
    return render(request,'balance_sheet_schedule_3.html',{'company':company})

def customize_report_bss3(request):
    company = company_details.objects.get(user = request.user.id)
    return render(request,'customize_report_bss3.html',{'company':company})
    
    
def view_vendor_active(request):
    company=company_details.objects.get(user=request.user)
    user_id=request.user.id
    udata=User.objects.get(id=user_id)
    data=vendor_table.objects.filter(user=udata,status='Active').order_by('-id')
    return render(request,'vendor_list.html',{'data':data,'company':company})
    
def view_vendor_inactive(request):
    company=company_details.objects.get(user=request.user)
    user_id=request.user.id
    udata=User.objects.get(id=user_id)
    data=vendor_table.objects.filter(user=udata,status='Inactive').order_by('-id')
    return render(request,'vendor_list.html',{'data':data,'company':company})

def sort_vendor_by_name(request):
    company=company_details.objects.get(user=request.user)
    user_id=request.user.id
    udata=User.objects.get(id=user_id)
    data=vendor_table.objects.filter(user=udata).order_by('first_name')
    return render(request,'vendor_list.html',{'data':data,'company':company})

def sort_vendor_by_amount(request):
    company=company_details.objects.get(user=request.user)
    user_id=request.user.id
    udata=User.objects.get(id=user_id)
    data=vendor_table.objects.filter(user=udata).order_by('opening_bal')
    return render(request,'vendor_list.html',{'data':data,'company':company})


def sort_vendor_by_name_det(request,pk):
    company=company_details.objects.get(user=request.user)
    user_id=request.user.id
    udata=User.objects.get(id=user_id)
    vdata1=vendor_table.objects.filter(user=udata).order_by('first_name')
    vdata2=vendor_table.objects.get(id=pk)
    mdata=mail_table.objects.filter(vendor=vdata2)
    ddata=doc_upload_table.objects.filter(user=udata,vendor=vdata2)
    cmt_data=comments_table.objects.filter(user=udata,vendor=vdata2)
    contact_persons = contact_person_table.objects.filter(user=udata,vendor=vdata2)

    fname = vdata2.first_name
    lname = vdata2.last_name
    fullname = fname + ' ' + lname
    v_email = vdata2.vendor_email
    name_and_id = fullname +' '+ str(vdata2.id) 
    id_and_name = str(vdata2.id) +' '+ fullname  

    print(fname)
    print(lname)
    print(fullname)
    print(v_email)
    print(name_and_id)

    expence = ExpenseE.objects.filter(user = udata,vendor_id = pk)
    recurring_expense = Expense.objects.filter(vendor_id = pk)
    purchase_ordr = Purchase_Order.objects.filter(user = udata,vendor_name = name_and_id)
    paymnt_made = payment_made.objects.filter(user = udata,vendor_id = pk)
    purchase_bill = PurchaseBills.objects.filter(user = udata,vendor_name = fullname,vendor_email = v_email)
    recurring_bill = recurring_bills.objects.filter(user = udata,vendor_name = id_and_name)

    context = {
        'company':company,
        'vdata':vdata1,
        'vdata2':vdata2,
        'mdata':mdata,
        'ddata':ddata,
        'cmt_data':cmt_data,
        'contact_persons':contact_persons,
        'expence':expence,
        'recurring_expense':recurring_expense,
        'purchase_ordr':purchase_ordr,
        'paymnt_made':paymnt_made,
        'purchase_bill':purchase_bill,
        'recurring_bill':recurring_bill,

    }

    return render(request,'vendor_details.html',context)

def sort_vendor_by_amount_det(request,pk):
    company=company_details.objects.get(user=request.user)
    user_id=request.user.id
    udata=User.objects.get(id=user_id)
    vdata1=vendor_table.objects.filter(user=udata).order_by('opening_bal')
    vdata2=vendor_table.objects.get(id=pk)
    mdata=mail_table.objects.filter(vendor=vdata2)
    ddata=doc_upload_table.objects.filter(user=udata,vendor=vdata2)
    cmt_data=comments_table.objects.filter(user=udata,vendor=vdata2)
    contact_persons = contact_person_table.objects.filter(user=udata,vendor=vdata2)

    fname = vdata2.first_name
    lname = vdata2.last_name
    fullname = fname + ' ' + lname
    v_email = vdata2.vendor_email
    name_and_id = fullname +' '+ str(vdata2.id) 
    id_and_name = str(vdata2.id) +' '+ fullname  

    print(fname)
    print(lname)
    print(fullname)
    print(v_email)
    print(name_and_id)

    expence = ExpenseE.objects.filter(user = udata,vendor_id = pk)
    recurring_expense = Expense.objects.filter(user = udata,vendor_id = pk)
    purchase_ordr = Purchase_Order.objects.filter(user = udata,vendor_name = name_and_id)
    paymnt_made = payment_made.objects.filter(user = udata,vendor_id = pk)
    purchase_bill = PurchaseBills.objects.filter(user = udata,vendor_name = fullname,vendor_email = v_email)
    recurring_bill = recurring_bills.objects.filter(user = udata,vendor_name = id_and_name)

    context = {
        'company':company,
        'vdata':vdata1,
        'vdata2':vdata2,
        'mdata':mdata,
        'ddata':ddata,
        'cmt_data':cmt_data,
        'contact_persons':contact_persons,
        'expence':expence,
        'recurring_expense':recurring_expense,
        'purchase_ordr':purchase_ordr,
        'paymnt_made':paymnt_made,
        'purchase_bill':purchase_bill,
        'recurring_bill':recurring_bill,

    }

    return render(request,'vendor_details.html',context)
    
    
    
@login_required(login_url='login')
def new_item(request):
    company = company_details.objects.get(user = request.user)
    if request.method=='POST':
        type=request.POST.get('type')
        name=request.POST['name']
        ut=request.POST['unit']

        print('ut',ut)

        inter=request.POST['inter']
        intra=request.POST['intra']
        sell_price=request.POST.get('sell_price')
        sell_acc=request.POST.get('sell_acc')
        sell_desc=request.POST.get('sell_desc')
        cost_price=request.POST.get('cost_price')
        cost_acc=request.POST.get('cost_acc')      
        cost_desc=request.POST.get('cost_desc')
        units=Unit.objects.get(unit=ut)
        sel=Sales.objects.get(id=sell_acc)
        cost=Purchase.objects.get(id=cost_acc)
        stock=request.POST.get('openstock')
        rate=request.POST.get('inventoryaccntperunit')
        status_stock=request.POST.get('satus',0)
        invacc=request.POST.get('invacc')
        history="Created by " + str(request.user)
        user = User.objects.get(id = request.user.id)
        item=AddItem(type=type,unit=units,sales=sel,purchase=cost,Name=name,p_desc=cost_desc,s_desc=sell_desc,s_price=sell_price,p_price=cost_price,
                    user=user,creat=history,interstate=inter,intrastate=intra,stock=stock,rate=rate,status_stock=status_stock,invacc=invacc)

        item.save()
        return HttpResponse({"message": "success"})
    


  
@login_required(login_url='login')        
def new_item_dropdown(request):
    user = User.objects.get(id=request.user.id) 
    options = {}
    option_objects = AddItem.objects.all()
    for option in option_objects:
         options[option.id] = {
            'name': option.Name,
            'stock': option.stock,  
            'rate': option.rate,   
        }
    return JsonResponse(options, safe=False)

# nasneen o m

def projfile_download(request,aid):
    att= projectfiles.objects.get(id=aid)
    file = att.attachment
    response = FileResponse(file)
    response['Content-Disposition'] = f'attachment; filename="{file.name}"'
    return response
    
def projdeletefile(request,aid):
    att=projectfiles.objects.get(id=aid)
    p=att.proj
    att.delete()
    return redirect('overview',p.id)

def holidays(request,date):
    company = company_details.objects.get(user=request.user)
    all_events = Events.objects.all()
    event_counts = {}
    event_dict = {}
    print(date)
    month_name, year = date.split('-')
    print(month_name)
    print(year)

    # Create a datetime object for the start of the specified month
    month_number = list(calendar.month_abbr).index(month_name[:3])
    start_date = datetime(year=int(year), month=month_number, day=1)
    if month_number == 12:
        end_date = start_date.replace(month=1, year=start_date.year + 1)
    else:
        end_date = start_date.replace(month=month_number + 1)
    end_date -= timedelta(days=1)  


    events = Events.objects.filter(start__gte=start_date, start__lt=end_date)

    # Create a dictionary to store the events by day
    
    for event in events:
        day = event.start.day
        if day in event_dict:
            event_dict[day].append(event.name)
        else:
            event_dict[day] = [event.name]
    for event in all_events:
        month_year = event.start.strftime('%Y-%m')  # Format: 'YYYY-MM'
    
    # If the month_year is not in the dictionary, add it with a count of 1
        if month_year not in event_counts:
            event_counts[month_year] = 1
        else:
        # If the month_year is already in the dictionary, increment the count
            event_counts[month_year] += 1
    event_counts_json = json.dumps(event_counts)
    print(date)
    default = month_name+" "+year
    context = {
        "events": all_events,
        "event_counts_json": event_counts_json,
        "company":company,
        "default":default,
        "event_dict":event_dict,
        "eve":events,
    }
    return render(request, 'holidays.html',context)

def all_events(request):                                                                                                 
    all_events = Events.objects.all()                                                                                    
    out = []                                                                                                             
    for event in all_events:                                                                                             
        out.append({                                                                                                     
            'title': event.name,                                                                                         
            # 'id': event.id,                                                                                              
            'start': event.start.date(),                                                         
            'end': event.end.date(), 
            # 'rendering': 'background',
            'color': 'red',
            'allDay': 'true',
                                                                       
        })   
                                                                                                                      
    return JsonResponse(out, safe=False)  
 
def add_holiday(request):
    if request.method=='POST':
        title = request.POST['title']
        start = request.POST['start']
        end = request.POST['end']
    
        event = Events(name=title, start=start, end=end)
        event.save()
        print("========================saved")
        return redirect('holiday_list')
    return redirect('holiday_list')
    
 

def remove(request,id):
    event = Events.objects.get(id=id)                                                                                    
    event.delete()
    return redirect('holiday_list')


def create_emp(request):
    if request.method=='POST':
        title=request.POST['title']
        fname=request.POST['fname']
        lname=request.POST['lname']
        alias=request.POST['alias']
        joindate=request.POST['joindate']
        saltype=request.POST['saltype']
        if (saltype == 'Fixed'):
            salary=request.POST['fsalary']
        else:
            salary=request.POST['vsalary']
        image=request.FILES.get('file')
        if image == None:
            image="image/img.png"
        empnum=request.POST['empnum']
        designation = request.POST['designation']
        location=request.POST['location']
        gender=request.POST['gender']
        dob=request.POST['dob']
        blood=request.POST['blood']
        fmname=request.POST['fm_name']
        sname=request.POST['s_name']        
        add1=request.POST['address']
        add2=request.POST['address2']
        address=add1+" "+add2
        padd1=request.POST['paddress'] 
        padd2=request.POST['paddress2'] 
        paddress= padd1+padd2
        phone=request.POST['phone']
        ephn=request.POST['ephone']
        if ephn=="":
            ephone=None
        else:
            ephone=request.POST['ephone']
        email=request.POST['email']
        isdts=request.POST['tds']
        if isdts == '1':
            istdsval=request.POST['pora']
            if istdsval == 'Percentage':
                tds=request.POST['pcnt']
            elif istdsval == 'Amount':
                tds=request.POST['amnt']
        else:
            istdsval='No'
            tds = 0
        itn=request.POST['itn']
        an=request.POST['an']        
        uan=request.POST['uan'] 
        pfn=request.POST['pfn']
        pran=request.POST['pran']
        payroll= Payroll(title=title,first_name=fname,last_name=lname,alias=alias,image=image,joindate=joindate,salary_type=saltype,salary=salary,emp_number=empnum,designation=designation,location=location,
                         gender=gender,dob=dob,blood=blood,parent=fmname,spouse_name=sname,address=address,permanent_address=paddress ,Phone=phone,emergency_phone=ephone,
                         email=email,ITN=itn,Aadhar=an,UAN=uan,PFN=pfn,PRAN=pran,isTDS=istdsval,TDS=tds)
        payroll.save()

        bank=request.POST['bank']
        if(bank == '1'):
            accno=request.POST['acc_no']       
            ifsc=request.POST['ifsc']       
            bname=request.POST['b_name']       
            branch=request.POST['branch']
            ttype=request.POST['ttype']
            b=Bankdetails(payroll=payroll,acc_no=accno,IFSC=ifsc,bank_name=bname,branch=branch,transaction_type=ttype)
            b.save()
        attach=request.FILES.get('attach')       
        if(attach):
            att=Payrollfiles(attachment=attach,payroll=payroll)
        # messages.success(request,'Saved succefully !')
        print(bank)
        options = {}
        option_objects = Payroll.objects.all()
        for option in option_objects:
            options[option.id] = [option.id , option.first_name , option.last_name]
        return JsonResponse(options) 
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def getemployee(request):
    employeeid = request.GET.get('id')
    # print(customer_id)
    payroll = Payroll.objects.get(id=employeeid)
    data7 = {'email': payroll.email}
    
    print(data7)
    return JsonResponse(data7)


def project_file(request,id):
    print("kjhhkkkkjhhhhhhhhhhhhhhhhh")
    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]
        proj=project1.objects.get(id=id)
        p=projectfiles(attachment=uploaded_file,proj=proj)
        p.save()
        print("hellooooooooooooooooo")
        return redirect('overview',id)
    else:
        return redirect('overview',id)
    
def add_projectcomment(request,id):
    p=project1.objects.get(id=id)
    if request.method== 'POST':
        comment=request.POST['comments']
        c= projectcomment(comment=comment,proj=p)
        c.save()
        print("=====================================dddddddddddd")
    return redirect('overview',id)

def delete_projectcomment(request,cid):
    
    try:
        comment = projectcomment.objects.get(id=cid)
        p=comment.proj
        # pr=project1.objects.get(id=p)
        print("================================")
        comment.delete()
        return redirect('overview', p.id)
    except:
        return redirect('overview', p.id)

        
def project_summary(request):
    company = company_details.objects.get(user=request.user)
    project = project1.objects.filter(user=request.user)
    taskz=task.objects.all()
    for t in taskz:
        usern=usernamez.objects.get(projn=t.proj)
        emp= Payroll.objects.get(id=usern.usernamez)
        fname= emp.first_name
        lname = emp.last_name
        t.username = fname+ " "+lname
        t.useremail=usern.emailz
        
    return render(request,'project_summary.html',{'company':company,'taskz':taskz})
    

def get_item_details(request):
    id = request.GET.get('id')

    try:
        item = AddItem.objects.get(id=id)
        hsn = item.hsn
        rate = item.s_price 

        data = {
            'hsn': hsn,
            'rate': rate,
        }

        return JsonResponse(data)
    except AddItem.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)


def purchase_item_credit(request):

    company = company_details.objects.get(user = request.user)
    print('purchase_item')

    if request.method=='POST':
        
        type=request.POST.get('type')
        
        name=request.POST['name']
        
        ut=int(request.POST.get('unit'))
        
        inter=request.POST['inter']
        
        intra=request.POST['intra']
        
        sell_price=request.POST.get('sell_price')
        
        sell_acc=request.POST.get('sell_acc')
        
        sell_desc=request.POST.get('sell_desc')
       
        cost_price=request.POST.get('cost_price')
        
        cost_acc=request.POST.get('cost_acc')
        
        cost_desc=request.POST.get('cost_desc')
        
        hsn=request.POST.get('item_hsn')
        
        units=Unit.objects.get(id=ut)
        
        sel=Sales.objects.get(id=sell_acc)
        
        cost=Purchase.objects.get(id=cost_acc)
       


        history="Created by " + str(request.user)
       
        user = User.objects.get(id = request.user.id)
        

        item=AddItem(type=type,unit=units,sales=sel,purchase=cost,Name=name,p_desc=cost_desc,s_desc=sell_desc,s_price=sell_price,p_price=cost_price,
                     user=user,creat=history,interstate=inter,intrastate=intra,hsn=hsn)

        item.save() 
        print("function")
        return JsonResponse({"message": "success"})
        
        
def purchase_item_dropdown_credit(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = AddItem.objects.all()
    for option in option_objects:
        options[option.id] = option.Name

    return JsonResponse(options)
    
    
def purchase_unit_credit(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        unit =request.POST.get('unit')
        
        u = User.objects.get(id = request.user.id)

        unit = Unit(unit= unit)
        unit.save()
     
        return JsonResponse({"message": "success"})
        
        
@login_required(login_url='login')        
def purchase_unit_dropdown_credit(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = Unit.objects.all()
    for option in option_objects:
        options[option.id] = option.unit
    
    return JsonResponse(options)
    
#___________________________Ashikh V U (start)__________________________________

@login_required(login_url='login')
def payment_received(request):
    todays_date = date.today().strftime('%d  %B  %Y')
    company = company_details.objects.get(id=request.user.id)
    customer_details = customer.objects.filter(user=request.user.id)
    return render(request,'payment_reciedved.html',{'todays_date':todays_date,
                                                    'customer':customer_details,
                                                    'company':company})
                                                    
@login_required(login_url='login')
def my_calendar(request):
    return TemplateResponse(request,'my_calendar.html')
    
    
@login_required(login_url='login')
def set_custom_date(request):
    start_date = request.POST.get('start_date_11')
    end_date = request.POST.get('end_date_11')
    shit = request.POST.get('shit')
    asd = request.POST.get('asd')
    print(f'{start_date}  {end_date}  {asd} {shit}')
    # start_date = start_date.strftime("%d %B %Y")
    # end_date = end_date.strftime("%d %B %Y")
    return HttpResponse(f"<h5 class='ts_sm_sm pt-1'>( {start_date} - {end_date} )</h5>")
    
    
@login_required(login_url='login')
def payment_reciedved_customize(request):
    company = company_details.objects.get(id=request.user.id)
    return render(request,'payment_reciedved_customize.html',{'company':company})
    
    
@login_required(login_url='login')
def payment_reciedved_customize_sub(request,new_id):
    return TemplateResponse(request,'filters/payment_reciedved_customize_sub.html',{'new_id':new_id})
    
@login_required(login_url='login')
def select_comparator(request,new_id):
    print(f'\n\n{new_id}\n\n')
    selected = request.GET.get('select_'+new_id)
    shit = 'select_'+new_id
    print(f'\n\n{shit}  {selected}\n\n')
    if selected == 'Payment Number' or selected == 'Customer Name' or selected == 'Reference Number' or selected == 'Invoice#' or selected == 'Unused Amount (BCY)':
        return TemplateResponse(request,'filters/select_comparator.html',{'selected_option':selected,'new_id':new_id})
    elif selected == 'Date' or selected == 'Applied Date' or selected == 'Refund Amount (BCY)' or selected == 'Amount (BCY)':
        return TemplateResponse(request,'filters/select_comparator_date.html',{'selected_option':selected,'new_id':new_id})
    else:
        return TemplateResponse(request,'filters/select_comparator_paymod.html',{'selected_option':selected,'new_id':new_id})
        
        
@login_required(login_url='login')
def add_note_or_date(request,selected_option,new_id):
    if selected_option == 'Payment Number' or selected_option == 'Customer Name' or selected_option == 'Reference Number' or selected_option == 'Invoice#' or selected_option == 'Unused Amount (BCY)':
        return TemplateResponse(request,'filters/add_note_or_date_input.html')
    elif selected_option == 'Date' or selected_option == 'Applied Date' or selected_option == 'Refund Amount (BCY)' or selected_option == 'Amount (BCY)':
        return TemplateResponse(request,'filters/add_note_or_date_date.html')
    else:
        return TemplateResponse(request,'filters/add_note_or_date_paymod.html')
        
        
@login_required(login_url='login')
def empty_filter(request):
    return TemplateResponse(request,'filters/empty_filter.html')
    
    
@login_required(login_url='login')
def payment_reciedved_customize_show(request):
    company = company_details.objects.get(id=request.user.id)
    return render(request,'payment_reciedved_customize_show.html',{'company':company})
    
@login_required(login_url='login')
def tax_summary_page(request):
    company = company_details.objects.get(id=request.user.id)
    customer_details = customer.objects.filter(user=request.user.id)
    return render(request,'tax_summary_page.html',{'company':company,
                                                    'customer_details':customer_details,
                                                        })
    
@login_required(login_url='login')
def generate_pdf(request,string_date,start_d,end_d):
    print(f'start date : {start_d}  end date : {end_d}')

    buffer = BytesIO()
    # p = canvas.Canvas(buffer,pagesize=A4)
    pdf_filename = "sample.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)


    # doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    customers = customer.objects.filter(user=request.user.id)
    d = string_date

    data = [["PAY-NUM", "FULL NAME", "DATE","REF-NUM","PAY-MOD","NOTE","INVOICE","FCY","U-FCY","BCY","U-BCY"]]

    heading_style = ParagraphStyle(
        'Heading1',
        parent=getSampleStyleSheet()['Heading1'],
        alignment=1,  # Centered alignment
        fontSize=16,
        fontName='Helvetica-Bold',
    )
    heading_style1 = ParagraphStyle(
        'Heading1',
        parent=getSampleStyleSheet()['Heading1'],
        alignment=1,  # Centered alignment
        fontSize=10,
        fontName='Helvetica',
    )
    heading_style3 = ParagraphStyle(
        'Heading1',
        parent=getSampleStyleSheet()['Heading1'],
        alignment=1,  # Centered alignment
        fontSize=15,
        fontName='Helvetica',
    )
    company = company_details.objects.get(id=request.user.id)
    heading3 = Paragraph(company.company_name, heading_style3)
    heading = Paragraph("Payment Received", heading_style)
    heading1 = Paragraph(f"{d}", heading_style1)
    elements.append(heading3)
    elements.append(heading)
    elements.append(heading1)

    for i in customers:
        data.append(["---------",i.customerName,"-----","---------","---------","------","--------","----","------","----","------"])

    table = Table(data)

    style = TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN',(0,1),(-1,-1 ),'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    table.setStyle(style)
    elements.append(table)
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
    # response.write(pdf)
    with open(pdf_filename, 'rb') as pdf_file:
        response.write(pdf_file.read())
    return response 
    
    
@login_required(login_url='login')
def generate_pdf1(request,string_date,start_d,end_d):

    buffer = BytesIO()
    # p = canvas.Canvas(buffer,pagesize=A4)
    pdf_filename = "sample.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

    # doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    customers = customer.objects.all()
    # d = datetime.now().date().strftime('%B %d %Y')
    d = string_date

    data = [["TAX NAME", "TAX PERCENTAGE %", "TAXABLE AMOUNT","TAXAMOUNT"]]

    heading_style = ParagraphStyle(
        'Heading1',
        parent=getSampleStyleSheet()['Heading1'],
        alignment=1,  # Centered alignment
        fontSize=16,
        fontName='Helvetica-Bold',
    )
    heading_style1 = ParagraphStyle(
        'Heading1',
        parent=getSampleStyleSheet()['Heading1'],
        alignment=1,  # Centered alignment
        fontSize=10,
        fontName='Helvetica',
    )
    heading_style3 = ParagraphStyle(
        'Heading1',
        parent=getSampleStyleSheet()['Heading1'],
        alignment=1,  # Centered alignment
        fontSize=15,
        fontName='Helvetica',
    )
    heading_style4 = ParagraphStyle(
        'Heading1',
        parent=getSampleStyleSheet()['Heading1'],
        alignment=1,  # Centered alignment
        fontSize=8,
        fontName='Helvetica',
    )
    company = company_details.objects.get(id=request.user.id)
    heading3 = Paragraph(company.company_name, heading_style3)
    heading = Paragraph("Tax Summary", heading_style)
    heading4 = Paragraph("Basic : Accural", heading_style4)
    heading1 = Paragraph(f"( {d} )", heading_style1)
    elements.append(heading3)
    elements.append(heading)
    elements.append(heading4)
    elements.append(heading1)

    # for i in customers:
    #     data.append(["---------",i.user.first_name +" "+ i.user.last_name,"-----","---------","---------","------","--------","----","------","----","------"])

    table = Table(data)

    style = TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    table.setStyle(style)
    elements.append(table)
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
    # response.write(pdf)
    with open(pdf_filename, 'rb') as pdf_file:
        response.write(pdf_file.read())
    return response 
    
@login_required(login_url='login')
def tax_summary_customize_general(request):
    company = company_details.objects.get(id=request.user.id)
    return render(request,'tax_summary_customize_general.html',{'company':company})

#___________________________Ashikh V U (end)__________________________________


def hsndata(request):
    name = request.GET.get('name')
    item = AddItem.objects.get(Name=name)
    data = {'hsn_data': item.hsn}
    return JsonResponse(data)
    
    
# nasneen o m

def projentr_custmrA(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            cr_data=customer()
            print('hii')
            print(cr_data)
            type=request.POST.get('type')
            fName=request.POST.get('fName')
            lName=request.POST.get('lName')
            txtFullName=request.POST.get('txtFullName')
            cpname=request.POST.get('cpname')           
            email=request.POST.get('email')
            wphone=request.POST.get('wphone')
            mobile=request.POST.get('mobile')
            skname=request.POST.get('skname')
            desg=request.POST.get('desg')      
            dept=request.POST.get('dept')
            wbsite=request.POST.get('wbsite')

            gstt=request.POST.get('v_gsttype')
            
            x=request.POST.get('v_gsttype')
            if x=="Unregistered Business-not Registered under GST":
                pan=request.POST.get('pan_number')
                gstin="null"
            else:
                gstin=request.POST.get('v_gstin')
                pan=request.POST.get('pan_number')
           
            posply=request.POST.get('posply')
            tax1=request.POST.get('tax1')
            crncy=request.POST.get('crncy')

            # select=request.POST.get('pterms')
            
            pterms=request.POST.get('pterms')

            plst=request.POST.get('plst')
            plang=request.POST.get('plang')
            fbk=request.POST.get('fbk')
            twtr=request.POST.get('twtr')
        
            atn=request.POST.get('atn')
            ctry=request.POST.get('ctry')
            
            addrs=request.POST.get('addrs')
            addrs1=request.POST.get('addrs1')
            bct=request.POST.get('bct')
            bst=request.POST.get('bst')
            bzip=request.POST.get('bzip')
            bpon=request.POST.get('bpon')
            bfx=request.POST.get('bfx')
            remark=request.POST.get('remark')
            obal= float(request.POST.get('obal', 0.0))
            crdr=request.POST.get('bal')
            status='Active'
            u = User.objects.get(id = request.user.id)
            if crdr == 'credit':
                obal = -obal
            else:
                obal = obal
          
            ctmr=customer(customerName=txtFullName,
                          Fname=fName,Lname=lName,
                          customerType=type,
                        companyName=cpname,
                        customerEmail=email,
                        customerWorkPhone=wphone,
                         customerMobile=mobile,skype=skname,
                         designation=desg,department=dept,
                           website=wbsite
                           ,GSTTreatment=gstt,
                           GSTIN=gstin,pan_no=pan,
                           placeofsupply=posply, Taxpreference=tax1,
                             currency=crncy,OpeningBalance=obal,
                             PaymentTerms=pterms,
                                PriceList=plst,PortalLanguage=plang,
                                Facebook=fbk,
                                Twitter=twtr,
                                 Attention=atn,country=ctry,Address1=addrs,Address2=addrs1,
                                  city=bct,state=bst,zipcode=bzip,phone1=bpon,
                                   fax=bfx,
                                     remark=remark,cr_dr=crdr,status=status,user=u )
            ctmr.save() 
 
            #  ...........................adding multiple rows of table to model  ........................................................       
            CPsalutation =request.POST.getlist('sal[]')
            Firstname=request.POST.getlist('ftname[]')
            Lastname =request.POST.getlist('ltname[]')
            CPemail =request.POST.getlist('mail[]')
            CPphone=request.POST.getlist('bworkpn[]')
            CPmobile=request.POST.getlist('bmobile[]')
            CPskype=request.POST.getlist('bskype[]')
            CPdesignation=request.POST.getlist('bdesg[]')
            CPdepartment=request.POST.getlist('bdept[]') 
            
            cdata=customer.objects.get(id=ctmr.id)
            Customr=cdata 
            
            if len(CPsalutation)==len(Firstname)==len(Lastname)==len(CPemail)==len(CPphone)==len(CPmobile)==len(CPskype)==len(CPdesignation)==len(CPdepartment):
                mapped2=zip(CPsalutation,Firstname,Lastname,CPemail,CPphone,CPmobile,CPskype,CPdesignation,CPdepartment)
                mapped2=list(mapped2)
                print(mapped2)
                for ele in mapped2:
                    created = customer_contact_person_table.objects.get_or_create(CPsalutation=ele[0],Firstname=ele[1],Lastname=ele[2],CPemail=ele[3],
                            CPphone=ele[4],CPmobile=ele[5],CPskype=ele[6],CPdesignation=ele[7],CPdepartment=ele[8],user=u,Customr=Customr)
            options = {}
            option_objects = customer.objects.filter(user=request.user)
            for option in option_objects:
                options[option.id] = [option.id , option.Fname , option.Lname]
            return JsonResponse(options) 
        else:
            return JsonResponse({'error': 'Invalid request'}, status=400)
            

def holiday_list(request):
    company = company_details.objects.get(user=request.user)
    all_events = Events.objects.all()
    event_counts = {}
    formatted_event_counts = {}

    for event in all_events:
        month_year = event.start.strftime('%Y-%m')  # Format: 'YYYY-MM'
    
    # If the month_year is not in the dictionary, add it with a count of 1
        if month_year not in event_counts:
            event_counts[month_year] = 1
        else:
        # If the month_year is already in the dictionary, increment the count
            event_counts[month_year] += 1
    for key, value in event_counts.items():
        year, month = key.split('-')
        month_name = calendar.month_name[int(month)]
        formatted_month_year = f"{month_name}-{year}"
        formatted_event_counts[formatted_month_year] = value   
    context = {
        "events": all_events,
        "event_counts_json": formatted_event_counts,
        "company":company
    }
    return render(request, 'holiday_list.html',context)
    
    
def project_active(request,id):
    p=project1.objects.get(id=id)
    if p.mode == 'Active':
        p.mode = 'Inactive'
    else:
        p.mode = 'Active'
    p.save()
    return redirect('overview',id=id)
    
    
@login_required(login_url='login')
def add_repeat(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        repeats = request.POST.get('repeats')
        
        
        u = User.objects.get(id = request.user.id)

        ad_repeat = repeat(repeat=repeats,  user = u)
        ad_repeat.save()

        return HttpResponse({"message": "success"})
    
        
@login_required(login_url='login')
def repeat_dropdown(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = repeat.objects.filter(user = user)
    for option in option_objects:
        options[option.id] = [option.repeat]

    return JsonResponse(options)

@login_required(login_url='login')
def get_rec_item(request):
    cmp1 = request.user
    name=request.GET.get('name')
    data=AddItem.objects.get(Name=name,user_id=cmp1) 
    return JsonResponse({"item":data})

@login_required(login_url='regcomp')
def add_rec_comments(request,id):
    if request.method == 'POST':
        
        recur_bills = recurring_bills.objects.get(id = id)
        
        comment = request.POST['comments']
        user = User.objects.get(id=request.user.id)
        
        comments= rec_comments(recur_bills=recur_bills,user=user,comment=comment)
        comments.save()
        return redirect('view_recurring_bills',id)

@login_required(login_url='regcomp')
def delete_rec_comments(request,id,commentid):
    try:
        print(str(commentid))
        comment = rec_comments.objects.get(commentid=commentid)
        print(comment)
        comment.delete()
        return redirect('view_recurring_bills',id)
    except:
        return redirect('view_recurring_bills',id)



    
def delete_purchase_bill(request,id):
    Bills=PurchaseBills.objects.get(id=id)
    Bills.delete()
    return redirect('view_bills')

def covert_to_recurring_bills(request, id): 
    
    r_bill = recurring_bills.objects.get(user=request.user, id=id)
    
    if r_bill.status == 'Draft':
        r_bill.status = 'Save'
    
    r_bill.save()  
    
    return redirect('view_recurring_bills', id)


@login_required(login_url='login')
def recur_bill_save(request,id):
    company = company_details.objects.get(user = request.user)
    bills = recurring_bills.objects.filter(user = request.user, status = 'Save')
    rbill=recurring_bills.objects.get(user = request.user, id= id)
    billitem = recurring_bills_items.objects.filter(user = request.user,recur_bills=id) 
    comment = rec_comments.objects.filter(recur_bills_id=rbill) 
    cust = customer.objects.get(id = rbill.customer_name.split(" ")[0])
    vend = vendor_table.objects.get(id = rbill.vendor_name.split(" ")[0])
    gst_or_igst = "GST" if company.state == (" ".join(rbill.source_supply.split(" ")[1:])) else "IGST"
    tax_total = [] 
    for b in billitem:
        if b.tax not in tax_total: 
            tax_total.append(b.tax)
    
    cust_name = cust.customerName
    vend_name = vend.salutation+ " " +vend.first_name + " " +vend.last_name
    context = {
                'company' : company,
                'recur_bills' : bills,
                'recur_bill' : rbill,
                'bill_item' : billitem,
                'tax' : tax_total,
                "gst_or_igst" : gst_or_igst,
                'customer' : cust,
                'vendor' : vend,
                'customer_name' : cust_name,
                'vendor_name' : vend_name,
                'comments':comment
            }

    return render(request, 'view_recurring_bills.html',context)

@login_required(login_url='login')
def recur_bill_draft(request,id):
    company = company_details.objects.get(user = request.user)
    bills = recurring_bills.objects.filter(user = request.user, status = 'Draft')
    rbill=recurring_bills.objects.get(user = request.user, id= id)
    billitem = recurring_bills_items.objects.filter(user = request.user,recur_bills=id) 
    comment = rec_comments.objects.filter(recur_bills_id=rbill) 
    cust = customer.objects.get(id = rbill.customer_name.split(" ")[0])
    vend = vendor_table.objects.get(id = rbill.vendor_name.split(" ")[0])
    gst_or_igst = "GST" if company.state == (" ".join(rbill.source_supply.split(" ")[1:])) else "IGST"
    tax_total = [] 
    for b in billitem:
        if b.tax not in tax_total: 
            tax_total.append(b.tax)
    
    cust_name = cust.customerName
    vend_name = vend.salutation+ " " +vend.first_name + " " +vend.last_name
    context = {
                'company' : company,
                'recur_bills' : bills,
                'recur_bill' : rbill,
                'bill_item' : billitem,
                'tax' : tax_total,
                "gst_or_igst" : gst_or_igst,
                'customer' : cust,
                'vendor' : vend,
                'customer_name' : cust_name,
                'vendor_name' : vend_name,
                'comments':comment
            }

    return render(request, 'view_recurring_bills.html',context)

@login_required(login_url='login')
def billno_recurring_sort(request,id):
    company = company_details.objects.get(user = request.user)
    bills = recurring_bills.objects.filter(user = request.user).order_by('bill_no')
    rbill=recurring_bills.objects.get(user = request.user, id= id)
    billitem = recurring_bills_items.objects.filter(user = request.user,recur_bills=id) 
    comment = rec_comments.objects.filter(recur_bills_id=rbill) 
    cust = customer.objects.get(id = rbill.customer_name.split(" ")[0])
    vend = vendor_table.objects.get(id = rbill.vendor_name.split(" ")[0])
    gst_or_igst = "GST" if company.state == (" ".join(rbill.source_supply.split(" ")[1:])) else "IGST"
    tax_total = [] 
    for b in billitem:
        if b.tax not in tax_total: 
            tax_total.append(b.tax)
    
    cust_name = cust.customerName
    vend_name = vend.salutation+ " " +vend.first_name + " " +vend.last_name
    context = {
                'company' : company,
                'recur_bills' : bills,
                'recur_bill' : rbill,
                'bill_item' : billitem,
                'tax' : tax_total,
                "gst_or_igst" : gst_or_igst,
                'customer' : cust,
                'vendor' : vend,
                'customer_name' : cust_name,
                'vendor_name' : vend_name,
                'comments':comment
            }

    return render(request, 'view_recurring_bills.html',context)

@login_required(login_url='login')
def vendor_recurring_sort(request,id):
    company = company_details.objects.get(user = request.user)
    bills = recurring_bills.objects.filter(user = request.user).order_by('vendor_name')
    rbill=recurring_bills.objects.get(user = request.user, id= id)
    billitem = recurring_bills_items.objects.filter(user = request.user,recur_bills=id) 
    comment = rec_comments.objects.filter(recur_bills_id=rbill) 
    cust = customer.objects.get(id = rbill.customer_name.split(" ")[0])
    vend = vendor_table.objects.get(id = rbill.vendor_name.split(" ")[0])
    gst_or_igst = "GST" if company.state == (" ".join(rbill.source_supply.split(" ")[1:])) else "IGST"
    tax_total = [] 
    for b in billitem:
        if b.tax not in tax_total: 
            tax_total.append(b.tax)
    
    cust_name = cust.customerName
    vend_name = vend.salutation+ " " +vend.first_name + " " +vend.last_name
    context = {
                'company' : company,
                'recur_bills' : bills,
                'recur_bill' : rbill,
                'bill_item' : billitem,
                'tax' : tax_total,
                "gst_or_igst" : gst_or_igst,
                'customer' : cust,
                'vendor' : vend,
                'customer_name' : cust_name,
                'vendor_name' : vend_name,
                'comments':comment
            }

    return render(request, 'view_recurring_bills.html',context)

@login_required(login_url='login')
def profilename_recurring_sort(request,id):
    company = company_details.objects.get(user = request.user)
    bills = recurring_bills.objects.filter(user = request.user).order_by('profile_name')
    rbill=recurring_bills.objects.get(user = request.user, id= id)
    billitem = recurring_bills_items.objects.filter(user = request.user,recur_bills=id) 
    comment = rec_comments.objects.filter(recur_bills_id=rbill) 
    cust = customer.objects.get(id = rbill.customer_name.split(" ")[0])
    vend = vendor_table.objects.get(id = rbill.vendor_name.split(" ")[0])
    gst_or_igst = "GST" if company.state == (" ".join(rbill.source_supply.split(" ")[1:])) else "IGST"
    tax_total = [] 
    for b in billitem:
        if b.tax not in tax_total: 
            tax_total.append(b.tax)
    
    cust_name = cust.customerName
    vend_name = vend.salutation+ " " +vend.first_name + " " +vend.last_name
    context = {
                'company' : company,
                'recur_bills' : bills,
                'recur_bill' : rbill,
                'bill_item' : billitem,
                'tax' : tax_total,
                "gst_or_igst" : gst_or_igst,
                'customer' : cust,
                'vendor' : vend,
                'customer_name' : cust_name,
                'vendor_name' : vend_name,
                'comments':comment
            }

    return render(request, 'view_recurring_bills.html',context)

@login_required(login_url='regcomp')
def add_purchase_comments(request,id):
    if request.method == 'POST':
        
        purchase_bill = PurchaseBills.objects.get(id=id)
        
        comment = request.POST['comments']
        user = User.objects.get(id=request.user.id)
        
        comments= purchase_comments(purchase_bill=purchase_bill,user=user,comment=comment)
        comments.save()
        return redirect('bill_view',id)

@login_required(login_url='regcomp')
def delete_purchase_comments(request,id,commentid):
    try:
        print(str(commentid))
        comment = purchase_comments.objects.get(commentid=commentid)
        print(comment)
        comment.delete()
        return redirect('bill_view',id)
    except:
        return redirect('bill_view',id)
    
def covert_to_purchase_bills(request, id): 
    
    purchase_bill = PurchaseBills.objects.get(user=request.user, id=id)
    
    if purchase_bill.status == 'Draft':
        purchase_bill.status = 'Save'
    
    purchase_bill.save()  
    
    return redirect('bill_view', id)


def billno_purchase_sort(request, b_id):
    user = request.user
    company = company_details.objects.get(user=user)
    bills = PurchaseBills.objects.filter(user=user).order_by('bill_no')
    bill = PurchaseBills.objects.get(id=b_id)
    items = PurchaseBillItems.objects.filter(purchase_bill=bill)
    comment = purchase_comments.objects.filter(purchase_bill=b_id)
    context = {
        'company': company,
        'bills': bills,
        'bill': bill,
        'items': items,
        'comments':comment,
    }
    return render(request, 'bill_slip.html', context)

def vendor_purchase_sort(request, b_id):
    user = request.user
    company = company_details.objects.get(user=user)
    bills = PurchaseBills.objects.filter(user=user).order_by('vendor_name')
    bill = PurchaseBills.objects.get(id=b_id)
    items = PurchaseBillItems.objects.filter(purchase_bill=bill)
    comment = purchase_comments.objects.filter(purchase_bill=b_id)
    context = {
        'company': company,
        'bills': bills,
        'bill': bill,
        'items': items,
        'comments':comment,
    }
    return render(request, 'bill_slip.html', context)

def customer_purchase_sort(request, b_id):
    user = request.user
    company = company_details.objects.get(user=user)
    bills = PurchaseBills.objects.filter(user=user).order_by('customer_name')
    bill = PurchaseBills.objects.get(id=b_id)
    items = PurchaseBillItems.objects.filter(purchase_bill=bill)
    comment = purchase_comments.objects.filter(purchase_bill=b_id)
    context = {
        'company': company,
        'bills': bills,
        'bill': bill,
        'items': items,
        'comments':comment,
    }
    return render(request, 'bill_slip.html', context)

def purchase_bill_save(request, b_id):
    user = request.user
    company = company_details.objects.get(user=user)
    bills = PurchaseBills.objects.filter(user = request.user, status = 'Save')
    bill = PurchaseBills.objects.get(id=b_id)
    items = PurchaseBillItems.objects.filter(purchase_bill=bill)
    comment = purchase_comments.objects.filter(purchase_bill=b_id)
    context = {
        'company': company,
        'bills': bills,
        'bill': bill,
        'items': items,
        'comments':comment,
    }
    return render(request, 'bill_slip.html', context)

def purchase_bill_draft(request, b_id):
    user = request.user
    company = company_details.objects.get(user=user)
    bills = PurchaseBills.objects.filter(user = request.user, status = 'Draft')
    bill = PurchaseBills.objects.get(id=b_id)
    items = PurchaseBillItems.objects.filter(purchase_bill=bill)
    comment = purchase_comments.objects.filter(purchase_bill=b_id)
    context = {
        'company': company,
        'bills': bills,
        'bill': bill,
        'items': items,
        'comments':comment,
    }
    return render(request, 'bill_slip.html', context)


@login_required(login_url='login')
def draft_recurring_bills(request):

    company = company_details.objects.get(user = request.user)
    # print(request.POST.get('customer').split(" ")[0])
    cust = customer.objects.get(id=request.POST.get('customer').split(" ")[0],user = request.user)

    if request.method == 'POST':
        # vname = request.POST.get('vendor').rsplit(' ', 1)
        # cname = request.POST.get('customer').split(" ")[1:]
        vname  = request.POST.get('vendor')
        cname = request.POST.get('customer')
        #cus=customer.objects.get(customerName=cname)   
        custo=cust.id 
        # cname = " ".join(cname)
        v_gst_no=request.POST.get('gstin_inp')   # haripriya add
        src_supply = request.POST.get('srcofsupply')
        prof = request.POST['prof_name']
        repeat = request.POST['repeats']
        start = request.POST.get('start_date')
        end = None if request.POST.get('end_date') == "" else  request.POST.get('end_date')
        pay_term =request.POST['terms']
        payment_method =request.POST['paymentmethod']
        amt_paid =request.POST['amtPaid']

        hsn = request.POST.get('HSN0')
        bill_no =  request.POST.get('bills')
        sub_total =request.POST['subtotal']
        adjustment =request.POST['add_round_off']

        sgst=None if request.POST.get('sgst') == "" else  request.POST.get('sgst')
        cgst=None if request.POST.get('cgst') == "" else  request.POST.get('cgst')
        igst= None if request.POST.get('igst') == "" else  request.POST.get('igst')

        status = 'Draft'
        taxamount =request.POST['total_taxamount']

        shipping_charge=0 if request.POST['addcharge'] == "" else request.POST['addcharge']
        grand_total=request.POST['grand_total']
        note=request.POST.get('note')
        balance = float(grand_total) - float(amt_paid)

        u = User.objects.get(id = request.user.id)

        bills = recurring_bills(vendor_name=vname,profile_name=prof,customer_name = cname,vendor_gst_number=v_gst_no,
                    source_supply=src_supply,repeat_every = repeat,start_date = start,end_date = end,
                    payment_terms =pay_term,sub_total=sub_total,sgst=sgst,cgst=cgst,igst=igst,
                    tax_amount=taxamount, shipping_charge = shipping_charge,
                    grand_total=grand_total,note=note,company=company,user = u,cname_recur_id=custo, bill_no = bill_no,status = status, payment_method=payment_method, amt_paid=amt_paid,  adjustment = adjustment,balance = balance )
        bills.save()

        r_bill = recurring_bills.objects.get(id=bills.id)

        if len(request.FILES) != 0:
            r_bill.document=request.FILES['file'] 
            r_bill.save()

        items = request.POST.getlist("item[]")
       
        
        quantity = request.POST.getlist("qty[]")
        rate = request.POST.getlist("rate[]")
        
        if (src_supply.split("-")[1]) == company.state:
            tax = request.POST.getlist("tax1[]")
        else:
            tax = request.POST.getlist("tax2[]")

        discount = request.POST.getlist("discount[]") 
        amount = request.POST.getlist("amount[]")
        hsn = request.POST.getlist('HSN[]')

        if len(items)==len(amount) == len(quantity) == len(rate)==len(tax) == len(discount) == len(hsn) and items and  quantity and rate and tax and discount and amount and hsn:
                
                mapped=zip(items,quantity,rate,tax,discount,amount,hsn)
                mapped=list(mapped)

                for ele in mapped:

                    it = AddItem.objects.get(user = request.user, id = ele[0]).Name
                        
                    created = recurring_bills_items.objects.create(item = it,quantity=ele[1],rate=ele[2],
                    tax=ele[3],discount = ele[4],amount=ele[5],hsn=ele[6], user = u,company = company, recur_bills = r_bill)
                
        return redirect('recurring_bill')
    
    return redirect('recurring_bill')



def change_draft_recurring_bills(request,id):
            
    company = company_details.objects.get(user = request.user)
    # cust = customer.objects.get(customerName=request.POST.get('customer').strip(" "),user = request.user)
    r_bill=recurring_bills.objects.get(user = request.user,id=id)
    cust = customer.objects.get(id=request.POST.get('customer').split(" ")[0],user = request.user)

    if request.method == 'POST':
        
        r_bill.vendor_name = request.POST.get('vendor')
        r_bill.customer_name= request.POST.get('customer')
        r_bill.profile_name = request.POST['prof_name']
        r_bill.source_supply=request.POST['srcofsupply']
        r_bill.repeat_every=request.POST['repeats']
        r_bill.start_date=request.POST['start_date']
        r_bill.end_date=None if request.POST.get('end_date') == "" else  request.POST.get('end_date')
        r_bill.payment_terms=request.POST['terms']
        r_bill.note=request.POST['note']
        r_bill.sub_total=None if request.POST.get('subtotal') == "" else  request.POST.get('subtotal')
        r_bill.igst=None if request.POST.get('igst') == "" else  request.POST.get('igst')
        r_bill.cgst=None if request.POST.get('cgst') == "" else  request.POST.get('cgst')
        r_bill.sgst=None if request.POST.get('sgst') == "" else  request.POST.get('sgst')
        r_bill.shipping_charge=request.POST['addcharge']
        r_bill.grand_total=request.POST.get('grand_total')
        r_bill.payment_method =request.POST['paymentmethod']
        r_bill.amt_paid =request.POST['amtPaid']
       
        r_bill.bill_no =  request.POST.get('bills')
        r_bill.adjustment =request.POST['add_round_off']
        r_bill.status = 'Draft'
        r_bill.grand_total = request.POST.get('grand_total')
        r_bill.amt_paid = request.POST['amtPaid']
        grand_total = request.POST.get('grand_total')
        amt_paid = request.POST['amtPaid']
        r_bill.balance = float(grand_total) - float(amt_paid)
        r_bill.cname_recur_id = cust.id

        if len(request.FILES) != 0:
             
            r_bill.document = request.FILES['file']
            

        r_bill.save()          

        items = request.POST.getlist("item[]")
        
        quantity = request.POST.getlist("quantity[]")
        rate = request.POST.getlist("rate[]")

        if (" ".join(request.POST['srcofsupply'].split(" ")[1:])) == company.state:
            tax = request.POST.getlist("tax1[]")
        else:
            tax = request.POST.getlist("tax2[]")

        discount = request.POST.getlist("discount[]") 
        amount = request.POST.getlist("amount[]")
        hsn = request.POST.getlist('HSN[]')

        if len(items)==len(amount) == len(quantity) == len(rate)==len(tax) == len(discount) == len(hsn) and items and quantity and rate and tax and discount and amount and hsn:
                
            mapped=zip(items,quantity,rate,tax,discount,amount,hsn)
            mapped=list(mapped)

            
            count = recurring_bills_items.objects.filter(recur_bills=r_bill.id).count()
            
            for ele in mapped:

                if int(len(items))>int(count):

                    pbillss=recurring_bills.objects.get(id=id)
                    company = company_details.objects.get(user = request.user)
                    it = AddItem.objects.get(user = request.user, id = ele[0]).Name
                    it = AddItem.objects.get(user = request.user, id = ele[0]).Name
                    try:
                        int(ele[1])
                        ac = Chart_of_Account.objects.get(user = request.user,id = ele[1]).account_name
                        
                    except ValueError:
                        
                        ac = ele[1]
                    
                    created = recurring_bills_items.objects.get_or_create(item = it,quantity=ele[2],rate=ele[3],
                    tax=ele[4],discount = ele[5],amount=ele[6],hsn=ele[7],recur_bills=r_bill.id,company=company,user = request.user)

                else:
                    
                    dbs=recurring_bills_items.objects.get(recur_bills =r_bill.id,item = ele[0])
                    created = recurring_bills_items.objects.filter(recur_bills =dbs.recur_bills,items = ele[0]).update(item = ele[0],
                        quantity=ele[1],rate=ele[2], tax=ele[3],discount=ele[4],amount= ele[5],hsn=ele[6])
 

        return redirect('view_recurring_bills',id)
    return redirect('recurring_bill')

def isNum(data):
    try:
        int(data)
        return True
    except ValueError:
        return False


def update_bills_save(request,pk):
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)

    if request.method == 'POST':
        bill = PurchaseBills.objects.get(id=pk)
        bill.user = user
        bill.vendor_name = request.POST['vendor_name']
        bill.vendor_email = request.POST['vendor_email']
        bill.vendor_gst = request.POST['gstin_inp']
        bill.source_of_supply = request.POST['sos']
        bill.customer_name = request.POST['customer_name']
        bill.customer_email = request.POST['customer_email']
        bill.place_of_supply = request.POST['pos']
        bill.bill_no = request.POST['bill_number']
        bill.order_number = request.POST['order_number']
        bill.bill_date = request.POST['bill_date']
        bill.due_date = None if request.POST.get('due_date') == "" else  request.POST.get('due_date')
        bill.payment_terms = request.POST['p_terms']
        bill.repeat_every = request.POST['repeats']
        bill.payment_method = request.POST['paymentmethod']
        bill.adjustment = request.POST['add_round_off']
        bill.amt_paid = request.POST['amtPaid']
        

        bill.sub_total = request.POST['subtotal']
        bill.igst = request.POST['igst']
        bill.sgst = request.POST['sgst']
        bill.cgst = request.POST['cgst']
        bill.tax_amount = request.POST['total_taxamount']
        bill.shipping_charge = request.POST['shipping_charge']
        
        bill.total = request.POST['total']
        bill.status = 'Save'
        total = request.POST['total']
        amt_paid = request.POST['amtPaid']
        bill.balance = float(total) - float(amt_paid)
       

        old=bill.attachment
        new=request.FILES.get('file')
        if old != None and new == None:
            bill.attachment = old
        else:
            bill.attachment = new

        bill.save()

        item = request.POST.getlist('item[]')
       
        quantity = request.POST.getlist('quantity[]')
        rate = request.POST.getlist('rate[]')
        tax = request.POST.getlist('tax[]')
        amount = request.POST.getlist('amount[]')
        hsn = request.POST.getlist('HSN[]')
        discount = request.POST.getlist('discount[]')
       
        objects_to_delete = PurchaseBillItems.objects.filter(purchase_bill_id=bill.id)
        objects_to_delete.delete()

       
        if len(item) == len(quantity) == len(rate) == len(tax) == len(amount) == len(hsn) == len(discount) and item and quantity and rate and tax and amount and hsn and discount:
            mapped = zip(item, quantity, rate, tax, amount ,hsn, discount)
            mapped = list(mapped)
            for element in mapped:
                created = PurchaseBillItems.objects.create(
                    purchase_bill=bill, item_name=element[0], quantity=element[1], rate=element[2], tax_percentage=element[3], amount=element[4], hsn=element[5], discount=element[6])
    return redirect('bill_view',b_id = bill.id)



def terms_dropdowns(request):
    terms = payment_terms.objects.all()
    term_data = []
    day_data = []
    for i in terms:
        term_data.append(i.Terms)
        day_data.append(i.Days)
    data = {'term_data': term_data,"day_data":day_data}
    return JsonResponse(data)


def new_estimate_item(request):
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':
        
        type=request.POST.get('type')
        name=request.POST.get('name')
        hsn=request.POST.get('hsn')
        ut=request.POST.get('unit')
        inter=request.POST.get('inter')
        intra=request.POST.get('intra')
        sell_price=request.POST.get('sell_price')
        sell_acc=request.POST.get('sell_acc')
        sell_desc=request.POST.get('sell_desc')
        cost_price=request.POST.get('cost_price')
        cost_acc=request.POST.get('cost_acc')      
        cost_desc=request.POST.get('cost_desc')
        
        units=Unit.objects.get(id=ut)
        sel=Sales.objects.get(id=sell_acc)
        cost=Purchase.objects.get(id=cost_acc)

        history="Created by " + str(request.user)

        u  = User.objects.get(id = request.user.id)

        item=AddItem(type=type,Name=name,hsn=hsn,p_desc=cost_desc,s_desc=sell_desc,s_price=sell_price,p_price=cost_price,
                     user=u ,creat=history,interstate=inter,intrastate=intra,unit = units,sales = sel, purchase = cost)

        item.save()

        return HttpResponse({"message": "success"})
    
    return HttpResponse("Invalid request method.")





def new_estimate_customer(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            tax = request.POST.get('tax_preference')
            cust_type = request.POST.get('customer_type')
            # title=request.POST.get('title')
            first_name=request.POST.get('firstname')
            last_name=request.POST.get('lastname')
            comp_name = request.POST.get('company_name')
            name = request.POST.get('display_name')
            email=request.POST.get('email')
            website=request.POST.get('website')
            w_mobile=request.POST.get('work_mobile')
            p_mobile=request.POST.get('pers_mobile')
            skype = request.POST.get('skype')
            fb = request.POST.get('facebook')
            twitter = request.POST.get('twitter')
            desg = request.POST.get('desg')
            dpt = request.POST.get('dpt')
            gsttype=request.POST.get('gsttype')
            gstin=request.POST.get('gstin')
            panno=request.POST.get('panno')
            supply=request.POST.get('placesupply')
            currency=request.POST.get('currency')
            balance=request.POST.get('openingbalance')
            payment=request.POST.get('paymentterms')


            street1=request.POST.get('street')
            street2=request.POST.get('street')
            city=request.POST.get('city')
            state=request.POST.get('state')
            pincode=request.POST.get('pincode')
            country=request.POST.get('country')
            fax=request.POST.get('fax')
            phone=request.POST.get('phone')
            sAddress1=request.POST.get('shipstreet')
            sAddress2=request.POST.get('shipstreet')
            scity=request.POST.get('shipcity')
            sstate=request.POST.get('shipstate')
            scountry=request.POST.get('shipcountry')
            szipcode=request.POST.get('shippincode')
            sphone1=request.POST.get('shipphone')
            sfax=request.POST.get('shipfax')

            # shipstreet1=request.POST.get('shipstreet1')
            # shipstreet2=request.POST.get('shipstreet2')
            # shipcity=request.POST.get('shipcity')
            # shipstate=request.POST.get('shipstate')
            # shippincode=request.POST.get('shippincode')
            # shipcountry=request.POST.get('shipcountry')
            # shipfax=request.POST.get('shipfax')
            # shipphone=request.POST.get('shipphone')

            u = User.objects.get(id = request.user.id)

            cust = customer(Taxpreference = tax, customerType = cust_type, Fname=first_name, Lname=last_name, companyName= comp_name, customerName = name, customerEmail=email,  GSTTreatment=gsttype, GSTIN=gstin, 
                            customerWorkPhone = w_mobile, customerMobile = p_mobile, skype = skype,Facebook = fb, 
                            Twitter = twitter, placeofsupply=supply, currency=currency, website=website, 
                            designation = desg, department = dpt,OpeningBalance=balance,Address1=street1,Address2=street2, city=city, 
                            state=state, PaymentTerms=payment,zipcode=pincode,country=country,fax = fax,  phone1 = phone,
                            sAddress1=sAddress1,sAddress2=sAddress2,scity=scity,sstate=sstate,scountry=scountry,szipcode=szipcode,
                            sphone1=sphone1,sfax=sfax,user=u,pan_no=panno)
            cust.save()
            print('success')

            return HttpResponse({"message": "success"})


        

def est_sort_by_estno(request):
    user=request.user.id
    est=Estimates.objects.filter(user=user).values()
    for r in est:
        vn = r['estimate_no'].split("-")
        r['est_no'] = " ".join(vn)
    sorted_est = sorted(est, key=lambda r: r['est_no'])  
    context = {
                'estimates' : sorted_est
            }  
    return render(request,'all_estimates.html',context)


def est_sort_by_name(request):
    user=request.user.id
    est=Estimates.objects.filter(user=user).values()
    for r in est:
        vn = r['customer_name'].split()[1:]
        r['cust_name'] = " ".join(vn)
    sorted_est = sorted(est, key=lambda r: r['cust_name'])  
    context = {
                'estimates' : sorted_est
            }  
    return render(request,'all_estimates.html',context)


def est_sort_by_name_estimate_view(request,pk):
    user=request.user.id
    company = company_details.objects.get(user=user)
    est=Estimates.objects.filter(user=user).values()
    estimate = Estimates.objects.get(id=pk)
    items = EstimateItems.objects.filter(estimate=estimate)
    for r in est:
        vn = r['customer_name'].split()[1:]
        r['cust_name'] = " ".join(vn)
    sorted_est = sorted(est, key=lambda r: r['cust_name'])  
    context = {
                'all_estimates' : sorted_est,
                'company': company,
                'estimate': estimate,
                'items': items,
            }  
    return render(request,'estimate_slip.html', context)

def est_sort_by_estno_estimate_view(request,pk):
    user=request.user.id
    company = company_details.objects.get(user=user)
    est=Estimates.objects.filter(user=user).values()
    estimate = Estimates.objects.get(id=pk)
    items = EstimateItems.objects.filter(estimate=estimate)
     
    for r in est:
        vn = r['estimate_no'].split("-")
        r['est_no'] = " ".join(vn)
    sorted_est = sorted(est, key=lambda r: r['est_no']) 
    context = {
                'all_estimates' : sorted_est,
                'company': company,
                'estimate': estimate,
                'items': items,
            }  
    return render(request, 'estimate_slip.html', context)


def convert_to_salesorder(request,pk):
    user = request.user.id
    estimate=Estimates.objects.get(id=pk)
    sale_status=estimate.convert_sales
    if sale_status=='not_converted':
        new_status="converted"
    else:
        new_status="converted"
    items = EstimateItems.objects.filter(estimate=estimate.id)
    cust=estimate.customer.id
    cust1=customer.objects.get(id=cust)
    if SalesOrder.objects.all().exists():
        sales_count = SalesOrder.objects.last().id
        count=sales_count+1
        sal_string="SO-"
        next_no=sal_string+str(count)
    else:
        count=1 
        sal_string="SO-"
        next_no=sal_string+str(count)
    sal = SalesOrder(customer_id=cust1.id,sales_no=next_no,reference=estimate.reference, sales_date=estimate.estimate_date,
                        cxnote=estimate.customer_notes,subtotal=estimate.sub_total,igst=estimate.igst,cgst=estimate.cgst,sgst=estimate.sgst,t_tax=estimate.tax_amount,
                        grandtotal=estimate.total,status=estimate.status,terms_condition=estimate.terms_conditions,file=estimate.attachment,
                        sos=estimate.customer.placeofsupply,sh_charge=estimate.shipping_charge,estimate=estimate.id)
    sal.save()
    saleid = SalesOrder.objects.get(id=sal.id)
    for item in items:
        itemss = sales_item(product=item.item_name,quantity=item.quantity,hsn=item.hsn,tax=item.tax_percentage,
                             total=item.amount,desc=item.discount,rate=item.rate,sale=saleid)
        itemss.save()
    
    estimate.convert_sales=new_status
    estimate.save()

    
    return redirect('allestimates')


def retainer_invoice_sort_by_name(request):
    user=request.user.id
    ret_inv=RetainerInvoice.objects.filter(user=user).values()
    for r in ret_inv:
        vn = r['customer_name1'].split()[1:]
        r['cust_name'] = " ".join(vn)
    sorted_est = sorted(ret_inv, key=lambda r: r['cust_name'])  
    context = {
                'invoices' : sorted_est
            }  
    return render(request,'retainer_invoice.html',context)

"""def retainer_invoice_sort_by_no(request):
    user=request.user.id
    ret_inv=RetainerInvoice.objects.filter(user=user).values()
    for r in ret_inv:
        vn = r['retainer_invoice_number'].split("-")
        r['ret_no'] = " ".join(vn)
    sorted_est = sorted(ret_inv, key=lambda r: r['ret_no'])  
    context = {
                'invoices' : sorted_est
            }  
    return render(request,'retainer_invoice.html',context)"""

def retainer_invoice_sort_by_no(request):
    user=request.user.id
    ret_inv=RetainerInvoice.objects.filter(user=user).order_by("retainer_invoice_number")
    
    context = {
                'invoices' : ret_inv
            }  
    return render(request,'retainer_invoice.html',context)

def get_retainer_accno(request):
    user1=request.user.id
    user=User.objects.get(id=user1)
    idd=request.POST.get('id')
    if Bankcreation.objects.filter(id=idd,user=user).exists():
        account_ob=Bankcreation.objects.get(id=idd,user=user.id)
        account_number=account_ob.ac_no
        print(account_number)
        return JsonResponse({'account_number':account_number},safe=False)
    else:
        account_number=0000
        return JsonResponse({'account_number':account_number},safe=False)

def ret_invoice_status_edit(request,pk):
    est_data=RetainerInvoice.objects.get(id=pk)
    est_data.is_draft=0
    est_data.is_sent=1
    est_data.save()
    return redirect('invoice_view',est_data.id) 

def sort_retainer_view_name(request,pk):
    user=request.user
    company=company_details.objects.get(user=user)
    invoices=RetainerInvoice.objects.filter(user=user).values()
    invoice=RetainerInvoice.objects.get(id=pk)
    item=Retaineritems.objects.filter(retainer=pk)
    ret_comments=retainer_invoice_comments.objects.filter(retainer=invoice.id,user=user)
    for r in invoices:
        vn = r['customer_name1'].split()[1:]
        r['cust_name'] = " ".join(vn)
    sorted_est = sorted(invoices, key=lambda r: r['cust_name'])  

    context={'invoices':invoices,'invoice':invoice,'item':item,'company':company,'ret_comments':ret_comments,'invoices':sorted_est}
    return render(request,'invoice_view.html',context)

def sort_retainer_view_no(request,pk):
    user=request.user
    company=company_details.objects.get(user=user)
    invoices=RetainerInvoice.objects.filter(user=user).values()
    invoice=RetainerInvoice.objects.get(id=pk)
    item=Retaineritems.objects.filter(retainer=pk)
    ret_comments=retainer_invoice_comments.objects.filter(retainer=invoice.id,user=user)
    for r in invoices:
        vn = r['retainer_invoice_number'].split()[1:]
        r['cust_no'] = " ".join(vn)
    sorted_est = sorted(invoices, key=lambda r: r['cust_no'])  

    context={'invoices':invoices,'invoice':invoice,'item':item,'company':company,'ret_comments':ret_comments,'invoices':sorted_est}
    return render(request,'invoice_view.html',context)

def estimste_status_edit(request,pk):
    est_data=Estimates.objects.get(id=pk)
    est_data.status='Sent'
    est_data.save()
    if SalesOrder.objects.filter(estimate=pk).exists():
        sal=SalesOrder.objects.get(estimate=pk)
        sal.status='Sent'
        sal.save()
    if invoice.objects.filter(estimate=pk).exists():
        invo=invoice.objects.get(estimate=pk)
        invo.status='Sent'
        invo.save()
    return redirect('estimateslip',est_data.id)



# ................................  Settings.........................................

def go_settings(request):
    user_id=User.objects.get(id=request.user.id)
    my_settings=setting_list.objects.get(user=user_id)
    return render (request,'settings.html',{'my_settings':my_settings})

def edit_setting(request,pk):
    setting_obj=setting_list.objects.get(id=pk)
    items1=request.POST.get('item',False)
    pricelist1=request.POST.get('pricelist',False)
    offlinebanking1=request.POST.get('offlinebanking',False)
    banking1=request.POST.get('banking',False)
    customer1=request.POST.get('customer',False)
    estimate1=request.POST.get('estimate',False)
    retainerinvoice1=request.POST.get('retainerinvoice',False)
    salesorder1=request.POST.get('salesorder',False)
    deliverychallan1=request.POST.get('deliverychallan',False)
    invoice1=request.POST.get('invoice',False)
    creditnotes1=request.POST.get('creditnotes',False)
    recurringinvoice1=request.POST.get('recurringinvoice',False)
    vendor1=request.POST.get('vendor',False)
    vendorcredit1=request.POST.get('vendorcredit',False)
    expense1=request.POST.get('expense',False)
    recurringexpense1=request.POST.get('recurringexpense',False)
    purchaseorder1=request.POST.get('purchaseorder',False)
    paymentmade1=request.POST.get('paymentmade',False)
    bill1=request.POST.get('bill',False)
    recurringbill1=request.POST.get('recurringbill',False)
    project1=request.POST.get('project',False)
    chartofaccount1=request.POST.get('chartofaccount',False)
    employee1=request.POST.get('employee',False)
    employeeloan1=request.POST.get('employeeloan',False)
    pdf1=request.POST.get('pdf',False)
    slip1=request.POST.get('slip',False)
    print1=request.POST.get('print',False)
    if not items1:
        x="no"
        setting_obj.items=x
    else:
        x="yes"
        setting_obj.items=x
# ................................    
    if not pricelist1:
        x="no"
        setting_obj.pricelist=x
    else:
        x="yes"
        setting_obj.pricelist=x
# ................................  
    if not offlinebanking1:
        x="no"
        setting_obj.offline_banking=x
    else:
        x="yes"
        setting_obj.offline_banking=x
# ................................  
    if not banking1:
        x="no"
        setting_obj.banking=x
    else:
        x="yes"
        setting_obj.banking=x
# ................................  
    if not customer1:
        x="no"
        setting_obj.customers=x
    else:
        x="yes"
        setting_obj.customers=x
# ................................  
    if not estimate1:
        x="no"
        setting_obj.estimates=x
    else:
        x="yes"
        setting_obj.estimates=x
# ................................  
    if not retainerinvoice1:
        x="no"
        setting_obj.retainer_invoices=x
    else:
        x="yes"
        setting_obj.retainer_invoices=x   



# ................................  
    if not salesorder1:
        x="no"
        setting_obj.sales_orders=x
    else:
        x="yes"
        setting_obj.sales_orders=x  

# ................................  
    if not deliverychallan1:
        x="no"
        setting_obj.delivery_challans=x
    else:
        x="yes"
        setting_obj.delivery_challans=x  
# ................................  
    if not invoice1:
        x="no"
        setting_obj.invoices=x
    else:
        x="yes"
        setting_obj.invoices=x  
# ................................  
    if not creditnotes1:
        x="no"
        setting_obj.credit_notes=x
    else:
        x="yes"
        setting_obj.credit_notes=x  
# ................................  
    if not recurringinvoice1:
        x="no"
        setting_obj.recurring_invoices=x
    else:
        x="yes"
        setting_obj.recurring_invoices=x  
# ................................  
    if not vendor1:
        x="no"
        setting_obj.vendors=x
    else:
        x="yes"
        setting_obj.vendors=x  
# ................................  
    if not vendorcredit1:
        x="no"
        setting_obj.vendor_credits=x
    else:
        x="yes"
        setting_obj.vendor_credits=x  
# ................................  
    if not expense1:
        x="no"
        setting_obj.expenses=x
    else:
        x="yes"
        setting_obj.expenses=x  
# ................................  
    if not recurringexpense1:
        x="no"
        setting_obj.recurring_expenses=x
    else:
        x="yes"
        setting_obj.recurring_expenses=x  
# ................................  
    if not purchaseorder1:
        x="no"
        setting_obj.purchase_orders=x
    else:
        x="yes"
        setting_obj.purchase_orders=x  
# ................................  
    if not paymentmade1:
        x="no"
        setting_obj.payment_made=x
    else:
        x="yes"
        setting_obj.payment_made=x  
# ................................  
    if not bill1:
        x="no"
        setting_obj.bills=x
    else:
        x="yes"
        setting_obj.bills=x  
# ................................  
    if not recurringbill1:
        x="no"
        setting_obj.recurring_bills=x
    else:
        x="yes"
        setting_obj.recurring_bills=x  
# ................................  
    if not project1:
        x="no"
        setting_obj.projects=x
    else:
        x="yes"
        setting_obj.projects=x  
# ................................  
    if not retainerinvoice1:
        x="no"
        setting_obj.retainer_invoices=x
    else:
        x="yes"
        setting_obj.retainer_invoices=x  
# ................................  
    if not chartofaccount1:
        x="no"
        setting_obj.chart_of_accounts=x
    else:
        x="yes"
        setting_obj.chart_of_accounts=x  
# ................................  
    if not employee1:
        x="no"
        setting_obj.employees=x
    else:
        x="yes"
        setting_obj.employees=x    

# ................................  
    if not employeeloan1:
        x="no"
        setting_obj.employees_loan=x
    else:
        x="yes"
        setting_obj.employees_loan=x  
# ................................  
    if not pdf1:
        x="no"
        setting_obj.pdf=x
    else:
        x="yes"
        setting_obj.pdf=x  

# ................................  
    if not slip1:
        x="no"
        setting_obj.slip=x
    else:
        x="yes"
        setting_obj.slip=x  

# ................................  
    if not print1:
        x="no"
        setting_obj.print_opt=x
    else:
        x="yes"
        setting_obj.print_opt=x   


    setting_obj.save()
    return redirect("go_settings")

#Nikhila
class EmailAttachementView(View):
    form_class = EmailForm
    template_name = 'newmail.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'email_form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            files = request.FILES.getlist('attach')

            try:
                mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email])
                for f in files:
                    mail.attach(f.name, f.read(), f.content_type)
                mail.send()
                return render(request, self.template_name, {'email_form': form, 'error_message': 'Sent email to %s'%email})
            except:
                return render(request, self.template_name, {'email_form': form, 'error_message': 'Either the attachment is too big or corrupt'})

        return render(request, self.template_name, {'email_form': form, 'error_message': 'Unable to send email. Please try again later'})
        
#End

def item_statuschange(request,id):
    item=AddItem.objects.get(id=id)
    if item.satus == 'Active':
        item.satus = 'Inactive'
        item.save()
    else:
        item.satus = 'Inactive'
        item.satus = 'Active'
        item.save()
    return redirect('detail',item.id)

#_______________________Godown(new)_____________Antony Tom_________________

def add_godown(request):
    company=company_details.objects.get(user=request.user)
    additem=AddItem.objects.all()
    unit=Unit.objects.all()
    sale=Sales.objects.all()
    purchase=Purchase.objects.all()
    accounts = Purchase.objects.all()
    account_types = set(Purchase.objects.values_list('Account_type', flat=True))

    
    account = Sales.objects.all()
    account_type = set(Sales.objects.values_list('Account_type', flat=True))
    return render(request,'add_godown.html',{'additem':additem,'sale':sale,'purchase':purchase,'company':company,'unit':unit,
               
                            "account":account,"account_type":account_type,"accounts":accounts,"account_types":account_types,})

def view_godown(request):
    company = company_details.objects.get(user=request.user)
    user_id = request.user.id
    product = Addgodown.objects.all()
    deleted_godowns = Delete_godown.objects.filter(deletestatus=1).values_list('godown', flat=True)
    addgodown = Addgodown.objects.exclude(id__in=deleted_godowns)

    print(product)  

    return render(request, 'view_godown.html', {'addgodown': addgodown, 'company': company, 'product': product})




@login_required(login_url='login')
def get_itemsdet(request):
    company= company_details.objects.get(user = request.user)
    name = request.POST.get('name')
    id = request.POST.get('id')
    cust = AddItem.objects.get(user=company.user_id,id=id)
    hsn = cust.hsn
    cust_id=id
    print(hsn)
    return JsonResponse({'hsn' :hsn,'cust_id':cust_id},safe=False)

def get_item_info(request, item_id):
    try:
        item = AddItem.objects.get(pk=item_id)
        item_info = {
            'hsn': item.hsn,
            'stock': item.stock,  
        }
        return JsonResponse(item_info)
    except AddItem.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)


@login_required(login_url='login')
def save_godown(request):
    if request.method == 'POST':
        current_user = request.user.id
        
        date = request.POST['date']
        item = request.POST['item']
        hsn = request.POST['hsn']
        stockinhand = request.POST['stock']
        godown_name = request.POST['name']
        Address = request.POST['address']
        stockkeeping = request.POST['stockkeeping']
        kilometer = request.POST['Kilometer']
        user=User.objects.get(id=current_user)
        item1=AddItem.objects.get(id=item)

        godown = Addgodown(date=date, item=item,hsn=hsn,stockinhand=stockinhand, godownname=godown_name,
                              Address=Address, stockkeeping=stockkeeping, kilometer=kilometer,user=user,additem=item1)
        godown.save()

  
        return redirect('view_godown')  

    return render(request, 'add_godown.html')  



@login_required(login_url='login')
def add_modalgodown(request):
    company = company_details.objects.get(user=request.user)

    if request.method == 'POST':
        type = request.POST.get('type')
        name = request.POST.get('name')
        ut = request.POST.get('unit')
        hsnc = request.POST.get('hsn')
        inter = request.POST.get('inter')
        intra = request.POST.get('intra')
        sell_price = request.POST.get('sell_price')
        sell_acc = request.POST.get('sell_acc')
        sell_desc = request.POST.get('sell_desc')
        cost_price = request.POST.get('cost_price')
        cost_acc = request.POST.get('cost_acc')
        cost_desc = request.POST.get('cost_desc')
        stock = request.POST.get('stock')
        rate = request.POST.get('rate')

        units = Unit.objects.get(id=ut)
        sel = Sales.objects.get(id=sell_acc)
        cost = Purchase.objects.get(id=cost_acc)

        history = "Created by " + str(request.user)

        u = User.objects.get(id=request.user.id)

        item = AddItem(type=type, Name=name, p_desc=cost_desc, s_desc=sell_desc, s_price=sell_price, p_price=cost_price,
                        user=u, creat=history, interstate=inter, intrastate=intra, unit=units, sales=sel, purchase=cost,
                        hsn=hsnc, stock=stock, rate=rate)

        item.save()

       
        added_item = {
            'id': item.id,
            'Name': item.Name
        }

        return JsonResponse(added_item)
    
    return HttpResponse("Invalid request method.")


@login_required(login_url='login')
def add_unitmodal(request):
    if request.method == 'POST':
        unit_name = request.POST['unit_name']
        unit = Unit(unit=unit_name)  
        unit.save()  
        unit_id = unit.id  
        return JsonResponse({"unit_name": unit_name, "unit_id": unit_id})
    return render(request, "add_godown.html")

@login_required(login_url='login')
def godownoverview(request,id):
    company=company_details.objects.get(user=request.user)
    user_id=request.user
    product=Addgodown.objects.get(id=id)
    Comments=Comments_godown.objects.filter(godown=product.id,user=user_id)

    deleted_godowns = Delete_godown.objects.filter(deletestatus=1).values_list('godown', flat=True)

    viewgodown = Addgodown.objects.exclude(id__in=deleted_godowns)
    
    return render(request,'godownoverview.html',{'viewgodown':viewgodown,'product':product,'Comments':Comments})


@login_required(login_url='login')
def godown_edit(request,id):
    item=AddItem.objects.all()
    godown=Addgodown.objects.all()
    edit=Addgodown.objects.get(id=id)
    company=company_details.objects.get(user=request.user)
    return render(request,'editgodown.html',{'e':edit,'godown':godown,'company':company,'item':item})


@login_required(login_url='login')
def edit_savegodown(request, id):
    additem = Addgodown.objects.all()
    edit = Addgodown.objects.get(id=id)
    company = company_details.objects.get(user=request.user)

    if request.method == 'POST':
        
        new_item_id = request.POST.get('item')

        
        if new_item_id:
            new_item = AddItem.objects.get(id=new_item_id)
            edit.additem = new_item

       
        edit.item = request.POST.get('item')
        edit.date = request.POST.get('date')
        edit.hsn = request.POST['hsn']
        edit.stockinhand = request.POST['stock']
        edit.godownname = request.POST['name']
        edit.Address = request.POST['address']
        edit.stockkeeping = request.POST['stockkeeping']
        edit.kilometer = request.POST['Kilometer']

        edit.save()

        return redirect('godownoverview', id=edit.id)

    return render(request, 'editgodown.html', {'e': edit, 'additem': additem, 'company': company})


@login_required(login_url='login')
def deletegodownoverview(request,id):
    godown = Addgodown.objects.get(id=id)

    if request.method == 'POST':
        reason = request.POST.get('deletereason')
        current_user = request.user

    
        new_godown = Delete_godown(
            user=current_user,
            godown=godown,
            reason=reason,
            deletestatus=1  
        )
        new_godown.save()

        return redirect('view_godown')

    return render(request, 'godownoverview.html')


@login_required(login_url='login')
def deleteviewgodown(request, id):
    godown = Addgodown.objects.get(id=id)

    if request.method == 'POST':
        reason = request.POST.get('deletereason')
        current_user = request.user

        
        new_godown = Delete_godown(
            user=current_user,
            godown=godown,
            reason=reason,
            deletestatus=1  
        )
        new_godown.save()

        return redirect('view_godown')

    return render(request, 'view_godown.html')



def commentgodown(request,product_id):
    if request.method=="POST":
        user=request.user      
        godown=Addgodown.objects.get(id=product_id)
       
        content=Comments_godown()
        content.user=user
        content.godown=godown
        content.content=request.POST.get('comments')
       
        content.save()
    return redirect('godownoverview',godown.id)

def editcommentgodown(request, product_id):
    if request.method == 'POST':
        user=request.user      
        godown=Addgodown.objects.get(id=product_id)
        edited_comment = request.POST['edited_comment']
        comment_id = request.POST['comment_id']
        
        # Get the comment based on its ID
        comment = Comments_godown.objects.get(id=comment_id)
        comment.content = edited_comment
        comment.save()
        return redirect("godownoverview",godown.id)


@login_required(login_url='login')
def delete_commentgodown(request, product_id, comment_id):
    try:
        comment = Comments_godown.objects.get(id=comment_id, godown=product_id, user=request.user)
        comment.delete()
    except Comments_godown.DoesNotExist:
        pass

    return redirect('godownoverview', product_id)



def godown_active(request,id):
    p=Addgodown.objects.get(id=id)
    if p.satus == 'Active':
        p.satus = 'Inactive'
    else:
        p.satus = 'Active'
    p.save()
    return redirect('godownoverview',id=id)

def upload_documentsgodown(request, godown_id):
    if request.method == 'POST':
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        godown = Addgodown.objects.get(id=godown_id)
        attachment_file = request.FILES.get('attachment')

        doc_data = Attachgodown.objects.create(user=user, godown=godown, attachment=attachment_file)
        doc_data.save()

        return redirect("godownoverview", id=godown_id)

@login_required(login_url='login')
def add_sales_godown(request):
    if request.method=='POST':
        Account_type  =request.POST['acc_type']
        Account_name =request.POST['acc_name']
        Acount_code =request.POST['acc_code']
        Account_desc =request.POST['acc_desc']        
        acc=Purchase(Account_type=Account_type,Account_name=Account_name,Acount_code=Acount_code,Account_desc=Account_desc)
        acc.save()
        return redirect("add_godown")
    return render(request,"add_godown.html")


@login_required(login_url='login')
def godownmodal_unit(request):
    
    company = company_details.objects.get(user = request.user)

    if request.method=='POST':

        unit =request.POST.get('unit')
        
        u = User.objects.get(id = request.user.id)

        unit = Unit(unit= unit)
        unit.save()

        return HttpResponse({"message": "success"})


@login_required(login_url='login')
def godownunit_dropdown(request):

    user = User.objects.get(id=request.user.id)

    options = {}
    option_objects = Unit.objects.all()
    for option in option_objects:
        options[option.id] = [option.unit,option.id]

    return JsonResponse(options)
    
    
#End

def draft_expense(request):
    if request.method == 'POST':
        print('draftbutton click')
        # Retrieve form data
        userId=request.user.id
        profile_name = request.POST['profile_name']
        repeatevery = request.POST['repeat_every']
        repeat=repeat_every.objects.filter(id=repeatevery).first()
        start_date = request.POST['start_date']
        expense_account_id  = request.POST['expense_account']
        expense_account = Account.objects.filter(pk=expense_account_id).first()

        refrenc=request.POST['refrnsid']

        expense_type = request.POST['expense_type']
          
        hsn = request.POST['goods_label']
        sac = request.POST['services_label']
        amount = request.POST['amount']
        currency = request.POST['currency']
        paidthrough = request.POST['paidthrough']
        cheque_id = request.POST.get('chequeId')
        upi_number = request.POST.get('upiNumber')
        bank_account = request.POST.get('bankAccount')
        vendor_id = request.POST['vendor']
        vendor = get_object_or_404(vendor_table, pk=vendor_id)
        gst_treatment=request.POST['gst_trt_inp']
        gst = request.POST.get('gstin_inp')
        vmail=request.POST['vmail']
        vdestination = request.POST['destination']
        tax = request.POST.getlist('tax[]',[])
        notes = request.POST['notes']
        customer_id = request.POST['customername']
        customer_obj = get_object_or_404(customer, pk=customer_id)
        cust_gsttreatmnt=request.POST['cu_gst_trt']
        custemail=request.POST.get('mail')
        cust_pos=request.POST['c_destination']
        # Handle the ends_on field
        file=request.FILES.get('file')
       
        udata=User.objects.get(id=userId)
       
        # Create and save the Expense instance
        expense = Expense(
            profile_name=profile_name,
            repeatevery=repeat,
            start_date=start_date,
           
            expense_account=expense_account,
            refrenceid=refrenc,
            expense_type=expense_type,
            hsn=hsn,
            sac=sac,
            amount=amount,
            currency=currency,
            paidthrough=paidthrough,
            cheque_id=cheque_id, 
            upi_number=upi_number,
            bank_account=bank_account,
            vendor=vendor,
            gst_treatment=gst_treatment,
            gst=gst,
            vendor_destination=vdestination,
            tax=tax,
            notes=notes,
            customer= customer_obj,
            customeremail=custemail,
            cust_gsttreatment=cust_gsttreatmnt,
            cust_placeofsupply=cust_pos,
            vendormail= vmail,
            document=file,
            activation_tag="Active", # Set the activation_tag to "active"
            status='Draft',
            user=udata
            
        )
        expense.save()

        return redirect('recurringbase')
    else:
       
        return render(request, 'recurring_home.html')
        
def recurring_expense_draft(request,expense_id):
   
    userid = request.user.id
    company = company_details.objects.get(user=userid)
    expenses = Expense.objects.filter(user = userid, status = 'Draft')
    expense = get_object_or_404(Expense, id=expense_id)
 
  
    context = {
        'company': company,
        'expense': expense,
        'expenses':expenses
       
        
    }
    return render(request, 'show_recurring.html', context)
    
    
def recurring_expense_save(request,expense_id):
    userid = request.user.id
    company = company_details.objects.get(user=userid)
    expenses = Expense.objects.filter(user = userid, status = 'Save')
    expense = get_object_or_404(Expense, id=expense_id)
    
    
    context = {
        'company': company,
        'expense': expense,
        'expenses':expenses
        
    }
    return render(request, 'show_recurring.html', context)
    
    
login_required(login_url='login')
def get_customer_gsttrmnt(request):
    if request.method == 'GET':
        customer_id = request.GET.get('customername')
        custmer = customer.objects.get(id=customer_id)
        gst_trtmnt=custmer.GSTTreatment
        pos=custmer.placeofsupply
        return JsonResponse({'gst_trtmnt': gst_trtmnt,'pos':pos})
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    
def get_vendor_place_of_supply(request):
    if request.method == 'GET':
        vendor_id = request.GET.get('vendor')
        
        try:
            vendor = vendor_table.objects.get(pk=vendor_id)
            source_supply = vendor.source_supply
            print(f"Found source supply: {source_supply}")
            return JsonResponse({'source_supply': source_supply})
        except vendor_table.DoesNotExist:
            return JsonResponse({'error': 'Vendor not found'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    
def covert_to_status(request, id): 
    
    expense = Expense.objects.get(user=request.user, id=id)
    
    if expense.status == 'Draft':
        expense.status = 'Save'
    elif expense.status == 'Save':
        expense.status = 'Draft'
    expense.save()  
    
    return redirect('show_recurring', id)
    
    
def recurring_expense_details(request):
    company = company_details.objects.get(user=request.user)
    expense=Expense.objects.filter(user=request.user)
    account=Account.objects.filter(user=request.user)
    vendor=vendor_table.objects.filter(user=request.user)
    custmr=customer.objects.filter(user=request.user)
    bank=Bankcreation.objects.all()

    
    context={
      'company':company,
      'expense':expense,
      'account':account,
      'vendor':vendor,
      'custmr':custmr,
      'bank':bank
        
    }
    return render(request,'expens_details.html', context)
    
    
def invoice_details(request):
    company = company_details.objects.get(user=request.user)
    invoices = invoice.objects.filter(user=request.user)
    return render(request,'invoice_details.html',{'company':company,'invoice':invoices})

#___________________________Ashikh V U (start)__________________________________
@login_required(login_url='login')
def payment_type_cash_in_hand(request):
    return render(request,'payment_type_cash_in_hand.html',{})
    
@login_required(login_url='login')
def generate_pdf3(request,string_date,start_d,end_d):
    print(f'start date : {start_d}  end date : {end_d}')

    buffer = BytesIO()
    # p = canvas.Canvas(buffer,pagesize=A4)
    pdf_filename = "sample.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)


    # doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    customers = customer.objects.filter(user=request.user.id)
    d = string_date

    data = [["DATE", "TYPE", "AMOUNT","BALANCE"]]

    heading_style = ParagraphStyle(
        'Heading1',
        parent=getSampleStyleSheet()['Heading1'],
        alignment=1,  # Centered alignment
        fontSize=16,
        fontName='Helvetica-Bold',
    )
    heading_style1 = ParagraphStyle(
        'Heading1',
        parent=getSampleStyleSheet()['Heading1'],
        alignment=1,  # Centered alignment
        fontSize=10,
        fontName='Helvetica',
    )
    heading_style3 = ParagraphStyle(
        'Heading1',
        parent=getSampleStyleSheet()['Heading1'],
        alignment=1,  # Centered alignment
        fontSize=15,
        fontName='Helvetica',
    )
    company = company_details.objects.get(id=request.user.id)
    heading3 = Paragraph(company.company_name, heading_style3)
    heading = Paragraph("CASH IN HAND", heading_style)
    heading1 = Paragraph(f"{d}", heading_style1)
    elements.append(heading3)
    elements.append(heading)
    elements.append(heading1)

    for _ in customers:
        data.append(["---------","-----","---------","---------"])

    table = Table(data,colWidths='*')

    style = TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN',(0,1),(-1,-1 ),'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    table.setStyle(style)
    elements.append(table)
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
    # response.write(pdf)
    with open(pdf_filename, 'rb') as pdf_file:
        response.write(pdf_file.read())
    return response 

@login_required(login_url='login')
def payment_type_upi(request):
    sales = SalesOrder.objects.filter(Q(pay_method='UPI') | Q(pay_method='upi'))
    total_upi_amount = sum([i.grandtotal for i in sales])
    return render(request,'payment_type_upi.html',{'sales':sales,
                                                    'total_upi_amount':total_upi_amount})


@login_required(login_url='login')
def payment_type_upi_get_data(request):
    sales = SalesOrder.objects.filter(Q(pay_method='UPI') | Q(pay_method='upi'))
    total_upi_amount = sum([i.grandtotal for i in sales])
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    if start_date != '' and end_date != '':
        sales = sales.filter(sales_date__gte=start_date,sales_date__lte=end_date)
        total_upi_amount = sum([i.grandtotal for i in sales])
    return TemplateResponse(request,'payment_type_upi_get_data.html',{'sales':sales,
                                                                    'total_upi_amount':total_upi_amount})

@login_required(login_url='login')
def generate_pdf4(request,jsondict,start_d,end_d):

    dict = json.loads(jsondict)
    start_date = dict["start_date"]
    end_date = dict["end_date"]

    sales = SalesOrder.objects.filter(Q(pay_method='UPI') | Q(pay_method='upi'))
    total_upi_amount = sum([i.grandtotal for i in sales])
    print(f'\n{start_date}\n{end_date}\n')
    if start_date != '' and end_date != '':
        sales = sales.filter(sales_date__gte=start_date,sales_date__lte=end_date)
        total_upi_amount = sum([i.grandtotal for i in sales])

    
    print(f'start date : {start_d}  end date : {end_d} total:{dict["total_upi_amount"]}')
    print(f'date : {dict["string_date"]}   total :{dict["total_upi_amount"]} ')

    print(f'\nstart date here : {dict["start_date"]}\n{dict["end_date"]}\n')

    total1 = str(total_upi_amount)

    buffer = BytesIO()
    # p = canvas.Canvas(buffer,pagesize=A4)
    pdf_filename = "sample.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)


    # doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    customers = customer.objects.filter(user=request.user.id)
    d = dict["string_date"]
    # d='uncomment the d in generatepdf4 and commend this'

    data = [["DATE", "TYPE", "UPI ID","AMOUNT"]]

    heading_style = ParagraphStyle(
        'Heading1',
        parent=getSampleStyleSheet()['Heading1'],
        alignment=1,  # Centered alignment
        fontSize=16,
        fontName='Helvetica-Bold',
    )
    heading_style1 = ParagraphStyle(
        'Heading1',
        parent=getSampleStyleSheet()['Heading1'],
        alignment=1,  # Centered alignment
        fontSize=10,
        fontName='Helvetica',
    )
    heading_style3 = ParagraphStyle(
        'Heading1',
        parent=getSampleStyleSheet()['Heading1'],
        alignment=1,  # Centered alignment
        fontSize=15,
        fontName='Helvetica',
    )
    company = company_details.objects.get(user = request.user)
    heading3 = Paragraph(company.company_name, heading_style3)
    heading = Paragraph("UPI DETAILS", heading_style)
    heading1 = Paragraph(f"{d}", heading_style1)
    elements.append(heading3)
    elements.append(heading)
    elements.append(heading1)

    for i in sales:
        data.append([str(i.sales_date),str(i.pay_method),str(i.upi_id),str(i.grandtotal)])

    data.append(["TOTAL UPI AMOUNT","","",""+total1])

    table = Table(data,colWidths='*')

    style = TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN',(0,1),(-1,-1 ),'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    table.setStyle(style)
    elements.append(table)
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
    # response.write(pdf)
    with open(pdf_filename, 'rb') as pdf_file:
        response.write(pdf_file.read())
    return response 

@login_required(login_url='login')
def payment_type_bank(request):
    banks = Bankcreation.objects.filter(user=request.user)
    transaction = transactions.objects.filter(user=request.user)
    return render(request,'payment_type_bank.html',{"banks":banks,
                                                    'transaction':transaction})

@login_required(login_url='login')
def generate_pdf5(request,jsondict,start_d,end_d):
    print(f'start date : {start_d}  end date : {end_d}')

    dict = json.loads(jsondict)
    start_date = dict["start_date"]
    end_date = dict["end_date"]
    print(start_date)
    print(end_date)

    banks = Bankcreation.objects.filter(user=request.user)
    bank_name = dict['bank_name']
    if bank_name != '':
        bank_detail = Bankcreation.objects.get(name=bank_name,user=request.user)
        transaction = transactions.objects.filter(user=request.user,bank_id=bank_detail.id)
        if start_date != "" and end_date != "":
            transaction = transaction.filter(date__gte=start_date,date__lte=end_date)
    else:
        transaction = transactions.objects.filter(user=request.user)
        if start_date != "" and end_date != "":
            transaction = transaction.filter(date__gte=start_date,date__lte=end_date)
    

    buffer = BytesIO()
    # p = canvas.Canvas(buffer,pagesize=A4)
    pdf_filename = "sample.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)


    # doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    d = dict['string_date']

    data = [["DATE", "TYPE","AMOUNT","BALANCE"]]

    heading_style = ParagraphStyle(
        'Heading1',
        parent=getSampleStyleSheet()['Heading1'],
        alignment=1,  # Centered alignment
        fontSize=16,
        fontName='Helvetica-Bold',
    )
    heading_style1 = ParagraphStyle(
        'Heading1',
        parent=getSampleStyleSheet()['Heading1'],
        alignment=1,  # Centered alignment
        fontSize=10,
        fontName='Helvetica',
    )
    heading_style3 = ParagraphStyle(
        'Heading1',
        parent=getSampleStyleSheet()['Heading1'],
        alignment=1,  # Centered alignment
        fontSize=15,
        fontName='Helvetica',
    )
    company = company_details.objects.get(user=request.user)
    heading3 = Paragraph(company.company_name, heading_style3)
    heading = Paragraph("BANK DETAILS", heading_style)
    heading1 = Paragraph(f"{d}", heading_style1)
    elements.append(heading3)
    elements.append(heading)
    elements.append(heading1)


    for i in transaction:
        data.append([str(i.date),str(i.type),str(i.amount),"--------"])

    # for i in transaction:
    #     data.append([str(i.date),str(i.type),str(i.amount),str(i.bank.balance)])

    # data.append(["Balance","","","","0.00"])
    # data.append(["Balance","","","",str(bank_detail.balance)])

    table = Table(data,colWidths='*')
    # table = Table(data)

    style = TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN',(0,1),(-1,-1 ),'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    table.setStyle(style)
    elements.append(table)
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
    # response.write(pdf)
    with open(pdf_filename, 'rb') as pdf_file:
        response.write(pdf_file.read())
    return response 


@login_required(login_url='login')
def payment_type_bank_get_data(request):
    print('\n\nenterd\n\n')
    startdate = request.POST.get('start_date')
    enddate = request.POST.get('end_date')
    banks = Bankcreation.objects.filter(user=request.user)
    try:
        bank_name = request.POST.get('bank_name')
        bank_detail = Bankcreation.objects.get(user=request.user,name=bank_name)
        transaction = transactions.objects.filter(user=request.user,bank_id=bank_detail.id)
        if enddate != "" and startdate != "":
            transaction = transaction.filter(date__gte=startdate,date__lte=enddate)
    except:
        transaction = transactions.objects.filter(user=request.user)
        if enddate != "" and startdate != "":
            transaction = transaction.filter(date__gte=startdate,date__lte=enddate)
        bank_detail= None
    return TemplateResponse(request,"payment_type_bank_get_data.html",{"banks":banks,
                                                                        "transaction":transaction,
                                                                        "bank_detail":bank_detail,})
#___________________________Ashikh V U (end)__________________________________

def save_payment_term(request):
    if request.method == 'POST':
        term_name = request.POST.get('name')
        term_days = request.POST.get('days')

        # Create a new payment term object and save it to the database
        new_term = payment_terms.objects.create(name=term_name, days=term_days)

        # Return a JsonResponse with the ID of the newly created term
        return JsonResponse({'id': new_term.id, 'name': new_term.name, 'days': new_term.days})
    else:
        return JsonResponse({'error': 'Invalid request method'})
        
def get_payment_terms_view(request):
    if request.method == 'GET':
        payment_terms_list = payment_terms.objects.all()  
        terms = []
        for term in payment_terms_list:
            terms.append({
                'id': term.id,
                'Terms': term.Terms,
                'Days': term.Days,
            })
        return JsonResponse({'payment_terms': terms})
        
def get_all_payment_terms(request):
    
    payment_terms = payment_terms.objects.all()

    # Serialize payment terms to JSON
    terms_list = [{'id': term.id, 'name': term.Terms, 'days': term.Days} for term in payment_terms]

    return JsonResponse(terms_list, safe=False)
    
def get_customer_details(request):
    if request.method == 'GET':
        customer_id = request.GET.get('customer_id')
        try:
            cust = customer.objects.get(id=customer_id)
            customer_data = {
                'email': cust.customerEmail,
                'gst_treatment': cust.GSTTreatment,
                'gst_number': cust.GSTIN,
                'place_of_supply': cust.placeofsupply,
            }
            return JsonResponse(customer_data)
        except customer.DoesNotExist:
            return JsonResponse({'error': 'Customer not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
        
def invoice_overview(request,id):
    user=request.user
    inv_dat=invoice.objects.filter(user=user)
    inv_master=invoice.objects.get(id=id)
    customers= customer.objects.filter(user=user,invoice=id)
    invoiceitem=invoice_item.objects.filter(inv_id=id)
    company=company_details.objects.get(user_id=request.user.id)
    inv_comments=invoice_comments.objects.filter(user=user,invoice=id)
    payment=InvoicePayment.objects.filter(invoice=id)
    bank= Bankcreation.objects.filter(user=user)
    
    context={
        'inv_dat':inv_dat,
        'invoiceitem':invoiceitem,
        'company':company,
        'invoice':inv_master,
        'inv_comments':inv_comments,
        'customers':customers,
        'payment':payment,
        'bank':bank,
    }
    return render(request,'invoice_overview.html',context)
    
    
def delivery_challan_overview(request, id):
    user = request.user
    company = company_details.objects.get(user=user)
    all_estimates = DeliveryChellan.objects.filter(user=user)
    estimate = DeliveryChellan.objects.get(id=id)
    items = ChallanItems.objects.filter(chellan=estimate)
    chellan_comments = delivery_chellan_comments.objects.filter(chellan=estimate.id, user=user)
    
    print(items)
    context = {
        'company': company,
        'all_estimates': all_estimates,
        'estimate': estimate,
        'items': items,
        'comments': chellan_comments,
        
    }
    return render(request, 'delivery_challan_overview.html', context)
    
    
def filter_invoice_overview_send(request,id):
    user=request.user
    inv_dat=invoice.objects.filter(user=user,status="send")
    inv_master=invoice.objects.get(id=id)
    invoiceitem=invoice_item.objects.filter(inv_id=id)
    company=company_details.objects.get(user_id=request.user.id)
    
    
    customers= customer.objects.filter(user=user,invoice=id)
    invoiceitem=invoice_item.objects.filter(inv_id=id)
    company=company_details.objects.get(user_id=request.user.id)
    inv_comments=invoice_comments.objects.filter(user=user,invoice=id)
    payment=InvoicePayment.objects.filter(invoice=id)
    bank= Bankcreation.objects.filter(user=user)
    
    
    
    context={
        'inv_dat':inv_dat,
        'invoiceitem':invoiceitem,
        'comp':company,
        'invoice':inv_master,
        'inv_dat':inv_dat,
        'invoiceitem':invoiceitem,
        'company':company,
        'invoice':inv_master,
        'inv_comments':inv_comments,
        'customers':customers,
        'payment':payment,
        'bank':bank,
    }
    return render(request,'invoice_overview.html',context)
    
    
def filter_invoice_overview_draft(request,id):
    user=request.user
    inv_dat=invoice.objects.filter(user=user,status="draft")
    inv_master=invoice.objects.get(id=id)
    invoiceitem=invoice_item.objects.filter(inv_id=id)
    company=company_details.objects.get(user_id=request.user.id)
    
    customers= customer.objects.filter(user=user,invoice=id)
    invoiceitem=invoice_item.objects.filter(inv_id=id)
    company=company_details.objects.get(user_id=request.user.id)
    inv_comments=invoice_comments.objects.filter(user=user,invoice=id)
    payment=InvoicePayment.objects.filter(invoice=id)
    bank= Bankcreation.objects.filter(user=user)
    
    
    
    
    context={
        'inv_dat':inv_dat,
        'invoiceitem':invoiceitem,
        'comp':company,
        'invoice':inv_master,
        'company':company,
        'invoice':inv_master,
        'inv_comments':inv_comments,
        'customers':customers,
        'payment':payment,
        'bank':bank,
    }
    return render(request,'invoice_overview.html',context)
    
def invoice_slip(request,id):
    user=request.user
    inv_dat=invoice.objects.filter(user=user)
    inv_master=invoice.objects.get(id=id)
    invoiceitem=invoice_item.objects.filter(inv_id=id)
    company=company_details.objects.get(user_id=request.user.id)
    inv_comments=invoice_comments.objects.filter(user=user,invoice=id)
    
    
    context={
        'inv_dat':inv_dat,
        'invoiceitem':invoiceitem,
        'company':company,
        'invoice':inv_master,
        'inv_comments':inv_comments,
    }
    return render(request,'invoice_slip.html',context)
    
    
def change_status_invoice(request, id):
    invoic = invoice.objects.get(id=id)
    invoic.status = 'Send'
    invoic.save()
    return redirect('invoice_overview', id=id)
    
    
# Expense by Employee
def expensebyemployee(request):
    emplo=Payroll.objects.all()
    company_data = company_details.objects.get(user=request.user)
    return render(request,'expence_by_employee.html',{"emplo":emplo,"company":company_data})  

def customize_expenseemployee_report(request):
    return render(request,'customize_expense_by_employee.html')

def milege(request):
    return render(request,'expense_milege.html')

def nonmilege(request):
    return render(request,'expense_nonmilege.html')  

#expense by project
def expensebyproject(request):
    cust = customer.objects.all()
    proj=project1.objects.all()
    company_data = company_details.objects.get(user=request.user)
    return render(request,'expense_by_project.html',{"company":company_data,"cust":cust,'proj':proj}) 


def customize_expenseproject_report(request):
    cust = customer.objects.all()
    proj=project1.objects.all()
    return render(request,'customize_expensebyproject.html',{'cust':cust,"proj":proj})

#End

def delivery_challan_slip(request, id):
    user = request.user
    company = company_details.objects.get(user=user)
    
    all_estimates = DeliveryChellan.objects.filter(user=user)
    estimate = DeliveryChellan.objects.get(id=id)
    items = ChallanItems.objects.filter(chellan=estimate)
    chellan_comments = delivery_chellan_comments.objects.filter(chellan=estimate.id, user=user)
    print(items)
    context = {
        'company': company,
        'all_estimates': all_estimates,
        'estimate': estimate,
        'items': items,
        'comments': chellan_comments,
        
    }
    return render(request, 'delivery_challan_slip.html', context)


def filter_by_draft_chellan_overview(request,pk):
    user = request.user
    company = company_details.objects.get(user=user)
    all_estimates = DeliveryChellan.objects.filter(user=user,status='draft')
    estimate = DeliveryChellan.objects.get(id=pk)
    items = ChallanItems.objects.filter(chellan=estimate)
    context = {
        'company': company,
        'all_estimates':all_estimates,
        'estimate': estimate,
        'items': items,
    }
    return render(request, 'delivery_challan_overview.html', context)
    
def filter_by_sent_chellan_overview(request,pk):
    user = request.user
    company = company_details.objects.get(user=user)
    all_estimates = DeliveryChellan.objects.filter(user=user,status='send')
    estimate = DeliveryChellan.objects.get(id=pk)
    items = ChallanItems.objects.filter(chellan=estimate)
    context = {
        'company': company,
        'all_estimates':all_estimates,
        'estimate': estimate,
        'items': items,
    }
    return render(request, 'delivery_challan_overview.html', context)





def convert_challan_to_invoice(request, id):
    
    challan = DeliveryChellan.objects.get(id=id)
    user = request.user
    company = company_details.objects.get(user=user)
    all_estimates = DeliveryChellan.objects.filter(user=user)
    estimate = DeliveryChellan.objects.get(id=id)
    items = ChallanItems.objects.filter(chellan=estimate)
    chellan_comments = delivery_chellan_comments.objects.filter(chellan=estimate.id, user=user)
    

   
    new_invoice = invoice(
        user=challan.user,
        customer=challan.cu,
        invoice_no=challan.chellan_no,
        terms=challan.terms_conditions,
        order_no=0,  # Update this value as needed
        inv_date=challan.chellan_date,
        due_date=challan.chellan_date,  # Update this value as needed
        igst=challan.igst,
        cgst=challan.cgst,
        sgst=challan.sgst,
        t_tax=challan.tax_amount,
        subtotal=challan.sub_total,
        shipping_charge=challan.shipping_charge,
        adjustment=challan.adjustment,
        grandtotal=challan.total,
        cxnote=challan.customer_notes,
        terms_condition=challan.terms_conditions,
        status=challan.status,
        file=challan.attachment,
        estimate=None,  # Update this value as needed
        paid_amount=0.0,
        balance=challan.total  # Set the balance to the total amount initially
    )
    new_invoice.save()

    # Retrieve the corresponding ChallanItems and create corresponding invoice_items
    challan_items = ChallanItems.objects.filter(chellan=challan)
    for item in challan_items:
        new_invoice_item = invoice_item(
            product=item.item_name,
            quantity=item.quantity,
            hsn=item.hsn,
            tax=item.tax_percentage,
            total=item.amount,
            discount=item.discount,
            rate=item.rate,
            inv=new_invoice
        )
        new_invoice_item.save()
        
        context = {
        
        'company': company,
        'all_estimates': all_estimates,
        'estimate': estimate,
        'items': items,
        'comments': chellan_comments,
        
        
    }

    return render(request, 'delivery_challan_overview.html', context)

def custmz_rprt_shw_hide(request):
    customer1 = customer.objects.all()
    company= company_details.objects.get(user=request.user)
    return render(request, 'custmz_rprt_shw_hide.html', {'cust': customer1, 'company': company},)  


def productsalereport(request):
    company = company_details.objects.get(user=request.user)
    item=AddItem.objects.all()
    inv = invoice_item.objects.all()
    rinv = Recurring_invoice.objects.all()
    pdebit_list = [] 
    for i in rinv:
        pdebit = recur_itemtable.objects.filter(ri=i)
        
        # Append each pdebit object to the pdebit_list
        for pd in pdebit:
            pdebit_list.append(pd)
    
   

    context = {'company':company,"inv":inv,"rinv":rinv,'item':item,'pdebit':pdebit_list
        }
    return render(request, 'productsaletwo.html', context)
    
    
def inven_salecount(request):
    company = company_details.objects.get(user=request.user)
    item=AddItem.objects.all()
    inv=invoice_item.objects.all()
    rinv=recur_itemtable.objects.all()
    estim=EstimateItems.objects.all()
    sorder=sales_item.objects.all()
    vencredit=Vendor_invoice_item.objects.all()
    totalsale=0
    totalsale1=0
    totalsale2=0
    totalsale3=0
    totalsale4=0
    subtotalsale=0
    subtotalsale1=0
    subtotalsale2=0
    subtotalsale3=0
    subtotalsale4=0
    count=0
    count1=0
    count2=0
    count3=0
    count4=0
    for i in rinv:
        count1 +=1
        print(count)
        if i.ri.total != 'NULL' or i.ri.total != " ":
            totalsale1 += float(i.ri.total)
            
        if i.ri.sub_total != 'NULL' or i.ri.sub_total != " ":
            subtotalsale1 += float(i.ri.sub_total)
    for i in inv:
        count +=1
        if i.inv.grandtotal != 'NULL' or i.inv.grandtotal != " ":
            totalsale += float(i.inv.grandtotal)
        if i.inv.subtotal != 'NULL' or i.inv.subtotal!= " ":
            subtotalsale += float(i.inv.subtotal)
        
    for i in estim:
        count2 +=1
        if i.estimate.total != 'NULL' or i.estimate.total != " ":
            totalsale2 += float(i.estimate.total)
        if i.estimate.sub_total != 'NULL' or i.estimate.sub_total != " ":
            subtotalsale2 += float(i.estimate.sub_total)
    for i in sorder:
        count3 +=1
        if i.sale.grandtotal != 'NULL' or i.sale.grandtotal != " ":
            totalsale3 += float(i.sale.grandtotal)
        if i.sale.subtotal != 'NULL' or i.sale.subtotal!= " ":
            subtotalsale3 += float(i.sale.subtotal)
    for i in vencredit:
        count4 +=1
        if i.inv.grandtotal != 'NULL' or i.inv.grandtotal != " ":
            totalsale4 += float(i.inv.grandtotal)
        if i.inv.subtotal != 'NULL' or i.inv.subtotal!= " ":
            subtotalsale4 += float(i.inv.subtotal)
          

    sale=totalsale
    sale1=totalsale1
    sale2=totalsale2
    sale3=totalsale3
    sale4=totalsale4
    subsale=subtotalsale
    subsale1=subtotalsale1
    subsale2=subtotalsale2
    subsale3=subtotalsale3
    subsale4=subtotalsale4
    sale='{:.2f}'.format(sale)
    sale1='{:.2f}'.format(sale1)
    sale2='{:.2f}'.format(sale2)
    sale3='{:.2f}'.format(sale3)
    sale4='{:.2f}'.format(sale4)
    subsale='{:.2f}'.format(subsale)
    subsale1='{:.2f}'.format(subsale1)
    subsale2='{:.2f}'.format(subsale2)
    subsale3='{:.2f}'.format(subsale3)
    subsale4='{:.2f}'.format(subsale4)
    context={
        'count':count,
        'count1':count1,
        'count2':count2,
        'count3':count3,
        'count4':count4,
        'item':item,
        'rinv':rinv,
        'inv':inv,
        'company':company,
        'estim':estim,
        'sorder':sorder,
        
        'vencredit':vencredit,
        'sale':sale,
        'sale1':sale1,
        'sale2':sale2,
        'sale3':sale3,
        'sale4':sale4,
        'subsale':subsale,
        'subsale1':subsale1,
        'subsale2':subsale2,
        'subsale3':subsale3,
        'subsale4':subsale4,
    }
    return render(request,'inventorysalecount.html', context)
    
    
def productsale_filter(request):
    company = company_details.objects.get(user=request.user)
    inv = sales_item.objects.all()
    rinv =recur_itemtable.objects.all()
    estim=EstimateItems.objects.all()
    sorder=sales_item.objects.all()
    vencredit=Vendor_invoice_item.objects.all()
    totalsale=0
    totalsale1=0
    totalsale2=0
    totalsale3=0
    totalsale4=0
    subtotalsale=0
    subtotalsale1=0
    subtotalsale2=0
    subtotalsale3=0
    subtotalsale4=0
    count=0
    count1=0
    count2=0
    count3=0
    count4=0
    if request.method == 'POST':
        s=request.POST['d1']
        start=str(s)
        e=request.POST['d2']
        end=str(e)
        inv = invoice_item.objects.filter(inv__due_date__range=[start,end])
        rinv = recur_itemtable.objects.filter(ri__start__range=[start,end])
        estim=EstimateItems.objects.filter(estimate__estimate_date__range=[start,end])
        sorder=sales_item.objects.filter(sale__sales_date__range=[start,end])
        vencredit=Vendor_invoice_item.objects.filter(inv__vendor_date__range=[start,end])
    for i in rinv:
        count1 +=1
        print(count)
        if i.ri.total != 'NULL' or i.ri.total != " ":
            totalsale1 += float(i.ri.total)
            
        if i.ri.sub_total != 'NULL' or i.ri.sub_total != " ":
            subtotalsale1 += float(i.ri.sub_total)
    for i in inv:
        count +=1
        if i.inv.grandtotal != 'NULL' or i.inv.grandtotal != " ":
            totalsale += float(i.inv.grandtotal)
        if i.inv.subtotal != 'NULL' or i.inv.subtotal!= " ":
            subtotalsale += float(i.inv.subtotal)
        
    for i in estim:
        count2 +=1
        if i.estimate.total != 'NULL' or i.estimate.total != " ":
            totalsale2 += float(i.estimate.total)
        if i.estimate.sub_total != 'NULL' or i.estimate.sub_total != " ":
            subtotalsale2 += float(i.estimate.sub_total)
    for i in sorder:
        count3 +=1
        if i.sale.grandtotal != 'NULL' or i.sale.grandtotal != " ":
            totalsale3 += float(i.sale.grandtotal)
        if i.sale.subtotal != 'NULL' or i.sale.subtotal!= " ":
            subtotalsale3 += float(i.sale.subtotal)
    for i in sorder:
        count3 +=1
        if i.sale.grandtotal != 'NULL' or i.sale.grandtotal != " ":
            totalsale3 += float(i.sale.grandtotal)
        if i.sale.subtotal != 'NULL' or i.sale.subtotal!= " ":
            subtotalsale3 += float(i.sale.subtotal)
    for i in vencredit:
        count4 +=1
        if i.inv.grandtotal != 'NULL' or i.inv.grandtotal != " ":
            totalsale3 += float(i.sale.grandtotal)
        if i.inv.subtotal != 'NULL' or i.inv.subtotal!= " ":
            subtotalsale3 += float(i.inv.subtotal)
    sale=totalsale
    sale1=totalsale1
    sale2=totalsale2
    sale3=totalsale3
    sale4=totalsale4
    subsale=subtotalsale
    subsale1=subtotalsale1
    subsale2=subtotalsale2
    subsale3=subtotalsale3
    subsale4=subtotalsale4
    sale='{:.2f}'.format(sale)
    sale1='{:.2f}'.format(sale1)
    sale2='{:.2f}'.format(sale2)
    sale3='{:.2f}'.format(sale3)
    sale4='{:.2f}'.format(sale4)
    subsale='{:.2f}'.format(subsale)
    subsale1='{:.2f}'.format(subsale1)
    subsale2='{:.2f}'.format(subsale2)
    subsale3='{:.2f}'.format(subsale3)
    subsale4='{:.2f}'.format(subsale4)
    context={
        'count':count,
        'count1':count1,
        'count2':count2,
        'count3':count3,
        'count4':count4,
        'end':end,
        'start':start,
        'rinv':rinv,
        'inv':inv,
        'company':company,
        'estim':estim,
        'sorder':sorder,
        'vencredit':vencredit,
        'sale':sale,
        'sale1':sale1,
        'sale2':sale2,
        'sale3':sale3,
        'sale4':sale4,
        'subsale':subsale,
        'subsale1':subsale1,
        'subsale2':subsale2,
        'subsale3':subsale3,
        'subsale4':subsale4,
    }
    return render(request, 'inventorysalecount.html', context)  

    

def product_graphview(request):
    company = company_details.objects.get(user=request.user)
    item=AddItem.objects.all()
   

    context = {
        " company": company,"item":item
    }
    return render(request,"product_graphview.html",context)
    
def product_graphview_btn(request, pk):
    
    company = company_details.objects.get(user=request.user)
    item=AddItem.objects.all()
    rec_total =recur_itemtable.objects.filter( items=pk)

    rec_totals = []
    for rec_item in rec_total:
        rec = Recurring_invoice.objects.get(recinvoiceid=rec_item.Recurring_invoice_id)
        rec_totals.append(rec)

    rec_totals_df = pd.DataFrame.from_records([rec.__dict__ for rec in rec_totals])
    rec_totals_df['date'] = pd.to_datetime(rec_totals_df['start'])
    rec_totals_df['month'] = rec_totals_df['date'].dt.month
    rec_totals_monthly_total = rec_totals_df.groupby('month')['grandtotal'].sum()

    inv_total = invoice_item.objects.filter(product=pk)

    inv_totals = []
    for inv_item in inv_total:
        inv = invoice.objects.get(invoiceid=inv_item.invoice_id)
        inv_totals.append(inv)

    inv_totals_df = pd.DataFrame.from_records([inv.__dict__ for inv in inv_totals])
    inv_totals_df['date'] = pd.to_datetime(inv_totals_df['inv_date'])
    inv_totals_df['month'] = inv_totals_df['date'].dt.month
    inv_totals_monthly_total = inv_totals_df.groupby('month')['grandtotal'].sum()
   

    rec_totals_monthly_total = rec_totals_monthly_total.reindex(range(1, 13), fill_value=0)
    inv_totals_monthly_total = inv_totals_monthly_total.reindex(range(1, 13), fill_value=0)

    total_monthly_total = (rec_totals_monthly_total + inv_totals_monthly_total).to_dict()

    print(total_monthly_total)
    context = {
        'item': item,
        'total_monthly_total':total_monthly_total,
        "company":company,
        "pk":pk
    }
    
    return render(request, "product_graphview.html", context)