# 影響力傳承平台（Demo）｜家族影響力指數

以人為本的家族傳承入門工具。採匿名作答，3 分鐘產出雷達圖與建議，做為家族會議與顧問諮詢的自然入口。

## 功能
- 《家族影響力指數》：12 題 Likert，四大面向（角色、參與、情感、願景）
- 即時雷達圖、分數表、建議摘要
- 下載 CSV 與圖像（PNG）
- 《傳承準備度測驗》頁面預留

## 專案結構
```
.
├── app.py
├── pages
│   ├── 01_家族影響力指數.py
│   └── 02_傳承準備度測驗.py
├── utils
│   ├── scoring.py
│   └── charts.py
├── assets
├── .streamlit
│   └── config.toml
└── requirements.txt
```

## 本地執行
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 部署到 Streamlit Cloud
1. 將此專案上傳至 GitHub（公開或私有）。
2. Streamlit Cloud 連結該 repo，主檔 `app.py`。
3. 其餘維持預設即可啟動。

## 版權與隱私
- 此 Demo 不會自動上傳作答資料；若需雲端保存，請自行接入後端或雲端資料庫。
- 聯絡：123@gracefo.com
