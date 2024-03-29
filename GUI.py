from tkinter import *
import numpy as np
from PIL import ImageGrab
import keras
from keras.models import load_model
from keras.models import Sequential
 
window = Tk()
window.title("Handwritten digit recognition")
l1 = Label()

model = load_model('mnist.h5')
modelchar = load_model('model_hand.h5')

word_dict = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H',8:'I',9:'J',
             10:'K',11:'L',12:'M',13:'N',14:'O',15:'P',16:'Q',17:'R',
             18:'S',19:'T',20:'U',21:'V',22:'W',23:'X', 24:'Y',25:'Z'}

def predict_digit(img):
    global label,res,reschar,img1,imgn
    imgn = img
    img = img.resize((28,28))
    img = img.convert('L')
    img = np.array(img)
    img = img.reshape(1,28,28,1)
    img = img/255.0

    img1 = img

    #Character Recognition
    imgn = imgn.resize((28,28))
    imgn = imgn.convert('L')
    imgn = np.array(imgn)
    imgn = imgn.reshape(1,28,28,1)

    #predicting the class
    res = model.predict([img])[0]
    reschar = modelchar.predict([imgn])[0]
    print(max(reschar))
    if max(res) >= max(reschar):
        label.configure(text= str(np.argmax(res))+', '+ str(int(max(res)*100))+'%')
        return np.argmax(res), max(res)
    else:
        label.configure(text= str(word_dict[np.argmax(reschar)])+', '+ str(int(max(reschar)*100))+'%')
        return np.argmax(reschar), max(reschar)

def classify_handwriting():
    global label
    try:
        t1.destroy()
    except:
        pass
    label = Label(window,text="Thinking..", font=("Helvetica", 48))
    widget = cv
    # Setting co-ordinates of canvas
    x = window.winfo_rootx() + widget.winfo_x()
    y = window.winfo_rooty() + widget.winfo_y()
    x1 = x + widget.winfo_width()
    y1 = y + widget.winfo_height()
    im = ImageGrab.grab().crop((x+150, y+150, x1+400, y1+400))
    #im.show()
    digit, acc = predict_digit(im)
    print(digit,acc)
    label.place(x=340, y=420)

    # Feedback
    corr_output = Label(window,text="Is the output correct?", font=("Helvetica", 20))
    corr_output.place(x=120,y=420)
    yes_button = Button(window, text="YES", font= 15, bg="white", fg="green", command=right_predict)
    yes_button.place(x=120, y=450)
    no_button = Button(window, text="NO", font= 15, bg="white", fg="red", command=wrong_pedict)
    no_button.place(x=180, y=450)
 
 
lastx, lasty = None, None
 
# Right Prefdiction(YES)
def right_predict():
    global res,reschar,img1,imgn
    if max(res) >= max(reschar):
        x_train = np.array(img1)
        y_train = [np.argmax(res)]
        x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
        input_shape = (28, 28, 1)
        y_train = keras.utils.to_categorical(y_train, 10)
        x_train = x_train.astype('float32')
        hist = model.fit(x_train, y_train,batch_size=128,epochs=10,verbose=1)
    else:
        x_train = np.array(imgn)
        y_train = [np.argmax(reschar)]
        x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
        input_shape = (28, 28, 1)
        y_train = keras.utils.to_categorical(y_train, 10)
        x_train = x_train.astype('float32')
        hist = modelchar.fit(x_train, y_train,batch_size=128,epochs=10,verbose=1)

    blank = Label(window,height=10,width=8,font=("Helvetica", 40))
    blank.place(x=120,y=420)  


# Wrong Prediction(NO)
def wrong_pedict():
    global t1
    blank = Label(window,height=10,width=8,font=("Helvetica", 40))
    blank.place(x=120,y=420) 
    t1 = Text(window, height = 1,width = 3,font=("Helvetica", 45),bg = "white",fg="black")
    t1.place(x=120, y=420)
    bw = Button(window,text= '☠️',height = 1,width = 2,font=("Helvetica", 45),bg = "black",fg="black",command=wrong_done )
    bw.place(x=220, y=420)

def wrong_done():
    global t1,reschar,img1,imgn
    blank = Label(window,height=10,width=8,font=("Helvetica", 40))
    blank.place(x=120,y=420) 

    realchar = t1.get(1.0, "end-1c")

    if realchar[0].isnumeric():
        x_train = np.array(img1)
        y_train = [realchar]
        x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
        input_shape = (28, 28, 1)
        y_train = keras.utils.to_categorical(y_train, 10)
        x_train = x_train.astype('float32')
        hist = model.fit(x_train, y_train,batch_size=128,epochs=10,verbose=1)

    else:
        x_train = np.array(imgn)
        y_train = [i for i in word_dict if word_dict[i]==realchar]
        x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
        input_shape = (28, 28, 1)
        y_train = keras.utils.to_categorical(y_train, 10)
        x_train = x_train.astype('float32')
        hist = modelchar.fit(x_train, y_train,batch_size=128,epochs=10,verbose=1)


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
    cv.create_line((lastx, lasty, x, y), width=10, fill='white', capstyle=ROUND, smooth=TRUE, splinesteps=12)
    lastx, lasty = x, y
 
 
# Label
L1 = Label(window, text="Handwritten Character Recoginition", fg="green",font=("Times", 36))
L1.place(x=35, y=10)
 
# Button to clear canvas
b1 = Button(window, text="1. Clear Canvas", font=("Helvetica", "20", "bold italic"), bg="orange", fg="black", command=clear_widget)
b1.place(x=120, y=370)
 
# Button to predict digit drawn on canvas
b2 = Button(window, text="2. Prediction", font=("Helvetica", "20", "bold italic"), bg="white", fg="red", command=classify_handwriting)
b2.place(x=320, y=370)

 
# Setting properties of canvas
cv = Canvas(window, width=350, height=290, bg='black')
cv.place(x=120, y=70)

 
cv.bind('<Button-1>', event_activation)
window.geometry("600x500")
window.mainloop()

model.save('mnist1.h5')
modelchar.save(r'model_hand1.h5')
