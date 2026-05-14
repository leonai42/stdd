#!/usr/bin/env python3
"""简单的命令行问候程序 — STDD 示例。"""
import argparse
from datetime import datetime


def get_greeting(hour: int, formal: bool = False) -> str:
    if 6 <= hour < 12:
        return "早上好"
    elif 12 <= hour < 18:
        return "下午好"
    elif 18 <= hour < 22:
        return "晚上好"
    else:
        return "你好"


def format_greeting(name: str, time_greeting: str, formal: bool = False) -> str:
    if formal:
        return f"尊敬的 {name}，{time_greeting}！"
    return f"{time_greeting}, {name}!"


def main():
    parser = argparse.ArgumentParser(description="问候程序")
    parser.add_argument("name", help="用户名")
    parser.add_argument("--formal", action="store_true", help="正式问候模式")
    args = parser.parse_args()

    hour = datetime.now().hour
    greeting = get_greeting(hour, args.formal)
    print(format_greeting(args.name, greeting, args.formal))


if __name__ == "__main__":
    main()
