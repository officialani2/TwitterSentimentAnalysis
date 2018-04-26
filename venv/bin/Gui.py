from tkinter import *
from TwitterClient import main

root = Tk()
root.title("Twitter Analysis")

label = Label(root, text="Enter your query:")
label.pack(side=LEFT)
name = StringVar()
field = Entry(root)
field.pack(side=LEFT)


def do_it():
    return "Hello" + str(name.get())


submitButton = Button(root, text="Submit", command=main(do_it))
submitButton.pack(side=LEFT)


root.mainloop()
