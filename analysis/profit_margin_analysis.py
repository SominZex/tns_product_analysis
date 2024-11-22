import streamlit as st
import pandas as pd
import plotly.express as px

def profit_margin_analysis(data, selected_products):
    st.markdown("<h1 style='text-align: center; color: green;'>Profit Analysis by Product</h1>", unsafe_allow_html=True)

    # Filter data for selected products
    filtered_data = data[data['productName'].isin(selected_products)]

    # Ensure sellingPrice, costPrice, and quantity are numeric
    filtered_data['sellingPrice'] = pd.to_numeric(filtered_data['sellingPrice'], errors='coerce')
    filtered_data['costPrice'] = pd.to_numeric(filtered_data['costPrice'], errors='coerce')
    filtered_data['quantity'] = pd.to_numeric(filtered_data['quantity'], errors='coerce')

    # Calculate total selling price and total cost price by multiplying by quantity
    filtered_data['total_sellingPrice'] = filtered_data['sellingPrice'] * filtered_data['quantity']
    filtered_data['total_costPrice'] = filtered_data['costPrice'] * filtered_data['quantity']

    # Calculate profit margin per product (unit-based, without multiplying by quantity)
    filtered_data['profit_margin'] = ((filtered_data['sellingPrice'] - filtered_data['costPrice']) / 
                                       filtered_data['sellingPrice']) * 100

    # Round profit margin and add percentage symbol
    filtered_data['profit_margin'] = filtered_data['profit_margin'].round(2).astype(str) + '%'

    # Group by productName and sum the total sellingPrice and total costPrice
    product_grouped = (filtered_data.groupby('productName')
                       .agg({'total_sellingPrice': 'sum', 'total_costPrice': 'sum'})
                       .reset_index())

    # Calculate average profit margin based on summed values
    product_grouped['avg_profit_margin'] = ((product_grouped['total_sellingPrice'] - product_grouped['total_costPrice']) / 
                                             product_grouped['total_sellingPrice']) * 100

    # Round avg_profit_margin and add percentage symbol
    product_grouped['avg_profit_margin'] = product_grouped['avg_profit_margin'].round(2).astype(str) + '%'

    # For each product, add the profit margin (calculated per unit) by merging the unique profit margin per product
    product_grouped['profit_margin'] = filtered_data.drop_duplicates(subset='productName')['profit_margin'].values

    # Display data table with all required features, including total_sellingPrice, total_costPrice, and profit_margin
    st.dataframe(product_grouped)

    # Sidebar options for chart customization
    st.sidebar.subheader("Profit Margin Chart Settings")
    
    # Assign unique keys to interactive elements
    chart_type = st.sidebar.selectbox("Select Chart Type", ["Bar Chart", "Scatter Plot"], key="profit_margin_chart_type")
    show_data_labels = st.sidebar.checkbox("Show Data Labels", False, key="profit_margin_show_data_labels")

    # Chart rendering based on user selection
    color_palette = px.colors.qualitative.Set3

    if chart_type == "Bar Chart":
        fig = px.bar(product_grouped, x='productName', y='avg_profit_margin', title="Average Profit Margin by Product",
                     labels={'avg_profit_margin': 'Profit Margin (%)'}, color='productName', color_discrete_sequence=color_palette)
        
        # Add data labels if checkbox is selected
        if show_data_labels:
            fig.update_traces(text=product_grouped['avg_profit_margin'], textposition="inside")
            
    elif chart_type == "Scatter Plot":
        fig = px.scatter(product_grouped, x='productName', y='avg_profit_margin', title="Profit Margin by Product",
                         labels={'avg_profit_margin': 'Profit Margin (%)'}, color='productName', color_discrete_sequence=color_palette)

        # Add data labels if checkbox is selected
        if show_data_labels:
            fig.update_traces(text=product_grouped['avg_profit_margin'], textposition="top center")

    st.plotly_chart(fig, use_container_width=True)
