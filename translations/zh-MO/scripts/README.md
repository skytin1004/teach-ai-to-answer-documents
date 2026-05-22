# Scripts

此資料夾包含存儲庫驗證腳本。

## `verify_notebooks.py`

驗證本地 Markdown 連結、筆記本 JSON、筆記本輸出清潔度以及高風險秘密模式：

```powershell
python scripts\verify_notebooks.py
```

執行所有公共本地安全的筆記本：

```powershell
python scripts\verify_notebooks.py --execute
```

GitHub Actions 工作流程使用相同的腳本。

`drafts/` 下的草稿材料將被跳過，直到準備好進入公開索引。

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們力求準確，但請注意，自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議尋求專業人工翻譯。我們不對因使用本翻譯而引起的任何誤解或曲解承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->