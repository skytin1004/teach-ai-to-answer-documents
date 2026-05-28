# 發佈檢查清單

在提交或推送公開更新之前使用此檢查清單。

## 安全性

- 確認沒有將 API 金鑰、令牌、密碼或私有端點寫入 Markdown 文件、筆記本、示例數據或腳本中。
- 將憑證保存在環境變量或受管理身份中，而非已提交的文件中。
- 不要提交 `.env` 文件或執行過的筆記本輸出文件。
- 保持 `.env.example` 僅作為佔位符。

## 驗證

運行存儲庫驗證腳本：

```powershell
python scripts\verify_notebooks.py
```

在發佈實作變更前執行完整的本地安全筆記本執行：

```powershell
python scripts\verify_notebooks.py --execute
```

預期檢查項目：

- 本地 Markdown 連結通過
- 筆記本 JSON 驗證通過
- 筆記本不包含已保存的輸出或執行計數
- 高風險秘密模式掃描通過
- 公開筆記本可在本地執行
- `drafts/` 下的草稿材料故意跳過

## 審核

- 確認 README 文章連結指向預期的文件。
- 確認每篇文章都有存儲庫導航和相關筆記本連結。
- 確認除非草稿已準備發佈，否則不從公開索引中鏈接草稿。
- 確認 GitHub issue 和 pull request 模板仍符合存儲庫工作流程。
- 確認文章中的驗證結果與最新的筆記本輸出相符。
- 確認 GitHub Actions 工作流程預期在推送後執行。
- 確認 `CHANGELOG.md` 反映正在發佈的更新。
- 確認 `CONTRIBUTING.md` 仍符合存儲庫工作流程。

## Git

- 檢查 `git status --short --branch`。
- 檢查 `git diff --stat`。
- 僅在明確準備好時提交和推送。

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件由 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻譯而成。雖然我們致力於確保準確性，但請注意，機器自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議進行專業人工翻譯。我們不對因使用本翻譯而產生的任何誤解或誤釋承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->