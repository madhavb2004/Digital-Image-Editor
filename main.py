from io import BytesIO
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk, ImageEnhance, ImageFilter, ImageOps, ImageDraw
import customtkinter
import numpy as np


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")


app = customtkinter.CTk()
app.geometry("1280x720")
app.title("PhotoEdit")
app.iconbitmap("Digital Image Editor/icon.ico")


current_image = None
original_image = None
label_image = None
brightness_value = 1.0
saturation_value = 1.0
highlights_value = 1.0
exposure_value = 1.0
contrast_value = 1.0
selected_effect = ""
compression_on = False


def toggle_compression():
    global compression_on
    compression_on = not compression_on
    print("Compression:", "On" if compression_on else "Off")


def import_image_and_display():
    global current_image, original_image, label_image, brightness_value, saturation_value
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")])
    if file_path:
        for widget in app.winfo_children():
            widget.destroy()

        image = Image.open(file_path)
        image = image.resize((800, 800))
        current_image = image.copy()
        original_image = image.copy()
        photo = ImageTk.PhotoImage(image)

        label_image = tk.Label(app, image=photo)
        label_image.photo = photo
        label_image.pack(side="right", padx=10, pady=10)

        tabview = customtkinter.CTkTabview(master=app)
        tabview.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        tabview.add("Position")
        tabview.add("Color")
        tabview.add("Effects")
        tabview.add("Export")
        tabview.set("Color")

 
        blur_effect_button = customtkinter.CTkButton(tabview.tab("Effects"), text="Blur Effect", command=apply_blur_effect)
        blur_effect_button.pack(padx=20, pady=10)

        sepia_effect_button = customtkinter.CTkButton(tabview.tab("Effects"), text="Sepia Effect", command=apply_sepia_effect)
        sepia_effect_button.pack(padx=20, pady=10)

        bw_effect_button = customtkinter.CTkButton(tabview.tab("Effects"), text="Black & White Effect", command=apply_bw_effect)
        bw_effect_button.pack(padx=20, pady=10)

        hdr_effect_button = customtkinter.CTkButton(tabview.tab("Effects"), text="HDR Effect", command=apply_hdr_effect)
        hdr_effect_button.pack(padx=20, pady=10)

        grayscale_effect_button = customtkinter.CTkButton(tabview.tab("Effects"), text="Grayscale Effect", command=apply_grayscale_effect)
        grayscale_effect_button.pack(padx=20, pady=10)

        invert_effect_button = customtkinter.CTkButton(tabview.tab("Effects"), text="Invert Effect", command=apply_invert_effect)
        invert_effect_button.pack(padx=20, pady=10)

        sharpen_effect_button = customtkinter.CTkButton(tabview.tab("Effects"), text="Sharpen Effect", command=apply_sharpen_effect)
        sharpen_effect_button.pack(padx=20, pady=10)

        emboss_effect_button = customtkinter.CTkButton(tabview.tab("Effects"), text="Emboss Effect", command=apply_emboss_effect)
        emboss_effect_button.pack(padx=20, pady=10)

        smooth_effect_button = customtkinter.CTkButton(tabview.tab("Effects"), text="Smooth Effect", command=apply_smooth_effect)
        smooth_effect_button.pack(padx=20, pady=10)

        export_button = customtkinter.CTkButton(tabview.tab("Export"), text="Export Image", command=export_image)
        export_button.pack(padx=20, pady=250)

        compress_button = customtkinter.CTkButton(tabview.tab("Export"), text="Compress", command=toggle_compression)
        compress_button.pack(side="bottom", padx=10, pady=10)

        revert_button = customtkinter.CTkButton(tabview.tab("Effects"), text="Revert", command=revert_image)
        revert_button.pack(side="bottom", padx=10, pady=10)

        rotate_label = customtkinter.CTkLabel(tabview.tab("Position"), text="Rotate", font=("Helvetica", 16))
        rotate_label.pack(padx=20, pady=10)


        def rotate_90_degrees():
            global current_image
            current_image = current_image.rotate(90)
            apply_brightness_and_saturation()

        rotate_90_button = customtkinter.CTkButton(tabview.tab("Position"), text="90 Degrees", command=rotate_90_degrees)
        rotate_90_button.pack(padx=20, pady=5)

        def rotate_180_degrees():
            global current_image
            current_image = current_image.rotate(180)
            apply_brightness_and_saturation()

        rotate_180_button = customtkinter.CTkButton(tabview.tab("Position"), text="180 Degrees", command=rotate_180_degrees)
        rotate_180_button.pack(padx=20, pady=5)

        brightness_label = customtkinter.CTkLabel(tabview.tab("Color"), text="Brightness", font=("Helvetica", 16))
        brightness_label.pack(padx=20, pady=10)

        brightness_slider = customtkinter.CTkSlider(tabview.tab("Color"), from_=0, to=200, command=brightness_slider_event)
        brightness_slider.set(brightness_value * 100)
        brightness_slider.pack(padx=20, pady=20)

        saturation_label = customtkinter.CTkLabel(tabview.tab("Color"), text="Saturation", font=("Helvetica", 16))
        saturation_label.pack(padx=20, pady=10)

        saturation_slider = customtkinter.CTkSlider(tabview.tab("Color"), from_=0, to=200, command=saturation_slider_event)
        saturation_slider.set(saturation_value * 100)
        saturation_slider.pack(padx=20, pady=20)

        highlights_label = customtkinter.CTkLabel(tabview.tab("Color"), text="Highlights", font=("Helvetica", 16))
        highlights_label.pack(padx=20, pady=10)

        highlights_slider = customtkinter.CTkSlider(tabview.tab("Color"), from_=0, to=200, command=highlights_slider_event)
        highlights_slider.set(highlights_value * 100)
        highlights_slider.pack(padx=20, pady=20)

        exposure_label = customtkinter.CTkLabel(tabview.tab("Color"), text="Exposure", font=("Helvetica", 16))
        exposure_label.pack(padx=20, pady=10)

        exposure_slider = customtkinter.CTkSlider(tabview.tab("Color"), from_=0, to=200, command=exposure_slider_event)
        exposure_slider.set(exposure_value * 100)
        exposure_slider.pack(padx=20, pady=20)

        contrast_label = customtkinter.CTkLabel(tabview.tab("Color"), text="Contrast", font=("Helvetica", 16))
        contrast_label.pack(padx=20, pady=10)

        contrast_slider = customtkinter.CTkSlider(tabview.tab("Color"), from_=0, to=200, command=contrast_slider_event)
        contrast_slider.set(contrast_value * 100)
        contrast_slider.pack(padx=20, pady=20)

        apply_brightness_and_saturation()

