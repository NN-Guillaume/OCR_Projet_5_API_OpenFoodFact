# Please, remember that the more fields you ask, the less are the chance to find products
from math import ceil
import requests


class Category:
    """class who represents the object category"""

    def __init__(self, name, nb, en, adresse, id):
        """Constructor of the category class"""
        self.name = name  # Category name
        self.nb_product = nb  # Number of products from the category
        self.name_en = en  # The english name
        self.adresse = adresse  # Category's URL
        self.nombre_pages = ceil(self.nb_product / 20)  # Page number
        self.id = id  # Category ID

    def display_category_type(self):
        """ Display a category's informations
         in a eyes-friendly way"""
        print("\n##############################")
        print(self.id, " - ", end=" ")
        print(self.name, end="       ")
        print("(", self.name_en, ")")
        print("\t Nombre de produits :", self.nb_product, end=" ")
        print("\t Nombre de pages :", self.nombre_pages)
        print("\t", self.adresse)
        print("\n##############################")

    def get_api_products(self, page):
        """Get a category's products page"""

        adresse = self.adresse + "/" + str(page) + ".json"
        p = requests.get(adresse)
        produits = p.json()
        return produits

    @staticmethod
    def get_api_categories():
        """Get the categories thanks to the OpenFoodFact's API"""
        print(" . . . Veuillez patienter... Requête en cours. . . ")
        r = requests.get("https://fr.openfoodfacts.org/categories.json")
        categories = r.json()
        category_number = categories.get("count")
        print(" {} catégories présentes sur le site.".format(category_number))
        return categories


class Product:
    """class who represent the object product"""

    compteur_instance = 0

    def __init__(self, name, url, note, id, categorie, stores, image_url):
        """Constructeur de la classe Produit"""
        self.name = name  # product_name_fr #generic_name #categories
        self.grade = note
        self.url = url
        self.code_barre = id
        self.categorie = categorie
        self.image_url = image_url
        self.stores = stores
        self.clean_product()

    def display_product(self):
        """ Display the informations about a product"""
        print("-------------------------------------------")
        print(
            "Nom : \t", self.name, end="         "
        )  # product_name_fr #generic_name #categories
        print("Grade : \t", self.grade.upper())
        print("url : \t", self.url)
        print("Code barre : \t", self.code_barre)
        print("Catégorie : \t", self.categorie)
        print("En vente ici : ", self.stores, end="          ")
        print("Image : ", self.image_url)
        print("-------------------------------------------")

    def clean_product(self):
        """Method who cleans a bit the product's description"""
        if self.grade in ["a", "b", "c", "d", "e"]:
            self.grade = self.grade.upper()
        elif self.grade not in ["A", "B", "C", "D", "E"]:
            print(self.grade)
