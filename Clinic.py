
import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="ERX Dashboard",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# Custom CSS for Al-Dawaa Theme
# =========================
st.markdown("""
    <style>
    .header {
        display: flex;
        align-items: center;
        padding: 12px 20px;
        background: linear-gradient(to right, #0c1d4f, #142a63);
        border-radius: 12px;
        margin-bottom: 20px;
        text-align: center;
    }
    .header img {
        height: 60px;
        margin-right: 15px;
    }
    .header h1 {
        color: white;
        font-size: 28px;
        font-weight: 700;
        margin: 0;
        padding: 0;
        text-align: center;
    }
    </style>

    <div class="header">
        <h1>Electronic Prescriptions Dashboard</h1>
    </div>
""", unsafe_allow_html=True)
st.markdown("""
    <style>

    /* ---------- Sidebar Container ---------- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg,#ebbe34);
        padding: 20px;
    }

    /* Text inside sidebar */
    [data-testid="stSidebar"] * {
        color: #182454 !important;
        font-weight: 500;
    }

    /* Hover Animation for Sidebar Items */
    [data-testid="stSidebar"] .css-1n76uvr:hover {
        transform: scale(1.03);
        transition: 0.2s ease-in-out;
        color: #dadad9 !important;
    }

    </style>
""", unsafe_allow_html=True)
st.markdown("""
    <style>

    .gold-gradient {
        background: linear-gradient(90deg, #e7c341, #f7de87);
        padding: 12px 20px;
        border-radius: 10px;
        font-size: 20px;
        color: #0c1d4f;
        font-weight: 700;
        margin-bottom: 15px;
        text-align: center;
    }

    </style>
""", unsafe_allow_html=True)
st.sidebar.markdown("## 📃 Pages")
st.sidebar.markdown("---")
page = (st.sidebar.radio('Select Page :', ['Clinic Overview', 'Region Overview', 
                                        'PHs Overview', 'Net Profit Overview']))
