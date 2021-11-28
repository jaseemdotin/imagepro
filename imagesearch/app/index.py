from .models import DSmodel
def index():
    import os
    import h5py
    import numpy as np
    import argparse

    from .train import VGGNetA

    '''
    Returns a list of filenames for all jpg images in a directory.
    '''
    def get_imlist(path):
        return [os.path.join(path,f) for f in os.listdir(path) ]


    '''
    Extract features and index the images
    '''

    db = r'../imagesearch/static/DSfolder' #args["database"]
    img_list = get_imlist(db)
    feats = []
    names = []

    model = VGGNetA()
    for i, img_path in enumerate(img_list):
        norm_feat = model.extract_feat(img_path)
        img_name = os.path.split(img_path)[1]
        feats.append(norm_feat)
        names.append(img_name)
        print(i,' Images Completed')

    feats = np.array(feats)
    # print(feats)
    # directory for storing extracted features
    ps = DSmodel.objects.latest('id')
    output = ps.image.path #args["index"]
    h5f = h5py.File(output, 'w')
    h5f.create_dataset('dataset_1', data = feats)
    # h5f.create_dataset('dataset_2', data = names)
    h5f.create_dataset('dataset_2', data = np.string_(names))
    h5f.close()

    # else:
    #     db =r'../imagesearch/static/bombardierDS' #args["database"]
    #     img_list = get_imlist(db)
    #     feats = []
    #     names = []

    #     model = VGGNetA()
    #     for i, img_path in enumerate(img_list):
    #         norm_feat = model.extract_feat(img_path)
    #         img_name = os.path.split(img_path)[1]
    #         feats.append(norm_feat)
    #         names.append(img_name)
    #         print(i,' Images Completed')

    #     feats = np.array(feats)
    #     # print(feats)
    #     # directory for storing extracted features
    #     ps = BombModel.objects.latest('id')
    #     output = ps.image.path  #args["index"]
    #     h5f = h5py.File(output, 'w')
    #     h5f.create_dataset('dataset_1', data = feats)
    #     # h5f.create_dataset('dataset_2', data = names)
    #     h5f.create_dataset('dataset_2', data = np.string_(names))
    #     h5f.close()