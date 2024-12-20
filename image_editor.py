import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter, ImageOps, ImageEnhance, ImageDraw, ImageFont

class SimpleImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Image Editor")
        self.root.geometry("800x600")
        
        self.image = None
        self.image_path = None
        self.tk_image = None
        self.image_history = []  # For undo functionality

        # UI Elements
        self.create_ui()

    def create_ui(self):
        """Create the UI components with enhanced design."""
        # Title Frame
        title_frame = tk.Frame(self.root, bg="#3b3b3b", pady=10)
        title_frame.pack(fill=tk.X)

        title_label = tk.Label(title_frame, text="Simple Image Editor", font=("Arial", 24, "bold"), fg="white", bg="#3b3b3b")
        title_label.pack()

        # Canvas for displaying image
        self.canvas = tk.Canvas(self.root, width=600, height=400)
        self.canvas.pack(pady=20)

        # Button Frame (enhanced)
        button_frame = tk.Frame(self.root, pady=10)
        button_frame.pack(fill=tk.X)

        self.load_button = tk.Button(button_frame, text="Load Image", command=self.load_image, font=("Arial", 12), bg="#4CAF50", fg="white", relief="raised", width=15)
        self.load_button.pack(side=tk.LEFT, padx=10)

        self.save_button = tk.Button(button_frame, text="Save Image", command=self.save_image, font=("Arial", 12), bg="#2196F3", fg="white", relief="raised", width=15)
        self.save_button.pack(side=tk.LEFT, padx=10)

        self.resize_button = tk.Button(button_frame, text="Resize", command=self.resize_image, font=("Arial", 12), bg="#FF9800", fg="white", relief="raised", width=15)
        self.resize_button.pack(side=tk.LEFT, padx=10)

        self.crop_button = tk.Button(button_frame, text="Crop", command=self.crop_image, font=("Arial", 12), bg="#FF5722", fg="white", relief="raised", width=15)
        self.crop_button.pack(side=tk.LEFT, padx=10)

        self.filter_button = tk.Button(button_frame, text="Apply Filter", command=self.apply_filter, font=("Arial", 12), bg="#673AB7", fg="white", relief="raised", width=15)
        self.filter_button.pack(side=tk.LEFT, padx=10)

        self.text_button = tk.Button(button_frame, text="Add Text Overlay", command=self.add_text_overlay, font=("Arial", 12), bg="#9C27B0", fg="white", relief="raised", width=15)
        self.text_button.pack(side=tk.LEFT, padx=10)

        self.undo_button = tk.Button(button_frame, text="Undo", command=self.undo_action, font=("Arial", 12), bg="#FFC107", fg="white", relief="raised", width=15)
        self.undo_button.pack(side=tk.LEFT, padx=10)

        # Footer Frame
        footer_frame = tk.Frame(self.root, bg="#3b3b3b", pady=10)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)

        footer_label = tk.Label(footer_frame, text="Created by Hassan Ahmed, for the Hack Club", font=("Arial", 10), fg="white", bg="#3b3b3b")
        footer_label.pack()

    def load_image(self):
        """Load an image from the file system."""
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if file_path:
            self.image_path = file_path
            self.image = Image.open(self.image_path)
            self.image_history.append(self.image.copy())  # Save the initial state for undo
            self.display_image()

    def display_image(self):
        """Display the image on the canvas."""
        if self.image:
            img = self.image.resize((600, 400))  # Resize for canvas display
            self.tk_image = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, image=self.tk_image, anchor=tk.NW)

            # Update image dimensions label
            width, height = self.image.size
            self.dim_label.config(text=f"Image Dimensions: {width}x{height}")

    def save_image(self):
        """Save the edited image."""
        if not self.image:
            messagebox.showerror("Error", "No image loaded!")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg")])
        if file_path:
            self.image.save(file_path)
            messagebox.showinfo("Success", "Image saved successfully!")

    def resize_image(self):
        """Resize the image."""
        if not self.image:
            messagebox.showerror("Error", "No image loaded!")
            return
        
        def apply_resize():
            try:
                width = int(width_entry.get())
                height = int(height_entry.get())
                self.image = self.image.resize((width, height))
                self.image_history.append(self.image.copy())  # Save state for undo
                self.display_image()
                resize_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid input for width or height.")

        resize_window = tk.Toplevel(self.root)
        resize_window.title("Resize Image")

        tk.Label(resize_window, text="Width:").pack(padx=10, pady=5)
        width_entry = tk.Entry(resize_window)
        width_entry.pack(padx=10, pady=5)

        tk.Label(resize_window, text="Height:").pack(padx=10, pady=5)
        height_entry = tk.Entry(resize_window)
        height_entry.pack(padx=10, pady=5)

        tk.Button(resize_window, text="Resize", command=apply_resize).pack(padx=10, pady=10)

    def crop_image(self):
        """Crop the image."""
        if not self.image:
            messagebox.showerror("Error", "No image loaded!")
            return

        def apply_crop():
            try:
                left = int(left_entry.get())
                top = int(top_entry.get())
                right = int(right_entry.get())
                bottom = int(bottom_entry.get())
                self.image = self.image.crop((left, top, right, bottom))
                self.image_history.append(self.image.copy())  # Save state for undo
                self.display_image()
                crop_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid input for crop coordinates.")

        crop_window = tk.Toplevel(self.root)
        crop_window.title("Crop Image")

        tk.Label(crop_window, text="Left:").pack(padx=10, pady=5)
        left_entry = tk.Entry(crop_window)
        left_entry.pack(padx=10, pady=5)

        tk.Label(crop_window, text="Top:").pack(padx=10, pady=5)
        top_entry = tk.Entry(crop_window)
        top_entry.pack(padx=10, pady=5)

        tk.Label(crop_window, text="Right:").pack(padx=10, pady=5)
        right_entry = tk.Entry(crop_window)
        right_entry.pack(padx=10, pady=5)

        tk.Label(crop_window, text="Bottom:").pack(padx=10, pady=5)
        bottom_entry = tk.Entry(crop_window)
        bottom_entry.pack(padx=10, pady=5)

        tk.Button(crop_window, text="Crop", command=apply_crop).pack(padx=10, pady=10)

    def apply_filter(self):
        """Apply a filter to the image."""
        if not self.image:
            messagebox.showerror("Error", "No image loaded!")
            return

        def apply_selected_filter():
            selected_filter = filter_var.get()
            if selected_filter == "Vivid":
                enhancer = ImageEnhance.Color(self.image)
                self.image = enhancer.enhance(1.5)
            elif selected_filter == "Dramatic":
                enhancer = ImageEnhance.Contrast(self.image)
                self.image = enhancer.enhance(2)
            elif selected_filter == "Mono":
                self.image = self.image.convert("L")
            elif selected_filter == "Instant":
                self.image = ImageOps.colorize(self.image.convert("L"), "#FDCB82", "#C27D35")
            elif selected_filter == "Noir":
                self.image = self.image.convert("L").point(lambda x: 255-x)
            elif selected_filter == "Fade":
                enhancer = ImageEnhance.Brightness(self.image)
                self.image = enhancer.enhance(0.7)
            elif selected_filter == "Process":
                self.image = self.image.filter(ImageFilter.CONTOUR)
            elif selected_filter == "Transfer":
                self.image = ImageOps.colorize(self.image.convert("L"), "#DEC4B4", "#B8C0CC")

            self.image_history.append(self.image.copy())  # Save state for undo
            self.display_image()
            filter_window.destroy()

        filter_window = tk.Toplevel(self.root)
        filter_window.title("Apply Filter")

        filter_var = tk.StringVar(value="Vivid")
        tk.Radiobutton(filter_window, text="Vivid", variable=filter_var, value="Vivid").pack(padx=10, pady=5)
        tk.Radiobutton(filter_window, text="Dramatic", variable=filter_var, value="Dramatic").pack(padx=10, pady=5)
        tk.Radiobutton(filter_window, text="Mono", variable=filter_var, value="Mono").pack(padx=10, pady=5)
        tk.Radiobutton(filter_window, text="Instant", variable=filter_var, value="Instant").pack(padx=10, pady=5)
        tk.Radiobutton(filter_window, text="Noir", variable=filter_var, value="Noir").pack(padx=10, pady=5)
        tk.Radiobutton(filter_window, text="Fade", variable=filter_var, value="Fade").pack(padx=10, pady=5)
        tk.Radiobutton(filter_window, text="Process", variable=filter_var, value="Process").pack(padx=10, pady=5)
        tk.Radiobutton(filter_window, text="Transfer", variable=filter_var, value="Transfer").pack(padx=10, pady=5)

        tk.Button(filter_window, text="Apply", command=apply_selected_filter).pack(padx=10, pady=10)

    def add_text_overlay(self):
        """Add text overlay on the image."""
        if not self.image:
            messagebox.showerror("Error", "No image loaded!")
            return

        def apply_text_overlay():
            text = text_entry.get()
            if text:
                draw = ImageDraw.Draw(self.image)
                font = ImageFont.load_default()
                draw.text((10, 10), text, font=font, fill="white")
                self.image_history.append(self.image.copy())  # Save state for undo
                self.display_image()
                text_window.destroy()

        text_window = tk.Toplevel(self.root)
        text_window.title("Add Text Overlay")

        tk.Label(text_window, text="Text:").pack(padx=10, pady=5)
        text_entry = tk.Entry(text_window)
        text_entry.pack(padx=10, pady=5)

        tk.Button(text_window, text="Add Text", command=apply_text_overlay).pack(padx=10, pady=10)

    def undo_action(self):
        """Undo the last action performed."""
        if len(self.image_history) > 1:
            self.image_history.pop()
            self.image = self.image_history[-1]
            self.display_image()
        else:
            messagebox.showwarning("Undo", "No action to undo!")

if __name__ == "__main__":
    root = tk.Tk()
    editor = SimpleImageEditor(root)
    root.mainloop()
