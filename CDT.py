from datetime import date
from interfaces import ActivoBase

class CDT(ActivoBase):
    #constructor
    def __init__ (self, simbolo: str, nombre:str, capital: float, tasa_anual: float, plazo_dias: int):
        super().__init__(
            simbolo=simbolo,
            nombre=nombre,
            cantidad=1,
            precio_compra=capital
            )
        self.capital=capital
        self.tasa_anual=tasa_anual
        self.plazo_dias=plazo_dias
        self.fecha_vencimiento= date.fromordinal(
            self.fecha_compra.toordinal()+plazo_dias
        )
    # funciones privadas
    def _dias_transcurridos(self) -> int:
        dias = (date.today() - self.fecha_compra).days
        return min(dias, self.plazo_dias)
    def _interes_diario(self) -> float:
        return self.capital * (self.tasa_anual /365)
    #funciones para ActivoBase
    def get_precio_actual(self) -> float:
        dias_ayer = max(0, self._dias_transcurridos()-1)
        return self.capital + (self._interes_diario()* dias_ayer)
    def get_precio_minimo_jornada(self) -> float:
        dias_ayer= max(0, self._dias_transcurridos()-1)
        return self.capital + (self._interes_diario()*dias_ayer)
    def get_precio_maximo_jornada(self) -> float:
        return self.get_precio_actual
    def get_dividendos_acumulados(self) -> float:
        return self._interes_diario() * self._dias_transcurridos()
    # funciones para determinar si el codigo esta vigente
    def get_dias_restantes(self) -> int:
        return max(0, self.plazo_dias - self._dias_transcurridos)
    def get_interes_total_esperado (self) -> float:
        return self._interes_diario () * self.plazo_dias
    def esta_vencido (self) -> bool:
        return date.today() >= self.fecha_vencimiento
    def __str__(self):
        estado = "vencido" if self.esta_vencido () else f"{self.get_dias_restantes()} días restantes"
        return (
            f"{'─'*48}\n"
            f"  {self.simbolo} · {self.nombre}\n"
            f"{'─'*48}\n"
            f"  Capital invertido  : ${self.capital:>12,.0f}\n"
            f"  Tasa anual         : {self.tasa_anual*100:>11.2f}%\n"
            f"  Plazo              : {self.plazo_dias:>11} días\n"
            f"  Estado             : {estado:>20}\n"
            f"  Interés por día    : ${self._interes_diario():>12,.0f}\n"
            f"  Intereses acum.    : ${self.get_dividendos_acumulados():>12,.0f}\n"
            f"  Valor actual       : ${self.get_precio_actual():>12,.0f}\n"
            f"  Rentabilidad       : {self.get_rentabilidad_porcentual():>+10.2f}%\n"
            f"  Interés al venc.   : ${self.get_interes_total_esperado():>12,.0f}\n"
            f"{'─'*48}"
        )
    
