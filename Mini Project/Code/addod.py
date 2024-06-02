import tkinter
from tkinter import ttk
from tkcalendar import DateEntry
from configs import config
import threading

class OdAdd(ttk.Frame):
    def __init__(self, parent,curr_user,info,notebook,tbl):
        super().__init__(parent, style="Card.TFrame", padding=15)

        self.columnconfigure(0, weight=1)

        self.add_widgets(parent,curr_user,info,notebook,tbl)

    def add_od_leave(self,todate,fromdate,subject,desc,curr_user,info,notebook,tbl):
        def add_odleave():
            info.destroy()
            print(subject)
            t = todate.split('/')
            f = fromdate.split('/')
            to_date = '20' + t[2] + '-' + t[0] + '-' + t[1]
            from_date = '20' + f[2] + '-' + f[0] + '-' + f[1]
            con = config()
            cur = con.cursor()
            cur.execute(
                f"insert into {tbl} values(default,{curr_user.id},default,'{from_date}','{to_date}','{subject}','{desc}',default,null);")
            con.commit()
            notebook.refresh_data(curr_user, con)
        threading.Thread(target=add_odleave).start()

    def add_widgets(self,parent,curr_user,info,notebook,tbl):

        self.fromdate = ttk.Label(self, text="From:")
        self.fromdate.grid(row=0, column=0, sticky="ew", padx=5, pady=(0, 10))

        self.from_entry=DateEntry(self,width=50)
        self.from_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=(0, 10))

        self.to = ttk.Label(self, text="To:")
        self.to.grid(row=1, column=0, sticky="ew",  padx=5, pady=(0, 10))

        self.subject_label = ttk.Label(self, text="Subject:")
        self.subject_label.grid(row=2, column=0, sticky="ew",  padx=5, pady=(0, 10))

        # Entry widgets
        self.to_entry = DateEntry(self,width=50)
        self.to_entry.grid(row=1, column=1, padx=5, pady=(0, 10), sticky="ew")

        self.subject_entry = ttk.Entry(self, width=50)
        self.subject_entry.grid(row=2, column=1, padx=5, pady=(0, 10), sticky="ew")

        self.body_text = tkinter.Text(self, width=80, height=20,highlightbackground="#8A8A8A",highlightcolor='#56C8FF',highlightthickness=1)
        self.body_text.grid(row=3, column=0,columnspan=2, padx=5, pady=(0, 10),sticky="ew")

        self.separator = ttk.Separator(self)
        self.separator.grid(row=5, column=0,columnspan=2, pady=10, sticky="ew")

        self.send_button = ttk.Button(self, text="Send",style="Accent.TButton",command=lambda :self.add_od_leave(self.to_entry.get(),self.from_entry.get(),self.subject_entry.get(),self.body_text.get("1.0", "end-1c"),curr_user,info,notebook,tbl))
        self.send_button.grid(row=7, column=0,columnspan=2, padx=5, pady=10, sticky="ew")



class App(ttk.Frame):
    def __init__(self, parent,curr_user,notebook,tbl):
        super().__init__(parent, padding=15)
        label = ttk.Label(self, text="")
        label.grid(row=0, column=0)
        big_font_label = ttk.Label( self,text=f"APPLY {tbl}", font=("Arial", 30, "bold"), foreground="#56C8FF")
        big_font_label.grid(row=1,column=1)
        OdAdd(self,curr_user,parent,notebook,tbl).grid(
            row=2, column=1, padx=10, pady=(10, 0), sticky="nsew",
        )
        label = ttk.Label(self, text="")
        label.grid(row=3, column=2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=0,minsize=200)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0,minsize=400)
        self.grid_columnconfigure(2, weight=1)


def addwindow(root,curr_user,notebook,tbl):
    info = tkinter.Toplevel(root)
    info.title(f"Create {tbl}")
    App(info,curr_user,notebook,tbl).pack(expand=True, fill="both")
