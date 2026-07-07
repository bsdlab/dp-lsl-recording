# LSL Recording

This a convenient wrapper, bridging to control the [LSL](https://labstreaminglayer.org/#/) [LabRecorder](https://github.com/labstreaminglayer/App-LabRecorder) via a Dareplane API server.

This module automatically launches [`LSL LabRecorder`](https://github.com/labstreaminglayer/App-LabRecorder) during startup, or connects to a running instance if it exists.

Please be referred to the [`dp-strawman-module`](https://github.com/bsdlab/dp-strawman-module) for a general introduction of how modules are structured and to the [`dp-control-room`](https://github.com/bsdlab/dp-control-room) for how modules are composed to full systems.

## Test the module

For testing the functionality of the module with your OS and libraries, first start the LabRecorder, then spawn the server by using `python -m api.server`. Login via `telnet 127.0.0.1 8080` and try to send the primary commands as specified in `./api/server.py`. E.g. `RECORD` or `STOPRECORD`.
