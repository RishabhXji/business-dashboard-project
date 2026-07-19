"""
Analytics service: loads dataset and computes KPIs, charts, and insights.
Keep computations in pandas for rapid prototyping; design is compatible with SQL-based operations.
"""
import pandas as pd
import numpy as np
from datetime import datetime

class AnalyticsService:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self._clean()

    def _clean(self):
        # Basic cleaning and feature engineering
        df = self.df
        # parse dates
        if not np.issubdtype(df['order_date'].dtype, np.datetime64):
            df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
        # drop rows with missing essential values
        df = df.dropna(subset=['order_id','order_date','sales'])
        # fill missing numeric with 0
        num_cols = ['sales','quantity','profit','discount','inventory','stock']
        for c in num_cols:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
        df['year_month'] = df['order_date'].dt.to_period('M').dt.to_timestamp()
        self.df = df

    def top_kpis(self):
        df = self.df
        total_revenue = float(df['sales'].sum())
        total_profit = float(df['profit'].sum())
        total_orders = int(df['order_id'].nunique())
        total_customers = int(df['customer_id'].nunique())
        avg_order_value = float(df.groupby('order_id')['sales'].sum().mean())
        profit_margin = float(total_profit / total_revenue) if total_revenue else 0
        # inventory turnover = cost of goods sold / average inventory; approximate with sales/inventory
        avg_inventory = df['inventory'].mean() if 'inventory' in df.columns else None
        inventory_turnover = float(df['sales'].sum() / avg_inventory) if avg_inventory and avg_inventory>0 else None
        return {
            'total_revenue': round(total_revenue,2),
            'total_profit': round(total_profit,2),
            'total_orders': total_orders,
            'total_customers': total_customers,
            'avg_order_value': round(avg_order_value,2),
            'profit_margin': round(profit_margin,4),
            'inventory_turnover': round(inventory_turnover,4) if inventory_turnover else None
        }

    def monthly_sales(self):
        df = self.df
        gp = df.groupby('year_month').agg({'sales':'sum'}).reset_index()
        gp = gp.sort_values('year_month')
        return [{'date': r['year_month'].strftime('%Y-%m-%d'), 'sales': round(r['sales'],2)} for _,r in gp.iterrows()]

    def revenue_by_category(self):
        df = self.df
        gp = df.groupby('category').agg({'sales':'sum'}).reset_index().sort_values('sales', ascending=False)
        return [{'category': r['category'], 'sales': round(r['sales'],2)} for _,r in gp.iterrows()]

    def revenue_by_region(self):
        df = self.df
        gp = df.groupby('region').agg({'sales':'sum','profit':'sum'}).reset_index().sort_values('sales', ascending=False)
        return [{'region': r['region'], 'sales': round(r['sales'],2), 'profit': round(r['profit'],2)} for _,r in gp.iterrows()]

    def top_products(self, n=10):
        df = self.df
        gp = df.groupby('product').agg({'sales':'sum','profit':'sum','quantity':'sum'}).reset_index().sort_values('sales', ascending=False).head(n)
        return gp.to_dict(orient='records')

    def bottom_products(self, n=10):
        df = self.df
        gp = df.groupby('product').agg({'sales':'sum','profit':'sum','quantity':'sum'}).reset_index().sort_values('sales', ascending=True).head(n)
        return gp.to_dict(orient='records')

    def customer_segmentation(self):
        df = self.df
        cust = df.groupby('customer_id').agg({'sales':'sum','order_id':'nunique'}).rename(columns={'order_id':'orders'}).reset_index()
        # simple RFM-like segmentation by sales
        bins = pd.qcut(cust['sales'].rank(method='first'), q=4, labels=['Bronze','Silver','Gold','Platinum'])
        cust['segment'] = bins
        seg = cust.groupby('segment').agg({'sales':'sum','orders':'sum','customer_id':'nunique'}).rename(columns={'customer_id':'customers'}).reset_index()
        return seg.to_dict(orient='records')

    def inventory_status(self):
        df = self.df
        gp = df.groupby('product').agg({'inventory':'mean','stock':'mean','sales':'sum'}).reset_index()
        gp['stock_ratio'] = gp['stock'] / (gp['inventory'].replace(0, np.nan))
        overstock = gp[gp['stock_ratio']>0.8].sort_values('stock_ratio', ascending=False).head(10).to_dict(orient='records')
        low_stock = gp[gp['stock_ratio']<0.2].sort_values('stock_ratio', ascending=True).head(10).to_dict(orient='records')
        return {'overstock': overstock, 'low_stock': low_stock}

    def profit_distribution(self):
        df = self.df
        hist = np.histogram(df['profit'].dropna(), bins=10)
        bins = [{'bin_start': float(hist[1][i]), 'bin_end': float(hist[1][i+1]), 'count': int(hist[0][i])} for i in range(len(hist[0]))]
        return bins

    def monthly_growth(self):
        gp = pd.DataFrame(self.monthly_sales())
        gp['date'] = pd.to_datetime(gp['date'])
        gp = gp.sort_values('date')
        gp['pct_change'] = gp['sales'].pct_change().fillna(0)
        latest = gp.iloc[-1]
        return {'latest_month': latest['date'].strftime('%Y-%m-%d'), 'growth_pct': round(float(latest['pct_change']),4)}

    def generate_insights(self):
        insights = []
        # Highest revenue category
        cat = self.df.groupby('category')['sales'].sum().idxmax()
        insights.append({'insight':'Highest revenue category', 'value': cat})
        # Most profitable region
        region = self.df.groupby('region')['profit'].sum().idxmax()
        insights.append({'insight':'Most profitable region', 'value': region})
        # Worst performing products (by profit)
        worst = self.df.groupby('product')['profit'].sum().sort_values().head(5)
        insights.append({'insight':'Worst performing products', 'value': worst.to_dict()})
        # Overstock products
        inv = self.inventory_status()
        insights.append({'insight':'Overstock products example', 'value': inv['overstock'][:5]})
        # Low stock
        insights.append({'insight':'Low stock products example', 'value': inv['low_stock'][:5]})
        # High discount impact
        disc = self.df[self.df['discount']>0].groupby('product').agg({'sales':'sum','profit':'sum'}).reset_index()
        if not disc.empty:
            disc['profit_pct'] = disc['profit'] / disc['sales'].replace(0, np.nan)
            impacted = disc.sort_values('profit_pct').head(5).to_dict(orient='records')
            insights.append({'insight':'High discount impact (low profit pct)', 'value': impacted})
        # Monthly sales growth
        insights.append({'insight':'Monthly sales growth', 'value': self.monthly_growth()})
        # Customer buying trends (top segments)
        insights.append({'insight':'Customer segments summary', 'value': self.customer_segmentation()})
        return insights

    def forecast_sales(self, periods=6):
        # Simple forecast using exponential smoothing on monthly sales
        ms = pd.DataFrame(self.monthly_sales())
        ms['date'] = pd.to_datetime(ms['date'])
        ms = ms.set_index('date').resample('M').sum().fillna(0)
        if len(ms) < 3:
            return []
        alpha = 0.3
        s = ms['sales'].ewm(alpha=alpha).mean()
        last = s.iloc[-1]
        forecasts = []
        for i in range(1, periods+1):
            pred = float(last)  # naive: use last smoothed value
            dt = (ms.index[-1] + pd.DateOffset(months=i)).strftime('%Y-%m-%d')
            forecasts.append({'date': dt, 'forecast': round(pred,2)})
        return forecasts
