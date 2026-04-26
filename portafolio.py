from interfaces import PortafolioBase
from estructuras import ListaEnlazada, Pila, Cola, MatrizPrecios

class PortafolioReal(PortafolioBase):
    def __init__(self, capital_inicial: float):
        self.capital_inicial = capital_inicial
        self.capital_disponible = capital_inicial
        self.activos = {}
        self.cantidades = {}
        self.historial = ListaEnlazada()
        self.compras = Pila()
        self.ventas = Cola()
        self.matriz_precios = MatrizPrecios()