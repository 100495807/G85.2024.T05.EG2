# UC3M Travel - Hotel Management EG2

Proyecto academico de Ingenieria del Software centrado en la gestion de reservas hoteleras. Implementa una libreria en Python para reservar habitaciones, registrar llegadas de huespedes y procesar salidas, usando ficheros JSON como almacenamiento y una bateria amplia de pruebas unitarias.

## Objetivo

Desarrollar una solucion funcional para los casos principales de un sistema de hotel:

- reserva de habitaciones,
- validacion de datos de cliente,
- check-in mediante fichero JSON,
- check-out mediante clave de habitacion,
- persistencia de reservas, estancias y salidas.

## Tecnologias

- Python
- JSON
- unittest
- PyBuilder
- Validacion de datos: DNI, tarjeta de credito, fechas, telefono y formato de entrada

## Funcionalidades

| Modulo | Responsabilidad |
| --- | --- |
| `HotelManager.py` | Orquesta reservas, llegadas y salidas. |
| `HotelReservation.py` | Representa una reserva y genera localizadores. |
| `HotelStay.py` | Representa la estancia y clave de habitacion. |
| `HotelManagementException.py` | Gestion de errores de dominio. |
| `src/JsonFiles/` | Casos validos e invalidos usados en pruebas. |
| `src/unittest/` | Tests de reserva, llegada y salida. |

## Pruebas

El repositorio contiene pruebas unitarias para los tres flujos principales:

- `test_roomreservation.py`
- `test_guestarrival.py`
- `test_guestcheckout.py`

Ejecutar desde la raiz del proyecto:

```bash
python -m unittest discover src/unittest
```

Tambien puede ejecutarse con PyBuilder si esta instalado:

```bash
pyb
```

## Aprendizajes

- Modelar reglas de negocio con clases de dominio.
- Validar entradas complejas y transformar errores en excepciones controladas.
- Persistir informacion en JSON de forma estructurada.
- Escribir pruebas unitarias para casos correctos y casos limite.
- Documentar y verificar requisitos funcionales de una entrega academica.

## Estado

Proyecto academico finalizado. Se conserva como primera iteracion de una solucion de gestion hotelera en Python, con foco en funcionalidad y cobertura de pruebas.