# Import necessary modules
from tkinter import *
from tkinter import filedialog as fd, ttk
import matplotlib.font_manager as fm
from tkinter.colorchooser import askcolor
import tkinter.messagebox
import PIL
from PIL import Image, ImageDraw, ImageFont, ImageTk
from ttkthemes import ThemedTk
import os

# Constants
BACKGROUND_COLOR = "#161a1d"
FILE_PATH = ""
IMAGE = ""
IMAGE_COPY = ""
FONT = "tahoma"
FONT_PATH = ""
OPACITY = 1.0
FONT_SIZE = 70
FULL_HEIGHT = 0
FULL_WIDTH = 0
HEIGHT = 0
WIDTH = 0
ORIGINAL_HEIGHT = 0
ORIGINAL_WIDTH = 0
ROTATION = 0
COLOR = (255, 255, 255)


# Function to open a file dialog and update the displayed image
def open_file_dialog():
    global FILE_PATH
    file_path = fd.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
    if file_path:
        update_image(file_path)
        FILE_PATH = file_path


# Function to update the displayed image
def update_image(file_path):
    global HEIGHT, WIDTH, FULL_HEIGHT, FULL_WIDTH, IMAGE, ORIGINAL_WIDTH, ORIGINAL_HEIGHT
    photo = Image.open(file_path)
    ORIGINAL_HEIGHT = photo.size[1]
    ORIGINAL_WIDTH = photo.size[0]
    print(photo.size[1], photo.size[0])
    photo.thumbnail(size=(800, 600))
    new_image = ImageTk.PhotoImage(photo)
    image_square.config(image=new_image)
    image_square.image = new_image
    FULL_HEIGHT = photo.size[1]
    HEIGHT = FULL_HEIGHT // 2
    FULL_WIDTH = photo.size[0]
    WIDTH = FULL_WIDTH // 2
    IMAGE = photo  # Save the PhotoImage for later use


# Function to get a list of available TTF fonts
def get_ttf_fonts():
    """ Get a list of available TTF fonts """
    ttf_fonts = fm.findSystemFonts(fontpaths=None, fontext='ttf')
    fonts_list = []
    formatted_fonts = [x.split("\\")[-1] for x in ttf_fonts]
    for f in formatted_fonts:
        if ".otf" not in f:
            fonts_list.append(f.replace(".ttf", "").replace(".TTF", "").replace(".ttc", ""))
    return fonts_list


# Callback function for font selection
def get_selected_font():
    """ Callback function for font selection """
    global FONT
    FONT = font_combobox.get()
    apply_watermark()


# Helper function to convert hex color to RGBA
def hex_to_rgba(hex_color):
    """ Convert hex color to RGBA """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


# Function to choose color
def choose_color():
    """ Choose a color """
    global COLOR
    color_dialog = askcolor()
    if color_dialog:
        hex_color = color_dialog[1]
        rgba_color = hex_to_rgba(hex_color)

        color_input.delete(0, END)
        color_input.insert(0, rgba_color)

        color_preview_canvas.config(bg=hex_color)
        COLOR = rgba_color
    apply_watermark()


# Validation function for size input
def validate_size_input(value, action):
    """ Validate size input """
    if action == '1':
        try:
            int_value = int(value)
            if 1 <= int_value <= 250:
                return True
            else:
                return False
        except ValueError:
            return False
    return True


# Function to update watermark size
def update_watermark_size(value):
    """ Update watermark size.  """
    try:
        float_value = float(value)
        int_value = int(float_value)
    except ValueError:
        int_value = 70  # Default value
    global FONT_SIZE
    FONT_SIZE = int_value
    size_input.delete(0, END)
    size_input.insert(0, str(int_value))
    apply_watermark()


# Function to update opacity
def update_opacity():
    """ Update opacity. """
    global OPACITY
    OPACITY = float(opacity_input.get())
    apply_watermark()


