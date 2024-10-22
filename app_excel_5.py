# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 13:38:51 2024

@author: SecTip
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import stft
from scipy.fftpack import fft
import pandas as pd
import pywt
import io
import mpld3
import streamlit.components.v1 as components

# Título de la aplicación
st.title("Análisis de Series Temporales")

# Opción para subir un archivo Excel
uploaded_file = st.file_uploader("Sube un archivo Excel con los datos de la serie temporal", type="xlsx")

if uploaded_file:
    try:
        # Leer el archivo Excel
        df = pd.read_excel(uploaded_file)
        st.write("Datos cargados:")
        st.write(df)

        # Obtener los nombres de las columnas
        columnas = df.columns.tolist()
        st.write(f"Nombres de las columnas disponibles: {columnas}")

        # Seleccionar las columnas de 't' y 'Valores'
        columna_t = columnas[0]
        columna_valores = columnas[1]

        # Asegurarse de que las columnas seleccionadas existan
        if columna_t and columna_valores:
            t = df[columna_t].values
            y = df[columna_valores].values

            # Definir step como la diferencia entre el segundo y el primer valor de t
            step = t[1] - t[0]
            st.write(f"El valor de step es: {step}")

            # Almacenar datos en session_state
            st.session_state.t = t
            st.session_state.y = y
            st.session_state.step = step
            st.session_state.columna_valores = columna_valores

    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")

