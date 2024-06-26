# Simulation_IA_Project

## Descripción del problema

El problema planteado consiste en desarrolar un generador de trayectorias de movilidad para La Habana capaz de simular el movimiento de los habitantes de la capital considerando fundamentalmente las redes de ómnibus (Metrobús y otras) y los recorridos de los vehículos de alquiler (Metrotaxi y otros). El objetivo fundamental es estimar que cantidad de habitantes se encuentran en cada municipio de la capital durante las 24 horas de un día.

### Información demográfica

Los datos demográficos de La Habana se obtendrán de la Oficina Nacional de Estadísticas e Información (ONEI) de Cuba, específicamente del reporte "Estudio y Datos de Población 2023".

### Información espacial

La información espacial de La Habana se obtendrá del proyecto OpenStreetMap, utilizando datos de Geofabrik para obtener extractos de datos de OpenStreetMap en formato PBF. La biblioteca Pyrosm se utilizará para leer y procesar estos datos en Python, permitiendo la extracción de redes de transporte, puntos de interés y otros elementos relevantes para la simulación.

## Arquitectura de la simulación

### Agentes

En una simulación, un agente es un objeto o un componente que representa una
entidad con capacidad de actuar y tomar decisiones dentro del sistema simulado.
Los agentes pueden interactuar entre sí y con el medio para lograr sus objetivos.
Cada agente tiene un conjunto de reglas o comportamientos programados que
determinan cómo actúa y cómo toma decisiones. En el problema planteado, los
agentes serían los vehículos, la empresa de transporte:

#### Vehículo

Un agente vehículo es un objeto que representa un vehículo en la simulación.
Tiene varias propiedades, como un identificador ínico, una capacidad de carga y un total de kilómetros que puede recorrer. La compañía asigna la ruta que debe cumplir.
Entre las posibles acciones del vehículo están:

- Moverse a la siguiente parada en la ruta asignada.
- Recoger y/o dejar pasajeros en la parada actual.
- Reportar su posición actual.
- Informar sobre el estado del vehículo.
- Cambiar la ruta si es necesario.

#### Compañía

El agente compañía es un objeto que representa la empresa de transporte en la
simulación. Tiene varias propiedades, como un depósito, una lista de vehículos,y un presupuesto. Entre las acciones posibles de la compañía
están:

- Asignar a cada vehículo su ruta.
- Enviar a mantenimiento a los vehículos que lo necesiten y buscar reemplazo
en lo posible.
- Pagar todos los gastos relacionados con los vehículos, como combustible y mantenimiento o arreglo.
- Analizar y optimizar las rutas y los costos de transporte.

### Medio

En una simulación, el medio es el entorno o el ambiente en el que se lleva a cabo la simulación. En el contexto del problema planteado, el medio será ser el
sistema de carreteras de La Habana.

## Sobre la solución del problema

La implementación computacional del problema fue abordada utilizando varios enfoques, como la programación de agentes, la inteligencia artificial.
Se utilizó un sistema de programación de agentes, donde cada agente (vehículo,
empresa) fue programado con un conjunto de reglas y comportamientos que le permiten interactuar con el medio y con los demás agentes. Los agentes vehículos se mueven de acuerdo a la ruta asignada y toman decisiones basadas en la información del medio y en las comunicaciones con la empresa. La empresa asigna las rutas a los vehículos y toma decisiones sobre el mantenimiento de los existentes.
También, se utilizaron técnicas de inteligencia artificial, como búsqueda,
metaheurísticas y planificación.

### Clases

#### NodeMap

La clase NodeMap representa un nodo en el grafo que es el mapa sobre el cual
los vehiculos se transportan. Esta clase tiene varias propiedades que se utilizan
para representar el estado del mapa en un punto específico. Algunas de las
propiedades más importantes son:

- position: esta propiedad indica la posición geografica del nodo en el
mapa.
- people: esta propiedad indica la cantidad de personas que se encuentran
en ese punto en el mapa.
- semaphore: esta propiedad indica si hay un semáforo en ese punto en el
mapa. Contiene un objeto Semaphore que con información adicional sobre
el semáforo.

#### Vehicle

La clase Vehicle representa al agente vehículo en la simulación. Esta clase tiene varias propiedades y métodos que se utilizan para simular el  
comportamiento del
vehículo y su interacción con el entorno. Algunas de las propiedades y métodos más importantes son:

- id: esta propiedad es el identificador único del vehículo.
- capacity: esta propiedad indica la capacidad del vehículo, es decir, la
cantidad máxima de personas que puede transportar.
- km traveled: esta propiedad indica la cantidad total de kilómetros que el
vehículo ha recorrido.
- route: esta propiedad indica la ruta asignada al vehículo.
- people on board: esta propiedad indica la cantidad de personas que hay
en el vehículo.
- move(): este método se utiliza para mover el vehículo a través del mapa,
guiándose por la ruta asignada.
- load(): este método se utiliza para cargar a las personas en la posición
actual en que se encuentra el veh´ıculo.
- unload(): este m´etodo se utiliza para dejar a las personas en la
posición actual en que se encuentra el vehículo.
- at semaphore(): este método se utiliza cuando hay semáforos en el punto
actual y para tomar decisiones sobre cómo evitarlas o adaptarse a las
restricciones.
- broken(): este método se utiliza cuando el vehículo se rompe en medio
de su ruta.
- plan(): este método se utiliza para hallar la próxima acción del vehículo
en el punto actual.

