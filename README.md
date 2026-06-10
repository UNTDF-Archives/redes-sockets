# RyTD

# Laboratorio de Programación de Redes y Sistemas Distribuidos
Este repositorio centraliza los recursos prácticos, entornos de experimentación y guías de laboratorio de la cátedra **Redes y Transmisión de Datos**.

## Propósito del Repositorio
A diferencia de los enfoques tradicionales de redes orientados puramente a la infraestructura o la configuración de hardware, este espacio está diseñado como un entorno de desarrollo e ingeniería de software orientado a las comunicaciones. El objetivo principal es que el estudiante experimente, diagnostique y comprenda el comportamiento de los protocolos de transporte e internet (TCP/IP) directamente desde la perspectiva del programador de aplicaciones.
A través de la implementación de sockets, el manejo de la concurrencia y la manipulación de flujos de datos binarios, se busca modelar el impacto real que tienen las decisiones de diseño de software sobre la eficiencia, robustez y seguridad de los sistemas distribuidos.

## Estructura General del Repositorio
El contenido de este espacio se encuentra en constante evolución académica y está organizado estratégicamente para acompañar el trayecto pedagógico de la materia:

## Código y Casos de Estudio de Clase
En esta sección se compilan los scripts, prototipos y ejemplos técnicos desarrollados incrementalmente durante las clases teórico-prácticas. Funciona como un cuaderno de campo de programación (utilizando principalmente Python), cubriendo desde la arquitectura básica de sockets bloqueantes hasta esquemas concurrentes multihilo.


## Laboratorios de Diagnóstico Forense (clase_forense)
Espacio dedicado a experiencias de laboratorio e investigación activa en el entorno virtualizado. Aquí se disponen los escenarios prácticos —como binarios de prueba, scripts de clientes y servidores base— junto a sus respectivas guías de instrumentación.
En estos laboratorios, los estudiantes integran el desarrollo de software con herramientas de auditoría y análisis de tráfico crudo (tcpdump/Wireshark), permitiéndoles validar en tiempo real conceptos críticos como el control de flujo (TCP Window), fragmentación (MSS) y la seguridad de los datos en tránsito.

## Requisitos del Entorno
Para la correcta ejecución y despliegue de los proyectos aquí contenidos, se requiere el uso del laboratorio virtualizado provisto por la cátedra (instancias Linux configuradas bajo topologías de red específicas) y las herramientas nativas de diagnóstico de red de consola.