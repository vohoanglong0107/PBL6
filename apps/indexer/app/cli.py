from .config import Config
from .indexer import get_index, load_memmap_data, save_index, train_index


def train():
    index_path = Config.INDEX_PATH
    emb_dir = Config.EMB_DIR
    db, db_shape = load_memmap_data(emb_dir, "db")
    index = get_index(db.shape)
    train_index(index, db)
    save_index(index, index_path)


if __name__ == "__main__":
    train()
