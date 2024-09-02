import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog, simpledialog
from ttkthemes import ThemedTk
from tkmacosx import Button
from PIL import Image, ImageTk, ImageDraw, ImageFont
from tkcolorpicker import askcolor

# TODO Download function of new image


# <--------------- GUI COLORS ------------------->
BACKGROUND_COLOR = '#374546'
HEADER_COLOR = '#c9c0b6'


# <--------------- GUI CONFIGURATION ------------------->
class GUI:  # Creates a window
    def __init__(self, root):
        self.root = root
        self.root.title("Watermark Applicator")
        self.root.geometry("1000x600")

        # Create a separate themed window for the sliders only
        self.themed_root = ThemedTk(theme='arc')
        self.themed_root.withdraw()

        # Initialize image variables
        self.original_image = None  # Store the original image
        self.watermarked_image = None  # Store the watermarked image for preview
        self.wm_color = (255, 255, 255)  # Default color (white)

        # <-----------------HEADER LAYOUT ---------------->
        self.header = tk.Frame(root, bg=HEADER_COLOR)
        self.header.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        # UPLOAD IMAGE BUTTON
        self.upload_btn = Button(
            text="Upload Image",
            foreground="black",
            highlightbackground="#c9c0b6",
            command=self.upload_image
        )
        self.upload_btn.place(relx=0.36, rely=0.03)

        # CLEAR IMAGE BUTTON
        self.clear_image_btn = Button(
            text="Clear Image",
            foreground="black",
            highlightbackground="#c9c0b6",
            command=self.clear_image
        )
        self.clear_image_btn.place(relx=0.5, rely=0.03)

        # <-----------------MAIN LAYOUT ---------------->

        # Image Display (Placeholder)
        self.image_canvas = Canvas(self.root, width=600, height=400, bg="gray")
        self.image_canvas.place(relx=0.45, rely=0.1, relwidth=0.55, relheight=1)

        # Watermark Entry
        Label(self.root, text='Watermark Text', font=('Ariel', 18)).place(relx=0.15, rely=0.15)
        self.watermark_text = Entry(self.root, width=50)
        self.watermark_text.place(relx=0.02, rely=0.2, relwidth=0.4, relheight=.05)

        # Font Chooser
        Label(self.root, text='Select Font').place(relx=0.035, rely=0.28)
        self.font_var = StringVar(self.root)
        self.font_var.set("Open Sans")  # Default
        self.font_menu = OptionMenu(self.root, self.font_var, "Open Sans", "Calligraffitti", "Great Vibes",
                                    "Nerko", "Pirata")
        self.font_menu.place(relx=0.12, rely=0.28)

        # Font Size Slider
        self.font_size_label = ttk.Label(self.root, text="Font Size: 10")
        self.font_size_label.place(relx=0.23, rely=0.28)
        self.font_size_var = tk.IntVar()  # Variable to store the font size value
        self.font_size_slide = ttk.Scale(self.root, from_=10, to=70, orient=HORIZONTAL,
                                         command=self.update_font_size, variable=self.font_size_var)
        self.font_size_slide.place(relx=0.32, rely=0.28)
        self.font_size_var.set(10)

        # Watermark Position Menu
        Label(self.root, text='Position').place(relx=0.19, rely=0.45)
        self.wm_position_var = StringVar(self.root)
        self.wm_position_var.set('Top Left')
        self.tr_radio = Radiobutton(self.root, variable=self.wm_position_var, value='Top Right', text='Top Right')
        self.tr_radio.place(relx=0.23, rely=0.5)
        self.br_radio = Radiobutton(self.root, variable=self.wm_position_var, value='Bottom Right',
                                    text='Bottom Right')
        self.br_radio.place(relx=0.23, rely=0.55)
        self.tl_radio = Radiobutton(self.root, variable=self.wm_position_var, value='Top Left', text='Top Left')
        self.tl_radio.place(relx=0.1, rely=0.5)
        self.bl_radio = Radiobutton(self.root, variable=self.wm_position_var, value='Bottom Left',
                                    text='Bottom Left')
        self.bl_radio.place(relx=0.1, rely=0.55)
        self.center_radio = Radiobutton(self.root, variable=self.wm_position_var, value='Center', text='Center')
        self.center_radio.place(relx=0.18, rely=0.6)

        # Color Picker Button
        self.color_btn = Button(
            text="Select Color",
            foreground="black",
            highlightbackground="#313232",
            command=self.pick_color
        )
        self.color_btn.place(relx=0.16, rely=0.67)

        # Transparency Slider
        self.trans_level_label = ttk.Label(self.root, text="Transparency Slider: 0")
        self.trans_level_label.place(relx=0.07, rely=0.75)
        self.trans_level_var = tk.IntVar()  # Variable to store the transparency value
        self.trans_level_slide = ttk.Scale(self.root, from_=0, to=100, orient=HORIZONTAL, length=150,
                                           command=self.update_transparency_level, variable=self.trans_level_var)
        self.trans_level_slide.place(relx=0.23, rely=0.75)
        self.trans_level_var.set(0)

        # Preview Image Button
        self.preview_btn = Button(
            text="Preview",
            foreground="black",
            highlightbackground="#313232",
            height=30,
            command=self.apply_watermark
        )
        self.preview_btn.place(relx=0.12, rely=0.85)

        # Save Image Button
        self.save_img_btn = Button(
            text="Save",
            background="#007aff",
            foreground="white",
            highlightbackground="#313232",
            height=30,
            command=self.save_image
        )
        self.save_img_btn.place(relx=0.22, rely=0.85)

    # <-----------------SELECT IMAGE FILE----------------->
    def upload_image(self):
        file_path = filedialog.askopenfilename(title="Select a Photo", filetypes=[("Jpg Files", "*.jpg"),
                                                                                 ("Png Files", "*.png")])
        if file_path:
            try:
                image = Image.open(file_path)
                image.thumbnail((600, 400))
                self.original_image = image.copy()
                self.uploaded_image = ImageTk.PhotoImage(image)
                self.image_canvas.create_image(0, 0, anchor=tk.NW, image=self.uploaded_image)
            except Exception as e:
                print(f"Error loading image: {e}")

    # <-----------------CLEAR IMAGE----------------->
    def clear_image(self):
        self.image_canvas.delete('all')
        self.original_image = None
        self.watermarked_image = None

    # <-----------------APPLY WATERMARK----------------->
    def apply_watermark(self):
        if not self.original_image:
            print("No image uploaded!")
            return

        # Get the watermark text
        wm_text = self.watermark_text.get()

        # Get font name and size
        wm_font = self.font_var.get()
        wm_font_size = self.font_size_var.get()

        font_paths = {
            "Open Sans": "fonts/OpenSans-Regular.ttf",
            "Calligraffitti": "fonts/Calligraffitti-Regular.ttf",
            "Great Vibes": "fonts/GreatVibes-Regular.ttf",
            "Nerko": "fonts/NerkoOne-Regular.ttf",
            "Pirata": "fonts/PirataOne-Regular.ttf",
        }

        # Load the font with the selected size
        try:
            font_path = font_paths.get(wm_font, "arial.ttf")
            font = ImageFont.truetype(font_path, wm_font_size)
        except IOError:
            print(f"Font '{wm_font}' not found. Using default font.")
            font = ImageFont.load_default()

        # Get Position
        wm_position = self.wm_position_var.get()

        # Get transparency level
        wm_transparency = self.trans_level_var.get()

        # Clear the canvas before applying a new watermark
        self.image_canvas.delete('all')

        # Create a copy of the original image to apply the watermark
        watermarked_image = self.original_image.copy()
        watermarked_image = watermarked_image.convert("RGBA")  # Ensure image is in RGBA mode
        drawable = ImageDraw.Draw(watermarked_image)

        # Calculate text bounding box and position
        text_bbox = drawable.textbbox((0, 0), wm_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        if wm_position == 'Top Right':
            wm_position = (watermarked_image.width - text_width - 10, 10)
        elif wm_position == 'Bottom Right':
            wm_position = (watermarked_image.width - text_width - 10, watermarked_image.height - text_height - 10)
        elif wm_position == 'Top Left':
            wm_position = (10, 10)
        elif wm_position == 'Bottom Left':
            wm_position = (10, watermarked_image.height - text_height - 10)
        elif wm_position == 'Center':
            wm_position = ((watermarked_image.width - text_width) // 2, (watermarked_image.height - text_height) // 2)

        # Add the watermark text to the image with the specified transparency
        # Combine color and transparency into RGBA format
        fill_color = self.wm_color[:3] + (int(255 * wm_transparency / 100),)
        drawable.text(wm_position, wm_text, font=font, fill=fill_color)

        # Update the canvas with the newly watermarked image
        self.watermarked_image = ImageTk.PhotoImage(watermarked_image)
        self.image_canvas.create_image(0, 0, anchor=NW, image=self.watermarked_image)

        # <------------UPDATE FONT SIZE AND TRANSPARENCY LEVELS------------------>

    def save_image(self):
        if self.watermarked_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
            if file_path:
                try:
                    self.original_image.save(file_path)
                    print(f"Image saved successfully at {file_path}")
                except Exception as e:
                    print(f"Error saving image: {e}")
        else:
            print("No watermarked image to save!")

    def update_font_size(self, value):
        # Update the label with the current font size
        self.font_size_label.config(text=f"Font Size: {int(float(value))}")

    def update_transparency_level(self, value):
        # Update the label with the current transparency level
        self.trans_level_label.config(text=f"Transparency Level: {int(float(value))}")

    def pick_color(self):
        picked_color, _ = askcolor(title="Watermark Color")
        if picked_color:
            self.wm_color = tuple(map(int, picked_color[:3])) + (255,)  # Default alpha value 255 (opaque)

    # Run the application


if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()