# CPG Promotional Lift & Optimal Pricing Engine

This engine provides a robust framework for quantifying promotional effectiveness and optimizing pricing strategies using retail scanner data. By integrating price elasticity modeling with scenario-based optimization, the system identifies the equilibrium between volume lift and margin erosion.

## Core Capabilities

### 1. Promotional Effectiveness Analytics
* **Baseline Decomposition:** Estimation of organic sales levels using historical non-promotional periods.
* **Lift Quantification:** Calculation of absolute and percentage lift, adjusted for seasonality and day-of-week effects.
* **Margin Impact:** Analysis of incremental revenue versus margin erosion to determine break-even discount thresholds.

### 2. Price Elasticity Modeling
* **Log-Log Regression:** Implementation of econometric models to derive price elasticity coefficients.
* **Segmentation:** Calculation of elasticity across different store formats (Urban vs. Suburban) and assortment types.
* **Demand Curve Mapping:** Visualization of the relationship between price depth and volume response.

### 3. Promotional Mix Optimization
* **Scenario Modeling:** Simulation of changes in discount depth (e.g., 20% to 15%) and frequency.
* **Profit Maximization:** Utilization of `scipy.optimize` to find the mathematical "sweet spot" for promotional depth that maximizes total margin.

### 4. Dynamic Recommendation Engine
* **Rule-Based Logic:** Automated pricing adjustments based on inventory levels, competitor activity, and holiday flags.
* **Real-time Feedback:** Recommendations for price adjustments with projected volume impacts.

## Project Structure

```text
├── data/               # Raw scanner data (Rossmann Store Sales)
├── src/
│   ├── analysis.py     # Lift and ROI logic
│   ├── modeling.py     # Elasticity regression models
│   ├── optimization.py # Scenario simulation and solver
│   └── recommendation.py# Dynamic pricing engine
├── main.py             # Integrated pipeline execution
└── requirements.txt    # System dependencies
```

## Setup & Execution

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Pipeline:**
   ```bash
   python main.py
   ```

## Technical Implementation Notes

The engine utilizes a log-log regression framework where $\log(Sales) = \beta_0 + \beta_1 \cdot \log(Price) + \dots$. The coefficient $\beta_1$ directly represents the price elasticity of demand. Optimization is performed using the L-BFGS-B algorithm to handle constrained price boundaries.

## Interview Talking Points (Resume Guide)

If you are explaining this project in an interview or on your resume, here is the breakdown of the logic:

### 1. Promotional Lift Analysis
* **The Problem:** How do we know if a 20% discount is actually "worth it"?
* **The Solution:** I established a **Baseline Sales** model by averaging sales on non-promo days (segmented by Day of Week). I then calculated the **Incremental Volume** by comparing actual promo sales against this baseline.
* **Key Metric:** *Promotional Lift %* (Total Promo Sales / Baseline Expected).

### 2. Price Elasticity Modeling
* **The Logic:** I implemented a **Log-Log Regression** model. In economics, the coefficient of a log-log model represents **constant elasticity**.
* **Interpretation:** If the elasticity is -2.5, it means for every 1% increase in price, volume drops by 2.5%. This is the foundation for any pricing strategy.
* **Feature Engineering:** Since unit prices weren't direct, I created a price proxy by mapping the Promo flag to a 20% discount depth.

### 3. Price Optimization
* **The Objective:** Maximizing total profit, not just volume.
* **The Methodology:** I built a profit function: $Profit = [Volume(P)] \times [Price - Cost]$.
* **Optimization:** I used `scipy.optimize.minimize` to solve for the price point that balances the trade-off between higher margins per unit and lower total volume.

---
*Note: This structure demonstrates a full end-to-end data science workflow: Data Cleaning -> Descriptive Analytics -> Statistical Modeling -> Business Optimization.*
