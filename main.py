import os
from datetime import date

# Importar modulos

from Interfaces import ActivoBase, PortafolioBase
from moc_data import ActivoMock, PortafolioMock, crear_portafolio_mock

try:
    from portafolio import PortafolioReal
    _TIENE_PORTAFOLIO_REAL = True
except Exception:
    _TIENE_PORTAFOLIO_REAL = False

# Activos
try:
    from Accion import Accion
    _TIENE_ACCION = True
except Exception:
    _TIENE_ACCION = False

try:
    from CDT import CDT
    _TIENE_CDT = True
except Exception:
    _TIENE_CDT = False

try:
    from Bonos import Bono
    _TIENE_BONO = True
except Exception:
    _TIENE_BONO = False

_MODO_REAL = _TIENE_ACCION and _TIENE_CDT and _TIENE_BONO

# Matplotlib

try:
    import matplotlib.pyplot as plt
    _MATPLOTLIB = True
except ImportError:
    _MATPLOTLIB = False

# VISUALIZACIONES

def _graficar_evolucion(portafolio):
    """Gráfica la evolución del valor del portafolio por transacción."""
    if not _MATPLOTLIB:
        print("Instala matplotlib: pip install matplotlib")
        return

    historial = portafolio.get_historial()
    if not historial:
        print("Sin transacciones aún — realiza al menos una compra primero.")
        return

    # Reconstruye el valor acumulado transacción por transacción
    etiquetas = []
    valores = []
    for i, t in enumerate(historial):
        etiquetas.append(f"T{i+1}\n{t['tipo']}\n{t['simbolo']}")
        valores.append(portafolio.get_valor_total())

    plt.figure(figsize=(10, 4))
    plt.plot(range(len(valores)), valores, marker="o", color="#2196F3", linewidth=2)
    plt.fill_between(range(len(valores)), valores, alpha=0.1, color="#2196F3")
    plt.title("Evolución del valor del portafolio", fontsize=14, fontweight="bold")
    plt.xlabel("Transacciones")
    plt.ylabel("Valor total ($)")
    plt.xticks(range(len(etiquetas)), etiquetas, fontsize=8)
    plt.tight_layout()
    plt.savefig("evolucion_portafolio.png", dpi=120)
    plt.show()
    print("Guardada como 'evolucion_portafolio.png'")


def _graficar_composicion(portafolio):
    """Pie chart con la composición actual del portafolio."""
    if not _MATPLOTLIB:
        print("Instala matplotlib: pip install matplotlib")
        return

    activos = [a for a in portafolio.activos if a.cantidad > 0]
    if not activos:
        print("No hay activos con posición abierta.")
        return

    valor_total = portafolio.get_valor_total()
    labels = []
    valores = []

    for a in activos:
        labels.append(a.simbolo)
        valores.append(a.get_valor_actual())

    # Agregar efectivo
    if portafolio.capital_disponible > 0:
        labels.append("Efectivo")
        valores.append(portafolio.capital_disponible)

    colores = ["#2196F3", "#4CAF50", "#FF9800", "#E91E63", "#9C27B0", "#00BCD4", "#795548"]

    plt.figure(figsize=(7, 7))
    plt.pie(valores, labels=labels, autopct="%1.1f%%",
            colors=colores[:len(labels)], startangle=90,
            wedgeprops=dict(edgecolor="white", linewidth=1.5))
    plt.title("Composición actual del portafolio", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig("composicion_portafolio.png", dpi=120)
    plt.show()
    print("  ✅ Guardada como 'composicion_portafolio.png'")


def _graficar_rendimiento_individual(portafolio):
    if not _MATPLOTLIB:
        print("  [!] Instala matplotlib: pip install matplotlib")
        return

    activos_con_posicion = [a for a in portafolio.activos if a.cantidad > 0]
    if not activos_con_posicion:
        print("  [!] No hay posiciones abiertas para graficar.")
        return

    tickers = [a.simbolo for a in activos_con_posicion]
    rendimientos = [a.get_rentabilidad_porcentual() for a in activos_con_posicion]
    colores = ["#4CAF50" if r >= 0 else "#F44336" for r in rendimientos]

    plt.figure(figsize=(8, 4))
    bars = plt.bar(tickers, rendimientos, color=colores, edgecolor="white", linewidth=1.2)
    plt.axhline(0, color="black", linewidth=0.8, linestyle="--")
    plt.title("Rendimiento individual por activo (%)", fontsize=14, fontweight="bold")
    plt.ylabel("Rendimiento (%)")
    for bar, val in zip(bars, rendimientos):
        plt.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 0.1 if val >= 0 else bar.get_height() - 0.5,
                 f"{val:+.2f}%", ha="center", va="bottom", fontsize=10)
    plt.tight_layout()
    plt.savefig("rendimiento_activos.png", dpi=120)
    plt.show()
    print("Guardada como 'rendimiento_activos.png'")

