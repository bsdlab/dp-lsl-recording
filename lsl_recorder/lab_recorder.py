import os
from pathlib import Path

from dareplane_utils.module_handling.launcher import ExeLauncher
from dareplane_utils.module_handling.module_connection import ModuleConnection

from lsl_recorder.controller import LSLRecorderCom
from lsl_recorder.utils.logging import logger


def initialize_lab_recorder(LSL_port: int) -> ModuleConnection:
    launcher = ExeLauncher(exe_path=find_lab_recorder_executable())
    communicator = LSLRecorderCom(name="LabRecorder", addr="localhost", port=LSL_port)
    connection = ModuleConnection(
        name="LabRecorder", launcher=launcher, communicator=communicator
    )

    try:
        communicator.connect()
        logger.info("Labrecorder already running, connected successfully.")
    except Exception:
        # Start the LabRecorder and establish communication
        connection.start(env=create_clean_env())
    return connection


def find_lab_recorder_executable():
    """Find the LabRecorder executable in common installation paths."""
    possible_paths = [
        "C:\\Program Files\\LabRecorder\\LabRecorder.exe",  # Windows default path
        "/Applications/LabRecorder.app/Contents/MacOS/LabRecorder",  # macOS default path
        "/usr/bin/LabRecorder",  # Common Linux path
    ]
    for path in possible_paths:
        if Path(path).exists():
            return path
    logger.error(
        "LabRecorder executable not found. Please check the installation path."
    )
    raise FileNotFoundError(
        "LabRecorder executable not found and can not be started. Please launch it manually and ensure it is running before starting the server."
    )


def create_clean_env():
    """Create a clean environment for launching LabRecorder, removing variables that can cause conflicts."""
    env = os.environ.copy()

    # Remove snap-related environment variables that can cause conflicts
    snap_vars_to_remove = ["GTK_PATH"]
    for var in snap_vars_to_remove:
        env.pop(var, None)

    return env
