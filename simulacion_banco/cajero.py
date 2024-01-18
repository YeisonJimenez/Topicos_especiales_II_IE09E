"""
Este módulo simula un objeto cajero de Banco.

Yeison Stiven Jiménez Mejía
Ingeniería Eléctrica
Universidad Tecnológica de Pereira
"""

# Librerías y módulos necesarios
import random
from cliente import Cliente


class Cajero:
    """
    Una clase para todos los cajeros.
    """
    # Atributo de clase
    __ID = 0

    def __init__(self, media_rend=2, std_rend=1):
        """
        Inicializa la clase.
        :param media_rend: Tiempo medio de rendimiento
        :param std_rend: desviación estándar del tiempo de rendimiento.
        """
        # -- Atributos del objeto --:

        Cajero.__ID += 1
        self.id = Cajero.__ID

        # Clientes atendidos
        self.contador = 0

        # Tiempo de rendimiento del cajero
        self.rendimiento = random.gauss(media_rend, std_rend)

        # Momento de salida
        self.salida = 0
        self.cliente = 0

    def atender(self, cliente, tstamp):
        """
        El método atender marca el tiempo que dura la atención del cliente.
        :param cliente: Se ingresa un objeto cliente
        :param tstamp: tiempo de la simulación
        :return: tiempo de salida
        """
        # Marcar el tiempo en el que el cliente ingresa a la caja
        cliente.t_caja = tstamp
        rend_mas_tarea = max(cliente.tarea + self.rendimiento, 10.0)
        self.salida = tstamp + rend_mas_tarea
        self.cliente = cliente
        self.contador += 1
        return self.salida

    def hora_salida(self, tstamp):
        """
        Este método marca la hora de salida del cliente

        :param tstamp: marca de tiempo
        :return: hora de salida
        """
        return tstamp >= self.salida

    def atendiendo(self, tstamp):
        """
        Este método es para determinar si un cajero está ateniendo o no.

        :param tstamp: Tiempo en que se atiende.
        :return: Boolean. True si está atendiendo.
        """
        if tstamp < self.salida:
            return True
        else:
            return False

    def terminar(self):
        """
        Este método es para terminar de atender a un cliente.
        Reestablece los tiempos.
        :return: None
        """
        self.cliente = 0
        self.salida = 0


# Salvaguarda
if __name__ == '__main__':
    # Hacer pruebas con la clase cliente y el método atender

    caja = Cajero()
    antendiendo = caja.atender(Cliente(), tstamp=30)
    # Accion = Cajero.hora_salida(15)
    # Accion = Cajero.hora_salida(15)
    terminar = caja.terminar()
    print("El cajero está ocupado?: ", caja.atendiendo(15))
    print('Tiempo de atender: ', antendiendo)
    print('Tiempo de terminar: ', terminar)
