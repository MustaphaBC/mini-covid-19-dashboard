import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def get_country_data(session, country):
    rows = session.execute("""
        SELECT date, total_cases FROM stats WHERE country=%s
    """, (country,))
    df = pd.DataFrame(rows.all())
    if df.empty:
        raise ValueError(f"Aucune donnée pour le pays {country}")
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    return df

def prepare_features(df):
    df['day_number'] = (df['date'] - df['date'].min()).dt.days
    X = df['day_number'].values.reshape(-1, 1)
    y = df['total_cases'].values
    return X, y

def predict_cases(session, country, days_ahead=7):
    df = get_country_data(session, country)
    if len(df) < 10:
        raise ValueError("Pas assez de données pour le pays sélectionné")
    X, y = prepare_features(df)
    model = LinearRegression()
    model.fit(X, y)
    last_day = X[-1][0]
    future_days = np.array([last_day + i for i in range(1, days_ahead + 1)]).reshape(-1, 1)
    predictions = model.predict(future_days)
    predictions = np.clip(predictions, 0, None)  # Pas de prédictions négatives
    return future_days.flatten(), predictions

# Nouvelle fonction prenant un DataFrame directement
def predict_cases_df(df, days_ahead=7):
    if len(df) < 10:
        raise ValueError("Pas assez de données dans le DataFrame fourni")
    X, y = prepare_features(df)
    model = LinearRegression()
    model.fit(X, y)
    last_day = X[-1][0]
    future_days = np.array([last_day + i for i in range(1, days_ahead + 1)]).reshape(-1, 1)
    predictions = model.predict(future_days)
    predictions = np.clip(predictions, 0, None)
    return future_days.flatten(), predictions

if __name__ == '__main__':
    from cassandra_connect import connect_cassandra
    session = connect_cassandra()
    days, preds = predict_cases(session, 'France', 7)
    print("Prédictions des cas confirmés pour les 7 prochains jours :")
    for d, p in zip(days, preds):
        print(f"Jour {d}: {int(p)} cas")
