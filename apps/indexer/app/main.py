# -*- coding: utf-8 -*-
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import time
import faiss
import numpy as np


def load_memmap_data(
    source_dir, fname, append_extra_length=None, shape_only=False, display=True
):
    """
    Load data and datashape from the file path.
    • Get shape from [source_dir/fname_shape.npy}.
    • Load memmap data from [source_dir/fname.mm].
    Parameters
    ----------
    source_dir : (str)
    fname : (str)
        File name except extension.
    append_empty_length : None or (int)
        Length to appened empty vector when loading memmap. If activate, the
        file will be opened as 'r+' mode.
    shape_only : (bool), optional
        Return only shape. The default is False.
    display : (bool), optional
        The default is True.
    Returns
    -------
    (data, data_shape)
    """
    path_shape = source_dir + fname + "_shape.npy"
    path_data = source_dir + fname + ".mm"
    data_shape = np.load(path_shape)
    if shape_only:
        return data_shape

    if append_extra_length:
        data_shape[0] += append_extra_length
        data = np.memmap(
            path_data, dtype="float32", mode="r+", shape=(data_shape[0], data_shape[1])
        )
    else:
        data = np.memmap(
            path_data, dtype="float32", mode="r", shape=(data_shape[0], data_shape[1])
        )
    if display:
        print(f"Load {data_shape[0]:,} items from \033[32m{path_data}\033[0m.")
    return data, data_shape


def get_index(train_data, train_data_shape, use_gpu=True, max_nitem_train=2e7):
    """
    • Create FAISS index
    • Train index using (partial) data
    • Return index

    Parameters
    ----------
    index_type : (str)
        Index type must be one of {'L2', 'IVF', 'IVFPQ', 'IVFPQ-RR',
                                   'IVFPQ-ONDISK', HNSW'}
    train_data : (float32)
        numpy.memmap or numpy.ndarray
    train_data_shape : list(int, int)
        Data shape (n, d). n is the number of items. d is dimension.
    use_gpu: (bool)
        If False, use CPU. Default is True.
    max_nitem_train : (int)
        Max number of items to be used for training index. Default is 1e7.

    Returns
    -------
    index : (faiss.swigfaiss_avx2.GpuIndex***)
        Trained FAISS index.

    References:

        https://github.com/facebookresearch/faiss/wiki/Faiss-indexes

    """

    # Fingerprint dimension, d
    d = train_data_shape[1]

    # Build a flat (CPU) index
    index = faiss.IndexFlatL2(d)  #

    print(f"Creating index: \033[93mivfpq\033[0m")

    # Using IVF-PQ index
    code_sz = 64  # power of 2
    n_centroids = 3  #
    nbits = 8  # nbits must be 8, 12 or 16, The dimension d should be a multiple of M.
    index = faiss.IndexIVFPQ(index, d, n_centroids, code_sz, nbits)

    # Train index
    start_time = time.time()
    if len(train_data) > max_nitem_train:
        print(
            "Training index using {:>3.2f} % of data...".format(
                100.0 * max_nitem_train / len(train_data)
            )
        )
        # shuffle and reduce training data
        sel_tr_idx = np.random.permutation(len(train_data))
        sel_tr_idx = sel_tr_idx[:max_nitem_train]
        index.train(train_data[sel_tr_idx, :])
    else:
        print("Training index...")
        index.train(train_data)  # Actually do nothing for {'l2', 'hnsw'}
    print("Elapsed time: {:.2f} seconds.".format(time.time() - start_time))

    # N probe
    index.nprobe = 40
    return index


emb_dir = "generated/"
# Load items from {query, db, dummy_db}
db, db_shape = load_memmap_data(emb_dir, "db5")
# Create and train FAISS index

index = get_index(db, db.shape)
index.add(db)
query = np.load("query.npy")
l = query.shape[0]
n, I = index.search(query, 20)
print(l)
print(I)
for offset in range(len(I)):
    I[offset, :] -= offset
print(n)
print(I)
candidates = np.unique(I[np.where(I >= 0)])
print(candidates)
_scores = np.zeros(len(candidates))
for ci, cid in enumerate(candidates):
    if cid + l > index.ntotal:
        continue
    _scores[ci] = np.mean(
        np.diag(
            # np.dot(query, index.reconstruct_n(int(cid), int(l)).T)
            np.dot(query, db[cid : cid + l, :].T)
        )
    )

print(_scores)
pred_ids = candidates[np.argsort(-_scores)[:10]]
print(pred_ids)
songs = set()
current_id = 0
with open("generated/songs5.txt") as f:
    for i, line in enumerate(f):
        if i == pred_ids[current_id]:
            songs.add(line)
            print(pred_ids[current_id], i, line)
            current_id += 1
print(songs)
