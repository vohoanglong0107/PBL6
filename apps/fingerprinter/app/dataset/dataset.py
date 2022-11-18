# -*- coding: utf-8 -*-
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
""" dataset.py """
import glob
from .genUnbalSequence import genUnbalSequence


class Dataset:
    """
    Build dataset for train, validation and test.
    USAGE:
        dataset = Dataset(cfg)
        ds_train = dataset.get_train_ds()
        print(ds_train.__getitem__(0))
    ...
    Attributes
    ----------
    cfg : dict
        a dictionary containing configurations
    Public Methods
    --------------
    get_train_ds()
    get_val_ds()
    get_test_dummy_db_ds()
    get_test_query_db_ds()
    get_custom_db_ds(source_root_dir)
    """

    def __init__(self, cfg=dict()):
        # Data location
        self.source_root_dir = cfg["DIR"]["SOURCE_ROOT_DIR"]
        self.bg_root_dir = cfg["DIR"]["BG_ROOT_DIR"]
        self.ir_root_dir = cfg["DIR"]["IR_ROOT_DIR"]

        # BSZ
        self.tr_batch_sz = cfg["BSZ"]["TR_BATCH_SZ"]
        self.tr_n_anchor = cfg["BSZ"]["TR_N_ANCHOR"]
        self.val_batch_sz = cfg["BSZ"]["VAL_BATCH_SZ"]
        self.val_n_anchor = cfg["BSZ"]["VAL_N_ANCHOR"]
        self.ts_batch_sz = cfg["BSZ"]["TS_BATCH_SZ"]

        # Model parameters
        self.dur = cfg["MODEL"]["DUR"]
        self.hop = cfg["MODEL"]["HOP"]
        self.fs = cfg["MODEL"]["FS"]

        # Time-domain augmentation parameter
        self.tr_snr = cfg["TD_AUG"]["TR_SNR"]
        self.ts_snr = cfg["TD_AUG"]["TS_SNR"]
        self.val_snr = cfg["TD_AUG"]["VAL_SNR"]
        self.tr_use_bg_aug = cfg["TD_AUG"]["TR_BG_AUG"]
        self.ts_use_bg_aug = cfg["TD_AUG"]["TS_BG_AUG"]
        self.val_use_bg_aug = cfg["TD_AUG"]["VAL_BG_AUG"]
        self.tr_use_ir_aug = cfg["TD_AUG"]["TR_IR_AUG"]
        self.ts_use_ir_aug = cfg["TD_AUG"]["TS_IR_AUG"]
        self.val_use_ir_aug = cfg["TD_AUG"]["VAL_IR_AUG"]

        # Pre-load file paths for augmentation
        self.tr_bg_fps = self.ts_bg_fps = self.val_bg_fps = None
        self.tr_ir_fps = self.ts_ir_fps = self.val_ir_fps = None
        self.__set_augmentation_fps()

        # Source (music) file paths
        self.tr_source_fps = self.val_source_fps = None
        self.ts_dummy_db_source_fps = None
        self.ts_query_icassp_fps = self.ts_db_icassp_fps = None
        self.ts_query_db_unseen_fps = None

    def __set_augmentation_fps(self):
        """
        Set file path lists:
            If validation set was not available, we replace it with subset of
            the trainset.
        """
        # File lists for Augmentations
        if self.tr_use_bg_aug:
            self.tr_bg_fps = sorted(
                glob.glob(self.bg_root_dir + "tr/**/*.wav", recursive=True)
            )
        if self.ts_use_bg_aug:
            self.ts_bg_fps = sorted(
                glob.glob(self.bg_root_dir + "ts/**/*.wav", recursive=True)
            )
        if self.val_use_bg_aug:
            self.val_bg_fps = sorted(
                glob.glob(self.bg_root_dir + "tr/**/*.wav", recursive=True)
            )

        if self.tr_use_ir_aug:
            self.tr_ir_fps = sorted(
                glob.glob(self.ir_root_dir + "tr/**/*.wav", recursive=True)
            )
        if self.ts_use_ir_aug:
            self.ts_ir_fps = sorted(
                glob.glob(self.ir_root_dir + "ts/**/*.wav", recursive=True)
            )
        if self.val_use_ir_aug:
            self.val_ir_fps = sorted(
                glob.glob(self.ir_root_dir + "tr/**/*.wav", recursive=True)
            )

        return

    def get_train_ds(self, max_train_items=None):
        # Source (music) file paths for train set
        _prefix = "train-10k-30s/"
        self.tr_source_fps = sorted(
            glob.glob(self.source_root_dir + _prefix + "**/*.wav", recursive=True)
        )

        ds = genUnbalSequence(
            fns_event_list=self.tr_source_fps,
            bsz=self.tr_batch_sz,
            n_anchor=self.tr_n_anchor,
            # ex) bsz=40, n_anchor=8: 4 positive samples per anchor
            duration=self.dur,  # duration in seconds
            hop=self.hop,
            fs=self.fs,
            shuffle=True,
            random_offset_anchor=True,
            bg_mix_parameter=[self.tr_use_bg_aug, self.tr_bg_fps, self.tr_snr],
            ir_mix_parameter=[self.tr_use_ir_aug, self.tr_ir_fps],
            max_items=max_train_items,
        )
        return ds

    def get_val_ds(self, max_song=500):
        # Source (music) file paths for validation set.
        """
        max_song: (int) <= 500.
        """
        self.val_source_fps = sorted(
            glob.glob(
                self.source_root_dir + "val-query-db-500-30s/" + "**/*.wav",
                recursive=True,
            )
        )[:max_song]

        ds = genUnbalSequence(
            self.val_source_fps,
            self.val_batch_sz,
            self.val_n_anchor,
            self.dur,
            self.hop,
            self.fs,
            shuffle=False,
            random_offset_anchor=False,
            bg_mix_parameter=[self.val_use_bg_aug, self.val_bg_fps, self.val_snr],
            ir_mix_parameter=[self.val_use_ir_aug, self.val_ir_fps],
        )
        return ds

    def get_test_dummy_db_ds(self):
        """
        Test-dummy-DB without augmentation:
            In this case, high-speed fingerprinting is possible without
            augmentation by setting ts_n_anchor=ts_batch_sz.
        """
        # Source (music) file paths for test-dummy-DB set
        self.ts_dummy_db_source_fps = sorted(
            glob.glob(
                self.source_root_dir + "test-dummy-db-100k-full/" + "**/*.wav",
                recursive=True,
            )
        )
        self.ts_dummy_db_source_fps = self.ts_dummy_db_source_fps[:10000]

        _ts_n_anchor = self.ts_batch_sz
        ds = genUnbalSequence(
            self.ts_dummy_db_source_fps,
            self.ts_batch_sz,
            _ts_n_anchor,
            self.dur,
            self.hop,
            self.fs,
            shuffle=False,
            random_offset_anchor=False,
            drop_the_last_non_full_batch=False,
        )  # No augmentations...
        return ds

    def get_test_query_db_ds(self):
        """
        To select test dataset, you can use config file or datasel parameter.
        cfg['DATASEL']['TEST_QUERY_DB']:
            'unseen_icassp' will use pre-defined queries and DB
            'unseen_syn' will synthesize queries from DB in real-time.
        Returns
        -------
        (ds_query, ds_db)
        """

        self.ts_query_db_unseen_fps = sorted(
            glob.glob(
                self.source_root_dir + "val-query-db-500-30s/" + "db/**/*.wav",
                recursive=True,
            )
        )

        _query_ts_batch_sz = self.ts_batch_sz * 2
        _query_ts_n_anchor = self.ts_batch_sz

        ds_query = genUnbalSequence(
            self.ts_query_db_unseen_fps,
            _query_ts_batch_sz,
            _query_ts_n_anchor,
            self.dur,
            self.hop,
            self.fs,
            shuffle=False,
            random_offset_anchor=False,
            bg_mix_parameter=[self.ts_use_bg_aug, self.ts_bg_fps, self.ts_snr],
            ir_mix_parameter=[self.ts_use_ir_aug, self.ts_ir_fps],
            reduce_batch_first_half=True,
            drop_the_last_non_full_batch=False,
        )

        _db_ts_n_anchor = self.ts_batch_sz
        ds_db = genUnbalSequence(
            self.ts_query_db_unseen_fps,
            self.ts_batch_sz,
            _db_ts_n_anchor,
            self.dur,
            self.hop,
            self.fs,
            shuffle=False,
            random_offset_anchor=False,
            drop_the_last_non_full_batch=False,
        )
        return ds_query, ds_db

    def get_custom_db_ds(self, source_root_dir):
        """Construc DB (or query) from custom source files."""
        fps = sorted(glob.glob(source_root_dir + "/**/*.wav", recursive=True))
        _ts_n_anchor = self.ts_batch_sz  # Only anchors...
        ds = genUnbalSequence(
            fps,
            self.ts_batch_sz,
            _ts_n_anchor,
            self.dur,
            self.hop,
            self.fs, shuffle=False,
            random_offset_anchor=False,
            drop_the_last_non_full_batch=False,
            return_song_name=True,
        )  # No augmentations, No drop-samples.
        return ds

    def get_query(self, file):
        _ts_n_anchor = self.ts_batch_sz  # Only anchors...
        ds = genUnbalSequence(
            [file],
            self.ts_batch_sz,
            _ts_n_anchor,
            self.dur,
            self.hop,
            self.fs, shuffle=False,
            random_offset_anchor=False,
            drop_the_last_non_full_batch=False,
            return_song_name=False,
        )  # No augmentations, No drop-samples.
        return ds
