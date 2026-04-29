from datetime import date
from interfaces import PortafolioBase, ActivoBase
from Estructuras import ListaEnlazada, Pila, Cola, MatrizPrecios


class PortafolioReal(PortafolioBase):

    def __init__(self, capital_inicial: float):
        super().__init__(capital_inicial)
        self._capital_inicial = capital_inicial
        self.historial = ListaEnlazada()
        self.compras = Pila()
        self.ventas = Cola()
        self.matriz_precios = MatrizPrecios()
        self.cantidades = {}

    def _validar_compra(self, simbolo: str, cantidad: float, precio: float):
        activo = self.buscar_activo(simbolo)
        if activo is None:
            raise ValueError(f"Activo '{simbolo}' no encontrado en el portafolio.")
        if not (activo.get_precio_minimo_jornada() <= precio <= activo.get_precio_maximo_jornada()):
            raise ValueError("Precio fuera del rango permitido para la jornada")
        costo_total = precio * cantidad
        if costo_total > self.capital_disponible:
            raise ValueError("Capital insuficiente")

    def _validar_venta(self, simbolo: str, cantidad: float, precio: float):
        activo = self.buscar_activo(simbolo)
        if activo is None:
            raise ValueError(f"Activo '{simbolo}' no encontrado en el portafolio.")
        if not (activo.get_precio_minimo_jornada() <= precio <= activo.get_precio_maximo_jornada()):
            raise ValueError("Precio fuera del rango permitido para la jornada")
        if self.cantidades.get(simbolo, 0) < cantidad:
            raise ValueError("No tienes suficientes unidades para vender")

    def comprar(self, simbolo: str, cantidad: float, precio: float) -> bool:
        self._validar_compra(simbolo, cantidad, precio)
        comision = precio * cantidad * 0.005
        costo_total = precio * cantidad + comision
        self.capital_disponible -= costo_total
        self.cantidades[simbolo] = self.cantidades.get(simbolo, 0) + cantidad
        t = {
            "tipo": "compra",
            "simbolo": simbolo,
            "cantidad": cantidad,
            "precio": precio,
            "comision": comision,
            "fecha": date.today()
        }
        self.historial.agregar_al_final(t)
        self.compras.push(t)
        return True

    def vender(self, simbolo: str, cantidad: float, precio: float) -> bool:
        self._validar_venta(simbolo, cantidad, precio)
        comision = precio * cantidad * 0.005
        ingreso = precio * cantidad - comision
        self.capital_disponible += ingreso
        self.cantidades[simbolo] = self.cantidades.get(simbolo, 0) - cantidad
        t = {
            "tipo": "venta",
            "simbolo": simbolo,
            "cantidad": cantidad,
            "precio": precio,
            "comision": comision,
            "fecha": date.today()
        }
        self.historial.agregar_al_final(t)
        self.ventas.encolar(t)
        return True

    def get_capital_disponible(self) -> float:
        return self.capital_disponible

    def get_cantidad(self, simbolo: str) -> float:
        return self.cantidades.get(simbolo, 0)

    def get_historial_transacciones(self) -> list:
        return self.historial.obtener_todos()

    def get_historial_por_fecha(self, fecha: date) -> list:
        return self.historial.buscar(lambda t: t["fecha"] == fecha)

    def get_composicion(self) -> dict:
        valor_total = self.get_valor_total()
        composicion = {}
        for activo in self.activos:
            valor_activo = activo.get_valor_actual()
            composicion[activo.simbolo] = round(valor_activo / valor_total * 100, 2)
        composicion["efectivo"] = round(self.capital_disponible / valor_total * 100, 2)
        return composicion

    def get_rentabilidad(self) -> float:
        return round(self.get_rentabilidad_total(), 2)

    def get_rentabilidad_neta(self) -> float:
        dividendos = sum(a.get_dividendos_acumulados() for a in self.activos)
        rentabilidad_base = self.get_valor_activos() - self.get_costo_total_invertido()
        return round((rentabilidad_base + dividendos) / self._capital_inicial * 100, 2)
