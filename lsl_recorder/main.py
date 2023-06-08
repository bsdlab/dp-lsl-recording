# import toml as tomllib
import tomllib
from pathlib import Path

from lsl_recorder.controller import LSLRecorderCom

cfg = tomllib.load(open("./configs/lsl_conf.toml", "rb"))


def init_lsl_recorder_com(
    lsl_recording_path: Path = Path(cfg["lsl_recording_path"]),
) -> LSLRecorderCom:
    return LSLRecorderCom(data_root=lsl_recording_path)