st.sidebar.markdown("---")
if page == 'Clinic Overview':
    # add image 
    st.image("erx.png")
    st.markdown('<div class="gold-gradient">CLINIC Analysis Overview</div>', unsafe_allow_html=True)
    st.markdown("""
        <style>
        .kpi-card {
            background-color: #F7DB81;   /* خلفية ناعمة */
            border-radius: 12px;
            padding: 16px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s ease-in-out;
            margin: 8px;
            color: #1C2C54;
        }
        .kpi-card:hover {
            transform: scale(1.02);
            background-color: #EBBE34;   /* Primary */
            color: #182454;
        }
        .kpi-label {
            font-size: 14px;
            font-weight: 400;
            color: #1C2454;
            margin-bottom: 6px;
        }
        .kpi-value {
            font-size: 30px;
            font-weight: 600;
            color: #182460;
            margin-bottom: 4px;
        }
        .kpi-percentage {
        font-size: 14px;
        font-weight: 500;
        color: #B13BFF;  /* أخضر */
        margin-left: 6px;
        }
        .kpi-delta {
            font-size: 14px;
            font-weight: 500;
            color: #8C94AC;
        }
        .kpi-card:hover .kpi-delta {
            color: #DADAD9;
        }
        </style>
    """, unsafe_allow_html=True)
    @st.cache_data
    def load_data():
        return pd.read_excel('cleaned_erx.xlsx', index_col = 0)
    
    df = load_data()
    st.dataframe(df.head(5))
    
    # ------------------------
    # Sidebar Filters
    # ------------------------
    
    st.sidebar.markdown("## 🧭 Filters")
    st.sidebar.markdown("---")
    
    min_date = df['prescription_date'].min().date()
    max_date = df['prescription_date'].max().date()
    
    start_date, end_date = st.sidebar.date_input(
        "📅 Select Date Range:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    selected_clinic = st.sidebar.multiselect("Select Clinic(s):", sorted(df['clinic'].unique()))
    selected_status = st.sidebar.multiselect("Select Status:", sorted(df['status'].unique()))
    selected_region = st.sidebar.multiselect("Select Region:", sorted(df['region'].fillna('Unknown').astype(str).unique()))
    selected_pres_method = st.sidebar.multiselect("Select Prescription Method:", sorted(df['prescription_method'].unique()))
    selected_delivery = st.sidebar.multiselect("Select Delivery Method:", sorted(df['delivery_method'].fillna('Unknown').astype(str).unique()))
    # Apply filters
    df_filtered = df[(df['prescription_date'] >= pd.to_datetime(start_date)) &
                     (df['prescription_date'] <= pd.to_datetime(end_date))]
    
    if selected_clinic:
        df_filtered = df_filtered[df_filtered['clinic'].isin(selected_clinic)]
    if selected_status:
        df_filtered = df_filtered[df_filtered['status'].isin(selected_status)]
    if selected_region:
        df_filtered = df_filtered[df_filtered['region'].isin(selected_region)]
    if selected_pres_method:
        df_filtered = df_filtered[df_filtered['prescription_method'].isin(selected_pres_method)]
    if selected_delivery:
        df_filtered = df_filtered[df_filtered['delivery_method'].isin(selected_delivery)]
        ##KPIS
    st.markdown("## 📊 Overview Dashboard")
    
    col1, col2, col3, col4 , col5 = st.columns(5)
    
    total_orders = df_filtered.shape[0]
    total_erx = df.shape[0]
    total_per = round((total_orders / total_erx) * 100, 2)
    order_collected = df_filtered[df_filtered['status'] == 'Order Collected'].shape[0]
    perc_collected = round((order_collected / total_orders) * 100, 2)
    cancelled_orders = df_filtered[(df_filtered['status'] == 'Order Cancelled')
        | (df_filtered['status'] == 'Cancelled on POS') | (df_filtered['status'] == 'Order Cancelled By The Partner')].shape[0]
    perc_cancelled = round((cancelled_orders / total_orders) * 100, 2)
    sent_to_pos = df_filtered[df_filtered['status'] == 'Sent to POS'].shape[0]
    pending = round((sent_to_pos / total_orders) * 100, 2)
    Total_value = df_filtered['netvalue'].sum().round(2)
    
    with col1:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">⚕️ Total Orders</div>
                <div class="kpi-value">{total_orders}</div>
                <span class="kpi-percentage">({total_per}%)</span>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">✅️ Order Collected</div>
                <div class="kpi-value">{order_collected}</div>
                <span class="kpi-percentage">({perc_collected}%)</span>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">❌ Order Cancelled</div>
                <div class="kpi-value">{cancelled_orders}</div>
                 <span class="kpi-percentage">({perc_cancelled}%)</span>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">⏳ Sent to POS</div>
                <div class="kpi-value">{sent_to_pos}</div>
                <span class="kpi-percentage">({pending}%)</span>
            </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">💰 Total Net Profit</div>
                <div class="kpi-value">{Total_value}</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        # tabs for choise
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "📶 Clinic vs Status", "🕒 Clinic vs Region", "💸 Revenue"])
    custom_colors = ["#000B58","#003161" ,"#006A67" ,"#473472", "#53629E", "#87BAC3", "#D6F4ED", "#060771", "#BF1A1A", "#BF1A1A"]
    
    # Clinic vs Day
    with tab1:
        st.markdown("## 📅 Clinics Over Time")
    
        chart_type = st.radio("Select Chart Type:", ["Line Chart", "Bar Chart"], horizontal=True, key='clinic_tab1')
        
        erx_day = df.groupby('day')['clinic'].count().reset_index()
        
        if chart_type == "Line Chart":
            st.plotly_chart(
                px.line(erx_day, x="day", y="clinic", markers=True,
                        title="Clinics Count Over Time",
                        color_discrete_sequence=custom_colors),
                use_container_width=True
            )
        else:
            st.plotly_chart(
                px.bar(erx_day, x="day", y="clinic",
                       title="Clinics Count Over Time",text_auto= True,
                       color_discrete_sequence=custom_colors),
                use_container_width=True
            )
    
    with tab2:
        st.markdown("## 📶 Clinic vs Status")
        chart_type = st.radio("Select Chart Type:", ["Pie Chart", "Bar Chart"], horizontal=True, key="clinic_tab2")
        
        # Group data
        clinic_status = df.groupby(['clinic', 'status']).size().reset_index(name='count')
        
        # Select clinics
        selected_clinic = st.multiselect("Select Clinic(s):", sorted(df['clinic'].unique()), default=df['clinic'].unique(), key='clinic_status')
        
        # Filter the data
        filtered_data = clinic_status[clinic_status['clinic'].isin(selected_clinic)]
        
        if chart_type == 'Bar Chart':
            fig = px.bar(
                filtered_data,
                x='clinic',
                y='count',
                color='status',
                barmode='group',color_discrete_sequence=custom_colors,
                title="Clinic vs Status"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == 'Pie Chart':
            
            fig = px.pie(
                filtered_data,
                names='status',
                values='count',
                color='status',  # use 'status' or 'clinic', but make sure it's filtered
                title="Clinic Share by Status",color_discrete_sequence=custom_colors,
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("## 📶 Clinic vs Region")
        chart_type = st.radio("Select Chart Type:", ["Pie Chart", "Column Chart"], key='clinic_tab3')
        
        # Group data
        clinic_region = df.groupby(['clinic', 'region']).size().reset_index(name='count').sort_values(by= 'count',ascending=False)
        
        # Select clinics
        selected_clinic_r = st.multiselect("Select Clinic(s):", sorted(df['clinic'].unique()), default=df['clinic'].unique(), key="clinic_region")
        
        # Filter the data
        filtered_data3 = clinic_region[clinic_region['clinic'].isin(selected_clinic_r)]
        
        if chart_type == 'Column Chart':
            fig = px.bar(
                filtered_data3,
                x='clinic',
                y='count',
                color='region',
                barmode='group',color_discrete_sequence=custom_colors,
                title="Clinic vs Region"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == 'Pie Chart':
            
            fig = px.pie(
                filtered_data3,
                names='region',
                values='count',
                color='region',  # use 'status' or 'clinic', but make sure it's filtered
                title="Clinic Share by Region",color_discrete_sequence=custom_colors,
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)
    with tab4:
        st.markdown("## 📶 Clinic vs Net Value")
        chart_type = st.radio("Select Chart Type:", ["Pie Chart", "Column Chart"], key='clinic_tab4')
        
        # Group data
        clinic_netvalue = df.groupby('clinic')['netvalue'].sum('netvalue').reset_index().sort_values(by="netvalue" , ascending = False)
        
        # Select clinics
        selected_clinic_n = st.multiselect("Select Clinic(s):", sorted(df['clinic'].unique()), default=df['clinic'].unique(), key="clinic_net")
        
        # Filter the data
        filtered_data4 = clinic_netvalue[clinic_netvalue['clinic'].isin(selected_clinic_n)]
        
        if chart_type == 'Column Chart':
            fig = px.bar(
                filtered_data4,
                x='clinic',
                y='netvalue',
                barmode='group',color_discrete_sequence=custom_colors,
                title="Clinic vs NetValue"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == 'Pie Chart':
            
            fig = px.pie(
                filtered_data4,
                names='clinic',
                values='netvalue',
                title="Clinic Share by NetValue",color_discrete_sequence=custom_colors,
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)
if page == 'Region Overview':
    st.markdown('<div class="gold-gradient"> Region Analysis Overview </div>', unsafe_allow_html=True)
    @st.cache_data
    def load_cleaned_data():
        return pd.read_excel('cleaned_erx.xlsx', index_col = 0)
    df = load_cleaned_data()
    # filtered_data
    @st.cache_data
    def load_region_data():
        return pd.read_excel('erx_region.xlsx', index_col = 0)
    df_region = load_region_data()
    
    def collected_color(val):
        if val >= 40:
            return 'background-color:#16a34a;color:white'
        elif val >= 20:
            return 'background-color:#fde047'
        else:
            return 'background-color:#dc2626;color:white'

    def cancelled_color(val):
        if val >= 40:
            return 'background-color:#dc2626;color:white'
        elif val >= 20:
            return 'background-color:#fde047'
        else:
            return 'background-color:#16a34a;color:white'
    
    styled_table = (
    df_region
    .style
    .set_table_styles([
        {
            'selector': 'th',
            'props': [
                ('background-color', '#1f4fd8'),
                ('color', 'white'),
                ('font-weight', 'bold'),
                ('text-align', 'center')]
        },
        {
            'selector': 'td',
            'props': [
                ('text-align', 'center'),   # ✅ أهم سطر
                ('vertical-align', 'middle')]
        },
        {
            'selector': 'tr:last-child',
            'props': [
                ('background-color', '#e5e7eb'),
                ('font-weight', 'bold')]
        }])
    .map(collected_color, subset=['order_collected_%'])
    .map(cancelled_color, subset=['order_cancelled_%'])
    )
    st.dataframe(styled_table.format({'netvalue': '{:,.2f}',
                                      'order_collected_%' : '{:,.2f}',
                                     'order_cancelled_%' : '{:,.2f}',
                                     'order_pending_%' :'{:,.2f}'}))
    st.markdown("---") 
    # tabs for choise
    tab1, tab2, tab3 = st.tabs(["📈 Overview", "📶 Region vs Status", "💸 Revenue"])
    custom_colors = ["#000B58","#003161" ,"#006A67" ,"#473472", "#53629E", "#87BAC3", "#D6F4ED", "#060771", "#BF1A1A", "#BF1A1A"]

    with tab1:
        st.markdown("## 📊 ERX Distributions per Regions")
        total_orders = df['region'].value_counts().reset_index()
        
        st.plotly_chart(
                px.bar(total_orders, x="region", y="count",
                       title="ERX Distributions per Regions",text_auto= True,
                       color_discrete_sequence=custom_colors),
                use_container_width=True
            )
    
    with tab2:
        st.markdown("## 📶 Region vs Status")
        chart_type = st.radio("Select Chart Type:", ["Pie Chart", "Bar Chart"], horizontal=True, key="region_tab2")
        
        # Group data
        region_status = df.groupby(['region', 'status']).size().reset_index(name='count')
        
        # Select clinics
        selected_region = st.multiselect("Select Region(s):", sorted(df['region'].fillna('others').astype(str).unique()),
                                         default=df['region'].fillna('others').astype(str).unique(), key='region_status_tab2')
        
        # Filter the data
        filtered_data_reg = region_status[region_status['region'].isin(selected_region)]
        
        if chart_type == 'Bar Chart':
            fig = px.bar(
                filtered_data_reg,
                x='region',
                y='count',
                color='status',
                barmode='group',color_discrete_sequence=custom_colors,
                title="Region vs Status"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == 'Pie Chart':
            fig = px.pie(
                filtered_data_reg,
                names='status',
                values='count',
                color='status',  # use 'status' or 'clinic', but make sure it's filtered
                title="Region Share by Status",color_discrete_sequence=custom_colors,
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)
    with tab3:
        st.markdown("#### 📈💰📊 Region vs Net Value")
        chart_type = st.radio("Select Chart Type:", ["Line Chart", "Bar Chart"], key='region_tab4')
        
        # Group data
        region_netvalue = df.groupby('region')['netvalue'].sum('netvalue').reset_index().sort_values(by="netvalue" , ascending = False)
        
        # Select clinics
        selected_region_n = st.multiselect("Select Region(s):", sorted(df['region'].fillna('others').astype(str).unique()),
                                         default=df['region'].fillna('others').astype(str).unique(), key="region_net")
        
        # Filter the data
        filtered_df_reg = region_netvalue[region_netvalue['region'].isin(selected_region_n)]
        
        if chart_type == 'Bar Chart':
            fig = px.bar(
                filtered_df_reg,
                x='region',
                y='netvalue',
                barmode='group',color_discrete_sequence=custom_colors,
                title="Region vs NetValue"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == 'Line Chart':
            
            fig = px.line(
                filtered_df_reg,
               x = 'region', y = 'netvalue', markers = True,
                title="Region Share by NetValue",color_discrete_sequence=custom_colors
            )
            st.plotly_chart(fig, use_container_width=True)
if page == 'PHs Overview':
    st.markdown('<div class="gold-gradient"> PHs Analysis Overview </div>', unsafe_allow_html=True)
    @st.cache_data
    def load_data():
        return pd.read_excel('cleaned_erx.xlsx', index_col = 0)
    df = load_data()
    #filtered_data
    @st.cache_data
    def load_data():
        return pd.read_excel('erx_store.xlsx', index_col = 0)
    df_store = load_data()
    
    def collected_color(val):
        if val >= 40:
            return 'background-color:#16a34a;color:white'
        elif val >= 20:
            return 'background-color:#fde047'
        else:
            return 'background-color:#dc2626;color:white'

    def cancelled_color(val):
        if val >= 40:
            return 'background-color:#dc2626;color:white'
        elif val >= 20:
            return 'background-color:#fde047'
        else:
            return 'background-color:#16a34a;color:white'
    
    styled_table = (
    df_store
    .style
    .set_table_styles([
        {
            'selector': 'th',
            'props': [
                ('background-color', '#1f4fd8'),
                ('color', 'white'),
                ('font-weight', 'bold'),
                ('text-align', 'center')]
        },
        {
            'selector': 'td',
            'props': [
                ('text-align', 'center'),   # ✅ أهم سطر
                ('vertical-align', 'middle')]
        },
        {
            'selector': 'tr:last-child',
            'props': [
                ('background-color', '#e5e7eb'),
                ('font-weight', 'bold')]
        }])
    .map(collected_color, subset=['order_collected_%'])
    .map(cancelled_color, subset=['order_cancelled_%'])
    )
    st.dataframe(styled_table.format({'netvalue': '{:,.2f}',
                                      'order_collected_%' : '{:,.2f}',
                                     'order_cancelled_%' : '{:,.2f}',
                                     'order_pending_%' :'{:,.2f}'}))
    st.markdown("---") 
    # tabs for choise
    tab1, tab2, tab3 = st.tabs(["📈 Overview", "📶 PHs vs Status", "💸 Revenue"])
    custom_colors = ["#000B58","#003161" ,"#006A67" ,"#473472", "#53629E", "#87BAC3", "#D6F4ED", "#060771", "#BF1A1A", "#BF1A1A"]

    with tab1:
        st.markdown("## 📊 ERX Distributions per Stores")
        total_orders = df['store_code'].value_counts().reset_index()
        
        st.plotly_chart(
                px.line(total_orders, x="store_code", y="count",
                       title="ERX Distributions per Stores",markers= True,
                       color_discrete_sequence=custom_colors),
                use_container_width=True
            )
    
    with tab2:
        st.markdown("## 📶 Stores vs Status")
        chart_type = st.radio("Select Chart Type:", ["Pie Chart", "Bar Chart"], horizontal=True, key="store_tab2")
        
        # Group data
        store_status = df.groupby(['store_code', 'status']).size().reset_index(name='count')
        
        #top_n
        top_n = st.slider('Top N Stores', min_value = 1, max_value = 100, value=10)
        top_stores = (df['store_code'].fillna('others').astype(str).value_counts().head(top_n).index.tolist())

        # Select clinics
        selected_store = st.multiselect("Select Store(s):", sorted(df['store_code'].fillna('others').astype(str).unique()),
                                        default = top_stores, key='store_status_tab2')
        # Filter the data
        filtered_data_store = store_status[store_status['store_code'].astype(str).isin(selected_store)]
        
        if chart_type == 'Bar Chart':
            fig = px.bar(
                filtered_data_store,
                x='store_code',
                y='count',
                color='status',
                barmode='group',color_discrete_sequence=custom_colors,
                title="Store vs Status"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == 'Pie Chart':
            fig = px.pie(
                filtered_data_store,
                names='status',
                values='count',
                color='status',  # use 'status' or 'clinic', but make sure it's filtered
                title="Store Share by Status",color_discrete_sequence=custom_colors,
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)
    with tab3:
        st.markdown("#### 💰 Stores vs Net Value")
        chart_type = st.radio("Select Chart Type:", ["Line Chart", "Bar Chart"], horizontal=True, key='store__net_tab3')
        
        # Group data
        store_netvalue = df.groupby(['store_code', 'prescription_method'])['netvalue'].sum('netvalue').reset_index()

        #top_n
        top_n = st.slider('Top N Stores', min_value = 1, max_value = 100, value=10, key='top_net')
        top_stores = (df['store_code'].fillna('others').astype(str).value_counts().head(top_n).index.tolist())

        # Select clinics
        selected_store = st.multiselect("Select Store(s):", sorted(df['store_code'].fillna('others').astype(str).unique()),
                                        default = top_stores, key='store_net_tab3')
        # Filter the data
        filtered_data_store = store_netvalue[store_netvalue['store_code'].astype(str).isin(selected_store)]
        
        if chart_type == 'Bar Chart':
            fig = px.bar(
                filtered_data_store,
                x='store_code',
                y='netvalue', color = 'prescription_method', facet_col = 'prescription_method',
                barmode='group',color_discrete_sequence=['#090040', '#B13BFF'],
                title="Region vs NetValue"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == 'Line Chart':
            
            fig = px.line(
                filtered_data_store,
               x = 'store_code', y = 'netvalue', facet_col = 'prescription_method', markers = True,
                title="Stores Share by NetValue",color_discrete_sequence=['#FFCC00', '#B13BFF']
            )
            st.plotly_chart(fig, use_container_width=True)
if page == 'Net Profit Overview':
    st.markdown('<div class="gold-gradient"> 💰 Net Profit Overview </div>', unsafe_allow_html=True)
    #df
    @st.cache_data
    def load_store_data():
        return pd.read_excel('cleaned_erx.xlsx', index_col = 0)
    df = load_store_data()
    clinic_m_status = df.groupby(['clinic', 'prescription_method', 'status']).size().reset_index(name='Count')
    clinic_m_net = df.groupby(['clinic', 'prescription_method'])['netvalue'].sum('netvalue').reset_index()
    
    custom_colors = ["#000B58","#006A67" , "#53629E", "#87BAC3", "#D6F4ED", "#060771", "#BF1A1A", "#BF1A1A"]
    # select clinic
    selected_clinic5 = st.multiselect("Select Clinic(s):", sorted(df['clinic'].unique()), default=df['clinic'].unique(), key = 'clinic_net_val')
    #filter date
    clinic_m_status5 = clinic_m_status[clinic_m_status['clinic'].isin(selected_clinic5)]
    clinic_m_net5 = clinic_m_net[clinic_m_net['clinic'].isin(selected_clinic5)]
    
    fig = px.bar(
    clinic_m_status5, x = 'clinic', y = 'Count', color = 'status',
        facet_col= 'prescription_method', barmode='group')
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.bar(
    clinic_m_net5, x = 'clinic', y = 'netvalue', color = 'prescription_method', facet_col= 'prescription_method',
    color_discrete_sequence= custom_colors)
    st.plotly_chart(fig2, use_container_width=True)
