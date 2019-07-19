import sqlite3
import datetime
import getpass
import random

class Item_Master:

    def __init__(self, **kwargs):

        if len(kwargs):

            for param in kwargs:
                if param == "Ino":
                    self.Ino = kwargs[param]
                if param == "Iname":
                    self.Iname = kwargs[param]
                if param == "Idesc":
                    self.Idesc = kwargs[param]
                if param == "Iqty":
                    self.Iqty = kwargs[param]
                if param == "Ibrand":
                    self.Ibrand = kwargs[param]
                if param == "Istatus":
                    self.status = kwargs[param]
                if param == "Icdt":
                    self.Icdt = kwargs[param]
                if param == "Imdt":
                    self.Imdt = kwargs[param]
                if param == "Icid":
                    self.cid = kwargs[param]
                if param == "Imid":
                    self.mid = kwargs[param]
                if param == "RecStatus":
                    self.mid = kwargs[param]


class Item_Price:

    def __init__(self, **kwargs):

        if len(kwargs):

            for param in kwargs:
                if param == "Ino":
                    self.Ino = kwargs[param]
                if param == "Iseqno":
                    self.Iseqno = kwargs[param]
                if param == "Ifdt":
                    self.Ifdt = kwargs[param]
                if param == "Itdt":
                    self.Itdt = kwargs[param]
                if param == "Iprice":
                    self.Iprice = kwargs[param]
                if param == "Icdt":
                    self.Icdt = kwargs[param]
                if param == "Imdt":
                    self.Imdt = kwargs[param]
                if param == "Icid":
                    self.cid = kwargs[param]
                if param == "Imid":
                    self.mid = kwargs[param]


class Item_Stock:

    def __init__(self, **kwargs):

        if len(kwargs):

            for param in kwargs:
                if param == "Ino":
                    self.Ino = kwargs[param]
                if param == "Istockid":
                    self.Istockid = kwargs[param]
                if param == "Imovedt":
                    self.Imovedt = kwargs[param]
                if param == "Imty":
                    self.Imty = kwargs[param]
                if param == "Imqty":
                    self.Imqty = kwargs[param]
                if param == "Icdt":
                    self.Icdt = kwargs[param]
                if param == "Imdt":
                    self.Imdt = kwargs[param]
                if param == "Icid":
                    self.cid = kwargs[param]
                if param == "Imid":
                    self.mid = kwargs[param]


class Item_Controller:

    def __init__(self):
        self._db = sqlite3.connect('CATALOG.DB')
        self._cur = self._db.cursor()


    def Get_ItemMaster(self,item_no=''):

        itemlist = []
        item = dict()
        sql = 'SELECT * FROM ITEM_MASTER'
        if not len(item_no):
            item_no = '0'
        sql += (f" WHERE Item_No = {item_no}")
        print(sql)
        self._cur.execute(sql)
        rows = self._cur.fetchall()

        for row in rows:
            item = dict({'Ino':row[0], 'Iname':row[1],'Idesc':row[2], 'Iqty':row[3], 'Ibrand':row[4],
                         'Istatus':row[5], 'Icdt':row[6],'Imdt':row[7], 'Icid':row[8],'Imid':row[9]})
                         #'Iprice':None, 'Imoveqty':None})
            itemlist.append(item)

        #Assign the diff prices & move-qty from other tables to this dict, so we get all data in one place

        #item["Iprice"] = self.Get_ItemPrice(item_no)
        #item["Imoveqty"] = self.Get_ItemStock(item_no)

        #print(item)
        return item


    def Get_ItemPrice(self,item_no=''):

        pricelist = []
        price = dict()
        sql = 'SELECT * FROM ITEM_PRICE'
        if not len(item_no):
            item_no = '0'
        sql += (f" WHERE Item_No = {item_no}")
        print(sql)
        self._cur.execute(sql)
        rows = self._cur.fetchall()

        for row in rows:
            price = dict({'Ino':row[0], 'Iseqno':row[1],'Ifdt':row[2], 'Itdt':row[3], 'Iprice':row[4],'Icdt':row[5],
                           'Imdt':row[6], 'Icid':row[7],'Imid':row[8]})
            pricelist.append(price)

        print(pricelist)
        return pricelist


    def Get_ItemStock(self,item_no=''):

        stocklist = []

        stock = dict()
        sql = 'SELECT * FROM ITEM_STOCK'
        if not len(item_no):
            item_no = '0'
        sql += (f" WHERE Item_No = {item_no}")
        print(sql)
        self._cur.execute(sql)
        rows = self._cur.fetchall()

        for row in rows:
            stock = dict(
                {'Ino': row[0], 'Istockid': row[1], 'Imovedt': row[2], 'Imovety': row[3], 'Imoveqty': row[4], 'Icdt': row[5],
                 'Imdt': row[6], 'Icid': row[7], 'Imid': row[8]})
            stocklist.append(stock)

        return stocklist

