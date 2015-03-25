# Setup fedmsg logging.
# See the following for constraints on this format http://bit.ly/Xn1WDn
config = dict(
    logging=dict(
        version=1,
        formatters=dict(
            bare={
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "format": "[%(asctime)s][%(name)10s %(levelname)7s] %(message)s"
            },
        ),
        handlers=dict(
            console={
                "class": "logging.StreamHandler",
                "formatter": "bare",
                "level": "DEBUG",
                "stream": "ext://sys.stdout",
            }
        ),
        loggers=dict(
            fedmsg={
                "level": "DEBUG",
                "propagate": False,
                "handlers": ["console"],
            },
            moksha={
                "level": "DEBUG",
                "propagate": False,
                "handlers": ["console"],
            },
        ),
    ),
)
