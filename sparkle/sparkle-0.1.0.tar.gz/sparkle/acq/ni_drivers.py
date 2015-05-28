def able_to_record():
    '''Whether the current installation has the device drivers installed,
    and a phyiscal device available

    :returns: bool - True is system has ability to record from hardware
    '''
    import logging
    logger = logging.getLogger('main')
    try:
        from PyDAQmx import *

        buf = create_string_buffer(512)
        buflen = c_uint32(sizeof(buf))
        DAQmxGetSysDevNames(buf, buflen)
        pybuf = buf.value
        devices = pybuf.decode(u'utf-8').split(u",")

        if len(devices) > 0:
            logger.debug('Found physical recording device(s)')
            return True
        else:   
            logger.warning('Found device drivers, no physical devices present, running in development mode')
            return False
    except:

        logger.warning('Error importing device drivers, running in development mode')
        raise
        return False