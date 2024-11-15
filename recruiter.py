from tkinter import *
from tkinter import ttk
from tkinter import messagebox, Label
from tkinter_uix.Entry import Entry
import mysql.connector as sql
import modules.login as l
from modules.creds import user_pwd
import os
import tempfile

def get_details(email):
    global name, company, gen, recid
    q = f'select RName,CompanyName,RGender,RID from mydb.recruiter where REmail="{email}"'
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(q)
    d = cur.fetchall()
    mycon.close()

    name = d[0][0]
    company = d[0][1]
    gen = d[0][2]
    recid = d[0][3]


def logi(root):
    try:
        bg.destroy()
    except:
        pass
    l.log(root)


def submit_job():
    global role1, jtype1, qual1, exp1, sal1
    role1 = role.get()
    jtype1 = jtype.get()
    qual1 = qual.get()
    exp1 = exp.get()
    sal1 = sal.get()
    print(role1, jtype1, qual1, exp1, sal1)
    if role1 and jtype1 and qual1 and exp1 and sal1:
        if jtype1 == "Select":
            messagebox.showinfo('ALERT!', 'Please provide Job Type')
        else:
            exe1 = f'INSERT INTO mydb.Job(RID, JID, JobRole, JobType, Qualification, MinExp, Salary) VALUES({recid}, NULL, "{role1}", "{jtype1}", "{qual1}", "{exp1}", {sal1})'
            try:
                mycon = sql.connect(host='localhost', user='root',
                                    passwd=user_pwd, database='mydb')
                cur = mycon.cursor()
                cur.execute(exe1)
                mycon.commit()
                mycon.close()
                role.delete(0, END)
                jtype.delete(0, END)
                qual.delete(0, END)
                exp.delete(0, END)
                sal.delete(0, END)
                messagebox.showinfo('SUCCESS!', 'You have successfully created a Job')
            except sql.Error as e:
                if "Duplicate job role posting is not allowed" in str(e):
                    messagebox.showerror('Error', 'Duplicate job role posting is not allowed')
                else:
                    messagebox.showerror('Error', f'An error occurred: {str(e)}')
    else:
        messagebox.showinfo('ALERT!', 'ALL FIELDS MUST BE FILLED')


# -------------------------------------------- Sort Queries --------------------------------------------------------
def sort_all(table):
    criteria = search_d.get()
    if(criteria == "Select"):
        pass
    else:
        table.delete(*table.get_children())
        mycon = sql.connect(host='localhost', user='root',
                            passwd=user_pwd, database='mydb')

        cur = mycon.cursor()
        cur.execute(
            f'select RID,JID, JobRole, JobType, Qualification, MinExp, Salary FROM mydb.Job where RID={recid} order by {criteria}')
        all_jobs = cur.fetchall()
        mycon.close()
    i = 0
    for r in all_jobs:
        table.insert('', i, text="", values=(
            r[1], r[2], r[3], r[4], r[5], r[6]))
        i += 1


def sort_applicants(table):
    criteria = search_d.get()
    if(criteria == "Select"):
        pass
    else:
        table.delete(*table.get_children())
        mycon = sql.connect(host='localhost', user='root',
                            passwd=user_pwd, database='mydb')

        cur = mycon.cursor()
        cur.execute(
            f'SELECT job.JobRole, client.CName, client.CEmail, client.CAge, client.CLocation, client.CGender, client.CExp, client.CSkills, client.CQualification, application.Status FROM application JOIN client ON application.cid=client.CID JOIN job ON job.jid=application.jid where job.rid={recid} order by {criteria}')
        applicats = cur.fetchall()
        mycon.close()
        print(applicats)
        i = 0
        for x in applicats:
            table.insert('', i, text="", values=(
                x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9]))
            i += 1

# ----------------------------------------------Posted jobs Query-----------------------------------------------


