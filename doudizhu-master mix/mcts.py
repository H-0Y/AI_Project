#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import math
import random
import numpy as np
import game
import myclass
import copy
from get_bestchild import get_bestchild_, get_bestchild


class State(object):
    def __init__(self, my_id, my_card, next_card, winner, action, cards_type, move_nums, last_move_type, next_moves, next_move_types):
        self.my_id = my_id  # 当前state序号
        self.my_card = my_card  # 手牌
        self.enemy_cards = next_card  # 对手的牌
        self.winner = winner  # 是否出完
        self.action = action  # 出的牌
        self.cards_type = cards_type  # 出的牌的类型
        self.move_nums = move_nums  # 判断是否all_expand
        self.last_move_type = last_move_type
        self.untried_actions = []  #
        self.untried_action_types = []
        self.next_moves = next_moves
        self.next_move_types = next_move_types

    def init_untried_actions(self, move):
        self.untried_actions.append(move)

    def init_untried_action_types(self, types):
        self.untried_action_types.append(types)

    def compute_reward(self, my_id):
        if my_id == 0:
            if self.winner == my_id:
                return 1
            else:
                return 0
        else:
            if self.winner != 0:
                return 1
            else:
                return 0

    def get_next_state_with_random_choice(self, untried_move, untried_move_type):

        random_move = untried_move
        random_move_type = untried_move_type
        """for move in random_move:
          print("move:", move.name)"""
        """for card in self.my_card:
          print("mycard:",card.name)"""
        # print("type",random_move_type)
        if random_move_type not in ["yaobuqi", "buyao"]:
            enemy_cards = []
            my_card = []
            for card in self.my_card:
                enemy_cards.append(card)
            for card in self.enemy_cards:
                my_card.append(card)
            """for card in enemy_cards:
            print("enemycard:", card.name)"""
            """print(random_move)
          print(enemy_cards)"""
            for card in random_move:
                enemy_cards.remove(card)

        next_id = (self.my_id + 1) % 2

        winner = self.my_id
        if len(enemy_cards) != 0:
            winner = -1

        if random_move_type in ["yaobuqi", "buyao"]:
            last_move_type = "start"
            last_move = []
        else:
            last_move_type = random_move_type
            last_move = random_move
        total_moves = myclass.Moves()
        total_moves.get_moves(my_card)
        next_move_types, next_moves = total_moves.get_next_moves(
            last_move_type, last_move)
        move_nums = len(next_moves)
        if move_nums == 0:
            move_nums = 1
            next_move_types = "start"
            next_moves = []
            # print("???????????")
        # print("move_type:",next_move_types)
        # print("movenumsss:",move_nums)
        next_state = State(next_id, my_card, enemy_cards, winner, last_move,
                           last_move_type, move_nums, last_move_type, next_moves, next_move_types)
        return next_state

    def get_next_state_with_random_choice_in_simulation(self):
        if len(self.next_moves) == 0:
            random_move = []
            random_move_type = "yaobuqi"
        else:
            if self.last_move_type == "start":
                r_max = len(self.next_moves)
            else:
                r_max = len(self.next_moves) + 1
            r = np.random.randint(0, r_max)
            if r == len(self.next_moves):
                random_move = []
                random_move_type = "buyao"
            else:
                random_move = self.next_moves[r]
                random_move_type = self.next_move_types[r]

        if random_move_type not in ["yaobuqi", "buyao"]:
            for move in random_move:
                self.my_card.remove(move)
        next_id = (self.my_id + 1) % 2
        enemy_cards = self.my_card
        my_card = self.enemy_cards

        winner = self.my_id
        if len(self.my_card) != 0:
            winner = -1
        if random_move_type in ["yaobuqi", "buyao"]:
            last_move_type = "start"
            last_move = []
        else:
            last_move_type = random_move_type
            last_move = random_move
        total_moves = myclass.Moves()
        total_moves.get_moves(my_card)
        next_move_types, next_moves = total_moves.get_next_moves(
            last_move_type, last_move)
        move_nums = len(next_move_types)
        next_state = State(next_id, my_card, enemy_cards, winner, None,
                           None, move_nums, last_move_type, next_moves, next_move_types)
        return next_state


