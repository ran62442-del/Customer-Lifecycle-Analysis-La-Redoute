# La Redoute Customer Lifecycle Analysis

## Overview
This project analyzes customer purchasing behavior for La Redoute, a French multichannel retailer specializing in fashion and home décor.

The objective was to identify customer segments, analyze purchasing behavior, evaluate retention patterns, and estimate Customer Lifetime Value (CLV) using transaction data from 2023–2024.

The project was completed as part of the Customer Lifecycle Management course at EDHEC Business School.

---

## Business Questions
The analysis focused on the following questions:

- Which customer segments generate the most value?
- What purchasing behaviors indicate customer loyalty?
- Which product categories and subcategories perform best?
- What seasonal purchasing patterns can be identified?
- Which products are frequently purchased together?
- When do customers become inactive?
- What opportunities exist for customer re-engagement?

---

## Dataset
The project used customer and transaction datasets containing:

- Customer demographics and registration information
- Transaction history from 2023–2024
- Product category and subcategory information
- Purchase amounts and purchase dates

The original dataset is not included due to academic and privacy restrictions.

---

## Tools & Technologies
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotnine
- Lifetimes (BG/NBD & Gamma-Gamma models)
- Jupyter Notebook

---

## Key Analyses

### Customer Segmentation
- RFM segmentation (Recency, Frequency, Monetary)
- Customer profiling by gender, region, and cohort
- Lifecycle grids and heatmaps

### Purchase Behavior Analysis
- Product category and subcategory analysis
- Seasonality and monthly revenue trends
- Cross-sell analysis using basket correlations

### Retention & Customer Value
- Repurchase rate analysis
- Churn and inactivity analysis
- Customer Lifetime Value (CLV) prediction using BG/NBD and Gamma-Gamma models
- Re-engagement opportunity identification

---

## Key Insights
- Customer behavior is very one-time-heavy: median frequency is 1, and 4,915 customers are occasional buyers. This means retention, not acquisition only, is the main growth lever.
- A small VIP group drives strong value: customers with 0–30 recency + 10+ purchases are only 160 customers, but contribute about 12.1% of revenue. Protect and reward them.
- Large reactivation opportunity: 2,610 customers bought once and have been inactive for 365+ days. They are low value individually, but huge in volume.
- Maison dominates the business: Maison generates 62.4% of revenue, led by Meuble and Linge de Maison. La Redoute’s revenue engine is more home-focused than fashion-focused.
- Loyal customers are much more valuable: loyal customers average €653 total value vs €137 for one-time buyers, and they are more recent. Moving customers from first to second purchase matters a lot.
- Win-back should be segmented: lapsed one-timers need low-cost reactivation, while 175 lapsed VIPs have high average value (€1,147) and deserve personalized win-back campaigns.



---

## Sample Visualizations
The project includes:
- RFM heatmaps
- Lifecycle grids
- Revenue trend charts
- Frequency and recency distributions
- CLV and probability-alive visualizations

