# Adidas US Sales Analysis

Data cleaning, exploratory data analysis (EDA) and business analysis of Adidas sales across US retailers, regions, states, products and sales channels, January 2020 to December 2021. The project turns a raw sales workbook into validated data, two interactive dashboards (HTML and Excel) and a set of business recommendations.

**Headline results:** $899.9M sales, $332.1M operating profit, 36.9% margin, 9,644 transactions.

## Table of Contents

1. Project Overview
2. Dataset
3. Tools and Skills
4. Project Workflow
5. Data Cleaning
6. Key Findings
7. Business Questions and Answers
8. Recommendations
9. Dashboards
10. Data Limitations and Assumptions
11. Repository Structure
12. How to Run
13. Author

---

## Project Overview

The goal is to turn raw sales data into reliable insight that a sales or management team can act on. The work covers:

- Cleaning and validating the raw data, and documenting every decision
- Exploring distributions, trends, relationships and outliers (see EDA_Report.md, also available as EDA_Report.pdf)
- Answering core business questions on sales, profit, margin, products, regions and channels
- Building an HTML dashboard and an Excel dashboard with filters
- Stating data limitations and assumptions clearly

## Dataset

| Item | Detail |
|---|---|
| Source file | `Adidas_US_Sales_Datasets.xlsx` |
| Period | 1 Jan 2020 to 31 Dec 2021 |
| Raw rows | 9,648 |
| Rows after cleaning | 9,644 |
| Granularity | One row per invoice line |

| Column | Description |
|---|---|
| Retailer, Retailer ID | Selling retailer (6) and its identifier |
| Invoice Date | Date of the sale |
| Region, State, City | Location (5 regions, 50 states) |
| Product | 6 categories: Men's and Women's Street Footwear, Athletic Footwear and Apparel |
| Price per Unit | Selling price in USD |
| Units Sold | Number of units sold |
| Total Sales | Revenue in USD |
| Operating Profit | Profit in USD |
| Operating Margin | Operating Profit / Total Sales |
| Sales Method | In-store, Online, Outlet |

## Tools and Skills

- **Python** (pandas, NumPy) for cleaning and EDA
- **MS Excel** for the cleaned workbook, formula-driven dashboard (SUMIFS, COUNTIFS, INDEX/MATCH, Data Validation) and native charts
- **HTML, CSS and JavaScript** for the interactive dashboard
- Skills shown: data cleaning and validation, descriptive statistics, outlier detection, correlation analysis, KPI reporting, dashboard design, business insight writing

## Project Workflow

1. Understand the data and define the business questions
2. Clean and validate the data
3. Create derived fields (Year, Month, Quarter, Weekday, Units Adjusted)
4. Explore the data (distributions, trends, segments, cross-tabs, correlations, outliers)
5. Answer the business questions and write recommendations
6. Build the dashboards and reconcile them to the source data
7. Document findings, assumptions and limitations

## Data Cleaning

| # | Issue found | Action |
|---|---|---|
| 1 | Title block and blank rows/column above the table | Removed; headers placed in row 1 |
| 2 | Retailer ID stored as a number | Converted to text (it is an identifier) |
| 3 | Spelling, case and space variants | Checked every text column; none found |
| 4 | Missing values | None found |
| 5 | Duplicate rows | None found |
| 6 | 4 rows with Units Sold = 0 and Total Sales = 0 | Removed and logged separately |
| 7 | Total Sales is exactly 10x Price x Units in 3,886 rows | Original values kept; flagged; `Units Adjusted` added (see limitations) |
| 8 | Retailer ID is not unique per retailer | Retailer name used as the key |
| 9 | City names repeat across states | State plus City used for city analysis |

Checks that passed: Operating Profit = Total Sales x Operating Margin in every row; all dates are valid and within the period. Row reconciliation: 9,648 raw rows - 4 removed = 9,644 clean rows.

## Key Findings

**By retailer**

