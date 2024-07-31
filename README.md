# Image Watermark Desktop App

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![TkInter](https://img.shields.io/badge/TkInter-o?style=for-the-badge&logo=python&logoColor=yellow&labelColor=blue&color=blue)
![Pillow](https://img.shields.io/badge/Pillow-w?style=for-the-badge&logo=python&logoColor=orange&labelColor=hsl(0%2C%200%25%2C%2090%25)&color=hsl(0%2C%200%25%2C%2090%25))

## Overview
#### This is a simple desktop application for adding watermarks to images. The application allows you to choose between a logo or text watermark.

## Features
#### Adding Watermark
1. Choose the watermark type (Logo or Text) from the dropdown menu.
![Text mode](./screenshots/Zrzut%20ekranu%202024-02-01%20135937.png)

![Change mode](./screenshots/Zrzut%20ekranu%202024-02-01%20140422.png)

![Logo mode](./screenshots/Zrzut%20ekranu%202024-02-02%20090252.png)

2. Provide the necessary information based on the selected type:
- For Logo: Enter the path to your logo image file.

![Choose logo path](./screenshots/Zrzut%20ekranu%202024-02-02%20090413.png)

- For Text: Enter the desired watermark text.

3. Adjust other settings such as transparency, color and position.
![Choose color](./screenshots/Zrzut%20ekranu%202024-02-01%20140343.png)

4. Click the "Apply Watermark" button to add the watermark to the selected image.
![Logo watermark](./screenshots/Zrzut%20ekranu%202024-02-02%20091249.png)

#### Saving Watermarked Image
After applying the watermark, you can save the watermarked image by following these steps:

1. Click the "Save" button.

2. Choose the destination folder and enter the desired filename.
![Save image](./screenshots/Zrzut%20ekranu%202024-02-02%20091349.png)


3. Click "Save" to save the watermarked image.

#### Resetting Watermark Settings
If you want to reset the watermark settings:

1. Click the "Reset" button.

2. Note: The watermark type will default to "Text" after the reset. You can then choose "Logo" again if needed.
-Choose between adding a text or logo watermark to your images.


## Getting Started
### Prerequisites
- Python 3.11
- Required Python packages (install using pip install -r requirements.txt)

## Installation
1. Clone the repository:
```bash 
git clone https://github.com/toster3d/Watermark-desktop-app.git
```
```bash
cd Image-Watermark-Desktop-App
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```
## Usage
1. Run the application:
```bash
python main.py
```
2. Open an image using the "File" menu.

3. Customize the watermark using the provided controls.

4. Click the "Apply Watermark" button to see the changes.

5. Save your watermarked image using the "Save" button.

## Issues and Contributions
If you encounter any issues or have suggestions for improvements, feel free to open an issue or create a pull request.

Enjoy watermarking your images!
## Author
Jagoda Spychala
