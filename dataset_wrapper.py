# -*- coding: utf-8 -*-
"""dataset_wrapper.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kmNE1NIutSdTKTYE7nELvQxGhkZ9T4WN
"""

import os
import torch
import torch.utils.data as utils_data

from PIL import Image, ImageOps
import skimage

#https://pytorch.org/tutorials/beginner/data_loading_tutorial.html
class Create_Dataset(utils_data.Dataset):

    def __init__(self, images_dir, masks_dir, transform=None, test = False):

        self.images_dir = images_dir
        self.masks_dir = masks_dir
        self.transform = transform
        self.images_titles = sorted(os.listdir(self.images_dir))
        self.masks_titles = sorted(os.listdir(self.masks_dir))
        self.test = test
        
    def __len__(self):
        return len(self.images_titles)
    
    def __getitem__(self, idx):

        images = skimage.io.imread(os.path.join(self.images_dir, self.images_titles[idx]))[:,:,:3]
        images = Image.fromarray((images / images.max()* 255).astype(np.uint8))
        images = images.resize((512,512),Image.ANTIALIAS)
        seed = random.randint(100)
        torch.manual_seed(seed)
        images = self.transform(images)

        if self.test:
          return images
        
        masks = skimage.io.imread(os.path.join(self.masks_dir, self.masks_titles[idx]))[:,:,:3]
        masks = Image.fromarray((masks / masks.max()* 255).astype(np.uint8))
        masks = masks.resize((512,512),Image.ANTIALIAS)
        masks = ImageOps.invert(masks)
        torch.manual_seed(seed)

        masks = self.transform(masks)
        masks[0,:,:] += masks[1,:,:] + masks[2,:,:]
        masks[masks > 0] = 1

        return images, masks
