from django.shortcuts import render
from django.http import JsonResponse
from .models import sampletb
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

@csrf_exempt
def resultView(request):
	RESULTS_ARRAY = []
	RESULT = []
	if request.method == "POST":
		image = request.FILES.get('image')
		try:
			limit = int(request.POST.get('limit'))
		except:
			limit = 1000
		try:
			min = int(request.POST.get('min'))
		except:
			min = 0
		try:
			max = int(request.POST.get('max'))
		except:
			max = 100
		
		
		print(limit,min,max)
		try:
			data = sampletb.objects.latest('id')
		except:
			data = sampletb.objects.create(image=image)
		data.image=image
		data.save()
		image_url = data.image.path
		cd = ColorDescriptor((8, 12, 3))
		query = cv2.imread(image_url)
		features = cd.describe(query)
		INDEX = r"./app/index.csv"
		searcher = Searcher(INDEX)
		results = searcher.search(features)
		for (score, resultID) in results:
			if score<max and score>min:
				# RESULTS_ARRAY.append({"image": str(resultID), "score": str(score),"ogimg":data.image.url})
				RESULTS_ARRAY.append([str(resultID),str(score),data.image.url])
		srt = Sort(RESULTS_ARRAY)
		for i in srt:
			RESULT.append({"image": str(i[0]), "score": str(i[1]),"ogimg":i[2]})
		if len(RESULT)==0:
			return JsonResponse([{"valid":1,"ogimg":data.image.url}],safe=False)
		else:
			return JsonResponse(RESULT[:limit],safe=False)
	return JsonResponse([1],safe=False)

def homeView(request):
	return render(request,'home.html')