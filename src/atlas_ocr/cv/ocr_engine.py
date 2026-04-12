from __future__ import annotations

import pytesseract


class OCREngine:
    def __init__(self, tesseract_cmd: str | None = None) -> None:
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def read_digits(self, image) -> str:
        config = "--psm 7 -c tessedit_char_whitelist=0123456789:"
        return pytesseract.image_to_string(image, config=config).strip()
