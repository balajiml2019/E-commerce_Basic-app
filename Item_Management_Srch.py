import Item_Management as IM

srch = IM.Item_Controller()

class Srch_Item_Param:

    def __init__(self, **kwargs):

        if len(kwargs):

            for param in kwargs:
                if param == "Item_No":
                    self.Ino = kwargs[param]
                if param == "Item_Name":
                    self.Iname = kwargs[param]
                if param == "Item_Brand":
                    self.Ibrand = kwargs[param]


def Item_Search(item_val):

    item_filter = False
    filter_cond = ''

    if item_val.Ino != '':
        filter_cond = f" Item_No like '{item_val.Ino}'"
        item_filter = True

    if item_val.Iname != '':
        if item_filter:
            filter_cond += f" AND "
        filter_cond += f" Item_Name like '%{item_val.Iname}%'"
        item_filter = True

    if item_val.Ibrand != '':
        if item_filter:
            filter_cond += f" AND "
        filter_cond += f" Item_Brand like '%{item_val.Ibrand}%'"
        item_filter = True

    item_srch = srch.Get_ItemMaster(filter_cond)

    print(*item_srch, sep="\n")

    #return item_srch

srch1 = Srch_Item_Param(Item_Name ='Pen', Item_No ='1', Item_Brand='Reynolds')

Item_Search(srch1)

#def Get_User_Search():

