from Tkinter import *
import tkMessageBox
import tkSimpleDialog
import tkFileDialog

t = Tk()

title = "Untitled"

t.wm_title(title)

saved = False
hasname = False

scroll = Scrollbar(t)
codebox = Text(t, height = t.winfo_screenheight() - 50, width = t.winfo_screenwidth())


menubar = Menu(t)
t.config(menu = menubar)

def newfile():
    global hasname
    global saved
    ow = False
    if not saved:
        ow = tkMessageBox.askyesno("New File", "Save current project?")
        if not ow:
            codebox.delete("1.0", END)
            hasname = False
            saved = False
            title = "Untitled"
            t.wm_title(title)
        else:
            save()
            codebox.delete("1.0", END)
            hasname = False
            saved = False
            title = "Untitled"
            t.wm_title(title)
    else:
        hasname = False
        saved = False
        codebox.delete("1.0", END)
        title = "Untitled"
        t.wm_title(title)
   
def save():
    global hasname
    global saved
    global title
    if not saved:
        if not hasname:
            name = tkSimpleDialog.askstring("Save as", "Name your file: ")
            hasname = True
        
        saved = True
        name = name + ".brain"
        f = open(name, 'w+')
        f.write(codebox.get("1.0", END))
        f.close()
        
        title = name
        t.wm_title(title)

def key(pressed):
    global saved
    global title
    saved = False    
    if "*" not in title:
        title = "* " + title 
        t.wm_title(title)

def openfile():
    ftypes = [('Brain files', '*.brain'), ('All files', '*')]
    dlg = tkFileDialog.Open(t, filetypes = ftypes)
    fl = dlg.show()
    
    if fl != '':
        with open(fl) as f:
            text = f.read()
            codebox.delete("1.0", END)
            codebox.insert(END, text)
            
        title = fl
        t.wm_title(title)
            

def helloworld():
    global hasname
    global saved
    ow = False
    if not saved:
        ow = tkMessageBox.askyesno("New File", "Save current project?")
        if not ow:
            codebox.delete("1.0", END)
            codebox.insert("1.0", ">+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.>>>++++++++[<++++>-]<.>>>++++++++++[<+++++++++>-]<---.<<<<.+++.------.--------.>>+.>++++++++++.")
            hasname = False
            saved = False
        else:
            save()
            codebox.delete("1.0", END)
            codebox.insert("1.0", ">+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.>>>++++++++[<++++>-]<.>>>++++++++++[<+++++++++>-]<---.<<<<.+++.------.--------.>>+.>++++++++++.")
    else:
        hasname = False
        saved = False
        codebox.delete("1.0", END)
        codebox.insert("1.0", ">+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.>>>++++++++[<++++>-]<.>>>++++++++++[<+++++++++>-]<---.<<<<.+++.------.--------.>>+.>++++++++++.")
     
def runcode():
    result = eval(codebox.get("1.0", END))
    logsfor = "Logs for", title.replace("* ", "")
    tkMessageBox.showinfo(logsfor, result)
        
file_menu = Menu(menubar)
run_menu = Menu(menubar)
sub_file = Menu(file_menu)
sub_file.add_command(label = "Hello World Template", command = helloworld)
sub_file.add_command(label = "Empty Project", command = newfile)
file_menu.add_cascade(label = "New", menu = sub_file)
file_menu.add_command(label = "Save", command = save)
file_menu.add_command(label = "Open", command = openfile)
menubar.add_cascade(label = "File", menu = file_menu)

menubar.add_cascade(label = "Run", menu = run_menu)
run_menu.add_command(label = "Run", command = runcode)



codebox.config(yscrollcommand = scroll.set)
scroll.config(command = codebox.yview)

scroll.pack(side = RIGHT, fill = Y)

codebox.pack(side = LEFT, fill = Y)

codebox.bind("<Key>", key)



def eval(user_input):
    res = ""
    inp = user_input.replace(" ", "")
    incr = 1
    raw_code = list(inp)
    
    get_cells = 1
    
    for codelen in range (len(raw_code)):
        current = raw_code[codelen]
        if (current != "+"
             and current != "-"
              and current != "<" 
               and current != ">"
                and current != "."
                 and current != "-"
                  and current != "["
                   and current != "]"
                    and current != ","):
            current = ""
        
        if (current == ">"):
            get_cells += 1
    
    cells = [0 for cell_getter in range(get_cells)]
    
    cc = 0
    
    for x in range (len(raw_code)):
        cread = raw_code[x]
        if (cread == "+"):
            cells[cc] += 1
            
        elif (cread == "-"):
            cells[cc] -= 1
            
        elif (cread == ">"):
            cc += 1
            
        elif (cread == "["):
            found_end = False
            end = 0
            incr = 1
            while not found_end:
                if(raw_code[x + incr] != "]"):
                    end += 1
                    incr += 1
                else:
                    found_end = True
                    
            for left in range(cells[cc] - 1):
                for l in range(end + 1):
                    if (raw_code[x + l] == "+"):
                        cells[cc] += 1
                        
                    elif (raw_code[x + l] == "-"):
                        cells[cc] -= 1
                        
                    elif (raw_code[x + l] == ">"):
                        cc += 1
                        
                    elif (raw_code[x + l] == "<"):
                        cc -= 1
                        
                    elif (raw_code[x + l] == "."):
                        res = res + unichr(cells[cc])
                    
        elif (cread == "<"):
            cc -= 1
            
        elif (cread == "."):
            res = res + unichr(cells[cc])
            
    return res
        
t.mainloop()


        