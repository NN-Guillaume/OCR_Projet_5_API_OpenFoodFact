import mysql.connector  # mysql-connector-python


# Singleton à faire
class Database:
    """ Classe d'interaction avec la BDD"""

    def __init__(self):
        """Constructeur de la class Database"""
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="Sparda",
            passwd="mot_de_passe",
            database="mydatabase"  # La base doit exister.
            # auth_plugin='mysql_native_password'
        )
        self.mycursor = self.mydb.cursor()

    ##############################################################
    #                       Insertion  of the data              #
    ##############################################################
    def set_categorie(self, categorie):
        """save the categories into the database"""
        sql = """INSERT INTO Categories(nom) VALUES (%s)"""
        val = (categorie.name,)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    def set_product(self, produit):
        """Method who add a product into the base"""
        sql = """INSERT INTO Produits(id_produits, url, nom, grade, categorie, magasin, image) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        val = (
            produit.code_barre,
            produit.url,
            produit.name,
            produit.grade,
            produit.categorie,
            produit.stores,
            produit.image_url
        )
        self.mycursor.execute(sql, val)
        self.mydb.commit()
        print(self.mycursor.rowcount, "record inserted.")


    def set_favoris(self, produit):
        """Method who add a product as a favorite"""
        sql = """INSERT INTO Favoris(produit)\
                VALUES (%s)"""
        val = (produit.code_barre,)
        self.mycursor.execute(sql, val)
        self.mydb.commit()


    ##############################################################
    #                       Selection  of the data               #
    ##############################################################

    def get_all_categorie(self):
        """ Method who returns all the categories saved into the database"""
        self.mycursor.execute("SELECT * FROM Categories")
        return self.mycursor.fetchall()

    def print_all_categories(self):
        """Display all the categories"""
        liste = self.get_all_categorie()
        for i in range(len(liste)):
            print(liste[i][0], ".\t", liste[i][1])

    def get_product_from_categorie(self, id):
        """ Method who returns all the products thanks to the category ID"""
        sql = """SELECT * FROM Produits WHERE categorie = (%s)"""
        val = (id,)
        self.mycursor.execute(sql, val)
        return self.mycursor.fetchall()

    def print_product_from_categorie(self, id):
        """Display the products from a given category"""
        list = self.get_product_from_categorie(id)
        for i in range(len(list)):
            print(i + 1, ".\t", list[i][2], "(", list[i][3], ")")
        return list

    def get_all_favoris(self):
        """ Method who returns all the favorites saved into the database"""
        sql = """SELECT *
                FROM Produits 
                INNER JOIN Favoris ON Produits.id_produits = Favoris.produit"""
        self.mycursor.execute(sql)
        return self.mycursor.fetchall()

    def print_all_favoris(self):
        """Display all the favorites"""
        list = self.get_all_favoris()
        for i in range(len(list)):
            print(i + 1, ".\t", list[i][2], "(", list[i][3], ")")

    def search_substitut(self, cat, grade):
        """Return a substitute with a better grade"""
        sql = """SELECT * 
                FROM Produits 
                WHERE categorie = (%s) AND grade <= (%s)
                ORDER BY grade"""
        val = (cat, grade)
        self.mycursor.execute(sql, val)
        return self.mycursor.fetchall()