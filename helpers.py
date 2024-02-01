import PIL
from PIL import Image
import tkinter.messagebox
import matplotlib.font_manager as fm


def get_ttf_fonts():
    """
    Retrieve a list of available TrueType Fonts (TTF).

    This function searches for TTF font files installed in the system and returns a list
    of font names without file extensions.

    Returns:
        List[str]: A list of available TrueType Fonts (TTF) installed in the system.
    """
    # Find system fonts with the TrueType font extension (.ttf)
    ttf_fonts = fm.findSystemFonts(fontpaths=None, fontext='ttf')

    # Initialize an empty list to store formatted font names
    fonts_list = []

    # Extract font names and remove file extensions
    formatted_fonts = [x.split("\\")[-1] for x in ttf_fonts]

    # Filter out OpenType fonts (.otf) and create a list of font names
    for f in formatted_fonts:
        if ".otf" not in f:
            fonts_list.append(f.replace(".ttf", "").replace(".TTF", "").replace(".ttc", ""))

    return fonts_list




def hex_to_rgba(hex_color):
    """
Convert hex color to RGBA.
Args:
    hex_color (str): Hexadecimal representation of the color.
Returns:
    Tuple[int, int, int, int]: RGBA values as a tuple.
"""
    # Remove '#' if present and convert pairs of hex digits to integers
    hex_color = hex_color.lstrip('#')
    # Convert a color represented in hexadecimal format (hex) to an RGBA tuple.
    # Iterate over three color components (R, G, B), transforming two hexadecimal digits into numerical values.
    # Return a tuple of four integers representing the color components: (R, G, B, A).
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def validate_size_input(value, action):
    """
    Validate size input.
    Args:
        value (str): The value to be validated.
        action (str): The type of action triggering the validation.
    Returns:
        bool: True if the size input is valid, False otherwise.
    """
    # Check if the action is an insertion (typing)
    if action == '1':
        try:
            # Attempt to convert the input value to an integer
            int_value = int(value)

            # Check if the integer value is within the valid range [1, 250]
            if 1 <= int_value <= 250:
                return True
            else:
                return False

        # Handle ValueError (non-integer input)
        except ValueError:
            return False

    # For other actions (deletion, etc.), consider the input as valid
    return True


def open_and_prepare_image(file_path):
    """
    Open and prepare an image for applying a watermark.

    Args:
        file_path (str): Path to the image file.

    Returns:
        Image: Prepared original image in RGBA mode.
            Returns None if an error occurs.
    """
    try:
        # Open the image and convert it to RGBA mode
        original_image = Image.open(file_path).convert("RGBA")

        # Resize the image to a thumbnail with a maximum size of 700x500 pixels
        original_image.thumbnail(size=(700, 500))

        # Return the prepared original image
        return original_image

    # Handle FileNotFoundError by displaying an error message
    except FileNotFoundError:
        tkinter.messagebox.showerror("Error", "File not found.")
        return None

    # Handle PIL.UnidentifiedImageError by displaying an error message
    except PIL.UnidentifiedImageError:
        tkinter.messagebox.showerror("Error", "Invalid file extension.")
        return None

    # Handle other exceptions by displaying the specific error message
    except Exception as e:
        tkinter.messagebox.showerror("Error", f"{e}.")
        return None
