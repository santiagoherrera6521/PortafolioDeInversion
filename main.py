import os
import sys
from datetime import date

try:
    from Accion import Accion
    from CDT import CDT
    from Bonos import Bono
    _MODO_REAL = True
except ImportError:
    _MODO_REAL = False

from moc_data import AccionMock, CDTMock, BonoMock, get_historial_precios_mock
from interfaces import ActivoBase
from portafolio import PortafolioReal

# ── Visualizaciones ──────────────────────────────────────────────────────────

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    _MATPLOTLIB = True
except ImportError:
    _MATPLOTLIB = False


def _graficar_evolucion(portafolio: PortafolioReal):
    """Gráfica la evolución histórica del valor del portafolio por jornada."""
    if not _MATPLOTLIB:
        print("  [!] matplotlib no disponible. Instala con: pip install matplotlib")
        return

    historial = portafolio.get_historial_transacciones()
    if not historial:
        print("  [!] Sin transacciones aún — no hay evolución que graficar.")
        return

    # Agrupa por fecha y calcula valor acumulado
    fechas_vistas = []
    valores = []
    fechas_set = sorted(set(t.fecha for t in historial))

    for f in fechas_set:
        fechas_vistas.append(str(f))
        valores.append(portafolio.get_valor_total())  # valor actual

    plt.figure(figsize=(10, 4))
    plt.plot(fechas_vistas, valores, marker="o", color="#2196F3", linewidth=2)
    plt.fill_between(range(len(fechas_vistas)), valores, alpha=0.1, color="#2196F3")
    plt.title("Evolución del valor del portafolio", fontsize=14, fontweight="bold")
    plt.xlabel("Fecha")
    plt.ylabel("Valor total ($)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("evolucion_portafolio.png", dpi=120)
    plt.show()
    print("Gráfica guardada como 'evolucion_portafolio.png'")


def _graficar_composicion(portafolio: PortafolioReal):
    """Gráfica de torta con la composición actual del portafolio."""
    if not _MATPLOTLIB:
        print("matplotlib no disponible.")
        return

    composicion = portafolio.get_composicion()
    if not composicion:
        print("Portafolio vacío — no hay composición que mostrar.")
        return

    labels = list(composicion.keys())
    valores = list(composicion.values())
    colores = ["#2196F3", "#4CAF50", "#FF9800", "#E91E63", "#9C27B0", "#00BCD4"]

    plt.figure(figsize=(7, 7))
    plt.pie(valores, labels=labels, autopct="%1.1f%%",
            colors=colores[:len(labels)], startangle=90,
            wedgeprops=dict(edgecolor="white", linewidth=1.5))
    plt.title("Composición actual del portafolio", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig("composicion_portafolio.png", dpi=120)
    plt.show()
    print("Gráfica guardada como 'composicion_portafolio.png'")


def _graficar_rendimiento_individual(portafolio: PortafolioReal):
    """Barras comparando el rendimiento de cada activo en el portafolio."""
    if not _MATPLOTLIB:
        print("matplotlib no disponible.")
        return

    activos = portafolio.get_activos()
    if not activos:
        print("  [!] No hay activos en el portafolio.")
        return

    tickers = []
    rendimientos = []

    for ticker, activo in activos.items():
        cantidad = portafolio.get_cantidad(ticker)
        if cantidad <= 0:
            continue
        # Busca precio promedio de compra en el historial
        compras = [t for t in portafolio.get_historial_transacciones()
                   if t.ticker == ticker and t.tipo == "compra"]
        if not compras:
            continue
        precio_prom = sum(t.precio for t in compras) / len(compras)
        precio_actual = activo.get_precio_actual()
        rend = round((precio_actual - precio_prom) / precio_prom * 100, 2)
        tickers.append(ticker)
        rendimientos.append(rend)

    if not tickers:
        print("  [!] Sin datos de rendimiento aún.")
        return

    colores = ["#4CAF50" if r >= 0 else "#F44336" for r in rendimientos]
    plt.figure(figsize=(8, 4))
    bars = plt.bar(tickers, rendimientos, color=colores, edgecolor="white", linewidth=1.2)
    plt.axhline(0, color="black", linewidth=0.8, linestyle="--")
    plt.title("Rendimiento individual por activo (%)", fontsize=14, fontweight="bold")
    plt.ylabel("Rendimiento (%)")
    for bar, val in zip(bars, rendimientos):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                 f"{val:+.2f}%", ha="center", va="bottom", fontsize=10)
    plt.tight_layout()
    plt.savefig("rendimiento_activos.png", dpi=120)
    plt.show()
    print("Gráfica guardada como 'rendimiento_activos.png'")


# ── Resumen ────────────────────────────────────────────────────────

def _mostrar_resumen(portafolio: PortafolioReal):
    """Imprime el resumen del portafolio."""
    sep = "─" * 50
    print(f"\n{'═'*50}")
    print(f"  📊  RESUMEN EJECUTIVO DEL PORTAFOLIO")
    print(f"{'═'*50}")
    print(f"  Capital disponible : ${portafolio.get_capital_disponible():>14,.2f}")
    print(f"  Valor total        : ${portafolio.get_valor_total():>14,.2f}")
    print(f"  Rentabilidad       : {portafolio.get_rentabilidad():>+13.2f}%")
    print(f"  Rentabilidad neta  : {portafolio.get_rentabilidad_neta():>+13.2f}%  (incl. dividendos)")
    print(sep)

    activos = portafolio.get_activos()
    composicion = portafolio.get_composicion()

    if activos:
        print("  POSICIONES ACTUALES:")
        for ticker, activo in activos.items():
            cantidad = portafolio.get_cantidad(ticker)
            if cantidad > 0:
                valor = activo.get_precio_actual() * cantidad
                pct = composicion.get(ticker, 0)
                print(f"    {ticker:<12} {cantidad:>6.2f} uds  "
                      f"@ ${activo.get_precio_actual():>8.2f}  "
                      f"= ${valor:>12,.2f}  ({pct:.1f}%)")
        efectivo_pct = composicion.get("efectivo", 0)
        print(f"    {'Efectivo':<12}                    "
              f"  ${portafolio.get_capital_disponible():>12,.2f}  ({efectivo_pct:.1f}%)")
    else:
        print("  Sin posiciones abiertas.")

    print(sep)
    historial = portafolio.get_historial_transacciones()
    if historial:
        print(f"  ÚLTIMAS 5 TRANSACCIONES:")
        for t in historial[-5:]:
            print(f"    {t}")
    print(f"{'═'*50}\n")


# ── CLI principal ────────────────────────────────────────────────────────────

def _crear_activo(modo_real: bool):
    """Asistente para añadir un activo al portafolio."""
    print("\n  Tipo de activo:")
    print("    1) Acción (bolsa)")
    print("    2) CDT")
    print("    3) Bono")
    tipo = input("  Opción: ").strip()

    if tipo == "1":
        ticker = input("  Ticker (e.g. AAPL, MSFT, NVDA): ").strip().upper()
        try:
            if modo_real:
                return ticker, Accion(ticker)
            else:
                return ticker, AccionMock(ticker)
        except Exception as e:
            print(f" Error: {e}")
            return None, None

    elif tipo == "2":
        nombre = input("  Nombre del CDT (e.g. CDT_BANCOLOMBIA): ").strip()
        capital = float(input("  Capital invertido ($): ").strip())
        tasa = float(input("  Tasa E.A. (e.g. 0.12 para 12%): ").strip())
        if modo_real:
            plazo = int(input("  Plazo en días: ").strip())
            return nombre, CDT(nombre, capital, tasa, date.today(), plazo)
        else:
            return nombre, CDTMock(nombre, capital, tasa)

    elif tipo == "3":
        nombre = input("  Nombre del bono (e.g. TES_2026): ").strip()
        nominal = float(input("  Valor nominal ($): ").strip())
        tasa = float(input("  Tasa cupón anual (e.g. 0.10): ").strip())
        if modo_real:
            plazo = int(input("  Plazo en días: ").strip())
            return nombre, Bono(nombre, nominal, tasa, date.today(), plazo)
        else:
            return nombre, BonoMock(nombre, nominal, tasa)

    else:
        print("  Opción inválida.")
        return None, None


def main():
    os.system("cls" if os.name == "nt" else "clear")
    print("║     PORTAFOLIO DE INVERSIÓN        ║")
    print("║    Estructura de Datos — 2026        ║")

    modo = "REAL" if _MODO_REAL else "MOCK"
    print(f"  Modo: {modo}")

    capital = input("\n  Capital inicial ($): ").strip()
    try:
        capital = float(capital)
    except ValueError:
        capital = 1_000_000
        print(f"  Usando capital por defecto: ${capital:,.0f}")

    portafolio = PortafolioReal(capital)

    # Cargar activos mock por defecto si estamos en modo mock
    if not _MODO_REAL:
        print("\n  Cargando activos de demostración (mock)...")
        portafolio.activos = {
            "AAPL": AccionMock("AAPL"),
            "MSFT": AccionMock("MSFT"),
            "NVDA": AccionMock("NVDA"),
        }
        portafolio.cantidades = {k: 0 for k in portafolio.activos}

    MENU = """
  ┌─────────────────────────────────────┐
  │  1) Añadir activo al portafolio     │
  │  2) Comprar                         │
  │  3) Vender                          │
  │  4) Ver resumen ejecutivo           │
  │  5) Gráfica evolución del portafolio│
  │  6) Gráfica composición             │
  │  7) Gráfica rendimiento por activo  │
  │  0) Salir                           │
  └─────────────────────────────────────┘
  Opción: """

    while True:
        try:
            opcion = input(MENU).strip()

            if opcion == "0":
                print("\n  ¡Hasta luego! \n")
                break

            elif opcion == "1":
                ticker, activo = _crear_activo(_MODO_REAL)
                if activo:
                    portafolio.activos[ticker] = activo
                    portafolio.cantidades.setdefault(ticker, 0)
                    print(f"  {activo.get_nombre()} añadido. Precio actual: ${activo.get_precio_actual():,.2f}")

            elif opcion == "2":
                if not portafolio.activos:
                    print("  [!] Primero añade activos (opción 1).")
                    continue
                print("  Activos disponibles:", list(portafolio.activos.keys()))
                ticker = input("  Ticker a comprar: ").strip().upper()
                if ticker not in portafolio.activos:
                    print("  ❌ Ticker no encontrado.")
                    continue
                cantidad = float(input("  Cantidad: ").strip())
                try:
                    t = portafolio.comprar(ticker, cantidad)
                    print(f"  {t}")
                except ValueError as e:
                    print(f"  {e}")

            elif opcion == "3":
                tickers_con_posicion = [k for k, v in portafolio.cantidades.items() if v > 0]
                if not tickers_con_posicion:
                    print("  No tienes posiciones abiertas para vender.")
                    continue
                print("  Posiciones abiertas:", tickers_con_posicion)
                ticker = input("  Ticker a vender: ").strip().upper()
                if ticker not in portafolio.activos:
                    print("  Ticker no encontrado.")
                    continue
                cantidad = float(input("  Cantidad: ").strip())
                try:
                    t = portafolio.vender(ticker, cantidad)
                    print(f"  {t}")
                except ValueError as e:
                    print(f"  {e}")

            elif opcion == "4":
                _mostrar_resumen(portafolio)

            elif opcion == "5":
                _graficar_evolucion(portafolio)

            elif opcion == "6":
                _graficar_composicion(portafolio)

            elif opcion == "7":
                _graficar_rendimiento_individual(portafolio)

            else:
                print("  Opción no válida.")

        except KeyboardInterrupt:
            print("\n\n  Interrumpido. ¡Hasta luego!\n")
            break
        except Exception as e:
            print(f"  Error inesperado: {e}")


if __name__ == "__main__":
    main()
