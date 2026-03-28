#!/usr/bin/env python3
"""
儲存台南活動資料到 output/YYYY-MM-DD.md，更新 dates.json，並 git push。
用法：python3 save_events.py --date "2026-03-28" --content "markdown 內容"
"""
import argparse
import json
import os
import subprocess
from datetime import datetime

REPO = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(REPO, "output")
DATES_FILE = os.path.join(REPO, "dates.json")

def update_dates(date_str):
    if os.path.exists(DATES_FILE):
        with open(DATES_FILE, "r", encoding="utf-8") as f:
            dates = json.load(f)
    else:
        dates = []
    if date_str not in dates:
        dates.append(date_str)
        dates.sort(reverse=True)
    with open(DATES_FILE, "w", encoding="utf-8") as f:
        json.dump(dates, f, ensure_ascii=False)

def save_and_push(date_str, content):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    md_path = os.path.join(OUTPUT_DIR, f"{date_str}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(content)
    update_dates(date_str)

    try:
        subprocess.run(["git", "-C", REPO, "add", md_path, DATES_FILE], check=True, capture_output=True)
        subprocess.run(["git", "-C", REPO, "commit", "-m", f"🗓️ 台南活動 {date_str}"], check=True, capture_output=True)
        subprocess.run(["git", "-C", REPO, "push"], check=True, capture_output=True)
        return "pushed"
    except subprocess.CalledProcessError as e:
        return f"failed: {e}"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"))
    parser.add_argument("--file", help="直接指定 markdown 檔案路徑")
    parser.add_argument("--content", help="直接傳入 markdown 內容")
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
    elif args.content:
        content = args.content
    else:
        print("請提供 --file 或 --content")
        return

    status = save_and_push(args.date, content)
    print(json.dumps({"date": args.date, "git": status}, ensure_ascii=False))

if __name__ == "__main__":
    main()
