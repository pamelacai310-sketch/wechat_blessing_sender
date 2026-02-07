#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
在指定时间向微信好友发送藏头祝福诗。

依赖：itchat（第三方微信个人号接口库）
安装：pip install itchat

使用说明：
1. 修改 FRIENDS 列表为你要发送的 18 位好友的备注名/昵称。
2. 修改 POEMS 列表为 18 条不同的藏头诗（每条为多行字符串）。
3. 运行脚本并扫码登录。
4. 脚本会在 2 月 15 日 18:00 发送对应祝福。

注意：
- itchat 依赖微信网页端接口，可能存在稳定性或风控限制。
- 若时间已过，将立即发送。
"""
from __future__ import annotations

import datetime as dt
import time
from typing import List

import itchat

# 18 位好友的微信“备注名”或“昵称”
FRIENDS: List[str] = [
    "好友1",
    "好友2",
    "好友3",
    "好友4",
    "好友5",
    "好友6",
    "好友7",
    "好友8",
    "好友9",
    "好友10",
    "好友11",
    "好友12",
    "好友13",
    "好友14",
    "好友15",
    "好友16",
    "好友17",
    "好友18",
]

# 18 条不同的藏头诗（示例：以“新年快乐”开头）
POEMS: List[str] = [
    """新风拂柳意融融\n年华流转梦成虹\n快马扬鞭追远志\n乐在心头万事通""",
    """新雨初晴花更艳\n年岁更迭福相伴\n快意人生多坦途\n乐随笑语到天边""",
    """新星闪耀夜如昼\n年年此时情更厚\n快歌一曲祝君安\n乐享清欢到永久""",
    """新绿萌芽迎曙光\n年丰人和庆吉祥\n快把祝福寄远方\n乐在眉梢喜满堂""",
    """新月如钩照归途\n年少心愿终不负\n快意随风来入梦\n乐观前行路更舒""",
    """新春喜气绕庭前\n年岁平安福满天\n快步向前心不惧\n乐观自有好因缘""",
    """新光照耀万家灯\n年年今日梦可成\n快马加鞭向远路\n乐在其中不觉程""",
    """新芽吐翠迎朝露\n年华似水情常驻\n快意人生多喜悦\n乐享时光不辜负""",
    """新景怡人花正好\n年年岁岁福来报\n快把心愿轻轻许\n乐随清风入怀抱""",
    """新雪初融春可期\n年年好运不相离\n快心顺意皆如愿\n乐在微笑里""",
    """新阳高照暖心房\n年年喜乐满庭芳\n快马轻蹄追梦想\n乐在当下不彷徨""",
    """新歌轻唱祝福到\n年年岁岁皆美好\n快意随风传千里\n乐在心间永不老""",
    """新霞满天映笑颜\n年岁更迭情更绵\n快把烦忧都放下\n乐在今天与明天""",
    """新雨润泽万物生\n年年顺遂福相迎\n快意人生皆可期\n乐在清欢与从容""",
    """新风徐来桂香浓\n年年今日喜相逢\n快意人生多精彩\n乐在眼前与梦中""",
    """新愿轻许心相知\n年年岁岁不相离\n快把祝福寄远方\n乐在天涯亦相思""",
    """新景如画人如玉\n年年好运伴君行\n快意高歌迎未来\n乐享人生不负心""",
    """新福盈门喜气扬\n年年平安笑声长\n快把吉祥传万里\n乐在今朝与远方""",
]

TARGET_MONTH = 2
TARGET_DAY = 15
TARGET_HOUR = 18
TARGET_MINUTE = 0


def wait_until(target: dt.datetime) -> None:
    now = dt.datetime.now()
    if target <= now:
        return
    delta_seconds = (target - now).total_seconds()
    time.sleep(delta_seconds)


def find_friend(username: str) -> str | None:
    friends = itchat.search_friends(name=username)
    if not friends:
        return None
    return friends[0]["UserName"]


def main() -> None:
    if len(FRIENDS) != 18 or len(POEMS) != 18:
        raise ValueError("FRIENDS 和 POEMS 都必须是 18 条。")

    itchat.auto_login(hotReload=True)

    target_time = dt.datetime(
        year=dt.datetime.now().year,
        month=TARGET_MONTH,
        day=TARGET_DAY,
        hour=TARGET_HOUR,
        minute=TARGET_MINUTE,
    )

    wait_until(target_time)

    for friend_name, poem in zip(FRIENDS, POEMS, strict=True):
        user_name = find_friend(friend_name)
        if not user_name:
            print(f"未找到好友：{friend_name}")
            continue
        itchat.send(msg=poem, toUserName=user_name)
        time.sleep(1)


if __name__ == "__main__":
    main()
