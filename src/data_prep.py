import pandas as pd
def prep_orders(df):
    df = df.dropna(how="any")#fehlende Werte entfernen
    df["order_date"] = pd.to_datetime(df["order_date"])#Date-Format für die Spalte um Zeit basierte Analysen durchzuführen
    df['order_Month'] = df["order_date"].dt.month
    df['order_Day'] = df["order_date"].dt.day_name()
    df['total_amount']=pd.to_numeric(df['total_amount'])
    return df
def prep_users(df):
    df.drop(['name','email'],axis=1,inplace=True)#irrelevant für die Analyse (dürden nicht verarbeitet werden DSGVO)
    df['signup_date'] = pd.to_datetime(df["signup_date"])
    df['signup_month'] = df["signup_date"].dt.month
    return df
def prep_order_items(df):
    df_grouped=df.rename(columns={'item_total':'revenue'})
    return df_grouped
def prep_reviews(df):
    def get_rating_category(r):#einteilen in sinnvolle Rating Kategorien
        if r >= 4.5: return 'top_rated'
        if r >= 3.5: return 'good'
        if r >= 2.5: return 'average'
        return 'poor'
    df['review_date'] = pd.to_datetime(df["review_date"])
    df['rating_category']= df['rating'].apply(get_rating_category)
    return df
def prep_products(df):
    q25=df['price'].quantile(0.25)
    q50=df['price'].quantile(0.5)
    q75=df['price'].quantile(0.75)
    def get_rating_category(r):
        if r >= 4.5: return 'top_rated'
        if r >= 3.5: return 'good'
        if r >= 2.5: return 'average'
        return 'poor'
    def get_price_category(n):#einteilen in sinnvolle Preiskategorien anhand der vorhandenen Preise
        match n:
            case n if n <= q25 :
                return 'low'
            case n if n <= q50:
                return 'medium'
            case n if n <=  q75:
                return 'high' 
            case n if n>  q75:
                return 'luxury'
        
        return n
    df['price_category']= df['price'].apply(get_price_category)
    df['rating_category']= df['rating'].apply(get_rating_category)
    return df
def prep_events(df):
    df["event_timestamp"] = pd.to_datetime(df["event_timestamp"])
    df['hour']= df["event_timestamp"].dt.hour
    def get_time_of_day(r):
        if 5<= r < 12: return 'morning'
        if 12<= r < 17: return 'afternoon'
        if 17<= r < 22 : return 'evening'
        return 'night'
    df ['time_of_day']=df['hour'].apply(get_time_of_day)
    df['day']=df['event_timestamp'].dt.day_name()
    return df