def show_all(table):
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(
        f'select RID,JID, JobRole, JobType, Qualification, MinExp, Salary FROM mydb.Job where RID={recid}')
    all_jobs = cur.fetchall()
    mycon.close()
    i = 0
    for r in all_jobs:
        table.insert('', i, text="", values=(
            r[1], r[2], r[3], r[4], r[5], r[6]))
        i += 1

# ----------------------------------------------Applicants-----------------------------------------------------


def show_applicants(table):
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(
        f'SELECT job.JobRole, client.CName, client.CEmail, client.CAge, client.CLocation, client.CGender, client.CExp, client.CSkills, client.CQualification, application.Status FROM application JOIN client ON application.cid=client.CID JOIN job ON job.jid=application.jid where job.rid={recid}')
    applicats = cur.fetchall()
    mycon.close()
    print(applicats)
    i = 0
    for x in applicats:
        table.insert('', i, text="", values=(
            x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9]))
        i += 1


# ---------------------------------------------Post a Job---------------------------------------------------
def create():
    global role, jtype, qual, exp, sal
    for widget in rt.winfo_children():
        widget.destroy()
    for widget in tab.winfo_children():
        widget.destroy()
    bgr.destroy()

    # Create Form
    f1 = Frame(rt, width=520)
    f1.load = PhotoImage(file="elements\\create.png")
    img = Label(rt, image=f1.load, bg="#FFFFFF")
    img.grid(row=0, column=1, padx=150, pady=10)

    # Form
    # Labels
    role_l = Label(tab, text="Role :", font=(
        'normal', 18, 'bold'), bg="#FFFFFF")
    role_l.grid(row=0, column=0, pady=10, padx=10)
    type_l = Label(tab, text="Type :", font=(
        'normal', 18, 'bold'), bg="#FFFFFF")
    type_l.grid(row=1, column=0, pady=10, padx=10)
    qual_l = Label(tab, text="Qualification :", font=(
        'normal', 18, 'bold'), bg="#FFFFFF")
    qual_l.grid(row=2, column=0, pady=10, padx=10)
    exp_l = Label(tab, text="Experience :", font=(
        'normal', 18, 'bold'), bg="#FFFFFF")
    exp_l.grid(row=3, column=0, pady=10, padx=10)
    sal_l = Label(tab, text="Salary :", font=(
        'normal', 18, 'bold'), bg="#FFFFFF")
    sal_l.grid(row=4, column=0, pady=10, padx=10)

    # Entries
    style = ttk.Style(tab)
    style.configure("TCombobox", background="white",
                    foreground="#696969")

    role = Entry(tab, placeholder="Enter Job Role")
    role.grid(row=0, column=1, pady=10, padx=10)
    jtype = ttk.Combobox(tab, font=("normal", 18),
                         width=23, state='readonly')
    jtype['values'] = ('Select', 'FullTime', 'PartTime', 'Intern')
    jtype.current(0)
    jtype.grid(row=1, column=1, pady=10, padx=10)
    qual = Entry(tab, placeholder="Enter Job Qualifications")
    qual.grid(row=2, column=1, pady=10, padx=10)
    exp = Entry(tab, placeholder="Enter Minimum Experience")
    exp.grid(row=3, column=1, pady=10, padx=10)
    sal = Entry(tab, placeholder="Enter Expected salary")
    sal.grid(row=4, column=1, pady=10, padx=10)

    btn = Button(tab, text="Submit", font=(20), bg="#45CE30",
                 fg="#FFFFFF", command=submit_job)
    btn.grid(row=5, column=1, pady=15)

# -------------------------------------------------Delete A Posted Job----------------------------------------------------------


def deletjob(table):
    selectedindex = table.focus()
    selectedvalues = table.item(selectedindex, 'values')
    ajid = selectedvalues[0]
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    cur.execute(f'delete from mydb.application where jid={ajid}')
    cur.execute(f'delete from mydb.job where jid={ajid}')
    mycon.commit()
    mycon.close()
    messagebox.showinfo('Thanks', 'Your Job has been Deleted')
    posted()

