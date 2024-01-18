"""
Este módulo hace la simulación de un Banco.

Yeison Stiven Jiménez Mejía
Ingeniería Eléctrica
Universidad Tecnológica de Pereira
"""

# ---- Librerías y archivos necesarios----#
from fila import Row
from cliente import Cliente
from cajero import Cajero
from proceso import Proceso
import numpy as np
import matplotlib.pyplot as plt


# Declarando la clase
class SimulacionBanco:
    """
    Esta clase crea la simulación de un banco con N cajeros.

    """

    def __init__(self, t_simulacion=7200, N_cajeros=3, f_arribo=(15.0 / 3600.0)):
        """
        Constructor de la clase SimulacionBanco
        :param t_simulacion: tiempo que dura la simulación en segundos.
        :param N_cajeros: Número de cajas disponibles
        :param f_arribo: lambda del proceso de Poisson
        """
        # Atributos:
        self.cola = Row(50)  # Fila del banco
        self.cajero = Cajero()
        self.t_simulacion = t_simulacion
        self.N_cajeros = N_cajeros
        # self.f_arribo = f_arribo

        # duraciones promedio de los clientes
        self.duraciones = list()

        # Establecer cajeros
        self.cajeros = self.__crear_banco()

        # Creamos el proceso de Poisson
        self.proceso = Proceso(lamda=f_arribo)

        # Clientes atendidos
        self.clientes_atendidos = 0

        # Índice de cajero disponible
        self.cajero_sig = None

    # Lista de cajeros
    def __crear_banco(self):
        """
        Método que crea el banco con el número de cajeros dados.
        :return: Cajeros del banco
        """
        return [Cajero() for _ in range(self.N_cajeros)]

    def rev_cajeros(self, tstamp):
        """
        Este método verifica si hay un cajero disponible para atender a un cliente.

        :param tstamp: Tiempo de la simulación
        :return: el índice del cajero que está disponible.
        """
        for idx in range(self.N_cajeros):  # recorre a los cajeros por su índice
            if self.cajeros[idx].atendiendo(tstamp) == 0:  # evalúa si está disponible un cajero
                self.cajero_sig = idx  # índice del cajero disponible en la lista de cajeros
                break
            else:
                self.cajero_sig = None  # No hay cajeros disponibles
        return self.cajero_sig

    def cliente_arribo(self, tstamp):
        """
        Determina si en el instante de tiempo "tstamp" ocurre un evento (arriba un cliente)
        :param tstamp: Maraca de tiempo en segundos
        :return: Boolean. True si ocurre el evento de cliente arriba al banco.
        """
        return self.proceso.esevento(tstamp)

    def simular(self):
        """
        Este método ejecuta la simulación del banco para un número de cajeros determinado.

        :return: None
        """

        # Ciclo de simulación:
        for tstamp in range(self.t_simulacion + 1):
            # verificar si hay un nuevo arribo en la fila
            if self.cliente_arribo(tstamp):  # Pregunta 1
                self.cola.enter(Cliente(tstamp=tstamp))  # Agrega un cliente en la fila

            # verificar si hay un cajero libre para sacar un cliente de la fila,
            # y enviarlo al cajero:
            caja_libre = self.rev_cajeros(tstamp)
            if (caja_libre in range(self.N_cajeros)) and (self.cola.size() > 0):
                nuevo_cliente = self.cola.exit()  # remueve el primer elemento de la cola
                nuevo_cliente.salir_fila(tstamp)  # saca al cliente de la fila
                # tiempo que dura el cliente en la caja
                self.cajeros[caja_libre].atender(nuevo_cliente, tstamp)  # Atender el nuevo cliente
                # self.clientes_atendidos += 1  # Contar clientes

                t_ingreso = nuevo_cliente.t_ingreso
                t_caja = nuevo_cliente.t_caja
                t_salida = nuevo_cliente.t_salida
                # tiempo que dura el cliente en la fila
                t_fila = t_caja - t_ingreso

                # Almacenar los tiempos en duraciones
                self.duraciones.append((t_ingreso, t_fila, t_caja, t_salida))
            # Terminar la acción de atender
            for caja in self.cajeros:
                if caja.hora_salida(tstamp):
                    caja.terminar()


