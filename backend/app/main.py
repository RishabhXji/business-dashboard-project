"""
FastAPI backend exposing REST APIs for dashboard and analytics.
Run: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os

from .database import load_data
from .services.analytics import AnalyticsService

app = FastAPI(title='Retail Sales & Inventory Analytics Dashboard')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load dataset once on startup
DATA_DF = None
ANALYTICS = None

@app.on_event('startup')
def startup_event():
    global DATA_DF, ANALYTICS
    try:
        DATA_DF = load_data()
        ANALYTICS = AnalyticsService(DATA_DF)
        print('Data loaded, records:', len(DATA_DF))
    except Exception as e:
        print('Warning: failed to load data on startup:', e)

@app.get('/health')
def health():
    return {'status':'ok'}

@app.get('/dashboard')
def get_dashboard():
    if ANALYTICS is None:
        raise HTTPException(status_code=500, detail='Analytics not initialized. Ensure dataset is available.')
    kpis = ANALYTICS.top_kpis()
    monthly = ANALYTICS.monthly_sales()
    by_cat = ANALYTICS.revenue_by_category()
    by_reg = ANALYTICS.revenue_by_region()
    top_products = ANALYTICS.top_products(10)
    bottom_products = ANALYTICS.bottom_products(10)
    return {
        'kpis': kpis,
        'monthly_sales': monthly,
        'revenue_by_category': by_cat,
        'revenue_by_region': by_reg,
        'top_products': top_products,
        'bottom_products': bottom_products
    }

@app.get('/sales')
def get_sales(start_date: str = Query(None), end_date: str = Query(None), region: str = Query(None), category: str = Query(None)):
    if ANALYTICS is None:
        raise HTTPException(status_code=500, detail='Analytics not initialized.')
    df = ANALYTICS.df
    if start_date:
        df = df[df['order_date']>=start_date]
    if end_date:
        df = df[df['order_date']<=end_date]
    if region:
        df = df[df['region']==region]
    if category:
        df = df[df['category']==category]
    # return aggregated sales by day
    res = df.groupby(df['order_date'].dt.date).agg({'sales':'sum','profit':'sum','quantity':'sum'}).reset_index()
    res['order_date'] = res['order_date'].astype(str)
    return res.to_dict(orient='records')

@app.get('/products')
def get_products(limit: int = 100):
    if ANALYTICS is None:
        raise HTTPException(status_code=500, detail='Analytics not initialized.')
    return ANALYTICS.top_products(n=limit)

@app.get('/customers')
def get_customers(limit: int = 100):
    if ANALYTICS is None:
        raise HTTPException(status_code=500, detail='Analytics not initialized.')
    # simple listing
    df = ANALYTICS.df
    cust = df.groupby('customer_id').agg({'customer_name':'first','sales':'sum','order_id':'nunique'}).rename(columns={'order_id':'orders'}).reset_index().sort_values('sales', ascending=False).head(limit)
    return cust.to_dict(orient='records')

@app.get('/inventory')
def get_inventory():
    if ANALYTICS is None:
        raise HTTPException(status_code=500, detail='Analytics not initialized.')
    return ANALYTICS.inventory_status()

@app.get('/forecast')
def get_forecast(periods: int = 6):
    if ANALYTICS is None:
        raise HTTPException(status_code=500, detail='Analytics not initialized.')
    return ANALYTICS.forecast_sales(periods=periods)

@app.get('/insights')
def get_insights():
    if ANALYTICS is None:
        raise HTTPException(status_code=500, detail='Analytics not initialized.')
    insights = ANALYTICS.generate_insights()
    return {'insights': insights}
