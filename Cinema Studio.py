from tkinter import Tk, Frame, Label, Button, FLAT
from PIL import Image, ImageTk

class Cinema:
    
    @staticmethod
    def on_button_click():
        print("hello!")
    
    def __init__(self, parent):
        self.parent = parent

        # Load and resize images using Pillow
        image_paths = [
            r"C:\Users\xavie\Downloads\image-from-rawpixel-id-9975454-original.jpg",
            r"C:\Users\xavie\Downloads\image-from-rawpixel-id-9976112-original.jpeg",
            r"C:\Users\xavie\Downloads\image-from-rawpixel-id-9976560-original.jpg",
            r"C:\Users\xavie\Downloads\image-from-rawpixel-id-9976063-original.jpg"
        ]
        desired_size = (130, 193)
        self.photos = []

        for path in image_paths:
            image = Image.open(path)
            resized_image = image.resize(desired_size, Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(resized_image)
            self.photos.append(photo)

        # Cinema Frame
        self.cinema_frame = Frame(parent, bg="#14213D")
        self.cinema_frame.grid(column=1)

        self.cinema_heading = Label(
            self.cinema_frame, text="RIZZ Cinema", font=("Poppins", "18", "bold"),
            fg="#FCA311", bg="#19294D", width=40, height=2
        )
        self.cinema_heading.grid(row=0)

        self.cinema_showing = Label(
            self.cinema_frame, text="Now showing", font=("Poppins", "11", "bold"),
            fg="#FFFFFF", bg="#14213D"
        )
        self.cinema_showing.grid(row=1, columnspan=4, sticky="WE")

        # Frame for Movies all together
        self.movie_frame = Frame(self.cinema_frame, bg="#14213D")
        self.movie_frame.grid(row=2)

        # Frame for Side Tab
        self.side_tab = Frame(parent, bg="#19294D", width=10
                              )
        self.side_tab.grid(row=0, column=0, sticky="NS")

        self.side_tab_logo = Label(self.side_tab, text="R", font=("Poppins", "35", "bold"),
                fg="#FCA311", bg="#19294D", justify="left"
            )
        self.side_tab_logo.grid(row= 0, pady=10)

        side_tab_labels = ["", "Movies", "Session Times", "Cinemas", "Food & Snacks"]
        for i, text in enumerate(side_tab_labels):
            label = Label(
                self.side_tab, text=text, font=("Poppins", "13"),
                fg="#FFFFFF", bg="#19294D", anchor="w"
            )
            label.grid(row=i+1, pady=5, padx=10, sticky="WE")

        # Frames and buttons for movies
        movie_titles = ["Movie One", "Movie Two", "Movie Three", "Movie Four"]
        for i, (photo, title) in enumerate(zip(self.photos, movie_titles)):
            movie_frame = Frame(self.movie_frame, bg="#14213D")
            movie_frame.grid(row=0, column=i, pady=5)

            movie_button = Button(
                movie_frame, image=photo, command=Cinema.on_button_click, bd=0, relief=FLAT
            )
            movie_button.image = photo
            movie_button.grid(row=0, column=0, padx=5, pady=5)

            movie_label = Label(
                movie_frame, text=title, font=("Poppins", "11", "bold"),
                fg="#FFFFFF", bg="#14213D"
            )
            movie_label.grid(row=1)


# main routine    
if __name__ == "__main__":
    root = Tk()
    root.title("Cinema")
    Cinema(root)
    root.mainloop()
