# Explicacion Tecnica y Teorica de la Implementacion

Este documento proporciona una explicacion detallada y educativa sobre la arquitectura del sistema de transferencia de archivos UDP, la teoria de redes subyacente, el uso de sockets en Python, y la logica de programacion para autenticacion, control de flujo y medicion de rendimiento.

---

## 1. Fundamentos de Redes: TCP vs. UDP y el Concepto de Sockets

### ¿Que es un Socket?
Un socket es un punto final (endpoint) de una comunicacion bidireccional entre dos programas que se ejecutan en una red. Se define conceptualmente por la tupla:
`(Direccion IP, Puerto, Protocolo de Transporte)`
- **Direccion IP:** Identifica el host en la red.
- **Puerto:** Identifica la aplicacion o proceso especifico dentro del host.
- **Protocolo:** Define las reglas de transporte de datos.

### TCP (Transmission Control Protocol) vs. UDP (User Datagram Protocol)
A nivel de la capa de transporte (Capa 4 del modelo OSI):
- **TCP** es orientado a la conexion y confiable. Antes de enviar datos, realiza un saludo de tres vias (3-way handshake) para establecer conexion. Se encarga de retransmitir paquetes perdidos, ordenar los fragmentos que lleguen desordenados, y controlar la velocidad del envio (control de flujo y de congestion).
- **UDP** es un protocolo no orientado a la conexion y no confiable. Envia datagramas (mensajes independientes) directamente sin establecer conexion previa y sin garantizar que lleguen al destino, que lo hagan en el orden correcto, o que no se dupliquen. No tiene mecanismos nativos de retransmision.

### ¿Por que implementar confiabilidad sobre UDP?
Aunque TCP ofrece confiabilidad integrada, tiene una alta sobrecarga de control (encabezados de 20 bytes minimo frente a 8 bytes de UDP, retardos por establecimiento de conexion, confirmaciones continuas, etc.). En ciertos escenarios (como juegos en linea, streaming, o entornos academicos de diagnostico), es util o necesario diseñar protocolos propios sobre UDP para decidir exactamente como y cuando retransmitir datos, reduciendo la latencia o simulando redes especificas.

---

## 2. Protocolo de Aplicacion: Autenticacion y Sesiones sobre UDP

Como UDP carece del concepto de conexion persistente, cada datagrama que llega al servidor es independiente. Para implementar seguridad e integridad, debimos crear un mecanismo de sesion a nivel de aplicacion (Capa 7 del modelo OSI).

### Sistema de Autenticacion
El proceso de autenticacion funciona como una maquina de estados secuencial:

1. **Estado Inicial (No Autenticado):** El servidor rechaza cualquier fragmento de archivo. Solo acepta paquetes de peticion de conexion (`CONN_REQ`) o de credenciales (`AUTH:`).
2. **Envio de Credenciales:** El cliente solicita el usuario y la contraseña de forma interactiva y los empaqueta en una cadena de texto:
   `AUTH:<usuario>:<contraseña>`
3. **Validacion en Servidor:** El servidor recibe el paquete, extrae el usuario y la contraseña usando el delimitador `:`, y los busca en un diccionario local (`CREDENTIALS`):
   ```python
   CREDENTIALS = {
       "admin": "admin123",
       "lucas": "redes2026",
   }
   ```
4. **Respuesta de Seguridad:**
   - Si los datos son correctos: El servidor responde con el mensaje `AUTH_OK` y registra la tupla de red del cliente (`client_addr = (IP, Puerto)`). A partir de ese instante, se considera la sesion iniciada y el servidor solo aceptara comandos de datos que provengan de esa direccion IP y puerto especificos, ignorando trafico externo.
   - Si los datos son incorrectos: Responde con `AUTH_FAIL` y el servidor finaliza su ejecucion de forma limpia llamando a `sys.exit(0)` tras cerrar el socket. El cliente recibe esta cadena, detecta el fallo de seguridad, informa en consola y termina la ejecucion inmediatamente (`sys.exit(0)`) para cumplir con la finalizacion segura solicitada.

---

## 3. Modos de Transmision e Integridad de Datos

### Modo con ACK: Parada y Espera (Stop-and-Wait ARQ)
Este modo prioriza la fiabilidad absoluta de la transferencia a costa de la velocidad de transmision:
- **Control de Tiempo (Timeout) en el Cliente:**
  El cliente configura un tiempo limite en su socket (`client.settimeout(2.0)`). Al enviar un fragmento, bloquea su ejecucion esperando la confirmacion (`ACK:<num>`) del servidor. Si transcurren 2.0 segundos sin respuesta, se captura la excepcion `socket.timeout` y el cliente vuelve a enviar el mismo fragmento.
