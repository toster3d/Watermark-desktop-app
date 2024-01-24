from tkinter import *
from tkinter import filedialog as fd, ttk
import tkinter.font as tkFont
import matplotlib.font_manager as fm
from tkinter.colorchooser import askcolor
import tkinter.messagebox
import PIL
from PIL import Image, ImageDraw, ImageFont, ImageTk
from PIL import UnidentifiedImageError

from tkinter.colorchooser import askcolor
from ttkthemes import ThemedTk, ThemedStyle
import os

BACKGROUND_COLOR = "#161a1d"
FILE_PATH = ""
IMAGE = ""
FONT = "tahoma"
print(FONT)
FONT_PATH = ""
COLOR = ""
OPACITY = 1.0
FONT_SIZE = 70
ORIGINAL_HEIGHT = 0
ORIGINAL_WIDTH = 0
HEIGHT = 0
WIDTH = 0
ROTATION = 0
COLOR = (255, 255, 255)


def open_file_dialog():
    global FILE_PATH
    file_path = fd.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
    if file_path:
        update_image(file_path)
        FILE_PATH = file_path
        print(FILE_PATH)


def update_image(file_path):
    global HEIGHT, WIDTH, ORIGINAL_HEIGHT, ORIGINAL_WIDTH, IMAGE
    photo = Image.open(file_path)
    photo.thumbnail(size=(800, 600))
    new_image = ImageTk.PhotoImage(photo)
    image_square.config(image=new_image)
    image_square.image = new_image
    ORIGINAL_HEIGHT = photo.size[1]
    HEIGHT = ORIGINAL_HEIGHT // 2
    ORIGINAL_WIDTH = photo.size[0]
    WIDTH = ORIGINAL_WIDTH // 2
    IMAGE = photo  # Save the PhotoImage for later use
    print(HEIGHT)
    print(WIDTH)


def get_selected_font(*args):
    global FONT
    FONT = font_combobox.get()
    apply_watermark()
    print(FONT)


