from tkinter import *
from PIL import Image, ImageTk
from functools import partial

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


        self.cinema_showing = Label(
            self.cinema_frame, text="Now showing:", font=("Bahnschrift Light Condensed", "17"),
            fg="#FFFFFF", bg="#14213D", anchor="w"
        )
        self.cinema_showing.grid(row=1, columnspan=4, sticky="WE", padx=5, pady=5)

        # Frame for Movies all together
        self.movie_frame = Frame(self.cinema_frame, bg="#14213D")
        self.movie_frame.grid(row=2)

        # Frame for Side Tab
        self.side_tab = Frame(parent, bg="#19294D", width=10
                              )
        self.side_tab.grid(row=0, column=0, sticky="NS")

        self.canvas = Canvas(self.side_tab, width=130, height=70, bg="#19294D", bd=0, highlightthickness=0)
        self.canvas.grid(row=0, column=0)

        self.canvas.create_text(10, -1, text="RIZZ", font=("Britannic Bold", "35"), fill="#FCA311", anchor="nw")

        self.canvas.create_text(11, 40, text="Cinemas", font=("Bahnschrift Light Condensed", "17"), fill="#FCA311", anchor="nw")


        side_tab_labels = ["", "Movies", "Session Times", "Cinemas", "Food & Snacks"]
        for i, text in enumerate(side_tab_labels):
            label = Label(
                self.side_tab, text=text, font=("Bahnschrift Light Condensed", "15"),
                fg="#FFFFFF", bg="#19294D", anchor="w"
            )
            label.grid(row=i+1, padx=10, sticky="WE")
        
        self.setup_movie_frames()

    def setup_movie_frames(self):
        # Frames and buttons for movies
        movie_titles = ["King Kong", "Movie Two", "Movie Three", "Movie Four"]
        self.movie_buttons = []
        for i, (photo, title) in enumerate(zip(self.photos, movie_titles)):
            movie_frame = Frame(self.movie_frame, bg="#14213D")
            movie_frame.grid(row=0, column=i+1, pady=5)

            def create_movie_button_callback(index):
                def callback():
                    self.on_movie_button_click(index)
                return callback

            movie_button = Button(
                movie_frame, image=photo, command=create_movie_button_callback(i), bd=0, relief=FLAT
            )
            movie_button.image = photo
            movie_button.grid(row=0, column=0, padx=5, pady=5)

            movie_label = Label(
                movie_frame, text=title, font=("Bahnschrift Light Condensed", "13", "bold"),
                fg="#FFFFFF", bg="#14213D"
            )
            movie_label.grid(row=1)

            self.movie_buttons.append(movie_button)

    def on_movie_button_click(self, index):
        # Define separate functions for each movie button action
        if index == 0:
            self.displaying_movie(index)
        elif index == 1:
            self.show_movie_two()
        elif index == 2:
            self.show_movie_three()
        elif index == 3:
            self.show_movie_four()

    def displaying_movie(self, index):
        for button in self.movie_buttons:
            button.config(state=DISABLED)        

        Movie(self, index)

    def enable_all_buttons(self):
        for button in self.movie_buttons:
            button.config(state=NORMAL)
    
    

    def show_movie_two(self):
        print("Showing details for Movie Two")

    def show_movie_three(self):
        print("Showing details for Movie Three")

    def show_movie_four(self):
        print("Showing details for Movie Four")

    
class Movie:

    def __init__(self, partner, index):
        background = "#14213D"
        self.movie_box = Toplevel()

        image_path = r"C:\Users\xavie\Downloads\image-from-rawpixel-id-9975454-original.jpg"
        image_path1 = r"C:\Users\xavie\OneDrive\Documents\PRG ASSESMENT\King kong banner.jpg"
        image1 = Image.open(image_path1)
        image = Image.open(image_path)

        desired_width = 100
        desired_height = 143

        resized_image1 = image1.resize((400, 220), Image.Resampling.LANCZOS)
        resized_image = image.resize((desired_width, desired_height), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(resized_image)  # Save reference to the image
        self.photo1 = ImageTk.PhotoImage(resized_image1)

        partner.movie_buttons[index].config(state=DISABLED)

        self.movie_box.protocol('WM_DELETE_WINDOW', partial(self.enable_button, partner, index))

        self.film_frame = Frame(self.movie_box, bg=background)
        self.film_frame.grid(column=0)

        self.canvas = Canvas(self.film_frame, width=400, height=350, bg=background)
        self.canvas.grid(row=0, column=0)

        self.canvas.create_image(1, 1, anchor="nw", image=self.photo1)


        self.canvas.create_image(285, 130, anchor="nw", image=self.photo)

        self.canvas.create_text(10, 220, text="KING KONG", font=("Poppins", "34", "bold"), fill= "#FCA311", anchor="nw")

        self.canvas.create_text(10, 270, text="R13  115min | 6 june 2024", font=("Poppins", "13"), fill= "#FCA311", anchor="nw")

        self.canvas.create_text(10, 290, text="Bloody violence, sexual refrences & offensive language", font=("Poppins", "10"), fill= "#FCA311", anchor="nw")


    def enable_button(self, partner, index):
        partner.enable_all_buttons()
        self.movie_box.destroy()



    


# main routine    
if __name__ == "__main__":
    root = Tk()
    root.title("Cinema")
    Cinema(root)
    root.mainloop()

