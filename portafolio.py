from interfaces import PortafolioBase, Transaccion
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

    def _validar_compra(self, ticker: str, cantidad: float, precio: float):
        activo = self.activos[ticker]
        precio_mercado = activo.get_precio_actual()
        precio_min = precio_mercado * 0.98
        precio_max = precio_mercado * 1.02

        if precio < precio_min or precio > precio_max:
            raise ValueError("Precio fuera del rango permitido para la jornada")

        costo_total = precio * cantidad
        if costo_total > self.capital_disponible:
            raise ValueError("Capital insuficiente")

    def _validar_venta(self, ticker: str, cantidad: float, precio: float):
        activo = self.activos[ticker]
        precio_mercado = activo.get_precio_actual()
        precio_min = precio_mercado * 0.98
        precio_max = precio_mercado * 1.02

        if precio < precio_min or precio > precio_max:
            raise ValueError("Precio fuera del rango permitido para la jornada")

        if self.cantidades[ticker] < cantidad:
            raise ValueError("No tienes suficientes unidades para vender")