- **Limite de Reintentos:**
  El cliente intenta retransmitir un mismo fragmento hasta un maximo de 5 veces. Si el contador se agota, se asume que la conexion se rompio y aborta limpiamente.
- **Control de Duplicados en el Servidor:**
  Si un fragmento llega al servidor pero el ACK se pierde en la red, el cliente lo retransmitira. Para evitar duplicar datos en el archivo destino, el servidor lleva un registro secuencial (`expected_chunk_num`). Si recibe un fragmento menor al esperado, descarta los datos y solo re-envia el `ACK` correspondiente para desatascar al cliente.

### Modo sin ACK: Envio Continuo
Este modo prioriza la velocidad de transmision sobre la fiabilidad:
- El cliente envia los fragmentos secuencialmente sin esperar confirmaciones intermedias.
- Para evitar que la rafaga de paquetes UDP desborde el buffer del socket del sistema operativo (lo que provocaria la perdida masiva de paquetes en el host local), se añade un retardo minimo (`time.sleep(0.0002)`) entre envios. Esto estabiliza la transferencia en transmisiones de alta velocidad.
- El servidor escribe los fragmentos en el orden en que los recibe. No hay mecanismos de retransmision, por lo que si ocurre una perdida en el canal de red, el archivo destino quedara corrupto (con bytes faltantes o desordenados).

---

## 4. Enmarcado de Datos (Framing) y Manejo Binario en Python

El canal UDP transmite un flujo de bytes planos. Si enviaramos el archivo de forma directa, ¿como sabria el servidor si los bytes recibidos son parte del PDF o el aviso de fin de archivo (`DONE`)?
Para separar el control de los datos, agregamos un encabezado de texto antes de la carga util de datos.

### Construccion de Encabezados Binarios
En Python, los strings (cadenas de caracteres unicode) y los bytes (cadenas binarias crudas) son tipos de datos distintos. No es posible concatenar directamente un string con bytes.
Por lo tanto, construimos el encabezado como un string, lo convertimos a bytes usando `.encode('utf-8')` y luego lo concatenamos con el fragmento leido del archivo:
```python
header = f"DATA:{chunk_num}:{chunk_len}:".encode('utf-8')
packet = header + data  # data ya esta en bytes porque se leyo con 'rb'
```

### Desempaquetado del Lado del Servidor
El servidor recibe un bloque de bytes de longitud variable. Debe extraer los metadatos del encabezado sin dañar la informacion binaria del archivo.
Utilizamos el metodo `.split(bytes, maxsplit)` de Python:
```python
parts = packet.split(b':', 3)
```
El segundo argumento `3` le dice a Python que solo realice las primeras 3 divisiones posibles. Esto asegura que el bloque binario del archivo (que se almacena en `parts[3]`) permanezca completamente intacto, incluso si los datos binarios del PDF contienen bytes que corresponden al caracter de dos puntos (`:`).

---

## 5. El API de Sockets en Python y Control de Tiempo

A continuacion, se explica el uso de las funciones principales de la libreria `socket` y `time`:

- `socket.socket(socket.AF_INET, socket.SOCK_DGRAM)`:
  Crea un socket. `AF_INET` indica IPv4. `SOCK_DGRAM` especifica UDP (datagramas).
- `server.bind((HOST, PORT))`:
  Asocia el socket a una direccion IP y puerto locales para empezar a escuchar paquetes.
- `server.recvfrom(bufsize)`:
  Llamada bloqueante que suspende la ejecucion hasta que llegue un datagrama. Retorna los bytes recibidos y la tupla de direccion del emisor.
- `client.sendto(data, (HOST, PORT))`:
  Envia un datagrama UDP directamente a la direccion de destino especificada.
- `time.perf_counter()`:
  Retorna el valor de un reloj de alta resolucion con precision de microsegundos.
  - Para calcular el tiempo exacto en milisegundos solicitado por el docente, tomamos `start_time` justo antes de enviar/recibir el primer fragmento y `end_time` inmediatamente despues de procesar el marcador `"DONE"`.
  - La formula aplicada es: `(end_time - start_time) * 1000`.
- **Parametrizacion Directa**:
  Para simplificar la portabilidad y ejecucion directa, la IP y Puerto se definen de forma explicita en las variables estaticas `HOST` y `PORT` al inicio de cada archivo fuente, evitando dependencias externas de lectura de archivos de configuracion ocultos.
