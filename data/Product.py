# class Product:
#     def __init__(self, id_service , naming, descrip, price, discount, id_type, name, photo= None):
#         self.id_service = id_service
#         self.naming = naming
#         self.descrip = descrip
#         self.price = price
#         self.discount = discount
#         self.id_type = id_type
#         self.name = name
#         self.photo = photo

class Product:
    def __init__(self, id_service, naming, descrip,
                 price, discount, id_type, name, photo = None ):
        self.id_service = id_service
        self.naming = naming
        self.descrip = descrip
        self.price = price
        self.discount = discount
        self.id_type = id_type
        self.name = name
        self.photo = photo
