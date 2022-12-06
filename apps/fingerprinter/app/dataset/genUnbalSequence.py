from pathlib import Path

import numpy as np

from tensorflow.keras.utils import Sequence

from .audio_utils import (
    bg_mix_batch,
    get_fns_seg_list,
    ir_aug_batch,
    load_audio,
    load_audio_multi_start,
)


MAX_IR_LENGTH = 600  # 400  # 50ms with fs=8000


class genUnbalSequence(Sequence):
    def __init__(
        self,
        fns_event_list,
        bsz=120,
        n_anchor=60,
        duration=1,
        hop=0.5,
        fs=8000,
        shuffle=False,
        seg_mode="all",
        amp_mode="normal",
        random_offset_anchor=False,
        offset_margin_hop_rate=0.4,
        bg_mix_parameter=[False],
        ir_mix_parameter=[False],
        reduce_batch_first_half=False,
        experimental_mode=False,
        drop_the_last_non_full_batch=True,
        return_song_name=False,
        max_items=None,
    ):
        """

        Parameters
        ----------
        fns_event_list : list(str),
            Song file paths as a list.
        bsz : (int), optional
            In TPUs code, global batch size. The default is 120.
        n_anchor : TYPE, optional
            ex) bsz=40, n_anchor=8 --> 4 positive samples for each anchor
            (In TPUs code, global n_anchor). The default is 60.
        duration : (float), optional
            Duration in seconds. The default is 1.
        hop : (float), optional
            Hop-size in seconds. The default is .5.
        fs : (int), optional
            Sampling rate. The default is 8000.
        shuffle : (bool), optional
            Randomize samples from the original songs. BG/IRs will not be
            affected by this parameter (BG/IRs are always shuffled).
            The default is False.
        seg_mode : (str), optional
            DESCRIPTION. The default is "all".
        amp_mode : (str), optional
            DESCRIPTION. The default is 'normal'.
        random_offset_anchor : (bool), optional
            DESCRIPTION. The default is False.
        offset_margin_hop_rate : (float), optional
            For example, 0.4 means max 40 % overlaps. The default is 0.4.
        bg_mix_parameter : list([(bool), list(str), (int, int)]), optional
            [True, BG_FILEPATHS, (MIN_SNR, MAX_SNR)]. The default is [False].
        ir_mix_parameter : list([(bool), list(str)], optional
            [True, BG_FILEPATHS, (MIN_SNR, MAX_SNR)]. The default is [False].
        speech_mix_parameter : list([(bool), list(str), (int, int)]), optional
            [True, SPEECH_FILEPATHS, (MIN_SNR, MAX_SNR)]. The default is [False].
        reduce_items_p : (int), optional
            Reduce dataset size to percent (%).
            Useful when debugging code with small data. The default is 0.
        reduce_batch_first_half : (bool), optional
            Remove the first half of elements from each output batch. The
            resulting output batch will contain only replicas. This is useful
            when collecting synthesized queries only. Default is False.
        experimental_mode : (bool), optional
            In experimental mode, we use a set of pre-defined offsets for
            the multiple positive samples.. The default is False.
        drop_the_last_non_full_batch : (bool), optional
            Set as False in test. Default is True.
        """
        self.bsz = bsz
        self.n_anchor = n_anchor
        if bsz != n_anchor:
            self.n_pos_per_anchor = round((bsz - n_anchor) / n_anchor)
            self.n_pos_bsz = bsz - n_anchor
        else:
            self.n_pos_per_anchor = 0
            self.n_pos_bsz = 0

        self.duration = duration
        self.hop = hop
        self.fs = fs
        self.shuffle = shuffle
        self.seg_mode = seg_mode
        self.amp_mode = amp_mode
        self.random_offset_anchor = random_offset_anchor
        self.offset_margin_hop_rate = offset_margin_hop_rate
        self.offset_margin_frame = int(hop * self.offset_margin_hop_rate * fs)

        self.bg_mix = bg_mix_parameter[0]
        self.ir_mix = ir_mix_parameter[0]

        if self.bg_mix is True:
            fns_bg_list = bg_mix_parameter[1]
            self.bg_snr_range = bg_mix_parameter[2]

        if self.ir_mix is True:
            fns_ir_list = ir_mix_parameter[1]

        self.fns_event_seg_list = get_fns_seg_list(
            fns_event_list, self.seg_mode, self.fs, self.duration, hop=self.hop
        )
        """Structure of fns_event_seg_list:
        
        [[filename, seg_idx, offset_min, offset_max], [ ... ] , ... [ ... ]]
        
        """

        self.drop_the_last_non_full_batch = drop_the_last_non_full_batch

        if self.drop_the_last_non_full_batch:  # training
            self.n_samples = int((len(self.fns_event_seg_list) // n_anchor) * n_anchor)
        else:
            self.n_samples = len(self.fns_event_seg_list)  # fp-generation

        if self.shuffle is True:
            self.index_event = np.random.permutation(self.n_samples)
        else:
            self.index_event = np.arange(self.n_samples)

        if self.bg_mix is True:
            self.fns_bg_seg_list = get_fns_seg_list(
                fns_bg_list, "all", self.fs, self.duration
            )
            self.n_bg_samples = len(self.fns_bg_seg_list)
            if self.shuffle is True:
                self.index_bg = np.random.permutation(self.n_bg_samples)
            else:
                self.index_bg = np.arange(self.n_bg_samples)

        if self.ir_mix is True:
            self.fns_ir_seg_list = get_fns_seg_list(
                fns_ir_list, "first", self.fs, self.duration
            )
            self.n_ir_samples = len(self.fns_ir_seg_list)
            if self.shuffle is True:
                self.index_ir = np.random.permutation(self.n_ir_samples)
            else:
                self.index_ir = np.arange(self.n_ir_samples)

        self.reduce_batch_first_half = reduce_batch_first_half
        self.experimental_mode = experimental_mode
        if experimental_mode:
            self.experimental_mode_offset_sec_list = (
                (np.arange(self.n_pos_per_anchor) - (self.n_pos_per_anchor - 1) / 2)
                / self.n_pos_per_anchor
            ) * self.hop
        self.return_song_name = return_song_name
        self.max_items = max_items

    def __len__(self):
        """Returns the number of batches per epoch."""
        if self.max_items:
            return min(
                int(np.ceil(self.n_samples / float(self.n_anchor))), self.max_items
            )
        return int(np.ceil(self.n_samples / float(self.n_anchor)))

    def on_epoch_end(self):
        """Re-shuffle"""
        if self.shuffle is True:
            self.index_event = list(np.random.permutation(self.n_samples))
        else:
            pass

        if self.bg_mix is True and self.shuffle is True:
            self.index_bg = list(
                np.random.permutation(self.n_bg_samples)
            )  # same number with event samples
        else:
            pass

        if self.ir_mix is True and self.shuffle is True:
            self.index_ir = list(
                np.random.permutation(self.n_ir_samples)
            )  # same number with event samples
        else:
            pass

    def __getitem__(self, idx):
        """Get anchor (original) and positive (replica) samples."""
        index_anchor_for_batch = self.index_event[
            idx * self.n_anchor : (idx + 1) * self.n_anchor
        ]
        Xa_batch, Xp_batch, name_batch = self.__event_batch_load(index_anchor_for_batch)
        global bg_sel_indices

        if self.bg_mix is True:
            if self.n_pos_bsz > 0:
                # Prepare bg for positive samples
                bg_sel_indices = (
                    np.arange(idx * self.n_pos_bsz, (idx + 1) * self.n_pos_bsz)
                    % self.n_bg_samples
                )
                index_bg_for_batch = self.index_bg[bg_sel_indices]
                Xp_bg_batch = self.__bg_batch_load(index_bg_for_batch)
                # mix
                Xp_batch = bg_mix_batch(
                    Xp_batch, Xp_bg_batch, self.fs, snr_range=self.bg_snr_range
                )

        if self.ir_mix is True:
            if self.n_pos_bsz > 0:
                # Prepare ir for positive samples
                ir_sel_indices = (
                    np.arange(idx * self.n_pos_bsz, (idx + 1) * self.n_pos_bsz)
                    % self.n_ir_samples
                )
                index_ir_for_batch = self.index_ir[ir_sel_indices]
                Xp_ir_batch = self.__ir_batch_load(index_ir_for_batch)

                # ir aug
                Xp_batch = ir_aug_batch(Xp_batch, Xp_ir_batch)

        Xa_batch = np.expand_dims(Xa_batch, 1).astype(np.float32)  # (n_anchor, 1, T)
        Xp_batch = np.expand_dims(Xp_batch, 1).astype(np.float32)  # (n_pos, 1, T)

        if self.return_song_name:
            if self.reduce_batch_first_half:
                return Xp_batch, [], name_batch
            else:
                return Xa_batch, Xp_batch, name_batch
        else:
            if self.reduce_batch_first_half:
                return Xp_batch, []  # Anchors will be reduced.
            else:
                return Xa_batch, Xp_batch

    def __event_batch_load(self, anchor_idx_list):
        """
        Get Xa_batch and Xp_batch for anchor (original)
        and positive (replica) samples.
        """
        Xa_batch = None
        Xp_batch = None
        name_batch = []
        for idx in anchor_idx_list:  # idx: index for one sample
            pos_start_sec_list = []
            # fns_event_seg_list =
            #   [[filename, seg_idx, offset_min, offset_max], [ ... ] , ... [ ... ]]
            offset_min, offset_max = (
                self.fns_event_seg_list[idx][2],
                self.fns_event_seg_list[idx][3],
            )
            anchor_offset_min = np.max([offset_min, -self.offset_margin_frame])
            anchor_offset_max = np.min([offset_max, self.offset_margin_frame])
            if (self.random_offset_anchor is True) & (self.experimental_mode is False):
                # Usually, we can apply random offset to anchor only in training.
                np.random.seed(idx)
                # Calculate anchor_start_sec
                _anchor_offset_frame = np.random.randint(
                    low=anchor_offset_min, high=anchor_offset_max
                )
                _anchor_offset_sec = _anchor_offset_frame / self.fs
                anchor_start_sec = (
                    self.fns_event_seg_list[idx][1] * self.hop + _anchor_offset_sec
                )
            else:
                _anchor_offset_frame = 0
                anchor_start_sec = self.fns_event_seg_list[idx][1] * self.hop
            """ Calculate multiple(=self.n_pos_per_anchor) pos_start_sec. """
            if self.n_pos_per_anchor > 0:
                pos_offset_min = np.max(
                    [(_anchor_offset_frame - self.offset_margin_frame), offset_min]
                )
                pos_offset_max = np.min(
                    [(_anchor_offset_frame + self.offset_margin_frame), offset_max]
                )
                if self.experimental_mode:
                    # In experimental_mode,
                    # we use a set of pre-defined offsets
                    # for multiple positive replicas...
                    _pos_offset_sec_list = (
                        self.experimental_mode_offset_sec_list
                    )  # [-0.2, -0.1,  0. ,  0.1,  0.2] for n_pos=5 with hop=0.5s
                    _pos_offset_sec_list[
                        (_pos_offset_sec_list < pos_offset_min / self.fs)
                    ] = (pos_offset_min / self.fs)
                    _pos_offset_sec_list[
                        (_pos_offset_sec_list > pos_offset_max / self.fs)
                    ] = (pos_offset_max / self.fs)
                    pos_start_sec_list = (
                        self.fns_event_seg_list[idx][1] * self.hop
                        + _pos_offset_sec_list
                    )
                else:
                    if pos_offset_min == pos_offset_max == 0:
                        # Only the case of running extras/dataset2wav.py
                        # as offset_margin_hot_rate=0
                        pos_start_sec_list = self.fns_event_seg_list[idx][1] * self.hop
                        pos_start_sec_list = [pos_start_sec_list]
                        # print('!!!!!!!!!!!!!!!!!!!!!!')
                        # print(pos_start_sec_list)
                        # print([anchor_start_sec])

                    else:
                        # Otherwise, we apply random offset to replicas
                        _pos_offset_frame_list = np.random.randint(
                            low=pos_offset_min,
                            high=pos_offset_max,
                            size=self.n_pos_per_anchor,
                        )
                        _pos_offset_sec_list = _pos_offset_frame_list / self.fs
                        pos_start_sec_list = (
                            self.fns_event_seg_list[idx][1] * self.hop
                            + _pos_offset_sec_list
                        )
            """
            load audio returns: [anchor, pos1, pos2,..pos_n]
            """
            # print(self.fns_event_seg_list[idx])
            start_sec_list = np.concatenate(([anchor_start_sec], pos_start_sec_list))
            xs = load_audio_multi_start(
                self.fns_event_seg_list[idx][0],
                start_sec_list,
                self.duration,
                self.fs,
                self.amp_mode,
            )  # xs: ((1+n_pos)),T)

            if Xa_batch is None:
                Xa_batch = xs[0, :].reshape((1, -1))
                Xp_batch = xs[
                    1:, :
                ]  # If self.n_pos_per_anchor==0: this produces an empty array
            else:
                Xa_batch = np.vstack(
                    (Xa_batch, xs[0, :].reshape((1, -1)))
                )  # Xa_batch: (n_anchor, T)
                Xp_batch = np.vstack((Xp_batch, xs[1:, :]))  # Xp_batch: (n_pos, T)
            name_batch.append(Path(self.fns_event_seg_list[idx][0]).stem)
        return Xa_batch, Xp_batch, name_batch

    def __bg_batch_load(self, idx_list):
        X_bg_batch = None  # (n_batch+n_batch//n_class, fs*k)
        random_offset_sec = (
            np.random.randint(0, self.duration * self.fs / 2, size=len(idx_list))
            / self.fs
        )
        for i, idx in enumerate(idx_list):
            idx = idx % self.n_bg_samples
            offset_sec = np.min(
                [random_offset_sec[i], self.fns_bg_seg_list[idx][3] / self.fs]
            )

            X = load_audio(
                filename=self.fns_bg_seg_list[idx][0],
                seg_start_sec=self.fns_bg_seg_list[idx][1] * self.duration,
                offset_sec=offset_sec,
                seg_length_sec=self.duration,
                seg_pad_offset_sec=0.0,
                fs=self.fs,
                amp_mode="normal",
            )

            X = X.reshape(1, -1)

            if X_bg_batch is None:
                X_bg_batch = X
            else:
                X_bg_batch = np.concatenate((X_bg_batch, X), axis=0)

        return X_bg_batch

    def __ir_batch_load(self, idx_list):
        X_ir_batch = None  # (n_batch+n_batch//n_class, fs*k)

        for idx in idx_list:
            idx = idx % self.n_ir_samples

            X = load_audio(
                filename=self.fns_ir_seg_list[idx][0],
                seg_start_sec=self.fns_ir_seg_list[idx][1] * self.duration,
                offset_sec=0.0,
                seg_length_sec=self.duration,
                seg_pad_offset_sec=0.0,
                fs=self.fs,
                amp_mode="normal",
            )
            if len(X) > MAX_IR_LENGTH:
                X = X[:MAX_IR_LENGTH]

            X = X.reshape(1, -1)

            if X_ir_batch is None:
                X_ir_batch = X
            else:
                X_ir_batch = np.concatenate((X_ir_batch, X), axis=0)

        return X_ir_batch