# Function to rotate clockwise
def clockwise_rotation():
    """ Rotate clockwise. """
    global ROTATION
    ROTATION -= 20
    apply_watermark()


# Function to rotate anticlockwise
def anticlockwise_rotation():
    """ Rotate anti-clockwise. """
    global ROTATION
    ROTATION += 20
    apply_watermark()


# Function to move text up
def move_up():
    """ Move text up. """
    global HEIGHT, FULL_HEIGHT
    if HEIGHT < FULL_HEIGHT:
        HEIGHT = max(0, HEIGHT - 10)
    apply_watermark()


# Function to move text down
def move_down():
    """ Move text down. """
    global HEIGHT, FULL_HEIGHT
    if HEIGHT < FULL_HEIGHT:
        HEIGHT = max(0, HEIGHT + 10)
    apply_watermark()


# Function to move text left
def move_left():
    """ Move text left. """
    global WIDTH, FULL_WIDTH
    if WIDTH < FULL_WIDTH:
        WIDTH = min(FULL_WIDTH, WIDTH - 10)
        apply_watermark()


# Function to move text right
def move_right():
    """ Move text right. """
    global WIDTH, FULL_WIDTH
    if WIDTH < FULL_WIDTH:
        WIDTH = min(FULL_WIDTH, WIDTH + 10)
        apply_watermark()


