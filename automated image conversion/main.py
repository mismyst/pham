import os
import cv2
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance
import numpy as np



class ImageSegmentationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("MRI Image Segmentation")

        self.image_label = Label(self.master)
        self.image_label.pack()

        self.filter_buttons_frame = Frame(self.master)
        self.filter_buttons_frame.pack()

        self.load_button = Button(self.filter_buttons_frame, text="Load Image", command=self.load_image)
        self.load_button.grid(row=0, column=0, padx=5, pady=5)

        self.filter_button = Button(self.filter_buttons_frame, text="Apply Filters", command=self.apply_filters)
        self.filter_button.grid(row=0, column=1, padx=5, pady=5)

        self.contrast_button = Button(self.filter_buttons_frame, text="Contrast Image", command=self.contrast_image)
        self.contrast_button.grid(row=0, column=2, padx=5, pady=5)

        self.segment_button = Button(self.filter_buttons_frame, text="Segment Image", command=self.segment_image)
        self.segment_button.grid(row=0, column=3, padx=5, pady=5)

        self.images = []
        self.filtered_images = []

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.bmp")])
        if file_path:
            image = Image.open(file_path)
            self.images.append(image)
            self.show_image(image)

    def show_image(self, image):
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo

    def apply_filters(self):
        if not self.images:
            return

        for image in self.images:
            # Apply filters to the image
            # Example: Use OpenCV to apply filters
            img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  # Convert PIL image to OpenCV format
            kernel = np.ones((5, 5), np.float32)/25
            filtered_image = cv2.filter2D(src=img, ddepth=-1, kernel=kernel)
            self.filtered_images.append(filtered_image)
            self.show_image(Image.fromarray(cv2.cvtColor(filtered_image, cv2.COLOR_BGR2RGB)))

    def contrast_image(self):
        if not self.images:
            return

        for image in self.images:
            # Contrast the image
            # Example: Modify image contrast using Pillow
            contrasted_image = ImageEnhance.Contrast(image).enhance(1.5)
            self.filtered_images.append(contrasted_image)
            self.show_image(contrasted_image)

    def segment_image(self):
        if not self.images:
            return

        for image in self.images:
            # Segment the image
            # Example: Implement your segmentation algorithm here
            img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  # Convert PIL image to OpenCV format
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
            self.filtered_images.append(img)
            self.show_image(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)))


def main():
    root = Tk()
    app = ImageSegmentationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()