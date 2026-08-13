from dareplane_utils.default_server.server import DefaultServer
from fire import Fire

from lsl_recorder.controller import LSLRecorderCom
from lsl_recorder.lab_recorder import initialize_lab_recorder
from lsl_recorder.utils.logging import logger


def main(
    port: int = 8080, ip: str = "127.0.0.1", loglevel: int = 10, LSL_port: int = 22345
):
    logger.setLevel(loglevel)

    # Initialize LabRecorder
    logger.debug("Starting LabRecorder and initializing connection")
    try:
        # Try to connect to LabRecorder, if it is not running, start it and then connect
        lsl_conn = initialize_lab_recorder(LSL_port=LSL_port)
        lsl_comm: LSLRecorderCom = lsl_conn.communicator

    except Exception as e:
        logger.error(f"Failed to initialize LabRecorder: {e}")
        raise RuntimeError(
            "Failed to initialize LabRecorder automatically. Please ensure it is running and accessible."
        ) from e

    logger.debug("Linking PCOMMS")
    pcommand_map = {
        "SELECT_ALL": lsl_comm.select_all,
        "SET_SAVE_PATH": lsl_comm.set_recording_file,
        "UPDATE": lsl_comm.update,
        "RECORD": lsl_comm.record,
        "STOPRECORD": lsl_comm.stop,
    }

    server = DefaultServer(
        port, ip=ip, pcommand_map=pcommand_map, name="lsl_control_server", logger=logger
    )

    # initialize to start the socket
    logger.debug("Initializing DefaultServer")
    server.init_server()
    # start processing of the server
    logger.debug("receiving connections")
    server.start_listening()

    return 0


if __name__ == "__main__":
    Fire(main)