# RESUMEN EJECUTIVO

def _mostrar_resumen(portafolio):
    sep = "─" * 52
    print(f"\n{'═'*52}")
    print(f" RESUMEN DEL PORTAFOLIO")
    print(f"{'═'*52}")
    print(f"  Capital disponible   : ${portafolio.capital_disponible:>14,.2f}")
    print(f"  Valor total activos  : ${portafolio.get_valor_activos():>14,.2f}")
    print(f"  Valor total portafolio: ${portafolio.get_valor_total():>13,.2f}")
    print(f"  Rentabilidad total   : {portafolio.get_rentabilidad_total():>+13.2f}%")
    print(f"  Dividendos totales   : ${portafolio.get_dividendos_totales():>14,.2f}")
    print(sep)

    activos_con_posicion = [a for a in portafolio.activos if a.cantidad > 0]
    if activos_con_posicion:
        print("  POSICIONES ACTUALES:")
        for a in activos_con_posicion:
            print(f"    {a.simbolo:<12} {a.cantidad:>6} uds  "
                  f"@ ${a.get_precio_actual():>10,.2f}  "
                  f"= ${a.get_valor_actual():>12,.2f}  "
                  f"({a.get_rentabilidad_porcentual():>+.2f}%)")
    else:
        print("  Sin posiciones abiertas.")

    print(sep)
    historial = portafolio.get_historial()
    if historial:
        print(f"  ÚLTIMAS 5 TRANSACCIONES:")
        for t in historial[-5:]:
            print(f"    [{t['tipo']}] {t['simbolo']} — cant: {t['cantidad']} "
                  f"@ ${t['precio']:,.2f} | comisión: ${t['comision']:,.2f}")
    print(f"{'═'*52}\n")


# CLI

def _agregar_activo(portafolio):
    """Añade un activo al portafolio."""
    print("\n  Tipo de activo:")
    print("    1) Acción (bolsa)")
    print("    2) CDT")
    print("    3) Bono")
    print("    4) Activo mock (para pruebas)")
    tipo = input("  Opción: ").strip()

    try:
        if tipo == "1":
            if not _TIENE_ACCION:
                print("Accion.py no disponible. Usa opción 4 para mock.")
                return
            ticker = input("Ticker (ej: AAPL, MSFT, NVDA): ").strip().upper()
            activo = Accion(ticker)
            portafolio.activos.append(activo)
            print(f" {activo.nombre} añadido — precio: ${activo.get_precio_actual():,.2f}")

        elif tipo == "2":
            if not _TIENE_CDT:
                print("CDT.py no disponible. Usa opción 4 para mock.")
                return
            simbolo = input("  Símbolo (ej: CDT_BC): ").strip()
            nombre  = input("  Nombre (ej: CDT Bancolombia 12m): ").strip()
            capital = float(input("  Capital ($): ").strip())
            tasa    = float(input("  Tasa anual (ej: 0.12 para 12%): ").strip())
            plazo   = int(input("  Plazo en días: ").strip())
            activo = CDT(simbolo, nombre, capital, tasa, plazo)
            portafolio.activos.append(activo)
            print(f" {activo.nombre} añadido.")

        elif tipo == "3":
            if not _TIENE_BONO:
                print("Bonos.py no disponible. Usa opción 4 para mock.")
                return
            simbolo   = input("  Símbolo (ej: TES_2026): ").strip()
            nombre    = input("  Nombre (ej: TES Tasa Fija 2026): ").strip()
            nominal   = float(input("  Valor nominal por bono ($): ").strip())
            cantidad  = int(input("  Cantidad de bonos: ").strip())
            tasa      = float(input("  Tasa cupón anual (ej: 0.08): ").strip())
            frecuencia= int(input("  Frecuencia cupón al año (1=anual, 2=semestral): ").strip())
            plazo     = int(input("  Plazo en días: ").strip())
            activo = Bono(simbolo, nombre, nominal, cantidad, tasa, frecuencia, plazo)
            portafolio.activos.append(activo)
            print(f" {activo.nombre} añadido.")

        elif tipo == "4":
            print("  Activos mock disponibles: AAPL, MSFT, GOOGL, AMZN, NVDA, CDT_1, BONO_1")
            from moc_data import ACTIVOS_MOCK
            simbolo = input("  Símbolo a agregar: ").strip().upper()
            encontrado = next((a for a in ACTIVOS_MOCK if a.simbolo == simbolo), None)
            if encontrado:
                portafolio.activos.append(encontrado)
                print(f" {encontrado.nombre} añadido — precio: ${encontrado.get_precio_actual():,.2f}")
            else:
                print(" Símbolo no encontrado en mock.")
        else:
            print("  Opción inválida.")

    except Exception as e:
        print(f" Error al agregar activo: {e}")


