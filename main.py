import tkinter as tk
from tkinter import filedialog, messagebox
import random, threading


class MainWindow(tk.Tk):


    # Template for the four answer buttons
    class AnswerButton(tk.Button):


        def __init__(self, *args, **kwargs):

            tk.Button.__init__(self, *args, **kwargs)
            self["width"] = 20
            self["height"] = 4


    def __init__(self):

        self.score = 0
        self.labels = []
        self.buttons = []

        # Basic window properties
        super().__init__()
        self.title("Nas Says")
        self.geometry("300x400")
        self.resizable(width=False, height=False)
        
        icon = tk.PhotoImage(file="nas_says.png")
        self.iconphoto(False, icon)

        # Settings button and menu
        self.settings_button = tk.Menubutton(self, text="⚙️")
        self.settings_button.pack(anchor=tk.NE)
        self.buttons.append(self.settings_button)

        self.time_limit = tk.IntVar()
        self.settings_menu = tk.Menu(self.settings_button, tearoff=0)
        self.settings_menu.add_radiobutton(
                                            label="3 seconds",
                                            variable=self.time_limit,
                                            value=3
                                        )
        self.settings_menu.add_radiobutton(
                                            label="5 seconds",
                                            variable=self.time_limit,
                                            value=5
                                        )
        self.settings_menu.add_command(
                                        label="Set as default",
                                        command=lambda:self.set_data(1, self.time_limit.get())
                                    )
        self.settings_menu.add_separator()
        self.settings_menu.add_command(
                                    label="Load theme...",
                                    command=lambda:self.load_theme("")
                                )
        self.settings_menu.add_command(
                                    label="Reset theme",
                                    command=self.reset_theme
                                    )
        self.settings_menu.add_separator()
        self.settings_menu.add_command(
                                        label="How to play",
                                        command=self.how_to_play
                                     )
        self.settings_button["menu"] = self.settings_menu

        self.get_data()
        self.time_limit.set(int(self.line_vals[1]))

        # Basic labels
        self.command = tk.Label(self)
        self.command.place(relx=0.5, rely=0.05, anchor=tk.N)
        self.labels.append(self.command)

        self.time_label = tk.Label(self)
        self.time_label.place(relx=0.5, rely=0.1, anchor=tk.N)
        self.labels.append(self.time_label)

        self.scoreboard = tk.Label(self)
        self.scoreboard.place(relx=0.5, rely=0.15, anchor=tk.N)
        self.labels.append(self.scoreboard)

        self.high_scoreboard = tk.Label(self)
        self.high_scoreboard.place(relx=0.5, rely=0.2, anchor=tk.N)
        self.labels.append(self.high_scoreboard)

        # Frames for stacking buttons (ordered bottom-top)
        self.state_frame = tk.Frame(self)
        self.state_frame.pack(side="bottom")

        self.ans_bframe = tk.Frame(self)
        self.ans_bframe.pack(side="bottom")

        self.ans_tframe = tk.Frame(self)
        self.ans_tframe.pack(side="bottom")

        # State buttons
        self.end_button = tk.Button(
                                    self.state_frame,
                                    text="End",
                                    width=42,
                                    height=2,
                                    command=self.end
                                )
        self.buttons.append(self.end_button)
        
        self.start_button = tk.Button(
                                    self.state_frame,
                                    text="Start",
                                    width=42,
                                    height=2,
                                    command=self.start
                                )
        self.buttons.append(self.start_button)

        # Answer buttons using template class, using lambdas to pass args to command
        self.tl_button = self.AnswerButton(self.ans_tframe, command=lambda:self.answered(0))
        self.tr_button = self.AnswerButton(self.ans_tframe, command=lambda:self.answered(1))
        self.bl_button = self.AnswerButton(self.ans_bframe, command=lambda:self.answered(2))
        self.br_button = self.AnswerButton(self.ans_bframe, command=lambda:self.answered(3))

        # Loading saved theme if present else default theme
        if self.line_vals[2]:
            self.load_theme(self.line_vals[2])
        else:
            self.reset_theme()

        self.reset()

    # Gets all data from data file
    def get_data(self):

        with open("data.txt", "r") as file:
            lines = [line.rstrip("\n") for line in file.readlines()]
            self.line_labels = [line.split("=")[0] for line in lines]
            self.line_vals = [line.split("=")[1] for line in lines]

    # Sets the value of one line of the data file
    def set_data(self, n, val):

        self.get_data()
        with open("data.txt", "w") as file:
            line = ""
            for i, line_label in enumerate(self.line_labels):
                if i == n:
                    line += line_label + "=" + str(val)
                else:
                    line += line_label + "=" + str(self.line_vals[i])
                line += "\n"
            file.write(line)

    # Sets theme
    def set_theme(self):

        self.configure(bg=self.window)

        self.state_frame["bg"] = self.window
        self.ans_bframe["bg"] = self.window
        self.ans_tframe["bg"] = self.window

        for label in self.labels:
            label["bg"] = self.window
            label["fg"] = self.text   
        
        for button in self.buttons:
            button["bg"] = self.button
            button["fg"] = self.text
            button["activebackground"] = self.active_button
            button["activeforeground"] = self.active_text

        for button in [self.tl_button, self.tr_button, self.bl_button, self.br_button]:
            button["activebackground"] = self.active_button

    # Resets theme values to defaults
    def reset_theme(self):

        self.window = "white",
        self.button = "white",
        self.text = "black",
        self.active_button = "white"
        self.active_text = "black"
        self.colour1 = ["green", "GREEN"]
        self.colour2 = ["red", "RED"]
        self.colour3 = ["magenta", "MAGENTA"]
        self.colour4 = ["blue", "BLUE"]
        
        self.set_theme()
        self.set_data(2, "")

    # Loads theme from filepath
    def load_theme(self, filepath=""):
        
        if not filepath:
            filepath = filedialog.askopenfilename()
        with open(filepath, "r") as file:
            lines = [line.rstrip("\n") for line in file.readlines()]
            lines = [line.split("=")[1] for line in lines]
            self.window = lines[0]
            self.button = lines[1]
            self.text = lines[2]
            self.active_button = lines[3]
            self.active_text = lines[4]
            self.colour1 = [lines[5].split(",")[0], lines[5].split(",")[1]]
            self.colour2 = [lines[6].split(",")[0], lines[6].split(",")[1]]
            self.colour3 = [lines[7].split(",")[0], lines[7].split(",")[1]]
            self.colour4 = [lines[8].split(",")[0], lines[8].split(",")[1]]
        self.set_theme()
        self.set_data(2, filepath)

    # Displays how to play messagebox
    def how_to_play(self):

        messagebox.showinfo(
                            title="How to play",
                            message="\n".join((
                                "What Simon says, he knows",
                                "You should follow as Nas shows",
                                "Else touch nothing 'til time goes",
                                "Get it wrong or take too long",
                                "And your score will soon be gone",
                                "\nGood luck!"
                            ))
                        )

    # Displays home screen
    def reset(self):

        # Resetting basic labels
        self.command["text"] = "Welcome to Nas Says"
        self.command["fg"] = self.text

        self.time_label["text"] = "Press Start to begin"

        self.scoreboard["text"] = ""

        # Getting and setting high score
        self.get_data()
        high_score = max(int(self.line_vals[0]), self.score)
        self.set_data(0, high_score)
        self.high_scoreboard["text"] = f"High Score: {high_score}"

        self.start_button.pack()

        self.score = 0
        
    # Starts a game
    def start(self):

        # Showing answer buttons
        self.tl_button.pack(side="left")
        self.tr_button.pack(side="right")
        self.bl_button.pack(side="left")
        self.br_button.pack(side="right")

        self.start_button.pack_forget()
        self.end_button.pack()

        self.turn()

    # Ends a game
    def end(self):
        
        # Trying to cancel all timers - ignoring error for no timers
        try:
            self.cancel_timers()
        except AttributeError:
            pass

        # Hiding answer buttons
        self.tl_button.pack_forget()
        self.tr_button.pack_forget()
        self.bl_button.pack_forget()
        self.br_button.pack_forget()

        self.end_button.pack_forget()

        self.reset()

    # Plays a turn
    def turn(self):

        # Trying to cancel all timers - ignoring error for no timers
        try:
            self.cancel_timers()
        except AttributeError:
            pass

        self.set_time_limit()

        # *says starters are 2x weighted
        starters = ["Simon says press ", "Nas says press "]
        starters += starters
        starters += ["Press "]

        colour_dict = {
            self.colour1[1]: self.colour1[0],
            self.colour2[1]: self.colour2[0],
            self.colour3[1]: self.colour3[0],
            self.colour4[1]: self.colour4[0]
        }

        # Choosing and applying a random starter, colour, and text colour
        starter = random.choice(starters)
        colour = random.choice(list(colour_dict.keys()))
        tcolour = random.choice(list(colour_dict.values()))

        self.command["text"] = starter + colour
        self.command["fg"] = tcolour

        # Choosing and applying random colours for answer buttons
        bcolours = list(colour_dict.values())
        random.shuffle(bcolours)
        self.tl_button["bg"] = bcolours[0]
        self.tr_button["bg"] = bcolours[1]
        self.bl_button["bg"] = bcolours[2]
        self.br_button["bg"] = bcolours[3]

        self.scoreboard["text"] = f"Score: {self.score}"

        # Determining answer
        if starter == starters[0]:
            self.answer = bcolours.index(colour_dict[colour])
        elif starter == starters[1]:
            self.answer = bcolours.index(tcolour)
        else:
            self.answer = 4

        # Running timers
        self.set_timer(0)
        for timer in self.timers:
            timer.start()

    # Sets time label
    def set_timer(self, n):
            
            self.time_label["text"] = f"Time Left: {self.time_limit.get() - n}"

    # Sets time limit
    def set_time_limit(self):

        # Creates a timer to go off each second, each updating the time label
        # until the last, which submits an answer
        self.timers = []
        time_limit = self.time_limit.get()
        for i in range(1, time_limit):
            self.timers.append(threading.Timer(i, self.set_timer, args=[i]))
        self.timers.append(threading.Timer(time_limit, self.answered, args=[4]))

    # Cancels timers
    def cancel_timers(self):

        for timer in self.timers:
            timer.cancel()

    # Submits an answer
    def answered(self, n):

        if n == self.answer:
            self.score += 1
            self.turn()
        else:
            self.end()
            

if __name__ == "__main__":
    main_window = MainWindow()
    main_window.mainloop()
