#!/usr/bin/python3
# -*- encoding: utf-8 -*-
import time
from pynput import keyboard
from util.keyboardListener import KeyboardListener


class config:
    def __init__(self):
        self.key = '<ctrl_l>与<alt_l>'  # 定义切换开关键,支持"或"(很遗憾我没有小键盘,自己用tool测试,我懒得试了)
        self.exit_key = '<cmd>与<ctrl_l>'  # 定义退出程序按键
        # 定义要触发哪几个键
        self.press_list = [
            keyboard.Key.f11,
            keyboard.Key.f12,
        ]
        self.operation_interval = 0.01  # 定义每个操作间隔(比如按下f11,0.01秒后松开,0.01秒后按下f12...)
        self.round_interval = 0.01  # 定义每轮操作间隔
        self.scanning_frequency = 128  # 定义每秒执行多少轮


setting = config()
exit_flag = False
ctrler = keyboard.Controller()
press_flag = False # 触发开关
on_press = False  # 是否处于按下状态


def keyIsPress(keys, rule):
    """
    传入规则和键列表,判断规定的键是否按下

    Args:
    - keys:['<cmd>','<alt_l>']
    - rule:"<cmd>与<alt_l>或<cmd>与<alt_gr>"

    Returns:
    - bool
    """
    rule_split = rule.split('或')
    for a_rule in rule_split:
        rule_keys = a_rule.split('与')
        flag = True
        for key in rule_keys:
            if not key in keys:
                flag = False
                break
        if flag:
            return True
    return False


def press(Keys):
    """
    传入键值,判断要做的操作

    Args:
        keys:键值组成的可迭代对象
    """
    global exit_flag, ctrler,press_flag,on_press,setting
    if keyIsPress(Keys, setting.exit_key):
        exit_flag = True
    elif keyIsPress(Keys, setting.key) and not on_press:
        if not on_press:
            press_flag = not press_flag
            on_press = True
    elif on_press and not keyIsPress(Keys, setting.key):
        on_press = False
    print(press_flag)

def main():
    # 创建键盘钩子
    # 开启键盘监听器
    listener = KeyboardListener(press, setting.scanning_frequency)
    listener.start()
    # 循环阻滞主线程,当exit_flag为True时退出
    while not exit_flag:
        if press_flag:
            for key in setting.press_list:
                ctrler.press(key)
                time.sleep(setting.operation_interval)
                ctrler.release(key)
                time.sleep(setting.operation_interval)
        # 每一轮暂停
        time.sleep(setting.round_interval)
    listener.stop()


if __name__ == '__main__':
    main()
