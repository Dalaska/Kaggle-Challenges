'''
adapted frm  https://zhuanlan.zhihu.com/p/35698470
'''
import pandas as pd
import numpy as np
from PIL import Image
import cv2

df = pd.read_csv('./dog_breed/labels.csv')
print(df.info())
print(df.head())

# 1------------------------------------------
from pandas import Series,DataFrame

breed = df['breed']
breed_np = Series.as_matrix(breed)
print(type(breed_np) )
print(breed_np.shape)   #(10222,)

#看一下一共多少不同种类
breed_set = set(breed_np)
print(len(breed_set))   #120

#构建一个编号与名称对应的字典，以后输出的数字要变成名字的时候用：
breed_120_list = list(breed_set)
dic = {}
for i in range(120):
    dic[  breed_120_list[i]   ] = i

# 2 -----------------------------------------
file =  Series.as_matrix(df["id"])
print(file.shape)

import os
file = [i+".jpg" for i in file]
file = [os.path.join("./dog_breed/train",i) for i in file ]
file_train = file[:8000]
file_test = file[8000:]
print(file_train)

np.save( "file_train.npy" ,file_train )
np.save( "file_test.npy" ,file_test )

#3 -------------
breed = Series.as_matrix(df["breed"])
print(breed.shape)
number = []
for i in range(10222):
    number.append(  dic[ breed[i] ]  )
number = np.array(number) 
number_train = number[:8000]
number_test = number[8000:]
np.save( "number_train.npy" ,number_train )
np.save( "number_test.npy" ,number_test )

# 4 ------------------------------------------
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils

normalize = transforms.Normalize(
    mean=[0.485, 0.456, 0.406],
    std=[0.229, 0.224, 0.225]
)
preprocess = transforms.Compose([
    #transforms.Scale(256),
    #transforms.CenterCrop(224),
    transforms.ToTensor(),
    normalize
])

def default_loader(path):
    img_pil =  Image.open(path)
    img_pil = img_pil.resize((224,224))
    img_tensor = preprocess(img_pil)
    return img_tensor

#当然出来的时候已经全都变成了tensor
class trainset(Dataset):
    def __init__(self, loader=default_loader):
        #定义好 image 的路径
        self.images = file_train
        self.target = number_train
        self.loader = loader

    def __getitem__(self, index):
        fn = self.images[index]
        img = self.loader(fn)
        target = self.target[index]
        return img,target

    def __len__(self):
        return len(self.images)

#5 
#file_train = ['./small/img_0.jpg','./small/img_1.jpg','./small/img_2.jpg']
#number_train = nu[1,2,3]
train_data  = trainset()
trainloader = DataLoader(train_data, batch_size=4,shuffle=True)

img, label = train_data[0]
img_np = img.numpy()
img2 = np.squeeze(img_np[0])

cv2.imshow('lines', img2)
cv2.waitKey()
cv2.destroyAllWindows()

pass