# ----------- SAVE ITEM MAIN CALL ---------------------#

    def Save_ItemMaster(self,item):


        existingitem = self.Get_ItemMaster(item.Ino)

        print(existingitem)

        if not existingitem:
            self.dbitem = self.__InsertItem(item)
            print("Insert happened")
        else:
            self.dbitem = self.__UpdateItem(item)
            print("Update happened")

        return item

    def Save_ItemPrice(self, item):

        existingitem = self.Get_ItemPrice(item.Ino)

        if existingitem == []:
            self.seqno = 1
            self.dbitem = self.__InsertItemPrice(item)
            print("Insert happened")
        else:
            #In Item2 if seqno is not passed, then we will
            if item.Iseqno == '': #need to handle for seqno which is given by user but not in table
                self.seqno = existingitem[-1]['Iseqno'] + 1
                self.dbitem = self.__InsertItemPrice(item)
                print("Insert happened")
            else:
                self.seqno = item.Iseqno
                self.dbitem = self.__UpdateItemPrice(item)
                print("Update happened")

        return item

    def Save_ItemStock(self, item):

        existingitem = self.Get_ItemStock(item.Ino)

        print('existing: ',existingitem)

        if item.Imty == 'OUT':
            item.Imqty = -item.Imqty

        if existingitem == []:
            self.stockid = 1
            self.dbitem = self.__InsertItemStock(item)
            print("Insert happened")
        else:
            #In Item3 if stockid is not passed, then we will add +1 to the last stockid and insert it.
            if item.Istockid == '':
                self.stockid = existingitem[-1]['Istockid'] + 1
                self.dbitem = self.__InsertItemStock(item)
                print("Insert happened")
            else:
                self.stockid = item.Istockid
                self.dbitem = self.__UpdateItemStock(item)
                print("Update happened")

        return item

# ----------- I N S E R T ---------------------#

    def __InsertItem(self, item):

        self.it = item

        if self.it.Ino == '':
            self.item_no = self.Generate_Item_No(item)

        Cre_dt = self.Get_Curr_date()

        Cre_id = self.Get_Username()

        if self.it.Iqty <= 0:
            status = 'Not Avail'
        else:
            status = 'Avail'

        sql = (
            f"INSERT INTO ITEM_MASTER (Item_No, Item_Name, Item_Desc, Item_Qty, Item_Brand, Item_Status, "
            f"Item_CreatedDt, Item_ModifiedDt, Item_CreatedId, Item_ModifiedId ) "
            f"VALUES ('{self.item_no}', '{self.it.Iname}', '{self.it.Idesc}', {self.it.Iqty}, '{self.it.Ibrand}', "
            f"'{status}','{Cre_dt}', '{Cre_dt}', '{Cre_id}', '{Cre_id}')")

        print(sql)
        try:
            self._cur.execute(sql)
            self._db.commit()
        except sqlite3.Error as err:
            self.it.RecStatus = err
        finally:
            self.it.RecStatus = "Created"
        return self.it

    def __InsertItemPrice(self, item):

        self.it = item

        Cre_dt = self.Get_Curr_date()

        Cre_id = self.Get_Username()

        sql = (
            f"INSERT INTO ITEM_PRICE (Item_No, Item_Seqno, Item_FromDt, Item_ToDt, Item_Price, "
            f"Item_CreatedDt, Item_ModifiedDt, Item_CreatedId, Item_ModifiedId ) "
            f"VALUES ('{self.it.Ino}', '{self.seqno}', '{self.it.Ifdt}', {self.it.Itdt}, '{self.it.Iprice}', "
            f"'{Cre_dt}', '{Cre_dt}', '{Cre_id}', '{Cre_id}')")

        print(sql)
        try:
            self._cur.execute(sql)
            self._db.commit()
        except sqlite3.Error as err:
            self.it.RecStatus = err
        finally:
            self.it.RecStatus = "Created"
        return self.it

    def __InsertItemStock(self, item):

        self.it = item

        Cre_dt = self.Get_Curr_date()

        Cre_id = self.Get_Username()

        sql = (
            f"INSERT INTO ITEM_STOCK (Item_No, Item_StockId, Item_MoveDt, Item_MoveTy, Item_MoveQty, "
            f"Item_CreatedDt, Item_ModifiedDt, Item_CreatedId, Item_ModifiedId ) "
            f"VALUES ('{self.it.Ino}', '{self.stockid}', '{self.it.Imdt}', '{self.it.Imty}', {self.it.Imqty}, "
            f"'{Cre_dt}', '{Cre_dt}', '{Cre_id}', '{Cre_id}')")

        print(sql)
        try:
            self._cur.execute(sql)
            self._db.commit()
        except sqlite3.Error as err:
            self.it.RecStatus = err
        finally:
            self.it.RecStatus = "Created"
        return self.it

