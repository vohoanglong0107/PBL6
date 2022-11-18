from loguru import logger
from tqdm import tqdm


class logging_tqdm(tqdm):
    def __init__(
        self,
        *args,
        logger=logger,
        mininterval: float = 1,
        bar_format: str = "{desc}{percentage:3.0f}%{r_bar}",
        desc: str = "progress: ",
        **kwargs,
    ):
        self._logger = logger
        super().__init__(
            *args,
            mininterval=mininterval,
            bar_format=bar_format,
            desc=desc,
            **kwargs,
        )

    @property
    def logger(self):
        if self._logger is None:
            return self._logger
        return logger

    def display(self, msg=None, pos=None):
        if not msg:
            msg = self.__str__()
        self.logger.info(msg)
