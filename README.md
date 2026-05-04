# CPG Pricing Strategy & Margin Optimization Engine

A quantitative framework developed to analyze promotional effectiveness and optimize retail pricing architectures using high-granularity scanner data. This tool integrates econometric modeling with non-linear optimization to balance the trade-off between volume lift and margin erosion.

## Executive Summary

The retail sector faces significant margin pressure due to over-promotion and suboptimal pricing. This project provides a data-driven approach to:
1.  **Quantify Promotional ROI:** Isolating the true incremental lift from trade promotions by establishing accurate sales baselines.
2.  **Model Price Sensitivity:** Determining the constant elasticity of demand across store segments using log-log regression.
3.  **Optimize Margin:** Identifying the mathematical equilibrium between price points and quantity demanded to maximize total profitability.

## Methodology

### 1. Promotional Lift Decomposition
Incremental volume is isolated using a day-of-week adjusted baseline model. By filtering for non-promotional periods, we establish a control "organic" sales rate, allowing for the quantification of the actual lift attributed to trade activities.

### 2. Econometric Elasticity Modeling
We utilize a constant-elasticity model where $\log(Q) = \alpha + \beta \log(P) + \epsilon$. The coefficient $\beta$ represents the price elasticity of demand, providing a robust metric for consumer price sensitivity that is comparable across categories and store formats.

### 3. Non-Linear Margin Optimization
The objective function maximizes total profit:
$$\text{Profit} = V_0 \left(\frac{P_{new}}{P_{base}}\right)^\beta \times (P_{new} - \text{Cost})$$
We employ the L-BFGS-B algorithm to solve for the price point that maximizes this function within operationally feasible boundaries (+/- 30% price depth).

## Key Components

*   `engine.py`: The core analytical engine containing the preprocessing pipeline, econometric models, and optimization solver.
*   `data/`: Retail scanner data (Rossmann Store Sales) including historical sales, promo flags, and store metadata.

---
**Technical Note:** This engine is built using Python, Scipy, and Statsmodels. It assumes a constant elasticity of demand within the local price range and utilizes DOW-seasonality adjustments for baseline estimation.
