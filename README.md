# MyComfyUIサーバー

このプロジェクトは、Docker Composeを使用してComfyUIサーバーをセットアップします。<br>
自分で使用するmodelやinput imageを設定することができます。

## 事前準備
1. （がんばってcontainer外のGPUを使用できるようにする。）
2. **依存関係のインストール**<br>
   必要なPythonパッケージをインストールします。
   ```bash
   pip install huggingface_hub
   ```

2. **モデルのダウンロード**<br>
   ダウンロードしたいモデルは`modles/input.json`に記述し、`download.py`スクリプトを使用してモデルをダウンロードします。
   ```bash
   python models/download.py
   ```

## サーバーの起動

1. **サーバーの立ち上げ**<br>
   依存関係のセットアップとモデルのダウンロードが完了したら、以下のコマンドでComfyUIサーバーを起動します。
   ```bash
   docker compose up
   ```

これにより、`compose.yml`ファイルに基づいてサーバーが初期化されます。

## 補足情報

- **Composeファイル**: `compose.yml`はすべてのコンテナ依存関係を管理します。
- **スクリプト**: `script/download.py`はサーバーに必要なモデルの自動ダウンロードを行います。
- **inputフォルダ**: `input`フォルダには、comfyUIでinputに使用したいimageを置けます。
-
```
