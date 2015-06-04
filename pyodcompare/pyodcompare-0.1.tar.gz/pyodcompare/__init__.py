#!/usr/bin/env python

import os
import sys
import time

DEFAULT_OPENOFFICE_PORT = 2002


class DocumentCompareException(Exception):

    def _get_message(self):
        return self._message

    def _set_message(self, message):
        self._message = message

    message = property(_get_message, _set_message)


class DocumentCompare(object):

    def __init__(self, listener=('localhost', DEFAULT_OPENOFFICE_PORT)):
        import uno
        from com.sun.star.connection import NoConnectException
        from com.sun.star.uno import RuntimeException
        address, port = listener
        localContext = uno.getComponentContext()
        resolver = localContext.ServiceManager.createInstanceWithContext(
                            "com.sun.star.bridge.UnoUrlResolver", localContext)

        tries = 10
        while tries:
            try:
                self.context = resolver.resolve("uno:socket,host={0},port={1};urp;StarOffice.ComponentContext".format(address, port))
                break
            except (NoConnectException, RuntimeException):
                if tries > 0:
                    time.sleep(0.5)
                    if tries == 10:
                        sys.stdout.write("Wait connection to libreoffice")
                        sys.stdout.flush()
                    else:
                        sys.stdout.write(".")
                        sys.stdout.flush()
                    # wait soffice has been launched
                tries -= 1
        else:
            sys.stdout.write("\n")
            raise DocumentCompareException("failed to connect to LibreOffice on {0}:{1}".format(address, port))


        self.desktop = self.context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", self.context)
        self.servicemanager = self.context.ServiceManager

    def compare(self, path, original_path, save_path):
        import uno
        from com.sun.star.beans import PropertyValue
        if not os.path.exists(path):
            raise DocumentCompareException("%s does not exist" % (path,))

        url = uno.systemPathToFileUrl(path)
        if not os.path.exists(original_path):
            raise DocumentCompareException("%s does not exist" % (original_path,))

        url_original = uno.systemPathToFileUrl(original_path)
        url_save = uno.systemPathToFileUrl(save_path)

        ### Load document
        p = PropertyValue()
        p.Name = "Hidden"
        p.Value = True
        properties = (p,)

        doc = self.desktop.loadComponentFromURL(url, "_blank", 0, properties)

        ### Compare with original document
        properties = []
        p = PropertyValue()
        p.Name = "URL"
        p.Value = url_original
        properties.append(p)
        properties = tuple(properties)

        dispatch_helper = self.servicemanager.createInstanceWithContext(
                                            "com.sun.star.frame.DispatchHelper",
                                            self.context)
        dispatch_helper.executeDispatch(doc.getCurrentController().getFrame(),
                                        ".uno:CompareDocuments", "",
                                        0, properties)

        ### Save File
        p = PropertyValue()
        p.Name = "Overwrite"
        p.Value = True
        properties = (p,)

        doc.storeToURL(url_save, properties)
        doc.dispose()
