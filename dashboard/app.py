import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
# --- KONFIGURATION & PFADE ---
month_order=['January','February','March','April','May','June','July','August','September','October','November','December']
days_order = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
st.set_page_config(page_title='E-Commerce Analyse',page_icon='📊',layout='wide')

@st.cache_data
def load_advanced_data():
    # Basisdaten
    df_orders = pd.read_csv(os.path.join(SCRIPT_DIR, 'dashboard_export', 'pbi_orders.csv'))
    df_products = pd.read_csv(os.path.join(SCRIPT_DIR, 'dashboard_export', 'pbi_products.csv'))
    df_events = pd.read_csv(os.path.join(SCRIPT_DIR, 'dashboard_export', 'pbi_events.csv'))
    df_order_conversion = pd.read_csv(os.path.join(SCRIPT_DIR, 'dashboard_export', 'pbi_order_conversion.csv'))
    df_users = pd.read_csv(os.path.join(SCRIPT_DIR, 'dashboard_export', 'pbi_users.csv'))
    df_order_items=pd.read_csv(os.path.join(SCRIPT_DIR, 'dashboard_export', 'pbi_order_items.csv'))
    
    # Spezialtabelle für Kohorten (Index beim Laden beachten)
    df_cohort = pd.read_csv(os.path.join(SCRIPT_DIR, 'dashboard_export', 'pbi_retention_matrix.csv'), index_col=0)
    
    df_orders['order_date'] = pd.to_datetime(df_orders['order_date'])
    return df_orders, df_products, df_events, df_cohort,df_order_conversion, df_users,df_order_items

df_orders, df_products, df_events, df_cohort, df_order_conversion, df_users,df_order_items = load_advanced_data()


# --- HEADER ---
st.title("E-Commerce Analyse: Umsatzrückgang, Conversion und Kundenbindung")
st.markdown("""
Dieses Dashboard analysiert Transaktions- und Kundendaten, um die Ursachen des Umsatzrückgangs im Q4 zu identifizieren und konkrete Handlungsempfehlungen abzuleiten.
""")
# Sidebar
st.sidebar.header("Kontrollpanel")
selected_segments = st.sidebar.multiselect(
    "Kundensegment filtern:",
    options=df_orders['customer_segment'].unique(), #laden von der Kundenkategorie
    default=df_orders['customer_segment'].unique()
)
# Datensatz filtern:
df_filtered = df_orders[df_orders['customer_segment'].isin(selected_segments)]
if df_filtered.empty:
    st.warning(" Bitte wähle mindestens ein Kundensegment in der Seitenleiste aus, um Daten zu sehen.")
    st.stop()
#Subheader
st.subheader("_:red[KPIs]_")
total_revenue=round(df_filtered['total_amount'].sum())
order_count=df_filtered['order_id'].count()
order_value_median=df_filtered['total_amount'].median()
conversion_rate=df_order_conversion['conversion_rate'].mean()
col1,col2,col3,col4= st.columns(4)
col1.metric(label="Gesamtumsatz",value=total_revenue,delta=None,border=True,format='euro')
col2.metric(label='Anzahl Bestellungen',value=order_count,delta=None,border=True,format='localized')
col3.metric(label='Medianer Warenkorbwert',value=order_value_median,delta=None,border=True,format='euro')
col4.metric(label='Conversionrate',value=conversion_rate,delta=None,border=True,format='percent')

#Jahresverlaufs graph
monthly_revenue = df_filtered.groupby('order_Month')['total_amount'].sum().replace({}).reindex(month_order).reset_index(name='Umsatz in €')
monthly_revenue_median = df_filtered.groupby('order_Month')['total_amount'].median().reindex(month_order).reset_index()

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
    go.Bar(x=monthly_revenue['order_Month'], y=monthly_revenue['Umsatz in €'], name="Gesamtumsatz (€)", opacity=0.7, marker_color='royalblue'),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=monthly_revenue_median['order_Month'], y=monthly_revenue_median['total_amount'], name="Median Warenkorb (€)", mode='lines+markers', 
               line=dict(color='firebrick', width=3), marker=dict(size=8)),
    secondary_y=True,
)