# Graficar la serie temporal
if 'y' in st.session_state:
    if st.button("Graficar Serie Temporal"):
        try:
            fig, ax = plt.subplots()
            ax.plot(st.session_state.t, st.session_state.y)
            ax.set_title(f"Serie Temporal: {st.session_state.columna_valores} vs {columna_t}")
            ax.set_xlabel(columna_t)
            ax.set_ylabel(columna_valores)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Error al graficar la serie temporal: {e}")

    # Menú de análisis
    opcion = st.selectbox("Selecciona una operación:", 
                          ("Transformada de Fourier", "Short-Time Fourier Transform (STFT)", "Transformada Wavelet Continua (CWT)", "Calcular derivada", "Calcular integral"))

    # Ejecutar análisis de la Transformada de Fourier
    if opcion == "Transformada de Fourier":
        if st.button("Ejecutar Transformada de Fourier"):
            try:
                L = len(st.session_state.y)
                Fs = 1 / st.session_state.step  # Frecuencia de muestreo
                Y = fft(st.session_state.y)
                P2 = np.abs(Y / L)
                P1 = P2[:L // 2 + 1]
                P1[1:-1] = 2 * P1[1:-1]
                f = Fs * np.arange(0, L // 2 + 1) / L

                fig1 = plt.figure(figsize=(6, 4))
                plt.subplot(121)
                plt.plot(st.session_state.t, st.session_state.y, color='tab:blue')
                plt.xlabel("Tiempo")
                plt.ylabel("X(t)")
                plt.title("Señal Original")

                plt.subplot(122)
                plt.plot(f, P1, color='tab:orange')
                plt.xlabel("Frecuencia (Hz)")
                plt.ylabel("|P1(f)|")
                plt.title("Espectro de Amplitud")

                # Mostrar la gráfica en Streamlit
                fig_html = mpld3.fig_to_html(fig1)
                components.html(fig_html, height=400)

                # Botón para descargar la imagen
                buf = io.BytesIO()
                fig1.savefig(buf, format="png")
                buf.seek(0)
                st.download_button(
                    label="Descargar imagen de FFT",
                    data=buf,
                    file_name="grafico_fft.png",
                    mime="image/png"
                )
            except Exception as e:
                st.error(f"Error al ejecutar la Transformada de Fourier: {e}")

   
    elif opcion == "Short-Time Fourier Transform (STFT)":
      f, t_stft, Zxx = stft(y, fs=1/step, nperseg=256)
      fig, ax = plt.subplots()
      ax.pcolormesh(t_stft, f, np.abs(Zxx), shading='gouraud')
      ax.set_title("Short-Time Fourier Transform (STFT)")
      ax.set_xlabel("Tiempo [s]")
      ax.set_ylabel("Frecuencia [Hz]")
      st.pyplot(fig)
    





# Ejecutar análisis de la Transformada Wavelet Continua
    elif opcion == "Transformada Wavelet Continua (CWT)":
        # Escalas para la CWT
        escalas = np.arange(2, len(st.session_state.y) // 2)

        # Transformada Wavelet Continua con Morlet compleja
        coefs, _ = pywt.cwt(st.session_state.y, escalas, 'cmor1.5-6.0')

        # Calcular frecuencias con 'cmor'
        frequencies = pywt.scale2frequency('cmor1.5-6.0', escalas) / st.session_state.step
        periodos = 1 / frequencies

        # Graficar todos los periodos
        fig, ax = plt.subplots()
        plt.contourf(st.session_state.t, periodos, np.abs(coefs) ** 2)
        ax.set_title("Transformada Wavelet Continua (CWT) con Morlet Compleja")
        ax.set_xlabel("Tiempo")
        ax.set_ylabel("Períodos")
        ax.set_yscale('log')  # Escala logarítmica para los periodos
        plt.colorbar(label='Magnitud de los coeficientes')
        st.pyplot(fig)

        # Mostrar al usuario los valores mínimo y máximo de los periodos
        min_periodo = float(np.min(periodos))
        max_periodo = float(np.max(periodos))

        st.write(f"El periodo mínimo es: {min_periodo}")
        st.write(f"El periodo máximo es: {max_periodo}")

        # Crear un formulario para introducir los valores de los periodos
        with st.form(key="form_periodos"):
            # Pedir que ingrese manualmente el rango de periodos
            min_input = st.number_input("Introduce el periodo mínimo a graficar:", value=min_periodo, min_value=min_periodo, max_value=max_periodo)
            max_input = st.number_input("Introduce el periodo máximo a graficar:", value=max_periodo, min_value=min_periodo, max_value=max_periodo)

            # Botón dentro del formulario
            submit_button = st.form_submit_button(label="Graficar periodo seleccionado")

        if submit_button:
            try:
                # Filtrar los periodos y coeficientes según el rango ingresado
                indices_periodos = (periodos >= min_input) & (periodos <= max_input)
                periodos_filtrados = periodos[indices_periodos]
                c_filtrado = np.abs(coefs[indices_periodos, :]) ** 2  # Coeficientes al cuadrado

                # Graficar los periodos seleccionados
                fig, ax = plt.subplots()
                plt.contourf(st.session_state.t, periodos_filtrados, c_filtrado)
                ax.set_title("CWT con Morlet Compleja (Periodos Seleccionados)")
                ax.set_xlabel("Tiempo")
                ax.set_ylabel("Períodos")
                ax.set_yscale('log')  # Escala logarítmica para los periodos
                plt.colorbar(label='Magnitud de los coeficientes')
                st.pyplot(fig)

            except Exception as e:
                st.error(f"Error al graficar el periodo seleccionado: {e}")

    # Calcular derivada
    elif opcion == "Calcular derivada":
        if st.button("Calcular Derivada"):
            derivada = np.gradient(st.session_state.y, st.session_state.step)
            fig, ax = plt.subplots()
            ax.plot(st.session_state.t, derivada, label="Derivada")
            ax.set_title("Derivada de la serie temporal")
            ax.set_xlabel("Tiempo")
            ax.set_ylabel("f'(t)")
            st.pyplot(fig)

    # Calcular integral
    elif opcion == "Calcular integral":
        if st.button("Calcular Integral"):
            integral = np.cumsum(st.session_state.y) * st.session_state.step
            fig, ax = plt.subplots()
            ax.plot(st.session_state.t, integral, label="Integral")
            ax.set_title("Integral de la serie temporal")
            ax.set_xlabel("Tiempo")
            ax.set_ylabel("Integral de f(t)")
            st.pyplot(fig)

else:
    st.error("Primero debes cargar un archivo Excel con datos de la serie temporal.")

