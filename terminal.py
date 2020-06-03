#
# Serial COM Port terminal program
# 8/17/2017, Dale Gambill
# I wrote 2 modules for this program: terminal.py and serial_rx_tx.py.
#
import tkinter as tk
import tkinter.scrolledtext as tkscrolledtext
from tkinter import *
from tkinter import filedialog
import serial_rx_tx
import _thread
import time
import webbrowser
from tkinter import messagebox
import numpy as np
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
import xlsxwriter

# globals
check_MSE = False
value = np.zeros(3)
array_value = []
serialPort = serial_rx_tx.SerialPort()
logFile = None

root = tk.Tk() # create a Tk root window
root.title( "TERMINAL - COLOR DETECTOR SENSOR" )
# set up the window size and position
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = screen_width/2
window_height = screen_width/3
window_position_x = screen_width/2 - window_width/2
window_position_y = screen_height/2 - window_height/2
root.geometry('%dx%d+%d+%d' % (window_width, window_height, window_position_x, window_position_y))
# scrolled text box used to display the serial data
frame = tk.Frame(root, bg='cyan')
frame.pack(side="bottom", fill='both', expand='no')
textbox = tkscrolledtext.ScrolledText(master=frame, wrap='word', width=180, height=28) #width=characters, height=lines
textbox.pack(side='bottom', fill='y', expand=True, padx=0, pady=0)
textbox.config(font="bold")

#COM Port label
label_comport = Label(root,width=10,height=2,text="COM Port:")
label_comport.place(x=10,y=26)
label_comport.config(font="bold")

#COM Port entry box
comport_edit = Entry(root,width=10)
comport_edit.place(x=100,y=36)
comport_edit.config(font="bold")
comport_edit.insert(END,"COM9")

#Color prediction label
label_color = Label(frame, width=20, height=2, text = "Color prediction")
label_color.place(x=800, y = 10)
label_color.config(font=("bold",30), bg='white')

#Color predict
size = (120,120,3)
color = np.ones(size, dtype=np.uint8)
img = color*np.array([255,255,0], dtype=np.uint8)
img =  ImageTk.PhotoImage(image=Image.fromarray(img))
canvas = Label(frame,width=size[0],height=size[1], image=img)
canvas.place(x=970,y=110)
canvas.config(bg = 'red')
def clear_error(entry, insert):
    entry.delete(first=0, last =END)
    entry.insert(END, str(insert))
def insert_error(var_array):
    average = np.sum(var_array, axis=0)/len(var_array)
    var = np.sum((average - var_array)**2, axis =0)/len(var_array)
    var = var.astype(int)
    std_ = np.ceil(np.sqrt(var)).astype(int)
    clear_error(variance_r, var[0])
    clear_error(variance_g, var[1])
    clear_error(variance_b, var[2])
    clear_error(std_dev, "Standard deviation (R- G- B): " + str(std_))
    if check_MSE:
        MSE = np.sum((var_array-np.array([255,255,255]))**2, axis = 0)/len(var_array)
        MSE = MSE.astype(int)
        rMSE = np.ceil(np.sqrt(MSE)).astype(int)
        
        clear_error(MSE_r, MSE[0])
        clear_error(MSE_g, MSE[1])
        clear_error(MSE_b, MSE[2])
        clear_error(root_MSE, "Root_MSE (R-G-B): " + str(rMSE))


# Show Color prediction 
def showColor(str_message):
    global value
    if len(str_message) > 20:
        value_RGB = [int(s) for s in str_message.split() if s.isdigit()]
        if (len(value_RGB) ==3):
            value = value_RGB.copy()
            f = open("data.txt", "w")
            f.write(str(value_RGB))
            f.close()
            print(value_RGB)
            color_predict= color*np.array(value_RGB, dtype=np.uint8)
            img2 = ImageTk.PhotoImage(image=Image.fromarray(color_predict))
            canvas.configure(image=img2)
            canvas.image = img2

# serial data callback function
def OnReceiveSerialData(message):
    str_message = message.decode("utf-8")
    textbox.insert('1.0', str_message)
    showColor(str_message)
    if button_xlsx['text'] == 'Close Xlsx file':
        array_value.append(value)
# Register the callback above with the serial port object
serialPort.RegisterReceiveCallback(OnReceiveSerialData)

def sdterm_main():
    root.after(200, sdterm_main)  # run the main loop once each 200 ms

#
#  commands associated with button presses
#
def OpenCommand():
    if button_openclose.cget("text") == 'Open COM Port':
        comport = comport_edit.get()
        baudrate = baudrate_edit.get()
        serialPort.Open(comport,baudrate)
        button_openclose.config(text='Close COM Port')
        textbox.insert('1.0', "COM Port Opened\r\n")
    elif button_openclose.cget("text") == 'Close COM Port':
        if button_replaylog.cget('text') == 'Stop Replay Log':
            textbox.insert('1.0',"Stop Log Replay first\r\n")
        else:
            serialPort.Close()
            button_openclose.config(text='Open COM Port')
            textbox.insert('1.0',"COM Port Closed\r\n")
def WriteXlsxFile():
    global array_value
    if button_xlsx.cget("text") == 'Write Xlsx file':
        button_xlsx.config(text='Close Xlsx file')
        textbox.insert('1.0', "Writting Xlsx file\r\n")
    elif button_xlsx.cget("text") == 'Close Xlsx file':
        button_xlsx.config(text='Write Xlsx file')
        textbox.insert('1.0',"Xlsx File Closed\r\n")
        #write data to xlsx file
        workbook = xlsxwriter.Workbook('data.xlsx', {'constant_memory': True})
        worksheet = workbook.add_worksheet('color value')
        col = 0
        worksheet.write_row(0,0,['Red', 'Green', 'Blue'])
        for row, data in enumerate(array_value,1):
            worksheet.write_row(row, col, data)
        workbook.close()
        insert_error(array_value)
        array_value=[]
