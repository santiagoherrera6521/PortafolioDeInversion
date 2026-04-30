# Simulador de Portafolio de Inversión

Proyecto de la materia Estructura de Datos del ITM, 2026.

Es un simuladr de un portafolio de inversiones real: puedes agregar acciones, CDTs y bonos, comprar y vender, y ver cómo va evolucionando tu dinero con el tiempo. Los precios de las acciones son reales y se traen directo de Yahoo Finance con yfinance.

## Integrantes

- Santiago Herrera — Parte 1: activos y datos
- Julian Zapata — Parte 2: motor de transacciones y estructuras de datos
- Integrante 3 — Parte 3: visualización e interfaz

## Cómo correrlo

Primero instalar las dependencias:

```bash
pip install yfinance matplotlib
```

Luego ejecutar:

```bash
python main.py
```

Se pide el capital inicial y aparece el menú. Desde ahí se puede agregar activos, comprar, vender y ver las gráficas.

## Archivos del proyecto

- `interfaces.py` — clases abstractas que definen los contratos del sistema
- `Estructuras.py` — estructuras de datos implementadas desde cero: lista enlazada, pila, cola y matriz
- `Accion.py` — conecta con yfinance para traer precios reales
- `CDT.py` — certifica depósito a término con liquidación diaria de intereses
- `Bonos.py` — bonos con pago de cupones
- `portafolio.py` — toda la lógica de compras, ventas y validaciones
- `moc_data.py` — datos de prueba para cuando no hay internet o las partes no están listas
- `main.py` — menú principal con todas las opciones

## Cómo está dividido el trabajo

Lo más importante del proyecto es que los tres podíamos trabajar al mismo tiempo sin esperar al otro. Para eso creamos dos archivos al inicio (`interfaces.py` y `moc_data.py`) que definen cómo se comunican las partes entre sí. Mientras el compañero de activos no terminaba, usábamos datos falsos del mock, y cuando terminó solo tocó cambiar el import.

## Estructuras de datos utilizadas

Todas las estructuras están hechas desde cero con nodos y punteros, sin usar las de Python directamente.

**Lista enlazada simple** — guarda el historial de transacciones. Cada transacción es un nodo con un puntero al siguiente. Se usa porque el historial crece sin saber cuántas operaciones va a hacer el usuario.

**Pila (LIFO)** — registra las órdenes de compra. La última compra queda en el tope, lo que tiene sentido porque cuando se quiere revisar la operación más reciente se accede en O(1).

**Cola (FIFO)** — registra las órdenes de venta. Las ventas se procesan en el orden en que llegaron, que es el principio contable FIFO.

**Matriz 2D** — guarda el historial de precios. Las filas son los activos y las columnas son las fechas. Permite acceder al precio de cualquier activo en cualquier fecha en tiempo constante.

## Validaciones del motor de transacciones

Antes de ejecutar cualquier compra o venta el sistema verifica:

- Que haya capital suficiente para comprar
- Que haya suficientes unidades del activo para vender
- Que el precio esté dentro del rango mínimo y máximo de la jornada

La comisión del bróker es del 0.5% por operación y se descuenta automáticamente.

## Acciones disponibles

AAPL, MSFT, GOOGL, AMZN, NVDA, TSLA, META, JPM, V, WMT
