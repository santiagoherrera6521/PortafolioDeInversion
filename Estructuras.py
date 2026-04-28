from datetime import date


class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class ListaEnlazada:
    def __init__(self):
        self.head = None
        self._tamanio = 0

    def agregar_al_final(self, dato):
        nuevo = Nodo(dato)
        if self.head is None:
            self.head = nuevo
        else:
            actual = self.head
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self._tamanio += 1

    def obtener_todos(self) -> list:
        resultado = []
        actual = self.head
        while actual is not None:
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado

    def buscar(self, condicion) -> list:
        resultado = []
        actual = self.head
        while actual is not None:
            if condicion(actual.dato):
                resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado

    def tamanio(self) -> int:
        return self._tamanio

    def esta_vacia(self) -> bool:
        return self.head is None

    def __repr__(self):
        elementos = self.obtener_todos()
        return " → ".join(str(e) for e in elementos) + " → None"


class Pila:
    def __init__(self):
        self._tope = None
        self._tamanio = 0

    def push(self, dato):
        nuevo = Nodo(dato)
        nuevo.siguiente = self._tope
        self._tope = nuevo
        self._tamanio += 1

    def pop(self):
        if self.esta_vacia():
            raise IndexError("La pila está vacía.")
        dato = self._tope.dato
        self._tope = self._tope.siguiente
        self._tamanio -= 1
        return dato

    def peek(self):
        if self.esta_vacia():
            raise IndexError("La pila está vacía.")
        return self._tope.dato

    def obtener_todos(self) -> list:
        resultado = []
        actual = self._tope
        while actual is not None:
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado

    def esta_vacia(self) -> bool:
        return self._tope is None

    def tamanio(self) -> int:
        return self._tamanio

    def __repr__(self):
        elementos = self.obtener_todos()
        return "Tope → " + " → ".join(str(e) for e in elementos) + " → Base"


class Cola:
    def __init__(self):
        self._frente = None
        self._final = None
        self._tamanio = 0

    def encolar(self, dato):
        nuevo = Nodo(dato)
        if self._final is not None:
            self._final.siguiente = nuevo
        self._final = nuevo
        if self._frente is None:
            self._frente = nuevo
        self._tamanio += 1

    def desencolar(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía.")
        dato = self._frente.dato
        self._frente = self._frente.siguiente
        if self._frente is None:
            self._final = None
        self._tamanio -= 1
        return dato

    def frente(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía.")
        return self._frente.dato

    def obtener_todos(self) -> list:
        resultado = []
        actual = self._frente
        while actual is not None:
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado

    def esta_vacia(self) -> bool:
        return self._frente is None

    def tamanio(self) -> int:
        return self._tamanio

    def __repr__(self):
        elementos = self.obtener_todos()
        return "Frente → " + " → ".join(str(e) for e in elementos) + " → Final"


class MatrizPrecios:
    def __init__(self):
        self._tickers: list[str] = []
        self._fechas: list[date] = []
        self._matriz: list[list[float]] = []

    def _fila(self, ticker: str) -> int:
        if ticker not in self._tickers:
            raise KeyError(f"Ticker '{ticker}' no registrado en la matriz.")
        return self._tickers.index(ticker)

    def _columna(self, fecha: date) -> int:
        if fecha not in self._fechas:
            raise KeyError(f"Fecha '{fecha}' no registrada en la matriz.")
        return self._fechas.index(fecha)

    def agregar_ticker(self, ticker: str):
        if ticker not in self._tickers:
            self._tickers.append(ticker)
            self._matriz.append([None] * len(self._fechas))

    def agregar_fecha(self, fecha: date):
        if fecha not in self._fechas:
            self._fechas.append(fecha)
            for fila in self._matriz:
                fila.append(None)

    def registrar_precio(self, ticker: str, fecha: date, precio: float):
        if ticker not in self._tickers:
            self.agregar_ticker(ticker)
        if fecha not in self._fechas:
            self.agregar_fecha(fecha)
        fila = self._fila(ticker)
        col = self._columna(fecha)
        self._matriz[fila][col] = precio

    def obtener_precio(self, ticker: str, fecha: date) -> float | None:
        fila = self._fila(ticker)
        col = self._columna(fecha)
        return self._matriz[fila][col]

    def obtener_fila(self, ticker: str) -> list[tuple[date, float]]:
        fila = self._fila(ticker)
        return [
            (self._fechas[j], self._matriz[fila][j])
            for j in range(len(self._fechas))
            if self._matriz[fila][j] is not None
        ]

    def tickers(self) -> list[str]:
        return list(self._tickers)

    def fechas(self) -> list[date]:
        return list(self._fechas)

    def __repr__(self):
        if not self._tickers:
            return "MatrizPrecios (vacía)"
        ancho = 12
        header = " " * 12 + "".join(str(f).ljust(ancho) for f in self._fechas)
        filas = [header]
        for i, ticker in enumerate(self._tickers):
            fila_str = ticker.ljust(12)
            for j in range(len(self._fechas)):
                v = self._matriz[i][j]
                fila_str += (f"{v:.2f}" if v is not None else "---").ljust(ancho)
            filas.append(fila_str)
        return "\n".join(filas)


if __name__ == "__main__":
    print("=== Lista enlazada ===")
    lista = ListaEnlazada()
    lista.agregar_al_final("Transacción 1")
    lista.agregar_al_final("Transacción 2")
    lista.agregar_al_final("Transacción 3")
    print(lista)

    print("\n=== Pila (compras) ===")
    pila = Pila()
    pila.push("Compra AAPL")
    pila.push("Compra MSFT")
    pila.push("Compra NVDA")
    print(pila)
    print("Pop:", pila.pop())
    print("Después del pop:", pila)

    print("\n=== Cola (ventas) ===")
    cola = Cola()
    cola.encolar("Venta AAPL")
    cola.encolar("Venta MSFT")
    cola.encolar("Venta NVDA")
    print(cola)
    print("Desencolar:", cola.desencolar())
    print("Después de desencolar:", cola)

    print("\n=== Matriz de precios ===")
    matriz = MatrizPrecios()
    matriz.registrar_precio("AAPL", date(2024, 1, 2), 185.20)
    matriz.registrar_precio("AAPL", date(2024, 1, 3), 186.10)
    matriz.registrar_precio("MSFT", date(2024, 1, 2), 415.00)
    matriz.registrar_precio("MSFT", date(2024, 1, 3), 418.30)
    print(matriz)
