from tkinter import *
import TwitterClient


root = Tk()
root.title("Twitter Analysis")
root.geometry("400x400")
title = Label(root, text="Welcome to Twitter Analysis")
title.pack()
label = Label(root, text="Enter your query:")
label.pack(side=LEFT)
name = StringVar()
field = Entry(root, textvariable=name)
field.pack(side=LEFT)


def do_it():
    return str(name.get())


submitButton = Button(root, text="Submit", command=TwitterClient.main(do_it))
submitButton.pack(side=LEFT)


root.mainloop()
