import os
from tkinter import *
from tkinter import messagebox, filedialog
from PIL import Image, ImageFont, ImageDraw
import math

file_path = None
# get file path


def getpath():
    global file_path
    file_path = filedialog.askopenfilename(title='Choose a file')
    return file_path

# custom watermark procedure


def run_program():
    if file_path and text_entry.get() != 'Enter Text...':
        with Image.open(file_path).convert("RGBA") as base:
            txt_side = int(math.sqrt(base.size[0] ** 2 + base.size[1] ** 2) * 1.25)
            txt_size = (txt_side, txt_side)
            # make a blank image for the text, initialized to transparent text color
            txt = Image.new("RGBA", txt_size, (255, 255, 255, 0))

            # get a font
            fnt = ImageFont.truetype("Fira_Sans/FiraSans-Regular.ttf", 50)
            # get a drawing context
            d = ImageDraw.Draw(txt)

            # draw repeating text on multiple lines, half opacity
            i = 0
            length = len(text_entry.get()) * 29

            for y in range(-100, txt_side, 70):
                start = (i % 2) * -150
                for x in range(start, txt_side, length):
                    d.text((x, y), text_entry.get(), font=fnt, fill=(255, 255, 255, 50))

                i += 1

            # rotate the text image and paste it to the base image
            w = txt.rotate(45)
            base.paste(im=w, box=(-int(base.size[0] / 10), -int(base.size[1] / 2) - 50), mask=w)

            # get file name and save the new image as a PNG file
            filename, ext = os.path.splitext(file_path)
            base.show()
            base.save(filename + "-watermarked.png", 'PNG')

    # Error messages for empty variables
    elif file_path and text_entry.get() == 'Enter Text...':
        messagebox.showerror(title="ERROR", message="Please enter a text!")

    else:
        messagebox.showerror(title="ERROR", message="Please choose a photo!")


# Set the GUI
window = Tk()
window.title('Translucent | Add Custom Watermarks to Photos')
window.config(pady=20, padx=20, bg="sky blue")

canvas = Canvas(width=1220, height=500, bg="white", highlightthickness=0)
img = PhotoImage(file="images/translucent.png")
canvas.create_image(610, 250, image=img)
canvas.grid(row=0, column=0, columnspan=4, rowspan=3)

photo = Label(text="Image:", width=10, bg="sky blue", font=("Arial", 12, 'bold'), borderwidth=1)
photo.grid(row=2, column=0)

photo_file = Button(text='Choose a photo', width=30, activebackground='blue', activeforeground='white',
                    command=getpath)
photo_file.grid(row=2, column=1)
photo_file.focus()

text_label = Label(text="Text:", width=10, bg="sky blue", font=("Arial", 12, 'bold'), borderwidth=1)
text_label.grid(row=2, column=2)

text_entry = Entry(width=70, font=("Arial", 12))
text_entry.grid(row=2, column=3)
text_entry.insert(END, "Enter Text...")

run_btn = Button(text="Add Watermark", font=("Arial", 12, 'bold'), width=20, activebackground='blue',
                 activeforeground='white', command=run_program)
run_btn.grid(row=3, column=3, columnspan=2, pady=10, ipady=10, sticky='E')

window.mainloop()
