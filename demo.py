#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
斗地主游戏演示
"""

from doudizhu import *

def main():
    print("🎮 斗地主游戏演示")
    print("=" * 50)
    
    # 创建游戏实例
    game = Game()
    
    # 创建AI玩家（非交互式）
    game.players = [
        Player("AI-小明", is_human=False),
        Player("AI-小红", is_human=False), 
        Player("AI-小刚", is_human=False)
    ]
    
    # 初始化游戏
    game.create_deck()
    game.deal_cards()
    
    print("✓ 已创建54张牌并发给3名AI玩家")
    print("✓ 每人17张牌，剩余3张作为地主牌")
    
    # 选择地主
    landlord = game.choose_landlord()
    
    print(f"✓ {landlord.name} 成为地主，获得额外3张牌")
    print(f"✓ 地主现在有{len(landlord.cards)}张牌")
    
    # 显示各玩家手牌数量
    print("\n当前玩家状态：")
    for player in game.players:
        role = "地主" if player.is_landlord else "农民"
        print(f"  {player.name}({role})：{len(player.cards)}张牌")
    
    print("\n✅ 斗地主游戏初始化完成！")
    print("\n游戏特性：")
    print("• 完整的54张牌（包含大小王）")
    print("• 支持所有经典牌型识别")
    print("• 智能AI对手")
    print("• 交互式命令行界面")
    
    print("\n🎯 要开始真正的游戏，请运行：")
    print("   python3 doudizhu.py")

if __name__ == "__main__":
    main()