# ----------------------------------------------Posted Jobs by Recruiter----------------------------------------------------


def posted():
    for widget in rt.winfo_children():
        widget.destroy()
    for widget in tab.winfo_children():
        widget.destroy()
    bgr.destroy()

    search_l = Label(rt, text="Order By : ", font=(
        'normal', 18), bg="#ffffff")
    search_l.grid(row=0, column=0, padx=10, pady=10)
    global search_d
    search_d = ttk.Combobox(rt, width=12, font=(
        'normal', 18), state='readonly')
    search_d['values'] = ('Select', 'JobRole', 'JobType')
    search_d.current(0)
    search_d.grid(row=0, column=2, padx=0, pady=10)
    search = Button(rt, text="Sort", font=('normal', 12, 'bold'),
                    bg="#00b9ed", fg="#ffffff", command=lambda: sort_all(table))
    search.grid(row=0, column=3, padx=10, pady=10, ipadx=15)
    dlt = Button(rt, text="Delete", font=('normal', 12, 'bold'),
                 bg="#00b9ed", fg="#ffffff", command=lambda: deletjob(table))
    dlt.grid(row=0, column=4, padx=10, pady=10, ipadx=5)

    scx = Scrollbar(tab, orient="horizontal")
    scy = Scrollbar(tab, orient="vertical")

    table = ttk.Treeview(tab, columns=('JID', 'JobRole', 'JobType', 'Qualification', 'MinExp', 'Salary'),
                         xscrollcommand=scx.set, yscrollcommand=scy.set)
    scx.pack(side="bottom", fill="x")
    scy.pack(side="right", fill="y")
    table.heading("JID", text="JobID")
    table.heading("JobRole", text="Role")
    table.heading("JobType", text='Type')
    table.heading("Qualification", text='Qualification')
    table.heading("MinExp", text='MinExp')
    table.heading("Salary", text="Salary")

    table['show'] = 'headings'

    scx.config(command=table.xview)
    scy.config(command=table.yview)

    table.column("JID", width=100)
    table.column("JobRole", width=150)
    table.column("JobType", width=150)
    table.column("Qualification", width=100)
    table.column("MinExp", width=100)
    table.column("Salary", width=150)
    show_all(table)
    table.pack(fill="both", expand=1)


# -----------------------------------------Applications on your recruiters posted jobs----------------------------------------------------------------
def app():
    for widget in rt.winfo_children():
        widget.destroy()
    for widget in tab.winfo_children():
        widget.destroy()
    bgr.destroy()

    view_resume_btn = Button(rt, text="View Resume", font=('normal', 12, 'bold'),
                             bg="#00b9ed", fg="#ffffff", command=lambda: view_resume(table))
    view_resume_btn.grid(row=0, column=0, padx=5, pady=10, ipadx=5, ipady=5)

    accept_btn = Button(rt, text="Accept", font=('normal', 12, 'bold'),
                        bg="#45CE30", fg="#ffffff", 
                        command=lambda: update_application_status(table, 'Accepted'))
    accept_btn.grid(row=0, column=1, padx=5, pady=10, ipadx=5, ipady=5)
    
    reject_btn = Button(rt, text="Reject", font=('normal', 12, 'bold'),
                        bg="#b32e2e", fg="#ffffff", 
                        command=lambda: update_application_status(table, 'Rejected'))
    reject_btn.grid(row=0, column=2, padx=5, pady=10, ipadx=5, ipady=5)

    scx = Scrollbar(tab, orient="horizontal")
    scy = Scrollbar(tab, orient="vertical")

    table = ttk.Treeview(tab, columns=('JobRole', 'CName', 'CEmail', 'CAge', 'CLocation', 'CGender', 'CExp', 'CSkills', 'CQualification', 'Status'),
                         xscrollcommand=scx.set, yscrollcommand=scy.set)
    scx.pack(side="bottom", fill="x")
    scy.pack(side="right", fill="y")

    table.heading("JobRole", text="Job Role")
    table.heading("CName", text='Applicants Name')
    table.heading("CEmail", text='Email')
    table.heading("CAge", text='Age')
    table.heading("CLocation", text='Location')
    table.heading("CGender", text='Gender')
    table.heading("CExp", text='Experience')
    table.heading("CSkills", text='Skills')
    table.heading("CQualification", text='Qualification')
    table.heading("Status", text='Status')

    table['show'] = 'headings'

    scx.config(command=table.xview)
    scy.config(command=table.yview)

    table.column("JobRole", width=150)
    table.column("CName", width=200)
    table.column("CEmail", width=100)
    table.column("CAge", width=50)
    table.column("CLocation", width=150)
    table.column("CGender", width=100)
    table.column("CExp", width=100)
    table.column("CSkills", width=200)
    table.column("CQualification", width=150)
    table.column("Status", width=100)
    show_applicants(table)
    table.pack(fill="both", expand=1)