fig.update_layout(
    title_text="Jahresverlauf: Gesamtumsatz vs. Median Warenkorbwert",
    template="plotly_white",
    hovermode="x unified",
    coloraxis_showscale=False,
    margin=dict(l=0, r=0, t=50, b=0) 
)

fig.update_yaxes(title_text="<b>Gesamtumsatz</b> (€)", secondary_y=False)
fig.update_yaxes(title_text="<b>Median Warenkorbwert</b> (€)", secondary_y=True)

st.plotly_chart(fig, width='stretch')


# --- 6. INSIGHT TEXT ---
st.info(title='Zentrales Problem:',body="""
Der Umsatzrückgang wird primär durch **sinkende Bestellfrequenzen** verursacht **nicht** durch geringere Warenkorbwerte.
""")

#7 Revenue und orders problem
st.markdown("---") # Trennlinie für eine saubere Optik
st.subheader("_:red[Umsatzverteilung & Klumpenrisiko]_")
col_pie,col_bar=st.columns(2)
with col_pie:
    st.markdown("**Umsatzanteil nach Kundensegment**")
    segment_revenue=df_filtered.groupby('customer_segment')['total_amount'].sum()
    fig_pie= px.pie(data_frame=segment_revenue,names=segment_revenue.index,values=segment_revenue.values,color_discrete_sequence=['#1f77b4', '#ff7f0e'] )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(showlegend=False,margin=dict(t=20,l=0,r=0))
    st.plotly_chart(fig_pie,width='stretch')  

with col_bar:
        st.markdown("**Median-Warenkorb nach Segment**")
        # Balkendiagramm für den Warenkorbwert
        segment_median = df_filtered.groupby('customer_segment')['total_amount'].median().reset_index()
        fig_bar = px.bar(
        segment_median, 
        x='customer_segment', 
        y='total_amount',
        color='customer_segment',
        text='total_amount',
        color_discrete_sequence=['#1f77b4', '#ff7f0e']
    )
        
        fig_bar.update_layout(
        margin=dict(t=20, b=20, l=0, r=0), 
        showlegend=False,
        xaxis_title="", 
        yaxis_title="Median Warenkorb (€)"
    )
        st.plotly_chart(fig_bar, width='stretch')

st.info(title='Erhebliches Risiko:',body="""
35% des Umsatzes werden von wenigen B2B-Großkunden generiert. 
Das B2C-Segment sorgt zwar für hohe Bestellzahlen, kann den Wegfall einzelner Großkunden aktuell jedoch nur schwer kompensieren.
""")
#8 Conversion
st.markdown("---") # Trennlinie für eine saubere Optik
st.subheader("_:red[Conversion]_")
col_funnel,col_user=st.columns(2)
with col_funnel:
    st.markdown("**Conversion Trichter nach Segment**")
    df_order_events=pd.merge(df_filtered,df_events,on='user_id')
    events_grouped=df_order_events.groupby(['event_type']).size().reset_index(name='event_count')
    events_grouped=events_grouped.sort_values(by='event_count',ascending=False).drop(events_grouped[events_grouped.event_type=='wishlist'].index)
    fig_funnel = px.funnel(events_grouped, x=events_grouped['event_count'], y=events_grouped['event_type'],labels={'event_type':'Event'},color_discrete_sequence=['#636EFA'])
    fig_funnel.update_traces(
    textinfo="value+percent initial+percent previous"
    )
    fig_funnel.update_layout(
      margin=dict(t=20, b=20, l=0, r=0), yaxis_title=""
    )
    st.plotly_chart(fig_funnel,width='stretch')
