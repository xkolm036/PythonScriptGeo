import csv,operator,os
import pyodbc

class Geo(object):
   def __init__(self,ADM,kodObce,NazevObce,kodCastiObce,nazevCastiObce,kodUlice,nazevUlice,typSO,cisloDomu,PSC,x,y):
       self.kodObce = kodObce
       self.PSC = PSC
       self.typSO = typSO
       self.kodUlice = kodUlice
       self.NazevObce = NazevObce
       self.nazevCastiObce = nazevCastiObce
       self.nazevUlice = nazevUlice
       self.cisloDomu = cisloDomu
       self.ADM = ADM
       self.kodCastiObce = kodCastiObce
       self.x = x
       self.y = y

class CastObce_ID(object):
    def __init__(self,nazev,id):
          self.nazev = nazev
          self.id = id

class NazevObceUlice(object):
    def __init__(self,nazevObce,NazevUlice):
          self.nazevObce = nazevObce
          self.NazevUlice = NazevUlice


cityId = 0
cityPartId = 0
StreetId = 0
houseId = 0

os.chdir("C://CSV")

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                     'Server=(localdb)\MSSQLLocalDB;'
                     'Database=DP;'
                     'Trusted_Connection=yes;')
cursor = conn.cursor()
cursor.execute("DELETE from House");
cursor.execute("DELETE from Street");
cursor.execute("DELETE from CityPart");
cursor.execute("DELETE from City");

for file in os.listdir("./"): #
  
    file = open(file,newline='')
    csv1 = csv.reader(file)
    print("{} CityID: {} CytyPart: {} StreetId: {} HouseId: {}".format(file.name,cityId,cityPartId,StreetId,houseId));
    rows = []
    rows.clear()
    header = next(csv1)
    #Vytvorim si pole trid s jednotlivyma argumentama cvs
    for line in csv1:
        arg = str(line).split(";")
        radek = Geo(arg[0],arg[1],arg[2],arg[7],arg[8],arg[9],arg[10],arg[11],arg[12],arg[15],arg[17],arg[16],)
        rows.append(radek)
    if len(rows)==0:
        continue
    rows_sorted = sorted(rows,key=lambda castobce:castobce.nazevCastiObce); #serazeno podle nazvu obce
    cityId = cityId + 1
    #Vytvorim mesto
    cursor.execute("INSERT into City(Id,ADM,Name,Nuber) VALUES(?,?,?,?)",cityId,str(rows_sorted[0].ADM).replace("['",""),rows_sorted[0].NazevObce,rows_sorted[0].kodObce)
    #Pridam domy a casti obce do DB
    castObcePred = "NotInit"
    existujiciCastiMesta = []
    existujiciCastiMesta.clear()
    for radek in rows_sorted:
        if radek.nazevCastiObce != castObcePred:
           cityPartId = cityPartId + 1
           castobce = CastObce_ID(radek.nazevCastiObce,cityPartId)
           existujiciCastiMesta.append(castobce)
           castObcePred=radek.nazevCastiObce
           cursor.execute("INSERT into CityPart(Id,Name,City_Id,Nuber,ZIP) VALUES(?,?,?,?,?)",cityPartId,radek.nazevCastiObce,cityId,radek.kodCastiObce,radek.PSC)

        if radek.typSO != "č.ev.":
           houseId = houseId + 1
           cursor.execute("INSERT into House(Id,Number,CityPart_Id,x,y) VALUES(?,?,?,?,?)",houseId,radek.cisloDomu,cityPartId,radek.x,radek.y)
    #pridam ulice                                                            
    if rows_sorted[0].nazevUlice != "":
       rows_sorted = sorted(rows,key=lambda ulice:ulice.nazevUlice)#serazeno podle nazvu ulice
       ulice=[];
       ulice.clear();
      
       for radek in rows_sorted:
           for existCastObce in existujiciCastiMesta:
               if existCastObce.nazev == radek.nazevCastiObce:
                  obecId=existCastObce.id

           if radek.nazevUlice!="":
              pom=0;
              for ul in ulice:               
                  if ul.nazevObce==radek.nazevCastiObce and ul.NazevUlice==radek.nazevUlice:               
                     pom=1;
                     break;      
              if pom==0:
                 ulice.append(NazevObceUlice(radek.nazevCastiObce,radek.nazevUlice))
                 StreetId = StreetId + 1
                 cursor.execute("INSERT into Street(Id,Name,Nuber,CityPart_Id) VALUES(?,?,?,?)",StreetId,radek.nazevUlice,radek.kodUlice,obecId)

                    

         
    conn.commit();

conn.close();
    
   

 
       



