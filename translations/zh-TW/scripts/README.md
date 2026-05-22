# Scripts

此資料夾包含儲存庫驗證腳本。

## `verify_notebooks.py`

驗證本地 Markdown 連結、筆記本 JSON、筆記本輸出乾淨度及高風險密鑰模式：

```powershell
python scripts\verify_notebooks.py
```

執行所有公開且本地安全的筆記本：

```powershell
python scripts\verify_notebooks.py --execute
```

GitHub Actions 工作流程使用相同的腳本。

`drafts/` 下的草稿內容會被跳過，直到準備好公開索引。

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
此文件已使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們努力追求準確性，但請注意自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應視為權威來源。對於關鍵資訊，建議採用專業人工翻譯。我們不對因使用此翻譯所產生的任何誤解或誤譯承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->