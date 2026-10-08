import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ml_analysis import predict_cases_df

API_URL = "http://127.0.0.1:5000/"
st.title("Dashboard COVID-19")

@st.cache(ttl=3600)
def fetch_countries():
    response = requests.get(f"{API_URL}/")
    if response.status_code == 200:
        return response.json()
    return []

countries = fetch_countries()
country = st.selectbox("Sélectionnez un pays", countries)

if country:
    country = country.strip()
    response = requests.get(f"{API_URL}/stats/{country}")
    st.write(f"Status code: {response.status_code}")
    st.write(f"Response text: {response.text[:500]}")

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')

        st.subheader(f"Statistiques COVID pour {country}")
        st.line_chart(df.set_index('date')[['total_cases', 'total_deaths']])

        st.subheader("Prédictions pour les prochains jours")
        try:
            days, preds = predict_cases_df(df, days_ahead=7)
            pred_df = pd.DataFrame({
                'Day': days,
                'Predicted Confirmed Cases': preds.astype(int)
            })
            st.table(pred_df)

            fig, ax = plt.subplots()
            ax.plot(pred_df['Day'], pred_df['Predicted Confirmed Cases'], marker='o')
            ax.set_xlabel('Jour (depuis début des données)')
            ax.set_ylabel('Cas confirmés prédits')
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Erreur de prédiction : {e}")
    else:
        st.error("Erreur lors de la récupération des données")
