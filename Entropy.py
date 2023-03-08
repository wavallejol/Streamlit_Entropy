import streamlit as st
from math import *
import numpy as np
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
from random import *
from scipy.special import comb, factorial

def main():
    st.title("Entropía y Probabilidad")
    st.markdown("""
    Normalmente, la temperatura se interpreta fácilmente como cierta medida de la energía molecular media y la energía interna se interpreta como la energía molecular total. 
    Sin embargo, la interpretación de la [entropía](https://en.wikipedia.org/wiki/Entropy) puede llegar a ser complicada por el grado de abstracción que normalmente presenta el formalismo matemático. 
    Es así que a pesar de realizar el calculo del cambio de ΔS en varios procesos, es común que no se logre disponer de una imagen clara de la naturaleza fisicoquímica de la entropía. 
    Aunque la entropía no admite una interpretación tan sencilla como la temperatura o la energía interna, en esta experiencia se tratará de abordar su significado por medio de una simulación apoyada en conceptos probabilísticos.""")
    
    with st.expander("Detalles:"):
        st.markdown("""
        La entropía de un sistema aislado es máxima en el equilibrio y desde el punto de vista macroscópico, un sistema en equilibrio se caracteriza por una distribución (configuración) de mayor probabilidad. 
        El sistema avanza espontáneamente a través de varios macroestados con valores crecientes de probabilidad hacia el macroestado con el mayor número de configuraciones. 
        La mecánica estadística esta relacionada con la probabilidad de diferentes estados energéticos y la entropía estadística se define como:""")
        st.latex(r"""\small S=k_{B}Ln\Omega """)
        st.write("""Donde ($\small k_{B}$) es la [constante de Boltzman](https://en.wikipedia.org/wiki/Boltzmann_constant) ($\small 1,380649x10^{-23} J/K$) y $\small \Omega$ es la función de multiplicidad que representa el número de configuraciones posibles (estados microscópicos “microestados”)
        compatibles con un estado macroscópico del sistema, se define como:""")
        st.latex(r"""\small \Omega =\frac{N!}{\prod_{i}^{\infty } n_{i}}""")
        st.write("""Donde $\small N!$ representa el numero de todas las configuraciones (modos diferentes) de ordenar $\small N$ objetos diferentes (también conocido como permutaciones de $\small N$), ($\small n_{i}!$) representa el numero de configuraciones diferentes (modos diferentes) de modo que produzcan el mismo macroestado. 
        La probabilidad de encontrar un sistema en un estado determinado depende de la multiplicidad de dicho estado ($\small \Omega$). Es decir, es proporcional al número de maneras en que se puede producir ese estado. El estado queda definido por alguna propiedad medible que permita distinguirlo de otros
        estados (color, numero, forma etc). El estado de equilibrio termodinámico de un sistema aislado es el estado más probable. El aumento de entropía en un sistema aislado que evoluciona hacia el equilibrio se relaciona directamente con el paso de estados menos probables a estados más probables. 
        Con este simulador podrás obtener la curva de distribución para el lanzamiento de dos dados y la distribución de un número determinado de particulas de un gas encerradas en una caja.""")

    with st.sidebar.form(key='my_form'):
        st.subheader('Lanzamiento de Dados')
        d= st.number_input('No. de lanzamientos (1-10000)', min_value=1, max_value=100000,step=1)
        st.write('Número de lanzamientos', d)

        submit_button = st.form_submit_button(label='Graficar!')
    
    with st.expander("Lanzamiento de dados"):
        if submit_button:
            y=range(1,d+1,1)
            z=[]
            s=[]

            for i in y:
                x = randint(1,6)
                x1= randint(1,6)
                z.append(x+x1)
                nz=np.array(z)

            lanza=np.arange(1,13,1)

            for i in range(1,13,1):
                conteo=z.count(i)
                s.append(conteo)
                ns=np.array(s)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(x=lanza, y=ns*100/d,name=f'Distribusión después de {d} lanzamientos'))
            fig.update_layout(
                xaxis_title="Resultado del lanzamiento",
                yaxis_title="Probabilidad (%)",
                title=f"Distribución  después de {d} lanzamiento de dos dados",
                width=500, height=500
            )
            st.plotly_chart(fig)
main()

def main2():
    with st.sidebar.form(key='my_form2'):
        st.subheader('Distribución partículas')
        N= st.number_input('No. Partículas (1-2000)', min_value=1, max_value=2000,step=1)
        st.write('Escribiste ', N)
        nstep= st.number_input('No. steps - (1-2000)', min_value=1, max_value=5000,step=1)
        st.write('Escribiste ', nstep)
        submit_button = st.form_submit_button(label='Graficar!')

    with st.expander("Distribución de partículas de gas"):
        if submit_button:
            n=np.zeros(nstep)
            m=np.ones(nstep)*N/2
            n[0]=N
            for i in range(1,nstep):
                r=np.random.rand(1)
                if (r < n[i-1]/N ):
                    n[i] = n[i-1] - 1
                else:
                    n[i] = n[i-1] + 1

            fig = go.Figure()
            time=np.array(range(0,nstep))
            ni=np.array(n)
            fig.add_trace(go.Scatter(x=time, y=n,
                                name='Costado Izquierdo'))
            fig.add_trace(go.Scatter(x=time, y=m,
                                mode='lines',
                                name='50% de partículas')) 
            fig.update_layout(
                xaxis_title="steps",
                yaxis_title="Numero de partículas de gas",
                title=f"Distribución partículas de gas en costado izquierdo despues de {nstep} steps")
            fig.update_layout(legend=dict(yanchor="top", y=0.9, xanchor="left", x=0.7))

            st.plotly_chart(fig)
main2()

def main3():
    with st.sidebar.form(key="my form3"):
        st.subheader("Entropía")
        n= st.number_input('No. Partículas (2-1002)', min_value=2, max_value=1020,step=2)
        st.write('Escribiste ', n)
        submit_button = st.form_submit_button(label='Graficar!')
    
    with st.expander("Entropía"):
        if submit_button:
            k=np.arange(0,n+1,1)
            KB=1.380649e-23 #J/K
            C=comb(n,k)
            s=sum(C)
            S=KB*np.log(C)

            fig = make_subplots(rows=1, cols=3)

            fig.add_trace(go.Scatter(x=k, y=C, name="Multiplicidad"),row=1, col=1)
            fig.add_trace(go.Scatter(x=k, y=C*100/s, name="Probabilidad (%)"), row=1, col=2)
            fig.add_trace(go.Scatter(x=k, y=S,name="Entropía (J/k)"), row=1, col=3)
            fig.update_xaxes(title_text="Partículas costado izquierdo",row=1,col=1)
            fig.update_xaxes(title_text="Partículas costado izquierdo",row=1,col=2)
            fig.update_xaxes(title_text="Partículas costado izquierdo",row=1,col=3)

            fig.update_layout(title=f"Resultado para {n} particulas", width=1200, height=500)
            fig.update_layout(legend=dict(yanchor="top", y=0.5, xanchor="left", x=0.8))

            st.plotly_chart(fig)
main3()