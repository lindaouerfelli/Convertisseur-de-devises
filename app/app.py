from PySide2 import QtWidgets
import currency_converter
# cette classe représente lafenetre de mon interface graphqie 
# la classe App hérite dela classe Qtwidgets

class App(QtWidgets.QTableWidget):
    # self = moi la classe
    def __init__(self):
        super().__init__() # permet d'appeler la méthode init de QtWidgets
        self.c = currency_converter.CurrencyConverter()
        self.setWindowTitle("Convertisseur de devise")
        self.setup_ui()
        self.set_default_values()
        self.setup_css()
        self.setup_connections()

    def setup_ui(self):
        # on va cree tout les widgets vont appartenir a qtwidgets
        self.layout = QtWidgets.QHBoxLayout(self) # ce dernier self pour lier le layout a notre fenetre
        self.cbb_devisesFrom = QtWidgets.QComboBox() # pas beosinde self ici car il sont liée a layout # une liste déroulante 
        self.spn_montant =  QtWidgets.QSpinBox() #une boîte de spin qui permet à l'utilisateur d'entrer des valeurs numériques en les incrémentant ou en les décrémentant à l'aide de flèches de rotation
        self.cbb_devisesTo = QtWidgets.QComboBox()
        self.spn_montantConverti = QtWidgets.QSpinBox() 
        self.btn_inverser = QtWidgets.QPushButton(" Inverser devises")

        self.layout.addWidget(self.cbb_devisesFrom) # ajouter tout les widgets au layout 
        self.layout.addWidget(self.spn_montant)
        self.layout.addWidget(self.cbb_devisesTo)
        self.layout.addWidget(self.spn_montantConverti)
        self.layout.addWidget(self.btn_inverser)

    def set_default_values(self) : 

        self.cbb_devisesFrom.addItems(sorted(list(self.c.currencies)))
        self.cbb_devisesTo.addItems(sorted(list(self.c.currencies)))
        self.cbb_devisesFrom.setCurrentText("EUR")
        self.cbb_devisesTo.setCurrentText("EUR")

        self.spn_montant.setRange(1, 1000000000)
        self.spn_montantConverti.setRange(1, 1000000000)
        
        self.spn_montant.setValue(100)
        self.spn_montantConverti.setValue(100)

        
    def setup_connections (self):
        self.cbb_devisesFrom.activated.connect(self.compute) #Si vous utilisez PyQt ou PySide2 avec un widget spécifique, comme QComboBox, le signal activated est utilisé pour détecter quand un élément de la liste déroulante est sélectionné
        self.cbb_devisesTo.activated.connect(self.compute)
     
        self.spn_montant.valueChanged.connect(self.compute)
        self.btn_inverser.clicked.connect(self.inverser_devise)

    def setup_css(self):
        self.setStyleSheet("""
        
        background-color: rgb(30, 30, 30);
        color: rgb(240, 240, 240);
        
        """)


    def compute(self): # event declencher quand on modifie le devise pour faire le calcul
        
        montant = self.spn_montant.value()
        devise_from = self.cbb_devisesFrom.currentText()
        devise_to = self.cbb_devisesTo.currentText()
        try : 
            resultat = self.c.convert(montant, devise_from, devise_to)
        except Exception as e:
            print (" ERRUER DECLENCHE : "+ str(e))
        else : # cas ou on a pas d'erreur se fait apres le try 
            self.spn_montantConverti.setValue(resultat)



    def inverser_devise (self):
        devise_from = self.cbb_devisesFrom.currentText()
        devise_to = self.cbb_devisesTo.currentText()
        self.cbb_devisesFrom.setCurrentText(devise_to)
        self.cbb_devisesTo.setCurrentText(devise_from)
        self.compute()

app = QtWidgets.QApplication([]) # c'est notre application  a l'interieur de laquelle on va pouvoir ouvrir nos fenetres ( qu'on va instancier de la classe app )  or que ici on une seule fenetre
win = App()
# le app cree une application et le win cree une fenetre qui tourne dans cette application 
win.show()
app.exec_()