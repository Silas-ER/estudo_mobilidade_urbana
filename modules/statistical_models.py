from prophet import Prophet
import pandas as pd

def prophet_forecast(df, periods=365): # prevendo os proximos 2 anos

    df = df.rename(columns={'Mes_Ano': 'ds', 'Qtd_Viagens': 'y'})
    df['ds'] = pd.to_datetime(df['ds'])
    df = df.groupby(pd.Grouper(key='ds', freq='M')).sum().reset_index() #reduzir a densidade dos dados

    model = Prophet(yearly_seasonality=True, daily_seasonality=False)
    model.fit(df)

    future = model.make_future_dataframe(periods=periods, freq='M')
    forecast = model.predict(future)

    fig = model.plot(forecast)

    return fig
