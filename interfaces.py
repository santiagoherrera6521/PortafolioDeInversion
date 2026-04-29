from abc import ABC, abstractmethod
from datetime import date
from typing import Optional


class Transaccion:

    def __init__(self, tipo: str, ticker: str, cantidad: float,
                 precio: float, comision: float, fecha: date):
        self.tipo = tipo          # 'compra' o 'venta'
        self.ticker = ticker
        self.cantidad = cantidad
        self.precio = precio
        self.comision = comision
        self.fecha = fecha

    def get_valor_bruto(self) -> float:
        return self.cantidad * self.precio

    def get_valor_neto(self) -> float:
        if self.tipo == 'compra':
            return self.get_valor_bruto() + self.comision
        return self.get_valor_bruto() - self.comision

    def __repr__(self):
        return (f"Transaccion({self.tipo.upper()} | {self.ticker} | "
                f"x{self.cantidad} @ ${self.precio:,.2f} | "
                f"comision ${self.comision:,.2f} | {self.fecha})")

class ActivoBase(ABC):
    """
    Clase abstracta base para todos los activos del portafolio.
    Parte 1 implementa: Accion, CDT, Bono.
    mock_data implementa: ActivoMock (para pruebas).
    """

    def __init__(self, simbolo: str, nombre: str, cantidad: float,
                 precio_compra: float):
        self.simbolo = simbolo
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio_compra = precio_compra
        self.fecha_compra = date.today()
    @abstractmethod
    def get_precio_actual(self) -> float:
        pass

    @abstractmethod
    def get_precio_minimo_jornada(self) -> float:
        pass

    @abstractmethod
    def get_precio_maximo_jornada(self) -> float:
        pass

    @abstractmethod
    def get_dividendos_acumulados(self) -> float:
        pass

    @abstractmethod
    def get_dividendo_anual(self) -> float:
        """
        Dividendo o interés anual estimado por unidad del activo.
        Necesario para calcular rentabilidad neta en PortafolioReal.
        - Accion: dividendo anual por acción (yfinance)
        - CDT: capital * tasa_anual
        - Bono: valor_nominal * tasa_cupon
        """
        pass

    # ── Métodos concretos — iguales para todos los activos ────────────────────

    def get_valor_actual(self) -> float:
        return self.cantidad * self.get_precio_actual()

    def get_costo_total(self) -> float:
        return self.cantidad * self.precio_compra

    def get_rentabilidad_neta(self, comision_total: float = 0.0) -> float:

        ganancia = self.get_valor_actual() - self.get_costo_total()
        return ganancia + self.get_dividendos_acumulados() - comision_total

    def get_rentabilidad_porcentual(self) -> float:
        costo = self.get_costo_total()
        if costo == 0:
            return 0.0
        return ((self.get_valor_actual() - costo) / costo) * 100

    def __repr__(self):
        return (f"{self.__class__.__name__}("
                f"simbolo={self.simbolo!r}, "
                f"cantidad={self.cantidad}, "
                f"precio_actual={self.get_precio_actual():.2f})")
class PortafolioBase(ABC):
    def __init__(self, capital_inicial: float):
        self.capital_disponible = capital_inicial
        self.activos = []
        self.historial = []
    @abstractmethod
    def comprar(self, simbolo: str, cantidad: float, precio: float) -> bool:
        pass

    @abstractmethod
    def vender(self, simbolo: str, cantidad: float, precio: float) -> bool:
        pass
    def get_valor_activos(self) -> float:
        return sum(a.get_valor_actual() for a in self.activos)

    def get_valor_total(self) -> float:
        return self.capital_disponible + self.get_valor_activos()

    def get_costo_total_invertido(self) -> float:
        """Suma del costo de compra de todos los activos."""
        return sum(a.get_costo_total() for a in self.activos)

    def get_rentabilidad_total(self) -> float:
        costo = self.get_costo_total_invertido()
        if costo == 0:
            return 0.0
        valor = self.get_valor_activos()
        dividendos = sum(a.get_dividendos_acumulados() for a in self.activos)
        return ((valor - costo + dividendos) / costo) * 100

    def get_dividendos_totales(self) -> float:
        return sum(a.get_dividendos_acumulados() for a in self.activos)

    def buscar_activo(self, simbolo: str) -> Optional[ActivoBase]:
        for activo in self.activos:
            if activo.simbolo.upper() == simbolo.upper():
                return activo
        return None

    def get_historial(self) -> list:
        return self.historial
