"""A demo script to showcase the Sun Valley ttk theme."""

import tkinter
from tkinter import ttk
from configs import config
from addod import addwindow
from tkcalendar import DateEntry
import threading

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tkinter.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
class Table:
    def __init__(self, tab,lst,n,m):
        for i in range(n):
            for j in range(m):
                self.e = ttk.Entry(tab, width=20,font=('Arial', 16, 'bold'))
                self.e.grid(row=i+1, column=j)
                self.e.insert('end', lst[i][j])
                self.e.config(state='disabled')

def approval(id,i,window,notebook,curr_user,tbl):
    def approv():
        con=config()
        cur=con.cursor()
        if i==-1:
            cur.execute(f"update {tbl} set status=-1,rejected_by={curr_user.role} where id={id}")
        else:
            cur.execute(f"update {tbl} set status=status+{i} where id={id}")
        con.commit()
        window.destroy()
        notebook.refresh_data(curr_user,con)
        print("approved")
    threading.Thread(target=approv).start()

def delete(id,tbl,window,notebook,curr_user):
    def delete1():
        con=config()
        cur=con.cursor()
        cur.execute(f"Delete from {tbl} where id={id}")
        con.commit()
        window.destroy()
        notebook.refresh_data(curr_user, con)
        print("Canceled")
    threading.Thread(target=delete1).start()

def show_record_info(tree,root,curr_user,notebook,tbl):
    selected_item = tree.focus()
    print(1)
    if selected_item:
        record = tree.item(selected_item)
        info_window = tkinter.Toplevel(root)
        info_window.title("Record Information")
        info_frame = ttk.Frame(info_window, padding=20)
        info_frame.pack(fill=tkinter.BOTH, expand=True)
        rn,dept,sec,name1=record['text'].split(' - ')

        name = ttk.Label(info_frame, text="Name:", style="email.TLabel")
        name.grid(row=0, column=0, sticky='nw')
        name_value = ttk.Label(info_frame, text=name1, style="email.TLabel")
        name_value.grid(row=0, column=1, sticky='w')

        rollno = ttk.Label(info_frame, text="College ID:", style="email.TLabel")
        rollno.grid(row=1, column=0, sticky='nw')
        rollno_values = ttk.Label(info_frame, text=rn, style="email.TLabel")
        rollno_values.grid(row=1, column=1, sticky='w')

        department = ttk.Label(info_frame, text="Department:", style="email.TLabel")
        department.grid(row=2, column=0, sticky='nw')
        department_value = ttk.Label(info_frame, text=dept, wraplength=400, style="email.TLabel")
        department_value.grid(row=2, column=1, sticky='w')

        section = ttk.Label(info_frame, text="Section:", style="email.TLabel")
        section.grid(row=3, column=0, sticky='nw')
        section_value = ttk.Label(info_frame, text=sec, wraplength=400, style="email.TLabel")
        section_value.grid(row=3, column=1, sticky='w')

        created = ttk.Label(info_frame, text="Created on:", style="email.TLabel")
        created.grid(row=4, column=0, sticky='nw')
        created_value = ttk.Label(info_frame, text=record['values'][3], wraplength=400, style="email.TLabel")
        created_value.grid(row=4, column=1, sticky='w')

        from_date = ttk.Label(info_frame, text="From :", style="email.TLabel")
        from_date.grid(row=5, column=0, sticky='nw')
        from_date_value = ttk.Label(info_frame, text=record['values'][1], wraplength=400, style="email.TLabel")
        from_date_value.grid(row=5, column=1, sticky='w')

        to_date = ttk.Label(info_frame, text="To :", style="email.TLabel")
        to_date.grid(row=6, column=0, sticky='nw')
        to_date_value = ttk.Label(info_frame, text=record['values'][2], wraplength=400, style="email.TLabel")
        to_date_value.grid(row=6, column=1, sticky='w')

        email = ttk.Label(info_frame, text="Event :", style="email.TLabel")
        email.grid(row=7, column=0, sticky='nw')
        email_value = ttk.Label(info_frame, text=record['values'][0], wraplength=400, style="email.TLabel")
        email_value.grid(row=7, column=1, sticky='w')

        desc = ttk.Label(info_frame, text="Description :", style="email.TLabel")
        desc.grid(row=8, column=0, sticky='nw')
        desc_value = ttk.Label(info_frame, text=record['values'][5], wraplength=400, style="email.TLabel")
        desc_value.grid(row=8, column=1, sticky='w')
        role={1:"Incharge",2:"Counselor",3:"HoD"}
        stats=""
        if(record['values'][6]==-1):
            stats="Rejected by "+role[record['values'][7]]
        else:
            for i in (1,2,3):
                if(record['values'][6]<i):
                    stats=stats+role[i]+" : "+"Waiting for approval\n"
                else:
                    stats=stats+role[i]+" : "+"Approved\n"
        status = ttk.Label(info_frame, text="Status :", style="email.TLabel")
        status.grid(row=9, column=0, sticky='nw')
        status_value = ttk.Label(info_frame, text=stats, wraplength=400, style="email.TLabel")
        status_value.grid(row=9, column=1, sticky='w')
        if (record['values'][6] == 0 and curr_user.role==1) or (record['values'][6] == 1 and curr_user.role==2) or (record['values'][6] == 2 and curr_user.role==3):
            reject = ttk.Button(info_window, text="Reject",style="Accent.TButton", command=lambda: approval(selected_item,-1,info_window,notebook,curr_user,tbl))
            reject.pack()
            approve = ttk.Button(info_window, text="Approve",style="Accent.TButton", command=lambda: approval(selected_item,1,info_window,notebook,curr_user,tbl))
            approve.pack()
        if(record['values'][6]>=0 and record['values'][6]<=2 and curr_user.role==-1):
            cancel = ttk.Button(info_window, text="Cancel", style="Accent.TButton",command=lambda: delete(selected_item,tbl,info_window,notebook,curr_user))
            cancel.pack()
        print(5)