def _comprar(portafolio):
    if not portafolio.activos:
        print(" Primero añade activos (opción 1).")
        return
    print("  Activos disponibles:")
    for a in portafolio.activos:
        print(f"    {a.simbolo} — ${a.get_precio_actual():,.2f}")
    simbolo  = input("  Símbolo a comprar: ").strip().upper()
    cantidad = float(input("  Cantidad: ").strip())
    precio   = float(input(f"  Precio de compra ($): ").strip())
    ok = portafolio.comprar(simbolo, cantidad, precio)
    if ok:
        print(f" Compra ejecutada: {cantidad} x {simbolo} @ ${precio:,.2f}")


def _vender(portafolio):
    con_posicion = [a for a in portafolio.activos if a.cantidad > 0]
    if not con_posicion:
        print("No tienes posiciones abiertas.")
        return
    print("  Posiciones abiertas:")
    for a in con_posicion:
        print(f"    {a.simbolo} — {a.cantidad} uds @ ${a.get_precio_actual():,.2f}")
    simbolo  = input("  Símbolo a vender: ").strip().upper()
    cantidad = float(input("  Cantidad: ").strip())
    precio   = float(input("  Precio de venta ($): ").strip())
    ok = portafolio.vender(simbolo, cantidad, precio)
    if ok:
        print(f" Venta ejecutada: {cantidad} x {simbolo} @ ${precio:,.2f}")


def main():
    os.system("cls" if os.name == "nt" else "clear")
    print("╔══════════════════════════════════════════╗")
    print("║     💼  PORTAFOLIO DE INVERSIÓN  💼      ║")
    print("║        Estructura de Datos — 2026        ║")
    print("╚══════════════════════════════════════════╝")
    print(f"  Modo: {'REAL ✅' if _MODO_REAL else 'MOCK 🧪'}")

    capital = input("\n  Capital inicial ($): ").strip()
    try:
        capital = float(capital)
    except ValueError:
        capital = 500_000
        print(f"  Usando capital por defecto: ${capital:,.0f}")

    # Usamos PortafolioMock porque es compatible con interfaces.py real
    portafolio = PortafolioMock(capital_inicial=capital)

    MENU = """
  ┌─────────────────────────────────────┐
  │  1) Añadir activo al portafolio     │
  │  2) Comprar                         │
  │  3) Vender                          │
  │  4) Ver resumen ejecutivo           │
  │  5) Gráfica evolución               │
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
                _agregar_activo(portafolio)
            elif opcion == "2":
                _comprar(portafolio)
            elif opcion == "3":
                _vender(portafolio)
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
            print("\n\n  Interrumpido. ¡Hasta luego! \n")
            break
        except Exception as e:
            print(f"  Error inesperado: {e}")


if __name__ == "__main__":
    main()