# ---------------------------------------------------------------------------------------------------------------------------
def rec(root, email1):
    global email
    email = email1
    bg = Frame(root, width=1050, height=700)
    bg.place(x=0, y=0)

    get_details(email)

    bg.load = PhotoImage(file=f'elements\\bg{gen}.png')
    img = Label(root, image=bg.load)
    img.place(x=0, y=0)

    # Navbar
    nm = Label(root, text=f'{name}', font=(
        'normal', 36, 'bold'), bg="#ffffff", fg="#0A3D62")
    nm.place(x=300, y=50)
    cp = Label(root, text=f'{company}', font=(
        'normal', 24), bg="#ffffff", fg="#0A3D62")
    cp.place(x=300, y=120)
    bn = Button(root, text="LOGOUT", font=(
        'normal', 20), bg="#b32e2e", fg="#ffffff", command=lambda: logi(root))
    bn.place(x=800, y=75)

    # Add a button to view total applications beside the LOGOUT button
    ta = Button(root, text="Total Applications", font=(
        'normal', 11), bg="#b32e2e", fg="#ffffff", command=display_total_applications)
    ta.place(x=650, y=90)

    # Left
    lf = Frame(root, width=330, height=440, bg="#ffffff")
    lf.place(x=60, y=220)
    cj = Button(lf, text="Post a Job", font=(
        'normal', 20), bg="#b32e2e", fg="#ffffff", command=create)
    cj.grid(row=0, column=0, padx=80, pady=40)
    pj = Button(lf, text="Posted Jobs", font=(
        'normal', 20), bg="#b32e2e", fg="#ffffff", command=posted)
    pj.grid(row=1, column=0, padx=80, pady=40)
    ap = Button(lf, text="Applications", font=(
        'normal', 20), bg="#b32e2e", fg="#ffffff", command=app)
    ap.grid(row=2, column=0, padx=80, pady=40)

    # Right
    global rt, tab, bgr
    rt = Frame(root, width=540, height=420, bg="#ffffff")
    rt.place(x=450, y=220)
    tab = Frame(root, bg="#FFFFFF")
    tab.place(x=460, y=300, width=520, height=350)
    bgrf = Frame(root, width=540, height=420)
    bgrf.load = PhotoImage(file="elements\\bgr.png")
    bgr = Label(root, image=bgrf.load, bg="#00b9ed")
    bgr.place(x=440, y=210)

