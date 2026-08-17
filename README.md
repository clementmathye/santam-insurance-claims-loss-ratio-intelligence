# Santam General Insurance | Claims & Loss-Ratio Intelligence Dashboard

An enterprise short-term insurance business intelligence model built in Power BI Desktop. This project evaluates **R343.75M** in underwritten policy premiums against claims exposure, tracking portfolio loss ratios, operational settlement velocity, and claims frequency across 5 major insurance classes.

![Dashboard Preview]
<img width="1182" height="684" alt="dashboard_preview" src="https://github.com/user-attachments/assets/c84f4905-401d-439e-b308-6f0f6af3adec" />


---

## Executive Summary & Key Findings

* **Blended Portfolio Loss Ratio (46.14%):** Portfolio underwriting remains profitable overall, staying well within the industry standard benchmark ceiling of **65.00%**.
* **Personal Motor Underwriting Alert (98.77% Loss Ratio):** Personal Motor is severely unprofitable and breaching risk tolerances. Recommended strategic action: immediate **12% – 15% rate review** on high-risk driver segments and telematics-based risk pricing.
* **Operational Claims Velocity (17.99 Days Avg TAT):** Western Cape registered the fastest settlement velocity at **16.2 days** via digitized assessor routing, while Commercial Fleet claims average **23.16 days** due to complex multi-party liability validation.
* **Claims Repudiation Governance (12.4%):** Active repudiation controls mitigated fraudulent and out-of-scope losses, protecting statutory solvency margins.

---

## Data Architecture & Dimensional Model

Structured using a **Relational Star Schema** to optimize DAX performance and slice underwriting metrics dynamically:
```
              +--------------+
              |   Dim_Date   |
              +------+-------+
                     | (1:*)
                     |
+-----------------+  |  +------------------+
| Dim_Underwriting +--+->|   Fact_Claims    |
|     Class        |(1:*)| (Settlement/TAT) |
+-----------------+  |  +---+--------------+
                      |      | (*:1)
+-----------------+   |      |
|   Dim_Region     +--+------+
|  (SA Provinces)  |(1:*)    |
+-----------------+   |      v
                      |  +--------------+
                      +->| Fact_Policies|
                    (1:*)|  (Inception) |
                         +--------------+
```

---

## Core DAX Formulations

```dax
// 1. Earned Premium Total
Total Premium = SUM(Fact_Policies[AnnualPremium])

// 2. Incurred Losses (Settled & Approved)
Incurred Claims = 
CALCULATE(
    SUM(Fact_Claims[ClaimAmount]),
    Fact_Claims[ClaimStatus] IN {"Settled", "Approved"}
)

// 3. Loss Ratio %
Portfolio Loss Ratio % = 
DIVIDE([Incurred Claims], [Total Premium], 0)

// 4. Claims Frequency %
Claims Frequency % = 
DIVIDE(
    DISTINCTCOUNT(Fact_Claims[ClaimID]),
    DISTINCTCOUNT(Fact_Policies[PolicyID]),
    0
)

// 5. Operational Settlement Turnaround Time (TAT)
Avg Settlement TAT (Days) = 
CALCULATE(
    AVERAGEX(
        Fact_Claims,
        DATEDIFF(Fact_Claims[IncidentDate], Fact_Claims[SettlementDate], DAY)
    ),
    Fact_Claims[ClaimStatus] = "Settled"
)
```

---

## Repository Structure

```
├── assets/
│   └── dashboard_preview.png        # High-resolution dashboard capture
├── data/
│   ├── Fact_Policies.csv            # Policy records across classes & provinces
│   └── Fact_Claims.csv              # Claims lifecycle, amounts, and statuses
├── scripts/
│   └── generate_insurance_data.py   # Synthetic insurance dataset generator
├── Santam_Underwriting_Claims_Intelligence.pbix
├── LICENSE
├── .gitignore
└── README.md
```

---

## Tech Stack & Tools

* **Business Intelligence:** Microsoft Power BI Desktop
* **Calculations & Data Modeling:** DAX (Data Analysis Expressions), Star Schema
* **ETL & Ingestion:** Power Query (M), Python (Pandas, NumPy)
* **Visual Theme:** Custom Corporate Design System (Santam Navy #002855, Azure #0072CE, Gold #EAA92C)
