import rpipe.config.heartbeat

WATCH_LOOP_INTERVAL_S = 1
DEFAULT_WATCH_WAIT_TIMEOUT_S = 5
UNHANDLED_EVENT_DEFAULT_RESULT_CODE = 255
MESSAGE_LOOP_READ_TIMEOUT_S = 1

WRITE_TIMEOUT_S = rpipe.config.heartbeat.HEARTBEAT_INTERVAL_S * 2
