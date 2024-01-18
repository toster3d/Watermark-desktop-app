from tkinter import *
from tkinter import filedialog as fd, ttk
import tkinter.font as tkFont
from tkinter.colorchooser import askcolor
import tkinter.messagebox
import PIL
from PIL import Image, ImageDraw, ImageFont, ImageTk
from tkinter.colorchooser import askcolor
from ttkthemes import ThemedTk, ThemedStyle

BACKGROUND_COLOR = "#161a1d"



def open_file_dialog():
    file_path = fd.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
    if file_path:
        update_image(file_path)


def update_image(file_path):
    photo = Image.open(file_path)
    photo.thumbnail(size=(800, 600))
    new_image = ImageTk.PhotoImage(photo)
    image_square.config(image=new_image)
    image_square.image = new_image


def get_selected_font(event):
    selected_font = font_combobox.get()
    return selected_font


def choose_color():
    pass
    color = askcolor()[1]
    color_input.delete(0, END)
    color_input.insert(0, color)
    color_preview_canvas.config(bg=color)

def validate_size_input(value, action):
    if action == '1':
        try:
            int_value = int(value)
            if 1 <= int_value <= 100:
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
        int_value = 10  # Domyślna wartość dla przypadku nieudanej konwersji

    size_input.delete(0, END)
    size_input.insert(0, str(int_value))



#
# def update_size(value):
#     pass
#     size_input.delete(0, END)
#     size_input.insert(0, value)

def increment_rotation():
    pass
    current_rotation = 0
    new_rotation = (current_rotation + 5) % 360  # Zwiększ obrot o 10 stopni
    apply_watermark()


def decrement_rotation():
    pass
    current_rotation = int(rotation_input.get())
    new_rotation = (current_rotation - 10) % 360  # Zmniejsz obrot o 10 stopni
    rotation_input.delete(0, END)
    rotation_input.insert(0, new_rotation)

def apply_watermark():
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
config_label = ttk.Label(text="Create your Watermark", background=BACKGROUND_COLOR, foreground='#fb8500', font=("Ubuntu", 18, "bold"),
                         justify="center")
config_label.grid(column=3, row=1, columnspan=4, pady=(0, 15))
watermark_label = ttk.Label(text="Watermark Text:", width=15, padding=[20, 0], background="#161a1d",
                            font=("Ubuntu", 12, "bold"))
watermark_label.grid(column=3, row=2, sticky='w')
watermark_input = ttk.Entry(width=47, font=("Ubuntu", 10, "bold"))
watermark_input.grid(column=4, row=2, columnspan=3, sticky='w')
watermark_input.get()

# --------------------------------FONT LABEL------------------------------------------#

font_label = ttk.Label(text="Font:", width=15, background="#161a1d", font=("Ubuntu", 12, "bold"))
font_label.grid(column=3, row=3)
all_fonts = tkFont.families()
font_combobox = ttk.Combobox(window, values=all_fonts, width=45, font=("Ubuntu", 10))
font_combobox.grid(column=4, row=3, columnspan=3, sticky='w', pady=(1, 1))
font_combobox.bind("<<ComboboxSelected>>", get_selected_font)
# font_combobox.set(all_fonts[0])
print(font_combobox.get())

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

size_label = ttk.Label(text="Size:", background=BACKGROUND_COLOR, width=15, font=("Ubuntu", 12, "bold"))
size_label.grid(column=3, row=5)

size_scale = ttk.Scale(window, length=250, from_=1, to=100, orient=HORIZONTAL, command=update_watermark_size)
size_scale.grid(column=4, row=5, columnspan=2, sticky='w')

validate_size_input_cmd = window.register(validate_size_input)
size_input = ttk.Entry(width=6, font=("Ubuntu", 10), validate='key', validatecommand=(validate_size_input_cmd, '%P', '%d'))
size_input.grid(column=6, row=5, pady=0)

# --------------------------------OPACITY LABEL------------------------------------------#

opacity_label = ttk.Label(text="Opacity:", background=BACKGROUND_COLOR, width=15, font=("Ubuntu", 12, "bold"))
opacity_label.grid(column=3, row=6)

# Spinbox dla wyboru wartości opacity
opacity_input = ttk.Spinbox(window, from_=0.0, to=1.0, increment=0.1, format="%.1f", justify="center", width=5, font=("Ubuntu", 10))
opacity_input.grid(column=4, row=6, sticky='w')


# --------------------------------ROTATION LABEL------------------------------------------#

rotation_label = ttk.Label(text="Rotation:", width=15, background=BACKGROUND_COLOR, font=("Ubuntu", 12, "bold"))
rotation_label.grid(column=3, row=7)

# Przyciski do zwiększania i zmniejszania wartości rotation
increment_rotation_button = ttk.Button(text="⭮", command=increment_rotation)
increment_rotation_button.grid(column=4, row=7, sticky='e', padx=20)

decrement_rotation_button = ttk.Button(text="⭯", command=decrement_rotation)
decrement_rotation_button.grid(column=5, row=7, sticky='w', pady=20)



position_label = ttk.Label(text="Position:", width=15, background=BACKGROUND_COLOR, font=("Ubuntu", 12, "bold"))
position_label.grid(column=3, row=8)

position_up_button = ttk.Button(text="▲", width=4)
position_up_button.grid(column=5, row=8)

position_left_button = ttk.Button(text='◀', width=4)
position_left_button.grid(column=4, row=9, sticky='e')

position_right_button = ttk.Button(text='▶', width=4)
position_right_button.grid(column=6, row=9, sticky='w')

position_down_button = ttk.Button(text='▼', width=4)
position_down_button.grid(column=5, row=10)

upload_button = ttk.Button(window, text="Apply", style="Custom.TButton", command=apply_watermark)
upload_button.grid(row=14, column=3, columnspan=2)
upload_button = ttk.Button(window, text="Save Image", style="Custom.TButton", command=apply_watermark)
upload_button.grid(row=14, column=5, sticky='e')
window.mainloop()
#