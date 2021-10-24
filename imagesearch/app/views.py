from django.contrib import auth
from django.contrib.messages.api import error
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import JsonResponse, request
from .models import dataModel, imagetb, indextb, sampletb
from skimage import io
import cv2
from django.views.decorators.csrf import csrf_exempt
from .work import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from django.urls import reverse

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
			cd = ColorDescriptor((8, 12, 3))
			query = cv2.imread(image_url)
			features = cd.describe(query)
			ind = indextb.objects.latest('id')
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
				RESULT.append({"image": "static/dataset/"+str(i[0]), "score": str(i[1]),"ogimg":i[2]})
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

def adminlogin(request):
	try:
		next = (request.GET.get('next'))
	except:
		next = '/'
	if request.method == "POST":
		
		uname = request.POST.get('name')
		passw = request.POST.get('pass')
		user = auth.authenticate(username = uname,password = passw)
		if user is not None:
			auth.login(request,user)
			return HttpResponseRedirect(next)
	return render(request,'adminlogin.html')

def adminlogout(request):
	auth.logout(request)
	return redirect('home')

@login_required(login_url="login")
def csvAddView(request):
	if request.method=="POST":
		file = request.FILES.get("file")
		name = request.POST.get("name")
		data =indextb.objects.latest('id')
		try:
			os.remove(data.image.path)
		except:
			pass
		data.image = file
		data.name = name
		data.save()
	return render(request,'csvadd.html')
from django.contrib import messages

@login_required(login_url="login")
def imageAddView(request):
	dup_list = []
	if request.method=="POST":
		file = request.FILES.getlist("file")
		name = request.POST.get("name")
		# data =imagetb.objects.latest('id')
		test = imagetb.objects.all()
		for i in test:
			try:
				ss = i.image.name.replace('static/dataset/',"")
			except:
				pass
			for i in file:
				if ss==str(i):
					dup_list.append(i.name)
					file.remove(i)
		try:
			# os.remove(data.image.path)
			
			for i in file:
				imagetb.objects.create(image=i)
			messages.success(request,f"{len(file)} item Saved")
			if dup_list:
				messages.error(request,f"Duplicate Images {dup_list} Not Saved")
			return HttpResponseRedirect('')
		except Exception as e:
			print(e)
			pass
		
	return render(request,'imageadd.html')