class Node(object):

    def __init__(self, parent, state):
        self.parent = parent
        self.state = state
        self.children = []

        self.reward = 0
        self.visit = 0

    def get_state(self):
        return self.state

    def get_parent(self):
        return self.parent

    def get_children(self):
        return self.children

    def is_all_expand(self):
        if len(self.children) < self.state.move_nums:
            return False
        return True

    def add_child(self, sub_node):
        self.children.append(sub_node)

    def set_state(self, state):
        self.state = state

    def expand(self, next_moves, next_move_types):
        if len(next_moves) != 0:
            valid_moves = next_moves
            move_nums = len(valid_moves)
            # print("move_num:",move_nums)
            i = np.random.choice(move_nums)
            untried_move = next_moves[i]
            untried_move_type = next_move_types[i]
            # print("cardofmyself:",len(self.state.my_card))
            new_state = self.state.get_next_state_with_random_choice(
                untried_move, untried_move_type)
            # print("nextmoves:",next_moves)
            sub_node = Node(self, new_state)
            self.add_child(sub_node)
            """for move in sub_node.state.action:
          print("randommove:", move.name)
      print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
      for cards in sub_node.state.next_moves:
          for card in cards:
            print("allmoves:", card.name)
      print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")"""
            return sub_node
        else:
            total_moves = myclass.Moves()
            total_moves.get_moves(self.state.enemy_cards)
            next_move_types, next_moves = total_moves.get_next_moves(
                "start", [])
            move_nums = len(next_move_types)
            # print("movenum222222222:",move_nums)
            new_state = State((self.state.my_id + 1) % 2, self.state.enemy_cards,
                              self.state.my_card, -1, [], "buyao", move_nums, "buyao", next_moves, next_move_types)
            sub_node = Node(self, new_state)
            self.add_child(sub_node)
            return sub_node


def tree_policy(node, my_id):
    #count = 0
    while node.state.winner == -1:
        if node.is_all_expand():
            #print("node info:",node.state.move_nums)

            node = get_bestchild(node, my_id)

        else:
            sub_node = node.expand(node.state.next_moves,
                                   node.state.next_move_types)
            return sub_node
    return node


def tree_policy2(node, my_id):
    #count = 0
    if node.state.winner == -1:
        if node.is_all_expand():
            #print("node info:",node.state.move_nums)

            node = get_bestchild(node, my_id)

        else:
            sub_node = node.expand(node.state.next_moves,
                                   node.state.next_move_types)
            return sub_node
    return node


def default_policy(node, my_id):

    #print("len: ",len(node.state.my_card))
    current_state = copy.deepcopy(node.state)
    #  随机出牌直到游戏结束
    while current_state.winner == -1:
        # print(current_state.winner)
        """for card in current_state.my_card:
          print("current_state_card:", card.name)
        print("currentchupai:",current_state.cards_type)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~") """
        # print(current_state.winner)
        current_state = current_state.get_next_state_with_random_choice_in_simulation()
    # print(current_state.winner)
    #print("len: ",len(node.state.my_card))
    final_state_reward = current_state.compute_reward(my_id)
    return final_state_reward


def backup(node, reward):

    while node is not None:
        node.visit += 1
        node.reward += reward
        node = node.parent


