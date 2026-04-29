
from Interfaces import ActivoBase, PortafolioBase


class ActivoMock(ActivoBase):
    def __init__(self, simbolo, nombre, cantidad, precio_compra,
                 precio_actual=None, dividendos=0.0):
        super().__init__(simbolo, nombre, cantidad, precio_compra)
        self._precio_actual = precio_actual or precio_compra
        self._dividendos = dividendos

    def get_precio_actual(self):
        return self._precio_actual

    def get_precio_minimo_jornada(self):
        return round(self._precio_actual * 0.98, 2)

    def get_precio_maximo_jornada(self):
        return round(self._precio_actual * 1.02, 2)

    def get_dividendos_acumulados(self):
        return self._dividendos

    def __str__(self):
        return (
            f"  {self.simbolo:10} | cant: {self.cantidad:6} "
            f"| precio: ${self.get_precio_actual():>12,.2f} "
            f"| valor: ${self.get_valor_actual():>12,.2f} "
            f"| rent: {self.get_rentabilidad_porcentual():>+6.2f}%"
        )
class PortafolioMock(PortafolioBase):
    COMISION = 0.001
    def comprar(self, simbolo: str, cantidad: float, precio: float) -> bool:
        activo = self.buscar_activo(simbolo)
        if not activo:
            print(f"  [Mock] Activo {simbolo} no encontrado.")
            return False
        if not (activo.get_precio_minimo_jornada() <= precio <= activo.get_precio_maximo_jornada()):
            print(f"  [Mock] Precio fuera del rango de jornada.")
            return False
        costo = cantidad * precio * (1 + self.COMISION)
        if costo > self.capital_disponible:
            print(f"  [Mock] Capital insuficiente.")
            return False
        self.capital_disponible -= costo
        activo.cantidad += cantidad
        self.historial.append({
            "tipo": "COMPRA", "simbolo": simbolo,
            "cantidad": cantidad, "precio": precio,
            "comision": cantidad * precio * self.COMISION
        })
        return True

    def vender(self, simbolo: str, cantidad: float, precio: float) -> bool:
        activo = self.buscar_activo(simbolo)
        if not activo:
            print(f"  [Mock] Activo {simbolo} no encontrado.")
            return False
        if cantidad > activo.cantidad:
            print(f"  [Mock] Cantidad insuficiente.")
            return False
        if not (activo.get_precio_minimo_jornada() <= precio <= activo.get_precio_maximo_jornada()):
            print(f"  [Mock] Precio fuera del rango de jornada.")
            return False
        ingreso = cantidad * precio * (1 - self.COMISION)
        self.capital_disponible += ingreso
        activo.cantidad -= cantidad
        self.historial.append({
            "tipo": "VENTA", "simbolo": simbolo,
            "cantidad": cantidad, "precio": precio,
            "comision": cantidad * precio * self.COMISION
        })
        return True

ACTIVOS_MOCK = [
    ActivoMock("AAPL",   "Apple Inc.",          10,  150.00,  178.50, dividendos=8.50),
    ActivoMock("MSFT",   "Microsoft Corp.",       5,  280.00,  310.20, dividendos=12.00),
    ActivoMock("GOOGL",  "Alphabet Inc.",         3,  120.00,  135.70, dividendos=0.00),
    ActivoMock("AMZN",   "Amazon.com Inc.",       8,  178.00,  182.30, dividendos=0.00),
    ActivoMock("NVDA",   "NVIDIA Corp.",          6,  450.00,  620.10, dividendos=2.40),
    ActivoMock("CDT_1",  "CDT Bancolombia 12m",   1, 5000000, 5041095, dividendos=41095),
    ActivoMock("BONO_1", "TES Tasa Fija 2026",    2, 1000000, 1015000, dividendos=25000),
]

CAPITAL_INICIAL_MOCK = 500_000.0


def crear_portafolio_mock() -> PortafolioMock:
    p = PortafolioMock(capital_inicial=CAPITAL_INICIAL_MOCK)
    p.activos = ACTIVOS_MOCK[:]
    return p