def apply_brightness_and_saturation():
    global current_image, original_image, brightness_value, saturation_value, highlights_value, exposure_value, contrast_value
    enhanced_image = original_image.copy()
    enhanced_image = ImageEnhance.Brightness(enhanced_image).enhance(brightness_value)
    enhanced_image = ImageEnhance.Color(enhanced_image).enhance(saturation_value)
    enhanced_image = ImageEnhance.Brightness(enhanced_image).enhance(highlights_value)
    enhanced_image = ImageEnhance.Contrast(enhanced_image).enhance(contrast_value)

    
    gamma = 1.0 / exposure_value 
    adjusted_pixels = adjust_exposure(enhanced_image, gamma)
    enhanced_image = Image.fromarray(adjusted_pixels)

    update_displayed_image(enhanced_image)

def adjust_exposure(image, gamma):
    pixels = np.array(image)
    adjusted_pixels = 255 * (pixels / 255) ** gamma
    adjusted_pixels = np.clip(adjusted_pixels, 0, 255)
    adjusted_pixels = adjusted_pixels.astype(np.uint8)
    return adjusted_pixels



def update_displayed_image(image):
    photo = ImageTk.PhotoImage(image)
    label_image.config(image=photo)
    label_image.photo = photo


def brightness_slider_event(value):
    global brightness_value
    brightness_value = float(value) / 100.0
    apply_brightness_and_saturation()

def saturation_slider_event(value):
    global saturation_value
    saturation_value = float(value) / 100.0
    apply_brightness_and_saturation()

def highlights_slider_event(value):
    global highlights_value
    highlights_value = float(value) / 100.0
    apply_brightness_and_saturation()

def exposure_slider_event(value):
    global exposure_value
    exposure_value = float(value) / 100.0
    apply_brightness_and_saturation()

def contrast_slider_event(value):
    global contrast_value
    contrast_value = float(value) / 100.0
    apply_brightness_and_saturation()


def revert_image():
    global current_image, original_image, selected_effect
    current_image = original_image.copy()
    selected_effect = "" 
    update_displayed_image(current_image) 


