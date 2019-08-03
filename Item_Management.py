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

class Validation_Error(Exception):

        pass
        #err = "Empty field passed..!!"


class Item_Controller:

    def __init__(self):
        self._db = sqlite3.connect('CATALOG.DB')
        self._cur = self._db.cursor()

    def Get_ItemMaster(self, filter_cond='',srch=None):

        itemlist = []
        item = dict()
        sql = 'SELECT * FROM ITEM_MASTER'

        sql += f" WHERE {filter_cond}"
        print(sql)
        self._cur.execute(sql)
        rows = self._cur.fetchall()

        for row in rows:
            item = dict({'Ino': row[0], 'Iname': row[1], 'Idesc': row[2], 'Iqty': row[3], 'Ibrand': row[4],
                         'Istatus': row[5], 'Icdt': row[6], 'Imdt': row[7], 'Icid': row[8], 'Imid': row[9],
                         'Iprice':None, 'Imoveqty':None})
            itemlist.append(item)

        # Assign the diff prices & move-qty from other tables to this dict, so we get all data in one place

            item["Iprice"] = self.Get_ItemPrice(row[0])
            item["Imoveqty"] = self.Get_ItemStock(row[0])

        # print(item)
        return itemlist

    def Get_ItemPrice(self, item_no=''):

        pricelist = []
        price = dict()
        sql = 'SELECT * FROM ITEM_PRICE'
        if int(item_no) < 0:
            item_no = 0
        sql += (f" WHERE Item_No = {item_no}")
        print(sql)
        self._cur.execute(sql)
        rows = self._cur.fetchall()

        for row in rows:
            price = dict(
                {'Ino': row[0], 'Iseqno': row[1], 'Ifdt': row[2], 'Itdt': row[3], 'Iprice': row[4], 'Icdt': row[5],
                 'Imdt': row[6], 'Icid': row[7], 'Imid': row[8]})
            pricelist.append(price)

        print(pricelist)
        return pricelist

    def Get_ItemStock(self, item_no=''):

        stocklist = []

        stock = dict()
        sql = 'SELECT * FROM ITEM_STOCK'

        if int(item_no) < 0:
            item_no = 0
        sql += (f" WHERE Item_No = {item_no}")

        print(sql)
        self._cur.execute(sql)
        rows = self._cur.fetchall()

        for row in rows:
            stock = dict(
                {'Ino': row[0], 'Istockid': row[1], 'Imovedt': row[2], 'Imovety': row[3], 'Imoveqty': row[4],
                 'Icdt': row[5],
                 'Imdt': row[6], 'Icid': row[7], 'Imid': row[8]})
            stocklist.append(stock)

        return stocklist

    # ----------- SAVE ITEM MAIN CALL ---------------------#

    def Save_ItemMaster(self, item):

        if not len(item.Ino):
            item.Ino = 0

        filter_cond = f"Item_No = {item.Ino}"

        existingitem = self.Get_ItemMaster(filter_cond)

        print(existingitem)

        if not existingitem:

            self.Item_Exception_Check(item)
            if not Validation_Error or self.Item_Check == True:
                self.dbitem1 = self.__InsertItem(item)
                if True:
                    print("ITEM_MASTER Insert happened")
                    self.dbitem4 = self.Price_Stock_Entry(item)
        else:
            self.dbitem = self.__UpdateItem(item)
            print("ITEM_MASTER Update happened")

        return item

    def Save_ItemPrice(self, item):

        existingitem = self.Get_ItemPrice(item.Ino)

        if existingitem == []:
            self.seqno = 1
            self.dbitem = self.__InsertItemPrice(item)
            print("ITEM_PRICE Insert happened")
        else:
            # In Item2 if seqno is not passed, then we will
            if item.Iseqno == '':  # need to handle for seqno which is given by user but not in table
                self.seqno = existingitem[-1]['Iseqno'] + 1
                self.dbitem = self.__InsertItemPrice(item)
                print("ITEM_PRICE Insert happened")
            else:
                self.seqno = item.Iseqno
                self.dbitem = self.__UpdateItemPrice(item)
                print("ITEM_PRICE Update happened")

        return item

    def Save_ItemStock(self, item):

        existingitem = self.Get_ItemStock(item.Ino)

        print('existing: ', existingitem)

        if item.Imty == 'OUT':
            item.Imqty = -item.Imqty

        # exist chk in stock

        if existingitem == []:
            self.stockid = 1
            self.dbitem = self.__InsertItemStock(item)
            print("ITEM_STOCK Insert1 happened")
        else:
            # In Item3 if stockid is not passed, then we will add +1 to the last stockid and insert it.
            if item.Istockid == '':
                self.stockid = existingitem[-1]['Istockid'] + 1
                self.dbitem = self.__InsertItemStock(item)
                print("ITEM_STOCK Insert2 happened")
            else:
                self.stockid = item.Istockid
                self.dbitem = self.__UpdateItemStock(item)
                print("ITEM_STOCK Update happened")

        return item

    # ----------- I N S E R T ---------------------#

    def __InsertItem(self, item):

        self.it = item

        if self.it.Ino == '':
            self.item_no = self.Generate_Item_No(item)
        else:
            self.item_no = self.it.Ino

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
            return True
        except sqlite3.Error as err:
            self.it.RecStatus = err


    def __InsertItemPrice(self, item):

        self.it = item

        Cre_dt = self.Get_Curr_date()

        Cre_id = self.Get_Username()

        print(self.it.Itdt)

        sql = (
            f"INSERT INTO ITEM_PRICE (Item_No, Item_Seqno, Item_FromDt, Item_ToDt, Item_Price, "
            f"Item_CreatedDt, Item_ModifiedDt, Item_CreatedId, Item_ModifiedId ) "
            f"VALUES ('{self.it.Ino}', '{self.seqno}', '{self.it.Ifdt}', '{self.it.Itdt}', '{self.it.Iprice}', "
            f"'{Cre_dt}', '{Cre_dt}', '{Cre_id}', '{Cre_id}')")

        print(sql)
        try:
            self._cur.execute(sql)
            self._db.commit()
            return True
        except sqlite3.Error as err:
            self.it.RecStatus = err


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
            if self.stockid != 1:
                print(self.stockid)
                self.Master_Qty_Updt(item)
            return True
        except sqlite3.Error as err:
            self.it.RecStatus = err

    # ----------- U P D A T E ---------------------#

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
            f"Item_Brand = '{self.it.Ibrand}', Item_Status = '{status}', "
            f"Item_ModifiedDt = '{Mod_dt}', Item_ModifiedId = '{Mod_id}' WHERE Item_No = {self.it.Ino}")
        print(sql)

        try:
            self._cur.execute(sql)
            self._db.commit()
            return True
        except sqlite3.Error as err:
            self.it.Recstatus = err


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
            return True
        except sqlite3.Error as err:
            self.it.Recstatus = err

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
            return True
        except sqlite3.Error as err:
            self.it.Recstatus = err

    #######----------- UPDATE MASTER FOR QTY UPDT IN STOCK ------------------########

    def Master_Qty_Updt(self, item):

        filter_cond = f"Item_No = {item.Ino}"

        existingitem = self.Get_ItemMaster(filter_cond)

        if not existingitem:
            print("Stock entry is not avail in Item Master table")
        else:
            existingitem['Iqty'] = existingitem['Iqty'] + item.Imqty

        item1 = Item_Master(Ino=item.Ino, Iname=existingitem['Iname'], Idesc=existingitem['Idesc'],
                            Iqty=existingitem['Iqty'], Ibrand=existingitem['Ibrand'])

        self.__UpdateItem(item1)
        print("Master_Qty_Updated")

    #######----------- INSERT IN PRICE & STOCK WHEN AN ENTRY HAPPENS IN ITEM MASTER -------########

    def Price_Stock_Entry(self, item):

        curr_dt = datetime.date.today()

        curr_dt_1 = datetime.date.today() + datetime.timedelta(days=1)

        item2 = Item_Price(Ino=item.Ino, Ifdt=curr_dt, Itdt=curr_dt_1, Iprice=item.Iprice)
        item3 = Item_Stock(Ino=item.Ino, Imdt=curr_dt, Imty='IN', Imqty=item.Iqty)

        self.dbitem2 = self.Save_ItemPrice(item2)
        self.dbitem3 = self.Save_ItemStock(item3)

        print("Price_Stock_Inserted")

        return item
    #######----------- GENERATE ITEM_NO, CURR_DT, USERNAME, EXCEPTION ------------------########

    def Generate_Item_No(self, item):

        self.item_id1 = item.Iname[0]
        self.item_id2 = item.Ibrand[0]
        self.item_id3 = "%06d" % random.randint(1, 100000)

        item_no = self.item_id1 + self.item_id2 + str(self.item_id3)

        return item_no

    def Get_Curr_date(self):
        self.Curr_datetime = datetime.datetime.now()
        return self.Curr_datetime

    def Get_Username(self):
        self.user_name = getpass.getuser()
        return self.user_name

    def Item_Exception_Check(self,item):

        try:
            self.Item_Check = False


            if item.Iname == '':
                raise Validation_Error('Empty Item Name passed')
            elif item.Idesc == '':
                raise Validation_Error('Empty Item Desc passed')
            elif item.Ibrand == '':
                raise Validation_Error('Empty Item Brand passed')
            elif item.Iprice == '':
                raise Validation_Error('Empty Item Price passed')
            elif item.Iqty == '':
                raise Validation_Error('Empty Item Quantity passed')
            else:
                self.Item_Check = True

        except Validation_Error as e:
            print(e)


#################################################################################


i = Item_Controller()
item1 = Item_Master(Ino='19', Iname='', Idesc='Glasss', Iqty='', Ibrand='Nataraj',Iprice=5)
item2 = Item_Price(Ino='2', Iseqno='3', Ifdt='2019-07-05', Itdt='2019-07-15', Iprice=5)
item3 = Item_Stock(Ino='1', Istockid='', Imdt='2019-07-21', Imty='OUT', Imqty=10)

if __name__ == '__main__':
    i.Save_ItemMaster(item1)


'''


if 2 or more items entered for srch criteria , then handle it.

    --> 


add price & stock to master dic and display

do.co - cloud > to create mysql 


'''
