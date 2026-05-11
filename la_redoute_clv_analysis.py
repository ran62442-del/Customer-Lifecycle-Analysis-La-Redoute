# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 13:25:36 2025

@author: Administrator
"""

import pandas as pd# working with dataframes
import datetime# working with dates
import missingno #package to find and display na
import numpy as np
import matplotlib.pyplot as plt
from plotnine import *#ggplot 2
import seaborn as sns
import os

#read in TRX dataset
orders = pd.read_csv('EDHEC_TRANSACTION_DATABASE_2YEARS.csv',parse_dates=['PURCHASE_DATE'])
missingno.matrix(orders)
plt.show()
#there are still some orders in the db from 31/12/2022, we will remove them
orders=orders[orders['PURCHASE_DATE']>=datetime.datetime.strptime('01/01/2023','%d/%m/%Y')]

#create a unique basket_id, assuming that all items ordered by a customer on a single day form a basket
orders['BASKET_ID'] = orders['CUSTOMER_ID'].astype(str) + "_" + orders['PURCHASE_DATE'].astype(str)
basket = orders.pivot_table(
    index='BASKET_ID',           
    columns='SUB_CATEGORY',        
    values='PURCHASE_AMOUNT',
    aggfunc='sum',
    fill_value=0
)

#read in customer info
customer=pd.read_csv('EDHEC_CUSTOMER_DATABASE.csv',parse_dates=['REGISTRATION_DATE'])
missingno.matrix(customer)
plt.show()

#missing values for gender and zipcode
customer['TOP_WOMAN'].describe()
customer['TOP_WOMAN']=customer['TOP_WOMAN'].fillna(1)
#77% women
customer['ZIP_CODE'].value_counts()
#most occuring zip code 75018
customer['ZIP_CODE']=customer['ZIP_CODE'].fillna(75018)

#conversion from department to region
dept_region_map = pd.DataFrame([
    # Auvergne-Rhône-Alpes
    ('01', 'Auvergne-Rhône-Alpes'), ('03', 'Auvergne-Rhône-Alpes'),
    ('07', 'Auvergne-Rhône-Alpes'), ('15', 'Auvergne-Rhône-Alpes'),
    ('26', 'Auvergne-Rhône-Alpes'), ('38', 'Auvergne-Rhône-Alpes'),
    ('42', 'Auvergne-Rhône-Alpes'), ('43', 'Auvergne-Rhône-Alpes'),
    ('63', 'Auvergne-Rhône-Alpes'), ('69', 'Auvergne-Rhône-Alpes'),
    ('73', 'Auvergne-Rhône-Alpes'), ('74', 'Auvergne-Rhône-Alpes'),
    # Bourgogne-Franche-Comté
    ('21', 'Bourgogne-Franche-Comté'), ('25', 'Bourgogne-Franche-Comté'),
    ('39', 'Bourgogne-Franche-Comté'), ('58', 'Bourgogne-Franche-Comté'),
    ('70', 'Bourgogne-Franche-Comté'), ('71', 'Bourgogne-Franche-Comté'),
    ('89', 'Bourgogne-Franche-Comté'), ('90', 'Bourgogne-Franche-Comté'),
    # Bretagne
    ('22', 'Bretagne'), ('29', 'Bretagne'), ('35', 'Bretagne'), ('56', 'Bretagne'),
    # Centre-Val de Loire
    ('18', 'Centre-Val de Loire'), ('28', 'Centre-Val de Loire'),
    ('36', 'Centre-Val de Loire'), ('37', 'Centre-Val de Loire'),
    ('41', 'Centre-Val de Loire'), ('45', 'Centre-Val de Loire'),
    # Corse
    ('2A', 'Corse'), ('2B', 'Corse'), ('20', 'Corse'),
    # Grand Est
    ('08', 'Grand Est'), ('10', 'Grand Est'), ('51', 'Grand Est'), ('52', 'Grand Est'),
    ('54', 'Grand Est'), ('55', 'Grand Est'), ('57', 'Grand Est'), ('67', 'Grand Est'),
    ('68', 'Grand Est'), ('88', 'Grand Est'),
    # Hauts-de-France
    ('02', 'Hauts-de-France'), ('59', 'Hauts-de-France'),
    ('60', 'Hauts-de-France'), ('62', 'Hauts-de-France'), ('80', 'Hauts-de-France'),
    # Île-de-France
    ('75', 'Île-de-France'), ('77', 'Île-de-France'), ('78', 'Île-de-France'),
    ('91', 'Île-de-France'), ('92', 'Île-de-France'), ('93', 'Île-de-France'),
    ('94', 'Île-de-France'), ('95', 'Île-de-France'),
    # Normandie
    ('14', 'Normandie'), ('27', 'Normandie'), ('50', 'Normandie'),
    ('61', 'Normandie'), ('76', 'Normandie'),
    # Nouvelle-Aquitaine
    ('16', 'Nouvelle-Aquitaine'), ('17', 'Nouvelle-Aquitaine'), ('19', 'Nouvelle-Aquitaine'),
    ('23', 'Nouvelle-Aquitaine'), ('24', 'Nouvelle-Aquitaine'), ('33', 'Nouvelle-Aquitaine'),
    ('40', 'Nouvelle-Aquitaine'), ('47', 'Nouvelle-Aquitaine'), ('64', 'Nouvelle-Aquitaine'),
    ('79', 'Nouvelle-Aquitaine'), ('86', 'Nouvelle-Aquitaine'), ('87', 'Nouvelle-Aquitaine'),
    # Occitanie
    ('09', 'Occitanie'), ('11', 'Occitanie'), ('12', 'Occitanie'), ('30', 'Occitanie'),
    ('31', 'Occitanie'), ('32', 'Occitanie'), ('34', 'Occitanie'), ('46', 'Occitanie'),
    ('48', 'Occitanie'), ('65', 'Occitanie'), ('66', 'Occitanie'), ('81', 'Occitanie'), ('82', 'Occitanie'),
    # Pays de la Loire
    ('44', 'Pays de la Loire'), ('49', 'Pays de la Loire'), ('53', 'Pays de la Loire'),
    ('72', 'Pays de la Loire'), ('85', 'Pays de la Loire'),
    # Provence-Alpes-Côte d’Azur
    ('04', 'Provence-Alpes-Côte d’Azur'), ('05', 'Provence-Alpes-Côte d’Azur'),
    ('06', 'Provence-Alpes-Côte d’Azur'), ('13', 'Provence-Alpes-Côte d’Azur'),
    ('83', 'Provence-Alpes-Côte d’Azur'), ('84', 'Provence-Alpes-Côte d’Azur'),
    # Guadeloupe
    ('971', 'Guadeloupe'),
    # Martinique
    ('972', 'Martinique'),
    # Guyane
    ('973', 'Guyane'),
    # La Réunion
    ('974', 'La Réunion'),
    # Mayotte
    ('976', 'Mayotte'),
    ('97', 'Outre-mer')     
], columns=['DEPARTMENT', 'REGION'])

# 0) SETTINGS

pd.set_option("display.max_columns", 200)
pd.set_option("display.width", 140)

START_DATE = pd.Timestamp("2023-01-01")   # assignment window start
END_DATE   = pd.Timestamp("2024-12-31")   # recency anchor upper bound (we also cap at max trx date)


# 1) LOAD DATA

orders = pd.read_csv("EDHEC_TRANSACTION_DATABASE_2YEARS.csv", parse_dates=["PURCHASE_DATE"])
customer = pd.read_csv("EDHEC_CUSTOMER_DATABASE.csv", parse_dates=["REGISTRATION_DATE"])

print("Orders shape:", orders.shape)
print("Customer shape:", customer.shape)
print("Orders columns:", list(orders.columns))
print("Customer columns:", list(customer.columns))


# 2) CLEAN ONCE (TRANSACTIONS + CUSTOMER)


# 2.1 ensure ID type consistency
orders["CUSTOMER_ID"] = orders["CUSTOMER_ID"].astype(str).str.strip()
customer["CUSTOMER_ID"] = customer["CUSTOMER_ID"].astype(str).str.strip()

# 2.2 keep only 2023+ (assignment window)
orders = orders[orders["PURCHASE_DATE"] >= START_DATE].copy()

# 2.3 essential missing checks
print("\nMissing checks (orders):")
for c in ["PURCHASE_DATE", "PURCHASE_AMOUNT", "CATEGORY", "SUB_CATEGORY", "CUSTOMER_ID"]:
    if c in orders.columns:
        print(f"{c} missing:", orders[c].isna().sum())

orders = orders.dropna(subset=["PURCHASE_DATE", "CUSTOMER_ID"]).copy()
orders["PURCHASE_AMOUNT"] = orders["PURCHASE_AMOUNT"].fillna(0)

# 2.4 Option A (your decision): keep net revenue but exclude cancellations/returns
# In practice here: drop negative amounts (typical cancellation/return lines).
# If you prefer to also drop zeros, change > 0.
orders = orders[orders["PURCHASE_AMOUNT"] > 0].copy()

# 2.5 remove duplicates
dup_n = orders.duplicated().sum()
print("Duplicate rows (orders):", dup_n)
if dup_n > 0:
    orders = orders.drop_duplicates().copy()

print("Date range after filter:", orders["PURCHASE_DATE"].min(), "to", orders["PURCHASE_DATE"].max())

# --- CUSTOMER ---
print("\nMissing checks (customer):")
if "TOP_WOMAN" in customer.columns:
    print("TOP_WOMAN missing:", customer["TOP_WOMAN"].isna().sum())
if "ZIP_CODE" in customer.columns:
    print("ZIP_CODE missing:", customer["ZIP_CODE"].isna().sum())

# Safe fills (your earlier choice)
if "TOP_WOMAN" in customer.columns:
    customer["TOP_WOMAN"] = customer["TOP_WOMAN"].fillna(1)
if "ZIP_CODE" in customer.columns:
    customer["ZIP_CODE"] = customer["ZIP_CODE"].fillna(75018)


# 3) BASKET (for cross-sell later)

# Basket definition: one customer + one day (purchase occasion)
orders["BASKET_ID"] = orders["CUSTOMER_ID"].astype(str) + "_" + orders["PURCHASE_DATE"].dt.date.astype(str)

basket = orders.pivot_table(
    index="BASKET_ID",
    columns="SUB_CATEGORY",
    values="PURCHASE_AMOUNT",
    aggfunc="sum",
    fill_value=0
)
basket_bin = (basket > 0).astype(int)


# 4) CUSTOMER-LEVEL KPIs (customer_master)

customer_agg = orders.groupby("CUSTOMER_ID", as_index=False).agg(
    monetary=("PURCHASE_AMOUNT", "sum"),
    frequency=("BASKET_ID", "nunique"),          # purchase occasions
    transactions=("PURCHASE_DATE", "count"),     # line items (optional)
    first_purchase=("PURCHASE_DATE", "min"),
    last_purchase=("PURCHASE_DATE", "max"),
)

validation = pd.DataFrame({
    "Original_Rows": [orders.shape[0]],
    "Sum_Transactions": [customer_agg["transactions"].sum()],
    "Original_Revenue": [orders["PURCHASE_AMOUNT"].sum()],
    "Sum_Monetary": [customer_agg["monetary"].sum()],
})
print("\nAggregation validation:")
print(validation)

customer_master = customer.merge(customer_agg, on="CUSTOMER_ID", how="left")

customer_master["frequency"] = customer_master["frequency"].fillna(0).astype(int)
customer_master["transactions"] = customer_master["transactions"].fillna(0).astype(int)
customer_master["monetary"] = customer_master["monetary"].fillna(0.0)

no_trx = (customer_master["frequency"] == 0).sum()
print("\nCustomer master shape:", customer_master.shape)
print("Customers with no transactions in window:", no_trx)


# 5) RFM IN ACTUAL UNITS (NO SCORING)

analysis_date = min(END_DATE, orders["PURCHASE_DATE"].max())
customer_master["recency_days"] = (analysis_date - customer_master["last_purchase"]).dt.days

worst_recency = (analysis_date - START_DATE).days + 1
customer_master["recency_days"] = customer_master["recency_days"].fillna(worst_recency).astype(int)

rfm = customer_master[customer_master["frequency"] > 0].copy()

print("\nRFM (actual units) preview:")
print(rfm[["CUSTOMER_ID", "recency_days", "frequency", "monetary"]].head())

print("\nRFM describe:")
print(rfm[["recency_days", "frequency", "monetary"]].describe())


# 6.1) R-F HEATMAP (TEXT = #CUSTOMERS, COLOR = AVG MONETARY €)

rec_bins   = [-1, 30, 90, 180, 365, np.inf]
rec_labels = ["0-30", "31-90", "91-180", "181-365", "365+"]

freq_bins   = [0, 1, 2, 4, 9, np.inf]
freq_labels = ["1", "2", "3-4", "5-9", "10+"]

rfm["rec_bin"]  = pd.cut(rfm["recency_days"], bins=rec_bins, labels=rec_labels, include_lowest=True, right=True)
rfm["freq_bin"] = pd.cut(rfm["frequency"],    bins=freq_bins, labels=freq_labels, include_lowest=True, right=True)

missing_bins = rfm[["rec_bin", "freq_bin"]].isna().sum()
print("\nMissing bins (should be 0):")
print(missing_bins)

heat = (
    rfm.dropna(subset=["rec_bin", "freq_bin"])
       .groupby(["rec_bin", "freq_bin"], observed=True)
       .agg(
           n_customers=("CUSTOMER_ID", "nunique"),
           mean_monetary=("monetary", "mean")
       )
       .reset_index()
)

count_pivot = heat.pivot(index="rec_bin", columns="freq_bin", values="n_customers").reindex(index=rec_labels, columns=freq_labels)
mon_pivot   = heat.pivot(index="rec_bin", columns="freq_bin", values="mean_monetary").reindex(index=rec_labels, columns=freq_labels)

plt.figure(figsize=(10, 6))
sns.heatmap(
    mon_pivot,
    annot=count_pivot,
    fmt=".0f",
    cmap="Greens",
    cbar_kws={"label": "Avg monetary (€)"},
)
plt.title("R-F Heatmap (Actual units): Color = Avg Monetary (€), Text = # Customers")
plt.xlabel("Frequency (purchase occasions)")
plt.ylabel("Recency (days since last purchase)")
plt.tight_layout()
plt.show()

# Revenue share by cell (approx)
heat["revenue_total"] = heat["n_customers"] * heat["mean_monetary"]
heat["revenue_share_%"] = heat["revenue_total"] / heat["revenue_total"].sum() * 100
print("\nTop cells by revenue share (approx):")
print(heat.sort_values("revenue_share_%", ascending=False).head(10))


# 6.2) LIFECYCLE GRIDS + HISTOGRAMS (PLOTNINE)


from plotnine import (
    ggplot, aes, geom_bar, geom_text, facet_grid, theme_bw, theme,
    element_blank, ggtitle, scale_x_continuous
)

# Ensure bins are strings for nice facet labels (plotnine sometimes dislikes category types)
rfm_plot = rfm.dropna(subset=["rec_bin", "freq_bin"]).copy()
rfm_plot["segmrec"]  = rfm_plot["rec_bin"].astype(str)
rfm_plot["segmfreq"] = rfm_plot["freq_bin"].astype(str)

# Keep your ordering (so facets appear in the same logical order)
rec_order  = ["0-30", "31-90", "91-180", "181-365", "365+"]
freq_order = ["1", "2", "3-4", "5-9", "10+"]

rfm_plot["segmrec"] = pd.Categorical(rfm_plot["segmrec"], categories=rec_order, ordered=True)
rfm_plot["segmfreq"] = pd.Categorical(rfm_plot["segmfreq"], categories=freq_order, ordered=True)

# ---------- A) RF QUANTITY GRID (counts of customers per cell) ----------
lcg_qty = (
    rfm_plot.groupby(["segmfreq", "segmrec"], observed=True, as_index=False)
            .agg(quantity=("CUSTOMER_ID", "nunique"))
)
lcg_qty["client"] = "client"

plot_qty = (
    ggplot(lcg_qty, aes(x="client", y="quantity", fill="quantity")) +
    theme_bw() +
    theme(panel_grid=element_blank()) +
    geom_bar(stat="identity", alpha=0.6) +
    geom_text(aes(y="quantity", label="quantity"), size=7) +
    facet_grid("segmfreq ~ segmrec") +
    ggtitle("RF quantity grid (your cutoffs)")
)
print(plot_qty)



# ---------- B) RF AVG MONETARY GRID (prof-style like your screenshot) ----------
lcg_m = (
    rfm_plot.groupby(["segmfreq", "segmrec"], observed=True, as_index=False)
            .agg(avgmvalue=("monetary", "mean"),
                 customers=("CUSTOMER_ID", "nunique"))
)
lcg_m["client"] = "client"
lcg_m["avgmvalue_round"] = lcg_m["avgmvalue"].round(0)

plot_avgm = (
    ggplot(lcg_m, aes(x="client", y="avgmvalue", fill="avgmvalue")) +
    theme_bw() +
    theme(panel_grid=element_blank()) +
    geom_bar(stat="identity", alpha=0.6) +
    geom_text(aes(y="avgmvalue", label="avgmvalue_round"), size=7) +
    facet_grid("segmfreq ~ segmrec") +
    ggtitle("RFM lifecycle plot: average monetary value (your cutoffs)")
)
print(plot_avgm)


# ---------- C) HISTOGRAM-LIKE BARS (prof vibe) ----------
# Frequency histogram (counts by frequency integer)
freq_dist = rfm_plot.groupby("frequency", as_index=False).agg(count=("CUSTOMER_ID", "nunique"))
plot_freq_hist = (
    ggplot(freq_dist, aes(x="frequency", y="count")) +
    theme_bw() +
    geom_bar(stat="identity", alpha=0.6) +
    ggtitle("Histogram of frequency values (unique baskets per customer)")
)
print(plot_freq_hist)

# Recency histogram (binned to make it readable)
# (If you prefer raw-day bars, it can get extremely spiky.)
recency_bin_width = 14  # 2 weeks; change to 7, 30, etc.
rfm_plot["recency_bin"] = (rfm_plot["recency_days"] // recency_bin_width) * recency_bin_width
rec_dist = rfm_plot.groupby("recency_bin", as_index=False).agg(count=("CUSTOMER_ID", "nunique"))

plot_rec_hist = (
    ggplot(rec_dist, aes(x="recency_bin", y="count")) +
    theme_bw() +
    geom_bar(stat="identity", alpha=0.6) +
    ggtitle(f"Histogram of recency (days), binned every {recency_bin_width} days")
)
print(plot_rec_hist)



# ---------- QUICK SANITY CHECKS ----------
print("rfm_plot rows:", len(rfm_plot))
print("lcg_qty rows:", len(lcg_qty), " (should be > 0)")
print("lcg_m rows:", len(lcg_m), " (should be > 0)")
print("freq_dist rows:", len(freq_dist), " (should be > 0)")
print("rec_dist rows:", len(rec_dist), " (should be > 0)")

# If these are 0, your bins are producing NaNs or rfm_plot is empty.

# ---------- SAVE PLOTS (GUARANTEED OUTPUT) ----------
out_dir = "outputs"
os.makedirs(out_dir, exist_ok=True)

plot_qty.save(os.path.join(out_dir, "rf_quantity_grid.png"), dpi=300, width=10, height=6)
plot_avgm.save(os.path.join(out_dir, "rf_avg_monetary_grid.png"), dpi=300, width=10, height=6)
plot_freq_hist.save(os.path.join(out_dir, "hist_frequency.png"), dpi=300, width=8, height=4)
plot_rec_hist.save(os.path.join(out_dir, "hist_recency.png"), dpi=300, width=8, height=4)

print("\nSaved plots to:", os.path.abspath(out_dir))
print(" - rf_quantity_grid.png")
print(" - rf_avg_monetary_grid.png")
print(" - hist_frequency.png")
print(" - hist_recency.png")

# ---------- OPTIONAL: DISPLAY SAVED FILES (works even in script environments) ----------
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

for fname in [
    "rf_quantity_grid.png",
    "rf_avg_monetary_grid.png",
    "hist_frequency.png",
    "hist_recency.png",
]:
    path = os.path.join(out_dir, fname)
    img = mpimg.imread(path)
    plt.figure()
    plt.imshow(img)
    plt.axis("off")
    plt.title(fname)
plt.show()

# 7) PROFILING SLICES (GENDER / REGION / COHORTS)


# 7.1 Gender profile (IMPORTANT: do NOT merge TOP_WOMAN again -> avoids TOP_WOMAN_x/y bug)
if "TOP_WOMAN" in rfm.columns:
    gender_profile = (
        rfm.groupby("TOP_WOMAN", as_index=False, observed=True)
           .agg(
               customers=("CUSTOMER_ID", "nunique"),
               avg_monetary=("monetary", "mean"),
               avg_frequency=("frequency", "mean"),
               avg_recency=("recency_days", "mean")
           )
    )
    print("\nGender profile (purchasers):")
    print(gender_profile)
else:
    print("\nGender profile skipped: TOP_WOMAN not found in rfm.")

# 7.2 Region mapping from ZIP
dept_region_map = pd.DataFrame([
    ('01', 'Auvergne-Rhône-Alpes'), ('03', 'Auvergne-Rhône-Alpes'), ('07', 'Auvergne-Rhône-Alpes'),
    ('15', 'Auvergne-Rhône-Alpes'), ('26', 'Auvergne-Rhône-Alpes'), ('38', 'Auvergne-Rhône-Alpes'),
    ('42', 'Auvergne-Rhône-Alpes'), ('43', 'Auvergne-Rhône-Alpes'), ('63', 'Auvergne-Rhône-Alpes'),
    ('69', 'Auvergne-Rhône-Alpes'), ('73', 'Auvergne-Rhône-Alpes'), ('74', 'Auvergne-Rhône-Alpes'),
    ('21', 'Bourgogne-Franche-Comté'), ('25', 'Bourgogne-Franche-Comté'), ('39', 'Bourgogne-Franche-Comté'),
    ('58', 'Bourgogne-Franche-Comté'), ('70', 'Bourgogne-Franche-Comté'), ('71', 'Bourgogne-Franche-Comté'),
    ('89', 'Bourgogne-Franche-Comté'), ('90', 'Bourgogne-Franche-Comté'),
    ('22', 'Bretagne'), ('29', 'Bretagne'), ('35', 'Bretagne'), ('56', 'Bretagne'),
    ('18', 'Centre-Val de Loire'), ('28', 'Centre-Val de Loire'), ('36', 'Centre-Val de Loire'),
    ('37', 'Centre-Val de Loire'), ('41', 'Centre-Val de Loire'), ('45', 'Centre-Val de Loire'),
    ('2A', 'Corse'), ('2B', 'Corse'), ('20', 'Corse'),
    ('08', 'Grand Est'), ('10', 'Grand Est'), ('51', 'Grand Est'), ('52', 'Grand Est'),
    ('54', 'Grand Est'), ('55', 'Grand Est'), ('57', 'Grand Est'), ('67', 'Grand Est'),
    ('68', 'Grand Est'), ('88', 'Grand Est'),
    ('02', 'Hauts-de-France'), ('59', 'Hauts-de-France'), ('60', 'Hauts-de-France'),
    ('62', 'Hauts-de-France'), ('80', 'Hauts-de-France'),
    ('75', 'Île-de-France'), ('77', 'Île-de-France'), ('78', 'Île-de-France'), ('91', 'Île-de-France'),
    ('92', 'Île-de-France'), ('93', 'Île-de-France'), ('94', 'Île-de-France'), ('95', 'Île-de-France'),
    ('14', 'Normandie'), ('27', 'Normandie'), ('50', 'Normandie'), ('61', 'Normandie'), ('76', 'Normandie'),
    ('16', 'Nouvelle-Aquitaine'), ('17', 'Nouvelle-Aquitaine'), ('19', 'Nouvelle-Aquitaine'), ('23', 'Nouvelle-Aquitaine'),
    ('24', 'Nouvelle-Aquitaine'), ('33', 'Nouvelle-Aquitaine'), ('40', 'Nouvelle-Aquitaine'), ('47', 'Nouvelle-Aquitaine'),
    ('64', 'Nouvelle-Aquitaine'), ('79', 'Nouvelle-Aquitaine'), ('86', 'Nouvelle-Aquitaine'), ('87', 'Nouvelle-Aquitaine'),
    ('09', 'Occitanie'), ('11', 'Occitanie'), ('12', 'Occitanie'), ('30', 'Occitanie'), ('31', 'Occitanie'),
    ('32', 'Occitanie'), ('34', 'Occitanie'), ('46', 'Occitanie'), ('48', 'Occitanie'), ('65', 'Occitanie'),
    ('66', 'Occitanie'), ('81', 'Occitanie'), ('82', 'Occitanie'),
    ('44', 'Pays de la Loire'), ('49', 'Pays de la Loire'), ('53', 'Pays de la Loire'),
    ('72', 'Pays de la Loire'), ('85', 'Pays de la Loire'),
    ('04', 'Provence-Alpes-Côte d’Azur'), ('05', 'Provence-Alpes-Côte d’Azur'), ('06', 'Provence-Alpes-Côte d’Azur'),
    ('13', 'Provence-Alpes-Côte d’Azur'), ('83', 'Provence-Alpes-Côte d’Azur'), ('84', 'Provence-Alpes-Côte d’Azur'),
    ('971', 'Guadeloupe'), ('972', 'Martinique'), ('973', 'Guyane'), ('974', 'La Réunion'), ('976', 'Mayotte'),
    ('97', 'Outre-mer'),
], columns=["DEPARTMENT", "REGION"])

if "ZIP_CODE" in customer_master.columns:
    customer_master["ZIP_CODE"] = customer_master["ZIP_CODE"].astype(str).str.zfill(5)
    customer_master["DEPARTMENT"] = customer_master["ZIP_CODE"].str[:2]
    customer_master = customer_master.merge(dept_region_map, on="DEPARTMENT", how="left")

    region_summary = (
        rfm[["CUSTOMER_ID", "monetary"]]
          .merge(customer_master[["CUSTOMER_ID", "REGION"]], on="CUSTOMER_ID", how="left")
          .groupby("REGION", as_index=False, observed=True)
          .agg(
              customers=("CUSTOMER_ID", "nunique"),
              total_revenue=("monetary", "sum"),
              avg_revenue=("monetary", "mean")
          )
          .sort_values("total_revenue", ascending=False)
    )
    print("\nRegion summary (purchasers):")
    print(region_summary.head(15))

# 7.3 Cohorts (registration month)
if "REGISTRATION_DATE" in customer_master.columns:
    customer_master["reg_year_month"] = customer_master["REGISTRATION_DATE"].dt.to_period("M")
    cohort_summary = (
        rfm[["CUSTOMER_ID", "monetary", "frequency", "recency_days"]]
          .merge(customer_master[["CUSTOMER_ID", "reg_year_month"]], on="CUSTOMER_ID", how="left")
          .groupby("reg_year_month", as_index=False, observed=True)
          .agg(
              customers=("CUSTOMER_ID", "nunique"),
              avg_monetary=("monetary", "mean"),
              avg_frequency=("frequency", "mean"),
              avg_recency=("recency_days", "mean"),
          )
          .sort_values("reg_year_month")
    )
    print("\nCohort summary (registration month) – last 12 rows:")
    print(cohort_summary.tail(12))


# PART 2 – PURCHASE BEHAVIOR ANALYSIS

print("\n==============================")
print("PART 2 – PURCHASE BEHAVIOR")
print("==============================")

# 2.1 Category performance
category_summary = (
    orders.groupby("CATEGORY", as_index=False)
          .agg(
              total_revenue=("PURCHASE_AMOUNT", "sum"),
              transactions=("BASKET_ID", "nunique")
          )
          .sort_values("total_revenue", ascending=False)
)
category_summary["revenue_share_%"] = category_summary["total_revenue"] / category_summary["total_revenue"].sum() * 100

print("\nCategory Summary:")
print(category_summary)

# 2.2 Sub-category performance
subcat_summary = (
    orders.groupby("SUB_CATEGORY", as_index=False)
          .agg(
              total_revenue=("PURCHASE_AMOUNT", "sum"),
              transactions=("BASKET_ID", "nunique")
          )
          .sort_values("total_revenue", ascending=False)
)
print("\nTop 15 Subcategories by Revenue:")
print(subcat_summary.head(15))

# 2.3 Seasonality
orders["year_month"] = orders["PURCHASE_DATE"].dt.to_period("M")

monthly_revenue = (
    orders.groupby("year_month")
          .agg(total_revenue=("PURCHASE_AMOUNT", "sum"))
          .sort_index()
)

monthly_baskets = (
    orders.groupby("year_month")
          .agg(baskets=("BASKET_ID", "nunique"))
          .sort_index()
)

print("\nMonthly Revenue (last 12):")
print(monthly_revenue.tail(12))

plt.figure(figsize=(12, 5))
plt.plot(monthly_revenue.index.astype(str), monthly_revenue["total_revenue"])
plt.xticks(rotation=45, ha="right")
plt.title("Monthly Revenue Trend")
plt.ylabel("Revenue (€)")
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 5))
plt.plot(monthly_baskets.index.astype(str), monthly_baskets["baskets"])
plt.xticks(rotation=45, ha="right")
plt.title("Monthly Purchase Occasions (Baskets)")
plt.ylabel("Baskets (#)")
plt.tight_layout()
plt.show()

# 2.4 Cross-sell correlations (binary co-occurrence)
corr = basket_bin.corr()
corr_pairs = (
    corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
        .stack()
        .sort_values(ascending=False)
)

print("\nTop 20 Cross-Sell Correlations (binary basket co-occurrence):")
print(corr_pairs.head(20))


# PART 3 — Retention + Customer Value (CLV) + Inactivity

print("\n==============================")
print("PART 3 – RETENTION + CLV + INACTIVITY")
print("==============================")


# 3.0 Order-level table (one row per basket/order)

orders_basket = (
    orders.groupby(["CUSTOMER_ID", "BASKET_ID"], as_index=False)
          .agg(
              PURCHASE_DATE=("PURCHASE_DATE", "min"),
              ORDER_VALUE=("PURCHASE_AMOUNT", "sum")
          )
)

obs_start = orders_basket["PURCHASE_DATE"].min()
obs_end   = orders_basket["PURCHASE_DATE"].max()
print("Observation window:", obs_start.date(), "to", obs_end.date())


# 3.1 Repurchase rate (>=2 orders in window)

cust_orders = (
    orders_basket.groupby("CUSTOMER_ID", as_index=False)
                .agg(
                    n_orders=("BASKET_ID", "nunique"),
                    total_value=("ORDER_VALUE", "sum"),
                    avg_order_value=("ORDER_VALUE", "mean"),
                    first_purchase=("PURCHASE_DATE", "min"),
                    last_purchase=("PURCHASE_DATE", "max"),
                )
)
cust_orders["recency_days"] = (obs_end - cust_orders["last_purchase"]).dt.days
cust_orders["loyal_flag"] = np.where(cust_orders["n_orders"] >= 2, "Loyal (>=2)", "Occasional (1)")

repurchase_rate = (cust_orders["n_orders"] >= 2).mean() * 100
print(f"\nAvg repurchase rate (>=2 orders): {repurchase_rate:.2f}%")


# 3.2 Loyal vs Occasional profiles + repurchase by segment
#     IMPORTANT: avoid column collisions by only merging demographics

demo_cols = ["CUSTOMER_ID"]
for c in ["TOP_WOMAN", "ZIP_CODE", "REGION", "reg_year_month", "rec_bin", "freq_bin"]:
    if c in customer_master.columns:
        demo_cols.append(c)

profile_base = cust_orders.merge(customer_master[demo_cols], on="CUSTOMER_ID", how="left")

if ("rec_bin" in profile_base.columns) and ("freq_bin" in profile_base.columns):
    profile_base["segment"] = profile_base["rec_bin"].astype(str) + " | " + profile_base["freq_bin"].astype(str)
else:
    profile_base["segment"] = pd.cut(
        profile_base["n_orders"],
        bins=[0, 1, 2, 4, 9, np.inf],
        labels=["1", "2", "3-4", "5-9", "10+"],
        include_lowest=True
    ).astype(str)

agg_dict = {
    "customers": ("CUSTOMER_ID", "nunique"),
    "avg_orders": ("n_orders", "mean"),
    "median_orders": ("n_orders", "median"),
    "avg_total_value": ("total_value", "mean"),
    "median_total_value": ("total_value", "median"),
    "avg_recency_days": ("recency_days", "mean"),
}
if "TOP_WOMAN" in profile_base.columns:
    agg_dict["female_share"] = ("TOP_WOMAN", "mean")

loyal_vs_occ = (
    profile_base.groupby("loyal_flag", as_index=False, observed=True)
                .agg(**agg_dict)
)

print("\nLoyal vs Occasional profile:")
print(loyal_vs_occ)

# RFM Segment Size and Value (Recency × Frequency)

repurchase_rfm = cust_orders.merge(
    rfm[["CUSTOMER_ID", "rec_bin", "freq_bin"]],
    on="CUSTOMER_ID",
    how="left"
).dropna(subset=["rec_bin", "freq_bin"]).copy()

table_3A = (
    repurchase_rfm.groupby(["rec_bin", "freq_bin"], as_index=False, observed=True)
    .agg(
        customers=("CUSTOMER_ID", "nunique"),
        avg_orders=("n_orders", "mean"),
        avg_total_value=("total_value", "mean"),
    )
    .sort_values("customers", ascending=False)
)

print("\nTable 3A – RFM Segment Size and Value (top 20 by size):")
print(table_3A.head(20))


# 3.3 CLV using BG/NBD (lifetimes) OR fallback proxy if lifetimes missing


from lifetimes.utils import calibration_and_holdout_data
from lifetimes import BetaGeoFitter, GammaGammaFitter
from lifetimes.plotting import plot_calibration_purchases_vs_holdout_purchases

# 0) Prepare dataframe in the exact format expected by lifetimes code on slides
# We map your columns:
# CUSTOMER_ID -> ID
# PURCHASE_DATE -> Date
# ORDER_VALUE -> Amount
df_life = orders_basket.rename(columns={
    "CUSTOMER_ID": "ID",
    "PURCHASE_DATE": "Date",
    "ORDER_VALUE": "Amount"
}).copy()

# 1) Define calibration + holdout split dates
# Use the same split_date logic you already had (example: 2024-01-01)
calibration_period_end = pd.Timestamp("2023-12-31")
observation_period_end = df_life["Date"].max()  # or a fixed end date if your assignment requires it

print("Calibration end:", calibration_period_end.date())
print("Observation end:", observation_period_end.date())

# 2) Build calibration+holdout basetable (includes frequency_cal, recency_cal, T_cal, and holdout columns)
summary_cal_holdout = calibration_and_holdout_data(
    df_life,
    customer_id_col="ID",
    datetime_col="Date",
    calibration_period_end=calibration_period_end,
    observation_period_end=observation_period_end,
    monetary_value_col="Amount",   # needed for Gamma-Gamma later
    freq="D"                       # your time unit is days
)

# 3) Fit BG/NBD model
bg = BetaGeoFitter(penalizer_coef=0.001)
bg.fit(
    summary_cal_holdout["frequency_cal"],
    summary_cal_holdout["recency_cal"],
    summary_cal_holdout["T_cal"]
)

# 4) Visual test: calibration purchases vs holdout purchases (oversampling / bias check)
plot_calibration_purchases_vs_holdout_purchases(bg, summary_cal_holdout)
plt.show()

# 5) Fit Gamma-Gamma on "returning" customers only (repeat buyers with positive monetary value)
summary_cal_holdout_returning = summary_cal_holdout[
    (summary_cal_holdout["frequency_cal"] > 0) &
    (summary_cal_holdout["monetary_value_cal"] > 0)
].copy()

gg = GammaGammaFitter(penalizer_coef=0.001)
gg.fit(
    summary_cal_holdout_returning["frequency_cal"],
    summary_cal_holdout_returning["monetary_value_cal"]
)

print(gg)

# 6) Compute CLV 
# time is in MONTHS in the slide example (3*12), while BG/NBD freq is in DAYS.
# lifetimes lets you specify freq='D' to interpret T/recency properly.
# discount_rate in the slide example is MONTHLY.
summary_cal_holdout_returning["clv_3y"] = gg.customer_lifetime_value(
    bg,
    summary_cal_holdout_returning["frequency_cal"],
    summary_cal_holdout_returning["recency_cal"],
    summary_cal_holdout_returning["T_cal"],
    summary_cal_holdout_returning["monetary_value_cal"],
    time=3*12,             # 3 years expressed in months (per slide)
    discount_rate=0.002,   # monthly discount rate (per slide)
    freq="D"               # your calibration data is in days
)

# 7) Optional: add p_alive + expected purchases for targeting
summary_cal_holdout_returning["p_alive"] = bg.conditional_probability_alive(
    summary_cal_holdout_returning["frequency_cal"],
    summary_cal_holdout_returning["recency_cal"],
    summary_cal_holdout_returning["T_cal"]
)

summary_cal_holdout_returning["exp_purchases_365d"] = bg.conditional_expected_number_of_purchases_up_to_time(
    365,
    summary_cal_holdout_returning["frequency_cal"],
    summary_cal_holdout_returning["recency_cal"],
    summary_cal_holdout_returning["T_cal"]
)

# 8) Bring customer_id back as a column and merge to your customer_master/demographics if needed
clv_table = summary_cal_holdout_returning.reset_index().rename(columns={"ID": "CUSTOMER_ID"})

print(clv_table[["CUSTOMER_ID", "clv_3y", "p_alive", "exp_purchases_365d"]].head())
print("\nCLV describe:")
print(clv_table["clv_3y"].describe())

# 9)
from lifetimes.plotting import plot_probability_alive_matrix
import matplotlib.pyplot as plt
import numpy as np


max_f = int(np.ceil(summary_cal_holdout["frequency_cal"].quantile(0.99)))  
max_r = int(np.ceil(summary_cal_holdout["recency_cal"].quantile(0.99)))

plt.figure(figsize=(10,6))
plot_probability_alive_matrix(bg, max_frequency=max_f, max_recency=max_r)
plt.title(f"Probability customer is alive (BG/NBD)\nmax_f={max_f}, max_r={max_r} (days)")
plt.show()


# 3.4 Inactivity point (gap-based) + model-based if available

orders_sorted = orders_basket.sort_values(["CUSTOMER_ID", "PURCHASE_DATE"]).copy()
orders_sorted["prev_date"] = orders_sorted.groupby("CUSTOMER_ID")["PURCHASE_DATE"].shift(1)
orders_sorted["gap_days"] = (orders_sorted["PURCHASE_DATE"] - orders_sorted["prev_date"]).dt.days

gaps = orders_sorted.dropna(subset=["gap_days"])
if gaps.shape[0] > 0:
    overall_gap_p75 = gaps["gap_days"].quantile(0.75)
    overall_gap_p90 = gaps["gap_days"].quantile(0.90)
else:
    overall_gap_p75, overall_gap_p90 = 90, 180

print(f"\nInterpurchase gap days — P75: {overall_gap_p75:.0f}, P90: {overall_gap_p90:.0f}")

inactive_threshold_days = int(max(overall_gap_p90, 180))
print("Suggested inactivity threshold (days):", inactive_threshold_days)

cust_orders["inactive_flag_gap"] = (cust_orders["recency_days"] >= inactive_threshold_days).astype(int)

# If lifetimes present, you can also flag inactive by low prob_alive
# Model-based inactivity using BG/NBD p_alive (from the prof-style CLV code)
model_inactive_cutoff = 0.30

model_status = (
    clv_table[["CUSTOMER_ID", "p_alive"]]
    .rename(columns={"p_alive": "prob_alive"})
    .copy()
)

model_status["inactive_flag_model"] = (model_status["prob_alive"] < model_inactive_cutoff).astype(int)

# Build inactivity table
inactive_table = cust_orders.merge(customer_master[demo_cols], on="CUSTOMER_ID", how="left")

# Merge model-based status if available
if model_status is not None:
    inactive_table = inactive_table.merge(model_status, on="CUSTOMER_ID", how="left")
else:
    inactive_table["prob_alive"] = np.nan
    inactive_table["inactive_flag_model"] = np.nan

# Bring RFM bins from rfm dataframe
inactive_table = inactive_table.merge(
    rfm[["CUSTOMER_ID", "rec_bin", "freq_bin"]],
    on="CUSTOMER_ID",
    how="left"
)

# Remove customers without RFM bins (non-purchasers)
inactive_table = inactive_table.dropna(subset=["rec_bin", "freq_bin"]).copy()

inactive_by_segment = (
    inactive_table.groupby(["rec_bin", "freq_bin"], as_index=False, observed=True)
    .agg(
        customers=("CUSTOMER_ID", "nunique"),
        inactive_rate_gap_pct=("inactive_flag_gap", lambda x: x.mean() * 100),
        avg_days_since_last=("recency_days", "mean"),
        avg_prob_alive=("prob_alive", "mean"),
        model_inactive_rate_pct=("inactive_flag_model", lambda x: np.nan if x.isna().all() else np.nanmean(x) * 100),
    )
    .sort_values("customers", ascending=False)
)

print("\nTable 3B – Inactivity by RFM Segment (top 20 by size):")
print(inactive_by_segment.head(20))


# 3.5 Re-engagement buckets

reengage_base = rfm[["CUSTOMER_ID", "recency_days", "frequency", "monetary"]].copy()

reengage_base["reengage_bucket"] = np.select(
    [
        (reengage_base["recency_days"] >= inactive_threshold_days) & (reengage_base["frequency"] >= 5),
        (reengage_base["recency_days"] >= inactive_threshold_days) & (reengage_base["frequency"].between(2, 4)),
        (reengage_base["recency_days"] >= inactive_threshold_days) & (reengage_base["frequency"] <= 1),
        (reengage_base["recency_days"] < inactive_threshold_days) & (reengage_base["frequency"] >= 5),
    ],
    [
        "Win-back VIP (lapsed frequent)",
        "Win-back (lapsed repeat)",
        "Reactivate (lapsed one-timer)",
        "Nurture loyal (active frequent)"
    ],
    default="Maintain / Upsell"
)

reengage_summary = (
    reengage_base.groupby("reengage_bucket", as_index=False, observed=True)
                 .agg(
                     customers=("CUSTOMER_ID", "nunique"),
                     avg_recency=("recency_days", "mean"),
                     avg_freq=("frequency", "mean"),
                     avg_monetary=("monetary", "mean"),
                 )
                 .sort_values("customers", ascending=False)
)

print("\nRe-engagement buckets (overview):")
print(reengage_summary)

plt.figure(figsize=(10, 5))
reengage_base.boxplot(column="recency_days", by="reengage_bucket", rot=45)
plt.title("Recency distribution by re-engagement bucket")
plt.suptitle("")
plt.ylabel("Days since last purchase")
plt.tight_layout()
plt.show()

print("\n✅ Script finished (Part 1 + Part 2 + Part 3).")