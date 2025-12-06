# analisis_eda.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class ExploradorDatos:
    """
    Una clase para realizar un Análisis Exploratorio de Datos (EDA) básico.
    
    Permite obtener resúmenes, y visualizar análisis univariados y bivariados
    de un conjunto de datos proporcionado como un DataFrame de pandas.

    Atributos
    ----------
    datos : pd.DataFrame
        El DataFrame que se va a analizar.
    """

    def __init__(self, dataframe: pd.DataFrame):
        """
        Inicializa el objeto ExploradorDatos.

        Parámetros
        ----------
        dataframe : pd.DataFrame
            El conjunto de datos para el análisis.
        """
        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError("El input debe ser un DataFrame de pandas.")
        self.datos = dataframe
        print("Objeto ExploradorDatos creado con éxito.")

    def resumen_descriptivo(self):
        """Imprime un resumen completo del DataFrame."""
        print("--- Información General ---")
        self.datos.info()
        print("\n", "--- Estadísticas Descriptivas (Numéricas) ---")
        print(self.datos.describe())
        print("\n", "--- Conteo de Valores Nulos ---")
        print(self.datos.isnull().sum())

    def analisis_univariado(self, columna: str):
        """Genera un gráfico univariado para una columna específica."""
        if columna not in self.datos.columns:
            print(f"Error: La columna '{columna}' no existe.")
            return
        
        plt.style.use('seaborn-v0_8-whitegrid')
        plt.figure(figsize=(10, 6))
        
        if pd.api.types.is_numeric_dtype(self.datos[columna]):
            sns.histplot(self.datos[columna], kde=True)
            plt.title(f'Distribución de {columna}', fontsize=16)
        else:
            sns.countplot(x=columna, data=self.datos, order=self.datos[columna].value_counts().index)
            plt.title(f'Conteo de categorías en {columna}', fontsize=16)
            plt.xticks(rotation=45)
        
        plt.ylabel('Frecuencia')
        plt.xlabel(columna)
        plt.tight_layout()
        plt.show()

    def analisis_bivariado(self, var_explicativa: str, var_respuesta: str):
        """
        Genera un gráfico bivariado entre dos variables.
        - Categórica vs Numérica: Boxplot
        - Categórica vs Categórica: Gráfico de barras agrupado
        """
        for col in [var_explicativa, var_respuesta]:
            if col not in self.datos.columns:
                print(f"Error: La columna '{col}' no existe.")
                return
        
        plt.style.use('seaborn-v0_8-whitegrid')
        plt.figure(figsize=(12, 8))
        
        if not pd.api.types.is_numeric_dtype(self.datos[var_explicativa]) and pd.api.types.is_numeric_dtype(self.datos[var_respuesta]):
            sns.boxplot(x=var_explicativa, y=var_respuesta, data=self.datos)
            plt.title(f'{var_respuesta} por {var_explicativa}', fontsize=16)
            plt.xticks(rotation=45)
        elif not pd.api.types.is_numeric_dtype(self.datos[var_explicativa]) and not pd.api.types.is_numeric_dtype(self.datos[var_respuesta]):
            sns.countplot(x=var_explicativa, hue=var_respuesta, data=self.datos)
            plt.title(f'Distribución de {var_explicativa} por {var_respuesta}', fontsize=16)
            plt.xticks(rotation=45)
        elif pd.api.types.is_numeric_dtype(self.datos[var_explicativa]) and pd.api.types.is_numeric_dtype(self.datos[var_explicativa]):
            sns.lmplot(x = var_explicativa, y = var_respuesta, data = self.datos, fit_reg= False)
            plt.xticks(rotation=45)
        else:
            print("Combinación de tipos no soportada. Prueba Categórica vs Numérica o Categórica vs Categórica.")
            return
            
        plt.tight_layout()
        plt.show()
