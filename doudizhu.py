#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
斗地主扑克游戏 - 命令行版本
"""

import random
import sys
from typing import List, Dict, Tuple, Optional
from enum import Enum
from collections import Counter


class Suit(Enum):
    """花色枚举"""
    SPADES = "♠"    # 黑桃
    HEARTS = "♥"    # 红桃  
    DIAMONDS = "♦"  # 方块
    CLUBS = "♣"     # 梅花
    JOKER = "★"     # 王


class CardValue(Enum):
    """牌值枚举"""
    THREE = (3, "3")
    FOUR = (4, "4")
    FIVE = (5, "5")
    SIX = (6, "6")
    SEVEN = (7, "7")
    EIGHT = (8, "8")
    NINE = (9, "9")
    TEN = (10, "10")
    JACK = (11, "J")
    QUEEN = (12, "Q")
    KING = (13, "K")
    ACE = (14, "A")
    TWO = (15, "2")
    SMALL_JOKER = (16, "小王")
    BIG_JOKER = (17, "大王")

    def __init__(self, numeric_value, display):
        self.numeric_value = numeric_value
        self.display = display


class Card:
    """扑克牌类"""
    
    def __init__(self, suit: Suit, card_value: CardValue):
        self.suit = suit
        self.value = card_value
    
    def __str__(self):
        if self.value in [CardValue.SMALL_JOKER, CardValue.BIG_JOKER]:
            return f"{self.value.display}"
        return f"{self.suit.value}{self.value.display}"
    
    def __repr__(self):
        return str(self)
    
    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit and self.value == other.value
    
    def __lt__(self, other):
        if not isinstance(other, Card):
            return False
        return self.value.numeric_value < other.value.numeric_value
    
    def __hash__(self):
        return hash((self.suit, self.value))


class CardType(Enum):
    """出牌类型枚举"""
    SINGLE = "单张"
    PAIR = "对子"
    TRIPLE = "三张"
    TRIPLE_WITH_SINGLE = "三带一"
    TRIPLE_WITH_PAIR = "三带对"
    STRAIGHT = "顺子"
    PAIR_STRAIGHT = "连对"
    TRIPLE_STRAIGHT = "飞机"
    FOUR_WITH_TWO = "四带二"
    BOMB = "炸弹"
    ROCKET = "火箭"
    INVALID = "无效"


class Hand:
    """手牌组合类"""
    
    def __init__(self, cards: List[Card], card_type: CardType = CardType.INVALID):
        self.cards = sorted(cards)
        self.card_type = card_type if card_type != CardType.INVALID else self._determine_type()
        self.weight = self._calculate_weight()
    
    def _determine_type(self) -> CardType:
        """判断出牌类型"""
        if not self.cards:
            return CardType.INVALID
        
        card_count = len(self.cards)
        value_counts = Counter([card.value.numeric_value for card in self.cards])
        counts = sorted(value_counts.values(), reverse=True)
        
        # 火箭（双王）
        if (card_count == 2 and 
            set(card.value for card in self.cards) == {CardValue.SMALL_JOKER, CardValue.BIG_JOKER}):
            return CardType.ROCKET
        
        # 炸弹
        if card_count == 4 and counts == [4]:
            return CardType.BOMB
        
        # 单张
        if card_count == 1:
            return CardType.SINGLE
        
        # 对子
        if card_count == 2 and counts == [2]:
            return CardType.PAIR
        
        # 三张
        if card_count == 3 and counts == [3]:
            return CardType.TRIPLE
        
        # 三带一
        if card_count == 4 and counts == [3, 1]:
            return CardType.TRIPLE_WITH_SINGLE
        
        # 三带对
        if card_count == 5 and counts == [3, 2]:
            return CardType.TRIPLE_WITH_PAIR
        
        # 四带二
        if card_count == 6 and counts == [4, 1, 1]:
            return CardType.FOUR_WITH_TWO
        
        # 顺子（5张以上连续单牌，不包含2和王）
        if card_count >= 5 and self._is_straight():
            return CardType.STRAIGHT
        
        # 连对（3对以上连续对子，不包含2和王）
        if card_count >= 6 and card_count % 2 == 0 and self._is_pair_straight():
            return CardType.PAIR_STRAIGHT
        
        # 飞机（连续三张）
        if card_count >= 6 and self._is_triple_straight():
            return CardType.TRIPLE_STRAIGHT
        
        return CardType.INVALID
    
    def _is_straight(self) -> bool:
        """判断是否为顺子"""
        values = [card.value.numeric_value for card in self.cards]
        
        # 不能包含2和王
        if any(v >= 15 for v in values):
            return False
        
        # 检查是否连续
        values = sorted(set(values))
        if len(values) != len(self.cards):  # 有重复
            return False
        
        for i in range(1, len(values)):
            if values[i] - values[i-1] != 1:
                return False
        
        return True
    
    def _is_pair_straight(self) -> bool:
        """判断是否为连对"""
        value_counts = Counter([card.value.numeric_value for card in self.cards])
        
        # 每个值都必须出现2次
        if not all(count == 2 for count in value_counts.values()):
            return False
        
        # 不能包含2和王
        values = list(value_counts.keys())
        if any(v >= 15 for v in values):
            return False
        
        # 检查是否连续
        values = sorted(values)
        for i in range(1, len(values)):
            if values[i] - values[i-1] != 1:
                return False
        
        return True
    
    def _is_triple_straight(self) -> bool:
        """判断是否为飞机"""
        value_counts = Counter([card.value.numeric_value for card in self.cards])
        triple_values = [v for v, count in value_counts.items() if count >= 3]
        
        if len(triple_values) < 2:
            return False
        
        # 不能包含2和王
        if any(v >= 15 for v in triple_values):
            return False
        
        # 检查三张是否连续
        triple_values = sorted(triple_values)
        for i in range(1, len(triple_values)):
            if triple_values[i] - triple_values[i-1] != 1:
                return False
        
        return True
    
    def _calculate_weight(self) -> int:
        """计算牌型权重，用于比较大小"""
        if self.card_type == CardType.INVALID:
            return 0
        
        # 火箭最大
        if self.card_type == CardType.ROCKET:
            return 1000
        
        # 炸弹次之
        if self.card_type == CardType.BOMB:
            return 900 + max(card.value.numeric_value for card in self.cards)
        
        # 其他牌型按主牌值计算
        main_value = self._get_main_value()
        base_weights = {
            CardType.SINGLE: 100,
            CardType.PAIR: 200,
            CardType.TRIPLE: 300,
            CardType.TRIPLE_WITH_SINGLE: 400,
            CardType.TRIPLE_WITH_PAIR: 500,
            CardType.STRAIGHT: 600,
            CardType.PAIR_STRAIGHT: 700,
            CardType.TRIPLE_STRAIGHT: 800,
            CardType.FOUR_WITH_TWO: 850
        }
        
        return base_weights.get(self.card_type, 0) + main_value
    
    def _get_main_value(self) -> int:
        """获取主牌值（用于比较的关键值）"""
        value_counts = Counter([card.value.numeric_value for card in self.cards])
        
        if self.card_type in [CardType.TRIPLE_WITH_SINGLE, CardType.TRIPLE_WITH_PAIR, 
                             CardType.TRIPLE, CardType.TRIPLE_STRAIGHT]:
            # 三张类型以三张的值为主
            for value, count in value_counts.items():
                if count >= 3:
                    return value
        
        if self.card_type == CardType.FOUR_WITH_TWO:
            # 四带二以四张的值为主
            for value, count in value_counts.items():
                if count == 4:
                    return value
        
        # 其他类型以最大值为主
        return max(card.value.numeric_value for card in self.cards)
    
    def can_beat(self, other: 'Hand') -> bool:
        """判断是否能压过另一手牌"""
        if not other or other.card_type == CardType.INVALID:
            return True
        
        # 火箭可以压任何牌
        if self.card_type == CardType.ROCKET:
            return True
        
        # 炸弹可以压非炸弹和火箭的牌
        if self.card_type == CardType.BOMB and other.card_type not in [CardType.BOMB, CardType.ROCKET]:
            return True
        
        # 相同类型才能比较（除了炸弹和火箭）
        if self.card_type != other.card_type:
            return False
        
        # 比较权重
        return self.weight > other.weight
    
    def __str__(self):
        cards_str = " ".join(str(card) for card in self.cards)
        return f"{cards_str} ({self.card_type.value})"


class Player:
    """玩家类"""
    
    def __init__(self, name: str, is_human: bool = False):
        self.name = name
        self.is_human = is_human
        self.cards: List[Card] = []
        self.is_landlord = False
        self.is_winner = False
    
    def add_cards(self, cards: List[Card]):
        """添加手牌"""
        self.cards.extend(cards)
        self.cards.sort()
    
    def remove_cards(self, cards: List[Card]):
        """移除手牌"""
        for card in cards:
            if card in self.cards:
                self.cards.remove(card)
    
    def has_cards(self, cards: List[Card]) -> bool:
        """检查是否拥有指定的牌"""
        card_count = Counter(self.cards)
        check_count = Counter(cards)
        
        for card, count in check_count.items():
            if card_count[card] < count:
                return False
        return True
    
    def get_valid_hands(self, last_hand: Optional[Hand] = None) -> List[Hand]:
        """获取所有有效的出牌组合"""
        valid_hands = []
        
        # 如果没有上家出牌，可以出任意有效组合
        if last_hand is None or last_hand.card_type == CardType.INVALID:
            valid_hands = self._get_all_possible_hands()
        else:
            # 需要找能压过上家的牌
            all_hands = self._get_all_possible_hands()
            valid_hands = [hand for hand in all_hands if hand.can_beat(last_hand)]
        
        # 添加不出牌的选项（如果不是主动出牌）
        if last_hand is not None:
            valid_hands.append(Hand([]))  # 空手表示不出
        
        return valid_hands
    
    def _get_all_possible_hands(self) -> List[Hand]:
        """获取所有可能的出牌组合"""
        hands = []
        
        # 单张
        for card in self.cards:
            hands.append(Hand([card]))
        
        # 对子
        value_groups = {}
        for card in self.cards:
            if card.value not in value_groups:
                value_groups[card.value] = []
            value_groups[card.value].append(card)
        
        for value, cards in value_groups.items():
            if len(cards) >= 2:
                hands.append(Hand(cards[:2]))
            if len(cards) >= 3:
                hands.append(Hand(cards[:3]))
            if len(cards) == 4:
                hands.append(Hand(cards))
        
        # 复杂组合（三带一、三带对等）
        hands.extend(self._get_complex_hands(value_groups))
        
        return hands
    
    def _get_complex_hands(self, value_groups: Dict) -> List[Hand]:
        """获取复杂的牌型组合"""
        hands = []
        
        triples = [(value, cards) for value, cards in value_groups.items() if len(cards) >= 3]
        pairs = [(value, cards) for value, cards in value_groups.items() if len(cards) >= 2]
        singles = [(value, cards) for value, cards in value_groups.items() if len(cards) >= 1]
        
        # 三带一
        for triple_value, triple_cards in triples:
            for single_value, single_cards in singles:
                if triple_value != single_value:
                    hand_cards = triple_cards[:3] + single_cards[:1]
                    hands.append(Hand(hand_cards))
        
        # 三带对
        for triple_value, triple_cards in triples:
            for pair_value, pair_cards in pairs:
                if triple_value != pair_value and len(pair_cards) >= 2:
                    hand_cards = triple_cards[:3] + pair_cards[:2]
                    hands.append(Hand(hand_cards))
        
        # 顺子（简化版，只检查连续5张）
        single_values = sorted([value.numeric_value for value, cards in singles if value.numeric_value < 15])
        for i in range(len(single_values) - 4):
            if all(single_values[j] == single_values[i] + j - i for j in range(i, i + 5)):
                straight_cards = []
                for j in range(i, i + 5):
                    for value, cards in singles:
                        if value.numeric_value == single_values[j]:
                            straight_cards.append(cards[0])
                            break
                if len(straight_cards) == 5:
                    hands.append(Hand(straight_cards))
        
        return hands
    
    def choose_hand(self, valid_hands: List[Hand]) -> Hand:
        """选择要出的牌"""
        if self.is_human:
            return self._human_choose_hand(valid_hands)
        else:
            return self._ai_choose_hand(valid_hands)
    
    def _human_choose_hand(self, valid_hands: List[Hand]) -> Hand:
        """人类玩家选择出牌"""
        print(f"\n{self.name}的手牌：")
        print(" ".join(f"{i+1}.{card}" for i, card in enumerate(self.cards)))
        
        print(f"\n可选择的出牌方案：")
        for i, hand in enumerate(valid_hands):
            if not hand.cards:
                print(f"{i+1}. 不出")
            else:
                print(f"{i+1}. {hand}")
        
        while True:
            try:
                choice = input(f"\n请选择出牌方案 (1-{len(valid_hands)}): ").strip()
                if choice:
                    idx = int(choice) - 1
                    if 0 <= idx < len(valid_hands):
                        return valid_hands[idx]
                print("输入无效，请重新选择")
            except (ValueError, IndexError):
                print("输入无效，请重新选择")
    
    def _ai_choose_hand(self, valid_hands: List[Hand]) -> Hand:
        """AI玩家选择出牌"""
        if not valid_hands:
            return Hand([])
        
        # 简单AI策略：
        # 1. 如果可以出完所有牌，直接出
        # 2. 否则出最小的能出的牌
        
        # 检查是否能一次出完
        for hand in valid_hands:
            if len(hand.cards) == len(self.cards):
                return hand
        
        # 排除不出牌的选项
        play_hands = [hand for hand in valid_hands if hand.cards]
        
        if not play_hands:
            return Hand([])  # 不出
        
        # 选择最小的牌
        return min(play_hands, key=lambda h: (len(h.cards), h.weight))
    
    def __str__(self):
        role = "地主" if self.is_landlord else "农民"
        return f"{self.name}({role})"


class Game:
    """斗地主游戏主类"""
    
    def __init__(self):
        self.players: List[Player] = []
        self.deck: List[Card] = []
        self.landlord_cards: List[Card] = []  # 地主牌
        self.current_player_idx = 0
        self.last_hand: Optional[Hand] = None
        self.last_player_idx = -1
        self.game_over = False
        self.winner: Optional[Player] = None
    
    def create_deck(self):
        """创建一副牌"""
        self.deck = []
        
        # 普通牌：每种花色A到K各一张，3到2各一张
        for suit in [Suit.SPADES, Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS]:
            for value in [CardValue.THREE, CardValue.FOUR, CardValue.FIVE, 
                         CardValue.SIX, CardValue.SEVEN, CardValue.EIGHT, 
                         CardValue.NINE, CardValue.TEN, CardValue.JACK, 
                         CardValue.QUEEN, CardValue.KING, CardValue.ACE, CardValue.TWO]:
                self.deck.append(Card(suit, value))
        
        # 大小王
        self.deck.append(Card(Suit.JOKER, CardValue.SMALL_JOKER))
        self.deck.append(Card(Suit.JOKER, CardValue.BIG_JOKER))
        
        random.shuffle(self.deck)
    
    def deal_cards(self):
        """发牌"""
        # 每人17张牌
        for i in range(17):
            for player in self.players:
                player.add_cards([self.deck.pop()])
        
        # 剩余3张作为地主牌
        self.landlord_cards = self.deck[:3]
        self.deck = self.deck[3:]
    
    def choose_landlord(self) -> Player:
        """选择地主"""
        print("\n=== 叫地主阶段 ===")
        
        # 简化版：随机选择地主
        landlord = random.choice(self.players)
        landlord.is_landlord = True
        landlord.add_cards(self.landlord_cards)
        
        print(f"{landlord.name} 成为了地主！")
        print(f"地主牌：{' '.join(str(card) for card in self.landlord_cards)}")
        
        # 地主先出牌
        self.current_player_idx = self.players.index(landlord)
        
        return landlord
    
    def play_round(self):
        """进行一轮游戏"""
        current_player = self.players[self.current_player_idx]
        
        print(f"\n=== {current_player.name} 的回合 ===")
        print(f"手牌数量：{len(current_player.cards)}")
        
        # 获取有效出牌
        valid_hands = current_player.get_valid_hands(self.last_hand)
        
        if not valid_hands:
            print(f"{current_player.name} 无法出牌")
            self._next_player()
            return
        
        # 玩家选择出牌
        chosen_hand = current_player.choose_hand(valid_hands)
        
        if not chosen_hand.cards:
            print(f"{current_player.name} 选择不出")
        else:
            print(f"{current_player.name} 出牌：{chosen_hand}")
            current_player.remove_cards(chosen_hand.cards)
            self.last_hand = chosen_hand
            self.last_player_idx = self.current_player_idx
            
            # 检查是否获胜
            if len(current_player.cards) == 0:
                self.game_over = True
                self.winner = current_player
                return
        
        self._next_player()
        
        # 如果一圈都没人出牌，重新开始
        if self.current_player_idx == self.last_player_idx:
            print("\n一圈都没人出牌，重新开始出牌")
            self.last_hand = None
            self.last_player_idx = -1
    
    def _next_player(self):
        """切换到下一个玩家"""
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
    
    def print_game_state(self):
        """显示游戏状态"""
        print("\n" + "="*50)
        print("当前游戏状态：")
        for player in self.players:
            role = "地主" if player.is_landlord else "农民"
            print(f"{player.name}({role})：{len(player.cards)}张牌")
        
        if self.last_hand and self.last_hand.cards:
            last_player = self.players[self.last_player_idx]
            print(f"上次出牌：{last_player.name} - {self.last_hand}")
        else:
            print("上次出牌：无")
        print("="*50)
    
    def check_winner(self):
        """检查游戏是否结束"""
        for player in self.players:
            if len(player.cards) == 0:
                self.game_over = True
                self.winner = player
                break
    
    def play(self):
        """开始游戏"""
        print("欢迎来到斗地主游戏！")
        
        # 创建玩家
        self.players = [
            Player("玩家", is_human=True),
            Player("电脑1", is_human=False),
            Player("电脑2", is_human=False)
        ]
        
        # 创建并发牌
        self.create_deck()
        self.deal_cards()
        
        # 选择地主
        self.choose_landlord()
        
        # 游戏主循环
        round_count = 0
        while not self.game_over and round_count < 1000:  # 防止无限循环
            self.print_game_state()
            self.play_round()
            round_count += 1
        
        # 游戏结束
        if self.winner:
            if self.winner.is_landlord:
                print(f"\n🎉 游戏结束！地主 {self.winner.name} 获胜！")
            else:
                print(f"\n🎉 游戏结束！农民获胜！{self.winner.name} 最先出完牌！")
        else:
            print("\n游戏异常结束")


def main():
    """主函数"""
    try:
        game = Game()
        game.play()
    except KeyboardInterrupt:
        print("\n\n游戏被中断，谢谢游玩！")
    except Exception as e:
        print(f"\n游戏出现错误：{e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()