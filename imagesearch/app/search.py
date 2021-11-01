from .models import indextb
def imgTest(path,limit=10,max=100):
    from .train import VGGNetA

    import numpy as np
    import h5py

    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    import argparse


    # ap = argparse.ArgumentParser()
    # ap.add_argument("-query", required = False,
    #     help = "Path to query which contains image to be queried")
    # ap.add_argument("-index", required = False,
    #     help = "Path to index")
    # ap.add_argument("-result", required = False,
    #     help = "Path for output retrieved images")
    # args = vars(ap.parse_args())


    # read in indexed images' feature vectors and corresponding image names
    hsfile = indextb.objects.latest('id')
    h5f = h5py.File(hsfile.image.path,'r')
    # feats = h5f['dataset_1'][:]
    feats = h5f['dataset_1'][:]
    #print(feats)
    imgNames = h5f['dataset_2'][:]
    #print(imgNames)
    h5f.close()
            
    # print("--------------------------------------------------")
    # print("               searching starts")
    # print("--------------------------------------------------")
        
    # read and show query image
    queryDir = path
    queryImg = mpimg.imread(queryDir)
    # plt.title("Query Image")
    # plt.imshow(queryImg)
    # plt.show()

    # init VGGNet16 model
    model = VGGNetA()

    # extract query image's feature, compute simlarity score and sort
    queryVec = model.extract_feat(queryDir)
    scores = np.dot(queryVec, feats.T)
    rank_ID = np.argsort(scores)[::-1]
    rank_score = scores[rank_ID]
    #print rank_ID
    #print rank_score

    #print ( "Rank_score : " ,rank_score )

    # number of top retrieved images to show
    maxres = limit
    imlist = [imgNames[index] for i,index in enumerate(rank_ID[0:maxres])]
    #print("top %d images in order are: " %maxres, imlist)

    # show top #maxres retrieved result one by one
    result = []
    for i,im in enumerate(imlist):
        imlist[i] = str(imlist[i]).replace('b','').replace("'",'')
        imlist[i] = 'static/dataset/' + str(imlist[i])
        result.append({'score':rank_score[i], 'image':imlist[i]}) 
        # image = mpimg.imread(r"C:\Users\jasee\OneDrive\Desktop\Projects\pro\deep\database"+"/"+str(im, 'utf-8'))
        # plt.title("search output %d" %(i+1))
        # plt.imshow(image)
        # plt.show()
    return result