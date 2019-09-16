import mysql.connector # mysql-connector-python


def reset():
    mydb = mysql.connector.connect(
        host="localhost",
        user="Sparda",
        passwd="mot_de_passe",
        )
    mycursor = mydb.cursor()
    mycursor.execute("DROP DATABASE IF exists mydatabase")
    mycursor.execute("CREATE DATABASE IF NOT exists mydatabase")
    mycursor.execute("USE mydatabase")
    ##############################################################
    #                        Tables creations               #
    ##############################################################
    mycursor.execute("CREATE TABLE IF NOT exists Categories("
                    "id_categorie INT NOT NULL AUTO_INCREMENT,"
                          " nom VARCHAR(255)," 
                    "PRIMARY KEY (id_categorie)) ENGINE=InnoDB")
    mycursor.execute("CREATE TABLE IF NOT exists Produits("
                          "id_produits VARCHAR(255),"
                          " url VARCHAR(255),"
                    "nom VARCHAR(255) NOT NULL, "
                          "grade ENUM('A','B','C','D','E') NOT NULL,"
                     "categorie INT, magasin VARCHAR(255), image VARCHAR(255),"
                    "PRIMARY KEY (id_produits)) ENGINE=InnoDB")
    mycursor.execute("CREATE TABLE IF NOT exists Favoris(produit VARCHAR(255))")
    ##############################################################
    #                    Tables modifications                #
    ##############################################################
    mycursor.execute("ALTER TABLE Produits "
                     "ADD CONSTRAINT fk_categories FOREIGN KEY (categorie) \
                     REFERENCES Categories(id_categorie)")
    mycursor.execute("ALTER TABLE Favoris "
                     "ADD CONSTRAINT fk_produits FOREIGN KEY (produit) \
                     REFERENCES Produits(id_produits)")

