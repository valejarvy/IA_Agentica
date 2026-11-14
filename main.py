"""Demostracion sencilla de colaboracion entre tres agentes de software."""

from __future__ import annotations

import argparse
import importlib.util
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent


BASE = Path(__file__).resolve().parent
RUTA_AGENTES = BASE / "agentes"
RUTA_SKILLS = BASE / "skills"
RUTA_SALIDA = BASE / "salida" / "programa_generado.py"


@dataclass
class CasoPrueba:
    prueba: str
    entrada: str
    esperado: str
    obtenido: str
    estado: str
    error: str = ""


def cargar_definicion(carpeta: Path, archivo: str, nombre: str) -> str:
    """Carga documentos reales de agentes y skills antes de usarlos."""
    ruta = carpeta / archivo
    if not ruta.is_file():
        raise FileNotFoundError(f"No existe la definicion requerida: {ruta}")
    contenido = ruta.read_text(encoding="utf-8")
    if nombre not in contenido:
        raise ValueError(f"La definicion {ruta.name} no contiene {nombre}.")
    return contenido


class AnalistaAgente:
    def __init__(self) -> None:
        self.definicion = cargar_definicion(
            RUTA_AGENTES, "agente_analista.md", "AnalistaAgente"
        )
        self.skill_requisitos = cargar_definicion(
            RUTA_SKILLS, "analizar_requisitos.md", "analizar_requisitos"
        )
        self.skill_diseno = cargar_definicion(
            RUTA_SKILLS, "disenar_programa.md", "disenar_programa"
        )

    def analizar_requisitos(self, idea: str) -> dict[str, object]:
        if not idea.strip():
            raise ValueError("La idea del programa no puede estar vacia.")

        return {
            "objetivo": idea.strip(),
            "datos_entrada": ["Nombre", "Lista de calificaciones entre 0 y 100"],
            "procesos": [
                "Registrar una persona y sus calificaciones",
                "Calcular el promedio de una persona",
                "Consultar los registros guardados",
            ],
            "datos_salida": ["Promedio calculado", "Lista de registros"],
            "reglas": [
                "El nombre no puede estar vacio",
                "Debe existir al menos una calificacion",
                "Cada calificacion debe estar entre 0 y 100",
            ],
        }

    def disenar_programa(self, requisitos: dict[str, object]) -> dict[str, object]:
        return {
            "clase": "RegistroSimple",
            "funciones": ["registrar", "calcular_promedio", "listar"],
            "archivo": "salida/programa_generado.py",
            "descripcion": (
                "Una clase guarda los registros en un diccionario y valida los datos "
                "antes de calcular el promedio."
            ),
            "requisitos": requisitos,
        }


class ProgramadorAgente:
    def __init__(self) -> None:
        self.definicion = cargar_definicion(
            RUTA_AGENTES, "agente_programador.md", "ProgramadorAgente"
        )
        self.skill_diseno = cargar_definicion(
            RUTA_SKILLS, "disenar_programa.md", "disenar_programa"
        )
        self.skill_codigo = cargar_definicion(
            RUTA_SKILLS, "generar_codigo.md", "generar_codigo"
        )

    def generar_codigo(self, diseno: dict[str, object], simular_error: bool = False) -> Path:
        """Genera un programa pequeno basado en el diseno recibido."""
        if diseno["clase"] != "RegistroSimple":
            raise ValueError("El diseno recibido no contiene la clase esperada.")
        validacion_superior = "" if simular_error else " or nota > 100"
        codigo = dedent(
            f'''\
            """Programa generado por ProgramadorAgente."""

            class RegistroSimple:
                def __init__(self):
                    self.registros = {{}}

                def registrar(self, nombre, calificaciones):
                    if not nombre or not nombre.strip():
                        raise ValueError("El nombre no puede estar vacio.")
                    if not calificaciones:
                        raise ValueError("Debe ingresar al menos una calificacion.")
                    for nota in calificaciones:
                        if not isinstance(nota, (int, float)) or nota < 0{validacion_superior}:
                            raise ValueError("Las calificaciones deben estar entre 0 y 100.")
                    self.registros[nombre.strip()] = list(calificaciones)

                def calcular_promedio(self, nombre):
                    if nombre not in self.registros:
                        raise KeyError("No existe un registro con ese nombre.")
                    notas = self.registros[nombre]
                    return sum(notas) / len(notas)

                def listar(self):
                    return dict(self.registros)


            if __name__ == "__main__":
                registro = RegistroSimple()
                registro.registrar("Ana", [90, 80, 100])
                print("Promedio de Ana:", registro.calcular_promedio("Ana"))
            '''
        )
        RUTA_SALIDA.parent.mkdir(exist_ok=True)
        RUTA_SALIDA.write_text(codigo, encoding="utf-8")
        return RUTA_SALIDA

    def corregir_codigo(self, diseno: dict[str, object], errores: list[str]) -> Path:
        print("ProgramadorAgente: corrigiendo codigo por:", "; ".join(errores))
        return self.generar_codigo(diseno, simular_error=False)