| Retailer | Sales | Share | Margin |
|---|---|---|---|
| West Gear | $243.0M | 27.0% | 35.3% |
| Foot Locker | $220.1M | 24.5% | 36.7% |
| Sports Direct | $182.5M | 20.3% | 40.7% |
| Kohl's | $102.1M | 11.3% | 36.0% |
| Amazon | $77.7M | 8.6% | 37.1% |
| Walmart | $74.6M | 8.3% | 34.6% |

**By region**

| Region | Sales | Share | Margin |
|---|---|---|---|
| West | $269.9M | 30.0% | 33.2% |
| Northeast | $186.3M | 20.7% | 36.5% |
| Southeast | $163.2M | 18.1% | 37.1% |
| South | $144.7M | 16.1% | 42.3% |
| Midwest | $135.8M | 15.1% | 38.9% |

**By product**

| Product | Sales | Share | Margin |
|---|---|---|---|
| Men's Street Footwear | $208.8M | 23.2% | 39.6% |
| Women's Apparel | $179.0M | 19.9% | 38.3% |
| Men's Athletic Footwear | $153.7M | 17.1% | 33.7% |
| Women's Street Footwear | $128.0M | 14.2% | 35.2% |
| Men's Apparel | $123.7M | 13.8% | 36.2% |
| Women's Athletic Footwear | $106.6M | 11.8% | 36.5% |

**By sales method**

| Method | Sales | Share | Margin | Transactions | Avg sale |
|---|---|---|---|---|---|
| In-store | $356.6M | 39.6% | 35.8% | 1,740 | $204,968 |
| Outlet | $295.6M | 32.9% | 36.5% | 3,017 | $97,973 |
| Online | $247.7M | 27.5% | 39.0% | 4,887 | $50,680 |

- Sales and profit are strongly right-skewed: the mean sale ($93,312) is about ten times the median ($9,581).
- Sales move with volume (correlation 0.94 with units), and bigger deals earn lower margins (-0.38 with units).
- 2021 sales peak in July and December and dip in March.
- New York, California and Florida lead on sales; Hawaii, Washington and California have the weakest margins; Alabama, Tennessee, Michigan and Idaho have the strongest.

The full analysis is in EDA_Report.md.

## Business Questions and Answers

**1. Which retailers drive sales and profit?** West Gear, Foot Locker and Sports Direct together generate about 72% of sales. Sports Direct has the best margin (40.7%); Walmart has the lowest (34.6%).

**2. Which regions and states perform best?** The West is the largest region (30.0% of sales) but has the lowest margin (33.2%). The South is smaller (16.1%) but the most profitable per dollar (42.3%). The top states are New York ($64.2M), California ($60.2M), Florida ($59.3M), Texas ($46.4M) and South Carolina ($29.3M).

**3. Which products perform best?** Men's Street Footwear leads on sales ($208.8M) and margin (39.7%). Men's Athletic Footwear has the weakest margin (33.7%).

**4. Which sales method is most profitable?** In-store has the most sales and profit in total, and Online has the best margin (39.0%). This ranking depends on the Total Sales issue described under limitations.

**5. How do sales trend over time?** 2021 is the reliable year: sales rise to a Q3 peak (July) with a second peak in December. The 2020 versus 2021 gap is not real growth, because 2020 has far fewer records.

**6. Where is margin high but volume low?** Nebraska, Missouri, Pennsylvania, West Virginia and Illinois (margin of 40% or more, sales under $11M). Alabama, Tennessee, Michigan and Idaho have the highest margins among mid-sized states.

**7. Where is margin weakest?** Hawaii (26.3%), Washington (26.6%), Massachusetts (30.3%), Alaska (30.5%) and California (32.1%), and Women's Apparel and Men's Athletic Footwear in the West.

## Recommendations