class MCTSModel(myclass.Cards, myclass.Player, game.Game, myclass.PlayRecords):
    def __init__(self):
        super(MCTSModel, self).__init__()
        root = Node(None, None)
        self.current_node = root

    def choose_with_mcts(self,
                         next_moves,
                         next_move_types,
                         last_move_type,
                         my_cards,
                         enemy_cards,
                         player_id):
        if len(next_moves) == 1:
            return next_move_types[0], next_moves[0]
        else:
            root = Node(None, None)
            self.current_node = root
            # print("last_type:",last_move_type)
            """for child in self.current_node.get_children():
          if self.compare(child.state.action,last_move):
            self.current_node = child"""
            my_id = player_id
            # print("id",my_id)
            state_ = State(my_id, my_cards, enemy_cards,  -1, None, None,
                           len(next_moves), last_move_type, next_moves, next_move_types)
            # print("len:",len(next_moves))
            self.current_node.set_state(state_)
            #count = 0
            computation_budget = 500
            for _ in range(computation_budget):
                # print("count:",count)
                """for card in self.current_node.state.my_card:
                  print("my_card_:", card.name)
                for card in self.current_node.state.enemy_cards:
                  print("enemy_card_:", card.name)"""
                # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`")
                # if the children of current node are not all_expanded,
                # then expand a new node
                # otherwise select its best child to be new checked node
                expand_node = tree_policy(self.current_node, my_id)
                # simulate the game til the end
                # and return the reward based on the game result
                reward = default_policy(expand_node, my_id)
                # backup the reward till the root
                backup(expand_node, reward)

                # print("done")
                # count+=1
            # print("here!!!!!!!!!!!!!!")
            # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            # print("parent:",self.current_node.parent)
            self.current_node = root

            best_next_node = get_bestchild_(self.current_node)
            # print("parent:",best_next_node.parent)
            new_move = best_next_node.get_state().action
            new_move_type = best_next_node.get_state().cards_type
            # print("parent:",best_next_node.parent)
            """print("children:",best_next_node.children)
        for moves in best_next_node.state.next_moves:
          for card in moves:
            print("all_moves:",card.name)
        for move in new_move:
          print("move!!!!!!!!!!!!!!!!!!!!!!!:",move.name,move.color)"""
            return new_move_type, new_move

    def choose_with_mcts_old(self, next_moves, next_move_types, last_move_type, my_cards, enemy_cards, player_id):
        if len(next_moves) == 1:
            return next_move_types[0], next_moves[0]
        else:
            root = Node(None, None)
            self.current_node = root
            # print("last_type:",last_move_type)
            """for child in self.current_node.get_children():
          if self.compare(child.state.action,last_move):
            self.current_node = child"""
            my_id = player_id
            # print("id",my_id)
            state_ = State(my_id, my_cards, enemy_cards,  -1, None, None,
                           len(next_moves), last_move_type, next_moves, next_move_types)
            # print("len:",len(next_moves))
            self.current_node.set_state(state_)
            #count = 0
            computation_budget = 500
            for _ in range(computation_budget):
                # print("count:",count)
                """for card in self.current_node.state.my_card:
                  print("my_card_:", card.name)
                for card in self.current_node.state.enemy_cards:
                  print("enemy_card_:", card.name)"""
                # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`")
                # if the children of current node are not all_expanded,
                # then expand a new node
                # otherwise select its best child to be new checked node
                expand_node = tree_policy2(self.current_node, my_id)
                # simulate the game til the end
                # and return the reward based on the game result
                reward = default_policy(expand_node, my_id)
                # backup the reward till the root
                backup(expand_node, reward)

                # print("done")
                # count+=1
            # print("here!!!!!!!!!!!!!!")
            # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            # print("parent:",self.current_node.parent)
            self.current_node = root

            best_next_node = get_bestchild_(self.current_node)
            # print("parent:",best_next_node.parent)
            new_move = best_next_node.get_state().action
            new_move_type = best_next_node.get_state().cards_type
            # print("parent:",best_next_node.parent)
            """print("children:",best_next_node.children)
        for moves in best_next_node.state.next_moves:
          for card in moves:
            print("all_moves:",card.name)
        for move in new_move:
          print("move!!!!!!!!!!!!!!!!!!!!!!!:",move.name,move.color)"""
            return new_move_type, new_move
