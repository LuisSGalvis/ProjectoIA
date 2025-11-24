Nuestra politica final, politica legendaria, es una politica que combina heuristica combinado con un MCTS, 
con el objetivo de plantear mejores posibles jugadas, las cuales sean exploradas mediante el MCTS.
Nuestra politica recibe el parametro time_out, mediante mount, y en caso de no hacerlo se inicializa por defecto con 10 segundos por accion para explorar y decidir
No requiere de datos de uso fuera de ajustar el tiempo que pensara para cada accion
Este primero evalua si cuenta con una oportunidad de ganar en su turno o si esta en riesgo de perder en el siguiente y debe bloquear
Posteriormente si es el primer turno y es el primer jugador pondra la primera ficha en la columna del medio,
despues, observara si es posible que la siguiente ficha en columna del centro es la tercera fila, para tomarla.
Finalmente evalua que jugador es para ver que columnas le favorecen bajo la estrageia de even/odd rows

Despues de esto, si no hubo movimiento forzado se por oportunidad de victoria, bloqueo o tomar el primer puesto del centro, este envia la lista
de columnas recomendadas, columnas a evitar, para realizar un MCTS con el cual explorar sub trials en las columnas filtradas para mejorar la información 
generada por los trials permitiendo guiarlo a movimientos estrategicos
Finalmente cuando no cuenta con mas tiempo para pensar, este evalua el valor asignado a jugar cada columna y elige la que mostro mejor oportunidad de victoria
