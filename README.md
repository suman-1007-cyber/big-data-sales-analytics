# Big Data Sales Analytics Dashboard

A Streamlit-based academic project demonstrating sales analytics using a synthetic dataset of 50,000 records.

## Objective

The objective of this project is to demonstrate how a large sales dataset can be generated, cleaned, filtered, aggregated and visualized using Python-based analytics tools.

This project is a lightweight educational Big Data analytics demonstration. It does not claim to deploy a Hadoop or Spark cluster.

## Technologies

- Python
- Streamlit
- Pandas
- NumPy
- Plotly

## Features

- 50,000 synthetic sales records
- Interactive date filtering
- Region filtering
- Category filtering
- Product filtering
- Total revenue
- Total orders
- Units sold
- Average order value
- Monthly revenue
- Revenue by region
- Revenue by category
- Top products by revenue
- Top products by quantity
- Top customers
- Data quality checks
- CSV download

## Dataset

The dataset contains:

- Order ID
- Order Date
- Product ID
- Product Name
- Category
- Region
- Customer ID
- Quantity
- Unit Price
- Discount

Revenue is calculated using:

Revenue = Quantity × Unit Price × (1 − Discount)

The dataset is synthetic and contains no real customer information.

## Project Structure

```text
big-data-sales-analytics/
│
├── app.py
├── generate_data.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── data/
    └── sales_data.csv