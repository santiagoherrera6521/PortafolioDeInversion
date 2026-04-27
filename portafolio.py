from datetime import date
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

    def comprar(self, ticker: str, cantidad: float) -> Transaccion:
        precio = self.activos[ticker].get_precio_actual()
        self._validar_compra(ticker, cantidad, precio)
        comision = precio * cantidad * 0.005
        costo_total = precio * cantidad + comision
        self.capital_disponible -= costo_total
        self.cantidades[ticker] = self.cantidades.get(ticker, 0) + cantidad
        t = Transaccion("compra", ticker, cantidad, precio, comision, date.today())
        self.historial.agregar_al_final(t)
        self.compras.push(t)
        return t