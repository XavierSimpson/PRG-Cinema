from tkinter import* 

class Cinema:
    
    def __init__(self):
        
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
        
        self.movie_frame = Label(self.cinema_frame, bg = "#14213D", width=750, height=600)
        self.movie_frame.grid(row=2)  
        
        self.movie_1_button = Button(self.movie_frame,
                                        text="movie one",
                                        bg= "#FCA311",
                                        fg= "#FFFFFF",
                                        font= ("Poppins", "12"), width=12, height=10)
        self.movie_1_button.grid(row=0, column=0, padx=5, pady=5)  
        
        self.movie_2_button = Button(self.movie_frame,
                                        text="movie two",
                                        bg= "#FCA311",
                                        fg= "#FFFFFF",
                                        font= ("Poppins", "12"), width=12, height=10)
        self.movie_2_button.grid(row=0, column=1, padx=5, pady=5)   
        
        self.movie_3_button = Button(self.movie_frame,
                                        text="movie three",
                                        bg= "#FCA311",
                                        fg= "#FFFFFF",
                                        font= ("Poppins", "12"), width=12, height=10)
        self.movie_3_button.grid(row=0, column=2, padx=5, pady=5)   
        
        self.movie_4_button = Button(self.movie_frame,
                                        text="movie four",
                                        bg= "#FCA311",
                                        fg= "#FFFFFF",
                                        font= ("Poppins", "12"), width=12, height=10)
        self.movie_4_button.grid(row=0, column=3, padx=5, pady=5)         

        
# main routine    
if __name__ == "__main__":
    root = Tk()
    root.title("Cinema")
    Cinema()
    root.mainloop()