# Function to apply watermark on the image
def apply_watermark():
    """ Apply watermark on the image. """
    global FILE_PATH, IMAGE, IMAGE_COPY, FONT_SIZE, HEIGHT, WIDTH, ROTATION, COLOR, OPACITY, FONT, FULL_HEIGHT, \
        FULL_WIDTH
    try:
        with Image.open(FILE_PATH).convert("RGBA") as original_image:
            original_image.thumbnail(size=(800, 600))
            watermark_field = Image.new("RGBA", original_image.size, (255, 255, 255, 0))
            # Set text position
            text_position = (WIDTH, HEIGHT)

            # Declare text color
            opacity_tuple = (int(255 * OPACITY),)
            watermark_fill = COLOR + opacity_tuple

            # Draw text in the watermark field
            draw = ImageDraw.Draw(watermark_field)
            font = ImageFont.truetype(FONT, FONT_SIZE)

            # Get text size
            text_bbox = draw.textbbox((text_position[0], text_position[1]), f"{watermark_input.get()}", font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            text_position = (text_position[0] - text_width // 2, text_position[1] - text_height // 2)
            draw.text(text_position, f"{watermark_input.get()}", fill=watermark_fill, font=font)

            watermark_rotation = watermark_field.rotate(ROTATION, expand=False)  # Expand the image to fit rotations

            # Adjust image size to fit in the window
            new_width = min(original_image.width, watermark_rotation.width)
            new_height = min(original_image.height, watermark_rotation.height)

            # Create new watermark and image fields to adjust their sizes
            resized_watermark = Image.new("RGBA", (new_width, new_height), (255, 255, 255, 0))
            resized_watermark.paste(watermark_rotation, (0, 0), watermark_rotation)
            resized_original = Image.new("RGBA", (new_width, new_height), (255, 255, 255, 0))
            resized_original.paste(original_image, (0, 0), original_image)

            watermark_output = Image.alpha_composite(resized_original, resized_watermark)

            watermark_output_rgba = watermark_output.convert("RGBA")

            photo_image = ImageTk.PhotoImage(watermark_output_rgba)

            image_square.configure(image=photo_image)
            image_square.image = photo_image

            IMAGE = watermark_output_rgba
            # Create a copy of the watermarked image with original height and width for saving image
            IMAGE_COPY = watermark_output_rgba.copy()
            IMAGE_COPY = IMAGE_COPY.resize((ORIGINAL_WIDTH, ORIGINAL_HEIGHT), Image.LANCZOS)

    except FileNotFoundError:
        tkinter.messagebox.showerror("Error", "File not found.")
    except PIL.UnidentifiedImageError:
        tkinter.messagebox.showerror("Error", "Invalid file extension.")
    except Exception as e:
        tkinter.messagebox.showerror("Error", f"{e}.")
        pass


def save_image():
    """ Save the image with watermark. """
    global IMAGE_COPY
    try:
        if IMAGE_COPY:
            path = fd.asksaveasfilename(confirmoverwrite=True, defaultextension="png",
                                        filetypes=[("jpeg", ".jpg"), ("png", ".png"), ("bitmap", "bmp"),
                                                   ("gif", ".gif")])

            if path:
                if os.path.splitext(path)[1] == ".jpg":
                    image_to_save = IMAGE_COPY.convert("RGB")
                    image_to_save.save(path)
                else:
                    IMAGE_COPY.save(path)
                tkinter.messagebox.showinfo("Success", "Image saved successfully!")
    except Exception as e:
        tkinter.messagebox.showerror("Error", f"An error occurred while saving the image: {e}")


# -------------------------------WINDOW CONFIG---------------------------------------#

# Create themed Tkinter window
window = ThemedTk(theme="equilux")
window.title("Image Watermark App")
window.minsize(height=800, width=1100)
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# ---------------------------------IMAGE SQUARE----------------------------------#

# Create an empty image for the initial display
empty_image = Image.new("RGBA", (800, 600), color=BACKGROUND_COLOR)
image = ImageTk.PhotoImage(empty_image)
image_square = ttk.Label(window, image=image, borderwidth=3)
image_square.image = image  # keep a reference
image_square.grid(column=0, rowspan=15, sticky='w')

# -------------------------------UPLOAD IMAGE BUTTON-------------------------------#

# Style for custom button
button_style = ttk.Style()
button_style.configure("Custom.TButton", width=13, background="#fb8500", foreground="#FFAB59",
                       font=("Ubuntu", 13, "bold"))
apply_button = ttk.Button(window, text="Upload Image", style="Custom.TButton", command=open_file_dialog)
apply_button.grid(row=15, column=0, pady=10)

# -------------------------------WATERMARK LABEL------------------------------------#

# Label for watermark configuration
config_label = ttk.Label(text="Create your Watermark", background=BACKGROUND_COLOR, foreground='#fb8500',
                         font=("Ubuntu", 18, "bold"),
                         justify="center")
config_label.grid(column=3, row=1, columnspan=4, pady=(0, 15))

# Label and input for watermark text
watermark_label = ttk.Label(text="Watermark Text:", width=15, padding=[20, 0], background="#161a1d",
                            font=("Ubuntu", 12, "bold"))
watermark_label.grid(column=3, row=2, sticky='w')
watermark_input = ttk.Entry(width=47, font=("Ubuntu", 10, "bold"))
watermark_input.grid(column=4, row=2, columnspan=3, sticky='w')
watermark_input.get()

# --------------------------------FONT LABEL------------------------------------------#

# Get a list of available fonts and create a sorted list
available_fonts = get_ttf_fonts()
sorted_fonts = sorted(available_fonts)

# Label for font selection
font_label = ttk.Label(text="Font:", width=15, background="#161a1d", font=("Ubuntu", 12, "bold"))
font_label.grid(column=3, row=3)

# Combobox for font selection
font_combobox = ttk.Combobox(window, values=sorted_fonts, width=45, font=("Ubuntu", 10))
font_combobox.grid(column=4, row=3, columnspan=3, sticky='w', pady=(1, 1))
font_combobox.bind("<<ComboboxSelected>>", get_selected_font)
font_combobox.set("tahoma")

# --------------------------------COLOR LABEL------------------------------------------#

# Label for color selection
color_label = ttk.Label(text="Color:", width=15, background=BACKGROUND_COLOR, font=("Ubuntu", 12, "bold"))
color_label.grid(column=3, row=4)

# Canvas to display color preview
color_preview_canvas = Canvas(window,
                              width=20,
                              height=20,
                              background="#FFFFFF",
                              highlightthickness=0)
color_preview_canvas.grid(column=6, row=4)

# Entry and button for color input
color_input = ttk.Entry(width=18, font=("Ubuntu", 10))
color_input.grid(column=5, row=4, columnspan=2, sticky='w')
choose_color_button = ttk.Button(window, text="Choose Color", command=choose_color)
choose_color_button.grid(column=4, row=4, sticky='w')

# --------------------------------SIZE LABEL------------------------------------------#

# Label for font size selection
size_label = ttk.Label(text="Font Size:", background=BACKGROUND_COLOR, width=15, font=("Ubuntu", 12, "bold"))
size_label.grid(column=3, row=5)

# Scale and entry for font size input
current_font_size = IntVar(value=70)
current_font_size.set(FONT_SIZE)
size_scale = ttk.Scale(window, length=250, from_=3, to=250, orient=HORIZONTAL, command=update_watermark_size,
                       variable=current_font_size)
size_scale.grid(column=4, row=5, columnspan=2, sticky='w')

validate_size_input_cmd = window.register(validate_size_input)
size_input = ttk.Entry(width=6, font=("Ubuntu", 10), validate='key', textvariable=current_font_size,
                       validatecommand=(validate_size_input_cmd, '%P', '%d'))
size_input.grid(column=6, row=5, pady=0)

# --------------------------------OPACITY LABEL------------------------------------------#

# Label for opacity selection
opacity_label = ttk.Label(text="Opacity:", background=BACKGROUND_COLOR, width=15, font=("Ubuntu", 12, "bold"))
opacity_label.grid(column=3, row=6)

# Spinbox to choose opacity values
opacity_input = ttk.Spinbox(from_=0.0, to=1.0, increment=0.1, format="%.1f", justify="center", width=5,
                            font=("Ubuntu", 10), command=update_opacity)
opacity_input.set(1.0)
opacity_input.grid(column=4, row=6, sticky='w')

# --------------------------------ROTATION LABEL------------------------------------------#

# Label for rotation selection
rotation_label = ttk.Label(text="Rotation:", width=15, background=BACKGROUND_COLOR, font=("Ubuntu", 12, "bold"))
rotation_label.grid(column=3, row=7)

# Buttons for clockwise and anticlockwise rotation
increment_rotation_button = ttk.Button(text="⭮", command=clockwise_rotation)
increment_rotation_button.grid(column=4, row=7, sticky='e', padx=20)

decrement_rotation_button = ttk.Button(text="⭯", command=anticlockwise_rotation)
decrement_rotation_button.grid(column=5, row=7, sticky='w', pady=20)

# --------------------------------POSITION LABEL------------------------------------------#

# Label for position selection
position_label = ttk.Label(text="Position:", width=15, background=BACKGROUND_COLOR, font=("Ubuntu", 12, "bold"))
position_label.grid(column=3, row=8)

# Buttons for moving text in different directions
position_up_button = ttk.Button(text="▲", width=4, command=move_up)
position_up_button.grid(column=5, row=8)

position_left_button = ttk.Button(text='◀', width=4, command=move_left)
position_left_button.grid(column=4, row=9, sticky='e')

position_right_button = ttk.Button(text='▶', width=4, command=move_right)
position_right_button.grid(column=6, row=9, sticky='w')

position_down_button = ttk.Button(text='▼', width=4, command=move_down)
position_down_button.grid(column=5, row=10)

apply_button = ttk.Button(window, text="Apply", style="Custom.TButton", command=apply_watermark)
apply_button.grid(row=14, column=3, columnspan=2)
save_button = ttk.Button(window, text="Save Image", style="Custom.TButton", command=save_image)
save_button.grid(row=14, column=5, sticky='e')
window.mainloop()
