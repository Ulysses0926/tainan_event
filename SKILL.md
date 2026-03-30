---
name: tainan-events
description: 搜尋並整理台南當日活動資訊，來源以官方網站為優先，輸出含時間、地點、來源 URL 的完整格式。
---

# 台南活動蒐集器 Skill

## 部署資訊

- **本地路徑**：`/Users/chenyuhang/Claude_Skill/tainan_events`
- **GitHub repo**：`https://github.com/Ulysses0926/tainan_event.git`
- **靜態網站**：Cloudflare Pages（連接 GitHub repo，Build command 留空，Output dir 為 `/`）
- **存檔腳本**：`save_events.py`，執行後會存 `output/YYYY-MM-DD.md`、更新 `dates.json`、並 git push

### 儲存活動資料

```bash
python3 /Users/chenyuhang/Claude_Skill/tainan_events/save_events.py \
  --date "YYYY-MM-DD" \
  --content "markdown 內容"
```

或用 `--file` 指定已存在的 md 檔案路徑。

---

## 目標
搜尋並整理台南當日活動資訊，來源以官方網站為優先。

## 觸發條件
Telegram 訊息包含：「台南今天有什麼活動」、「台南活動」、「今天台南」

---

## 資料來源優先順序

### 官方／政府
1. 台南市文化局：https://culture.tainan.gov.tw/act_month/index?Parser=99,5,44
2. 台南文化中心：https://www.tmcc.gov.tw/Event/C000014
3. 台南市政府活動公告：https://www.tainan.gov.tw/News.aspx?n=13372&sms=9752
4. 台南市美術館：https://www.tnam.museum/event/current

### 民間場館
5. 奇美博物館：https://www.chimeimuseum.org/
6. 十鼓文化村：https://www.ten-drum.com.tw/
7. 南紡購物中心：https://www.nanfung.com.tw/
8. 三井 Outlet Park 台南：搜尋「三井 Outlet 台南 活動」
9. 新光三越台南：搜尋「新光三越台南 活動」
10. 誠品生活台南：搜尋「誠品台南 活動」

---

## 執行步驟

1. 取得今日日期（YYYY-MM-DD）

2. WebSearch 搜尋：
   - `台南 活動 [今日日期]`
   - `台南文化中心 活動 [今日日期]`
   - `site:culture.tainan.gov.tw 活動 [今日日期]`

3. WebFetch 依優先順序擷取各來源頁面

4. 對各來源找到的活動，**點進個別活動頁面**取得詳細時間（HH:MM–HH:MM）
   - 台南文化中心個別活動連結格式：`https://www.tmcc.gov.tw/Event/C000014/{event-id}`

5. 依下方格式整理並回覆 Telegram

---

## 輸出格式（每筆活動都必須包含以下欄位）

```
📅 台南今日活動（YYYY/MM/DD）

🏛 來源名稱（如：台南文化中心）
- 活動名稱
  時間：HH:MM–HH:MM（或「全天」／「時間待確認」）
  地點：XXX（完整地址）
  來源：https://...
  來源網站：XXX

🎪 來源名稱
- ...
```

---

## 規則
- 不抓取任何圖片，只保留文字與 URL
- 每筆活動的來源 URL 欄位不可省略（找不到則標「無連結」）
- 不確定的資訊標「待確認」，不要自行補填
- 多天活動不要只寫開幕時間，要標明完整期間與每日開放時間
- 時間格式統一為 HH:MM–HH:MM（例如 15:30–17:30）

## 來源多元性規則
- 每次搜尋必須至少涵蓋 3 個不同來源網站
- 同一來源網站的活動不得超過總筆數的 40%
- 彙整網站（如熱血玩台南）可以使用，但必須同時搜尋官方網站
- 搜尋順序：先逐一查詢各官方場館，最後才用彙整網站補充漏網之魚

---

## 完整工作流程（Telegram 觸發）

1. 收到 Telegram 訊息含「台南活動」觸發字
2. 取得今日日期
3. WebSearch + WebFetch 各官方場館頁面
4. 對個別活動點入詳情頁取得精確時間（HH:MM–HH:MM）
5. 整理成 markdown 格式
6. 執行 `save_events.py` 存檔並 git push（更新 Cloudflare 靜態網站）
7. 用 Telegram reply 回覆整理結果

## 輸出 Markdown 格式（儲存用）

```markdown
# 台南今日活動（YYYY/MM/DD）

---

## 🏛 來源名稱

- **活動名稱**
  時間：HH:MM–HH:MM
  地點：完整地點
  來源：https://...
  來源網站：來源名稱
```

## 注意事項
- 台南文化中心個別活動詳情頁格式：`https://www.tmcc.gov.tw/Event/C000014/{event-id}`
- 熱血玩台南彙整頁：`https://decing.tw/tainan-[日期]/`（例如 `tainan-2026032829`）
