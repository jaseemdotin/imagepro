from django.contrib import auth
from django.contrib.messages.api import error
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import JsonResponse, request
from .models import PlantTB, indextbanimal,indextbplant, sampletb, AnimalTB
from skimage import io
import cv2
from django.views.decorators.csrf import csrf_exempt
from .work import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from django.urls import reverse
from django.contrib.auth.models import User
from .search import imgTest
from django.core.paginator import Paginator
from .decorators import admin_only, staff_only
from PIL import Image

def Sort(sub_li):
    l = len(sub_li)
    for i in range(0, l):
        for j in range(0, l-i-1):
            if (sub_li[j][1] > sub_li[j + 1][1]):
                tempo = sub_li[j]
                sub_li[j]= sub_li[j + 1]
                sub_li[j + 1]= tempo
    return sub_li
def resultView(request):
	RESULT = []
	if request.method == "POST":
		imtype = request.POST.get('sname')
		print(imtype,123)
		try:
			image = request.FILES.get('image')
		except:
			pass
		try:
			limit = int(request.POST.get('limit'))
		except:
			limit = 10
		try:
			paths = request.POST.get('path')
		except:
			paths = None
		try:
			max = float(request.POST.get('max'))
		except Exception as e:
			max = 0.0
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
				data = sampletb.objects.create(image=image)
				data.image=image
				data.save()
			if paths:
				image_url = paths
			else:
				image_url = data.image.path
			if not limit:
				limit = 10
			src = imgTest(image_url,limit,type=imtype)
			final_result= []
			if max:
				for r,i in enumerate(src):
					d =  i.get('score')
					if d < max:
						pass
					else:
						final_result.append(i)
				src = final_result[:limit]
			# if max:
			# 	for r,i in enumerate(src):
			# 		d =  i.get('score')
			# 		if d < max:
			# 			del src[r]
			return render(request,"result.html",{"data":src,'qimage':data})
		except Exception as err:
			messages.info(request,err)
			return redirect(searchView)
	return render(request,"result.html")

def resultView1(request):
	RESULTS_ARRAY = []
	RESULT = []
	if request.method == "POST":
		image = request.FILES.get('image')
		try:
			limit = int(request.POST.get('limit'))
		except:
			limit = 10
		try:
			paths = request.POST.get('path')
		except:
			paths = None
		try:
			max = int(request.POST.get('max'))
		except:
			max = 101
		try:
			data = sampletb.objects.latest('id')
			if data.image:
				os.remove(data.image.path)
			
		except:
			data = sampletb.objects.create(image=image)
		data.image=image
		data.save()
		if paths:
			image_url = paths
		else:
			image_url = data.image.path
		try:
			imtype = request.POST.get('type')
			cd = ColorDescriptor((8, 12, 3))
			query = cv2.imread(image_url)
			features = cd.describe(query)
			if imtype=='plant':
				try:
					ind = indextbplant.objects.latest('id')
				except:
					ind = indextbplant.objects.create(image=image)
					ind.save()
			else:
				try:
					ind = indextbanimal.objects.latest('id')
				except:
					ind = indextbanimal.objects.create(image=image)
					ind.save()
			
			INDEX = ind.image.path
			searcher = Searcher(INDEX)
			if limit:
				results = searcher.search(features,limit)
			for (score, resultID) in results:
				if score<max:
					# RESULTS_ARRAY.append({"image": str(resultID), "score": str(score),"ogimg":data.image.url})
					RESULTS_ARRAY.append([str(resultID),str(score),paths])
			srt = Sort(RESULTS_ARRAY)
			for i in srt:
				if imtype=='plant':
					RESULT.append({"image": "plantdataset/"+str(i[0]), "score": str(i[1]),"ogimg":i[2]})
				else:
					RESULT.append({"image": "animaldataset/"+str(i[0]), "score": str(i[1]),"ogimg":i[2]})
				
		# if len(RESULT)==0:
		except:
			return render(request,"result.html",{"fail":"invalid image"})
		# 	#return JsonResponse([{"valid":1,"ogimg":paths}],safe=False)
		# else:
			#return JsonResponse(RESULT[:limit],safe=False)
		if len(RESULT)==0:
			return render(request,"result.html")
		else:
			return render(request,"result.html",{"data":RESULT})
		#return render(request,"result.html",{"data":RESULT[:limit]})
	return render(request,"result.html")

def homeView(request):
	return render(request,'nindex.html')

def searchView(request):
	return render(request,'search.html')

@login_required(login_url="login")
@admin_only
def userlistview(request):
	data = User.objects.filter(is_superuser=False)
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
	data.is_staff = False
	data.save()
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
		name = request.POST.get("name")
		if name=='plant':
			try:
				data = indextbplant.objects.latest('id')
			except:
				data = indextbplant.objects.create(image=file)
		else:
			try:
				data = indextbanimal.objects.latest('id')
			except:
				data = indextbanimal.objects.create(image=file)
		try:
			os.remove(data.image.path)
		except:
			pass
		data.image = file
		data.name = name
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
			name = request.POST.get("name")
			if name=='plant':
				for i in file:
					PlantTB.objects.create(image=i)
				from .index import index
				index(name)
			else:
				for i in file:
					AnimalTB.objects.create(image=i)
				from .index import index
				index(name)

			
			messages.success(request,'Training is completed' )
			return HttpResponseRedirect('')
		except Exception as e:
			messages.error(request,e)
			return HttpResponseRedirect('')
		# data =imagetb.objects.latest('id')
		# test = imagetb.objects.all()
		# for i in test:
		# 	try:
		# 		ss = i.image.name.replace('static/dataset/',"")
		# 	except:
		# 		pass
		# 	for i in file:
		# 		if ss==str(i):
		# 			dup_list.append(i.name)
		# 			file.remove(i)
		# try:
		# 	# os.remove(data.image.path)
			
		# 	for i in file:
		# 		imagetb.objects.create(image=i)
		# 	messages.success(request,f"{len(file)} item Saved")
		# 	if dup_list:
		# 		messages.error(request,f"Duplicate Images {dup_list} Not Saved")
		# 	return HttpResponseRedirect('')
		# except Exception as e:
		# 	print("error" ,e)
		# 	pass
		
	return render(request,'imageadd.html')