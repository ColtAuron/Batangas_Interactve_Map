import sqlite3
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "bimData.db")
con = sqlite3.connect(db_path)
c = con.cursor()

command = ('''CREATE TABLE IF NOT EXISTS Animal(
            AnimalID INTEGER PRIMARY KEY,
            Name Varchar(30),
            sciName Varchar(50),
            desc Varchar(500),
            img Varchar(100)
            )''')

c.execute(command)

command = ('''CREATE TABLE IF NOT EXISTS Plant(
            PlantID INTEGER PRIMARY KEY,
            Name Varchar(30),
            sciName Varchar(50),
            desc Varchar(500),
            img Varchar(100)
            )''')

c.execute(command)

command = ('''CREATE TABLE IF NOT EXISTS Biome (
            BiomeID INTEGER PRIMARY KEY,
            Name Varchar(30),
            desc Varchar(500),
            img Varchar(100)
            )''')

c.execute(command)

command = ('''CREATE TABLE IF NOT EXISTS Tourist (
            TouristID INTEGER PRIMARY KEY,
            Name Varchar(30),
            link Varchar(50),
            desc Varchar(500),
            img Varchar(100)
            )''')

c.execute(command)

command = ('''CREATE TABLE IF NOT EXISTS City (
            CityID INTEGER PRIMARY KEY,
            Name Varchar(50)          
)''')

c.execute(command)

command = ('''CREATE TABLE IF NOT EXISTS AnimalsLoc (
            ID INTEGER PRIMARY KEY,
            AnimalID INTEGER,
            CityID INTEGER,
            xPos FLOAT(3, 7),
            yPos FLOAT(3, 7),
            Disabled TINYINT(1),
            FOREIGN KEY(AnimalID) REFERENCES Animal(AnimalID),
            FOREIGN KEY(CityID) REFERENCES City(CityID)
            )''')

c.execute(command)

command = ('''CREATE TABLE IF NOT EXISTS PlantsLoc (
            ID INTEGER PRIMARY KEY,
            PlantsID INTEGER,
            CityID INTEGER,
            xPos FLOAT(3, 7),
            yPos FLOAT(3, 7),
            Disabled TINYINT(1),
            FOREIGN KEY(PlantsID) REFERENCES Plant(ID),
            FOREIGN KEY(CityID) REFERENCES City(ID)
            )''')

c.execute(command)

command = ('''CREATE TABLE IF NOT EXISTS BiomeLoc (
            ID INTEGER PRIMARY KEY,
            BiomeID INTEGER,
            CityID INTEGER,
            xPos FLOAT(3, 7),
            yPos FLOAT(3, 7),
            Disabled TINYINT(1),
            FOREIGN KEY(BiomeID) REFERENCES Biome(ID),
            FOREIGN KEY(CityID) REFERENCES City(ID)
            )''')

c.execute(command)

command = ('''CREATE TABLE IF NOT EXISTS TouristLoc (
            ID INTEGER PRIMARY KEY,
            TouristID INTEGER,
            CityID INTEGER,
            xPos FLOAT(3, 7),
            yPos FLOAT(3, 7),
            Disabled TINYINT(1),
            FOREIGN KEY(TouristID) REFERENCES Tourist(ID),
            FOREIGN KEY(CityID) REFERENCES City(ID)
            )''')

c.execute(command)

# cities = [("Nasugbu",),("Lian",), ("Tuy",), ("Calatagan",), ("Balayan",), ("Calaca",), ("Lemery",),
#           ("Laurel",), ("Agoncillo",), ("Taal",), ("San Luis",), ("Bauan",), ("Mabini",), ("Tingloy",),
#           ("Sta. Teresita",), ("Talisay",), ("San Nicolas",), ("Alitagtag",), ("San Pascual",),
#           ("Cuenca",), ("San Jose",), ("Tanauan",), ("Malvar",), ("Balete",), ("Mataas na Kahoy",),
#           ("Lipa",), ("Ibaan",), ("Sto. Tomas",), ("Padre Garcia",), ("Rosario",), ("Taysan",),
#           ("Lobo",), ("San Juan",)]

# c.executemany("INSERT INTO CITY(Name) VALUES(?)", cities)

# c.execute("INSERT INTO Animal VALUES (1, 'Parrot', 'berb', 'a bird', 'picture.png')")

# c.execute("INSERT INTO AnimalsLoc Values (1, 1, 1, 13.7627346, 121.0569921, 0)")

#c.execute("INSERT INTO PLANT VALUES (1, 'Sunflower', 'araw', 'a flower', 'sunflower.png')")

# c.execute("INSERT INTO PlantsLoc VALUES (1, 1, 1, 13.7647354, 121.0602537, 0)")

#c.execute("INSERT INTO Tourist VALUES (1, 'Swimming pool', 'www.youtube.com', 'for swimming', 'pool.png')")

# c.execute("INSERT INTO TouristLoc VALUES (1, 1, 1, 13.7620260, 121.0685793, 0)")

#c.execute("INSERT INTO Biome VALUES (1, 'River', 'Waterflow', 'river.png')")

# c.execute("INSERT INTO BiomeLoc VALUES (1, 1, 1, 13.7577326, 121.0643736, 0)")

c.execute("Select Plant.Name, sciName, desc, img, City.Name, xPos, yPos, Disabled From PlantsLoc, Plant, City WHERE PlantsLoc.PlantsID = Plant.PlantID AND PlantsLoc.CityID = City.CityID")
print(c.fetchall())

con.commit()