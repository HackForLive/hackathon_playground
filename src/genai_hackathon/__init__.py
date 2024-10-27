from pathlib import Path

base_dir = Path(__file__).parent
src_dir = base_dir.parent

env_cfg_path = src_dir.parent / '.env'
db_path = src_dir.parent / 'db' / 'vector_db'