with col_user:
    st.markdown("**Käufer-Typen (Time-to-Purchase)**")
    user_order= pd.merge(df_filtered,df_users,on=['user_id'])
    user_order['order_date']=pd.to_datetime(user_order['order_date'])
    user_order['signup_date']=pd.to_datetime(user_order['signup_date'])
    user_order['days_to_order']=(user_order['order_date']-user_order['signup_date']).dt.days
    def get_buyer_type(r):
        if r <0: return 'Bestellung vor Registrierung'
        if r == 0: return 'Sofort-Kauf'
        if r >0: return 'Account Bestellung'
        return 'sonstige'
    user_order['buyer_type']=user_order['days_to_order'].apply(get_buyer_type)
    buyer_counts = user_order['buyer_type'].value_counts().reset_index()
    buyer_counts.columns = ['buyer_type', 'Anzahl']
    
    fig_buyer = px.bar(
        buyer_counts, 
        x='Anzahl', 
        y='buyer_type', 
        orientation='h', # Horizontale Balken lesen sich besser
        color='buyer_type',
        color_discrete_sequence=px.colors.qualitative.Pastel,
        text='Anzahl'
    )
    fig_buyer.update_layout(
        showlegend=False, 
        margin=dict(t=30, b=20, l=0, r=0), 
        yaxis_title="", 
        xaxis_title="Anzahl Bestellungen"
    )
    st.plotly_chart(fig_buyer, width='stretch')

st.info(title='Conversion Insights:',body="""
 Der größte Verlust im Kaufprozess entsteht zwischen Produktansicht und Warenkorb. 
Gleichzeitig deutet der hohe Anteil nicht registrierter Käufer auf ungenutztes Potenzial in der Kundenbindung hin.
""")
#9 User Verhalten
st.markdown("---") 
st.subheader("_:red[User Verhalten]_")
df_order_events['day']=df_order_events['day'].replace({
    'Monday': 'Montag',
    'Tuesday': 'Dienstag',
    'Wednesday': 'Mittwoch',
    'Thursday': 'Donnerstag',
    'Friday': 'Freitag',
    'Saturday': 'Samstag',
    'Sunday': 'Sonntag'
})
time_activity=df_order_events.groupby(['day','hour']).size().unstack()
time_activity=time_activity.reindex(days_order)
col_heat,col_line=st.columns(2)
with col_heat:
    st.markdown("**User Aktivität HeatMap**")
    fig_heat = px.imshow(
        time_activity, 
        labels=dict(x="Uhrzeit", y="", color="Aktivität"),
        color_continuous_scale='Blues',
        aspect="auto"
    )
    # Optisches Finetuning
    fig_heat.update_layout(margin=dict(t=20, b=20, l=0, r=0), yaxis_title="")
    fig_heat.update_xaxes(dtick=2) 
    st.plotly_chart(fig_heat, width='stretch')

with col_line:
     st.markdown("**Bestellfrequenz an den Wochen Tagen**")
     df_filtered['order_Day']=df_filtered['order_Day'].replace({
    'Monday': 'Montag',
    'Tuesday': 'Dienstag',
    'Wednesday': 'Mittwoch',
    'Thursday': 'Donnerstag',
    'Friday': 'Freitag',
    'Saturday': 'Samstag',
    'Sunday': 'Sonntag'
})
     line_data=df_filtered.groupby('order_Day').size()
     line_data=line_data.reindex(days_order)
     fig_line=px.line(data_frame=line_data,
            markers=True,
            labels={'order_Day':'Wochentag','value':'Anzahl Bestellungen'}
)
     fig_line.update_layout(
        margin=dict(t=20, b=20, l=0, r=0),
        xaxis_title="",
        yaxis_title="Anzahl Bestellungen",
        showlegend=False,
    )
     st.plotly_chart(fig_line, width='stretch')
st.info(title="**User Verhalten Insight**:",body="""
Die **höchste Nutzeraktivität** tritt dienstags um 12 Uhr,freitags um 20 Uhr auf und sonntags um 4 Uhr auf. 
Die **meisten Bestellungen** werden freitags generiert, während dienstags und sonntags die **niedrigere** Bestellzahlen verzeichnet werden.
Dies deutet darauf hin, dass **hohe Aktivität nicht automatisch zu mehr Käufen führt** und Marketingmaßnahmen zeitlich stärker auf konvertierungsstarke Zeiträume fokussiert werden sollten.
""")

