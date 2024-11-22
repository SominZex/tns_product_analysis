import streamlit as st
import pandas as pd
import plotly.express as px

def hourly_sales_analysis(data, selected_products, selected_stores):
    st.markdown("<h1 style='text-align: center; color: green;'>Hourly Sales</h1>", unsafe_allow_html=True)

    # Filter data for selected products and stores
    filtered_data = data[data['productName'].isin(selected_products) & data['storeName'].isin(selected_stores)]
    
    # Extract hour from the time column and calculate total selling price and cost price
    filtered_data['hour'] = filtered_data['time'].apply(lambda x: x.hour if pd.notnull(x) else None)
    filtered_data['total_selling_price'] = filtered_data['sellingPrice'] * filtered_data['quantity']
    filtered_data['total_cost_price'] = filtered_data['costPrice'] * filtered_data['quantity']
    
    hourly_sales = filtered_data.groupby(['productName', 'hour']).agg(
        total_selling_price=('total_selling_price', 'sum'),
        total_cost_price=('total_cost_price', 'sum'),
        quantity=('quantity', 'sum')
    ).reset_index()

    # Pivoting data for 24 columns (one for each hour) for each product
    hourly_sales_pivot = hourly_sales.pivot_table(
        index='productName', 
        columns='hour', 
        values='total_selling_price', 
        aggfunc='sum',
        fill_value=0
    ).reset_index()

    # Display the pivoted data (product-wise hourly sales)
    st.dataframe(hourly_sales_pivot)

    # Sidebar options for product-wise chart
    st.sidebar.subheader("Product-wise Hourly Sales Chart Settings")
    
    chart_type_products = st.sidebar.selectbox(
        "Select Chart Type (Product-wise)", 
        ["Line Chart", "Bar Chart", "Area Chart"], 
        key="hourly_sales_chart_type_product"
    )
    
    show_data_labels_products = st.sidebar.checkbox(
        "Show Data Labels (Product-wise)", 
        False, 
        key="hourly_sales_show_data_labels_product"
    )

    # Reshaping the data for plotting (long format)
    hourly_sales_long = hourly_sales_pivot.melt(id_vars='productName', 
                                                value_vars=hourly_sales_pivot.columns[1:], 
                                                var_name='hour', 
                                                value_name='total_selling_price')

    # Chart rendering for product-wise analysis
    if chart_type_products == "Line Chart":
        fig_products = px.line(hourly_sales_long, x='hour', y='total_selling_price', color='productName', 
                               title="Product-wise Hourly Sales",
                               labels={'total_selling_price': 'Total Sales', 'hour': 'Hour'})
    elif chart_type_products == "Bar Chart":
        fig_products = px.bar(hourly_sales_long, x='hour', y='total_selling_price', color='productName', 
                              title="Product-wise Hourly Sales",
                              labels={'total_selling_price': 'Total Sales', 'hour': 'Hour'})
    else:
        fig_products = px.area(hourly_sales_long, x='hour', y='total_selling_price', color='productName', 
                               title="Product-wise Hourly Sales",
                               labels={'total_selling_price': 'Total Sales', 'hour': 'Hour'})
    
    # Ensure all hours (0-23) are on the x-axis
    fig_products.update_xaxes(range=[0, 23], tickmode='linear', tick0=0, dtick=1)
    
    if show_data_labels_products:
        fig_products.update_traces(textposition="top center")
    
    # Display the Product-wise Hourly Sales chart
    st.plotly_chart(fig_products, use_container_width=True)

    # Aggregated Hourly Sales Analysis (with 24 columns for total sales)
    st.subheader("Total Hourly Sales")

    # Aggregated hourly sales data (with 24 columns for each hour)
    total_hourly_sales = filtered_data.groupby('hour').agg(
        total_selling_price=('total_selling_price', 'sum'),
        total_cost_price=('total_cost_price', 'sum'),
        quantity=('quantity', 'sum')
    ).reset_index()

    # Display aggregated data table (with 24 columns representing each hour)
    st.dataframe(total_hourly_sales)

    # Sidebar options for aggregated chart
    st.sidebar.subheader("Aggregated Hourly Sales Chart Settings")

    chart_type_total = st.sidebar.selectbox(
        "Select Chart Type (Aggregated)", 
        ["Line Chart", "Bar Chart", "Area Chart"], 
        key="hourly_sales_chart_type_total"
    )

    show_data_labels_total = st.sidebar.checkbox(
        "Show Data Labels (Aggregated)", 
        False, 
        key="hourly_sales_show_data_labels_total"
    )

    # Chart rendering for aggregated analysis
    if chart_type_total == "Line Chart":
        fig_total = px.line(total_hourly_sales, x='hour', y='total_selling_price',
                            title="Total Hourly Sales",
                            labels={'total_selling_price': 'Total Sales', 'hour': 'Hour'})
    elif chart_type_total == "Bar Chart":
        fig_total = px.bar(total_hourly_sales, x='hour', y='total_selling_price',
                           title="Total Hourly Sales",
                           labels={'total_selling_price': 'Total Sales', 'hour': 'Hour'})
    else:
        fig_total = px.area(total_hourly_sales, x='hour', y='total_selling_price',
                            title="Total Hourly Sales",
                            labels={'total_selling_price': 'Total Sales', 'hour': 'Hour'})

    # Ensure all hours (0-23) are on the x-axis
    fig_total.update_xaxes(range=[0, 23], tickmode='linear', tick0=0, dtick=1)

    if show_data_labels_total:
        fig_total.update_traces(textposition="outside")

    # Display the Aggregated Hourly Sales chart
    st.plotly_chart(fig_total, use_container_width=True)