#----------- U P D A T E ---------------------#

    def __UpdateItem(self, item):
        self.it = item

        Mod_dt = self.Get_Curr_date()

        Mod_id = self.Get_Username()


        if self.it.Iqty <= 0:
            status = 'Not Avail'
        else:
            status = 'Avail'


        sql = (
            f"UPDATE ITEM_MASTER SET Item_Name = '{self.it.Iname}', Item_Desc = '{self.it.Idesc}', "
            f"Item_Qty = {self.it.Iqty}, Item_Brand = '{self.it.Ibrand}', Item_Status = '{status}', "
            f"Item_ModifiedDt = '{Mod_dt}', Item_ModifiedId = '{Mod_id}' WHERE Item_No = {self.it.Ino}")
        print(sql)

        try:
            self._cur.execute(sql)
            self._db.commit()
        except sqlite3.Error as err:
            self.it.Recstatus = err
        finally:
            self.it.RecStatus = "Updated"
        return self.it

    def __UpdateItemPrice(self, item):
        self.it = item

        Mod_dt = self.Get_Curr_date()

        Mod_id = self.Get_Username()


        sql = (
            f"UPDATE ITEM_PRICE SET Item_FromDt = '{self.it.Ifdt}', Item_ToDt = '{self.it.Itdt}', "
            f"Item_Price = {self.it.Iprice}, Item_ModifiedDt = '{Mod_dt}', Item_ModifiedId = '{Mod_id}' "
            f" WHERE Item_No = {self.it.Ino} AND Item_Seqno = {self.seqno}")
        print(sql)

        try:
            self._cur.execute(sql)
            self._db.commit()
        except sqlite3.Error as err:
            self.it.Recstatus = err
        finally:
            self.it.RecStatus = "Updated"
        return self.it

    def __UpdateItemStock(self, item):
        self.it = item

        Mod_dt = self.Get_Curr_date()

        Mod_id = self.Get_Username()


        sql = (
            f"UPDATE ITEM_STOCK SET Item_MoveDt = '{self.it.Imdt}', Item_MoveTy = '{self.it.Imty}', "
            f"Item_MoveQty = {self.it.Imqty}, Item_ModifiedDt = '{Mod_dt}', Item_ModifiedId = '{Mod_id}' "
            f" WHERE Item_No = {self.it.Ino} AND Item_StockId = {self.stockid}")
        print(sql)

        try:
            self._cur.execute(sql)
            self._db.commit()
        except sqlite3.Error as err:
            self.it.Recstatus = err
        finally:
            self.it.RecStatus = "Updated"
        return self.it


    def Generate_Item_No(self,item):

        self.item_id1 = item.Iname[0]
        self.item_id2 = item.Ibrand[0]
        self.item_id3 = "%06d" % random.randint(1,100000)

        item_no = self.item_id1 + self.item_id2 + str(self.item_id3)

        return item_no

    def Get_Curr_date(self):
        self.Curr_datetime = datetime.datetime.now()
        return self.Curr_datetime

    def Get_Username(self):
        self.user_name = getpass.getuser()
        return self.user_name


#################################################################################


i = Item_Controller()
item1 = Item_Master(Ino='1', Iname='Pencil Sharpner', Idesc='Pencil only', Iqty=50, Ibrand='Nataraj')
item2 = Item_Price(Ino='2', Iseqno = '3', Ifdt='2019-07-05', Itdt='2019-07-15', Iprice=5)
item3 = Item_Stock(Ino='2', Istockid = '', Imdt='2019-07-06', Imty='IN', Imqty=10)

i.Save_ItemStock(item3)



#Post stock - insert each entry / for each entry update master table

'''
1. validation - 
empty for name, desc

it shd be in master table

In stock, insert only shd be done.


modify the SaveItem method to accept all 3 (item_no, price, stock) to do below insert
price & stock insert shd be done after a insert is done in master

qty shd not be updt in master table


return true for all save

2. srch criteira:
Get method for master table shd be modified to accept different filter condi, chng whr to dynamic

Add like for item

'''


