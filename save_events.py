#!/usr/bin/env python3
"""
儲存台南活動資料，更新 dates.json，並 git push。

手動模式（--type manual，預設）：
  覆蓋 output/manual/latest.md，更新 dates.json["manual"]["updated"]

自動模式（--type auto）：
  存至 output/auto/YYYY/YYYY-MM-DD.md（週起始日，週三）
  更新 dates.json["auto"][YYYY][MM]

用法：
  python3 save_events.py --date "2026-03-30" --content "markdown 內容"
  python3 save_events.py --type auto --date "2026-04-02" --content "markdown 內容"
"""
import argparse
import json
import os
import subprocess
from datetime import datetime

REPO = os.path.dirname(os.path.abspath(__file__))
DATES_FILE = os.path.join(REPO, "dates.json")


def load_dates() -> dict:
    if os.path.exists(DATES_FILE):
        with open(DATES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # 相容舊格式（list）
        if isinstance(data, list):
            return {"manual": {"updated": data[0] if data else None}, "auto": {}}
        return data
    return {"manual": {"updated": None}, "auto": {}}


def save_dates(dates: dict):
    with open(DATES_FILE, "w", encoding="utf-8") as f:
        json.dump(dates, f, ensure_ascii=False, indent=2)


def save_manual(content: str, date_str: str) -> str:
    out_dir = os.path.join(REPO, "output", "manual")
    os.makedirs(out_dir, exist_ok=True)
    md_path = os.path.join(out_dir, "latest.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(content)

    dates = load_dates()
    dates.setdefault("manual", {})["updated"] = date_str
    save_dates(dates)

    return git_push([md_path, DATES_FILE], f"📋 手動推送 {date_str}")


def save_auto(content: str, date_str: str) -> str:
    d = datetime.strptime(date_str, "%Y-%m-%d")
    year = d.strftime("%Y")
    month = d.strftime("%m")

    out_dir = os.path.join(REPO, "output", "auto", year)
    os.makedirs(out_dir, exist_ok=True)
    md_path = os.path.join(out_dir, f"{date_str}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(content)

    dates = load_dates()
    auto = dates.setdefault("auto", {})
    weeks = auto.setdefault(year, {}).setdefault(month, [])
    if date_str not in weeks:
        weeks.append(date_str)
        weeks.sort(reverse=True)
    save_dates(dates)

    return git_push([md_path, DATES_FILE], f"📅 自動推送 {date_str}")


def git_push(files: list, message: str) -> str:
    try:
        subprocess.run(["git", "-C", REPO, "add"] + files, check=True, capture_output=True)
        subprocess.run(["git", "-C", REPO, "commit", "-m", message], check=True, capture_output=True)
        subprocess.run(["git", "-C", REPO, "push"], check=True, capture_output=True)
        return "pushed"
    except subprocess.CalledProcessError as e:
        return f"failed: {e}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", choices=["manual", "auto"], default="manual")
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

    if args.type == "auto":
        status = save_auto(content, args.date)
    else:
        status = save_manual(content, args.date)

    print(json.dumps({"type": args.type, "date": args.date, "git": status}, ensure_ascii=False))


if __name__ == "__main__":
    main()