if __name__ == '__main__':
    # unit test:

    # Coleccionar tiempos
    tiempos = list()
    t_fila = []  # Tiempos de espera en la fila por simulación
    eventos = []  # Número de eventos por simulación
    atendidos = []  # Número de atendidos por simulación

    # Ciclo de 100 simulaciones para 3 cajeros en el banco
    for _ in range(100):
        simu = SimulacionBanco(N_cajeros=3)  # Creando el banco
        simu.simular()  # Simualando el banco
        eventos.append(simu.proceso.num_eventos)  # Agregando número de eventos a la lsita "eventos"
        atendidos.append(simu.cajeros[0].contador)  # Clientes atendidos por el cajero 1
        atendidos.append(simu.cajeros[1].contador)  # Clientes atendidos por el cajero 2
        atendidos.append(simu.cajeros[2].contador)  # Clientes atendidos por el cajero 3

        # Extrayendo los tiempos de espera en la fila:
        for times in simu.duraciones:
            tiempos.append(times)
            for i in range(tiempos.__len__()):
                tfila = tiempos[i][1]  # Tiempo de espera en la fila
                t_fila.append(tfila)
    # print('Eventos: ', eventos)
    # 1) ¿Cuántos clientes se atendieron en promedio?
    # print('Atendidos: ', atendidos)
    # print('Eventos: ', eventos)
    # Promedio de clientes atendidos:
    prom_atendidos = np.mean(atendidos)
    print('Número promedio de clientes atendidos: ', int(prom_atendidos))

    # 2) ¿Cuánto esperó el cliente que más tuvo que esperar en la fila?
    t_max_fila = max(t_fila)
    print('Tiempo máximo de espera en la fila: %d s' % t_max_fila)

    # 3) ¿Cuál fue el tiempo promedio de espera en la fila?

    # def t_promedio_fila(list):
    #     """
    #     Esta función calcula el promedio de los valores contenidos en una lista
    #     :param list: lista de números
    #     :return: valor promedio
    #     """
    #     return sum(list)/len(list)

    # t_prom_fila = t_promedio_fila(t_fila)
    t_prom_fila = np.mean(t_fila)
    print('Tiempo promedio de espera en la fila: %d s' % t_prom_fila)
    # print('Tiempo promedio de espera en la fila con mean(): %d s' % np.mean(t_fila))

    # 4) Crear una gráfica de tiempo promedio de espera en la fila contra número de cajeros.
    # Inicializando almacenadores:
    tiempos1 = []  # lista con tuplas de tiempos con 1 cajero por banco
    tiempos2 = []  # lista con tuplas de tiempos con 2 cajeros por banco
    tiempos3 = []  # lista con tuplas de tiempos con 3 cajeros por banco
    t_fila1 = []  # tiempos de espera en la fila para 1 cajero
    t_fila2 = []  # tiempos de espera en la fila para 2 cajeros
    t_fila3 = []  # tiempos de espera en la fila para 3 cajeros

    # Ciclo de 100 simulaciones para 1, 2 y 3 cajeros en el banco
    for _ in range(100):
        for i in [1, 2, 3]:
            simu = SimulacionBanco(N_cajeros=i)
            simu.simular()
            eventos.append(simu.proceso.num_eventos)  # Agregando número de eventos a la lsita "eventos"

            if i == 1:  # condición para 1 cajero en el banco
                for times in simu.duraciones:
                    tiempos1.append(times)
                    for j in range(tiempos1.__len__()):
                        tfila = tiempos1[j][1]
                        t_fila1.append(tfila)
            elif i == 2:  # condición para 2 cajeros en el banco
                for times in simu.duraciones:
                    tiempos2.append(times)
                    for j in range(tiempos2.__len__()):
                        tfila = tiempos2[j][1]
                        t_fila2.append(tfila)
            else:  # condición para 3 cajeros en el banco
                for times in simu.duraciones:
                    tiempos3.append(times)
                    for j in range(tiempos3.__len__()):
                        tfila = tiempos3[j][1]
                        t_fila3.append(tfila)

    # Tiempos promedio de espera en la fila para cada número de cajeros
    t_prom_fila1 = np.mean(t_fila1)  # 1 cajero
    t_prom_fila2 = np.mean(t_fila2)  # 2 cajeros
    t_prom_fila3 = np.mean(t_fila3)  # 3 cajeros
    t_prom = [t_prom_fila1, t_prom_fila2, t_prom_fila3]
    N_cajeros = [1, 2, 3]

    # 5) Cuál es el promedio de eventos de todas las simulaciones? ¿Este valor es esperado? ¿Por qué?
    prom_eventos = np.mean(eventos)  # Promedio de eventos
    print('Promedio de eventos: %d eventos ' % int(prom_eventos))
    print('-' * 80)
    print('El promedio de eventos esperado es de "30". Puesto que la tasa \n '
          'de arribo definida para la simulación es de 15/3600, es decir, de 15 eventos por hora\n '
          'y la simulación se define para 7200 s, para 2 horas.')
    print('-' * 80)

    # Creando la gráfica de tiempos promedio de espera en la fila contra número de cajeros
    fig, ax = plt.subplots(2, 1, figsize=(10, 8), dpi=150)
    titulo = 'Tiempo de espera en la fila vs # de cajeros'
    fig.suptitle(titulo, fontsize=16)
    # gráfico escalón
    ax[0].step(N_cajeros, t_prom, '-*b')
    ax[0].set_ylabel('Tiempo [s]')
    ax[0].set_xlabel('Número de cajeros ')
    ax[0].grid()

    # gráfico de barras
    ax[1].bar(N_cajeros, t_prom)
    ax[1].set_ylabel('Tiempo [s]')
    ax[1].set_xlabel('Número de cajeros ')

    plt.show()
