# MyComfyUIサーバー

このプロジェクトは、Docker Composeを使用してComfyUIサーバーをセットアップします。<br>
自分で使用するmodelやinput imageを設定することができます。
## 前提条件
- nvidia-driverがinstallされていること。
```nvidia-smi```で確認。
- Dockerがinstallされていること。
```docker --version```で確認。

## セットアップ
1. **モデルの一括ダウンロード**<br>
   ダウンロードしたいモデルは`modles/input.json`に記述し、`download.py`スクリプトを使用してモデルをダウンロードします。<br>普通にダウンロードしてもいいです。
   ```bash
   python models/download.py
   ```
2. input imageはComfyUI-Managerがめっちゃ使いやすくなったのでいらなくなりました。
## containerの起動

   依存関係のセットアップとモデルのダウンロードが完了したら、以下のコマンドでComfyUIサーバーを起動します。
   ```bash
   docker compose up
   ```

これにより、`compose.yml`ファイルに基づいてサーバーが初期化されます。

## 補足情報

- **Composeファイル**: `compose.yml`はすべてのコンテナ依存関係を管理します。
- **スクリプト**: `script/download.py`はサーバーに必要なモデルの自動ダウンロードを行います。
- **inputフォルダ**: `input`フォルダには、comfyUIでinputに使用したいimageを置けます。
