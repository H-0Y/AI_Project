import sys
import math
import random
import numpy as np
#import myutil
#import myclass
#import main_ddz
from copy import copy
from collections import Counter
#from get_bestchild import get_bestchild_,get_bestchild

TOTAL_Cards_types = ['1-a-12', '1-b-12','1-c-12','1-d-12',
                           '2-a-13', '2-b-13','2-c-13','2-d-13',
                           '3-a-1', '3-b-1','3-c-1','3-d-1',
                           '4-a-2', '4-b-2','4-c-2','4-d-2',
                           '5-a-3', '5-b-3','5-c-3','5-d-3',
                           '6-a-4', '6-b-4','6-c-4','6-d-4',
                           '7-a-5', '7-b-5','7-c-5','7-d-5',
                           '8-a-6', '8-b-6','8-c-6','8-d-6',
                           '9-a-7', '9-b-7','9-c-7','9-d-7',
                           '10-a-8', '10-b-8','10-c-8','10-d-8',
                           '11-a-9', '11-b-9','11-c-9','11-d-9',
                           '12-a-10', '12-b-10','12-c-10','12-d-10',
                           '13-a-11', '13-b-11','13-c-11','13-d-11',
                           '14-a-14', '15-a-15']



def get_table_of_cards(cards):
    cardtable = [0]*15
    for card in cards:
        card_name = int(card.name)-1
        cardtable[card_name] += 1
    return cardtable

import torch
import matplotlib.pyplot as plt
from torch.autograd import Variable

class Net():
    def __init__(self):
        # 搭建网络
        try:
            self.load_model("stupid_model_plus_4.pkl")
            print("Load net")
        except (FileNotFoundError):            
            print("Build net")          
            self.net = torch.nn.Sequential(
                torch.nn.Linear(46, 250),
                torch.nn.ReLU(),
                torch.nn.Linear(250, 50),
                torch.nn.ReLU(),
                torch.nn.Linear(50, 1)
            )

    def train(self,input,output):
        # 训练网络
        #print('train start')
        x = Variable(torch.tensor(input)).float()
        y = Variable(torch.tensor(output)).float()
        y = y.view(-1,1)
        #print(x)
        #print(y)
        # 设置优化器
        optimizer = torch.optim.SGD(self.net.parameters(), lr=0.001)
        loss_func = torch.nn.MSELoss()

        # 训练
        for i in range(100):
            out = self.net(x)
            loss = loss_func(out, y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            #plt.scatter(i, loss.data.numpy(),marker='.')
            #print(loss.data.numpy())
        #plt.show()   
        #print('train end')
    
    def get_value_only(self,input):
        x = Variable(torch.tensor(input)).float()
        #print(x)
        out = self.net(x)
        #print(out)
        return out
    
    def save_model(self):
        torch.save(self.net, "stupid_model_plus_4.pkl")
        print("model saved")
    
    def load_model(self,path):
        self.net = torch.load(path)


#print(get_table_of_cards(TOTAL_Cards_types))



         








        
            


