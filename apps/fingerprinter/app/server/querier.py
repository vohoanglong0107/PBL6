from app.model import get_melspec_layer, get_fingerprinter
from app.dataset import Dataset
from app.utils import read_config
import numpy as np


class Querier:
    def __init__(self) -> None:
        self.cfg = read_config()
        self.bsz = int(self.cfg["BSZ"]["TS_BATCH_SZ"])
        self.dataset = Dataset(self.cfg)
        self.m_fp = get_fingerprinter(self.cfg, trainable=False)
        self.m_pre = get_melspec_layer(self.cfg, trainable=False)

    def predict(self, song):
        query_sequence = self.dataset.get_query(song)
        embs = []
        for i in range(len(query_sequence)):
            X, _ = query_sequence[i]
            emb = self.m_fp(self.m_pre(X))
            embs.append(emb.numpy())
        embs = np.concatenate(embs, axis=0)
        return embs