class PanedDemo(ttk.PanedWindow):
    def __init__(self, parent,root,curr_user,con):
        super().__init__(parent)


        self.var = tkinter.IntVar(self, 47)

        self.add_widgets(root,curr_user,parent,con)

    def settabs(self,root,curr_user,tab,tbl,sbar,tree):
        sbar.pack(side="right", fill="y")

        sbar.config(command=tree.yview)

        tree.pack(fill="both", expand=True)
        tree.column("#0", anchor='w', width=200, stretch='no')
        tree.column("1", anchor='n')
        tree.column("2", anchor='w', width=100, stretch='no')
        tree.column("3", anchor='w', width=100, stretch='no')
        tree.column("4", anchor='w', width=100, stretch='no')
        tree.column("5", anchor='w', width=120, stretch='no')
        tree.heading("#0", text="Student")
        tree.heading(1, text="Event")
        tree.heading(2, text="From")
        tree.heading(3, text="To")
        tree.heading(4, text="Created on")
        tree.heading(5, text="Status")
        tree.bind("<Double-1>", lambda event: show_record_info(tree, root, curr_user, self,tbl))
        if curr_user.role == -1:
            self.addbutton = ttk.Button(tab, text="Create", style="Accent.TButton",command=lambda: addwindow(root, curr_user, self,tbl))
            self.addbutton.pack()
    def settable(self,sframe,date,tbl,curr_user):
        con=config()
        cur=con.cursor()
        if(curr_user.role==1):
            cur.execute(f"select {tbl}.user_id,users.username,dept.name||'-'||class.sec,subject from {tbl} join students s on {tbl}.user_id=s.user_id join class on class.id=s.class_id join dept on dept.id=class.dept_id join users on users.id={tbl}.user_id where '{date}'>= from_date AND '{date}' <= to_date AND class.incharge_id={curr_user.id} AND status=3")
        elif(curr_user.role == 2):
            cur.execute(
                f"select {tbl}.user_id,users.username,dept.name||'-'||class.sec,subject from {tbl} join students s on {tbl}.user_id=s.user_id join class on class.id=s.class_id join dept on dept.id=class.dept_id join users on users.id={tbl}.user_id where '{date}'>= from_date AND '{date}' <= to_date AND class.counselor_id={curr_user.id} AND status=3")
        elif(curr_user.role == 3):
            cur.execute(
                f"select {tbl}.user_id,users.username,dept.name||'-'||class.sec,subject from {tbl} join students s on {tbl}.user_id=s.user_id join class on class.id=s.class_id join dept on dept.id=class.dept_id join users on users.id={tbl}.user_id where '{date}'>= from_date AND '{date}' <= to_date AND dept.hod_id={curr_user.id} AND status=3")
        data=cur.fetchall()
        for widgets in sframe.winfo_children()[3:]:
            widgets.destroy()
        print(data)
        if(data):
            Table(sframe.scrollable_frame,data,len(data),len(data[0]))
        count=ttk.Label(sframe.scrollable_frame,text=f"The Total number of students : {len(data)}")
        count.grid(row=len(data)+1,column=0)
        sframe.grid(row=1,column=0,columnspan=2,sticky="nsew")
        con.close()
        
    def add_widgets(self,root,curr_user,parent,con):
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")
        self.tab_1=ttk.Frame(self.notebook)
        self.notebook.add(self.tab_1,text="OD")
        self.tab_2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_2, text="LEAVE")
        if(curr_user.role>0):
            self.tab_3 = tkinter.Frame(self.notebook)
            self.notebook.add(self.tab_3, text="OD STATS")
            self.tab_4 = ttk.Frame(self.notebook)
            self.notebook.add(self.tab_4, text="LEAVE STATS")
            self.od_date=DateEntry(self.tab_3)
            self.od_date.grid(row=0, column=0, sticky="w", padx=5, pady=(0, 10))
            self.od_date_button = ttk.Button(self.tab_3, text="Search", style="Accent.TButton",command=lambda: self.settable(ScrollableFrame(self.tab_3),self.od_date.get(),'od',curr_user))
            self.od_date_button.grid(row=0,column=1, sticky="w", padx=5, pady=(0, 10))
            self.tab_3.columnconfigure(1, weight=1)
            self.tab_3.rowconfigure(1, weight=1)
            self.tab_4.columnconfigure(1, weight=1)
            self.tab_4.rowconfigure(1, weight=1)
            self.leave_date = DateEntry(self.tab_4)
            self.leave_date.grid(row=0, column=0, sticky="w", padx=5, pady=(0, 10))
            self.leave_date_button = ttk.Button(self.tab_4, text="Search", style="Accent.TButton",command=lambda: self.settable(ScrollableFrame(self.tab_4),self.leave_date.get(),'leave',curr_user))
            self.leave_date_button.grid(row=0,column=1, sticky="w", padx=5, pady=(0, 10))

        self.scrollbar = ttk.Scrollbar(self.tab_1)
        self.tree = ttk.Treeview(
            self.tab_1,
            columns=(1, 2, 3, 4, 5),
            height=11,
            selectmode="browse",
            yscrollcommand=self.scrollbar.set,
        )
        self.scrollbar1 = ttk.Scrollbar(self.tab_2)
        self.tree1 = ttk.Treeview(
            self.tab_2,
            columns=(1, 2, 3, 4, 5),
            height=11,
            selectmode="browse",
            yscrollcommand=self.scrollbar.set
        )
        self.settabs(root, curr_user,self.tab_1, 'OD',self.scrollbar,self.tree)
        self.settabs(root, curr_user,self.tab_2, 'LEAVE',self.scrollbar1,self.tree1)
        self.refreshButton = ttk.Button(root, text="Refresh",style="Accent.TButton", command=lambda :self.refresh_data(curr_user,config()))
        self.refreshButton.pack()
        self.refresh_data(curr_user,con)

    def refresh_data(self, curr_user, con):
        print("refresh clicked")
        cur = con.cursor()
        user_id=curr_user.id
        # Combined query for both 'od' and 'leave'
        queries = {
            -1: f"""
                SELECT 'od' AS type, od.id, od.user_id||' - '||d.name||' - '||class.sec||' - '||u.username, subject,
                       TO_CHAR(from_date,'YYYY-MM-DD'), TO_CHAR(to_date,'YYYY-MM-DD'), 
                       TO_CHAR(created_date,'YYYY-MM-DD'), 
                       CASE WHEN status=-1 THEN 'Rejected' 
                            WHEN status=3 THEN 'Approved' 
                            ELSE 'Pending' 
                       END, description, status,rejected_by
                FROM od 
                JOIN students on od.user_id = students.user_id 
                JOIN class ON class.id = students.class_id 
                JOIN dept d ON class.dept_id = d.id 
                JOIN users u ON od.user_id=u.id
                WHERE od.user_id = {user_id}

                UNION ALL

                SELECT 'leave' AS type, leave.id, leave.user_id||' - '||d.name||' - '||class.sec||' - '||u.username, subject,
                       TO_CHAR(from_date,'YYYY-MM-DD'), TO_CHAR(to_date,'YYYY-MM-DD'), 
                       TO_CHAR(created_date,'YYYY-MM-DD'), 
                       CASE WHEN status=-1 THEN 'Rejected' 
                            WHEN status=3 THEN 'Approved' 
                            ELSE 'Pending' 
                       END, description, status,rejected_by
                FROM leave 
                JOIN students on leave.user_id = students.user_id 
                JOIN class ON class.id = students.class_id 
                JOIN dept d ON class.dept_id = d.id 
                JOIN users u ON leave.user_id=u.id
                WHERE leave.user_id = {user_id}
            """,
            1:f"""
                SELECT 'od' AS type, od.id, od.user_id||' - '||d.name||' - '||class.sec||' - '||u.username, subject,
                       TO_CHAR(from_date,'YYYY-MM-DD'), TO_CHAR(to_date,'YYYY-MM-DD'), 
                       TO_CHAR(created_date,'YYYY-MM-DD'), 
                       CASE WHEN status=-1 THEN 'Rejected' 
                            WHEN status=3 THEN 'Approved' 
                            WHEN status=0 THEN 'Requested' 
                            ELSE 'Approved by Me' 
                       END, description, status,rejected_by
                FROM od 
                JOIN students on od.user_id = students.user_id 
                JOIN class ON class.id = students.class_id 
                JOIN dept d ON d.id = class.dept_id 
                JOIN users u ON od.user_id=u.id
                WHERE class.incharge_id = {user_id} AND (status>=0 OR rejected_by >= 1)

                UNION ALL

                SELECT 'leave' AS type, leave.id, leave.user_id||' - '||d.name||' - '||class.sec||' - '||u.username, subject,
                       TO_CHAR(from_date,'YYYY-MM-DD'), TO_CHAR(to_date,'YYYY-MM-DD'), 
                       TO_CHAR(created_date,'YYYY-MM-DD'), 
                       CASE WHEN status=-1 THEN 'Rejected' 
                            WHEN status=3 THEN 'Approved' 
                            WHEN status=0 THEN 'Requested' 
                            ELSE 'Approved by Me' 
                       END, description, status,rejected_by
                FROM leave 
                JOIN students on leave.user_id = students.user_id 
                JOIN class ON class.id = students.class_id 
                JOIN dept d ON d.id = class.dept_id 
                JOIN users u ON leave.user_id=u.id
                WHERE class.incharge_id = {user_id} AND (status>=0 OR rejected_by >= 1)
            """,
            2: f"""
                SELECT 'od' AS type, od.id, od.user_id||' - '||d.name||' - '||class.sec||' - '||u.username, subject,
                       TO_CHAR(from_date,'YYYY-MM-DD'), TO_CHAR(to_date,'YYYY-MM-DD'), 
                       TO_CHAR(created_date,'YYYY-MM-DD'), 
                       CASE WHEN status=-1 THEN 'Rejected' 
                            WHEN status=3 THEN 'Approved' 
                            WHEN status=1 THEN 'Requested' 
                            ELSE 'Approved by Me' 
                       END, description, status,rejected_by
                FROM od 
                JOIN students on od.user_id = students.user_id 
                JOIN class ON class.id = students.class_id 
                JOIN dept d ON d.id = class.dept_id 
                JOIN users u ON od.user_id=u.id
                WHERE class.counselor_id = {user_id} AND (status >= 1 OR rejected_by >= 2)

                UNION ALL

                SELECT 'leave' AS type, leave.id, leave.user_id||' - '||d.name||' - '||class.sec||' - '||u.username, subject,
                       TO_CHAR(from_date,'YYYY-MM-DD'), TO_CHAR(to_date,'YYYY-MM-DD'), 
                       TO_CHAR(created_date,'YYYY-MM-DD'), 
                       CASE WHEN status=-1 THEN 'Rejected' 
                            WHEN status=3 THEN 'Approved' 
                            WHEN status=1 THEN 'Requested' 
                            ELSE 'Approved by Me' 
                       END, description, status,rejected_by
                FROM leave 
                JOIN students on leave.user_id = students.user_id 
                JOIN class ON class.id = students.class_id 
                JOIN dept d ON d.id = class.dept_id 
                JOIN users u ON leave.user_id=u.id
                WHERE class.counselor_id = {user_id} AND (status >= 1 OR rejected_by >= 2)
            """,
            3: f"""
                SELECT 'od' AS type, od.id, od.user_id||' - '||d.name||' - '||class.sec||' - '||u.username, subject,
                       TO_CHAR(from_date,'YYYY-MM-DD'), TO_CHAR(to_date,'YYYY-MM-DD'), 
                       TO_CHAR(created_date,'YYYY-MM-DD'), 
                       CASE WHEN status=-1 THEN 'Rejected' 
                            WHEN status=3 THEN 'Approved' 
                            WHEN status=2 THEN 'Requested' 
                            ELSE 'Approved by Me' 
                       END, description, status,rejected_by
                FROM od 
                JOIN students on od.user_id = students.user_id 
                JOIN class ON class.id = students.class_id 
                JOIN dept d ON d.id = class.dept_id 
                JOIN users u ON od.user_id=u.id
                WHERE d.hod_id = {user_id} AND (status >= 2 OR rejected_by = 3)

                UNION ALL

                SELECT 'leave' AS type, leave.id, leave.user_id||' - '||d.name||' - '||class.sec||' - '||u.username, subject,
                       TO_CHAR(from_date,'YYYY-MM-DD'), TO_CHAR(to_date,'YYYY-MM-DD'), 
                       TO_CHAR(created_date,'YYYY-MM-DD'), 
                       CASE WHEN status=-1 THEN 'Rejected' 
                            WHEN status=3 THEN 'Approved' 
                            WHEN status=2 THEN 'Requested' 
                            ELSE 'Approved by Me' 
                       END, description, status,rejected_by
                FROM leave 
                JOIN students on leave.user_id = students.user_id 
                JOIN class ON class.id = students.class_id 
                JOIN dept d ON d.id = class.dept_id 
                JOIN users u ON leave.user_id=u.id
                WHERE d.hod_id = {user_id} AND (status >= 2 OR rejected_by = 3)
            """,
            0:f"SELECT NULL Where False"
        }

        cur.execute(queries[curr_user.role])
        data = cur.fetchall()
        con.close()

        print("Data fetched, updating trees")

        # Batch update for both tree views
        tree_data = {
            'od': [],
            'leave': []
        }
        for row in data:
            type, *values = row
            tree_data[type].append(("", values[0], values[1], values[2:10]))
        print(tree_data)
        if self.tree.get_children():
            self.tree.delete(*self.tree.get_children())
        for item in tree_data['od']:
            parnt, iid, text, values = item
            tag = self.get_tag(values[6], curr_user.role)
            self.tree.insert(parent=parnt, index="end", iid=iid, text=text, values=values, tags=[tag])

        if self.tree1.get_children():
            self.tree1.delete(*self.tree1.get_children())
        for item in tree_data['leave']:
            parnt, iid, text, values = item
            tag = self.get_tag(values[6], curr_user.role)
            self.tree1.insert(parent=parnt, index="end", iid=iid, text=text, values=values, tags=[tag])

        # Tag configuration
        self.configure_tags(self.tree)
        self.configure_tags(self.tree1)
        self.after(60000, self.refresh_data, curr_user,config())

    def get_tag(self, status, role):
        if status == (role - 1):
            return 'unapproved'
        elif status == 3:
            return 'approved'
        elif status == -1:
            return 'rejected'
        else:
            return ''

    def configure_tags(self, tree):
        tree.tag_configure('unapproved', background='#57C7FF', foreground='#000000')
        tree.tag_configure('approved', background='#1CD760', foreground='#000000')
        tree.tag_configure('rejected', background='#EA4938', foreground='#000000')


class App(ttk.Frame):
    def __init__(self, parent,curr_user,con):
        super().__init__(parent, padding=15)

        for index in range(2):
            self.columnconfigure(index, weight=1)
            self.rowconfigure(index, weight=1)

        PanedDemo(self,parent,curr_user,con).grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nsew")


def home(root,curr_user,con):
    root.title(curr_user.name)
    App(root,curr_user,con).pack(expand=True, fill="both")

