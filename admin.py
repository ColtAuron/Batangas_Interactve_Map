import customtkinter
import tkinter
import sqlite3
import os
from PIL import ImageTk,Image
from CTkTable import *
from CTkMessagebox import CTkMessagebox
from coltinputdialog import ColtInputDialog
import re
from tkintermapview import TkinterMapView

class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(self.BASE_DIR, "Batangas_IM.db")
        self.con = sqlite3.connect(self.db_path)
        self.c = self.con.cursor()

        self.app_Width = 1500
        self.app_Height = 900
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.CenterX = int((self.screen_width-self.app_Width)/2) #-200
        self.CenterY = int((self.screen_height-self.app_Height)/2) #-200

        self.regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

        self.title("BIM Admin")
        self.geometry(f'{self.app_Width}x{self.app_Height}+{self.CenterX}+{self.CenterY}')
        self.minsize(width=self.app_Width, height=self.app_Height)
        self.maxsize(width=self.screen_width, height=self.screen_height)

        self.current_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        self.img1= customtkinter.CTkImage(light_image=Image.open(os.path.join(self.current_path, 'images', 'map.png')), size=(1920,1080))
        self.bg=customtkinter.CTkLabel(master=self,image=self.img1, text="")
        self.bg.pack()

        self.mainframe=customtkinter.CTkFrame(master=self.bg, width=1400, height=800, corner_radius=18)
        self.mainframe.place(relx=0.5, rely=.5, anchor=tkinter.CENTER)

        self.sidebar=customtkinter.CTkFrame(master=self.mainframe, width=270, height=800, border_color="grey")
        self.sidebar.place(relx=0, rely=.5, anchor=tkinter.W)
        
        self.font1= ('Arial',25,'bold')
        self.font2= ('Arial',18)
        self.fontnumber=('Arial',75)

        #--------- Side bar ----------

        self.APlabel=customtkinter.CTkLabel(master=self.sidebar, font=self.font1, text='Admin Panel', text_color='#fff')
        self.APlabel.place(relx=0.5, rely=.045, anchor=tkinter.N)

        self.overview=customtkinter.CTkButton(self.sidebar, font=self.font2, text='Dashboard', fg_color="transparent", hover_color="#808080", corner_radius=0, width=270, height=50, command=self.showoverview)
        self.overview.place(relx=0.5, rely=0.17, anchor=tkinter.CENTER)
        self.users=customtkinter.CTkButton(self.sidebar, font=self.font2, text='Cities', fg_color="transparent", hover_color="#808080", corner_radius=0, width=270, height=50, command=self.showusers)
        self.users.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)
        self.requests=customtkinter.CTkButton(self.sidebar, font=self.font2, text='Animals', fg_color="transparent", hover_color="#808080", corner_radius=0, width=270, height=50, command=self.showrequests)
        self.requests.place(relx=0.5, rely=0.33, anchor=tkinter.CENTER)
        self.routes=customtkinter.CTkButton(self.sidebar, font=self.font2, text='Plants', fg_color="transparent", hover_color="#808080", corner_radius=0, width=270, height=50, command=self.showroutes)
        self.routes.place(relx=0.5, rely=0.41, anchor=tkinter.CENTER)
        self.todas=customtkinter.CTkButton(self.sidebar, font=self.font2, text='Tourists', fg_color="transparent", hover_color="#808080", corner_radius=0, width=270, height=50, command=self.showtodas)
        self.todas.place(relx=0.5, rely=0.49, anchor=tkinter.CENTER)
        self.bus=customtkinter.CTkButton(self.sidebar, font=self.font2, text='Suggestions', fg_color="transparent", hover_color="#808080", corner_radius=0, width=270, height=50, command=self.showbus)
        self.bus.place(relx=0.5, rely=0.57, anchor=tkinter.CENTER)

        #--------- OV Frame ----------

        self.OVFrame=customtkinter.CTkFrame(master=self.mainframe, width=1000, height=700, corner_radius=20)

        self.OVlabel=customtkinter.CTkLabel(master=self.OVFrame, font=self.font1, text='Overview', text_color='#fff')
        self.OVlabel.place(relx=.04, rely=.04, anchor=tkinter.NW)

        self.OVUser=customtkinter.CTkFrame(master=self.OVFrame, width=200, height=250, corner_radius=20)
        self.OVUser.place(relx=0.33, rely=.30, anchor=tkinter.CENTER)
        self.OVUserlabel=customtkinter.CTkLabel(master=self.OVUser, font=self.font1, text='Cities', text_color='#fff')
        self.OVUserlabel.place(relx=.5, rely=.15, anchor=tkinter.N)
        self.OVUsernum=customtkinter.CTkLabel(master=self.OVUser, font=self.fontnumber, text='0', text_color='#fff')
        self.OVUsernum.place(relx=.5, rely=.65, anchor=tkinter.CENTER)

        self.OVRequest=customtkinter.CTkFrame(master=self.OVFrame, width=200, height=250, corner_radius=20)
        self.OVRequest.place(relx=0.66, rely=.30, anchor=tkinter.CENTER)
        self.OVRequestlabel=customtkinter.CTkLabel(master=self.OVRequest, font=self.font1, text='Animals', text_color='#fff')
        self.OVRequestlabel.place(relx=.5, rely=.15, anchor=tkinter.N)
        self.OVReqnum=customtkinter.CTkLabel(master=self.OVRequest, font=self.fontnumber, text='0', text_color='#fff')
        self.OVReqnum.place(relx=.5, rely=.65, anchor=tkinter.CENTER)

        self.OVjeep=customtkinter.CTkFrame(master=self.OVFrame, width=200, height=250, corner_radius=20)
        self.OVjeep.place(relx=0.20, rely=.75, anchor=tkinter.CENTER)
        self.OVjeeplabel=customtkinter.CTkLabel(master=self.OVjeep, font=self.font1, text='Plant', text_color='#fff')
        self.OVjeeplabel.place(relx=.5, rely=.15, anchor=tkinter.N)
        self.OVjeepnum=customtkinter.CTkLabel(master=self.OVjeep, font=self.fontnumber, text='0', text_color='#fff')
        self.OVjeepnum.place(relx=.5, rely=.65, anchor=tkinter.CENTER)

        self.OVtrike=customtkinter.CTkFrame(master=self.OVFrame, width=200, height=250, corner_radius=20)
        self.OVtrike.place(relx=0.50, rely=.75, anchor=tkinter.CENTER)
        self.OVtrikelabel=customtkinter.CTkLabel(master=self.OVtrike, font=self.font1, text='Tourist', text_color='#fff')
        self.OVtrikelabel.place(relx=.5, rely=.15, anchor=tkinter.N)
        self.OVtrikenum=customtkinter.CTkLabel(master=self.OVtrike, font=self.fontnumber, text='0', text_color='#fff')
        self.OVtrikenum.place(relx=.5, rely=.65, anchor=tkinter.CENTER)

        self.OVbus=customtkinter.CTkFrame(master=self.OVFrame, width=200, height=250, corner_radius=20)
        self.OVbus.place(relx=0.80, rely=.75, anchor=tkinter.CENTER)
        self.OVbuslabel=customtkinter.CTkLabel(master=self.OVbus, font=self.font1, text='Suggestions', text_color='#fff')
        self.OVbuslabel.place(relx=.5, rely=.15, anchor=tkinter.N)
        self.OVbusnum=customtkinter.CTkLabel(master=self.OVbus, font=self.fontnumber, text='0', text_color='#fff')
        self.OVbusnum.place(relx=.5, rely=.65, anchor=tkinter.CENTER)
        
        #--------- Users Frame ----------

        self.usersframe=customtkinter.CTkFrame(master=self.mainframe, width=1000, height=700, corner_radius=20)
        usersvalues = [['CityID', 'Name', 'District', 'Population', 'Width', 'Description', 'Image', 'Link']]
        self.userstitle=CTkTable(master=self.usersframe, width=95, height=10, values=usersvalues)
        self.userstitle.place(relx=.455, rely=.13, anchor=tkinter.CENTER)
        self.userscroll= customtkinter.CTkScrollableFrame(self.usersframe, width=810, height=500)
        self.userscroll.place(relx=.505, rely=.15, anchor=tkinter.N)
        self.userstable=CTkTable(master=self.userscroll, width=200, height=10, values=[[1,2,3,4,5]], command=self.usertableclick)

        #--------- Requests Frame ----------
        self.requestsframe=customtkinter.CTkFrame(master=self.mainframe, width=1000, height=700, corner_radius=20)
        requestsvalues = [['AnimalID', 'Name', 'SciName', 'Class','Description', 'Image', 'Link']]
        self.requeststitle=CTkTable(master=self.requestsframe, width=105, height=10, values=requestsvalues)
        self.requeststitle.place(relx=.090, rely=.13, anchor=tkinter.W)
        self.requestscroll= customtkinter.CTkScrollableFrame(self.requestsframe, width=810, height=500)
        self.requestscroll.place(relx=.505, rely=.15, anchor=tkinter.N)
        self.requesttable=CTkTable(master=self.requestscroll, width=200, height=10, values=[[1,2,3,4,5]], command=self.reqtableclick)

        #--------- Jeep Routes Frame ----------
        self.jeepframe=customtkinter.CTkFrame(master=self.mainframe, width=1000, height=700, corner_radius=20)
        Jeepvalues = [['PlantID', 'Name', 'SciName', 'Description', 'Image', 'Link']]
        self.jeeptitle= CTkTable(master=self.jeepframe, width=135, height=10, values=Jeepvalues)
        self.jeeptitle.place(relx=.500, rely=.13, anchor=tkinter.CENTER)
        self.jeepscroll= customtkinter.CTkScrollableFrame(self.jeepframe, width=810, height=500)
        self.jeepscroll.place(relx=.505, rely=.15, anchor=tkinter.N)
        self.jeeptable=CTkTable(master=self.jeepscroll, width=200, height=10, values=[[1,2,3,4]], command=self.routetableclick)

        #--------- Toda Pins Frame ----------
        self.todaframe=customtkinter.CTkFrame(master=self.mainframe, width=1000, height=700, corner_radius=20)
        Todavalues = [['TodaID', 'LocationName', 'Disabled']]
        self.todatitle= CTkTable(master=self.todaframe, width=160, height=10, values=Todavalues)
        self.todatitle.place(relx=.3375, rely=.13, anchor=tkinter.CENTER)
        self.todascroll= customtkinter.CTkScrollableFrame(self.todaframe, width=810, height=500)
        self.todascroll.place(relx=.505, rely=.15, anchor=tkinter.N)
        self.todatable=CTkTable(master=self.todascroll, width=200, height=10, values=[[1,2,3,4,5]], command=self.todatableclick)

        #--------- Bus Pins Frame ----------
        self.busframe=customtkinter.CTkFrame(master=self.mainframe, width=1000, height=700, corner_radius=20)
        Busvalues = [['TerminalID', 'LocationName', 'Disabled']]
        self.bustitle= CTkTable(master=self.busframe, width=160, height=10, values=Busvalues)
        self.bustitle.place(relx=.3375, rely=.13, anchor=tkinter.CENTER)
        self.busscroll= customtkinter.CTkScrollableFrame(self.busframe, width=810, height=500)
        self.busscroll.place(relx=.505, rely=.15, anchor=tkinter.N)
        self.bustable=CTkTable(master=self.busscroll, width=200, height=10, values=[[1,2,3,4,5]], command=self.bustableclick)

        self.overview.configure(state='disabled')
        self.users.configure(state='disabled')
        self.requests.configure(state='disabled')
        self.routes.configure(state='disabled')
        self.todas.configure(state='disabled')
        self.bus.configure(state='disabled')

        self.showoverview()
    
    #----------- OV ------------

    def showoverview(self):
        self.unshowall()
        self.OVFrame.place(relx=0.6, rely=.5, anchor=tkinter.CENTER)
        self.overview.configure(state='disabled', fg_color='#808080', text_color_disabled='#ffffff')
        self.c.execute("SELECT COUNT(*) FROM City")
        self.OVUsernum.configure(text=str(self.c.fetchall()[0][0]))
        self.c.execute("SELECT COUNT(*) FROM Animal")
        self.OVReqnum.configure(text=str(self.c.fetchall()[0][0]))
        self.c.execute("SELECT COUNT(*) FROM Plant")
        self.OVjeepnum.configure(text=str(self.c.fetchall()[0][0]))
        self.c.execute("SELECT COUNT(*) FROM Tourist")
        self.OVtrikenum.configure(text=str(self.c.fetchall()[0][0]))
        self.c.execute("SELECT COUNT(*) FROM Suggest")
        self.OVbusnum.configure(text=str(self.c.fetchall()[0][0]))

    def unshowoverview(self):
        self.OVFrame.place_forget()
        self.overview.configure(state='normal', fg_color='transparent',)

    #----------- users ------------

    def showusers(self):
        self.unshowall()
        self.usersframe.place(relx=0.6, rely=.5, anchor=tkinter.CENTER)
        self.users.configure(state='disabled', fg_color='#808080', text_color_disabled='#ffffff')
        self.refreshusers()

    def refreshusers(self):
        updated_table = list()
        self.c.execute("SELECT CityID, Name, District, Population, Width, Description, Image, Link FROM City")
        table = self.c.fetchall()
        for items in table:
            updated_table.append((items[0],items[1],items[2],items[3],items[4],'DESCRIPTION',items[6],'LINK','DELETE'))
        try:
            self.userstable=CTkTable(master=self.userscroll, width=150, height=10, values=updated_table, command=self.usertableclick) #self.usertableclick returns values rows, colm, args
            self.userstable.pack()
        except:
            pass

    def usertableclick(self, args): #stored in the first argument
        if args["value"] == 'DELETE': #calls the value with key "value"
            user = self.userstable.get_row(row=args["row"])[1] #"Grabs the column 2 which is the username"
            id = self.userstable.get_row(row=args["row"])[0] #Grabs the column 0 which is the ID
            msg = CTkMessagebox(title="Delete?", message=f"Delete city: {user} id: {id} ?", icon="question", option_1="No", option_3="Yes") #Asks for confirmation
            response = msg.get() #Waits and grabs information
            if response=="Yes": #Self explanatory DUUUHH
                self.c.execute("DELETE from CITY WHERE CityID=?", (id,)) #Delete query
                self.con.commit() #Commit and save changes
                CTkMessagebox(title="DELETED!", message="Successfully Deleted") #Alert User
        elif args["column"] == 0: #Checks if the column is equal to 0 meaning its an ID
            CTkMessagebox(title="Error", message="Altering IDs are not allowed", icon="cancel") #Alert User
        else:
            text = "Alter: " 
            title = "Change "
            id = self.userstable.get_row(row=args["row"])[0]
            typ = None
            if args["value"] == 'DESCRIPTION' or args["value"] == 'LINK':
                val = args["value"]
                self.c.execute("SELECT {} FROM City WHERE CityID = ?".format(val), (id,))
                tochange = self.c.fetchall()[0][0]
                typ = val
            else:
                tochange = args["value"]
            dialog = ColtInputDialog(text=text, title=title, placeholder_text=tochange) #Prompt user for change
            option = {
                1: "Name",
                2: "District",
                3: "Population",
                4: "Width",
                6: "Image"
            }
            if not typ:
                typ = option.get(args["column"])
            output = dialog.get_input() 
            if output and output != tochange:
                self.c.execute("UPDATE City Set {} = ? WHERE CityID = ?".format(typ), (output, id))
                self.con.commit()
        self.userstable.destroy() #Destroys current table
        self.refreshusers() #Creates and build from the database
    
    def unshowusers(self):
        self.userstable.destroy()
        self.usersframe.place_forget()
        self.users.configure(state='normal', fg_color='transparent',)

    #--------------- Requests -------------

    def showrequests(self):
        self.unshowall()
        self.requestsframe.place(relx=0.6, rely=.5, anchor=tkinter.CENTER)
        self.requests.configure(state='disabled', fg_color='#808080', text_color_disabled='#ffffff')
        self.refreshrequests()

    def unshowrequests(self):
        self.requesttable.destroy()
        self.requestsframe.place_forget()
        self.requests.configure(state='normal', fg_color='transparent',)
        pass

    def refreshrequests(self):
        updated_table = list()
        self.c.execute("SELECT AnimalID, Name, SciName, Class, Image FROM Animal")
        table = self.c.fetchall()
        for items in table:
            updated_table.append((items[0],items[1],items[2],items[3],'DESCRIPTION',items[4],'LINK', 'DELETE'))
        try:
            self.requesttable=CTkTable(master=self.requestscroll, width=150, height=10, values=updated_table, command=self.reqtableclick) #self.usertableclick returns values rows, colm, args
            self.requesttable.pack()
        except:
            pass
        pass

    def reqtableclick(self, args):
        if args["value"] == 'DELETE': #calls the value with key "value"
            user = self.requesttable.get_row(row=args["row"])[1] #"Grabs the column 2 which is the username"
            id = self.requesttable.get_row(row=args["row"])[0] #Grabs the column 0 which is the ID
            msg = CTkMessagebox(title="Delete?", message=f"Delete Animal: {user} id: {id} ?", icon="question", option_1="No", option_3="Yes") #Asks for confirmation
            response = msg.get() #Waits and grabs information
            if response=="Yes": #Self explanatory DUUUHH
                self.c.execute("DELETE from Animal WHERE AnimalID=?", (id,)) #Delete query
                self.con.commit() #Commit and save changes
                CTkMessagebox(title="DELETED!", message="Successfully Deleted") #Alert User
        elif args["column"] == 0: #Checks if the column is equal to 0 meaning its an ID
            CTkMessagebox(title="Error", message="Altering IDs are not allowed", icon="cancel") #Alert User
        else:
            text = "Alter: " 
            title = "Change "
            id = self.requesttable.get_row(row=args["row"])[0]
            typ = None
            if args["value"] == 'DESCRIPTION' or args["value"] == 'LINK':
                val = args["value"]
                self.c.execute("SELECT {} FROM Animal WHERE AnimalID = ?".format(val), (id,))
                tochange = self.c.fetchall()[0][0]
                typ = val
            else:
                tochange = args["value"]
            dialog = ColtInputDialog(text=text, title=title, placeholder_text=tochange) #Prompt user for change
            option = {
                1: "Name",
                2: "SciName",
                3: "Class",
                4: "Width",
                5: "Image"
            }
            if not typ:
                typ = option.get(args["column"])
            output = dialog.get_input() 
            if output and output != tochange:
                self.c.execute("UPDATE Animal Set {} = ? WHERE AnimalID = ?".format(typ), (output, id))
                self.con.commit()
        self.requesttable.destroy() #Destroys current table
        self.refreshrequests() #Creates and build from the database
        pass

    #--------------- Routes ---------------

    def showroutes(self):
        self.unshowall()
        self.jeepframe.place(relx=0.6, rely=.5, anchor=tkinter.CENTER)
        self.routes.configure(state='disabled', fg_color='#808080', text_color_disabled='#ffffff')
        self.refreshroutes()
        pass

    def unshowroutes(self):
        self.jeeptable.destroy()
        self.jeepframe.place_forget()
        self.routes.configure(state='normal', fg_color='transparent',)
        pass

    def routetableclick(self, args):
        if args["value"] == 'DELETE':  # calls the value with key "value"
            plant = self.jeeptable.get_row(row=args["row"])[1]  # "Grabs the column 2 which is the plant name"
            id = self.jeeptable.get_row(row=args["row"])[0]  # Grabs the column 0 which is the PlantID
            msg = CTkMessagebox(title="Delete?", message=f"Delete plant: {plant} id: {id} ?", icon="question",
                                option_1="No", option_3="Yes")  # Asks for confirmation
            response = msg.get()  # Waits and grabs information
            if response == "Yes":  # Self explanatory
                self.c.execute("DELETE from Plant WHERE PlantID=?", (id,))  # Delete query
                self.con.commit()  # Commit and save changes
                CTkMessagebox(title="DELETED!", message="Successfully Deleted")  # Alert User
        elif args["column"] == 0:  # Checks if the column is equal to 0 meaning it's the PlantID
            CTkMessagebox(title="Error", message="Altering Plant IDs is not allowed", icon="cancel")  # Alert User
        else:
            text = "Alter: "
            title = "Change "
            id = self.jeeptable.get_row(row=args["row"])[0]
            typ = None
            if args["value"] == 'Description' or args["value"] == 'Link':
                val = args["value"]
                self.c.execute("SELECT {} FROM Plant WHERE PlantID = ?".format(val), (id,))
                tochange = self.c.fetchall()[0][0]
                typ = val
            else:
                tochange = args["value"]
            dialog = ColtInputDialog(text=text, title=title, placeholder_text=tochange)  # Prompt user for change
            option = {
                1: "Name",
                2: "SciName",
                3: "Description",
                4: "Image",
                5: "Link"
            }
            if not typ:
                typ = option.get(args["column"])
            output = dialog.get_input()
            if output and output != tochange:
                self.c.execute("UPDATE Plant Set {} = ? WHERE PlantID = ?".format(typ), (output, id))
        self.jeeptable.destroy()  # Destroys current table
        self.refreshroutes()  # Rebuilds table from the database

    def refreshroutes(self):
        updated_table = list()
        self.c.execute("SELECT PlantID, Name, SciName, Image  FROM Plant")
        table = self.c.fetchall()
        for items in table:
            updated_table.append((items[0],items[1],items[2],items[3],'DESCRIPTION', 'LINK', 'DELETE'))
        try:
            self.jeeptable=CTkTable(master=self.jeepscroll, width=200, height=10, values=updated_table, command=self.routetableclick)
            self.jeeptable.pack()
        except:
            pass
        pass

    #--------------- Todas ----------------

    def showtodas(self):
        self.unshowall()
        self.todaframe.place(relx=0.6, rely=.5, anchor=tkinter.CENTER)
        self.todas.configure(state='disabled', fg_color='#808080', text_color_disabled='#ffffff')
        self.refreshtodas()
        pass

    def todatableclick(self, args):
        id = int(self.todatable.get_row(row=args["row"])[0])
        name = self.todatable.get_row(row=args["row"])[1]
        if args["value"] == "INSPECT":
            self.c.execute("SELECT Point_X, Point_Y FROM TODA WHERE TodaID=?", (id,))
            point = self.c.fetchall()
            InspectWindow = ColtInspect(point, name)
            InspectWindow.after(100, InspectWindow.lift)
            InspectWindow.wait_window()
        elif args["value"] == "DELETE":
            msg = CTkMessagebox(title="Delete?", message=f"Delete Point: {name},\nRNum = {id} ?", icon="question", option_1="No", option_3="Yes")
            response = msg.get()
            if response=="Yes":
                self.c.execute("DELETE from TODA WHERE TodaID=?", (id,)) 
                self.con.commit() 
                CTkMessagebox(title="DELETED!", message="Successfully Deleted")
        elif args["column"] == 0:
            CTkMessagebox(title="Error", message="Altering IDs are not allowed", icon="cancel")
        else:
            text = "Enter New Location Name"
            title = "Location Name Change"
            if args["column"] == 2:
                text = "Alter: 1 = True, 0 = False"
                title = "Give Administrator"
            tochange = args["value"]
            dialog = ColtInputDialog(text=text, title=title, placeholder_text=tochange) #Prompt user for change
            output = dialog.get_input()
            if output and output != tochange:
                if args["column"] == 1:
                    self.c.execute("SELECT * FROM TODA WHERE locName=?", (output,))
                    username_table = self.c.fetchall()
                    if username_table == []:
                        self.c.execute("UPDATE TODA SET locName = ? WHERE TodaID=?", (output, id)) #Change Query
                        self.con.commit()
                        CTkMessagebox(title="COMMITED!", message="Successfully Changed!")
                    else:
                        CTkMessagebox(title="Error", message="Location Name Already Taken", icon="cancel")
                else:
                    output = int(output)
                    if output == 1 or output == 0:
                        self.c.execute("UPDATE TODA SET Disabled = ? WHERE TodaID=?", (output, id)) #Change Query
                        self.con.commit()
                        CTkMessagebox(title="COMMITED!", message="Successfully Changed!")
                    else:
                        CTkMessagebox(title="Error", message="Please input 1 or 0", icon="cancel")
        self.todatable.destroy()
        self.refreshtodas()
        pass
    
    def unshowtodas(self):
        self.todatable.destroy()
        self.todaframe.place_forget()
        self.todas.configure(state='normal', fg_color='transparent',)
        pass

    def refreshtodas(self):
        updated_table = list()
        self.c.execute("SELECT * FROM TODA")
        table = self.c.fetchall()
        
        for items in table:
            updated_table.append((items[0],items[3],items[4],"INSPECT", "DELETE"))
        try:
            self.todatable=CTkTable(master=self.todascroll, width=200, height=10, values=updated_table, command=self.todatableclick)
            self.todatable.pack()
        except:
            pass
        pass

    #-------------- Bus -------------------

    def showbus(self):
        self.unshowall()
        self.busframe.place(relx=0.6, rely=.5, anchor=tkinter.CENTER)
        self.bus.configure(state='disabled', fg_color='#808080', text_color_disabled='#ffffff')
        self.refreshbus()
        pass

    def bustableclick(self, args):
        id = int(self.bustable.get_row(row=args["row"])[0])
        name = self.bustable.get_row(row=args["row"])[1]
        if args["value"] == "INSPECT":
            self.c.execute("SELECT Point_X, Point_Y FROM TERMINAL WHERE TemiID=?", (id,))
            point = self.c.fetchall()
            InspectWindow = ColtInspect(point, name)
            InspectWindow.after(100, InspectWindow.lift)
            InspectWindow.wait_window()
        elif args["value"] == "DELETE":
            msg = CTkMessagebox(title="Delete?", message=f"Delete Point: {name},\nRNum = {id} ?", icon="question", option_1="No", option_3="Yes")
            response = msg.get()
            if response=="Yes":
                self.c.execute("DELETE from TERMINAL WHERE TemiID=?", (id,)) 
                self.con.commit() 
                CTkMessagebox(title="DELETED!", message="Successfully Deleted")
        elif args["column"] == 0:
            CTkMessagebox(title="Error", message="Altering IDs are not allowed", icon="cancel")
        else:
            text = "Enter New Location Name"
            title = "Location Name Change"
            if args["column"] == 2:
                text = "Alter: 1 = True, 0 = False"
                title = "Give Administrator"
            tochange = args["value"]
            dialog = ColtInputDialog(text=text, title=title, placeholder_text=tochange) #Prompt user for change
            output = dialog.get_input()
            if output and output != tochange:
                if args["column"] == 1:
                    self.c.execute("SELECT * FROM TERMINAL WHERE locName=?", (output,))
                    username_table = self.c.fetchall()
                    if username_table == []:
                        self.c.execute("UPDATE TERMINAL SET locName = ? WHERE TemiID=?", (output, id)) #Change Query
                        self.con.commit()
                        CTkMessagebox(title="COMMITED!", message="Successfully Changed!")
                    else:
                        CTkMessagebox(title="Error", message="Location Name Already Taken", icon="cancel")
                else:
                    output = int(output)
                    if output == 1 or output == 0:
                        self.c.execute("UPDATE TERMINAL SET Disabled = ? WHERE TemiID=?", (output, id)) #Change Query
                        self.con.commit()
                        CTkMessagebox(title="COMMITED!", message="Successfully Changed!")
                    else:
                        CTkMessagebox(title="Error", message="Please input 1 or 0", icon="cancel")
        self.bustable.destroy()
        self.refreshbus()
        pass

    def unshowbus(self):
        self.bustable.destroy()
        self.busframe.place_forget()
        self.bus.configure(state='normal', fg_color='transparent',)
        pass

    def refreshbus(self):
        updated_table = list()
        self.c.execute("SELECT * FROM TERMINAL")
        table = self.c.fetchall()
        for items in table:
            updated_table.append((items[0],items[3],items[4],"INSPECT", "DELETE"))
        try:
            self.bustable=CTkTable(master=self.busscroll, width=200, height=10, values=updated_table, command=self.bustableclick)
            self.bustable.pack()
        except:
            pass
        pass

    #------------- Misc ------------------

    def unshowall(self):
        self.unshowoverview()
        self.unshowusers()
        self.unshowrequests()
        self.unshowroutes()
        self.unshowtodas()
        self.unshowbus()
        pass

class ColtInspect(customtkinter.CTkToplevel):
    def __init__(self, points, name, color = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.CenterX = int((self.screen_width-800)/2) #-200
        self.CenterY = int((self.screen_height-600)/2) #-200
        self.geometry(f"{800}x{600}+{self.CenterX}+{self.CenterY}")
        self.maxsize(width=800, height=600)
        self.minsize(width=800, height=600)
        self.grab_set()
        title = "Route"
        if len(points) == 1:
            title = "Point"
        self.title(f"{name} {title}")
        self.attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(self.BASE_DIR, "batangas.db")

        self.map_widget = TkinterMapView(self, width=800, height=600,database_path=self.db_path, use_database_only=False)
        self.map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.map_widget.set_position(deg_x=points[0][0],deg_y=points[0][1])

        if len(points) == 1:
            self.obj = self.map_widget.set_marker(deg_x=points[0][0], deg_y=points[0][1], text=name)
        else:
            self.obj = self.map_widget.set_path(position_list=points, color=color, width=3)

    def _on_closing(self):
        self.map_widget.delete(self.obj)
        self.grab_release
        self.destroy()
        
App().mainloop()
