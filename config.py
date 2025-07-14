import yaml
with open("config.yml", "r", encoding="utf-8") as f:
    # 安全加载 YAML 内容（避免执行恶意代码）
    config = yaml.safe_load(f)

redis_url = config["redis_url"]
save_path = config["save_path"]
chunk_size = config["chunk_size"]
chunk_overlap = config["chunk_overlap"]
embedding_url = config["embedding_model_url"]
file_upload_delete = config["file_upload_delete"]