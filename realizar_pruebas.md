# realizar_pruebas

## Objetivo
Verificar que el codigo cumple los requisitos y generar un informe claro de resultados.

## Entrada
- Codigo fuente a probar.
- Requisitos funcionales y reglas.

## Proceso
1. Crear casos de prueba a partir de las funciones y reglas.
2. Ejecutar un caso normal.
3. Ejecutar una entrada incorrecta y verificar que se rechace.
4. Ejecutar un caso limite valido.
5. Comparar el resultado obtenido con el esperado.

## Salida
Informe de pruebas y lista de errores encontrados.

## Como crear casos de prueba
Cada requisito importante debe tener al menos un caso. Las reglas de validacion deben tener un caso que intente incumplirlas.

## Tipos de entrada
- Normales: datos validos de uso frecuente.
- Incorrectas: datos vacios, texto donde se espera un numero o valores no permitidos.
- Limite: valores minimos o maximos validos.

## Como informar resultados
Cada registro del informe debe indicar:
- Prueba realizada.
- Entrada.
- Resultado esperado.
- Resultado obtenido.
- Estado: APROBADA o FALLIDA.
- Error encontrado, si existe.

## Como detectar errores
Una prueba es FALLIDA si el valor no coincide con lo esperado, no se produce la validacion requerida o aparece una excepcion inesperada. El error se comunica al ProgramadorAgente para su correccion.
