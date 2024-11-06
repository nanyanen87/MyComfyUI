from huggingface_hub import hf_hub_download
import os
import glob
import json



# 現在のスクリプトのディレクトリを取得
script_dir = os.path.dirname(os.path.abspath(__file__))
# huggingfaceのcacheディレクトリのdefault path
src_path = os.path.join(script_dir, "..")
HUGGINGFACE_CACHE_PATH = os.path.join(src_path, "hug/cache")
# comfyuiのmodelディレクトリのpath
COMFYUI_MODEL_PATH = os.path.join(script_dir, "..", "ComfyUI/models")
# input.jsonからモデルの情報をリストで準備
models = json.load(open(os.path.join(script_dir, "input.json")))
#     "repo_id": "PvDeep/Add-Detail-XL", # huggingfaceのモデルのリポジトリID
#     "filename": "add-detail-xl.safetensors", # huggingfaceのモデルのファイル名
#     "model_type": "loras" # comfyuiのモデルのディレクトリ名、分類は雰囲気で

# 各モデルをデフォルトのキャッシュディレクトリにダウンロード
for model in models:
    repo_id = model["repo_id"]
    filename = model["filename"]

    # ファイルの存在を確認
    file_path = os.path.join(src_path, filename)

    if os.path.exists(file_path):
        print(f"'{filename}' はすでに存在します。ダウンロードはスキップします。")
    else:
        # モデルをダウンロード
        try:
            model_path = hf_hub_download(repo_id=repo_id, filename=filename, cache_dir=HUGGINGFACE_CACHE_PATH)  # cache_dirを指定しないことでデフォルトを使用
            print(f"'{filename}' をダウンロードしました: {model_path}")
        except Exception as e:
            print(f"'{filename}' のダウンロード中にエラーが発生しました: {e}")

# シンボリックリンクの作成
for model in models:
    # huggingface の　cacheディレクトリの構造
    # repo_id : PvDeep/Add-Detail-XL　->　models--PvDeep--Add-Detail-XL
    # https://huggingface.co/docs/huggingface_hub/guides/manage-cache

    model_name_dir = 'models--' + model['repo_id'].replace('/', '--')
    blob_dir = os.path.join(HUGGINGFACE_CACHE_PATH, model_name_dir,'blobs')
    blob_file = glob.glob(blob_dir + "/*")
    hugging_blob_path = os.path.join(blob_dir, 'blob', blob_file[0])
    # blobファイルの存在を確認
    if not os.path.exists(hugging_blob_path):
        print(f"'{hugging_blob_path}' が存在しません。シンボリックリンクの作成はスキップします。")
        continue

    filename = model["filename"]
    model_type = model["model_type"]
    comfyui_model_path = os.path.join(COMFYUI_MODEL_PATH, model_type, filename)

    if os.path.exists(comfyui_model_path):
        print(f"'{comfyui_model_path}' はすでに存在します。シンボリックリンクの作成はスキップします。")
    else:
        try:
            print(f"'{comfyui_model_path}' にシンボリックリンクを作成します...")
            os.symlink(hugging_blob_path, comfyui_model_path)
            print(f"'{comfyui_model_path}' にシンボリックリンクを作成しました")
        except Exception as e:
            print(f"'{comfyui_model_path}' にシンボリックリンクを作成中にエラーが発生しました: {e}")