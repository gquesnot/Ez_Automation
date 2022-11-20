import pytesseract

from util.pixel import apply_region, apply_save, perform_ocr

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'


class Tcr:
    def __init__(self, game):
        self.game = game
        self.text_config = r'-l eng --tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata" --oem 3 --psm 8'
        self.number_config = r'--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata" --psm 6 outputbase digits'

    def init_scan(self, region, save):
        img = self.game.screen_shot
        img = apply_region(img, region)
        apply_save(img, save)
        return img

    def scan_text(self, region=None, save=None, img=None):
        if img is None:
            img = self.init_scan(region, save)
        else:
            img = perform_ocr(img)
        text = pytesseract.image_to_string(img, config=self.text_config).replace("\n", "").replace("\x0c", "")
        return img, text

    def scan_number(self, region=None, save=None, img=None, max_digit=None):
        if img is None:
            img = self.init_scan(region, save)
        else:
            img = perform_ocr(img)
        text = pytesseract.image_to_string(img, config=self.number_config) \
            .replace("\n", "") \
            .replace("\x0c", "") \
            .replace(" ", "")
        if max_digit is not None:
            if len(text) > max_digit:
                text = text[:2]

        if text == "":
            return None, None
        return img, int(text)
