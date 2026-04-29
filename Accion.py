from datetime import date
import yfinance as yf
from interfaces import ActivoBase


ACCIONES_DISPONIBLES = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA",
    "TSLA", "META", "JPM", "V", "WMT"
]


class Accion(ActivoBase):

    def __init__(self, simbolo: str, cantidad: float = 0, precio_compra: float = None):
        self._ticker_obj = yf.Ticker(simbolo)
        try:
            info = self._ticker_obj.info
            nombre = info.get("longName") or info.get("shortName") or simbolo
        except Exception:
            nombre = simbolo
        if precio_compra is None:
            precio_compra = self._obtener_precio_cierre()
        super().__init__(
            simbolo=simbolo.upper(),
            nombre=nombre,
            cantidad=cantidad,
            precio_compra=precio_compra
        )

    def _obtener_precio_cierre(self) -> float:
        try:
            hist = self._ticker_obj.history(period="1d")
            if not hist.empty:
                return round(float(hist["Close"].iloc[-1]), 2)
        except Exception:
            pass
        return 0.0

    def _obtener_historial(self, periodo: str = "1mo"):
        try:
            return self._ticker_obj.history(period=periodo)
        except Exception:
            return []

    def get_precio_actual(self) -> float:
        return self._obtener_precio_cierre()

    def get_precio_minimo_jornada(self) -> float:
        try:
            hist = self._ticker_obj.history(period="1d")
            if not hist.empty:
                return round(float(hist["Low"].iloc[-1]), 2)
        except Exception:
            pass
        return round(self._obtener_precio_cierre() * 0.98, 2)

    def get_precio_maximo_jornada(self) -> float:
        try:
            hist = self._ticker_obj.history(period="1d")
            if not hist.empty:
                return round(float(hist["High"].iloc[-1]), 2)
        except Exception:
            pass
        return round(self._obtener_precio_cierre() * 1.02, 2)

    def get_dividendos_acumulados(self) -> float:
        try:
            divs = self._ticker_obj.dividends
            if divs.empty:
                return 0.0
            divs_desde_compra = divs[divs.index.date >= self.fecha_compra]
            return round(float(divs_desde_compra.sum()) * self.cantidad, 2)
        except Exception:
            return 0.0

    def get_dividendo_anual(self) -> float:
        try:
            divs = self._ticker_obj.dividends
            if divs.empty:
                return 0.0
            return round(float(divs.tail(4).sum()), 2)
        except Exception:
            return 0.0

    def get_precio_historico(self, periodo: str = "3mo") -> list:
        try:
            hist = self._obtener_historial(periodo)
            if not hist.empty:
                return [
                    (row.Index.date(), round(float(row.Close), 2))
                    for row in hist.itertuples()
                ]
        except Exception:
            pass
        return []

    def __str__(self):
        return (
            f"{'─'*48}\n"
            f"  {self.simbolo} · {self.nombre}\n"
            f"{'─'*48}\n"
            f"  Cantidad           : {self.cantidad:>11.0f} acciones\n"
            f"  Precio compra      : ${self.precio_compra:>12,.2f}\n"
            f"  Precio actual      : ${self.get_precio_actual():>12,.2f}\n"
            f"  Mínimo jornada     : ${self.get_precio_minimo_jornada():>12,.2f}\n"
            f"  Máximo jornada     : ${self.get_precio_maximo_jornada():>12,.2f}\n"
            f"  Valor posición     : ${self.get_valor_actual():>12,.2f}\n"
            f"  Dividendo anual    : ${self.get_dividendo_anual():>12,.2f}\n"
            f"  Rentabilidad       : {self.get_rentabilidad_porcentual():>+10.2f}%\n"
            f"{'─'*48}"
        )


if __name__ == "__main__":
    print("Acciones disponibles:", ACCIONES_DISPONIBLES)
    print("\nCargando AAPL...")
    a = Accion("AAPL", cantidad=10)
    print(a)
