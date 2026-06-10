# Respuestas a las Preguntas de Rendimiento y Confiabilidad

A continuacion se presentan las respuestas a las preguntas planteadas en la consigna de trabajo, fundamentadas en la teoria de redes y en las mediciones realizadas durante las pruebas de los scripts.

---

### Pregunta 1
**¿Que diferencia de tiempo notaron entre el modo CON ACK y SIN ACK? ¿A que se debe este comportamiento si el tamaño del archivo es el mismo?**

#### Respuesta:
Se observa que el **modo CON ACK** requiere un tiempo de transferencia significativamente mayor en comparacion con el **modo SIN ACK**, a pesar de que el archivo transmitido es exactamente el mismo y tiene el mismo tamaño.

#### Justificacion:
Esta diferencia de rendimiento se debe al impacto del **RTT (Round-Trip Time o Tiempo de Ida y Vuelta)** y a la logica del protocolo **Stop-and-Wait**:

- En el **modo CON ACK**, el cliente implementa una parada obligatoria por cada fragmento enviado. Despues de transmitir 4096 bytes, el proceso del cliente se suspende bloqueado en una llamada de lectura esperando que el servidor procese el bloque y le envie de vuelta el mensaje de confirmacion (`ACK`). El tiempo total de transferencia queda penalizado por la suma de los tiempos de propagacion e ida y vuelta de cada par de paquetes (Dato + ACK) a traves de la red. Si el archivo se divide en $N$ fragmentos, el tiempo total se incrementa en al menos $N \times RTT$.
- En el **modo SIN ACK**, el cliente opera en modo de transmision continua (streaming). Envia todos los fragmentos uno detras de otro de forma asincrona sin bloquearse ni esperar ninguna confirmacion de la red. La velocidad de transferencia en este modo esta limitada unicamente por el ancho de banda del canal fisico y la velocidad de procesamiento de entrada/salida (I/O) de los dispositivos, eliminando la latencia de RTT del calculo del tiempo.

---

### Pregunta 2
**En un entorno de red real (con latencia y perdida de paquetes), ¿cual de los dos modos garantiza que el archivo no se corrompa y por que?**

#### Respuesta:
El **modo CON ACK** es el unico de los dos modos que garantiza la integridad y previene la corrupcion del archivo en un entorno de red real con latencia y pérdidas.

#### Justificacion:
Debido a que UDP es un protocolo no confiable por naturaleza, la red no realiza ningun control sobre los datagramas. La logica de control de errores debe implementarse en la capa de aplicacion:

- El **modo CON ACK** implementa un mecanismo **ARQ (Automatic Repeat reQuest)** de parada y espera. Si un paquete de datos se pierde en el trayecto, o si su confirmacion de recepcion (ACK) no regresa al cliente en el lapso del temporizador (timeout de 2 segundos), el cliente detecta la falla y retransmite el bloque. Asimismo, el servidor utiliza numeros de secuencia para verificar que cada bloque se escriba en el orden correcto y para descartar fragmentos duplicados (en caso de que se haya recibido el fragmento pero se haya perdido el ACK de regreso). Esto asegura que cada byte del archivo original se escriba exactamente una vez en el archivo de destino.
- El **modo SIN ACK** no posee ningun metodo de control ni confirmacion de flujo. Si un fragmento de datos se pierde debido a colisiones o saturacion de buffers en los enrutadores de la red real, el cliente no tiene forma de detectarlo y continua transmitiendo el resto de la informacion. El servidor escribira el archivo omitiendo los fragmentos perdidos, lo que resultara en un archivo truncado y con corrupcion de datos insalvable.
