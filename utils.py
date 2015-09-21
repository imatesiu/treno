from Tkinter import *

def sel():
   selection = "Value = " + str(var.get())
   label.config(text = selection)

root = Tk()
var = DoubleVar()

scale = Scale( root,from_=0, to=1020, variable = var,orient=HORIZONTAL )
scale.pack(anchor=CENTER)

button = Button(root, text="Get Scale Value", command=sel)
button.pack(anchor=CENTER)

label = Label(root)
label.pack()
selection = "Value = " 
label.config(text = selection)
root.mainloop()