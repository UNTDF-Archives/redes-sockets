# Guia de Ejecucion y Diagnostico de Redes

Esta guia describe como configurar, ejecutar y auditar el sistema de transferencia de archivos UDP con autenticacion, seleccion de modos y medicion de rendimiento, despues de la reestructuracion en subdirectorios.

## 1. Obtener la Direccion IP en Linux

Para configurar los scripts en un entorno de red real, es necesario conocer la IP de las interfaces activas.

Ejecute uno de los siguientes comandos en la terminal del sistema Linux:

- Usando iproute2 (Recomendado):
  ```bash
  ip addr show
  ```
  Busque la interfaz activa (usualmente eth0, enp3s0 o wlan0) y copie la direccion IPv4 que aparece despues del campo `inet` (ejemplo: 10.7.70.209).

- Usando hostname (Rapido):
  ```bash
  hostname -I
  ```
  Este comando devuelve directamente todas las direcciones IP asignadas a la maquina separadas por espacios.

## 2. Configuracion de Direcciones IP y Puertos

- Servidor UDP (`source/UDP/srv_udp_file.py`) y Cliente UDP (`source/UDP/cli_udp_file.py`):
  La IP y el puerto se configuran directamente en las variables `HOST` y `PORT` definidas en las primeras lineas de ambos archivos:
  ```python
  HOST = '10.7.70.209'
  PORT = 9090
  ```

- Servidor TCP (`source/TCP/srv_tcp_echo.py`) y Cliente TCP (`source/TCP/cli_tcp_echo.py`):
  La IP y el puerto se configuran directamente en las variables `HOST` y `PORT` definidas en las primeras lineas de ambos archivos:
  ```python
  HOST = '10.7.70.209'
  PORT = 50007
  ```

## 3. Ejecucion del Sistema

### Sockets UDP (Transferencia de Archivos)
Asegurate de situarte en el directorio `source/UDP/` antes de ejecutar. El archivo `Libro.pdf` debe encontrarse en ese mismo directorio.

#### Paso 1: Iniciar el Servidor
En la primera terminal, ejecute:
```bash
cd source/UDP
python srv_udp_file.py
```

#### Paso 2: Iniciar el Cliente
En la segunda terminal, ejecute:
```bash
cd source/UDP
python cli_udp_file.py
```
1. Ingrese el nombre de **usuario** y **contraseña** de autenticacion (Ejemplos validos: usuario `lucas` y contraseña `redes2026`, o usuario `admin` y contraseña `admin123`).
2. Una vez aceptado el acceso, ingrese el modo de transmision:
   - Ingrese `1` para el **Modo con ACK** (Alta fiabilidad, parada y espera).
   - Ingrese `2` para el **Modo sin ACK** (Máxima velocidad, transmision continua).

---

### Sockets TCP (Eco)
Asegurate de situarte en el directorio `source/TCP/` antes de ejecutar.

#### Paso 1: Iniciar el Servidor
En la primera terminal, ejecute:
```bash
cd source/TCP
python srv_tcp_echo.py
```

#### Paso 2: Iniciar el Cliente
En la segunda terminal, ejecute:
```bash
cd source/TCP
python cli_tcp_echo.py
```

---

## 4. Medicion con Wireshark

Para capturar y analizar el trafico de red generado por la transferencia, siga estos pasos:

1. Inicie Wireshark en su sistema.
2. Seleccione la interfaz de red apropiada para capturar (use `Loopback: lo` si cliente y servidor estan en la misma maquina y usas IP de loopback, o la interfaz de red fisica activa, ej. `wlan0`, si usas la IP de red local como `10.7.70.209`).
3. Inicie la captura de paquetes.
4. Aplique el siguiente filtro en la barra de busqueda superior para aislar la transferencia:
   ```text
   udp.port == 9090
   ```
5. En los paquetes capturados podra inspeccionar:
   - Los mensajes de control iniciales: autenticacion (`AUTH:`), confirmacion de modo (`MODE:`), y nombre del archivo (`FILE:`).
   - En **Modo con ACK**: vera la secuencia de parada y espera (Stop-and-Wait). Cada paquete `DATA` va precedido por su respectivo `ACK` de confirmacion del servidor antes de que se envie el siguiente.
   - En **Modo sin ACK**: vera una rafaga continua de paquetes `DATA` sucesivos enviados a la maxima velocidad de la red, sin confirmaciones intermedias.

## 5. Aspectos a Tener en Cuenta

- El tamaño maximo de los datagramas UDP es de 65,535 bytes, pero para evitar la fragmentacion IP, se utiliza un fragmento de lectura (`CHUNK_SIZE`) de 4096 bytes.
- En el modo con ACK, el cliente tiene configurado un timeout de 2.0 segundos para cada respuesta del servidor. Si en ese periodo no recibe confirmacion, retransmitira el fragmento.
- Se permiten un maximo de 5 reintentos por fragmento. Si todos fallan, el cliente asume que la red o el servidor estan caidos, cancela la transmision de manera limpia y se cierra.
- El servidor esta preparado para ignorar fragmentos de datos duplicados y re-enviar la confirmacion (ACK) si detecta que escribe un fragmento cuyo numero de secuencia es menor al esperado. Esto asegura la integridad final del archivo sin duplicaciones de contenido.