1. Protect the three anchor retailers (about 72% of sales) and grow Kohl's, Amazon and Walmart to reduce dependence.
2. Review discounts and costs in the West and in premium-price states (Washington, Hawaii, California).
3. Scale the high-margin states (Alabama, Tennessee, Michigan, Idaho) and test growth in high-margin, low-volume states.
4. Grow the Online channel where it is weak, especially in the Northeast.
5. Plan inventory and promotions around the July and December peaks and the March dip.
6. Keep investing in Men's Street Footwear and Women's Apparel, and review price and cost for Athletic Footwear.

## Dashboards

Both dashboards use the cleaned data and show the same headline numbers with no filters: $899.9M sales, $332.1M profit, 36.9% margin, 9,644 transactions, $93,312 average sale.

**HTML dashboard** (`dashboard/adidas_sales_dashboard.html`): open it in any browser; no installation is needed. It has KPI cards, a monthly sales trend, sales and margin by retailer, region, product and sales method, a top 10 states chart, and filters for year, retailer and sales method.

**Excel dashboard** (`dashboard/excel/Adidas_US_Sales_Dashboard.xlsx`): three yellow dropdown filters (Year, Retailer, Sales method), five KPI cards and six charts (monthly trend for both years, retailer, region, product, sales method and top 10 states). It is formula-driven: the Dashboard sheet reads from a Calc sheet of SUMIFS tables, which read from the Data sheet. The monthly chart always shows both years. Images of the Excel dashboard are in the `images/` folder and are shown in EDA_Report.md. Test case: with 2021, Foot Locker and Online selected, it shows $71.9M sales, $27.3M profit, 37.9% margin and 1,248 transactions.

## Data Limitations and Assumptions

1. **Total Sales scale issue (important).** In 3,886 rows (40% of records, 96% of sales dollars) Total Sales is exactly 10x Price x Units. Operating Profit is consistent with Total Sales in every row, so Units Sold appears understated 10x in those rows, and `Units Adjusted = Total Sales / Price` is used for volume. This is an assumption to confirm with the data owner. If Total Sales were overstated instead, total sales would be about $120.2M. Rankings of regions, products and the top four retailers would not change, but Online would rank first by sales and In-store third. Margin percentages would not change.
2. **Retailer ID** is not a unique key (4 IDs for 6 retailers); analysis uses the Retailer name.
3. **Uneven coverage between years.** 2020 has about 110 records a month against about 700 in 2021, Amazon has no 2020 data and Kohl's starts in late December 2020, so year-on-year growth is unreliable.
4. The dataset has no cost, discount, customer or inventory fields, so profit drivers can be described but not proven.

## Repository Structure

```
adidas-us-sales-analysis/
|-- README.md
|-- EDA_Report.md                          # full EDA report (with dashboard images)
|-- EDA_Report.pdf                         # PDF copy of the EDA report (with images)
|-- adidas_eda.py                          # cleaning + EDA script
|-- requirements.txt                       # Python packages
|-- .gitignore
|-- data/
|   |-- Adidas_US_Sales_Datasets.xlsx      # raw data
|   `-- Adidas_US_Sales_Cleaned.xlsx       # cleaned data, removed rows, cleaning log
|-- dashboard/
|   |-- adidas_sales_dashboard.html        # interactive HTML dashboard
|   `-- excel/Adidas_US_Sales_Dashboard.xlsx   # Excel dashboard with filters and charts
|-- images/                                # dashboard images used in EDA_Report.md
`-- eda_tables/                            # CSV outputs generated by the script
```

The cleaned workbook has three sheets: `Clean_Data` (with Year, Month, Quarter, Calculated Sales, Units Check and Units Sold Adjusted), `Removed_Rows` and `Cleaning_Log`.

## How to Run

```bash
pip install -r requirements.txt
python adidas_eda.py data/Adidas_US_Sales_Datasets.xlsx
```

The script prints every table used in the reports and writes them as CSV files to `eda_tables/`. To view the dashboards, open the HTML file in a browser and the Excel file in Microsoft Excel.

## Author

**Gautam Kurpatwar**
GitHub: github.com/GK3210
