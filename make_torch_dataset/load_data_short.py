from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
from PIL import Image
import cv2 

normalize = transforms.Normalize(
    mean=[0.485, 0.456, 0.406],
    std=[0.229, 0.224, 0.225]
)
preprocess = transforms.Compose([
    #transforms.Scale(256),
    #transforms.CenterCrop(224),
    transforms.ToTensor(),
    #normalize
])

def default_loader(path):
    img_pil =  Image.open(path).convert('LA')
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
file_train = ['./dog_breed/small/img_0.jpg','./dog_breed/small/img_1.jpg','./dog_breed/small/img_2.jpg']
number_train = [1,2,3]
train_data  = trainset()
img, label = train_data[0]
#trainloader = DataLoader(train_data, batch_size=4,shuffle=True)
img_np = img.numpy()

cv2.imshow('lines', img_np)
cv2.waitKey()
cv2.destroyAllWindows()

pass