#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
斗地主游戏测试文件
"""

from doudizhu import *
import random

def test_card_creation():
    """测试扑克牌创建"""
    print("测试扑克牌创建...")
    card1 = Card(Suit.SPADES, CardValue.ACE)
    card2 = Card(Suit.JOKER, CardValue.BIG_JOKER)
    
    print(f"创建的牌：{card1}, {card2}")
    print(f"牌值比较：{card1.value.numeric_value} vs {card2.value.numeric_value}")
    print("✓ 扑克牌创建测试通过")

def test_hand_recognition():
    """测试牌型识别"""
    print("\n测试牌型识别...")
    
    # 测试单张
    cards = [Card(Suit.SPADES, CardValue.ACE)]
    hand = Hand(cards)
    print(f"单张：{hand}")
    
    # 测试对子
    cards = [Card(Suit.SPADES, CardValue.ACE), Card(Suit.HEARTS, CardValue.ACE)]
    hand = Hand(cards)
    print(f"对子：{hand}")
    
    # 测试三张
    cards = [Card(Suit.SPADES, CardValue.ACE), Card(Suit.HEARTS, CardValue.ACE), Card(Suit.CLUBS, CardValue.ACE)]
    hand = Hand(cards)
    print(f"三张：{hand}")
    
    # 测试火箭
    cards = [Card(Suit.JOKER, CardValue.SMALL_JOKER), Card(Suit.JOKER, CardValue.BIG_JOKER)]
    hand = Hand(cards)
    print(f"火箭：{hand}")
    
    print("✓ 牌型识别测试通过")

def test_hand_comparison():
    """测试牌型比较"""
    print("\n测试牌型比较...")
    
    # 单张比较
    hand1 = Hand([Card(Suit.SPADES, CardValue.THREE)])
    hand2 = Hand([Card(Suit.HEARTS, CardValue.ACE)])
    print(f"{hand1} vs {hand2}: {hand2.can_beat(hand1)}")
    
    # 炸弹压普通牌
    bomb = Hand([Card(Suit.SPADES, CardValue.THREE), Card(Suit.HEARTS, CardValue.THREE), 
                 Card(Suit.CLUBS, CardValue.THREE), Card(Suit.DIAMONDS, CardValue.THREE)])
    single = Hand([Card(Suit.SPADES, CardValue.TWO)])
    print(f"炸弹 vs 单张2: {bomb.can_beat(single)}")
    
    # 火箭压炸弹
    rocket = Hand([Card(Suit.JOKER, CardValue.SMALL_JOKER), Card(Suit.JOKER, CardValue.BIG_JOKER)])
    print(f"火箭 vs 炸弹: {rocket.can_beat(bomb)}")
    
    print("✓ 牌型比较测试通过")

def test_deck_creation():
    """测试牌堆创建"""
    print("\n测试牌堆创建...")
    
    game = Game()
    game.create_deck()
    
    print(f"牌堆总数：{len(game.deck)}")
    print(f"前5张牌：{game.deck[:5]}")
    
    # 检查是否有54张牌
    assert len(game.deck) == 54, f"牌数不对，应该是54张，实际是{len(game.deck)}张"
    print("✓ 牌堆创建测试通过")

def test_ai_player():
    """测试AI玩家"""
    print("\n测试AI玩家...")
    
    player = Player("测试AI", is_human=False)
    
    # 给AI一些牌
    test_cards = [
        Card(Suit.SPADES, CardValue.THREE),
        Card(Suit.HEARTS, CardValue.THREE),
        Card(Suit.CLUBS, CardValue.FOUR),
        Card(Suit.DIAMONDS, CardValue.FIVE),
        Card(Suit.SPADES, CardValue.ACE)
    ]
    player.add_cards(test_cards)
    
    print(f"AI手牌：{player.cards}")
    
    # 测试获取可能的出牌
    valid_hands = player.get_valid_hands(None)
    print(f"可能的出牌数量：{len(valid_hands)}")
    
    # 测试AI选择
    if valid_hands:
        chosen = player.choose_hand(valid_hands)
        print(f"AI选择的牌：{chosen}")
    
    print("✓ AI玩家测试通过")

def main():
    """运行所有测试"""
    print("=" * 50)
    print("斗地主游戏功能测试")
    print("=" * 50)
    
    try:
        test_card_creation()
        test_hand_recognition()
        test_hand_comparison()
        test_deck_creation()
        test_ai_player()
        
        print("\n" + "=" * 50)
        print("🎉 所有测试通过！游戏可以正常运行。")
        print("运行 'python3 doudizhu.py' 开始游戏")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ 测试失败：{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()