def export_image():
    global current_image, brightness_value, saturation_value, selected_effect, compression_on
    if current_image:
        if selected_effect:
            if selected_effect == "Blur Effect":
                current_image = current_image.filter(ImageFilter.GaussianBlur(radius=2))
            elif selected_effect == "Sepia Effect":
                current_image = ImageOps.colorize(current_image.convert('L'), "#704214", "#C0C090")
            elif selected_effect == "Black & White Effect":
                current_image = current_image.convert("L")
            elif selected_effect == "HDR Effect":
                current_image = ImageEnhance.Contrast(current_image).enhance(1.5)
        elif brightness_value != 1.0 or saturation_value != 1.0:  
            enhanced_image = current_image.copy()
            enhanced_image = ImageEnhance.Brightness(enhanced_image).enhance(brightness_value)
            enhanced_image = ImageEnhance.Color(enhanced_image).enhance(saturation_value)
            current_image = enhanced_image
       
        if compression_on:
            compressed_image = compress_image(current_image, compression_factor=0.8)  
        else:
            compressed_image = current_image
        
    
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[
            ("JPEG files", "*.jpg"),
            ("PNG files", "*.png"),
            ("Bitmap files", "*.bmp"),
            ("All files", "*.*")
        ])
        if file_path:
            compressed_image.save(file_path)
    else:
        messagebox.showerror("Error", "No image to export.")


def set_selected_effect(effect):
    global selected_effect
    selected_effect = effect

# EFFECTS
def apply_effect(effect):
    global current_image
    if current_image:
        if effect == "Blur Effect":
            current_image = current_image.filter(ImageFilter.GaussianBlur(radius=2))
        elif effect == "Sepia Effect":
            current_image = ImageOps.colorize(current_image.convert('L'), "#704214", "#C0C090")
        elif effect == "Black & White Effect":
            current_image = current_image.convert("L")
        elif effect == "HDR Effect":
            current_image = ImageEnhance.Contrast(current_image).enhance(1.5)
        apply_brightness_and_saturation()

def apply_blur_effect():
    global current_image, selected_effect
    selected_effect = "Blur Effect"  
    print("Selected effect:", selected_effect)  
    if current_image:
        blurred_image = current_image.filter(ImageFilter.GaussianBlur(radius=2))
        update_displayed_image(blurred_image)

def apply_sepia_effect():
    global current_image, selected_effect
    selected_effect = "Sepia Effect"  
    print("Selected effect:", selected_effect)  
    if current_image:
        sepia_image = ImageOps.colorize(current_image.convert('L'), "#704214", "#C0C090")
        update_displayed_image(sepia_image)

def apply_bw_effect():
    global current_image, selected_effect
    selected_effect = "Black & White Effect"  
    print("Selected effect:", selected_effect)  
    if current_image:
        bw_image = current_image.convert("L")
        update_displayed_image(bw_image)

def apply_hdr_effect():
    global current_image, selected_effect
    selected_effect = "HDR Effect"  
    print("Selected effect:", selected_effect)  
    if current_image:
        hdr_image = ImageEnhance.Contrast(current_image).enhance(1.5)
        update_displayed_image(hdr_image)

def apply_grayscale_effect():
    global current_image, selected_effect
    selected_effect = "Grayscale Effect"
    print("Selected effect:", selected_effect)
    if current_image:
        grayscale_image = current_image.convert("L")
        update_displayed_image(grayscale_image)

def apply_invert_effect():
    global current_image, selected_effect
    selected_effect = "Invert Effect"
    print("Selected effect:", selected_effect)
    if current_image:
        invert_image = ImageOps.invert(current_image)
        update_displayed_image(invert_image)

def apply_sharpen_effect():
    global current_image, selected_effect
    selected_effect = "Sharpen Effect"
    print("Selected effect:", selected_effect)
    if current_image:
        sharpen_image = current_image.filter(ImageFilter.SHARPEN)
        update_displayed_image(sharpen_image)

def apply_emboss_effect():
    global current_image, selected_effect
    selected_effect = "Emboss Effect"
    print("Selected effect:", selected_effect)
    if current_image:
        emboss_image = current_image.filter(ImageFilter.EMBOSS)
        update_displayed_image(emboss_image)


def apply_smooth_effect():
    global current_image, selected_effect
    selected_effect = "Smooth Effect"
    print("Selected effect:", selected_effect)
    if current_image:
        smooth_image = current_image.filter(ImageFilter.SMOOTH)
        update_displayed_image(smooth_image)

def compress_image(image, compression_factor=0.5):
    quality = int(100 * (1 - compression_factor))
    

    buffered = BytesIO()
    image.save(buffered, format="JPEG", quality=quality)
    buffered.seek(0)
    compressed_image = Image.open(buffered)
    
    return compressed_image


import_button = customtkinter.CTkButton(app, text="Import Image", command=import_image_and_display)
import_button.place(relx=0.5, rely=0.5, anchor="center")

app.mainloop()
