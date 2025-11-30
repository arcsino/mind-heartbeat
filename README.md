# mind-heartbeat

スタンプとコメントで「気持ち」を記録し、心拍数データとあわせてその関係性をグラフで可視化できるシステムです。日々の感情の変化や、心身の状態とのつながりを直感的に振り返ることができます。

## 初期セットアップ

1. **リポジトリのクローン**

   ```powershell
   git clone <このリポジトリのURL>
   cd mind-heartbeat
   ```

2. **Python 仮想環境の作成・有効化**

   ```powershell
   python -m venv .venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   # source venv/bin/activate
   ```

3. **依存パッケージのインストール**

   ```powershell
   pip install -r requirements.txt
   ```

   ※ `requirements.txt` がない場合は主要パッケージを手動でインストールしてください。

4. **マイグレーションの実行**

   ```powershell
   cd mind_heartbeat
   python manage.py migrate
   ```

5. **開発サーバの起動**

   ```powershell
   python manage.py runserver
   ```

6. **アクセス**
   ブラウザで [http://localhost:8000/](http://localhost:8000/) を開いて動作確認。

---

## フロントエンド

- UI は Tailwind CSS（CDN）で装飾済み
- グラフは Chart.js（CDN）で描画

---

## その他

- 管理画面: `/admin/` でアクセス可能（スーパーユーザー作成は `python manage.py createsuperuser`）
- 静的ファイル: `static/` ディレクトリ
- テンプレート: `mind_heartbeat/templates/` 配下
