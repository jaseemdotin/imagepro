from django.contrib import auth
from django.contrib.messages.api import error
from django.http import response
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import JsonResponse, request
from django.urls.base import resolve
from .models import ImageTB, DSmodel, sampletb
from skimage import io
import cv2
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from django.urls import reverse
from django.contrib.auth.models import User
from .search import imgTest
from django.core.paginator import Paginator
from .decorators import admin_only, staff_only
from PIL import Image

dataDIC = None


def Sort(sub_li):
    l = len(sub_li)
    for i in range(0, l):
        for j in range(0, l-i-1):
            if (sub_li[j][1] > sub_li[j + 1][1]):
                tempo = sub_li[j]
                sub_li[j]= sub_li[j + 1]
                sub_li[j + 1]= tempo
    return sub_li
	

def homeView(request):
	return render(request,'nindex.html')

def searchView(request):
	return render(request,'imgsearchnew.html')

@login_required(login_url="login")
@admin_only
def userlistview(request):
	data = User.objects.filter()
	paginator = Paginator(data, 15) # Show 25 contacts per page.
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request,'userlist.html',{'page_obj':page_obj})

@login_required(login_url="login")
@admin_only
def activateUserView(request, id):
	data = User.objects.get(id=id)
	data.is_staff = True
	data.save()
	return redirect(userlistview)

@login_required(login_url="login")
@admin_only
def deactivateUserView(request, id):
	data = User.objects.get(id=id)
	data.delete()
	return redirect(userlistview)

def AdminRegister(request):
	if request.method == "POST":
		uname = request.POST.get('name')
		passw = request.POST.get('pass')
		email = request.POST.get('email')
		empid = request.POST.get('empid')
		try:
			User.objects.create_user(username=uname,password=passw,email=email,first_name=empid)
			return redirect('login')
		except Exception as e:
			messages.error(request,e)
			return HttpResponseRedirect('')
	return render(request,'register.html')

def adminlogin(request):
	if request.method == "POST":
		next = (request.GET.get('next'))
		uname = request.POST.get('name')
		passw = request.POST.get('pass')
		user = auth.authenticate(username = uname,password = passw)
		if user is not None:
			auth.login(request,user)
			if next:
				return HttpResponseRedirect(next)
			else:
				return redirect('home')
		else:
			messages.error(request,'Incorrect Username or password')
	return render(request,'adminlogin.html')

def adminlogout(request):
	auth.logout(request)
	return redirect('home')

@login_required(login_url="login")
@staff_only
def csvAddView(request):
	if request.method=="POST":
		file = request.FILES.get("file")
		try:
			data = DSmodel.objects.latest('id')
		except:
			data = DSmodel.objects.create(image=file)
		try:
			os.remove(data.image.path)
		except:
			pass
		data.image = file
		data.name = 'model'
		data.save()
		messages.info(request,'Model Added Succesfully')
		return HttpResponseRedirect('')
	return render(request,'csvadd.html')

from django.contrib import messages

@login_required(login_url="login")
@staff_only
def imageAddView(request):
	dup_list = []
	if request.method=="POST":
		try:
			file = request.FILES.getlist("file")
			for i in file:
				ImageTB.objects.create(image=i)
			from .index import index
			index()
			messages.success(request,'Training is completed' )
			return HttpResponseRedirect('')
		except Exception as e:
			messages.error(request,e)
			return HttpResponseRedirect('')
		
	return render(request,'imageadd.html')

def samplesearch(request):
	RESULT = []
	global dataDIC
	try:
		if request.method == 'GET':
			val = sampletb.objects.latest('id')
			paginator = Paginator(dataDIC, 10) # Show 25 contacts per page.
			page_number = request.GET.get('page')
			if not page_number:
				dataDIC = None
				return render(request,'imagesample.html')
			page_obj = paginator.get_page(page_number)
			response = {"page_obj":page_obj,'qimage':val}
			return render(request,'newres.html', response)
	except:
		return render(request,'imagesample.html')
	if request.method == "POST":
		dataDIC = None
		try:
			image = request.FILES.get('image')
		except:
			pass
		try:
			limit = int(request.POST.get('limit'))
		except:
			limit = False
		try:
			paths = request.POST.get('path')
		except:
			paths = None
		try:
			max = float(request.POST.get('max'))
		except Exception as e:
			max = 0.0
		try:
			x = int(float(request.POST.get('fx')))
			y = int(float(request.POST.get('fy')))
			w = int(float(request.POST.get('fw')))
			h = int(float(request.POST.get('fh')))
		except Exception as e:
			print('error', e)
		try:
			data = sampletb.objects.latest('id')
			if paths:
				img1 = Image.open(paths)
				img1copy = img1.copy()
				imgname= data.image.name
				img2 = Image.open(data.image.path)
				width, height = img1copy.size
				newsize = (width, height)
				img2 = img2.resize(newsize)
				img2.paste(img1copy,(0,0))
				img2.save(imgname)
			else:
				data = sampletb.objects.latest('id')
				data.image = image
				data.save()
				
			if paths:
				image_url = paths
			else:
				image_url = data.image.path
			src = imgTest(image_url,limit)
			image = Image.open(data.image)
			cropped_image = image.crop((x, y, w + x, h + y))
			resized_image = cropped_image.resize((w, h))
			resized_image.save(data.image.path)
			final_result= []
			if max:
				for r,i in enumerate(src):
					d =  i.get('score')
					if float(d) < max:
						pass
					else:
						final_result.append(i)
				src = final_result
			if limit:
				src = src[:limit]
			else:
				src = src
			paginator = Paginator(src, 10) # Show 25 contacts per page.
			page_number = request.GET.get('page')
			page_obj = paginator.get_page(page_number)
			dataDIC = src
			# return render(request,"result.html",{"data":src,'qimage':data})
			data = sampletb.objects.latest('id')
			response = {"page_obj":page_obj,'qimage':data}
			dataDIC = src
			return render(request,'newres.html', response)
		except Exception as err:
			response = [{"error":err}]
			messages.info(request,err)
			print(err,'error')
			return HttpResponse('not working')
			# return redirect(searchView)
	return render(request,'imagesample.html')

@login_required(login_url="login")
@admin_only
def editUserView(request, id):
	try:
		user = User.objects.get(id = id)
		if request.method == 'POST':
			uname = request.POST.get('username')
			email = request.POST.get('email')
			fname = request.POST.get('first_name')
			user.username=uname
			user.email=email
			user.first_name=fname
			user.save()
			return redirect(userlistview)
			# User.objects.create_user()
		return render(request, 'edituser.html',{'data':user})
	except:
		return redirect(userlistview)

@login_required(login_url="login")
@admin_only
def superUserView(request, id):
	user = User.objects.get(id = id)
	user.is_superuser = True
	user.save()
	return redirect(userlistview)
	