#### Company

La clase Company representa a la empresa de transporte en la simulación. Algunas de las propiedades y métodos más importantes son:

- vehicles: esta propiedad es una lista de objetos Vehicle, que representan
los vehículos de la empresa.
- passengers: esta propiedad es un diccionario con los ids de los pasajeros y la lista de paradas de cada uno.
- budget: esta propiedad indica el presupuesto actual de la empresa.
- assign(): este método se utiliza para obterner asignación de las rutas a los vehículos.
- start route(): este método se utiliza para asignar rutas a los vehículos.
- pay taxes(): este método se utiliza para pagar los gastos de los vehículos,
incluyendo el combustible y el mantenimiento.
- check vehicle(): este método se utiliza para verificar el estado de un
vehículo.
- check maintenance(): este método se utiliza para conocer que vehículos
están en mantenimiento y reasignar, según las necesidades, a los que salgan.
- find replacement(): este método se utiliza para hallar sustituto a vehículo
en mantenimiento.
- plan(): este método se utiliza para hallar el plan de acción de la compañía
por cada vehículo que posee.

#### Semaphore

La clase Semaphore representa los semáforos en el medio de la simulación. Esta clase tiene varias propiedades y métodos que se utilizan para simular el comportamiento de los semáforos y su interacción con los vehículos. Algunas de las propiedades y métodos más importantes son:

- position: esta propiedad indica la posición en el mapa donde se encuentra
el semáforo.
- state: esta propiedad indica el color actual del semáforo.
- color range: esta propiedad indica la duración de cada color del semáforo.
- update color() : dado el tiempo global y la duración de cada color del
semáforo, actualiza el color del mismo.

### Inteligencia Artificial

#### Búsqueda

La búsqueda es una técnica de inteligencia artificial que se utiliza para encontrar soluciones óptimas en problemas de navegación en espacios de estados. Se utilizó junto al algoritmo de planificación para encontrar la siguiente acción de la compañía, dado un estado y un dominio. El algoritmo de búsqueda utilizado fue el algoritmo de costo uniforme.

#### Recocido Simulado

El enfoque de recocido simulado (Simulated Annealing, SA) es un algoritmo de
optimización que se utiliza para encontrar soluciones óptimas en problemas de optimización complejos. Se inspira en el proceso de enfriamiento de los metales al ser forjados.
En el problema, la compañía de transporte tiene que asignar a los vehículos las paradas. El proceso de asignación de paradas es un problema de optimización complejo debido a las restricciones y las diferentes variables involucradas, como la capacidad de carga de los vehículos y la cantidad de personas en que debe recojer y/o dejar cada parada.

El algoritmo de recocido simulado se utiliza para encontrar la asignación
óptima de vehículos y paradas. El algoritmo comienza con una solución inicial que es una asignación aleatoria y luego aplica un proceso iterativo de mejora de la solución. En cada iteración, el algoritmo genera una nueva solución modificando ligeramente la solución actual. La nueva solución se evalúa y se decide si se acepta o no en función de una función de probabilidad que depende de la diferencia entre la solución actual y la nueva solución y de un parámetro de temperatura que se va reduciendo a medida que el proceso avanza. El proceso continua hasta que se alcanza un criterio de parada, que en este caso es un número fijo de iteraciones.

#### Colonia de Hormigas

La metaheuristica colonia de hormigas (ACO, por sus siglas en inglés) es un
algoritmo de optimización que se utiliza para encontrar soluciones óptimas en
problemas de optimización de rutas. Se basa en el comportamiento de las hormigas al buscar comida.
En el problema, la compañía de transporte tiene que planificar las rutas
de los vehículos de forma óptima para maximizar el traslado de pasajeros en 24 horas. El algoritmo de colonia de hormigas se utiliza para encontrar la ruta óptima para cada vehículo. El algoritmo comienza con una solución inicial y luego aplica un proceso iterativo de mejora de la solución. En cada iteración, el algoritmo simula el comportamiento de las hormigas para recolectar comida. Cada hormiga se mueve a través de las diferentes paradas y decide qué parada visitar en función de una función de probabilidad que depende de la cantidad de feromona depositada en cada parada y de la distancia entre las paradas. La feromona es una sustancia que las hormigas depositan en el camino para indicar a las demás hormigas que ruta es más prometedora. Cuanto más feromona hay en un camino, más probable es que las hormigas elijan esa ruta.
A medida que las hormigas recorren las paradas, depositan feromona en el
camino que han seguido. Esto aumenta la probabilidad de que las hormigas
futuras elijan esa ruta. Al final de cada iteración, el algoritmo actualiza la
feromona en las paradas, evapora una parte de la feromona para evitar que se
acumule en una sola ruta y añade nueva feromona para fomentar la exploración
de nuevas rutas.

#### Planificación

La planificación de inteligencia artificial (AI Planning) es una técnica que se utiliza para encontrar soluciones óptimas en problemas de planificación en los que existen varias acciones posibles y restricciones. Puede ser utilizado para
asistir en la toma de decisiones de la empresa y optimizar las acciones que
realiza. Esta herramienta se utiliza en la compañía de transporte debido a que las acciones de la compañía son estáticas y consisten en tareas repetitivas como asignar rutas a los vehículos, pagar combustible y mantenimiento, y verificar el estado de los vehículos. Con esto se logra automatizar y optimizar estas tareas mediante la generación de planes de acción que consideran las restricciones y limitaciones existentes.
