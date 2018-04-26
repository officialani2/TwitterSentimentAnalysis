from tkinter import *

root = Tk()

topFrame = Frame(root)
topFrame.pack()
bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM)

label1 = Label(topFrame, text="Enter your text", fg="grey")
textEnter = Entry(topFrame)
buttonSubmit = Button(topFrame, text="Submit", fg="black")

label1.pack(side=LEFT)
textEnter.pack(side=LEFT)
buttonSubmit.pack(side=LEFT)

root.mainloop()
