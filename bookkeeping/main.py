import pandas as pd
import re

shopify_df = pd.read_csv("bookkeeping/jan_shopify_export.csv")
qikink_consolidated_df = pd.read_csv("bookkeeping/jan_qikink_consolidated_statement.csv")
qikink_order_df = pd.read_csv("bookkeeping/jan_qikink_order_export.csv", dtype=str)

def extract_order_number(text):
    match = re.search(r">172208_(\d+)<", text)
    return match.group(1) if match else None

def process_qikink_consolidated_df():
    # Ensure column names are consistent
    qikink_consolidated_df.columns = qikink_consolidated_df.columns.str.strip()
    # Forward fill the 'Order Reference No.' column
    qikink_consolidated_df['Order Reference No.'] = qikink_consolidated_df['Order Reference No.'].fillna(method='ffill')
    qikink_consolidated_df["Order Reference No."] = qikink_consolidated_df["Order Reference No."].astype(str).str.replace("172208_", "")
    
    # Convert 'Item Total' to numeric, coercing errors to NaN
    qikink_consolidated_df['Item Total'] = pd.to_numeric(qikink_consolidated_df['Item Total'], errors='coerce').fillna(0)
    
    # Separate shipping and non-shipping items
    df_non_shipping = qikink_consolidated_df[qikink_consolidated_df['Item'].str.lower() != 'shipping']
    df_shipping = qikink_consolidated_df[qikink_consolidated_df['Item'].str.lower() == 'shipping']
    
    # Group by 'Order Reference No.' and sum 'Item Total' for non-shipping items
    order_summary = df_non_shipping.groupby('Order Reference No.').agg(
        Order_Cost_Price=('Item Total', 'sum')
    ).reset_index()
    
    # Group by 'Order Reference No.' and sum 'Item Total' for shipping items
    shipping_summary = df_shipping.groupby('Order Reference No.').agg(
        Order_Shipping=('Item Total', 'sum')
    ).reset_index()

    # Merge both summaries
    final_summary = pd.merge(order_summary, shipping_summary, on='Order Reference No.', how='left')
    final_summary['Order_Shipping'] = final_summary['Order_Shipping'].fillna(0)  # Fill NaN with 0

    return final_summary

def main():
    # Extract order number from qikink_order_df
    qikink_order_df["Order Number"] = qikink_order_df["Order Number"].apply(extract_order_number)

    # Extract relevant data from shopify_df
    shopify_df["Name"] = shopify_df["Name"].astype(str).str.replace("#", "")
    shopify_df["Total"] = shopify_df["Total"].astype(float)
    shopify_df["Shipping"] = shopify_df["Shipping"].astype(float)
    numeric_columns = shopify_df.select_dtypes(include=["number"]).columns.tolist()

    # Group by 'Name' and sum numeric values
    shopify_df_cleaned = shopify_df.groupby("Name", as_index=False)[numeric_columns].sum()

    qikink_consolidated_df = process_qikink_consolidated_df()

    merged_df = qikink_order_df.merge(shopify_df_cleaned, left_on="Order Number", right_on="Name", how="left").merge(qikink_consolidated_df, left_on="Order Number", right_on="Order Reference No.", how="left")

    merged_df["GST on Total"] = merged_df["Total"] * 0.05
    merged_df["GST on Shipping"] = merged_df["Shipping_y"] * 0.18
    merged_df["GST on Order_Cost_Price"] = merged_df["Order_Cost_Price"] * 0.05
    merged_df["GST on Order_Shipping"] = merged_df["Order_Shipping"] * 0.18

    merged_df["P&L"] = (merged_df["Total"] + merged_df["Shipping_y"] + merged_df["GST on Total"] + merged_df["GST on Shipping"]) - (merged_df["Order_Cost_Price"] + merged_df["Order_Shipping"] + merged_df["GST on Order_Cost_Price"] + merged_df["GST on Order_Shipping"])

    total_orders = len(merged_df[merged_df['Order Number'].notna()])
    total_pnl = merged_df["P&L"].sum()
    total_row = pd.DataFrame([{col: total_pnl if col == "P&L" else (total_orders if col == "Name" else "") for col in merged_df.columns}])
    merged_df = pd.concat([merged_df, total_row], ignore_index=True)

    final_df = merged_df[["Live Date", "Name", "Order Date", "Status", "Status New", "Total", "Shipping_y", "Order_Cost_Price", "Order_Shipping", "GST on Total", "GST on Shipping", "GST on Order_Cost_Price", "GST on Order_Shipping", "P&L"]]
    final_df.to_csv("bookkeeping/monthly_pnl_torcc.csv", index=False)

main()
