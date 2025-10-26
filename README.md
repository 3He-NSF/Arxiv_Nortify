# 🧠 arXiv Discord Notifier

GitHub Actions を使って、指定したキーワードに関連する **arXiv の最新論文を毎朝 Discord に自動通知**する Bot です。  
重複通知を防ぎ、新しい論文がない場合も「📭 No new papers found today.」と知らせてくれます。

---

## 🚀 機能

- 📰 arXiv の最新論文を毎日自動取得  
- 🔄 既に通知済みの論文はスキップ（`notified_ids.json` で管理）  
- 🕓 日本時間 朝5時に自動実行（GitHub Actions）  
- 📭 新規論文がない日も Discord に通知  

---

## 📂 リポジトリ構成

```plaintext
arxiv-discord-notifier/
├── notify.py              # Discord通知スクリプト
├── queries.json           # 通知対象クエリとWebhook設定
├── notified_ids.json      # 通知済み論文IDを保存（自動更新）
└── .github/
    └── workflows/
        └── notify.yml     # GitHub Actions の自動実行設定
