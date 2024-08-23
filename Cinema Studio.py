from tkinter import*
from PIL import Image, ImageTk
from functools import partial
from tkinter.font import Font
from datetime import datetime, timedelta
import json
import os


#The json file that holds all the info
file_name = 'data.json'

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# find the full path to the data.json file
file_path = os.path.join(script_dir, file_name)

#This is where I load the data from the json file
class Movie_info_storage:
    def __init__(self):
        self.data = self.load_data(file_path)
    
    def load_data(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data.get('movies', [])

    #This allows for seats to be saved permanently, this does it by opening the json file and adding to it
    def save_booked_seats(self, file_path, movie_index, date, time, new_seats):
        try:
            #Open the json file
            with open(file_path, 'r') as file:
                data = json.load(file)
        #If there is any error for it.
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"movies": []}

        # Find the movie info for a specified movie_index
        movie = data["movies"][movie_index]
        booked_seats_entry = next((entry for entry in movie["booked_seats"] if entry["date"] == date and entry["time"] == time), None)
        if booked_seats_entry:
            # Merge new seats with existing seats
            existing_seats = set(booked_seats_entry["seats"])
            new_seats_set = set(new_seats)
            booked_seats_entry["seats"] = list(existing_seats.union(new_seats_set))
            # Otherwise save a new info for the json file
        else:
            movie["booked_seats"].append({"date": date, "time": time, "seats": new_seats})

        #Close the file and save it
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=1)

#This makes the toggle button for chosing the seats in the booking window     
class ToggleButton(Button):
    def __init__(self, root, on_colour, off_colour, on_command=None, off_command=None, *args, **kwargs):
        #Make sure that the button is off by default
        self.is_on = False

        #This is the colour of the button when it is on and off if no value is given
        self.on_colour = on_colour
        self.off_colour = off_colour

        #This is the command that is run when the button is clicked, defualt value is 'none'
        self.on_command = on_command
        self.off_command = off_command

        #Make it so the toggle button has the assessets of the button from tkinter
        super().__init__(root, bg=self.off_colour, command=self.toggle, *args, **kwargs)

    #This function calls activates different things when the button is clicked, toggeling off and on
    def toggle(self):
        #checks if the button is on, if true, when it gets clicked, it will toggle it off
        if self.is_on:
            
            #Setting button to off colour
            self.config(bg=self.off_colour)
            #Checks if there is a command, if there is, calls that command
            if self.off_command:
                self.off_command()
        
        #If button is not on, and gets clicked, toggle on
        else:
            
            #Setting button to on colour
            self.config(bg=self.on_colour)
            #Checks if there is a command, if there is, calls that command
            if self.on_command:
                self.on_command()

        #Toggles the state of the code.   
        self.is_on = not self.is_on

    #This disables the button and sets the colour to on_colour
    def set_off_and_disable(self):
        self.is_on = True
        self.config(bg=self.on_colour, state=DISABLED)

    def set_off(self):
        self.is_on = False
        self.configure(bg=self.off_colour)

#My main window class
class Cinema():
    @staticmethod
    def on_button_click():
        print("hello!")

    #Set up, passing root and the json file through 
    def __init__(self, root, movie_info):
        self.root = root

        # Load and resize images using Pillow
        desired_size = (200, 293)
        self.photos = []

        #This gets the image paths from the json file, then finds the image and makes it usable by tkinter
        for movie in movie_info.data:
            image_path = movie['image_poster']
            image = Image.open(image_path)
            resized_image = image.resize(desired_size, Image.LANCZOS)
            photo = ImageTk.PhotoImage(resized_image)
            #Add the photos to a list to be used later 
            self.photos.append(photo)

        #Setting up the frame that holds the movie poster
        self.cinema_frame = Frame(root, bg="#14213D")
        self.cinema_frame.grid(column=1, sticky="nsew")

        #Setting up GUI for window, labels, buttons, etc...

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

        #Canvas for name of Cinema 
        self.canvas = Canvas(self.side_tab, width=200, height=200, bg="#19294D", bd=0, highlightthickness=0)
        self.canvas.grid(row=0, column=0)

        #Cinema name
        self.canvas.create_text(10, -1, text="RIZZ", font=("Broadway", 45), fill="#FCA311", anchor="nw")
        self.canvas.create_text(11, 50, text="Cinemas", font=("Bahnschrift Light Condensed", 25), fill="#FCA311", anchor="nw")

        #call the functions that set up the buttons for the main window
        self.setup_movie_frames()
        self.setup_side_buttons()

    #This function sets up the side buttons for the main window
    def setup_side_buttons(self):
        side_tab_labels = ["Movies", "Session Times", "Cinemas", "Food & Snacks", "Exit"]
        self.side_buttons = []
        for i, text in enumerate(side_tab_labels):

            button = Button(
                self.side_tab, text=text, font=("Bahnschrift Light Condensed", 17),
                fg="#FFFFFF", bg="#19294D", anchor="w", command=lambda i=i: self.on_label_button_click(i), bd=0, relief=FLAT
            )
            button.grid(row=i+1, padx=15, pady=7, sticky="WE")
        #Adds buttons to list in order to use them later
        self.side_buttons.append(button)

    #This functions sets up the movie poster buttons 
    def setup_movie_frames(self):
        # Frames and buttons for movies
        movie_titles = ["King Kong", "The Day the Earth stood still", "All quiet on the Western Front", "Dracula's Daughter"]
        self.movie_buttons = []
        #Connects photo and title together for efficiancy 
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

            #Adds buttons to list in order to use them later
            self.movie_buttons.append(movie_button)

    #Different outputs for the side tab buttons
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

    #Command to open up the movie window for each movie using the specific index
    def displaying_movie(self, index):
        for button in self.movie_buttons:
            #Disbles each movie button when movie poster is clicked
            button.config(state=DISABLED)
        
        #Making sure it is connected to root and the json file is passed through
        Movie_info(self.root, self, index, movie_info)

    #Enable all buttons when called
    def enable_all_buttons(self):
        for button in self.movie_buttons:
            button.config(state=NORMAL)

