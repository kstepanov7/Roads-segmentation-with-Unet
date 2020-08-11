# -*- coding: utf-8 -*-
"""Unet.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18rpbQLQyMe3uH1QuiXK2NGosng6rDCV5
"""

import torch
import torch.nn as nn


class DoubleConv_layer(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(DoubleConv_layer, self).__init__()

        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1)
        self.batch1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1)
        self.batch2 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU()

    def forward(self, input):

        output = self.conv1(input)
        output = self.batch1(output)
        output = self.relu(output)

        output = self.conv2(output)
        output = self.batch2(output)
        output = self.relu(output)

        return output

class UNet(nn.Module):

    def __init__(self):
        super(UNet, self).__init__()
                
        self.down1 = DoubleConv_layer(3, 64)
        self.down2 = DoubleConv_layer(64, 128)
        self.down3 = DoubleConv_layer(128, 256)
        self.down4 = DoubleConv_layer(256, 512)        

        self.maxpool = nn.MaxPool2d(2)

        self.middle = DoubleConv_layer(512, 1024) 

        self.ConvT1 = nn.ConvTranspose2d(1024, 1024, 2, 2)
        self.ConvT2 = nn.ConvTranspose2d(512, 512, 2, 2)
        self.ConvT3 = nn.ConvTranspose2d(256, 256, 2, 2)
        self.ConvT4 = nn.ConvTranspose2d(128, 128, 2, 2)

        self.up1 = DoubleConv_layer(1536, 512)
        self.up2 = DoubleConv_layer(768, 256)
        self.up3 = DoubleConv_layer(384, 128)
        self.up4 = DoubleConv_layer(192, 64)
        
        self.conv_last = nn.Conv2d(64, 1, 1)

    def forward(self, input):

        conv1 = self.down1(input)
        output = self.maxpool(conv1)

        conv2 = self.down2(output)
        output = self.maxpool(conv2)
        
        conv3 = self.down3(output)
        output = self.maxpool(conv3)   

        conv4 = self.down4(output)
        output = self.maxpool(conv4)   

        output = self.middle(output)

        output = self.ConvT1(output)        
        output = torch.cat([output, conv4], dim=1)
        output = self.up1(output)

        output = self.ConvT2(output)        
        output = torch.cat([output, conv3], dim=1)       
        output = self.up2(output)

        output = self.ConvT3(output)  
        output = torch.cat([output, conv2], dim=1)   
        output = self.up3(output)

        output = self.ConvT4(output)     
        output = torch.cat([output, conv1], dim=1)   
        output = self.up4(output)

        output = self.conv_last(output)
        
        return output