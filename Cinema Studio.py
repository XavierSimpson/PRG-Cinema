
from tkinter import*
from PIL import Image, ImageTk
from functools import partial
from tkinter.font import Font
from datetime import datetime, timedelta
import json
import os

file_name = 'data.json'

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build the full path to the data.json file
file_path = os.path.join(script_dir, file_name)

class Movie_info_storage:
    def __init__(self):
        self.data = self.load_data(file_path)

    def load_data(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data.get('movies', [])
    
class ToggleButton(Button):
    def __init__(self, parent, on_colour, off_colour, on_command=None, off_command=None, *args, **kwargs):
        self.is_on = False

        
        self.on_colour = on_colour
        self.off_colour = off_colour

        self.on_command = on_command
        self.off_command = off_command

        super().__init__(parent, bg=self.off_colour, command=self.toggle, *args, **kwargs)

    def toggle(self):
        if self.is_on:

            self.config(bg=self.off_colour)
            if self.off_command:
                self.off_command()
        else:
            

            self.config(bg=self.on_colour)
            if self.on_command:
                self.on_command()
        self.is_on = not self.is_on



class Cinema():

    def __init__(self, root, movie_info):
        self.root = root

        # Load and resize images using Pillow
        desired_size = (200, 293)
        self.photos = []

        for movie in movie_info.data:
            image_path = movie['image_poster']
            image = Image.open(image_path)
            resized_image = image.resize(desired_size, Image.LANCZOS)
            photo = ImageTk.PhotoImage(resized_image)
            self.photos.append(photo)

        # Cinema Frame
        self.cinema_frame = Frame(root, bg="#14213D")
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
        self.side_tab = Frame(root, bg="#19294D", width=10)
        self.side_tab.grid(row=0, column=0, sticky="NS")

        self.canvas = Canvas(self.side_tab, width=200, height=200, bg="#19294D", bd=0, highlightthickness=0)
        self.canvas.grid(row=0, column=0)

        self.canvas.create_text(10, -1, text="RIZZ", font=("Broadway", 45), fill="#FCA311", anchor="nw")
        self.canvas.create_text(11, 50, text="Cinemas", font=("Bahnschrift Light Condensed", 25), fill="#FCA311", anchor="nw")

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
                fg="#FFFFFF", bg="#19294D", anchor="w", command=lambda i=i: self.on_label_button_click(i), bd=0, relief=FLAT
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

            movie_button = Button(
                movie_frame, image=photo, command= lambda i=i: self.displaying_movie(i), bd=0, relief=FLAT,
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
            self.root.destroy()

    def displaying_movie(self, index):
        for button in self.movie_buttons:
            button.config(state=DISABLED)

        Movie(self.root, self, index, movie_info)

    def enable_all_buttons(self):
        for button in self.movie_buttons:
            button.config(state=NORMAL)


class Movie(Toplevel):
    def __init__(self, root, partner, index, movie_info, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.root = root
        self.partner = partner
        self.index = index
        self.movie_info = movie_info
        self.is_minimized = False
        self.is_restoring = False
        self.last_state = self.root.wm_state()
        self.offset_x = 0
        self.offset_y = 0

        self.root.bind("<Unmap>", self.on_unmap)
        self.root.bind("<Map>", self.on_map)
        self.root.bind("<Configure>", self.handle_configure)

        print("Movie title:", self.movie_info.data[index]['title'])

        background = "#14213D"

        self.overrideredirect(True)
        self.transient(self.root)
        self.lift()

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.calculate_original_offset()

        parent_x = self.root.winfo_rootx()
        parent_y = self.root.winfo_rooty()

        # Coordinates of the Toplevel window
        custom_width = 900
        custom_height = 598

        custom_x = parent_x + 199
        custom_y = parent_y + 1

        self.geometry(f"{custom_width}x{custom_height}+{custom_x}+{custom_y}")
        self.configure(bg=background)

        movie_poster_path = self.movie_info.data[index]['image_poster']
        movie_banner_path = self.movie_info.data[index]['image_banner']

        image = Image.open(movie_poster_path)
        image1 = Image.open(movie_banner_path)

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
        self.scrollbar.grid(row=0, column=2, sticky='ns', padx=5)

        self.font = Font(family="Bahnschrift Light Condensed", size=13)


        movie_title = self.movie_info.data[index]['title']
        movie_info = f"{self.movie_info.data[index]['rating']}  {self.movie_info.data[index]['duration']}  |  {self.movie_info.data[index]['release_date']}"
        movie_warnings = self.movie_info.data[index]['warnings']
        movie_summary = self.movie_info.data[index]['summary']


        self.canvas = Canvas(self.film_frame, width=852, height=598, bg=background, bd=0, highlightthickness=0,
                             yscrollcommand=self.scrollbar.set)
        self.canvas.grid(row=0, column=1)

        self.scrollable_frame = Frame(self.canvas, bg=background)
        self.canvas.create_window((1, 550), window=self.scrollable_frame, anchor="nw")

        self.time_frame = Frame(self.canvas, bg="#19294D")
        self.canvas.create_window((2,630), window=self.time_frame, anchor="nw")

        self.scrollbar.config(command=self.canvas.yview)

        self.canvas.create_rectangle(1, 326, 850, 480, fill="#1e2749", outline="#1e2749")
        self.canvas.create_rectangle(1, 900, 850, 600, fill="#19294D", outline="#1e2749")

        self.canvas.create_image(1, 1, anchor="nw", image=self.photo1)
        self.canvas.create_image(26, 330, anchor="nw", image=self.photo)
        
        self.canvas.create_text(1, 530, text="Screening Times: ", font=("Bahnschrift Light Condensed", 20),
                                 fill="#E5E5E5", anchor="w")

        self.canvas.create_text(135, 325, text=movie_title, font=("Britannic Bold", 40), fill="#FCA311", anchor="nw")

        self.canvas.create_text(135, 375, text=movie_info, font=("Bahnschrift Light Condensed", 20), fill="#E5E5E5", anchor="nw")
        
        self.canvas.create_text(135, 400, text=movie_warnings, font=("Bahnschrift Light Condensed", 15), fill="#E5E5E5", anchor="nw")
        
        self.wrap_text(movie_summary, 600)
        
        self.create_date_buttons()

        self.canvas.create_text(150, 1000,
                                text="Blah blah blah blah blah Blah",
                                font=("Bahnschrift Light Condensed", 15), fill="#FCA311", anchor="nw",)

        self.canvas.update_idletasks()  # Ensure all pending events are processed
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        self.bind("<MouseWheel>", self.on_mousewheel)
        

    def handle_configure(self, event):
        self.on_configure(event)
        self.follow_main_window(event)   

    def on_unmap(self, event):
        current_state = self.root.wm_state()
        if self.last_state != 'iconic' and current_state == 'iconic':
            self.is_minimized = True
        self.last_state = current_state

    def on_map(self, event):
        current_state = self.root.wm_state()
        if self.last_state == 'iconic' and current_state != 'iconic':
            self.is_restoring = True
            self.after(300, self.finish_restore)
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
        self.root.attributes("-topmost", False)
        self.after(10, lambda: self.attributes("-topmost", False))

    def enable_button(self, partner, index):
        partner.enable_all_buttons()
        self.destroy()

    def calculate_original_offset(self):
        # Get initial positions
        parent_x = self.root.winfo_rootx()
        parent_y = self.root.winfo_rooty()
        
        toplevel_x = 297
        toplevel_y = 72

        # Calculate the offset
        self.offset_x = toplevel_x - parent_x
        self.offset_y = toplevel_y - parent_y

        print(f"Offset X: {self.offset_x}, Offset Y: {self.offset_y}")


    def follow_main_window(self, event):
        if not self.is_restoring and not self.is_minimized:
            parent_x = self.root.winfo_rootx()
            parent_y = self.root.winfo_rooty()

            # Use original offsets to maintain relative position
            custom_x = parent_x + 199
            custom_y = parent_y + 1

            self.geometry(f"+{custom_x}+{custom_y}")

    def wrap_text(self, text, width):
        lines = []
        words = text.split()
        current_line = words[0]
        
        for word in words[1:]:
            if self.font.measure(current_line + " " + word) < width:
                current_line += " " + word
            else:
                lines.append(current_line)
                current_line = word

        lines.append(current_line)
        
        y_position = 430
        for line in lines:
         self.canvas.create_text(135, y_position, text=line, font=("Bahnschrift Light Condensed", 13), fill="#ADADAD", anchor="nw", width=width)
         y_position += self.font.metrics("linespace")


    def create_date_buttons(self):
        today = datetime.now()

        for i in range(7):
            date = today + timedelta(days=i)
            date_str = date.strftime("%d %b")
            button = Button(
                self.scrollable_frame, text=date_str, font=("Bahnschrift Light Condensed", 15),
                bg="#1e2749", fg="#FFFFFF", anchor='n', bd=0, relief=FLAT, width=12,
                command=lambda d=date: self.show_times(d),
                takefocus=False
            )
            button.grid(row=0, column=i, padx=10, pady=10, sticky="ns")

    def show_times(self, date):

        for widget in self.time_frame.winfo_children():
            widget.destroy()

        times_for_days = {
            0: ["7:00 AM","11:00 AM", "1:00 PM", "3:00 PM", "5:00 PM", "7:00 PM", "9:00 PM", "11:00 PM"],
            1: ["7:00 AM","11:00 AM", "1:00 PM", "3:00 PM", "5:00 PM", "7:00 PM", "9:00 PM", "11:00 PM"],
            2: ["7:00 AM","11:00 AM", "1:00 PM", "3:00 PM", "5:00 PM", "7:00 PM", "9:00 PM", "11:00 PM"],
            3: ["7:00 AM","11:00 AM", "1:00 PM", "3:00 PM", "5:00 PM", "7:00 PM", "9:00 PM", "11:00 PM"],
            4: ["7:00 AM","11:00 AM", "1:00 PM", "3:00 PM", "5:00 PM", "7:00 PM", "9:00 PM", "11:00 PM"],
            5: ["7:00 AM","11:00 AM", "1:00 PM", "3:00 PM", "5:00 PM", "7:00 PM", "9:00 PM", "11:00 PM"],
            6: ["7:00 AM","11:00 AM", "1:00 PM", "3:00 PM", "5:00 PM", "7:00 PM", "9:00 PM", "11:00 PM"],
        }

        current_date = datetime.now().date()
        current_time = datetime.now().time()

        day_diff = (date.date() - current_date).days

        times = times_for_days.get(day_diff, [])
        if day_diff == 0:
            times = [t for t in times if datetime.strptime(t, "%I:%M %p").time() > current_time]

        max_width = 150 # Maximum width before starting a new row
        button_width = 24 # Width of each button

        current_width = 0
        row = 0
        column = 0

        for i, time in enumerate(times):
            time_button = Button(
                self.time_frame, text=time, font=("Bahnschrift Light Condensed", 15),
                bg="#e09f3e", fg="#FFFFFF", anchor='w', bd=0, relief=FLAT,
                command=lambda t=time: self.book_time(date, t), width=24, height=2,
                takefocus=False
            )
            time_button.grid(row=row, column=column, padx=7, pady=10, sticky="w")

            button_width_with_padding = button_width + 17 
            current_width += button_width_with_padding

            if current_width > max_width:
                row += 1
                column = 0
                current_width = 0
            else:
                column += 1


    def book_time(self, date, time):
            print(f"Booking for {date.strftime('%d %b')} at {time}")

            Movie_booking(self.root, self.index, self.movie_info, date, time)

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")

class Movie_booking(Toplevel):
    def __init__(self, partner, index, movie_info, date, time,*args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.seats = []
        self.booked_seats = []
        self.buttons = {}
    
        self.root = root
        self.partner = partner
        self.index = index
        self.movie_info = movie_info 
        self.root.bind("<Configure>", self.handle_configure)   

        background = "#14213D"

        self.overrideredirect(True)
        self.transient(self.root)
        self.lift()

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        custom_width = 900
        custom_height = 598

        root_x = self.root.winfo_rootx()
        root_y = self.root.winfo_rooty()

        # Debugging prints to trace coordinate values
        print(f"Root window coordinates: ({root_x}, {root_y})")


        custom_x = root_x  + 199
        custom_y = root_y  + 1

        self.geometry(f"{custom_width}x{custom_height}+{custom_x}+{custom_y}")
        self.configure(bg=background)

        self.film_frame = Frame(self, bg=background)
        self.film_frame.grid(column=0, sticky="nsew")

        self.scrollbar = Scrollbar(self.film_frame, orient=VERTICAL)
        self.scrollbar.grid(row=0, column=2, sticky='nsew', padx=5,)

        self.exit_button = Button(self.film_frame, text="x", command=self.destroy, font=("Biome Light", 17), bg = "#14213D", fg="#FFFFFF", anchor="n", bd=0, relief=FLAT)
        self.exit_button.grid(row=0, column=0, sticky="n")

        self.canvas = Canvas(self.film_frame, bg=background, highlightthickness=0, width=852, height=598, yscrollcommand=self.scrollbar.set)
        self.canvas.grid(row=0, column=1, sticky="nsew")

        self.scrollbar.config(command=self.canvas.yview)

        num_seats_per_row = 18
        button_width = 20
        button_height= 35
        button_spacing = 5

        total_button_width = num_seats_per_row * button_width + (num_seats_per_row - 1) * button_spacing
        start_x = (900 - total_button_width) // 2

        self.canvas.create_rectangle(172, 150, 727, 450, fill="#1e2749", outline="#1e2749")
        self.canvas.create_rectangle(172, 550, 727, 932, fill="#1e2749", outline="#1e2749")

        for row in range(3):
            for col in range(num_seats_per_row):
                x_position = start_x + col * (button_width + button_spacing)
                y_position = 300 + row * (button_height + button_spacing)
                self.button1 = ToggleButton(self.canvas, on_colour="#495057", off_colour="#e09f3e", on_command = lambda s=col: self.clicked_seat(s), off_command= lambda s=col: self.unlcicked_seat(s), anchor='n', bd=0, relief=FLAT)
                self.canvas.create_window(x_position, y_position, anchor="nw", window=self.button1, width=button_width, height=20)

        for row in range(2):
            for col in range(num_seats_per_row):
                x_position = start_x + col * (button_width + button_spacing)
                y_position = 190 + row * (button_height + button_spacing)
                self.button1 = ToggleButton(self.canvas, on_colour="#495057", off_colour="#e09f3e", on_command = lambda s=col: self.clicked_seat(s), off_command= lambda s=col: self.unlcicked_seat(s), anchor='n', bd=0, relief=FLAT)
                self.canvas.create_window(x_position, y_position, anchor="nw", window=self.button1, width=button_width, height=20)

        self.canvas.create_text(177, 187, text="A", font=("Bahnschrift Light Condensed", 15), fill="#E5E5E5", anchor="nw", width=100)
        self.canvas.create_text(177, 227, text="B", font=("Bahnschrift Light Condensed", 15), fill="#E5E5E5", anchor="nw", width=100)

        self.canvas.create_text(177, 297, text="C", font=("Bahnschrift Light Condensed", 15), fill="#E5E5E5", anchor="nw", width=100)
        self.canvas.create_text(177, 337, text="D", font=("Bahnschrift Light Condensed", 15), fill="#E5E5E5", anchor="nw", width=100)
        self.canvas.create_text(177, 377, text="E", font=("Bahnschrift Light Condensed", 15), fill="#E5E5E5", anchor="nw", width=100)

        self.canvas.create_text(177, 50, text="Choose your seats: ", font=("Bahnschrift Light Condensed", 25), fill="#E5E5E5", anchor="nw")

        start = start_x - 30
        self.canvas.create_polygon(172, 100, 727, 100, 697, 130, 202, 130, fill="#19294D", outline="#1e2749")  

        self.create_ticket_buttons()

        for button in self.buttons.values():
              button.config(state=DISABLED)

        

        self.canvas.create_text(425, 100, text="screen", font=("Bahnschrift Light Condensed", 15), fill="#E5E5E5", anchor="nw", width=100)

        self.confirm_text_id = self.canvas.create_text(370, 950, font=("Bahnschrift Light Condensed", 20), fill="#FFFFFF", anchor="nw")

        self.button2 = Button(self.canvas, text="Confirm", command=self.confirm_booking, font=("Bahnschrift Light Condensed", 15), bg="#e09f3e", fg="#FFFFFF", bd=0, relief=FLAT, state=DISABLED)
        self.canvas.create_window(300, 1000, anchor="nw", window=self.button2, width=300, height=50)


        self.canvas.create_text(425, 2000, text="screen", font=("Bahnschrift Light Condensed", 15), fill="#E5E5E5", anchor="nw", width=100)


        self.canvas.update_idletasks()  # Ensure all pending events are processed
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        
    def confirm_booking(self):
        if (len(self.booked_seats)) > 0:
            self.canvas.itemconfig(self.confirm_text_id, text="Booking Confirmed")
            print("Confirm booking")
            self.after(1000, self.destroy)
        else:
            self.button2.config(state=DISABLED)



    def create_ticket_buttons(self):
        background = "#14213D"

        start_2 = 587
        button_start = 600
        tickets = {
                "Adult Ticket":25.00, 
                "Child Ticket":19.00, 
                "Student Ticket":21.00, 
                "Senior Ticket":18.50
                    }
        
        #self.canvas.create_text(177, 500, text="Ticket Type:", font=("Bahnschrift Light Condensed", 25), fill="#E5E5E5", anchor="nw")
        self.ticket_choice = self.canvas.create_text(177, 500, text="Ticket Type:", font=("Bahnschrift Light Condensed", 25), fill="#E5E5E5", anchor="nw")

        for i in range(len(tickets)):
            lines = start_2 + 58
            lines_2 = lines + 2
            key_list = list(tickets.keys())

            self.canvas.create_text(200, start_2, text=key_list[i], font=("Bahnschrift Light Condensed", 15), fill="#E5E5E5", anchor="nw", width=100)
            self.canvas.create_rectangle(172, lines, 727, lines_2, fill=background, outline=background)
            
            self.canvas.create_text(530 , start_2, text=f"${tickets[key_list[i]]:.2f}", font=("Bahnschrift Light Condensed", 15), fill="#E5E5E5", anchor="nw", width=100)

            button = Button(self.canvas, text="Add", font=("Bahnschrift Light Condensed", 15), bg = "#e09f3e", fg="#FFFFFF", bd=0, relief=FLAT, 
                                command=lambda p=key_list[i]: self.book_ticket(p))
            self.canvas.create_window(640, button_start, window=button, width=100, height=40)

            self.buttons[key_list[i]] = button

            start_2 += 95
            button_start += 95


    def book_ticket(self, price):

        print(self.seats)
        print(self.booked_seats)
        print("done")

        if len(self.seats) == len(self.booked_seats):
            for button in self.buttons.values():
              button.config(state=DISABLED)

        else:
            self.booked_seats.append(price)
            print(self.booked_seats)
            print("done1")

            if len(self.seats) == len(self.booked_seats):
                for button in self.buttons.values():
                    button.config(state=DISABLED)
            
                self.button2.config(state=NORMAL)
            self.update_ticket_choice()

    def update_ticket_choice(self):
        #string for booked tickets 
        tickets_booked_string = ""

        for ticket in self.booked_seats:
            tickets_booked_string += f" {ticket},"
        self.canvas.itemconfig(self.ticket_choice, text=f"Ticket type: {tickets_booked_string.strip()}")
            
            
    def clicked_seat(self, seat):
        print(f"Clicked seat {seat}")
        self.seats.append(seat)
        print(self.seats)
        for button in self.buttons.values():
            button.config(state=NORMAL)
    
    def unlcicked_seat(self, seat):
        print(f"Unclicked seat {seat}")
        self.seats.remove(seat)
        print(self.seats)
        x = len(self.seats)
        if len(self.booked_seats) > x >= 0:
            for button in self.buttons.values():
              button.config(state=DISABLED)
            self.booked_seats.pop()
            self.update_ticket_choice()

            print(self.booked_seats)
        elif x > 0:
            for button in self.buttons.values():
              button.config(state=NORMAL)
              self.button2.config(state=DISABLED)
        else:
            for button in self.buttons.values():
              button.config(state=DISABLED)
            self.button2.config(state=DISABLED)
    

    def handle_configure(self, event):
        self.bring_movie_box_front(event)

    def bring_movie_box_front(self, event=None):
        self.lift()
        self.attributes("-topmost", True)
        self.root.attributes("-topmost", False)
        self.after(10, lambda: self.attributes("-topmost", False)) 

        

            




        

    



# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("RIZZ Cinemas")

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

    root.update_idletasks()  
    
    root.rowconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)

    movie_info = Movie_info_storage()

    Cinema(root, movie_info)
    root.mainloop()