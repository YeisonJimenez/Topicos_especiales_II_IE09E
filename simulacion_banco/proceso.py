"""
Módulo para simular el proceso de arribo de clientes al banco

Yeison Stiven Jiménez Mejía
Ingeniería Eléctrica
Universidad Tecnológica de Pereira
"""

# Librerías necesarias
import math
import random
import matplotlib.pyplot as plt


# Declarando la clase
class Proceso:
    """
    Esta es una clase para simular un proceso de Poisson.
    """
    temp = True

    def __init__(self, lamda):
        """
        Inicializacion.
        :param lamda: Frecuencia promedio de arribo de clientes [eventos/seg]
        """
        self.lamda = lamda
        self.num_eventos = 0  # Contador de número de eventos
        self.tiempo_evento = self.prox_evento()

    def prox_evento(self):
        """
        Metodo para calcular el tiempo en donde ocurrirá el próximo evento
        :return: t_next tiempo donde ocurrirá el próximo evento
        """
        # Determinar el valor de p de una exponencial. Que es de una distribución uniforme
        p = random.random()  # obtiene un número aleatorio entre 0 y 1.
        t_next = -math.log(1 - p) / self.lamda
        # t_next es el valor en tiempo relativo. Tiempo inter-evento.

        if self.temp:
            self.temp = False
            return t_next
        else:
            self.tiempo_evento += t_next  # Convertir en tiempo absoluto.
        self.num_eventos += 1  # Actualiza contador de eventos

    def esevento(self, tstamp):
        """
        Determina si la marca de tiempo actual es un evento o no
        :param tstamp:
        :return: Boolean. True si la marca de tiempo es un evento
        """
        retorno = False

        if tstamp >= self.tiempo_evento:
            retorno = True
            self.prox_evento()

        return retorno


if __name__ == "__main__":
    # unit test:
    obj1 = Proceso(lamda=15.0 / 3600.0)  # lambda: 15 clientes en una hora

    # Coleccionar eventos
    eventos = list()

    # El tiempo correrá desde 0 hasta 7200 seg. 2 horas:
    for stamp_t in range(7200):
        if obj1.esevento(stamp_t):
            eventos.append(stamp_t)
            print("[%d] : %d" % (obj1.num_eventos, stamp_t))  # eventos.__len__(), stamp_t

    plt.step(eventos, range(1, eventos.__len__() + 1), "*-", where='post', label='post')
    plt.grid()
    plt.show()
