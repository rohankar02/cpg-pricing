# CPG Pricing Strategy & Margin Optimization Engine

A data-driven tool to help retail managers set the best prices and evaluate promotions.

## How it Works (Interview-Ready Logic)

This project answers three business questions:

### 1. Does our promotion work? (Lift Analysis)
I compared sales during promotional weeks to sales during normal weeks. This showed me the **"Lift"**—exactly how many extra units we sell when we put an item on sale.

### 2. How sensitive are our customers? (Price Sensitivity)
I calculated **Price Elasticity**. If we drop the price by 20%, does our volume go up enough to cover the cost? I used historical data to find this "Sensitivity Score."

### 3. What is the perfect price? (Profit Optimization)
Instead of guessing, I built a **Simulation**. The code tests every price point from £7 to £13 (in 10-cent increments) and calculates the projected profit for each. It then simply picks the one that makes the most money.

---
**Why this matters:** This tool replaces "gut feeling" with a mathematical simulation, ensuring we don't leave money on the table by over-discounting or over-pricing.

---
*Note: This project demonstrates a full end-to-end consulting workflow: Data Cleaning -> Descriptive Analytics -> Scenario Simulation -> Final Recommendation.*
