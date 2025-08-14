import yaml
with open("Config/config.yml", "r", encoding="utf-8") as f:
    # 安全加载 YAML 内容（避免执行恶意代码）
    config = yaml.safe_load(f)

DirectoryLoader_load_path = config["DirectoryLoader_path"]

redis_url = config["redis_url"]

save_path = config["save_path"]

chunk_size = config["chunk_size"]
chunk_overlap = config["chunk_overlap"]


#embedding模型相关配置参数
embed_dim = config["dim"]
embedding_model_name = config["embedding"]["model_name"]
embedding_load_remote = config["embedding"]["load_from_remote"]
embedding_local_path = config["embedding"]["local_path"]



file_upload_delete = config["file_upload_delete"]
#llm相关配置参数
llm_type = config['llm']["type"]
llm_config = config['llm'][llm_type]

Database = config["Database"]
update_database = config["update_database"]
milvus_config = config["Milvus_config"]
split_strategy = config["split_strategy"]