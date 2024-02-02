from tkinter import *
from tkinter import filedialog as fd, ttk
from tkinter.colorchooser import askcolor
import tkinter.messagebox
import PIL
from PIL import Image, ImageDraw, ImageFont, ImageTk
from PIL.Image import Resampling
from ttkthemes import ThemedTk
import os
from helpers import open_and_prepare_image, get_ttf_fonts, hex_to_rgba, validate_size_input

# Constants
BACKGROUND_COLOR = "#161a1d"    # Background color for the GUI
FILE_PATH = ""                  # Path to the selected image file
IMAGE = ""                      # Original image
IMAGE_COPY = ""                 # Copy of the original image for watermarking
FONT = "tahoma"                 # Default font for text watermark
OPACITY = 1.0                   # Default opacity for the watermark
FONT_SIZE = 70                  # Default font size for text watermark
FULL_HEIGHT = 0                 # Full height of the thumbnail image
FULL_WIDTH = 0                  # Full width of the thumbnail image
CENTER_HEIGHT = 0               # Vertical center of the thumbnail original image
CENTER_WIDTH = 0                # Horizontal center of the thumbnail original image
ORIGINAL_HEIGHT = 0             # Height of the original image
ORIGINAL_WIDTH = 0              # Width of the original image
ROTATION = 0                    # Rotation angle for the watermark
COLOR = (255, 255, 255)         # Default color for text watermark
LOGO_FILE_PATH = ""             # Path to the selected logo file
LOGO_WIDTH = 100                # Default width for logo watermark
LOGO_HEIGHT = 100               # Default height for logo watermark
WATERMARK_TYPE = "Text"         # Default watermark type ("Text" or "Logo")


def open_file_dialog():
    """Open a file dialog to choose an image file."""
    global FILE_PATH

    # Open a file dialog to select an image file with specific extensions
    file_path = fd.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])

    # Check if a file was selected
    if file_path:
        # Update the image in the GUI with the selected file
        update_image(file_path)

        # Update the global FILE_PATH variable with the selected file path
        FILE_PATH = file_path


# Function to update the displayed image
def update_image(file_path):
    """Update the displayed image in the GUI."""
    global CENTER_HEIGHT, CENTER_WIDTH, FULL_HEIGHT, FULL_WIDTH, IMAGE, ORIGINAL_WIDTH, ORIGINAL_HEIGHT

    # Open the image file using the Pillow library
    photo = Image.open(file_path)

    # Save the original dimensions of the image
    ORIGINAL_HEIGHT = photo.size[1]
    ORIGINAL_WIDTH = photo.size[0]

    # Resize the image to fit within a specified size while maintaining the aspect ratio
    photo.thumbnail(size=(700, 500))

    # Convert the image to a PhotoImage object for displaying in the Tkinter GUI
    new_image = ImageTk.PhotoImage(photo)

    # Update the Tkinter Label widget with the new image
    image_square.config(image=new_image)
    image_square.image = new_image

    # Update global variables with the new dimensions of the displayed image
    FULL_HEIGHT = photo.size[1]
    CENTER_HEIGHT = FULL_HEIGHT // 2
    FULL_WIDTH = photo.size[0]
    CENTER_WIDTH = FULL_WIDTH // 2

    # Save the original Pillow image for later use
    IMAGE = photo


def choose_logo_file():
    """
    Opens a file dialog to choose a logo file and updates the global LOGO_FILE_PATH variable.

    Globals:
        LOGO_FILE_PATH (str): Path to the logo image file.

    Functions:
        None
    """
    global LOGO_FILE_PATH

    # Open a file dialog to choose a logo file
    logo_file_path = fd.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])

    # Update the global LOGO_FILE_PATH variable if a file is selected
    if logo_file_path:
        LOGO_FILE_PATH = logo_file_path


def get_selected_font(event):
    """Callback function for font selection."""
    global FONT

    # Get the selected font from the font combobox
    FONT = font_combobox.get()

    # Apply the watermark with the updated font
    apply_watermark()


