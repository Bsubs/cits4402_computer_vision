# Joo Kai Tay, 22489437, Week 5 Lab04
# There are two edge detection techniques bring used, Canny and Sobel to identify step discontinuities in the image as edges
# The threshold determines the edges detected. The lower the threshold, the more edges detected but is more susceptible to noise
# A higher threshold means less noise but may result in fragmented edges or missing edges altogether
# The circle is detected by a Hough Transform. It finds imperfect instances of objects within a class of objects by a voting procedure
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import numpy as np
import cv2
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.draw import circle_perimeter

class ImageGUI:
    # Size of the GUI
    maxsize=500
   
    def __init__(self, master):
        self.master = master
        self.master.title("Image GUI")

        # Create a frame for the GUI and center it
        self.frame = tk.Frame(self.master)
        self.frame.pack(expand=True, padx=10, pady=10)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # Create a border for the GUI
        self.border = tk.Frame(self.frame, borderwidth=2, relief="groove")
        self.border.grid(row=0, column=0, sticky="nsew")

        # Create a "Load Image" button
        self.load_button = tk.Button(self.border, text="Load Image", command=self.load_image)
        self.load_button.grid(column=0, row=1, padx=5, pady=5)
        # Create a label to display the chosen image
        self.image_label = tk.Label(self.border)
        self.image_label.grid(column=0, row=0, padx=5, pady=5)

        # Create a label to display the filtered image
        self.filtered_label = tk.Label(self.border)
        self.filtered_label.grid(column=3, row=0, padx=5, pady=5)

        # Create detect edge button
        self.detect_edge = tk.Button(self.border, text="Detect Edge", command=self.detect_edges)
        self.detect_edge.grid(column=1, row = 1, padx=5, pady=5)

        # Create edge detection drop down menu
        self.algo = tk.StringVar(self.border)
        self.algo.set("canny") # default value
        self.algo_select = tk.OptionMenu(self.border, self.algo, "sobel", "canny")
        self.algo_select.grid(column=1, row=2, padx=5, pady=5)

        # Create edge detection threshold slider widget
        self.edge_detection_slider = tk.Scale(self.border, label='Threshold for edge detection', from_=0, to=255, orient=tk.HORIZONTAL, length=255, showvalue=0, command=self.detect_edges)
        self.edge_detection_slider.set('127')
        self.edge_detection_slider.grid(column=3, row=1, padx=5, pady=5) 

        # Create circle detection radius slider widget
        self.circle_detection_slider = tk.Scale(self.border, label='Approximate Radius for circle detection', from_=25, to=80, orient=tk.HORIZONTAL, length=255, showvalue=0, command=self.draw_circles)
        self.circle_detection_slider.set('0')
        self.circle_detection_slider.grid(column=3, row=2, padx=5, pady=5) 




    def load_image(self):
        # Open a file selection dialog box to choose an image file
        file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])

        # Load the chosen image using PIL
        self.original_image = Image.open(file_path)
        np_image = np.array(self.original_image)

        # Placeholder for global variable holding the filtered image
        self.filtered_image = 0

        # Convert the image back to PIL format
        pil_image = Image.fromarray(np_image)

        # Resize the image to fit in the label
        width, height = pil_image.size
        max_size = self.maxsize
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_width = int(width * (max_size / height))
            new_height = max_size
        pil_image = pil_image.resize((new_width, new_height))

        # Convert the image to Tkinter format and display it on the left side
        photo = ImageTk.PhotoImage(pil_image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo

    def detect_edges(self, _event=None):
        # Convert the original image to grayscale
        original_image = self.original_image
        grayscale_image = original_image.convert('L')
        np_image = np.array(grayscale_image)

        # Get the threshold value from slider widget (default = 127)
        thresh_val = self.edge_detection_slider.get()
        # threshold the image using the value (default = 127)
        ret, threshold_img = cv2.threshold(np_image, thresh_val, 255, cv2.THRESH_BINARY)

        # do edge detection using algo from the drop down menu
        if self.algo.get() == 'canny':
            edge_detected = cv2.Canny(image=threshold_img, threshold1=100, threshold2=200)
        elif self.algo.get() == 'sobel':
            grad_x = cv2.Sobel(threshold_img, cv2.CV_64F, 1, 0)
            grad_y = cv2.Sobel(threshold_img, cv2.CV_64F, 0, 1)
            edge_detected = np.sqrt(grad_x**2 + grad_y**2)
        
        # Update the global variable 
        self.filtered_image = edge_detected
        # Convert the image back to PIL format
        pil_image = Image.fromarray(edge_detected)

        # Resize the image to fit in the label
        width, height = pil_image.size
        max_size = self.maxsize
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_width = int(width * (max_size / height))
            new_height = max_size
        pil_image = pil_image.resize((new_width, new_height))

        # Convert the image to Tkinter format and display it on the right side
        photo = ImageTk.PhotoImage(pil_image)
        self.filtered_label.configure(image=photo)
        self.filtered_label.image = photo


    def draw_circles(self, _event=None):

        # retrive the original and edge detected image from global variables
        original_img = np.array(self.original_image)
        grayscale_image = np.array(self.original_image.convert('L'))
        edge_img = np.array(self.filtered_image)

        # Get the approximate radius value from slider widget (default = 25)
        radius = self.circle_detection_slider.get()
        # Apply Hough transform to image
        edge_img = np.uint8(edge_img)
        # Radii to try 
        try_radii = np.arange(radius, radius+1)
        hough_res= hough_circle(edge_img.astype(dtype=bool), try_radii)
        accums, cx,cy,radii = hough_circle_peaks(hough_res, try_radii,threshold=0.25 ,min_xdistance=radius*3, min_ydistance=radius*3, total_num_peaks=2)

        # Convert thresholded image to RBG to allow for plotting of coloured circles
        coloured_image = Image.fromarray(edge_img)
        coloured_image = np.array(coloured_image.convert('RGB'))

        # Draw the circles
        if radii is not None:
            for center_x, center_y, radius in zip(cx,cy,radii):
                # draw the outer circle
                cv2.circle(original_img,(center_x, center_y),radius,(0,255,0),2)
                # draw the center of the circle
                cv2.circle(original_img,(center_x, center_y),2,(0,0,255),3)
            
            for center_x, center_y, radius in zip(cx,cy,radii):
                # draw the outer circle
                cv2.circle(coloured_image,(center_x, center_y),radius,(0,255,0),2)
                # draw the center of the circle
                cv2.circle(coloured_image,(center_x, center_y),2,(0,0,255),3)

        pil_image = Image.fromarray(original_img)
        # Resize the image to fit in the label
        width, height = pil_image.size
        max_size = self.maxsize
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_width = int(width * (max_size / height))
            new_height = max_size
        pil_image = pil_image.resize((new_width, new_height))

        # Convert the image to Tkinter format and display it on the left side
        photo = ImageTk.PhotoImage(pil_image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo

        pil_image = Image.fromarray(coloured_image)
        # Resize the image to fit in the label
        width, height = pil_image.size
        max_size = self.maxsize
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_width = int(width * (max_size / height))
            new_height = max_size
        pil_image = pil_image.resize((new_width, new_height))

        # Convert the image to Tkinter format and display it on the right side
        photo = ImageTk.PhotoImage(pil_image)
        self.filtered_label.configure(image=photo)
        self.filtered_label.image = photo



        
            
if __name__ == "__main__":
    root = tk.Tk()
    gui = ImageGUI(root)
    root.mainloop()
