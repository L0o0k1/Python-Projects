import cv2
import numpy as np
import imutils
import pytesseract
from tkinter import Tk, Button, Label, filedialog
from PIL import Image, ImageTk
from fpdf import FPDF
import os

def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped

def scan_document(image_path):
    image = cv2.imread(image_path)
    resized = imutils.resize(image, height=500)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)

    contours = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

        if len(approx) == 4:
            screenCnt = approx
            break

    warped = four_point_transform(resized, screenCnt.reshape(4, 2))

    warped_gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    T = cv2.adaptiveThreshold(warped_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(T)

    output_path = "scanned_document.jpg"
    cv2.imwrite(output_path, enhanced)

    return output_path

def extract_text(image_path):
    text = pytesseract.image_to_string(image_path, config='--psm 6')
    return text

def save_as_pdf(image_path, output_pdf):
    pdf = FPDF()
    pdf.add_page()
    pdf.image(image_path, x=10, y=10, w=190)
    pdf.output(output_pdf, "F")

class DocumentScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Document Scanner")
        self.root.geometry("400x300")

        self.label = Label(root, text="Select an image to scan")
        self.label.pack(pady=20)

        self.scan_button = Button(root, text="Scan Document", command=self.scan_document)
        self.scan_button.pack(pady=10)

        self.ocr_button = Button(root, text="Extract Text", command=self.extract_text)
        self.ocr_button.pack(pady=10)

        self.save_pdf_button = Button(root, text="Save as PDF", command=self.save_as_pdf)
        self.save_pdf_button.pack(pady=10)

        self.image_path = None
        self.scanned_image_path = None

    def scan_document(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
        if self.image_path:
            self.scanned_image_path = scan_document(self.image_path)
            self.label.config(text="Document scanned successfully!")

    def extract_text(self):
        if self.scanned_image_path:
            text = extract_text(self.scanned_image_path)
            print("Extracted Text:\n", text)
            self.label.config(text="Text extracted successfully!")
        else:
            self.label.config(text="Please scan a document first.")

    def save_as_pdf(self):
        if self.scanned_image_path:
            output_pdf = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
            if output_pdf:
                save_as_pdf(self.scanned_image_path, output_pdf)
                self.label.config(text="PDF saved successfully!")
        else:
            self.label.config(text="Please scan a document first.")

if __name__ == "__main__":
    root = Tk()
    app = DocumentScannerApp(root)
    root.mainloop()