class TesterAgente:
    def __init__(self) -> None:
        self.definicion = cargar_definicion(
            RUTA_AGENTES, "agente_tester.md", "TesterAgente"
        )
        self.skill_pruebas = cargar_definicion(
            RUTA_SKILLS, "realizar_pruebas.md", "realizar_pruebas"
        )

    @staticmethod
    def _cargar_programa(ruta: Path):
        especificacion = importlib.util.spec_from_file_location("programa_generado", ruta)
        if especificacion is None or especificacion.loader is None:
            raise ImportError("No se pudo cargar el programa generado.")
        modulo = importlib.util.module_from_spec(especificacion)
        especificacion.loader.exec_module(modulo)
        return modulo

    def realizar_pruebas(
        self, ruta_codigo: Path, requisitos: dict[str, object]
    ) -> list[CasoPrueba]:
        modulo = self._cargar_programa(ruta_codigo)
        resultados: list[CasoPrueba] = []
        regla_rango = next(
            (regla for regla in requisitos["reglas"] if "0 y 100" in regla), ""
        )

        try:
            registro = modulo.RegistroSimple()
            registro.registrar("Ana", [80, 90, 100])
            obtenido = registro.calcular_promedio("Ana")
            estado = "APROBADA" if obtenido == 90 else "FALLIDA"
            resultados.append(CasoPrueba(
                "Calculo normal", "Ana, [80, 90, 100]", "90", str(obtenido), estado
            ))
        except Exception as error:
            resultados.append(CasoPrueba(
                "Calculo normal", "Ana, [80, 90, 100]", "90", "Excepcion", "FALLIDA", str(error)
            ))

        for nombre, notas, descripcion in [
            ("", [80], "Entrada incorrecta: nombre vacio"),
            ("Luis", [101], "Caso limite invalido: nota mayor a 100"),
            ("Eva", [0, 100], "Caso limite valido: notas 0 y 100"),
        ]:
            try:
                registro = modulo.RegistroSimple()
                registro.registrar(nombre, notas)
                if nombre == "Eva":
                    promedio = registro.calcular_promedio(nombre)
                    estado = "APROBADA" if promedio == 50 else "FALLIDA"
                    resultados.append(CasoPrueba(
                        descripcion, str(notas), "Promedio 50", str(promedio), estado
                    ))
                else:
                    resultados.append(CasoPrueba(
                        descripcion, str(notas), "ValueError", "Sin error", "FALLIDA",
                        f"La entrada invalida fue aceptada. Regla: {regla_rango}",
                    ))
            except ValueError:
                esperado = "ValueError" if nombre != "Eva" else "Promedio 50"
                resultados.append(CasoPrueba(
                    descripcion, str(notas), esperado, "ValueError", "APROBADA" if nombre != "Eva" else "FALLIDA"
                ))
            except Exception as error:
                resultados.append(CasoPrueba(
                    descripcion, str(notas), "Resultado valido", "Excepcion", "FALLIDA", str(error)
                ))
        return resultados


def mostrar_requisitos(requisitos: dict[str, object]) -> None:
    print("\nREQUISITOS PRODUCIDOS POR AnalistaAgente")
    for clave, valor in requisitos.items():
        print(f"- {clave.replace('_', ' ').title()}: {valor}")


def mostrar_informe(resultados: list[CasoPrueba]) -> None:
    print("\nINFORME PRODUCIDO POR TesterAgente")
    for caso in resultados:
        print(f"- {caso.prueba}: {caso.estado}")
        print(f"  Entrada: {caso.entrada} | Esperado: {caso.esperado} | Obtenido: {caso.obtenido}")
        if caso.error:
            print(f"  Error: {caso.error}")


def ejecutar_flujo(idea: str, simular_error: bool = False) -> bool:
    """Ejecuta Analista -> Programador -> Tester y una correccion si hace falta."""
    analista = AnalistaAgente()
    programador = ProgramadorAgente()
    tester = TesterAgente()

    print("Definiciones cargadas: 3 agentes y 4 skills.")
    requisitos = analista.analizar_requisitos(idea)
    diseno = analista.disenar_programa(requisitos)
    mostrar_requisitos(requisitos)
    print("\nDISENO: ", diseno["descripcion"])

    ruta_codigo = programador.generar_codigo(diseno, simular_error)
    print(f"\nProgramadorAgente genero: {ruta_codigo.relative_to(BASE)}")
    resultados = tester.realizar_pruebas(ruta_codigo, requisitos)
    mostrar_informe(resultados)

    errores = [caso.prueba for caso in resultados if caso.estado == "FALLIDA"]
    if errores:
        print("\nTesterAgente encontro errores y los envia al ProgramadorAgente.")
        ruta_codigo = programador.corregir_codigo(diseno, errores)
        resultados = tester.realizar_pruebas(ruta_codigo, requisitos)
        print("\nINFORME DESPUES DE LA CORRECCION")
        mostrar_informe(resultados)

    exito = all(caso.estado == "APROBADA" for caso in resultados)
    print("\nRESULTADO FINAL:", "Programa aprobado." if exito else "Quedan errores por corregir.")
    return exito


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sistema academico de IA agentica")
    parser.add_argument("--idea", help="Idea del programa que desea crear")
    parser.add_argument("--simular-error", action="store_true", help="Demuestra el ciclo de correccion")
    argumentos = parser.parse_args()
    idea_usuario = argumentos.idea or input("Escriba la idea de su programa: ")
    ejecutar_flujo(idea_usuario, argumentos.simular_error)
