from tkinter import* 
from PIL import Image, ImageTk

class Cinema:
    
    def __init__(self):

        # Load an image using Pillow

        # Movie Posters 
        image_path = r"C:\Users\xavie\Downloads\image-from-rawpixel-id-9975454-original.jpg"
        image = Image.open(image_path)

        image_path1 = r"C:\Users\xavie\Downloads\image-from-rawpixel-id-9976112-original.jpeg"
        image1 = Image.open(image_path1)

        image_path2 = r"C:\Users\xavie\Downloads\image-from-rawpixel-id-9976560-original.jpg"
        image2 = Image.open(image_path2)

        image_path3 = r"C:\Users\xavie\Downloads\image-from-rawpixel-id-9976063-original.jpg"
        image3 = Image.open(image_path3)

        # Resize the image
        # Set your desired width and height
        desired_width = 130
        desired_height = 193
        resized_image = image.resize((desired_width, desired_height), Image.Resampling.LANCZOS)
        resized_image1 = image1.resize((desired_width, desired_height), Image.Resampling.LANCZOS)
        resized_image2 = image2.resize((desired_width, desired_height), Image.Resampling.LANCZOS)
        resized_image3 = image3.resize((desired_width, desired_height), Image.Resampling.LANCZOS)

        # Convert the image to a Tkinter-compatible PhotoImage
        photo = ImageTk.PhotoImage(resized_image)
        photo1 = ImageTk.PhotoImage(resized_image1)
        photo2 = ImageTk.PhotoImage(resized_image2)
        photo3 = ImageTk.PhotoImage(resized_image3)

        # Cinema Frame 
        self.cinema_frame = Frame(bg = "#19294D")
        self.cinema_frame.grid()
        
        self.cinema_heading = Label(self.cinema_frame,
                                  text="RIZZ Cinema",
                                  font=("Poppins", "18", "bold"),
                                  fg="#FCA311",
                                  bg ="#19294D", width= 40, height = 2)
        
        self.cinema_heading.grid(row=0, pady=5) 
        
        self.cinema_showing = Label(self.cinema_frame,
                                       text="Now showing",
                                       font=("Poppins", "11", "bold"),
                                       fg="#FFFFFF", bg ="#14213D")
        
        self.cinema_showing.grid(row=1, columnspan=4, sticky="WE")   


        @staticmethod
        def on_button_click():
            print("hello!")
        

        # Frame for Movies all together 
        self.movie_frame = Frame(self.cinema_frame, bg = "#14213D")
        self.movie_frame.grid(row=2) 

        # Frame for Side Tab
        self.side_tab = Frame(self.movie_frame, bg="#1E325C", width=20, height=30)
        self.side_tab.grid(row=0, column=0, padx=5, pady=5)

        self.side_tab_label = Label(self.side_tab, text="Movies", font=("Poppins", "11", "bold"),
                                       fg="#FFFFFF", bg ="#14213D", justify="left")
        self.side_tab_label.grid(row=0, pady=5)

        self.side_tab_label_1 = Label(self.side_tab, text="Session Times", font=("Poppins", "11", "bold"),
                                       fg="#FFFFFF", bg ="#14213D", justify="left")
        self.side_tab_label_1.grid(row=1, pady=5)

        self.side_tab_label_2 = Label(self.side_tab, text="Cinemas", font=("Poppins", "11", "bold"),
                                       fg="#FFFFFF", bg ="#14213D", justify="left")
        self.side_tab_label_2.grid(row=2, pady=5)

        self.side_tab_label_3 = Label(self.side_tab, text="Food & Snacks", font=("Poppins", "11", "bold"),
                                       fg="#FFFFFF", bg ="#14213D", justify="left")
        self.side_tab_label_3.grid(row=3, pady=5)



        # Frame for movie and name
        self.movie_1_frame = Frame(self.movie_frame, bg = "#14213D") 
        self.movie_1_frame.grid(row=0, column=1, pady=5)  
        
        self.movie_1_button = Button(self.movie_1_frame, image=photo, command=on_button_click, bd=0, relief=FLAT)
        self.movie_1_button.image = photo
        self.movie_1_button.grid(row=0, column=0, padx=5, pady=5) 

        self.movie_1_label = Label(self.movie_1_frame, text="Movie One", font=("Poppins", "11", "bold"),
                                       fg="#FFFFFF", bg ="#14213D") 
        self.movie_1_label.grid(row=1)

        self.movie_2_frame = Frame(self.movie_frame, bg = "#14213D") 
        self.movie_2_frame.grid(row=0, column=2, pady=5) 
        
        self.movie_2_button = Button(self.movie_2_frame, image=photo1, command=on_button_click, bd=0, relief=FLAT)
        self.movie_2_button.image = photo1
        self.movie_2_button.grid(row=0, column=0, padx=5, pady=5)   

        self.movie_2_label = Label(self.movie_2_frame, text="Movie Two", font=("Poppins", "11", "bold"),
                                       fg="#FFFFFF", bg ="#14213D") 
        self.movie_2_label.grid(row=1)

        self.movie_3_frame = Frame(self.movie_frame, bg="#14213D")
        self.movie_3_frame.grid(row=0, column=3, pady=5) 
        
        self.movie_3_button = Button(self.movie_3_frame, image=photo2, command=on_button_click, bd=0, relief=FLAT)
        self.movie_3_button.image = photo2
        self.movie_3_button.grid(row=0, column=0, padx=5, pady=5)  

        self.movie_3_label = Label(self.movie_3_frame, text="Movie Three", font=("Poppins", "11", "bold"),
                              fg="#FFFFFF", bg ="#14213D")
        self.movie_3_label.grid(row=1)

        self.movie_4_frame = Frame(self.movie_frame, bg="#14213D")
        self.movie_4_frame.grid(row=0, column=4, pady=5)

        self.movie_4_button = Button(self.movie_4_frame, image=photo3, command=on_button_click, bd=0, relief=FLAT)
        self.movie_4_button.image = photo3
        self.movie_4_button.grid(row=0, column=0, padx=5, pady=5)       

        self.movie_4_label = Label(self.movie_4_frame, text="Movie Four", font=("Poppins", "11", "bold"),
                              fg="#FFFFFF", bg ="#14213D")  
        self.movie_4_label.grid(row=1)

        
# main routine    
if __name__ == "__main__":
    root = Tk()
    root.title("Cinema")
    Cinema()
    root.mainloop()