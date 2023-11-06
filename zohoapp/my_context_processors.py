from .models import *
from django.shortcuts import render,redirect,get_object_or_404

def base_setting(request):
    if setting_list.objects.filter(user=request.user.id).exists():
        return{
        "setting_variable":setting_list.objects.get(user=request.user.id),
      }
    else:
        return{
        "setting_variable":"null",
      }
def get_company_name(request):
  if company_details.objects.filter(user=request.user.id).exists():
      return{
        "company":company_details.objects.get(user=request.user.id),
      }
  else:
    return{
      "company":"No company name",
    }
