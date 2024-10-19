import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk


def adjust_contrast():
    # Get current values from sliders
    alpha = alpha_scale.get()  # Contrast control
    beta = beta_scale.get()  # Brightness control

    # Apply contrast adjustment
    adjusted_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

    # Display adjusted image
    cv2.imshow('Adjusted Image', adjusted_image)
    cv2.waitKey(1)


# Load the image
image = cv2.imread('mobs/human/health_area.png')

# Create a Tkinter window
root = tk.Tk()
root.title("Contrast Adjustment")

# Create sliders for alpha (contrast) and beta (brightness)
alpha_label = ttk.Label(root, text="Alpha (Contrast)")
alpha_label.pack()
alpha_scale = ttk.Scale(root, from_=0, to=3, orient=tk.HORIZONTAL)
alpha_scale.pack()

beta_label = ttk.Label(root, text="Beta (Brightness)")
beta_label.pack()
beta_scale = ttk.Scale(root, from_=-100, to=100, orient=tk.HORIZONTAL)
beta_scale.pack()

# Button to apply contrast adjustment
adjust_button = ttk.Button(root, text="Adjust Contrast", command=adjust_contrast)
adjust_button.pack()

# Start the Tkinter event loop
root.mainloop()
