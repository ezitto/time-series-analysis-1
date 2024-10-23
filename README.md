Análisis de Series Temporales
Esta aplicación web permite realizar un análisis de series temporales utilizando diversas técnicas como la Transformada de Fourier, Short-Time Fourier Transform (STFT), Transformada Wavelet Continua (CWT), cálculo de derivadas e integrales. Está construida con Streamlit y utiliza bibliotecas como NumPy, Matplotlib, SciPy y PyWavelets para realizar los cálculos y visualizaciones.

Requisitos
Asegúrate de tener instalado Python 3.x y las siguientes bibliotecas:

streamlit
numpy
matplotlib
scipy
pandas
pywt
mpld3
Puedes instalarlas utilizando pip:

bash
Copiar código
pip install streamlit numpy matplotlib scipy pandas pywt mpld3
Cómo usar la aplicación
Ejecutar la aplicación: Navega a la carpeta donde se encuentra el archivo app.py (o el nombre que le hayas dado) y ejecuta el siguiente comando en la terminal:

bash
Copiar código
streamlit run app.py
Subir un archivo Excel: La aplicación permite cargar un archivo Excel que contenga dos columnas:

La primera columna debe contener los valores de tiempo.
La segunda columna debe contener los valores de la serie temporal.
Seleccionar una operación: Después de cargar los datos, puedes seleccionar una de las siguientes operaciones para analizar la serie temporal:

Transformada de Fourier: Realiza el análisis en el dominio de la frecuencia.
Short-Time Fourier Transform (STFT): Permite observar cómo las frecuencias cambian a lo largo del tiempo.
Transformada Wavelet Continua (CWT): Proporciona una representación de la serie temporal en múltiples escalas.
Calcular derivada: Calcula la derivada de la serie temporal.
Calcular integral: Calcula la integral acumulativa de la serie temporal.
Visualización: Cada operación mostrará gráficos relevantes y, en algunos casos, opciones para descargar las imágenes generadas.

Estructura del Código
Importaciones: Se importan las bibliotecas necesarias al inicio del archivo.
Carga de datos: Se utiliza pandas para leer el archivo Excel cargado.
Graficación: Se utilizan matplotlib y mpld3 para visualizar los resultados.
Análisis: Se implementan funciones para cada tipo de análisis seleccionado por el usuario.

Link para correrla
https://time-series-analysis-1-jwzaqeib4pltgzpjyscivm.streamlit.app/

