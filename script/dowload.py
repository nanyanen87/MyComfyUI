from huggingface_hub import hf_hub_download
import os
import glob


# $home/.cache/huggingface/hubにモデルをダウンロードする
# 現在のスクリプトのディレクトリを取得
script_dir = os.path.dirname(os.path.abspath(__file__))

# モデルの情報をリストで準備
models = [
    {
        "repo_id": "PvDeep/Add-Detail-XL",
        "filename": "add-detail-xl.safetensors",
        "model_type": "loras"
    },
    {
        "repo_id": "zdouble/model",
        "filename": "animagineXLV31_v31.safetensors",
        "model_type": "checkpoints"
    },
    {
        "repo_id": "lllyasviel/sd_control_collection",
        "filename": "diffusers_xl_depth_full.safetensors",
        "model_type": "controlnet"
    },
    {
        "repo_id": "stabilityai/sdxl-vae",
        "filename": "sdxl_vae.safetensors",
        "model_type": "vae"
    },
    # 必要なモデル情報を追加
]

# 各モデルをデフォルトのキャッシュディレクトリにダウンロード
for model in models:
    repo_id = model["repo_id"]
    filename = model["filename"]

    # ファイルの存在を確認
    file_path = os.path.join(os.path.expanduser("~/.cache/huggingface/hub"), filename)  # デフォルトのキャッシュディレクトリのパスを組み立てる

    if os.path.exists(file_path):
        print(f"'{filename}' はすでに存在します。ダウンロードはスキップします。")
    else:
        # モデルをダウンロード
        try:
            model_path = hf_hub_download(repo_id=repo_id, filename=filename)  # cache_dirを指定しないことでデフォルトを使用
            print(f"'{filename}' をダウンロードしました: {model_path}")
        except Exception as e:
            print(f"'{filename}' のダウンロード中にエラーが発生しました: {e}")

# シンボリックリンクの作成
COMFYUI_MODEL_PATH = os.path.join(script_dir, "..", "ComfyUI/models")
HUGGINGFACE_CACHE_PATH = os.path.expanduser("~/.cache/huggingface/hub")
for model in models:
    # 指定したディレクトリのファイルを取得
    # dir models--PvDeep--Add-Detail-XL
    # repo_id : PvDeep/Add-Detail-XL
    model_name_dir = 'models--' + model['repo_id'].replace('/', '--')
    blob_dir = os.path.join(HUGGINGFACE_CACHE_PATH, model_name_dir,'blobs')
    blob_file = glob.glob(blob_dir + "/*")
    hugging_blob_path = os.path.join(HUGGINGFACE_CACHE_PATH, 'blob', blob_file[0])
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