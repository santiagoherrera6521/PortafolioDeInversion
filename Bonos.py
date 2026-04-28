from datetime import date
from interfaces import ActivoBase


class Bono(ActivoBase):
    def __init__(self, simbolo: str, nombre: str, valor_nominal: float,
                 cantidad: int, tasa_cupon: float, frecuencia_cupon: int,
                 plazo_dias: int, precio_mercado: float = None):
        """
        Args:
            simbolo:           Identificador, ej: 'TES_2026'
            nombre:            Descripción, ej: 'TES Tasa Fija 2026'
            valor_nominal:     Valor facial de cada bono (ej: 1_000_000).
            cantidad:          Número de bonos en cartera.
            tasa_cupon:        Tasa del cupón anual en decimal (ej: 0.08 para 8%).
            frecuencia_cupon:  Veces que paga cupón al año (1=anual, 2=semestral, 4=trimestral).
            plazo_dias:        Duración total del bono en días.
            precio_mercado:    Precio actual en mercado secundario por bono.
                               Si es None, se asume igual al valor nominal (par).
        """
        precio_compra = precio_mercado or valor_nominal
        super().__init__(
            simbolo=simbolo,
            nombre=nombre,
            cantidad=cantidad,
            precio_compra=precio_compra
        )
        self.valor_nominal = valor_nominal
        self.tasa_cupon = tasa_cupon
        self.frecuencia_cupon = frecuencia_cupon
        self.plazo_dias = plazo_dias
        self.fecha_vencimiento = date.fromordinal(
            self.fecha_compra.toordinal() + plazo_dias
        )
        self._precio_mercado = precio_mercado or valor_nominal
    def _dias_transcurridos(self) -> int:
        return min((date.today() - self.fecha_compra).days, self.plazo_dias)

    def _dias_por_periodo_cupon(self) -> int:
        """Días entre cada pago de cupón."""
        return 365 // self.frecuencia_cupon

    def _cupones_pagados(self) -> int:
        """Número de cupones que ya se han pagado."""
        return self._dias_transcurridos() // self._dias_por_periodo_cupon()

    def _cupon_por_bono(self) -> float:
        """Monto de cada cupón por bono."""
        return self.valor_nominal * (self.tasa_cupon / self.frecuencia_cupon)
    def get_precio_actual(self) -> float:
        """Precio de mercado actual por bono."""
        return self._precio_mercado

    def get_precio_minimo_jornada(self) -> float:
        """Simulación: el mínimo es 0.5% menos que el precio actual."""
        return self._precio_mercado * 0.995

    def get_precio_maximo_jornada(self) -> float:
        """Simulación: el máximo es 0.5% más que el precio actual."""
        return self._precio_mercado * 1.005

    def get_dividendos_acumulados(self) -> float:
        """
        Total de cupones cobrados desde la compra.
        cupones_pagados × monto_cupon × cantidad_bonos
        """
        return self._cupones_pagados() * self._cupon_por_bono() * self.cantidad
    def actualizar_precio_mercado(self, nuevo_precio: float):
        """
        Actualiza el precio de mercado del bono.
        En producción este valor vendría de una fuente de datos externa.
        """
        self._precio_mercado = nuevo_precio

    def get_dias_restantes(self) -> int:
        return max(0, self.plazo_dias - self._dias_transcurridos())

    def get_cupon_siguiente(self) -> float:
        """Monto del próximo cupón a cobrar (por toda la posición)."""
        return self._cupon_por_bono() * self.cantidad

    def get_rendimiento_al_vencimiento(self) -> float:
        """
        Estimación simple del YTM (Yield to Maturity).
        Fórmula aproximada: (cupón_anual + (nominal - precio) / años) / ((nominal + precio) / 2)
        """
        anos_restantes = self.get_dias_restantes() / 365
        if anos_restantes <= 0:
            return 0.0
        cupon_anual = self.valor_nominal * self.tasa_cupon
        ytm = (cupon_anual + (self.valor_nominal - self._precio_mercado) / anos_restantes) \
              / ((self.valor_nominal + self._precio_mercado) / 2)
        return ytm

    def esta_vencido(self) -> bool:
        return date.today() >= self.fecha_vencimiento

    def __str__(self):
        freq_texto = {1: "Anual", 2: "Semestral", 4: "Trimestral"}.get(
            self.frecuencia_cupon, f"{self.frecuencia_cupon}x/año"
        )
        estado = "VENCIDO" if self.esta_vencido() else f"{self.get_dias_restantes()} días restantes"
        return (
            f"{'─'*48}\n"
            f"  {self.simbolo} · {self.nombre}\n"
            f"{'─'*48}\n"
            f"  Cantidad           : {self.cantidad:>11} bonos\n"
            f"  Valor nominal c/u  : ${self.valor_nominal:>12,.0f}\n"
            f"  Tasa cupón         : {self.tasa_cupon*100:>11.2f}% ({freq_texto})\n"
            f"  Estado             : {estado:>20}\n"
            f"  Precio de mercado  : ${self._precio_mercado:>12,.0f}\n"
            f"  Valor posición     : ${self.get_valor_actual():>12,.0f}\n"
            f"  Cupones cobrados   : {self._cupones_pagados():>11}\n"
            f"  Cupones acumulados : ${self.get_dividendos_acumulados():>12,.0f}\n"
            f"  Próximo cupón      : ${self.get_cupon_siguiente():>12,.0f}\n"
            f"  YTM estimado       : {self.get_rendimiento_al_vencimiento()*100:>+10.2f}%\n"
            f"  Rentabilidad       : {self.get_rentabilidad_porcentual():>+10.2f}%\n"
            f"{'─'*48}"
        )
