from tkinter import* 
from PIL import Image, ImageTk

class Cinema:
    
    def __init__(self):

        # Load an image using Pillow
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

        self.cinema_frame = Frame(bg = "#14213D")
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
                                       fg="#FFFFFF", bg ="#14213D",
                                       wrap=250, width=40,
                                       justify="left")
        
        self.cinema_showing.grid(row=1)   


        @staticmethod
        def on_button_click():
            print("You clicked on ME")
        
        self.movie_frame = Frame(self.cinema_frame, bg = "#14213D")
        self.movie_frame.grid(row=2)  
        
        self.movie_1_button = Button(self.movie_frame, image=photo, command=on_button_click, bd=0, relief=FLAT)
        self.movie_1_button.image = photo
        self.movie_1_button.grid(row=0, column=0, padx=5, pady=5)  
        
        self.movie_2_button = Button(self.movie_frame, image=photo1, command=on_button_click, bd=0, relief=FLAT)
        self.movie_2_button.image = photo1
        self.movie_2_button.grid(row=0, column=1, padx=5, pady=5)   
        
        self.movie_3_button = Button(self.movie_frame, image=photo2, command=on_button_click, bd=0, relief=FLAT)
        self.movie_3_button.image = photo2
        self.movie_3_button.grid(row=0, column=2, padx=5, pady=5)   
        
        self.movie_4_button = Button(self.movie_frame, image=photo3, command=on_button_click, bd=0, relief=FLAT)
        self.movie_4_button.image = photo3
        self.movie_4_button.grid(row=0, column=3, padx=5, pady=5)         

        
# main routine    
if __name__ == "__main__":
    root = Tk()
    root.title("Cinema")
    Cinema()
    root.mainloop()