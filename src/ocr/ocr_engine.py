import pytesseract
from pytesseract import Output
from PIL import Image, ImageEnhance, ImageFilter, UnidentifiedImageError
import os
import cv2
import numpy as np
import time
import logging

# Set log file path inside src/ocr directory
log_file_path = os.path.join(os.path.dirname(__file__), "ocr_engine.log")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler()
    ]
)

class OCREngine:
    def __init__(self, tesseract_cmd=None, lang='eng'):
        """
        Initialize the OCR engine.
        Args:
            tesseract_cmd (str): Optional path to tesseract executable.
            lang (str): Default language for OCR.
        """
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        self.default_lang = lang

    def preprocess_image(self, image_path):
        """
        Preprocess the image for better OCR accuracy.
        Steps: grayscale, denoise, threshold.

        Returns:
            PIL.Image: Preprocessed image object.
        """
        try:
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (3, 3), 0)
            _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            processed = Image.fromarray(thresh)
            logging.info("Image preprocessing completed.")
            return processed
        except Exception as e:
            logging.error(f"Preprocessing failed: {e}")
            raise

    def extract_text_from_image(self, image_path, lang=None, return_data=False, config="--psm 3"):
        """
        Extract text from an image using Tesseract OCR with preprocessing.

        Args:
            image_path (str): Path to the image.
            lang (str): Language(s) to use.
            return_data (bool): If True, return detailed data (bounding boxes).
            config (str): Custom tesseract config string.

        Returns:
            dict: {
                'success': bool,
                'text': str,
                'data': list of boxes (if return_data is True),
                'time': seconds,
                'error': str (if any)
            }
        """
        start_time = time.time()

        if not os.path.isfile(image_path):
            logging.warning(f"File not found: {image_path}")
            return {"success": False, "text": "", "error": f"File not found: {image_path}"}

        try:
            processed_img = self.preprocess_image(image_path)
            lang = lang or self.default_lang

            if return_data:
                ocr_data = pytesseract.image_to_data(
                    processed_img, lang=lang, config=config, output_type=Output.DICT
                )
                structured_text = "\n".join([
                    ocr_data['text'][i] for i in range(len(ocr_data['text']))
                    if int(ocr_data['conf'][i]) > 60 and ocr_data['text'][i].strip()
                ])
                elapsed = round(time.time() - start_time, 2)
                logging.info(f"OCR completed in {elapsed}s with structured output.")
                return {
                    "success": True,
                    "text": structured_text.strip(),
                    "data": ocr_data,
                    "time": elapsed
                }
            else:
                raw_text = pytesseract.image_to_string(processed_img, lang=lang, config=config)
                elapsed = round(time.time() - start_time, 2)
                logging.info(f"OCR completed in {elapsed}s with plain output.")
                return {
                    "success": True,
                    "text": raw_text.strip(),
                    "time": elapsed
                }

        except UnidentifiedImageError:
            logging.error("Invalid or corrupted image format.")
            return {"success": False, "text": "", "error": "Invalid or corrupted image format."}
        except Exception as e:
            logging.exception("OCR processing failed")
            return {"success": False, "text": "", "error": str(e)}
