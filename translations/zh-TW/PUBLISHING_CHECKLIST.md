# 發布檢查清單

在提交或推送公共更新之前，請使用此檢查清單。

## 安全

- 確認沒有在 Markdown 文件、筆記本、範例資料或腳本中寫入 API 金鑰、令牌、密碼或私有端點。
- 將憑證保存在環境變數或受管理身份中，而非已提交的文件中。
- 不要提交 `.env` 文件或執行過的筆記本輸出文件。
- 保持 `.env.example` 僅作為佔位符。

## 驗證

執行存放庫驗證腳本：

```powershell
python scripts\verify_notebooks.py
```

在發布實作變更之前，執行完整的本地安全筆記本運行：

```powershell
python scripts\verify_notebooks.py --execute
```

預期檢查項目：

- 本地 Markdown 連結通過
- 筆記本 JSON 驗證通過
- 筆記本不包含已保存的輸出或執行計數
- 高風險秘密模式掃描通過
- 公共筆記本可在本地執行
- `drafts/` 下的草稿資料故意跳過

## 審查

- 確認 README 文章連結指向預期的文件。
- 確認每篇文章都有存放庫導航和相關的筆記本連結。
- 確認草稿未從公開索引鏈接，除非已準備好發布。
- 確認 GitHub 問題和拉取請求模板仍符合存放庫流程。
- 確認文章中的驗證結果與最新筆記本輸出匹配。
- 確認 GitHub Actions 工作流程預期在推送後運行。
- 確認 `CHANGELOG.md` 反映了即將發布的更新。
- 確認 `CONTRIBUTING.md` 仍符合存放庫流程。

## Git

- 查看 `git status --short --branch`。
- 查看 `git diff --stat`。
- 僅在明確準備好時提交並推送。

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
此文件已使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們努力追求準確性，但請注意自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應視為權威來源。對於關鍵資訊，建議採用專業人工翻譯。我們不對因使用此翻譯所產生的任何誤解或誤譯承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->