def view_resume(table):
    selectedindex = table.focus()
    if not selectedindex:
        messagebox.showinfo('Alert', 'Please select an applicant first')
        return
        
    selectedvalues = table.item(selectedindex, 'values')
    client_email = selectedvalues[2]  # Get client email from selected row
    
    try:
        mycon = sql.connect(host='localhost', user='root',
                          passwd=user_pwd, database='mydb')
        cur = mycon.cursor()
        cur.execute("""SELECT CResume, CResumeFileName 
                      FROM mydb.Client 
                      WHERE CEmail = %s""", (client_email,))
        result = cur.fetchone()
        mycon.close()
        
        if result and result[0]:
            resume_data, file_name = result
            # Create temporary file and open with default application
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, file_name)
            
            with open(temp_path, 'wb') as f:
                f.write(resume_data)
            
            os.startfile(temp_path)  # Windows
            # For Linux: subprocess.run(['xdg-open', temp_path])
            # For Mac: subprocess.run(['open', temp_path])
        else:
            messagebox.showinfo('Alert', 'No resume available for this applicant')
            
    except Exception as e:
        messagebox.showerror('Error', f'Failed to open resume: {str(e)}')

def update_application_status(table, status):
    selectedindex = table.focus()
    if not selectedindex:
        messagebox.showinfo('Alert', 'Please select an application first')
        return
        
    selectedvalues = table.item(selectedindex, 'values')
    job_role = selectedvalues[0]
    client_email = selectedvalues[2]
    
    try:
        mycon = sql.connect(host='localhost', user='root',
                          passwd=user_pwd, database='mydb')
        cur = mycon.cursor()
        # Update application status
        cur.execute("""UPDATE mydb.Application a 
                      JOIN mydb.Client c ON a.CID = c.CID
                      JOIN mydb.Job j ON a.JID = j.JID
                      SET a.Status = %s 
                      WHERE c.CEmail = %s AND j.JobRole = %s""", 
                   (status, client_email, job_role))
        mycon.commit()
        mycon.close()
        messagebox.showinfo('Success', f'Application {status.lower()}')
        app()  # Refresh the applications view
    except Exception as e:
        messagebox.showerror('Error', f'Failed to update application: {str(e)}')

def show_total_applications(table):
    # Connect to the database
    mycon = sql.connect(host='localhost', user='root',
                        passwd=user_pwd, database='mydb')
    cur = mycon.cursor()
    
    # Execute the query to get total applications per job role
    cur.execute("""
        SELECT 
            j.JobRole,
            COUNT(a.AID) AS TotalApplications
        FROM 
            mydb.Application a
        JOIN 
            mydb.Job j ON a.JID = j.JID
        GROUP BY 
            j.JobRole;
    """)
    
    # Fetch the results
    total_applications = cur.fetchall()
    mycon.close()
    
    # Debugging: Print the fetched results
    print("Total Applications Fetched:", total_applications)
    
    # Clear the table before inserting new data
    table.delete(*table.get_children())
    
    # Insert the results into the table
    for i, (job_role, total) in enumerate(total_applications):
        table.insert('', i, text="", values=(job_role, total))

def display_total_applications():
    for widget in rt.winfo_children():
        widget.destroy()
    for widget in tab.winfo_children():
        widget.destroy()
    bgr.destroy()

    # Create a button to fetch and display total applications
    fetch_btn = Button(rt, text="Fetch Total Applications", font=('normal', 12, 'bold'),
                       bg="#00b9ed", fg="#ffffff", command=lambda: show_total_applications(table))
    fetch_btn.grid(row=0, column=0, padx=5, pady=10, ipadx=5, ipady=5)

    # Create a table to display the results
    scx = Scrollbar(tab, orient="horizontal")
    scy = Scrollbar(tab, orient="vertical")

    table = ttk.Treeview(tab, columns=('JobRole', 'TotalApplications'),
                         xscrollcommand=scx.set, yscrollcommand=scy.set)
    scx.pack(side="bottom", fill="x")
    scy.pack(side="right", fill="y")

    table.heading("JobRole", text="Job Role")
    table.heading("TotalApplications", text='Total Applications')

    table['show'] = 'headings'

    scx.config(command=table.xview)
    scy.config(command=table.yview)

    table.column("JobRole", width=150)
    table.column("TotalApplications", width=150)
    table.pack(fill="both", expand=1)