def hex_to_rgba(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def choose_color():
    global COLOR
    color_dialog = askcolor()
    if color_dialog:
        hex_color = color_dialog[1]
        rgba_color = hex_to_rgba(hex_color)

        color_input.delete(0, END)
        color_input.insert(0, rgba_color)

        color_preview_canvas.config(bg=hex_color)
        COLOR = rgba_color
        print(COLOR)



def validate_size_input(value, action):
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


def update_watermark_size(value):
    try:
        float_value = float(value)
        int_value = int(float_value)
    except ValueError:
        int_value = 70  # Domyślna wartość dla przypadku nieudanej konwersji
    global FONT_SIZE
    FONT_SIZE = int_value
    print(FONT_SIZE)
    size_input.delete(0, END)
    size_input.insert(0, str(int_value))
    apply_watermark()


def update_opacity():
    print(opacity_input.get())
    global OPACITY
    OPACITY = float(opacity_input.get())
    apply_watermark()


# def update_size(value):
#     global FONT_SIZE
#     FONT_SIZE = int(value.get())
#     apply_watermark()
#     # size_input.delete(0, END)
#     # size_input.insert(0, value)


def clockwise_rotation():
    global ROTATION
    ROTATION += 20
    print(ROTATION)
    # new_rotation = (current_rotation + 5) % 360  # Zwiększ obrot o 10 stopni
    apply_watermark()


def anticlockwise_rotation():
    global ROTATION
    ROTATION -= 20
    print(ROTATION)
    apply_watermark()

def move_up():
    global HEIGHT, ORIGINAL_HEIGHT
    print(HEIGHT)
    if HEIGHT < ORIGINAL_HEIGHT:
        HEIGHT = max(0, HEIGHT - 10)
        print(HEIGHT)
    apply_watermark()



def move_down():
    global HEIGHT, ORIGINAL_HEIGHT
    print(HEIGHT)
    if HEIGHT < ORIGINAL_HEIGHT:
        HEIGHT = max(0, HEIGHT + 10)
        print(HEIGHT)
    apply_watermark()


def move_left():
    global WIDTH, ORIGINAL_WIDTH
    print(WIDTH)
    if WIDTH < ORIGINAL_WIDTH:
        WIDTH = min(ORIGINAL_WIDTH, WIDTH - 10)
        print(WIDTH)
        apply_watermark()


def move_right():
    global WIDTH, ORIGINAL_WIDTH
    print(WIDTH)
    if WIDTH < ORIGINAL_WIDTH:
        WIDTH = min(ORIGINAL_WIDTH, WIDTH + 10)
        print(WIDTH)
        apply_watermark()

def apply_watermark():
    global FILE_PATH, IMAGE, FONT_SIZE, HEIGHT, WIDTH, ROTATION, COLOR, OPACITY, FONT

    try:
        print(f"Otwieranie pliku: {FILE_PATH}")
        with Image.open(FILE_PATH).convert("RGBA") as original_image:
            print("Tworzenie pola znaku wodnego")

            # Ustaw rozmiar pola znaku wodnego na oryginalny rozmiar obrazu
            watermark_field = Image.new("RGBA", original_image.size, (255, 255, 255, 0))

            print(f"Tekst znaku wodnego: {watermark_input.get()}")

            # Ustaw pozycję tekstu
            text_position = (WIDTH, HEIGHT)

            # Zadeklaruj kolor tekstu
            opacity_tuple = (int(255 * OPACITY),)
            watermark_fill = COLOR + opacity_tuple
            print(f"Kolor tekstu: {watermark_fill}")

            # Narysuj tekst na polu znaku wodnego
            draw = ImageDraw.Draw(watermark_field)
            font = ImageFont.truetype(FONT, FONT_SIZE)
            draw.text(text_position, f"{watermark_input.get()}", fill=watermark_fill, font=font)

            print("Obracanie pola znaku wodnego")
            watermark_rotation = watermark_field.rotate(ROTATION, expand=True)  # Rozszerz obraz, aby pomieścił obroty

            print("Kompresja alfa")
            watermark_output = Image.alpha_composite(original_image, watermark_rotation)

            print("Konwersja na RGBA")
            watermark_output_rgba = watermark_output.convert("RGBA")

            print("Tworzenie PhotoImage")
            photo_image = ImageTk.PhotoImage(watermark_output_rgba)

            print("Aktualizacja image_square")
            image_square.configure(image=photo_image)
            image_square.image = photo_image

            IMAGE = watermark_output_rgba

    except FileNotFoundError:
        tkinter.messagebox.showerror("Błąd", "Brak pliku.")
    except PIL.UnidentifiedImageError:
        tkinter.messagebox.showerror("Błąd", "Nieprawidłowe rozszerzenie pliku.")
    except Exception as e:
        print(f"Błąd: {e}")
        pass



# -------------------------------WINDOW CONFIG---------------------------------------#

window = ThemedTk(theme="equilux")
window.title("Image Watermark App")
window.minsize(height=800, width=1100)
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# ---------------------------------IMAGE SQUARE----------------------------------#

empty_image = Image.new("RGBA", (800, 600), color=BACKGROUND_COLOR)
image = ImageTk.PhotoImage(empty_image)
image_square = ttk.Label(window, image=image, borderwidth=3)
image_square.image = image  # keep a reference
image_square.grid(column=0, rowspan=15, sticky='w')

# -------------------------------UPLOAD IMAGE BUTTON-------------------------------#
button_style = ttk.Style()
button_style.configure("Custom.TButton", width=13, background="#fb8500", foreground="#FFAB59",
                       font=("Ubuntu", 13, "bold"))
upload_button = ttk.Button(window, text="Upload Image", style="Custom.TButton", command=open_file_dialog)
upload_button.grid(row=15, column=0, pady=10)

# -------------------------------WATERMARK LABEL------------------------------------#
config_label = ttk.Label(text="Create your Watermark", background=BACKGROUND_COLOR, foreground='#fb8500',
                         font=("Ubuntu", 18, "bold"),
                         justify="center")
config_label.grid(column=3, row=1, columnspan=4, pady=(0, 15))
watermark_label = ttk.Label(text="Watermark Text:", width=15, padding=[20, 0], background="#161a1d",
                            font=("Ubuntu", 12, "bold"))
watermark_label.grid(column=3, row=2, sticky='w')
watermark_input = ttk.Entry(width=47, font=("Ubuntu", 10, "bold"))
watermark_input.grid(column=4, row=2, columnspan=3, sticky='w')
watermark_input.get()


# --------------------------------FONT LABEL------------------------------------------#
def get_ttf_fonts():
    # Pobierz listę dostępnych czcionek TTF
    ttf_fonts = fm.findSystemFonts(fontpaths=None, fontext='ttf')
    fonts_list = []
    formated_fonts = [x.split("\\")[-1] for x in ttf_fonts]
    for f in formated_fonts:
        if ".otf" not in f:
            fonts_list.append(f.replace(".ttf", "").replace(".TTF", "").replace(".ttc", ""))
    return fonts_list


available_fonts = get_ttf_fonts()
sorted_fonts = sorted(available_fonts)
font_label = ttk.Label(text="Font:", width=15, background="#161a1d", font=("Ubuntu", 12, "bold"))
font_label.grid(column=3, row=3)
all_fonts = tkFont.families()
font_combobox = ttk.Combobox(window, values=sorted_fonts, width=45, font=("Ubuntu", 10))
font_combobox.grid(column=4, row=3, columnspan=3, sticky='w', pady=(1, 1))
font_combobox.bind("<<ComboboxSelected>>", get_selected_font)
font_combobox.set("tahoma")

# --------------------------------COLOR LABEL------------------------------------------#
color_label = ttk.Label(text="Color:", width=15, background=BACKGROUND_COLOR, font=("Ubuntu", 12, "bold"))
color_label.grid(column=3, row=4)

color_preview_canvas = Canvas(window,
                              width=20,
                              height=20,
                              background="#FFFFFF",
                              highlightthickness=0)
color_preview_canvas.grid(column=6, row=4)

color_input = ttk.Entry(width=18, font=("Ubuntu", 10))
color_input.grid(column=5, row=4, columnspan=2, sticky='w')

choose_color_button = ttk.Button(window, text="Choose Color", command=choose_color)
choose_color_button.grid(column=4, row=4, sticky='w')

# --------------------------------SIZE LABEL------------------------------------------#

size_label = ttk.Label(text="Font Size:", background=BACKGROUND_COLOR, width=15, font=("Ubuntu", 12, "bold"))
size_label.grid(column=3, row=5)
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

opacity_label = ttk.Label(text="Opacity:", background=BACKGROUND_COLOR, width=15, font=("Ubuntu", 12, "bold"))
opacity_label.grid(column=3, row=6)

# Spinbox dla wyboru wartości opacity
opacity_input = ttk.Spinbox(from_=0.0, to=1.0, increment=0.1, format="%.1f", justify="center", width=5,
                            font=("Ubuntu", 10), command=update_opacity)
opacity_input.set(1.0)
opacity_input.grid(column=4, row=6, sticky='w')

# --------------------------------ROTATION LABEL------------------------------------------#

rotation_label = ttk.Label(text="Rotation:", width=15, background=BACKGROUND_COLOR, font=("Ubuntu", 12, "bold"))
rotation_label.grid(column=3, row=7)

# Przyciski do zwiększania i zmniejszania wartości rotation
increment_rotation_button = ttk.Button(text="⭮", command=clockwise_rotation)
increment_rotation_button.grid(column=4, row=7, sticky='e', padx=20)

decrement_rotation_button = ttk.Button(text="⭯", command=anticlockwise_rotation)
decrement_rotation_button.grid(column=5, row=7, sticky='w', pady=20)

# --------------------------------POSITION LABEL------------------------------------------#

position_label = ttk.Label(text="Position:", width=15, background=BACKGROUND_COLOR, font=("Ubuntu", 12, "bold"))
position_label.grid(column=3, row=8)

position_up_button = ttk.Button(text="▲", width=4, command=move_up)
position_up_button.grid(column=5, row=8)

position_left_button = ttk.Button(text='◀', width=4, command=move_left)
position_left_button.grid(column=4, row=9, sticky='e')

position_right_button = ttk.Button(text='▶', width=4, command=move_right)
position_right_button.grid(column=6, row=9, sticky='w')

position_down_button = ttk.Button(text='▼', width=4, command=move_down)
position_down_button.grid(column=5, row=10)

upload_button = ttk.Button(window, text="Apply", style="Custom.TButton", command=apply_watermark)
upload_button.grid(row=14, column=3, columnspan=2)
upload_button = ttk.Button(window, text="Save Image", style="Custom.TButton")
upload_button.grid(row=14, column=5, sticky='e')
window.mainloop()
#