from Interfaces import ActivoBase, PortafolioBase


class ActivoMock(ActivoBase):
    def __init__(self, simbolo, nombre, cantidad, precio_compra,
                 precio_actual=None, dividendos=0.0):
        super().__init__(simbolo, nombre, cantidad, precio_compra)
        self._precio_actual = precio_actual or precio_compra
        self._dividendos = dividendos

    def get_precio_actual(self):
        return self._precio_actual

    def get_precio_minimo_jornada(self):
        return round(self._precio_actual * 0.98, 2)

    def get_precio_maximo_jornada(self):
        return round(self._precio_actual * 1.02, 2)

    def get_dividendos_acumulados(self):
        return self._dividendos

    def __str__(self):
        return (
            f"  {self.simbolo:10} | cant: {self.cantidad:6} "
            f"| precio: ${self.get_precio_actual():>12,.2f} "
            f"| valor: ${self.get_valor_actual():>12,.2f} "
            f"| rent: {self.get_rentabilidad_porcentual():>+6.2f}%"
        )
class PortafolioMock(PortafolioBase):
    COMISION = 0.001
    def comprar(self, simbolo: str, cantidad: float, precio: float) -> bool:
        activo = self.buscar_activo(simbolo)
        if not activo:
            print(f"  [Mock] Activo {simbolo} no encontrado.")
            return False
        if not (activo.get_precio_minimo_jornada() <= precio <= activo.get_precio_maximo_jornada()):
            print(f"  [Mock] Precio fuera del rango de jornada.")
            return False
        costo = cantidad * precio * (1 + self.COMISION)
        if costo > self.capital_disponible:
            print(f"  [Mock] Capital insuficiente.")
            return False
        self.capital_disponible -= costo
        activo.cantidad += cantidad
        self.historial.append({
            "tipo": "COMPRA", "simbolo": simbolo,
            "cantidad": cantidad, "precio": precio,
            "comision": cantidad * precio * self.COMISION
        })
        return True

    def vender(self, simbolo: str, cantidad: float, precio: float) -> bool:
        activo = self.buscar_activo(simbolo)
        if not activo:
            print(f"  [Mock] Activo {simbolo} no encontrado.")
            return False
        if cantidad > activo.cantidad:
            print(f"  [Mock] Cantidad insuficiente.")
            return False
        if not (activo.get_precio_minimo_jornada() <= precio <= activo.get_precio_maximo_jornada()):
            print(f"  [Mock] Precio fuera del rango de jornada.")
            return False
        ingreso = cantidad * precio * (1 - self.COMISION)
        self.capital_disponible += ingreso
        activo.cantidad -= cantidad
        self.historial.append({
            "tipo": "VENTA", "simbolo": simbolo,
            "cantidad": cantidad, "precio": precio,
            "comision": cantidad * precio * self.COMISION
        })
        return True

ACTIVOS_MOCK = [
    ActivoMock("AAPL",   "Apple Inc.",          10,  150.00,  178.50, dividendos=8.50),
    ActivoMock("MSFT",   "Microsoft Corp.",       5,  280.00,  310.20, dividendos=12.00),
    ActivoMock("GOOGL",  "Alphabet Inc.",         3,  120.00,  135.70, dividendos=0.00),
    ActivoMock("AMZN",   "Amazon.com Inc.",       8,  178.00,  182.30, dividendos=0.00),
    ActivoMock("NVDA",   "NVIDIA Corp.",          6,  450.00,  620.10, dividendos=2.40),
    ActivoMock("CDT_1",  "CDT Bancolombia 12m",   1, 5000000, 5041095, dividendos=41095),
    ActivoMock("BONO_1", "TES Tasa Fija 2026",    2, 1000000, 1015000, dividendos=25000),
]

CAPITAL_INICIAL_MOCK = 500_000.0


def crear_portafolio_mock() -> PortafolioMock:
    p = PortafolioMock(capital_inicial=CAPITAL_INICIAL_MOCK)
    p.activos = ACTIVOS_MOCK[:]
    return p
