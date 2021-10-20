from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse
from .models import dataModel, imagetb, indextb, sampletb
from skimage import io
import cv2
from django.views.decorators.csrf import csrf_exempt
from .work import *

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
import json
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
def imageAddView(request):
	if request.method=="POST":
		file = request.FILES.get("file")
		name = request.POST.get("name")
		data =imagetb.objects.latest('id')
		test = imagetb.objects.all()
		for i in test:
			ss = i.image.name.replace('static/dataset/',"")
			if ss==str(file):
				messages.error(request,"Duplicate Image")
				return HttpResponseRedirect('')
			elif str(file).endswith('.png') or str(file).endswith('.jpeg') or str(file).endswith('.jpg'):
				break
			else:
				messages.error(request,"Image is not valid")
				return HttpResponseRedirect('')
		try:
			os.remove(data.image.path)
		except:
			pass
		data.image = file
		data.name = name
		data.save()
		messages.success(request,"saved")
		return HttpResponseRedirect('')
	return render(request,'imageadd.html')