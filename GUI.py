from tkinter import *
import numpy as np
from PIL import ImageGrab
from keras.models import load_model
#from Prediction import predict
 
window = Tk()
window.title("Handwritten digit recognition")
l1 = Label()

model = load_model('mnist.h5')
modelchar = load_model('model_hand.h5')

word_dict = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H',8:'I',9:'J',
             10:'K',11:'L',12:'M',13:'N',14:'O',15:'P',16:'Q',17:'R',
             18:'S',19:'T',20:'U',21:'V',22:'W',23:'X', 24:'Y',25:'Z'}

def predict_digit(img):
    #resize image to 28x28 pixels
    img = img.resize((28,28))
    #convert rgb to grayscale
    img = img.convert('L')
    img = np.array(img)
    #reshaping to support our model input and normalizing
    img = img.reshape(1,28,28,1)
    img = img/255.0
    #predicting the class
    res = model.predict([img])[0]
    reschar = modelchar.predict([img])[0]
    # if max(res) >= max(reschar):
    #     return np.argmax(res), max(res)
    # else:
    #     return np.argmax(reschar), max(reschar)

    return np.argmax(reschar), max(reschar)

def classify_handwriting():
    label = Label(window,text="Thinking..", font=("Helvetica", 48))
    widget = cv
    # Setting co-ordinates of canvas
    x = window.winfo_rootx() + widget.winfo_x()
    y = window.winfo_rooty() + widget.winfo_y()
    x1 = x + widget.winfo_width()
    y1 = y + widget.winfo_height()
    im = ImageGrab.grab().crop((x+150, y+150, x1+300, y1+300))
    im.show()
    digit, acc = predict_digit(im)
    print(digit,acc)
    label.configure(text= str(word_dict[digit])+', '+ str(int(acc*100))+'%')
    label.place(x=340, y=420)
 
 
lastx, lasty = None, None
 
 
# Clears the canvas
def clear_widget():
    global cv, l1
    cv.delete("all")
    l1.destroy()
 
 
# Activate canvas
def event_activation(event):
    global lastx, lasty
    cv.bind('<B1-Motion>', draw_lines)
    lastx, lasty = event.x, event.y
 
 
# To draw on canvas
def draw_lines(event):
    global lastx, lasty
    x, y = event.x, event.y
    cv.create_line((lastx, lasty, x, y), width=10, fill='black', capstyle=ROUND, smooth=TRUE, splinesteps=12)
    lastx, lasty = x, y
 
 
# Label
L1 = Label(window, text="Handwritten Digit Recoginition", font= 25, fg="blue")
L1.place(x=35, y=10)
 
# Button to clear canvas
b1 = Button(window, text="1. Clear Canvas", font= 15, bg="orange", fg="black", command=clear_widget)
b1.place(x=120, y=370)
 
# Button to predict digit drawn on canvas
b2 = Button(window, text="2. Prediction", font= 15, bg="white", fg="red", command=classify_handwriting)
b2.place(x=320, y=370)
 
# Setting properties of canvas
cv = Canvas(window, width=350, height=290, bg='white')
cv.place(x=120, y=70)
 
cv.bind('<Button-1>', event_activation)
window.geometry("600x500")
window.mainloop()