# Function to choose a color
def choose_color():
    """Choose a color."""
    global COLOR

    # Open a color dialog and get the selected color
    color_dialog = askcolor()

    # Check if a color was selected
    if color_dialog:
        hex_color = color_dialog[1]

        # Convert the hexadecimal color to RGBA format
        rgba_color = hex_to_rgba(hex_color)

        # Update the color input field with the RGBA color value
        color_input.delete(0, END)
        color_input.insert(0, rgba_color)

        # Update the color preview canvas with the selected color
        color_preview_canvas.config(bg=hex_color)

        # Update the global COLOR variable with the RGBA color value
        COLOR = rgba_color

    # Apply the watermark with the updated color
    apply_watermark()


def update_watermark_size(value):
    """Update watermark size."""
    global FONT_SIZE

    # Try to convert the input value to a float and then to an integer
    try:
        float_value = float(value)
        int_value = int(float_value)
    except ValueError:
        int_value = 70  # Default value if conversion fails

    # Update the global FONT_SIZE variable with the integer value
    FONT_SIZE = int_value

    # Update the size input field with the new size value
    size_input.delete(0, END)
    size_input.insert(0, str(int_value))

    # Apply the watermark with the updated size
    apply_watermark()


def update_logo_size_height(value):
    """Update logo size (height)."""
    global LOGO_HEIGHT

    # Try to convert the input value to a float and then to an integer
    try:
        float_value = float(value)
        int_value = int(float_value)
    except ValueError:
        int_value = 100  # Default value if conversion fails

    # Update the global LOGO_HEIGHT variable with the integer value
    LOGO_HEIGHT = int_value

    # Update the logo height input field with the new height value
    logo_height_input.delete(0, END)
    logo_height_input.insert(0, str(int_value))

    # Apply the watermark with the updated logo size
    apply_watermark()


def update_logo_size_width(value):
    """Update logo size (width)."""
    global LOGO_WIDTH

    # Try to convert the input value to a float and then to an integer
    try:
        float_value = float(value)
        int_value = int(float_value)
    except ValueError:
        int_value = 70  # Default value if conversion fails

    # Update the global LOGO_WIDTH variable with the integer value
    LOGO_WIDTH = int_value

    # Update the logo width input field with the new width value
    logo_width_input.delete(0, END)
    logo_width_input.insert(0, str(int_value))

    # Apply the watermark with the updated logo size
    apply_watermark()


def update_opacity():
    """Update opacity."""
    global OPACITY

    # Get the opacity value from the opacity input field and convert it to a float
    OPACITY = float(opacity_input.get())

    # Apply the watermark with the updated opacity
    apply_watermark()


def clockwise_rotation():
    """Rotate clockwise."""
    global ROTATION

    # Decrease the global rotation angle by 10 degrees
    ROTATION -= 10

    # Apply the watermark with the updated rotation
    apply_watermark()


# Function to rotate anticlockwise
def anticlockwise_rotation():
    """Rotate anticlockwise. Returns the result to the apply_watermark function."""
    global ROTATION

    # Increase the global rotation angle by 10 degrees
    ROTATION += 10

    # Apply the watermark with the updated rotation
    apply_watermark()


def move_up():
    """Move the watermark text up."""
    move_watermark(-10, 0)


# Function to move text down
def move_down():
    """Move the watermark text down."""
    move_watermark(10, 0)


# Function to move text left
def move_left():
    """Move the watermark text left."""
    move_watermark(0, -10)


# Function to move text right
def move_right():
    """Move the watermark text right."""
    move_watermark(0, 10)


# Function to move the watermark position
def move_watermark(vertical_shift, horizontal_shift):
    """Shift the watermark position and apply the updated watermark.
    Args:
        vertical_shift (int): Vertical shift value.
        horizontal_shift (int): Horizontal shift value."""
    global CENTER_HEIGHT, CENTER_WIDTH, IMAGE

    # Calculate the new position by shifting the current position
    new_center_height = max(0, min(FULL_HEIGHT, CENTER_HEIGHT + vertical_shift))
    new_center_width = max(0, min(FULL_WIDTH, CENTER_WIDTH + horizontal_shift))

    # Update the global variables with the new position
    CENTER_HEIGHT = new_center_height
    CENTER_WIDTH = new_center_width

    # Apply the watermark with the updated position
    apply_watermark()


