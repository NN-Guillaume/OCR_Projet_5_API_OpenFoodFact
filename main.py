from database import *
from product import *
import resetDataBase

# The constants
url_base = "https://fr.openfoodfacts.org/categorie/"  # we add produit/i.json
url_pages_loading = "https://world.openfoodfacts.org/cgi/search.pl?search_terms=page_size=1000&action=process&json=1"
products_number = url_pages_loading
total_products = 0
total_charged = 0
total_analysed = 0

print("------------------------------------------------------")
print("1. Création et initialisation de la BDD avant d'utiliser l'application")
print("2. Utiliser directement l'application ")
print("0. Quitter le programme")
print("------------------------------------------------------")
choice = int(input("\n"))

if choice == 1:
    resetDataBase.reset()
    # The use of the API shall be made only on the first use of the program
    instance = Database()
    categories = Category.get_api_categories()
    number_to_display = int(input("Combien de catégories voulez-vous charger ? "))
    # I begun with a number of products per category
    for i in range(1, number_to_display + 1):
        categorie = Category(
            categories["tags"][i].get("name"),
            categories["tags"][i].get("products"),
            categories["tags"][i].get("id"),
            categories["tags"][i].get("url"),
            i,
        )
        categorie.display_category_type()
        total_products += categorie.nb_product
        instance.set_categorie(categorie)
        # for page in range(1, nb_produit + 1):
        for page in products_number:
            produits = categorie.get_api_products(page)
            for k in range(
                20
            ):  # Warning, there could be an error of loading on the last page
                total_analysed += 1
                # Use of "get" for the dictionaries instead of the [""]
                try:
                    produit = Product(
                        produits["products"][k].get("product_name", "XXX"),
                        produits["products"][k].get("url", "url absente"),
                        produits["products"][k].get("nutrition_grade_fr", "E"),
                        produits["products"][k].get("id", "ID absent"),
                        i,
                        produits["products"][k].get("stores", "Information manquante"),
                        produits["products"][k].get(
                            "image_url", "Information manquante"
                        ),
                    )
                    produit.display_product()
                    try:
                        instance.set_product(produit)
                        total_charged += 1
                    except:
                        print("produit ignoré cause base de données incomplète")
                        pass
                except:
                    print(
                        "Produit ignoré pour cause d'information essentielle manquante"
                    )
    print(
        "\n Ces {} catégories contiennent {} produits dont {} ont été analysés et {} retenus".format(
            number_to_display, total_products, total_analysed, total_charged
        )
    )
### In the case where the base already exists
else:
    instance = Database()

reception_menu = True
while reception_menu:
    print("------------------------------------------------------")
    print("1. Afficher les catégories et commencer une recherche ")
    print("2. Afficher les favoris sauvegardés")
    print("0. Quitter le programme")
    print("------------------------------------------------------")
    choice = int(input())
    if choice == 1:
        instance.print_all_categories()
        choice = int(input("Numéro de la catégorie :\n"))
        list = instance.print_product_from_categorie(choice)
        choice = int(input("Sélectionnez un produit : \n"))
        print("------------ Votre selection ------------")

        produit = Product(
            list[choice - 1][2],
            list[choice - 1][1],
            list[choice - 1][3],
            list[choice - 1][0],
            list[choice - 1][4],
            list[choice - 1][5],
            list[choice - 1][6],
        )
        produit.display_product()
        print("------------ Votre substitut ------------")
        list = instance.search_substitut(produit.categorie, produit.grade)
        substitut = Product(
            list[0][2],
            list[0][1],
            list[0][3],
            list[0][0],
            list[0][4],
            list[0][5],
            list[0][6],
        )
        substitut.display_product()
        choice = input("Souhaitez vous le sauvgarder ? O/N\n").upper()
        if choice == "O":
            instance.set_favoris(substitut)
        elif choice == "N":
            pass
        else:
            print("Veuillez recommencer")
            pass
    elif choice == 2:
        instance.print_all_favoris()
    elif choice == 0:
        print("Vous quittez le programme")
        reception_menu = False
    else:
        print("Veuillez réessayer en regardant votre clavier")
