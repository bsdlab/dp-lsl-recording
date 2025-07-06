#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# date: 20210505
#
# Recorder for collecting lsl streams store to a file
# We use the TCP API for the LSL APP-LabRecorder
# https://github.com/labstreaminglayer/App-LabRecorder

import socket
import time
from pathlib import Path

from lsl_recorder.utils.logging import logger


class LSLRecorderCom(object):
    """Class to communicate with LSL [LabRecorder](https://github.com/labstreaminglayer/App-LabRecorder) via TCP commands.
    
    This class provides a wrapper to communicate with the LSL [LabRecorder](https://github.com/labstreaminglayer/App-LabRecorder)
    application via TCP commands using a Dareplane server. This allows you to set the recording location,
    start and stop the recording via the Dareplane control room.
    
    The LSL LabRecorder application must be running separately and listening
    on the specified TCP port before creating an instance of this class.
    
    Parameters
    ----------
    data_root : Path, optional
        Root directory for saving recorded data files, by default Path(".")
    addr : str, optional
        IP address of the LSL LabRecorder TCP server
    port : int, optional
        Port number of the LSL LabRecorder TCP serve
    """

    def __init__(
        self, data_root: Path = Path("."), addr="localhost", port=22345
    ):
        """Initialize the LSLRecorderCom class with the approrpiate parameters."""
        self._addr = addr
        self._port = port
        self._data_root = data_root

        self._data_root.mkdir(exist_ok=True, parents=True)

        self._socket = socket.create_connection((self._addr, self._port))

    def select_all(self):
        self._socket.sendall(b"select all\n")
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
            logger.debug(
                f"Overwriting data root for lsl recorder to: {data_root}"
            )
            self._data_root = data_root

        # Increment with time if already exists

        fname = self._data_root.joinpath(f"{fname}.xdf")
        if fname.exists() and not overwrite:
            # find latest suffix and add next
            fname = fname.parent.joinpath(
                fname.stem + "_" + time.strftime("%Y%m%d%H%M%S") + fname.suffix
            )

        msg = f"filename {{root:{fname.parent}}} {{template:{fname.stem + fname.suffix}}}\n"
        self._socket.sendall(msg.encode("UTF-8"))
        time.sleep(1)
        return 0

    def update(self):
        self._socket.sendall(b"update\n")
        return 0

    def record(self):
        self._socket.sendall(b"start\n")
        return 0

    def stop(self):
        ret = self._socket.sendall(b"stop\n")
        time.sleep(5)
        return 0


if __name__ == "__main__":
    communicator = LSLRecorderCom()

    communicator.set_recording_file("testfile", data_root=Path("D:/"))

    communicator.record()
    time.sleep(3)
    communicator.stop()
