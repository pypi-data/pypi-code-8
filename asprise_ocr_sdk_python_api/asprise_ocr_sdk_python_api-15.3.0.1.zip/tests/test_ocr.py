import unittest

from asprise_ocr_api import ocr


class Test(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.ocr = ocr.Ocr()

    def test_get_version(self):
        self.assertTrue(len(self.ocr.get_version()) > 0)

    def test_ocr(self):
        time_start = ocr.Ocr.get_time_tick()
        self.ocr.start_engine("eng")
        print("Time taken to start: %s " % (ocr.Ocr.get_time_tick() - time_start))
        time_start = ocr.Ocr.get_time_tick()
        s = self.ocr.recognize(
            "C:\\J\\dev-projects\\asprise\\ocr\\projects\\res\\image-processing\\deskew\\skewed.gif",
            ocr.OCR_PAGES_ALL, -1, -1, -1, -1, ocr.OCR_RECOGNIZE_TYPE_TEXT, ocr.OCR_OUTPUT_FORMAT_PDF,
            PROP_PDF_OUTPUT_FILE="C:\\J\\dev-projects\\asprise\\ocr\\projects\\res\\image-processing\\deskew\\out\\skewed.pdf",
            PROP_PDF_OUTPUT_TEXT_VISIBLE=True,
            PROP_OUTPUT_SEPARATE_WORDS=False,
            PROP_PDF_OUTPUT_RETURN_TEXT=ocr.OCR_OUTPUT_FORMAT_PLAINTEXT)
        print s
        print("Time taken to recognize: %s " % (ocr.Ocr.get_time_tick() - time_start))
        self.ocr.stop_engine()

if __name__ == '__main__':
    unittest.main()