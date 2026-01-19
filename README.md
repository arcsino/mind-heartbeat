# mind-heartbeat

スタンプとコメントで「気持ち」を記録し、心拍数データとあわせてその関係性をグラフで可視化できるシステムです。日々の気持ちの変化や、心身の状態とのつながりを直感的に振り返ることができます。

## 初期セットアップ

1. **リポジトリのクローン**

   ```powershell
   git clone <このリポジトリのURL>
   ```

2. **Python 仮想環境の作成・有効化**

   ```powershell
   python -m venv .venv
   # Windows:
   .\.venv\Scripts\activate
   # macOS/Linux:
   # source .venv/bin/activate
   ```

3. **依存パッケージのインストール**

   ```powershell
   pip install -r requirements.txt
   ```

4. **環境変数ファイル(.env)の作成**

   プロジェクトルート(例: mind-heartbeat/mind_heartbeat/, manage.py と同じディレクトリ)に `.env` ファイルを作成し、必要な環境変数(例：`SECRET_KEY` やデータベース設定など)を記述してください。
   ※この設定を行わないとサーバーを起動できません。

   ```env
   # 例
   SECRET_KEY=your-secret-key
   DEBUG=True
   # 必要に応じて追加
   ```

5. **VS Code デバッグ設定(.vscode/launch.json)**

   `.vscode/launch.json` には、VS Code で Django サーバーをデバッグ起動するための設定が記述されています。内容例：

   ```json
   {
     "version": "0.2.0",
     "configurations": [
       {
         "name": "runserver",
         "type": "debugpy",
         "request": "launch",
         "args": ["runserver"],
         "django": true,
         "autoStartBrowser": true,
         "program": "${workspaceFolder}\\mind_heartbeat\\manage.py",
         "envFile": "${workspaceFolder}\\mind_heartbeat\\.env"
       }
     ]
   }
   ```

   この設定により、VS Code のデバッグボタンから直接サーバーを起動できます。

6. **マイグレーションの実行**

   アプリディレクトリ(`mind_heartbeat`)に移動して実行：

   ```powershell
   cd mind_heartbeat
   python manage.py migrate
   ```

---

## 開発サーバーの起動

1. **Django 開発サーバーの起動**

   アプリディレクトリ(`mind_heartbeat`)で実行：

   ```powershell
   python manage.py runserver
   ```

   VS Code のデバッグボタンからも直接サーバーを起動できます。

2. **アクセス**
   ブラウザで [http://127.0.0.1:8000/](http://127.0.0.1:8000/) を開いて動作確認してください。

---

## フロントエンド

- UI は Bootstrap5 で装飾
- グラフは Chart.js(CDN)で描画

---

## その他

- 管理画面: `/admin/` でアクセス可能(スーパーユーザー作成は `python manage.py createsuperuser` を実行)
- 静的ファイル: `static/` ディレクトリ
- テンプレート: `mind_heartbeat/templates/` 配下