#9 Customer Insights
st.markdown("---")
st.subheader("_:red[Kudenbindung und Sortiment]_")
st.markdown("**Kohorten-Analyse: Wie gut binden wir unsere Kunden?**")
cohort_counts=df_filtered.groupby(['cohort','cohort_index'])['user_id'].nunique().reset_index()
cohort_pivot=cohort_counts.pivot(index='cohort',columns='cohort_index',values='user_id')
cohort_size = cohort_pivot.iloc[:, 0]
retention_matrix = cohort_pivot.divide(cohort_size, axis=0)
fig_retention=px.imshow(retention_matrix, labels=dict(x="Monate nach Erstkauf", y="Erstkaufmonat",color="Retention Rate"),color_continuous_scale='Teal',text_auto='.1%',aspect="auto")
fig_retention.update_layout(
    margin=dict(t=20, b=20, l=0, r=0),
    xaxis_title="Monate nach dem ersten Kauf",
    yaxis_title="Kohorte"
)

st.plotly_chart(fig_retention, width='stretch')
st.info(title="Retention Insight",body="""
Die Gewinnung neuer Kunden verläuft kontinuierlich auf einem **hohen Niveau**. Gleichzeitig zeigt die Cohort-Analyse eine **sehr geringe** langfristige Kundenbindung:
 Bereits nach dem **ersten Monat** geht ein Großteil der Kunden verloren, während langfristig nur ca. **5%** aktiv bleiben.
""")
st.markdown("**Produkt Streudiagramm**")
fig_product=px.scatter(data_frame=df_products,x='price',y='rating')
fig_product.update_layout(
    margin=dict(t=20, b=20, l=0, r=0),
    xaxis_title="Preis in €",
    yaxis_title="Bewertung"
)
st.plotly_chart(fig_product, width='stretch')
st.info(title="Produkt Insight",body="""
Das Diagramm zeigt, dass die durchschnittlichen Produktbewertungen im Hochpreissegment deutlich **niedriger** ausfallen, obwohl Produkte in allen Preiskategorien ähnlich stark vertreten sind. 
Dies **deutet darauf hin**, dass hochpreisige Produkte entweder seltener gekauft werden oder höhere Kundenerwartungen **schwieriger** erfüllen.
""")
st.markdown("---")
st.subheader("_:red[Finale Handlungsempfehlungen]_")
st.info(title="Zentrale Erkenntnisse", body="""
• Der Umsatzrückgang wird primär durch sinkende Bestellungen verursacht nicht durch geringere Warenkorbwerte.

• Der größte Verlust im Kaufprozess entsteht zwischen Produktansicht und Warenkorb, wodurch ein erheblicher Teil der Nutzer nicht konvertiert.

• Die langfristige Kundenbindung ist kritisch niedrig: Bereits nach dem ersten Monat verliert der Shop einen Großteil seiner Kunden.

• Ein signifikanter Teil des Umsatzes stammt von wenigen B2B-Großkunden, wodurch ein erhöhtes Klumpenrisiko entsteht.
""")
st.info(title="Strategische Handlungsempfehlungen", body="""
• Marketingmaßnahmen sollten stärker auf konvertierungsstarke Zeiträume, wie Freitag Abend fokussiert werden.

• Der Kaufprozess zwischen Produktansicht und Warenkorb sollte optimiert werden, da hier der größte Nutzerverlust entsteht.

• Maßnahmen zur Kundenbindung und Reaktivierung bestehender Kunden sollten priorisiert werden, um das B2C Geschäft langfristig zu stabilsieren.

• Die Abhängigkeit von einzelnen B2B-Großkunden sollte durch den Ausbau stabiler B2C-Umsätze reduziert werden. Zusätzlich könnten Qualitätskontrollen für hochpreisige Produkte sowie ein exklusives VIP-Programm für besonders umsatzstarke B2B-Kunden etabliert werden.
""")