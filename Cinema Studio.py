from tkinter import*
from PIL import Image, ImageTk
from functools import partial

class Cinema():
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
        desired_size = (200, 293)
        self.photos = []

        for path in image_paths:
            image = Image.open(path)
            resized_image = image.resize(desired_size, Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(resized_image)
            self.photos.append(photo)

        # Cinema Frame
        self.cinema_frame = Frame(parent, bg="#14213D")
        self.cinema_frame.grid(column=1, sticky="nsew")

        self.cinema_showing = Label(
            self.cinema_frame, text="Now showing:", font=("Bahnschrift Light Condensed", 20),
            fg="#FFFFFF", bg="#14213D", anchor="w"
        )
        self.cinema_showing.grid(row=1, columnspan=4, sticky="WE", padx=5, pady=5)

        # Frame for Movies all together
        self.movie_frame = Frame(self.cinema_frame, bg="#14213D")
        self.movie_frame.grid(row=2, sticky="nsew")

        # Frame for Side Tab
        self.side_tab = Frame(parent, bg="#19294D", width=10)
        self.side_tab.grid(row=0, column=0, sticky="NS")

        self.canvas = Canvas(self.side_tab, width=200, height=200, bg="#19294D", bd=0, highlightthickness=0)
        self.canvas.grid(row=0, column=0)

        self.canvas.create_text(10, -1, text="RIZZ", font=("Britannic Bold", 45), fill="#FCA311", anchor="nw")
        self.canvas.create_text(11, 50, text="Cinemas", font=("Bahnschrift Light Condensed", 17), fill="#FCA311", anchor="nw")

        self.setup_movie_frames()
        self.setup_side_buttons()

    def setup_side_buttons(self):

        side_tab_labels = ["Movies", "Session Times", "Cinemas", "Food & Snacks", "Exit"]
        self.side_buttons = []
        for i, text in enumerate(side_tab_labels):
            
            def create_label_button_callback(index):
                def callback():
                    self.on_label_button_click(index)
                return callback

            button = Button(
                self.side_tab, text=text, font=("Bahnschrift Light Condensed", 17),
                fg="#FFFFFF", bg="#19294D", anchor="w", command=create_label_button_callback(i), bd=0, relief=FLAT
            )
            button.grid(row=i+1, padx=15, pady=7, sticky="WE")

        self.side_buttons.append(button)

    def setup_movie_frames(self):
        # Frames and buttons for movies
        movie_titles = ["King Kong", "The Day the Earth stood still", "All quiet on the Western Front", "Dracula's Daughter"]
        self.movie_buttons = []
        for i, (photo, title) in enumerate(zip(self.photos, movie_titles)):
            movie_frame = Frame(self.movie_frame, bg="#14213D")
            movie_frame.grid(row=0, column=i+1, pady=5)

            def create_movie_button_callback(index):
                def callback():
                    self.displaying_movie(index)
                return callback

            movie_button = Button(
                movie_frame, image=photo, command=create_movie_button_callback(i), bd=0, relief=FLAT
            )
            movie_button.image = photo
            movie_button.grid(row=0, column=0, padx=10, pady=5)

            movie_label = Label(
                movie_frame, text=title, font=("Bahnschrift Light Condensed", 15),
                fg="#FFFFFF", bg="#14213D", justify="left"
            )
            movie_label.grid(row=1)

            self.movie_buttons.append(movie_button)

    def on_label_button_click(self, index):
        if index == 0:
            print("1")
        elif index == 1:
            print("2")
        elif index == 2:
            print("3")
        elif index == 3:
            print("4")
        elif index == 4:
            self.parent.destroy()

    def displaying_movie(self, index):
        for button in self.movie_buttons:
            button.config(state=DISABLED)

        Movie(self.parent, self, index)

    def enable_all_buttons(self):
        for button in self.movie_buttons:
            button.config(state=NORMAL)


class Movie(Toplevel):
    def __init__(self, parent, partner, index, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.parent = parent
        self.partner = partner
        self.index = index
        self.is_minimized = False
        self.is_restoring = False
        self.last_state = self.parent.wm_state()
        self.offset_x = 0
        self.offset_y = 0

        self.parent.bind("<Unmap>", self.on_unmap)
        self.parent.bind("<Map>", self.on_map)
        self.parent.bind("<Configure>", self.handle_configure)
  


        background = "#14213D"

        self.overrideredirect(True)
        self.transient(self.parent)
        self.lift()

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.calculate_original_offset()

        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()

        # Coordinates of the Toplevel window
        custom_width = 900
        custom_height = 598

        custom_x = parent_x + self.offset_x
        custom_y = parent_y + self.offset_y

        self.geometry(f"{custom_width}x{custom_height}+{custom_x}+{custom_y}")
        self.configure(bg=background)

        image_paths = {
            0: [r"C:\Users\xavie\Downloads\image-from-rawpixel-id-9975454-original.jpg",
                r"C:\Users\xavie\OneDrive\Documents\PRG ASSESMENT\King kong banner.jpg"],
            1: [r"C:\Users\xavie\Downloads\image-from-rawpixel-id-9976112-original.jpeg",
                r"C:\Users\xavie\Downloads\The.Day.The.Earth.Stood.Still.(1951)-poster.(16x9).jpg"],
            2: [r"C:\Users\xavie\Downloads\image-from-rawpixel-id-9976560-original.jpg",
                r"C:\Users\xavie\Downloads\All-Quiet-on-the-Wester-Front-Featured.webp"],
            3: [r"C:\Users\xavie\Downloads\image-from-rawpixel-id-9976063-original.jpg",
                r"C:\Users\xavie\Downloads\draculas-daughter-featured.webp"]
        }

        images = image_paths[index]
        image = Image.open(images[0])
        image1 = Image.open(images[1])

        desired_width = 100
        desired_height = 143

        resized_image1 = image1.resize((850, 320), Image.Resampling.LANCZOS)
        resized_image = image.resize((desired_width, desired_height), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(resized_image)
        self.photo1 = ImageTk.PhotoImage(resized_image1)

        partner.movie_buttons[index].config(state=DISABLED)
        self.protocol('WM_DELETE_WINDOW', partial(self.enable_button, partner, index))

        self.film_frame = Frame(self, bg=background)
        self.film_frame.grid(column=0, sticky="nsew")

        self.exit_button = Button(self.film_frame, text="x", font=("Biome Light", 17), bg=background,
                                  fg="#FFFFFF", anchor='n', bd=0, relief=FLAT,
                                  command=partial(self.enable_button, partner, index))
        self.exit_button.grid(row=0, column=0, sticky="n")

        self.scrollbar = Scrollbar(self.film_frame, orient=VERTICAL)
        self.scrollbar.grid(row=0, column=2)

        movie_titles = ["King Kong", "The Day the Earth stood still", "All quiet on the Western Front",
                        "Dracula's Daughter"]
        movie_name = movie_titles[index]

        self.canvas = Canvas(self.film_frame, width=852, height=500, bg=background, bd=0, highlightthickness=0)
        self.canvas.grid(row=0, column=1)

        self.canvas.create_image(1, 1, anchor="nw", image=self.photo1)
        self.canvas.create_image(26, 330, anchor="nw", image=self.photo)

        self.canvas.create_text(135, 325, text=movie_name, font=("Britannic Bold", 40), fill="#FCA311", anchor="nw")
        self.canvas.create_text(135, 375, text="R13  115min | 6 june 2024", font=("Bahnschrift Light Condensed", 20),
                                fill="#FCA311", anchor="nw")
        self.canvas.create_text(135, 400,
                                text="Bloody violence, sexual references & offensive language",
                                font=("Bahnschrift Light Condensed", 15), fill="#FCA311", anchor="nw")
        

    def handle_configure(self, event):
        self.on_configure(event)
        self.follow_main_window(event)   

    def on_unmap(self, event):
        current_state = self.parent.wm_state()
        if self.last_state != 'iconic' and current_state == 'iconic':
            self.is_minimized = True
        self.last_state = current_state

    def on_map(self, event):
        current_state = self.parent.wm_state()
        if self.last_state == 'iconic' and current_state != 'iconic':
            self.is_restoring = True
            self.after(500, self.finish_restore)
        self.last_state = current_state

    def on_configure(self, event):
        if not self.is_restoring:
            self.bring_movie_box_front()

    def finish_restore(self):
        self.is_minimized = False
        self.is_restoring = False
        self.bring_movie_box_front()
            
    def bring_movie_box_front(self, event=None):
        self.lift()
        self.attributes("-topmost", True)
        self.parent.attributes("-topmost", False)
        self.after(10, lambda: self.attributes("-topmost", False))

    def enable_button(self, partner, index):
        partner.enable_all_buttons()
        self.destroy()

    def calculate_original_offset(self):
        # Get initial positions
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        
        toplevel_x = 297
        toplevel_y = 72

        # Calculate the offset
        self.offset_x = toplevel_x - parent_x
        self.offset_y = toplevel_y - parent_y

        print(f"Offset X: {self.offset_x}, Offset Y: {self.offset_y}")


    def follow_main_window(self, event):
        if not self.is_restoring and not self.is_minimized:
            parent_x = self.parent.winfo_rootx()
            parent_y = self.parent.winfo_rooty()

            # Use original offsets to maintain relative position
            custom_x = parent_x + self.offset_x
            custom_y = parent_y + self.offset_y

            self.geometry(f"+{custom_x}+{custom_y}")

    #def on_window_map(self, event):
        #if not hasattr(self, 'has_shown'):
           # self.has_shown = True
           # self.after(500, lambda: self.deiconify())

# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Cinema")

    desired_width = 1100
    desired_height = 600

    # Calculate the center of the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - desired_width) // 2
    y = (screen_height - desired_height) // 2

    # Adjust y position to account for the taskbar height
    taskbar_height = 40  # Typical height of the taskbar
    y = y - (taskbar_height // 2)

    # Set the geometry to the desired size and centered position
    root.geometry(f"{desired_width}x{desired_height}+{x}+{y}")

    root.update_idletasks()  # Ensure the geometry has been applied before centering

    root.rowconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)

    Cinema(root)
    root.mainloop()