#This is the movie_info window
class Movie_info(Toplevel):
    def __init__(self, root, partner, index, movie_info, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        #Set up the instance variables 
        self.root = root
        self.partner = partner
        self.index = index
        self.movie_info = movie_info
        self.is_minimized = False
        self.is_restoring = False
        self.last_state = self.root.wm_state()
        self.currently_toggled_button = None
        self.buttons = {}

        #Set up the bindings

        #This is when the window is minimized 
        self.root.bind("<Unmap>", self.on_unmap)

        #This is when the window is restored 
        self.root.bind("<Map>", self.on_map)

        #This is when the window is changed in someway shape or form
        self.root.bind("<Configure>", self.handle_configure)


        #Varible of the general background colour 
        background = "#14213D"

        #Window properties 
        self.overrideredirect(True)
        self.transient(self.root)
        self.lift()
    
        #Coordinates of the main window
        parent_x = self.root.winfo_rootx()
        parent_y = self.root.winfo_rooty()

        #Height and width for the movie_info window
        custom_width = 900
        custom_height = 598

        #Coordinates for the movie_info window
        custom_x = parent_x + 199
        custom_y = parent_y + 1
        self.geometry(f"{custom_width}x{custom_height}+{custom_x}+{custom_y}")
        self.configure(bg=background)


        #Setting up the images for the movie_info window, by rezising them.
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

        #Setting up main frame for this window
        self.film_frame = Frame(self, bg=background)
        self.film_frame.grid(column=0, sticky="nsew")

        #Setting up exit button
        self.exit_button = Button(self.film_frame, text="x", font=("Biome Light", 17), bg=background,
                                  fg="#FFFFFF", anchor='n', bd=0, relief=FLAT,
                                  command=partial(self.enable_button, partner))
        self.exit_button.grid(row=0, column=0, sticky="n")

        #Setting up scrollbar 
        self.scrollbar = Scrollbar(self.film_frame, orient=VERTICAL)
        self.scrollbar.grid(row=0, column=2, sticky='ns', padx=5)

        #Setting the main font of text
        self.font = Font(family="Bahnschrift Light Condensed", size=13)

        #Setting up the movie_info from the json file
        movie_title = self.movie_info.data[index]['title']
        movie_info = f"{self.movie_info.data[index]['rating']}  {self.movie_info.data[index]['duration']}  |  {self.movie_info.data[index]['release_date']}"
        movie_warnings = self.movie_info.data[index]['warnings']
        movie_summary = self.movie_info.data[index]['summary']

        #Setting up the canvas for the aesthetics 
        self.canvas = Canvas(self.film_frame, width=852, height=598, bg=background, bd=0, highlightthickness=0,
                             yscrollcommand=self.scrollbar.set)
        self.canvas.grid(row=0, column=1)
        self.scrollable_frame = Frame(self.canvas, bg=background)
        self.canvas.create_window((1, 550), window=self.scrollable_frame, anchor="nw")

        #Frame for the time slots to choose from
        self.time_frame = Frame(self.canvas, bg="#19294D")
        self.canvas.create_window((2,630), window=self.time_frame, anchor="nw")

        self.scrollbar.config(command=self.canvas.yview)

        #Creating the window GUI
        self.canvas.create_rectangle(1, 326, 850, 480, fill="#1e2749", outline="#1e2749")
        self.canvas.create_rectangle(1, 900, 850, 600, fill="#19294D", outline="#1e2749")

        self.canvas.create_image(1, 1, anchor="nw", image=self.photo1)
        self.canvas.create_image(26, 330, anchor="nw", image=self.photo)
        
        #Movie info
        self.canvas.create_text(1, 530, text="Screening Times: ", font=("Bahnschrift Light Condensed", 20),
                                 fill="#E5E5E5", anchor="w")
        self.canvas.create_text(135, 325, text=movie_title, font=("Britannic Bold", 40), fill="#FCA311", anchor="nw")
        self.canvas.create_text(135, 375, text=movie_info, font=("Bahnschrift Light Condensed", 20), fill="#E5E5E5", anchor="nw")
        self.canvas.create_text(135, 400, text=movie_warnings, font=("Bahnschrift Light Condensed", 15), fill="#E5E5E5", anchor="nw")

        #create the booking time buttons
        self.create_date_buttons()


        self.canvas.create_text(150, 1000,
                                text="Blah blah blah blah blah Blah",
                                font=("Bahnschrift Light Condensed", 15), fill="#FCA311", anchor="nw",)

        # Ensure all pending events are processed
        self.canvas.update_idletasks() 
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        #Make it so you can scroll using mouse wheel
        self.bind("<MouseWheel>", self.on_mousewheel)
        

    def handle_configure(self, event):
        self.on_configure(event)
        self.follow_main_window(event)   

    #When the window gets minmized it checks what state it is and stores it
    def on_unmap(self, event):
        current_state = self.root.wm_state()
        if self.last_state != 'iconic' and current_state == 'iconic':
            self.is_minimized = True
        self.last_state = current_state

    #When the window gets restored it checks what state it is and stores it
    def on_map(self, event):
        current_state = self.root.wm_state()
        if self.last_state == 'iconic' and current_state != 'iconic':
            self.is_restoring = True
            self.after(300, self.finish_restore)
        self.last_state = current_state

    #Checks if window is resoring, if not calls function
    def on_configure(self, event):
        if not self.is_restoring:
            self.bring_movie_box_front()

    #Checks if window is finished restoring, calls bring movie to front
    def finish_restore(self):
        self.is_minimized = False
        self.is_restoring = False
        self.bring_movie_box_front()
        
    #This brings the movie_info window to the front of the program
    def bring_movie_box_front(self, event=None):
        self.lift()
        self.attributes("-topmost", True)
        self.root.attributes("-topmost", False)
        self.after(10, lambda: self.attributes("-topmost", False))

    #Enables all buttons before dstroying window
    def enable_button(self, partner):
        partner.enable_all_buttons()
        self.destroy()

    #Makes the movie_info window follow the coordinates of the main window
    def follow_main_window(self, event):
        if not self.is_restoring and not self.is_minimized:
            parent_x = self.root.winfo_rootx()
            parent_y = self.root.winfo_rooty()

            # Use original offsets to maintain position
            custom_x = parent_x + 199
            custom_y = parent_y + 1

            self.geometry(f"+{custom_x}+{custom_y}")

    #This function creates the buttons that show what days seats are avilable to book
    def create_date_buttons(self):
        today = datetime.now()

        for i in range(7):
            date = today + timedelta(days=i)
            date_str = date.strftime("%d %b")
            button = ToggleButton(
                self.scrollable_frame, on_colour="#e09f3e", off_colour="#1e2749", text=date_str, font=("Bahnschrift Light Condensed", 15),
                fg="#FFFFFF", anchor='n', bd=0, relief=FLAT, width=12,
                on_command=lambda d=date, i=i: self.toggle_date_button(d, i), off_command=self.destroy_widget,
                takefocus=False)
            button.grid(row=0, column=i, padx=10, pady=10, sticky="ns")
            self.buttons[i]= button


    def toggle_date_button(self, date, index):
        button = self.buttons[index]
        if self.currently_toggled_button and self.currently_toggled_button != button:
            self.currently_toggled_button.set_off()
        self.currently_toggled_button = button
        self.show_times(date)

    def destroy_widget(self):
        for widget in self.time_frame.winfo_children():
            widget.destroy()


    def show_times(self, date):

        #To clear buttons in the time_frame so to put new ones in
        for widget in self.time_frame.winfo_children():
            widget.destroy()

        #The times that screenings are held
        times_for_days = {
            0: ["7:00 AM","11:00 AM", "1:00 PM", "3:00 PM", "5:00 PM", "7:00 PM", "9:00 PM", "11:00 PM"],
            1: ["7:00 AM","11:00 AM", "1:00 PM", "3:00 PM", "5:00 PM", "7:00 PM", "9:00 PM", "11:00 PM"],
            2: ["7:00 AM","11:00 AM", "1:00 PM", "3:00 PM", "5:00 PM", "7:00 PM", "9:00 PM", "11:00 PM"],
            3: ["7:00 AM","11:00 AM", "1:00 PM", "3:00 PM", "5:00 PM", "7:00 PM", "9:00 PM", "11:00 PM"],
            4: ["7:00 AM","11:00 AM", "1:00 PM", "3:00 PM", "5:00 PM", "7:00 PM", "9:00 PM", "11:00 PM"],
            5: ["7:00 AM","11:00 AM", "1:00 PM", "3:00 PM", "5:00 PM", "7:00 PM", "9:00 PM", "11:00 PM"],
            6: ["7:00 AM","11:00 AM", "1:00 PM", "3:00 PM", "5:00 PM", "7:00 PM", "9:00 PM", "11:00 PM"],
        }

        #Finds the current date 
        current_date = datetime.now().date()
        current_time = datetime.now().time()

        #Finds the key for the times_for_days list for the selected date
        day_diff = (date.date() - current_date).days

        #Uses that key to get the screenings available to watch film 
        times = times_for_days.get(day_diff)
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

            #Sets the current width so far
            button_width_with_padding = button_width + 17 # Adjust padding as needed
            current_width += button_width_with_padding

            #Checks if current width is larger than max width, if so, starts line of buttons on new row
            if current_width > max_width:
                row += 1
                column = 0
                current_width = 0
            #Else continues to add buttons to new column 
            else:
                column += 1

    #Calls for movie booking window when clicking on screening times
    def book_time(self, date, time):
            Movie_booking(self.root, self.index, self.movie_info, date, time)

    #Makes sure you can view the scrollable canvus using mouse wheel
    def on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")



class Movie_booking(Toplevel):
    def __init__(self, partner, index, movie_info, date, time,*args, **kwargs):
        super().__init__(root, *args, **kwargs)

        # Lists / Dictionaries 
        self.seats = []
        self.booked_seats = []
        self.buttons = {}
        self.booked_tickets = []
        self.seat_buttons = {}

        #Instance varibles 
        self.root = root
        self.partner = partner
        self.index = index
        self.movie_info = movie_info 
        self.time = time
        self.date = date

        #Bindings 
        self.root.bind("<Configure>", self.handle_configure)   

        #Gets the selected date 
        date_str = self.date.strftime("%Y-%m-%d")

        #Finds the info from the json file of the seats that have been booked already 
        booked_seats_entry = next((entry for entry in self.movie_info.data[self.index]["booked_seats"] if entry["date"] == date_str and entry["time"] == self.time), {"seats": []})
        self.booked_tickets = booked_seats_entry["seats"]

        #Sets the background colour for general use 
        background = "#14213D"

        #Set the window properties 
        self.overrideredirect(True)
        self.transient(self.root)
        self.lift()

        #Setting the coordinates and the width and heights of the window
        custom_width = 900
        custom_height = 598
        root_x = self.root.winfo_rootx()
        root_y = self.root.winfo_rooty()
        custom_x = root_x  + 199
        custom_y = root_y  + 1
        self.geometry(f"{custom_width}x{custom_height}+{custom_x}+{custom_y}")
        self.configure(bg=background)

        #Setting up the main frame for the window
        self.film_frame = Frame(self, bg=background)
        self.film_frame.grid(column=0, sticky="nsew")

        #Scrollbar
        self.scrollbar = Scrollbar(self.film_frame, orient=VERTICAL)
        self.scrollbar.grid(row=0, column=2, sticky='nsew', padx=5,)

        #Exit button
        self.exit_button = Button(self.film_frame, text="x", command=self.destroy, font=("Biome Light", 17), bg = "#14213D", fg="#FFFFFF", anchor="n", bd=0, relief=FLAT)
        self.exit_button.grid(row=0, column=0, sticky="n")

        #Canvas 
        self.canvas = Canvas(self.film_frame, bg=background, highlightthickness=0, width=852, height=598, yscrollcommand=self.scrollbar.set)
        self.canvas.grid(row=0, column=1, sticky="nsew")
        self.scrollbar.config(command=self.canvas.yview)

        #Screen visual
        self.canvas.create_polygon(172, 100, 727, 100, 697, 130, 202, 130, fill="#19294D", outline="#1e2749") 
        self.canvas.create_text(425, 100, text="screen", font=("Bahnschrift Light Condensed", 15), fill="#E5E5E5", anchor="nw", width=100)

        #GUI functions to set up seat GUI and ticket booking GUI
        self.make_seats()
        self.create_ticket_buttons()

        for button in self.buttons.values():
              button.config(state=DISABLED)

        #This text changes when they confirm their booking
        self.confirm_text_id = self.canvas.create_text(370, 950, font=("Bahnschrift Light Condensed", 20), fill="#FFFFFF", anchor="nw")

        #Confirm booking button
        self.button2 = Button(self.canvas, text="Confirm", command=self.confirm_booking, font=("Bahnschrift Light Condensed", 15), bg="#e09f3e", fg="#FFFFFF", bd=0, relief=FLAT, state=DISABLED)
        self.canvas.create_window(300, 1000, anchor="nw", window=self.button2, width=300, height=50)

        self.canvas.create_text(425, 2000, text="screen", font=("Bahnschrift Light Condensed", 15), fill="#E5E5E5", anchor="nw", width=100)

        self.canvas.update_idletasks()  # Ensure all pending events are processed
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def make_seats(self):
        num_seats_per_row = 18
        button_width = 20
        button_spacing = 5

        total_button_width = num_seats_per_row * button_width + (num_seats_per_row - 1) * button_spacing
        start_x = (900 - total_button_width) // 2

        self.canvas.create_text(177, 50, text="Choose your seats: ", font=("Bahnschrift Light Condensed", 25), fill="#E5E5E5", anchor="nw")

        self.canvas.create_rectangle(172, 150, 727, 450, fill="#1e2749", outline="#1e2749")
        self.canvas.create_rectangle(172, 550, 727, 932, fill="#1e2749", outline="#1e2749")

        seat_rows = [("A", 190), ("B", 230), ("C", 300), ("D", 340), ("E", 380)]
        for row, y_cord in seat_rows:
            for col in range(num_seats_per_row):
                x_position = start_x + col * (button_width + button_spacing)
                y_position = y_cord +5 #Adjustment I made 
                seat_label = f"{row}{col}"
                self.button1 = ToggleButton(self.canvas, on_colour="#495057", off_colour="#e09f3e", on_command=lambda r=row, s=col: self.clicked_seat(r, s), off_command=lambda r=row, s=col: self.unlcicked_seat(r, s), anchor='n', bd=0, relief=FLAT)
                self.canvas.create_window(x_position, y_position, anchor="nw", window=self.button1, width=button_width, height=20)
                self.canvas.create_text(177, y_cord, text=row, font=("Bahnschrift Light Condensed", 15), fill="#E5E5E5", anchor="nw", width=100)
                self.canvas.create_text(x_position+5, 425, text=col+1, font=("Bahnschrift Light Condensed", 13), fill="#E5E5E5", anchor="nw", width=100)
                self.seat_buttons[seat_label] = self.button1
                if seat_label in self.booked_tickets:
                     self.button1.set_off_and_disable()
                     print(f"{seat_label} DISABLED") 
        

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


    def confirm_booking(self):
        if len(self.booked_seats) > 0:
            self.canvas.itemconfig(self.confirm_text_id, text="Booking Confirmed")
            print("Confirm booking")
            self.movie_info.save_booked_seats(file_path, self.index, self.date.strftime("%Y-%m-%d"), self.time, self.seats)

            self.movie_info.data = self.movie_info.load_data(file_path)

            self.after(1000, self.destroy)
        else:
            self.button2.config(state=DISABLED)


    def update_seat_buttons(self):
        booked_seats_entry = next((entry for entry in self.movie_info.data[self.index]["booked_seats"] if entry["date"] == self.date.strftime("%Y-%m-%d") and entry["time"] == self.time), {"seats": []})
        self.booked_tickets = booked_seats_entry["seats"]


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
            
            
    def clicked_seat(self, row, seat):
        seat_num = (f"{row}{seat}")
        print(f"Clicked seat {seat_num}")
        self.seats.append(seat_num)
        print(self.seats)
        for button in self.buttons.values():
            button.config(state=NORMAL)
    
    def unlcicked_seat(self, row, seat):
        seat_num = (f"{row}{seat}")
        print(f"Unclicked seat {seat_num}")
        self.seats.remove(seat_num)
        print(self.seats)
        x = len(self.seats)
        if len(self.booked_seats) > x >= 0:
            for button in self.buttons.values():
              button.config(state=DISABLED)
            self.button2.config(state=DISABLED)
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