def ClearDataCommand():
    textbox.delete('1.0',END)

def SendDataCommand():
    global check_MSE
    message = senddata_edit.get()
    if serialPort.IsOpen():
        if message =='check':
            check_MSE = True
        elif message == 'do not check':
            check_MSE = False
        message += '\r\n'
        serialPort.Send(message)
        textbox.insert('1.0',message)

    else:
        textbox.insert('1.0', "Not sent - COM port is closed\r\n")

def ReplayLogFile():
    try:
      if logFile != None:
        readline = logFile.readline()
        global serialPort
        serialPort.Send(readline)
    except:
      print("Exception in ReplayLogFile()")

def ReplayLogThread():
    while True:
        time.sleep(1.0)
        global logFile
        if serialPort.IsOpen():
            if logFile != None:
                ReplayLogFile()

def OpenLogFile():
    if not serialPort.IsOpen():
        textbox.insert('1.0', "Open COM port first\r\n")
    else:
        if button_replaylog.cget('text') == 'Replay Log':
            try:
                root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                           filetypes=(("log files", "*.log"), ("all files", "*.*")))
                global logFile
                logFile = open(root.filename,'r')
                _thread.start_new_thread(ReplayLogThread, ())
                button_replaylog.config(text='Stop Log Replay')
                textbox.insert('1.0', "Sending to open COM port from: " + root.filename + "\r\n")
            except:
                textbox.insert('1.0', "Could not open log file\r\n")
        else:
            button_replaylog.config(text='Replay Log')
            textbox.insert('1.0', "Stopped sending messages to open COM port\r\n")
            logFile = None

# COM Port open/close button
button_openclose = Button(root,text="Open COM Port",width=20,command=OpenCommand)
button_openclose.config(font="bold")
button_openclose.place(x=210,y=30)

# Xlsx Write/ Close button
button_xlsx = Button(root,text="Write Xlsx file",width=20,command=WriteXlsxFile)
button_xlsx.config(font="bold")
button_xlsx.place(x=620,y=30)

#Clear Rx Data button
button_cleardata = Button(root,text="Clear Rx Data",width=20,command=ClearDataCommand)
button_cleardata.config(font="bold")
button_cleardata.place(x=210,y=72)

#Send Message button
button_senddata = Button(root,text="Send Message",width=20,command=SendDataCommand)
button_senddata.config(font="bold")
button_senddata.place(x=420,y=72)

#Replay Log button
button_replaylog = Button(root,text="Replay Log",width=20,command=OpenLogFile)
button_replaylog.config(font="bold")
button_replaylog.place(x=420,y=30)

#
# data entry labels and entry boxes
#

#Send Data entry box
senddata_edit = Entry(root,width=34)
senddata_edit.place(x=620,y=78)
senddata_edit.config(font="bold")
senddata_edit.insert(END,"Message")

#Baud Rate label
label_baud = Label(root,width=10,height=2,text="Baud Rate:")
label_baud.place(x=10,y=70)
label_baud.config(font="bold")

#Baud Rate entry box
baudrate_edit = Entry(root,width=10)
baudrate_edit.place(x=100,y=80)
baudrate_edit.config(font="bold")
baudrate_edit.insert(END,"9600")

#Label variance
variance = Label(frame, width =30, height =8, text="Variance ", anchor=N)
variance.config(font=("bold",14), bg='white')
variance.place(x=880, y=260)

MSE_label= Label(variance, width =30, height =2, text="Mean Square Error ", anchor=N)
MSE_label.config(font=("bold",14), bg='white')
MSE_label.place(x=0, y=70)

# Calculate Variance
variance_r = Entry(variance, width=8)
variance_r.config(font=("bold",12))
variance_r.pack(side = LEFT)
variance_r.place(x= 30, y= 40)
variance_r.insert(END,"0")

variance_g = Entry(variance, width=8)
variance_g.config(font=("bold",12))
variance_g.pack(side = LEFT)
variance_g.place(x=120, y=40)
variance_g.insert(END, "0")

variance_b = Entry(variance, width=8)
variance_b.config(font=("bold",12))
variance_b.pack(side = LEFT)
variance_b.place(x=220, y=40)
variance_b.insert(END, "0")


# MSE
MSE_r = Entry(variance, width=8)
MSE_r.config(font=("bold",12))
MSE_r.pack(side = LEFT)
MSE_r.place(x= 30, y= 110)
MSE_r.insert(END,"0")

MSE_g = Entry(variance, width=8)
MSE_g.config(font=("bold",12))
MSE_g.pack(side = LEFT)
MSE_g.place(x=120, y=110)
MSE_g.insert(END, "0")

MSE_b = Entry(variance, width=8)
MSE_b.config(font=("bold",12))
MSE_b.pack(side = LEFT)
MSE_b.place(x=220, y=110)
MSE_b.insert(END, "0")

# Summary
Result_label = Label(frame, width =100, height =8, )
Result_label.config(bg='white')
Result_label.place(x=600, y=400)

std_dev = Entry(Result_label, width =30)
std_dev.place(x=100, y = 30)
std_dev.config(font=("bold",12))
std_dev.insert(END, "Standard deviation (R- G- B): None")

root_MSE = Entry(Result_label, width = 26)
root_MSE.place(x=400, y = 30)
root_MSE.config(font=("bold",12))
root_MSE.insert(END, "Root_MSE (R- G- B): None")

#
# The main loop
#
root.after(200, sdterm_main)
root.mainloop()
#

