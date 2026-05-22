# 發佈清單

在提交或推送公開更新前，請使用此清單。

## 安全性

- 確認沒有將 API 金鑰、令牌、密碼或私有端點寫入 Markdown 檔案、筆記本、範例資料或腳本中。
- 將憑證保存在環境變數或受管理身分中，不要放在已提交的檔案裡。
- 不要提交 `.env` 檔案或已執行的筆記本輸出檔案。
- 保持 `.env.example` 僅為佔位符。

## 驗證

執行儲存庫驗證腳本：

```powershell
python scripts\verify_notebooks.py
```

在發佈實作更改前，執行完整本地安全的筆記本執行：

```powershell
python scripts\verify_notebooks.py --execute
```

預期檢查：

- 本地 Markdown 連結通過
- 筆記本 JSON 驗證通過
- 筆記本不含已保存的輸出或執行計數
- 高風險秘密模式掃描通過
- 公開筆記本可本地執行
- 故意略過 `drafts/` 下的草稿資料

## 審查

- 確認 README 文章連結指向預期的檔案。
- 確認每篇文章都有儲存庫導覽和相關筆記本連結。
- 確認草稿未從公開索引連結，除非已準備好發佈。
- 確認 GitHub issue 和 pull request 範本仍符合儲存庫工作流程。
- 確認文章中的驗證結果與最新的筆記本輸出一致。
- 確認 GitHub Actions 工作流程會在推送後執行。
- 確認 `CHANGELOG.md` 反映正在發佈的更新。
- 確認 `CONTRIBUTING.md` 仍符合儲存庫工作流程。

## Git

- 查看 `git status --short --branch`。
- 查看 `git diff --stat`。
- 僅在明確準備好時提交並推送。

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：
本文件使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們力求準確，但請注意，自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議尋求專業人工翻譯。我們不對因使用本翻譯而引起的任何誤解或曲解承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->