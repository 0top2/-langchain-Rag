import yaml
with open("Config/config.yml", "r", encoding="utf-8") as f:
    # 安全加载 YAML 内容（避免执行恶意代码）
    config = yaml.safe_load(f)
DirectoryLoader_load_path = config["DirectoryLoader_path"]
redis_url = config["redis_url"]
save_path = config["save_path"]
chunk_size = config["chunk_size"]
chunk_overlap = config["chunk_overlap"]
embedding_url = config["embedding_model_url"]
embed_dim = config["dim"]
file_upload_delete = config["file_upload_delete"]
llm_type = config["llm_type"]

zhipu_api_key = config["zhipu_api_key"]
spark_api_key = config["spark_api_key"]
spark_api_id = config["spark_api_id"]
spark_api_secret = config["spark_api_secret"]

Database = config["Database"]
update_database = config["update_database"]
milvus_config = config["Milvus_config"]