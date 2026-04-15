#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# date: 20210505
#
# Recorder for collecting lsl streams store to a file
# We use the TCP API for the LSL APP-LabRecorder
# https://github.com/labstreaminglayer/App-LabRecorder

import time
from pathlib import Path

from dareplane_utils.module_handling.communication import SocketCommunicator

from lsl_recorder.utils.logging import logger


class LSLRecorderCom(SocketCommunicator):
    """Communication object to use TCP API of LSL APP-LabRecorder"""

    def __init__(
        self, name: str, data_root: Path = Path("."), addr="localhost", port=22345
    ):
        super().__init__(name=name, ip=addr, port=port)
        self._data_root = data_root

    def select_all(self):
        self.send(b"select all\n")
        return 0

    def set_recording_file(
        self,
        fname: str,
        data_root: str | Path | None = None,
        overwrite: bool = False,
    ):
        self.update()
        time.sleep(2)

        data_root = Path(data_root)  # make sure it is a Path

        if data_root is not None:
            logger.debug(f"Overwriting data root for lsl recorder to: {data_root}")
            self._data_root = data_root

        # Increment with time if already exists

        fname = self._data_root.joinpath(f"{fname}.xdf")
        if fname.exists() and not overwrite:
            # find latest suffix and add next
            fname = fname.parent.joinpath(
                fname.stem + "_" + time.strftime("%Y%m%d%H%M%S") + fname.suffix
            )

        msg = f"filename {{root:{fname.parent}}} {{template:{fname.stem + fname.suffix}}}\n"
        self.send(msg.encode("UTF-8"))
        time.sleep(1)
        return 0

    def update(self):
        self.send(b"update\n")
        return 0

    def record(self):
        self.send(b"start\n")
        return 0

    def stop(self):
        self.send(b"stop\n")
        time.sleep(5)
        return 0


if __name__ == "__main__":
    communicator = LSLRecorderCom()

    communicator.set_recording_file("testfile", data_root=Path("D:/"))

    communicator.record()
    time.sleep(3)
    communicator.stop()
