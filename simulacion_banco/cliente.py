"""
Este módulo se usa para simular un objeto cliente de un Banco.

Yeison Stiven Jiménez Mejía
Ingeniería Eléctrica
Universidad Tecnológica de Pereira
"""

# Librerías y módulos necesarios
import random
from fila import Row


# Declarando la clase
class Cliente:
    """
    La clase modela un objeto tipo cliente
    """
    # Atributo de la clase para ID único
    __ID = 0
    # Media  del tiempo para la tarea
    __t_medio = 180.0  # seg
    # std del tiempo para la tarea
    __t_std = 60.0  # seg
    # Tiempo mínimo para una tarea
    __t_min = 15.0  # seg

    def __init__(self, tstamp=0):
        """
        Esta es la función de inicialización de la clase Cliente

        :param tstamp: Tiempo de donde ocurre evento.
        """
        # Actualizar el ID único de la clase
        Cliente.__ID += 1
        self.id = Cliente.__ID

        # tiempo para la tarea
        self.tarea = max(random.gauss(Cliente.__t_medio, Cliente.__t_std), Cliente.__t_min)

        # Marcas de tiempo
        self.t_ingreso = tstamp  # tiempo de ingreso
        self.t_salida = 0  # tiempo de salida
        self.t_caja = 0  # Tiempo en la caja

    # Actualiza el tiempo de ingreso
    def entrar_fila(self, tstamp):
        """
        Esta función actualiza el tiempo de ingreso del usuario
        :return: None
        """
        self.t_ingreso = tstamp

    # Actualiza el tiempo de salida
    def salir_fila(self, tstamp):
        """
        Esta función actualiza el tiempo en que sale el usuario
        :return: None
        """
        self.t_salida = tstamp

    def tiempo_caja(self, tstamp):
        """
        Este método actualiza el tiempo que el cliente lleva en la caja.
        :return: None
        """
        self.t_caja = tstamp


# Salvaguarda
if __name__ == "__main__":
    mis_clientes = list()  # Lista que almacena el objeto cliente
    for _ in range(50):
        mis_clientes.append(Cliente())  # Agregando clientes a lista

    # Imprimiendo el tiempo mínimo de tarea de los clientes
    print(min(cliente.tarea for cliente in mis_clientes))

    # Mostrando la lista de clientes
    print('Mis clientes: ', mis_clientes)

    # Mostrando el ID único de cliente
    for cliente in mis_clientes:
        print(cliente.id)
