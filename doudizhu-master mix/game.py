import myclass
import myutil
import time
import copy    
import DQN

def Load_Net():
    net = DQN.Net()
    return net


class Game(object):
    
    def __init__(self, model):
        #初始化一副扑克牌类
        self.cards = myclass.Cards()
        
        #play相关参数
        self.end = False
        self.last_move_type = self.last_move = "start"
        self.playround = 1
        self.i = 0
        self.yaobuqis = []
        self.cards_out = []

        #choose模型
        self.model = []
        for mod in model:
            self.model.append(mod)
        #print("length:",self.model)

        #初始化players
        self.players = []
        for i in range(1,3):
            if self.model[i-1] == 'DQN':
                self.players.append(myclass.Player(i,self.model[i-1],Load_Net()))
            else: 
                self.players.append(myclass.Player(i,self.model[i-1]))

    #发牌
    def game_start(self):
        
        #初始化扑克牌记录类
        self.playrecords = myclass.PlayRecords()    
        
        #发牌
        myutil.game_init(self.players, self.playrecords, self.cards)
    
    
    #返回扑克牌记录类
    """def get_record(self):
        web_show = WebShow(self.playrecords)
        return jsonpickle.encode(web_show, unpicklable=False)"""
        
    #游戏进行    
    def next_move(self):
        
        self.last_move_type, self.last_move, self.end, self.yaobuqi = self.players[self.i].go(self.last_move_type, self.last_move, self.playrecords, self.model,self.i)
        if self.yaobuqi:
            self.yaobuqis.append(self.i)
        else:
            self.yaobuqis = []
        #都要不起
        if len(self.yaobuqis) == 1:
            self.yaobuqis = []
            self.last_move_type = self.last_move = "start"
        if self.end:
            self.playrecords.winner = self.i+1
        self.i = self.i + 1
        #一轮结束
        if self.i > 1:
            #playrecords.show("=============Round " + str(playround) + " End=============")
            self.playround = self.playround + 1
            #playrecords.show("=============Round " + str(playround) + " Start=============")
            self.i = 0    