# Function to create a text watermark
def create_watermark_text(original_image):
    """Create a watermark field and draw text into it.
    Args:
        original_image (Image): Original image in RGBA mode.
    Returns:
        Image: Watermark field with drawn text."""
    # Create a transparent watermark field with the same size as the original image
    watermark_field = Image.new("RGBA", original_image.size, (255, 255, 255, 0))

    # Set the initial text position to the center of the image
    text_position = (CENTER_WIDTH, CENTER_HEIGHT)

    # Create a tuple for opacity based on the global OPACITY variable
    opacity_tuple = (int(255 * OPACITY),)

    # Combine color and opacity for the watermark fill
    watermark_fill = COLOR + opacity_tuple

    # Create a drawing object
    draw = ImageDraw.Draw(watermark_field)

    # Load the specified font
    font = ImageFont.truetype(FONT, FONT_SIZE)

    # Calculate the bounding box of the text to determine its width and height
    text_bbox = draw.textbbox((text_position[0], text_position[1]), f"{watermark_input.get()}", font=font)

    # Calculate the position to center the text within the bounding box
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_position = (text_position[0] - text_width // 2, text_position[1] - text_height // 2)

    # Draw the text onto the watermark field
    draw.text(text_position, f"{watermark_input.get()}", fill=watermark_fill, font=font)

    # Return the resulting watermark field
    return watermark_field


def create_watermark_logo(original_image):
    """
    Function to create a logo watermark
    Args:
        original_image (Image): Original image in RGBA mode.
    Returns:
        Image: Watermark field with the applied logo.
    """
    global OPACITY, CENTER_WIDTH, CENTER_HEIGHT, LOGO_WIDTH, LOGO_HEIGHT, LOGO_FILE_PATH

    try:
        # Open the logo image and convert it to RGBA mode
        with Image.open(LOGO_FILE_PATH).convert("RGBA") as logo_image:
            # Resize the logo based on the user-defined scale
            resized_logo_width = int(LOGO_WIDTH * (size_scale.get() / 100.0))
            resized_logo_height = int(LOGO_HEIGHT * (size_scale.get() / 100.0))
            resized_logo = logo_image.resize((resized_logo_width, resized_logo_height), Image.LANCZOS)

            # Create a copy of the logo with alpha channel based on the global opacity
            logo_image_with_alpha = resized_logo.copy()
            logo_image_with_alpha.putalpha(int(255 * OPACITY))

            # Create a transparent watermark field with the same size as the original image
            watermark_field = Image.new("RGBA", original_image.size, (255, 255, 255, 0))

            # Calculate the position to paste the logo at the center of the image
            logo_position = (CENTER_WIDTH - resized_logo_width // 2, CENTER_HEIGHT - resized_logo_height // 2)

            # Update the global CENTER_HEIGHT and CENTER_WIDTH based on the logo position
            CENTER_HEIGHT = logo_position[1] + resized_logo_height // 2
            CENTER_WIDTH = logo_position[0] + resized_logo_width // 2

            # Paste the logo onto the watermark field
            watermark_field.paste(logo_image_with_alpha, logo_position, logo_image_with_alpha)

            # Return the resulting watermark field
            return watermark_field
    except FileNotFoundError:
        tkinter.messagebox.showerror("Error", "Logo file not found.")
        return None
    except PIL.UnidentifiedImageError:
        tkinter.messagebox.showerror("Error", "Invalid logo file extension.")
        return None


def resize_and_composite_images(original_image, watermark_field):
    """Resize and composite the original image and watermark field.
    Args:
        original_image (Image): Original image in RGBA mode.
        watermark_field (Image): Watermark field with drawn text or logo.
    Returns:
        Tuple[Image, Image]: Tuple containing resized original image and watermark."""
    # Rotate the watermark field based on the global rotation angle
    watermark_rotation = watermark_field.rotate(ROTATION, expand=False, resample=Resampling.BILINEAR)

    # Determine the new width and height based on the minimum dimensions of original and rotated watermark
    new_width = min(original_image.width, watermark_rotation.width)
    new_height = min(original_image.height, watermark_rotation.height)

    # Create a new RGBA image for the resized watermark
    resized_watermark = Image.new("RGBA", (new_width, new_height), (255, 255, 255, 0))
    resized_watermark.paste(watermark_rotation, (0, 0), watermark_rotation)

    # Create a new RGBA image for the resized original image
    resized_original = Image.new("RGBA", (new_width, new_height), (255, 255, 255, 0))
    resized_original.paste(original_image, (0, 0), original_image)

    # Return the resized original image and watermark
    return resized_original, resized_watermark


def apply_watermark():
    """Fetch the original image, create the appropriate watermark field (text or logo), resize and composite the
    original image and watermark, and update the display with the resulting image."""
    global FILE_PATH, IMAGE, IMAGE_COPY, FONT_SIZE, CENTER_HEIGHT, CENTER_WIDTH, ROTATION, COLOR, OPACITY, FONT, \
        FULL_HEIGHT, FULL_WIDTH, WATERMARK_TYPE

    # Open and prepare the original image
    original_image = open_and_prepare_image(FILE_PATH)
    watermark_field = None

    # Create watermark field based on the selected type (Text or Logo)
    if original_image:
        if WATERMARK_TYPE == "Text":
            watermark_field = create_watermark_text(original_image)
        elif WATERMARK_TYPE == "Logo":
            watermark_field = create_watermark_logo(original_image)

        # Resize and composite the original image and watermark
        if watermark_field:
            resized_original, resized_watermark = resize_and_composite_images(original_image, watermark_field)

            # Create an alpha-composited output image
            watermark_output = Image.alpha_composite(resized_original, resized_watermark)
            watermark_output_rgba = watermark_output.convert("RGBA")

            # Update the display with the resulting image
            update_image_display(watermark_output_rgba)

            # Update global variables
            IMAGE = watermark_output_rgba
            IMAGE_COPY = watermark_output_rgba.copy()
            IMAGE_COPY = IMAGE_COPY.resize((ORIGINAL_WIDTH, ORIGINAL_HEIGHT), Image.LANCZOS)


def set_watermark_type(variety):
    """Set the watermark type and adjust the GUI elements accordingly.

    Args:
        variety (str): The selected watermark type ("Text" or "Logo").
    """
    global WATERMARK_TYPE
    WATERMARK_TYPE = variety

    if WATERMARK_TYPE == "Text":
        # Show elements related to text watermark
        watermark_input.grid(column=4, row=3, columnspan=3, sticky='w')
        font_combobox.grid(column=4, row=4, columnspan=3, sticky='w', pady=(1, 1))
        font_label.grid(column=3, row=4)
        color_label.grid(column=3, row=5)
        color_preview_canvas.grid(column=6, row=5)
        color_input.grid(column=5, row=5, columnspan=2, sticky='w')
        choose_color_button.grid(column=4, row=5, sticky='w')

        # Hide elements related to logo watermark
        logo_file_button.grid_forget()
        logo_height_input.grid_forget()
        logo_height_label.grid_forget()
        logo_height_scale.grid_forget()
        logo_width_label.grid_forget()
        logo_width_input.grid_forget()
        logo_width_scale.grid_forget()

    elif WATERMARK_TYPE == "Logo":
        # Show/hide elements related to logo watermark
        watermark_input.grid_forget()
        watermark_label.config(text="Watermark Logo")
        logo_file_button.grid(column=4, row=3, columnspan=3, sticky='w', pady=(1, 1))
        logo_height_label.grid(column=3, row=5)
        logo_height_scale.grid(column=4, row=5, columnspan=2, sticky='w')
        logo_height_input.grid(column=6, row=5, pady=0)
        logo_width_label.grid(column=3, row=6)
        logo_width_scale.grid(column=4, row=6, columnspan=2, sticky='w')
        logo_width_input.grid(column=6, row=6, pady=0)

        # Hide elements related to text watermark
        size_input.grid_forget()
        size_label.grid_forget()
        size_scale.grid_forget()
        font_combobox.grid_forget()
        font_label.grid_forget()
        choose_color_button.grid_forget()
        color_input.grid_forget()
        color_label.grid_forget()
        color_preview_canvas.grid_forget()


def update_image_display(photo_image):
    """
    Update the displayed image with the given PhotoImage.
    Args:
        photo_image (ImageTk.PhotoImage): PhotoImage to be displayed.
    """
    # Convert the Image to PhotoImage for displaying in the tkinter window
    photo_image = ImageTk.PhotoImage(photo_image)

    # Configure the tkinter Label widget to display the new image
    image_square.configure(image=photo_image)
    image_square.image = photo_image


def save_image():
    """ Save the image with watermark. """
    global IMAGE_COPY

    try:
        # Check if there is a copy of the image with a watermark
        if IMAGE_COPY:
            # Ask the user for the save file path
            path = fd.asksaveasfilename(confirmoverwrite=True, defaultextension="png",
                                        filetypes=[("jpeg", ".jpg"), ("png", ".png"), ("bitmap", "bmp"),
                                                   ("gif", ".gif")])

            # Check if the user provided a file path
            if path:
                # Check the file extension and convert to RGB if saving as JPEG
                if os.path.splitext(path)[1] == ".jpg":
                    image_to_save = IMAGE_COPY.convert("RGB")
                    image_to_save.save(path)
                else:
                    # Save the image copy
                    IMAGE_COPY.save(path)

                # Show a success message
                tkinter.messagebox.showinfo("Success", "Image saved successfully!")

    # Handle any exceptions that might occur during the image saving process
    except Exception as e:
        tkinter.messagebox.showerror("Error", f"An error occurred while saving the image: {e}")


def reset_settings():
    """Reset all settings to their default values and delete the current watermark."""
    global CENTER_HEIGHT, CENTER_WIDTH, ROTATION, COLOR, OPACITY, FONT, FULL_HEIGHT, FULL_WIDTH, WATERMARK_TYPE
    global LOGO_WIDTH, LOGO_HEIGHT, LOGO_FILE_PATH

    # Reset position and rotation
    CENTER_HEIGHT = FULL_HEIGHT // 2
    CENTER_WIDTH = FULL_WIDTH // 2
    ROTATION = 0

    # Reset color, opacity, font, and watermark type
    COLOR = (255, 255, 255)
    OPACITY = 1.0
    FONT = "tahoma"
    WATERMARK_TYPE = "Text"
    set_watermark_type(WATERMARK_TYPE)

    # Reset logo dimensions and file path
    LOGO_WIDTH = 100
    LOGO_HEIGHT = 100
    LOGO_FILE_PATH = ""

    # Reset size scale, opacity input, font combobox, and watermark type combobox
    size_scale.set(100)
    opacity_input.set(1.0)
    font_combobox.set("tahoma")
    watermark_type_combobox.set("Text")

    # Reset input fields for size, logo height, logo width, and color
    watermark_input.delete(0, END)
    size_input.delete(0, END)
    size_input.insert(0, "70")
    logo_height_input.delete(0, END)
    logo_height_input.insert(0, str(LOGO_HEIGHT))
    logo_width_input.delete(0, END)
    logo_width_input.insert(0, str(LOGO_WIDTH))
    color_input.delete(0, END)
    color_preview_canvas.config(background="#FFFFFF")

    # Delete current watermark
    apply_watermark()


# -------------------------------WINDOW CONFIG---------------------------------------#

# Create themed Tkinter window
window = ThemedTk(theme="equilux")
window.title("Image Watermark App")
window.minsize(height=700, width=1000)
window.config(padx=50, pady=80, bg=BACKGROUND_COLOR)

# ---------------------------------IMAGE SQUARE--------------------------------------#

# Create an empty image for the initial display
empty_image = Image.new("RGBA", (700, 500), color=BACKGROUND_COLOR)
image = ImageTk.PhotoImage(empty_image)
image_square = ttk.Label(window, image=image, borderwidth=3)
image_square.image = image  # keep a reference
image_square.grid(column=0, rowspan=15, sticky='w')

# -------------------------------UPLOAD IMAGE BUTTON-------------------------------#

watermark_type_combobox = ttk.Combobox(window, values=["Text", "Logo"], width=14, font=("Ubuntu", 10))
watermark_type_combobox.grid(column=3, row=2, sticky='w', padx=20)
watermark_type_combobox.bind("<<ComboboxSelected>>", lambda event: set_watermark_type(watermark_type_combobox.get()))
watermark_type_combobox.set("Text")

# Style for custom button
button_style = ttk.Style()
button_style.configure("Custom.TButton", width=11, height=8, background="#fb8500", foreground="#FFAB59",
                       font=("Ubuntu", 9, "bold"))
upload_image_button = ttk.Button(window, text="Upload Image", style="Custom.TButton", command=open_file_dialog)
upload_image_button.grid(row=15, column=0, pady=10)

# -------------------------------WATERMARK LABEL------------------------------------#

# Label for watermark configuration
config_label = ttk.Label(text="Create your Watermark", background=BACKGROUND_COLOR, foreground='#fb8500',
                         font=("Ubuntu", 18, "bold"),
                         justify="center")
config_label.grid(column=3, row=1, columnspan=5, pady=(0, 15))

# Label and input for watermark text
watermark_label = ttk.Label(text="Watermark Text:", width=15, padding=[20, 0], background="#161a1d",
                            font=("Ubuntu", 12, "bold"))
watermark_label.grid(column=3, row=3, sticky='w')
watermark_input = ttk.Entry(width=33, font=("Ubuntu", 10, "bold"))
watermark_input.grid(column=4, row=3, columnspan=3, sticky='w')
watermark_input.get()
logo_file_button = ttk.Button(window, text="Choose Logo", command=choose_logo_file)
apply_button = ttk.Button(window, text="Apply", style="Custom.TButton", command=apply_watermark)
apply_button.grid(row=3, column=6)

# --------------------------------FONT LABEL---------------------------------------------#

# Get a list of available fonts and create a sorted list
available_fonts = get_ttf_fonts()
sorted_fonts = sorted(available_fonts)

# Label for font selection
font_label = ttk.Label(text="Font:", width=15, background="#161a1d", font=("Ubuntu", 12, "bold"))
font_label.grid(column=3, row=4)

# Combobox for font selection
font_combobox = ttk.Combobox(window, values=sorted_fonts, width=46, font=("Ubuntu", 10))
font_combobox.grid(column=4, row=4, columnspan=4, sticky='w', pady=(1, 1))
font_combobox.bind("<<ComboboxSelected>>", get_selected_font)
font_combobox.set("tahoma")

# --------------------------------COLOR LABEL------------------------------------------#

# Label for color selection
color_label = ttk.Label(text="Color:", width=15, background=BACKGROUND_COLOR, font=("Ubuntu", 12, "bold"))
color_label.grid(column=3, row=5)
# Canvas to display color preview
color_preview_canvas = Canvas(window,
                              width=20,
                              height=20,
                              background="#FFFFFF",
                              highlightthickness=0)
color_preview_canvas.grid(column=6, row=5)

# Entry and button for color input
color_input = ttk.Entry(width=18, font=("Ubuntu", 10))
color_input.grid(column=5, row=5, columnspan=2, sticky='w')
choose_color_button = ttk.Button(window, text="Choose Color", command=choose_color)
choose_color_button.grid(column=4, row=5, sticky='w')

# --------------------------------SIZE LABEL------------------------------------------#

# Label for font size selection
size_label = ttk.Label(text="Font Size:", background=BACKGROUND_COLOR, width=15, font=("Ubuntu", 12, "bold"))
size_label.grid(column=3, row=6)

# Scale and entry for font size input
current_size = IntVar(value=70)
current_size.set(FONT_SIZE)
size_scale = ttk.Scale(window, length=250, from_=3, to=250, orient=HORIZONTAL, command=update_watermark_size,
                       variable=current_size)
size_scale.grid(column=4, row=6, columnspan=2, sticky='w')

validate_size_input_cmd = window.register(validate_size_input)
size_input = ttk.Entry(width=6, font=("Ubuntu", 10), validate='key', textvariable=current_size,
                       validatecommand=(validate_size_input_cmd, '%P', '%d'))
size_input.grid(column=6, row=6, pady=0)

# --------------------------------LOGO SIZE LABEL--------------------------------------------#

logo_height_label = ttk.Label(text="Logo Height:", background=BACKGROUND_COLOR, width=15, font=("Ubuntu", 12, "bold"))
height_variable = IntVar(value=LOGO_HEIGHT)
logo_height_scale = ttk.Scale(window, length=250, from_=3, to=250, orient=HORIZONTAL, command=update_logo_size_height,
                              variable=height_variable)
logo_height_input = ttk.Entry(width=6, font=("Ubuntu", 10), validate='key', textvariable=height_variable,
                              validatecommand=(validate_size_input_cmd, '%P', '%d'))
width_variable = IntVar(value=LOGO_WIDTH)
logo_width_label = ttk.Label(text="Logo Width:", background=BACKGROUND_COLOR, width=15, font=("Ubuntu", 12, "bold"))
logo_width_scale = ttk.Scale(window, length=250, from_=3, to=250, orient=HORIZONTAL, command=update_logo_size_width,
                             variable=width_variable)
logo_width_input = ttk.Entry(width=6, font=("Ubuntu", 10), validate='key', textvariable=width_variable,
                             validatecommand=(validate_size_input_cmd, '%P', '%d'))

# --------------------------------OPACITY LABEL---------------------------------------------#

# Label for opacity selection
opacity_label = ttk.Label(text="Opacity:", background=BACKGROUND_COLOR, width=15, font=("Ubuntu", 12, "bold"))
opacity_label.grid(column=3, row=7)

# Spinbox to choose opacity values
opacity_input = ttk.Spinbox(from_=0.0, to=1.0, increment=0.1, format="%.1f", justify="center", width=5,
                            font=("Ubuntu", 10), command=update_opacity)
opacity_input.set(1.0)
opacity_input.grid(column=4, row=7, sticky='w')

# --------------------------------ROTATION LABEL------------------------------------------#

# Label for rotation selection
rotation_label = ttk.Label(text="Rotation:", width=15, background=BACKGROUND_COLOR, font=("Ubuntu", 12, "bold"))
rotation_label.grid(column=3, row=8)

# Buttons for clockwise and anticlockwise rotation
increment_rotation_button = ttk.Button(text="⭮", command=clockwise_rotation)
increment_rotation_button.grid(column=4, row=8, padx=20)

decrement_rotation_button = ttk.Button(text="⭯", command=anticlockwise_rotation)
decrement_rotation_button.grid(column=5, row=8, sticky='w', pady=20)

# --------------------------------POSITION LABEL------------------------------------------#

# Label for position selection
position_label = ttk.Label(text="Position:", width=15, background=BACKGROUND_COLOR, font=("Ubuntu", 12, "bold"))
position_label.grid(column=3, row=9)

# Buttons for moving text in different directions
position_up_button = ttk.Button(text="▲", width=4, command=move_up)
position_up_button.grid(column=5, row=9)

position_left_button = ttk.Button(text='◀', width=4, command=move_left)
position_left_button.grid(column=4, row=10, sticky='e')

position_right_button = ttk.Button(text='▶', width=4, command=move_right)
position_right_button.grid(column=6, row=10, sticky='w')

position_down_button = ttk.Button(text='▼', width=4, command=move_down)
position_down_button.grid(column=5, row=11)

# ------------------------------------ RESET BUTTON AND SAVE BUTTON ---------------------------#
save_button = ttk.Button(window, text="Save Image", style="Custom.TButton", command=save_image)
save_button.grid(row=14, column=6, sticky='w', pady=20)
reset_button = ttk.Button(window, text="Reset", style="Custom.TButton", command=reset_settings)
reset_button.grid(row=14, column=5, sticky='w', pady=20)

window.mainloop()
