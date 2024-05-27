import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import os


class Datos:
    # Ruta del archivo de datos, inicialmente None
    __ruta: str | None = None

    @staticmethod
    def __consultar_archivo() -> None:
        # Solicita al usuario el nombre del archivo a consultar
        while True:
            nombre_archivo: str = input("Ingrese el archivo que desea consultar [0 para salir]: \n>\t")

            # Si el usuario ingresa '0', se sale del programa
            if nombre_archivo == '0':
                exit()

            # Verifica si el archivo existe
            elif os.path.exists(f'{nombre_archivo}.txt'):
                print(f'Archivo "{nombre_archivo}" ejecutado correctamente.')
                Datos.__ruta = f'{nombre_archivo}.txt'  # Asigna la ruta del archivo
                break

            # Si el archivo no existe, informa al usuario
            else:
                print(f'Archivo "{nombre_archivo}" no existe. Intente nuevamente. Escriba "0" para salir.')

    @staticmethod
    def __buscar_alumno() -> None:
        # Busca un alumno por su RUT
        while True:
            try:
                rut: str = input('Ingrese el rut del alumno ["0" para volver]: \n>\t')

                if rut == '0':
                    return  # Regresa si el usuario ingresa '0'

                df: pd.DataFrame = pd.read_csv(Datos.__ruta)  # Lee el archivo de datos
                res: pd.DataFrame = df[df['rut'] == rut]  # Busca el alumno por RUT
                assert not res.empty  # Verifica que el resultado no esté vacío

                print('-' * 18)

                # Imprime la información del alumno encontrado
                for e in res:
                    print(f'{e}: {list(res[e])[0]}')

                print('-' * 18)

                break

            # Si no encuentra el alumno, informa al usuario
            except AssertionError:
                print('El rut ingresado no tiene coincidencias o es inválido. Intente nuevamente')
                continue

            except KeyboardInterrupt:
                pass

    @staticmethod
    def __modificar_alumno() -> None:
        # Modifica la información de un alumno
        df: pd.DataFrame = pd.read_csv(Datos.__ruta)  # Lee el archivo de datos
        rut: str = input('Ingrese el rut del alumno ["0" para salir]: \n>\t')
        alumno_df: pd.DataFrame = df[df['rut'] == rut]  # Busca el alumno por RUT

        # Si no encuentra el alumno, informa al usuario
        if alumno_df.empty:
            print('Rut incorrecto, intente nuevamente.')
            Datos.__modificar_alumno()

        # Menú para modificar información del alumno
        while True:
            try:
                texto_menu: str = """Que desea modificar?
                1. Nombre.
                2. Apellidos
                3. Certamen 1
                4. Certamen 2
                5. Certamen 3
                6. Tarea 1.
                7. Tarea 2.
                8. Controles.
                0. Salir\n
                Ingrese su elección: """

                res: int = int(input(texto_menu))
                index = alumno_df.index[0]

                # Modifica el campo seleccionado
                if res == 1:
                    print(f'Nombre actual = {df.at[index, "nombre"]}')
                    nuevo: str = input("Ingrese nombre: ")
                    df.at[index, 'nombre'] = nuevo

                elif res == 2:
                    print(f'Apellidos actual = {df.at[index, "apellidos"]}')
                    nuevo: str = input("Ingrese apellidos: ")
                    df.at[index, 'apellidos'] = nuevo

                elif res == 3:
                    print(f'Certamen 1 actual = {df.at[index, "certamen1"]}')
                    nuevo: float = float(input("Ingrese certamen 1: "))
                    df.at[index, 'certamen1'] = nuevo

                elif res == 4:
                    print(f'Certamen 2 actual = {df.at[index, "certamen2"]}')
                    nuevo: float = float(input("Ingrese certamen 2: "))
                    df.at[index, 'certamen2'] = nuevo

                elif res == 5:
                    print(f'Certamen 3 actual = {df.at[index, "certamen3"]}')
                    nuevo: float = float(input("Ingrese certamen 3: "))
                    df.at[index, 'certamen3'] = nuevo

                elif res == 6:
                    print(f'Tarea 1 actual = {df.at[index, "tarea1"]}')
                    nuevo: float = float(input("Ingrese tarea 1: "))
                    df.at[index, 'tarea1'] = nuevo

                elif res == 7:
                    print(f'Tarea 2 actual = {df.at[index, "tarea2"]}')
                    nuevo: float = float(input("Ingrese tarea 2: "))
                    df.at[index, 'tarea2'] = nuevo

                elif res == 8:
                    print(f'Controles actual = {df.at[index, "controles"]}')
                    nuevo: float = float(input("Ingrese controles: "))
                    df.at[index, 'controles'] = nuevo

                elif res == 0:
                    exit()

                else:
                    print('Opción no válida.')
                    continue

                df.to_csv(Datos.__ruta, sep=',', index=False)  # Guarda los cambios en el archivo
                print('Valor cambiado correctamente.')
                break

            # Maneja errores de entrada de datos
            except ValueError:
                print('Datos ingresados no son válidos. Intente nuevamente')
                continue

    @staticmethod
    def __graficar_notas() -> None:
        # Grafica las notas de dos secciones
        try:
            secciones: dict[str, pd.DataFrame | None] = {
                'seccion1': pd.read_csv('seccion1.txt').describe(),
                'seccion2': pd.read_csv('seccion2.txt').describe()
            }

            x_axis: np.ndarray = np.arange(secciones['seccion1'].columns.size)

            fig, ax = plt.subplots(layout='constrained')

            # Crea las barras para las notas de cada sección
            ax.bar(x_axis - 0.2, secciones['seccion1'].mean(), 0.4, color='darkorange')
            ax.bar(x_axis + 0.2, secciones['seccion2'].mean(), 0.4, color='steelblue')

            # Configura el gráfico
            ax.set_title('Notas Seccion 1 Vs Seccion 2.')
            ax.set_xlabel('Evaluación.')
            ax.set_ylabel('Notas promedio.')
            ax.set_xticks(x_axis, secciones['seccion1'].columns)
            plt.show()

        # Maneja el error de archivos no encontrados
        except FileNotFoundError:
            print('Archivo/s inexistente/s.')

    @staticmethod
    def __imprimir_notas() -> None:
        # Imprime las notas promedio de cada sección
        try:
            seccion1: pd.DataFrame = pd.read_csv(f'seccion1.txt')
            seccion2: pd.DataFrame = pd.read_csv(f'seccion2.txt')

            columnas: list[str] = list(seccion1)[3:]

            # Imprime las notas de la sección 1
            print('\nSección 1\n')
            [print(f'{columna}: {seccion1.describe()[columna].mean():.2f}') for columna in columnas]

            print()
            print('-' * 18)

            # Imprime las notas de la sección 2
            print('\nSección 2\n')
            [print(f'{columna}: {seccion2.describe()[columna].mean():.2f}') for columna in columnas]
            print()

        # Maneja el error de archivos no encontrados
        except FileNotFoundError:
            print('Archivo/s inexistente/s.')

    @staticmethod
    def main() -> None:
        # Punto de entrada del programa
        Datos.__consultar_archivo()

        while True:
            texto_menu: str = """Opciones (Ingrese 'salir' para terminar el programa):
                            1. Buscar un alumno.
                            2. Modificar un alumno.
                            3. Graficar periodo de notas.
                            4. Cambiar archivo.\n>\t"""

            res: str = input(texto_menu)

            # Ejecuta la opción seleccionada
            match res:
                case '1':
                    Datos.__buscar_alumno()

                case '2':
                    Datos.__modificar_alumno()

                case '3':
                    Datos.__graficar_notas()
                    Datos.__imprimir_notas()

                case '4':
                    Datos.__consultar_archivo()

                case 'salir':
                    exit()


# Ejecuta el programa principal
if __name__ == '__main__':
    Datos.main()
