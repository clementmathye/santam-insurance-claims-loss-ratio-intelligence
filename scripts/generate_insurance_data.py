"""
Santam General Insurance - Synthetic Dataset Generator
Generates realistic South African short-term insurance data for Fact_Policies, Fact_Claims,
Dim_UnderwritingClass, and Dim_Region tables with zero third-party dependencies (Pure Python).
"""

import csv
import os
import random
from datetime import datetime, timedelta

def main():
    random.seed(42)
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(output_dir, exist_ok=True)
    
    print("Generating Santam Short-Term Insurance Analytical Dataset...")

    # 1. Dim_UnderwritingClass
    underwriting_classes = [
        {"ClassID": 1, "UnderwritingClass": "Personal Motor", "LineOfBusiness": "Personal Lines", "TargetLossRatioBenchmark": 0.65, "TargetTATDays": 12},
        {"ClassID": 2, "UnderwritingClass": "Personal Property", "LineOfBusiness": "Personal Lines", "TargetLossRatioBenchmark": 0.58, "TargetTATDays": 14},
        {"ClassID": 3, "UnderwritingClass": "Commercial Property", "LineOfBusiness": "Commercial Lines", "TargetLossRatioBenchmark": 0.62, "TargetTATDays": 21},
        {"ClassID": 4, "UnderwritingClass": "Commercial Fleet", "LineOfBusiness": "Commercial Lines", "TargetLossRatioBenchmark": 0.70, "TargetTATDays": 15},
        {"ClassID": 5, "UnderwritingClass": "Agri & Specialist", "LineOfBusiness": "Specialty Lines", "TargetLossRatioBenchmark": 0.60, "TargetTATDays": 25}
    ]
    
    dim_class_file = os.path.join(output_dir, "Dim_UnderwritingClass.csv")
    with open(dim_class_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["ClassID", "UnderwritingClass", "LineOfBusiness", "TargetLossRatioBenchmark", "TargetTATDays"])
        writer.writeheader()
        writer.writerows(underwriting_classes)

    # 2. Dim_Region
    regions = [
        {"RegionID": 1, "Province": "Gauteng", "PrimaryMetro": "Johannesburg / Pretoria", "RiskProfile": "High Hail & Theft Exposure"},
        {"RegionID": 2, "Province": "Western Cape", "PrimaryMetro": "Cape Town", "RiskProfile": "Moderate Maritime & Storm Exposure"},
        {"RegionID": 3, "Province": "KwaZulu-Natal", "PrimaryMetro": "Durban", "RiskProfile": "High Flood & Coastal Weather"},
        {"RegionID": 4, "Province": "Eastern Cape", "PrimaryMetro": "Gqeberha / East London", "RiskProfile": "Moderate Coastal & Wind"},
        {"RegionID": 5, "Province": "Free State", "PrimaryMetro": "Bloemfontein", "RiskProfile": "Agricultural & Severe Weather"},
        {"RegionID": 6, "Province": "Mpumalanga", "PrimaryMetro": "Mbombela", "RiskProfile": "High Summer Storm & Freight Traffic"},
        {"RegionID": 7, "Province": "Limpopo", "PrimaryMetro": "Polokwane", "RiskProfile": "High Temperature & Rural Freight"}
    ]
    
    dim_region_file = os.path.join(output_dir, "Dim_Region.csv")
    with open(dim_region_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["RegionID", "Province", "PrimaryMetro", "RiskProfile"])
        writer.writeheader()
        writer.writerows(regions)

    # 3. Fact_Policies (5,000 Policies)
    n_policies = 5000
    broker_channels = ["Direct Digital", "Independent Broker", "Corporate Intermediary", "Affinity Partner"]
    policy_statuses = ["Active", "Lapsed", "Cancelled"]
    policy_status_weights = [0.88, 0.08, 0.04]
    
    # Class weights: Motor 35%, Property 25%, Commercial Prop 15%, Fleet 15%, Agri 10%
    class_pool = [1]*35 + [2]*25 + [3]*15 + [4]*15 + [5]*10
    
    # Region weights: GP 40%, WC 22%, KZN 16%, EC 8%, FS 5%, MP 5%, LP 4%
    region_pool = [1]*40 + [2]*22 + [3]*16 + [4]*8 + [5]*5 + [6]*5 + [7]*4

    start_inception = datetime(2024, 1, 1)
    policies = []
    
    for i in range(1, n_policies + 1):
        pid = f"POL-{100000 + i}"
        days_offset = random.randint(0, 540) # Jan 2024 to June 2025
        inc_date = start_inception + timedelta(days=days_offset)
        exp_date = inc_date + timedelta(days=365)
        
        cid = random.choice(class_pool)
        rid = random.choice(region_pool)
        
        # Premium distribution by class (in ZAR)
        if cid == 1: # Motor
            annual_prem = round(random.uniform(9600, 26000), 2)
        elif cid == 2: # Personal Property
            annual_prem = round(random.uniform(7200, 21000), 2)
        elif cid == 3: # Commercial Property
            annual_prem = round(random.uniform(42000, 160000), 2)
        elif cid == 4: # Commercial Fleet
            annual_prem = round(random.uniform(75000, 320000), 2)
        else: # Agri
            annual_prem = round(random.uniform(50000, 220000), 2)
            
        status = random.choices(policy_statuses, weights=policy_status_weights, k=1)[0]
        channel = random.choices(broker_channels, weights=[0.30, 0.45, 0.15, 0.10], k=1)[0]
        
        policies.append({
            "PolicyID": pid,
            "InceptionDate": inc_date.strftime("%Y-%m-%d"),
            "ExpiryDate": exp_date.strftime("%Y-%m-%d"),
            "ClassID": cid,
            "RegionID": rid,
            "AnnualPremium": annual_prem,
            "PolicyStatus": status,
            "BrokerChannel": channel
        })
        
    fact_policies_file = os.path.join(output_dir, "Fact_Policies.csv")
    with open(fact_policies_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["PolicyID", "InceptionDate", "ExpiryDate", "ClassID", "RegionID", "AnnualPremium", "PolicyStatus", "BrokerChannel"])
        writer.writeheader()
        writer.writerows(policies)

    # 4. Fact_Claims (~1,650 claims)
    claim_types_by_class = {
        1: ["Vehicle Collision", "Hail Damage", "Windscreen Replacement", "Vehicle Theft / Hijack", "Third Party Liability"],
        2: ["Geyser Burst / Water Damage", "Housebreaking / Theft", "Storm / Roof Damage", "Power Surge", "Accidental Damage"],
        3: ["Commercial Fire Damage", "Building Storm Inundation", "Business Interruption", "Machinery Breakdown", "Premises Liability"],
        4: ["Fleet Heavy Collision", "Cargo Loss in Transit", "Driver Vehicle Rollover", "Fleet Hail Damage", "Major Fleet Theft"],
        5: ["Crop Hail Damage", "Livestock Loss", "Agricultural Machinery Breakdown", "Farm Property Fire", "Severe Drought / Heat Stress"]
    }
    
    repudiation_reasons = [
        "Uninsured Peril / Exclusion Applied",
        "Material Non-Disclosure at Inception",
        "Unlicensed / Unauthorised Driver",
        "Failure to Take Reasonable Precautions",
        "Fraudulent / Inflated Claim"
    ]

    claims = []
    claim_id_counter = 50001
    
    # Select subset of active/lapsed policies for claims (some have multiple claims)
    eligible_policies = [p for p in policies if p["PolicyStatus"] in ["Active", "Lapsed"]]
    
    # We want ~1,650 claims to match realistic 30-33% claims frequency across portfolio
    target_claims = 1650
    
    for _ in range(target_claims):
        policy = random.choice(eligible_policies)
        cid = policy["ClassID"]
        rid = policy["RegionID"]
        p_inc = datetime.strptime(policy["InceptionDate"], "%Y-%m-%d")
        
        # Incident date must occur between inception and end of observation (e.g. Dec 2025)
        max_incident = min(p_inc + timedelta(days=350), datetime(2025, 12, 31))
        if max_incident <= p_inc:
            continue
            
        days_from_inc = random.randint(5, (max_incident - p_inc).days)
        inc_date = p_inc + timedelta(days=days_from_inc)
        
        # Seasonal weather bump in Nov-Jan for GP/KZN (Hail/Floods)
        if rid in [1, 3] and inc_date.month in [11, 12, 1]:
            # higher probability of storm/hail
            claim_type = random.choice(["Hail Damage", "Geyser Burst / Water Damage", "Storm / Roof Damage", "Vehicle Collision"])
        else:
            claim_type = random.choice(claim_types_by_class[cid])
            
        # Status distribution: Settled 72%, Approved (pending payment) 10%, Repudiated 12%, Under Investigation 6%
        status = random.choices(
            ["Settled", "Approved", "Repudiated", "Under Investigation"],
            weights=[0.72, 0.10, 0.12, 0.06],
            k=1
        )[0]
        
        # Turnaround time distribution (exponential-like realistic turnaround)
        # Western Cape is slightly faster, Commercial & Agri takes longer
        base_tat = random.randint(3, 10)
        if cid in [1, 2]: # Personal Lines
            tat_days = base_tat + random.randint(1, 14)
            if rid == 2: # Western Cape efficiency
                tat_days = max(3, tat_days - 3)
        elif cid in [3, 4]: # Commercial Lines
            tat_days = base_tat + random.randint(7, 28)
        else: # Agri / Specialist
            tat_days = base_tat + random.randint(10, 35)
            
        settlement_date_str = ""
        rep_reason = ""
        
        if status == "Settled":
            settlement_date = inc_date + timedelta(days=tat_days)
            settlement_date_str = settlement_date.strftime("%Y-%m-%d")
        elif status == "Approved":
            # Approved recent claims might settle soon
            settlement_date = inc_date + timedelta(days=tat_days)
            settlement_date_str = settlement_date.strftime("%Y-%m-%d")
        elif status == "Repudiated":
            rep_reason = random.choice(repudiation_reasons)
            tat_days = ""
        elif status == "Under Investigation":
            tat_days = ""
            
        # Claim Amount (ZAR) based on class and type
        if "Theft" in claim_type or "Fire" in claim_type or "Rollover" in claim_type:
            # High severity claim
            if cid == 1:
                claim_amount = round(random.uniform(90000, 320000), 2)
            elif cid == 2:
                claim_amount = round(random.uniform(45000, 180000), 2)
            elif cid in [3, 4]:
                claim_amount = round(random.uniform(150000, 680000), 2)
            else:
                claim_amount = round(random.uniform(120000, 550000), 2)
        elif "Windscreen" in claim_type or "Power Surge" in claim_type:
            # Low severity / high frequency
            claim_amount = round(random.uniform(2800, 14500), 2)
        else:
            # Medium severity
            if cid == 1:
                claim_amount = round(random.uniform(12000, 58000), 2)
            elif cid == 2:
                claim_amount = round(random.uniform(9500, 42000), 2)
            elif cid == 3:
                claim_amount = round(random.uniform(45000, 210000), 2)
            elif cid == 4:
                claim_amount = round(random.uniform(65000, 310000), 2)
            else:
                claim_amount = round(random.uniform(35000, 240000), 2)

        claims.append({
            "ClaimID": f"CLM-{claim_id_counter}",
            "PolicyID": policy["PolicyID"],
            "IncidentDate": inc_date.strftime("%Y-%m-%d"),
            "SettlementDate": settlement_date_str,
            "TurnaroundDays": tat_days if status in ["Settled", "Approved"] else "",
            "ClaimType": claim_type,
            "ClaimAmount": claim_amount,
            "ClaimStatus": status,
            "RepudiationReason": rep_reason
        })
        claim_id_counter += 1

    fact_claims_file = os.path.join(output_dir, "Fact_Claims.csv")
    with open(fact_claims_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "ClaimID", "PolicyID", "IncidentDate", "SettlementDate", 
            "TurnaroundDays", "ClaimType", "ClaimAmount", "ClaimStatus", "RepudiationReason"
        ])
        writer.writeheader()
        writer.writerows(claims)

    print(f"Data Generation Completed Successfully!")
    print(f"- Fact_Policies.csv: {len(policies)} rows")
    print(f"- Fact_Claims.csv: {len(claims)} rows")
    print(f"- Dim_UnderwritingClass.csv: {len(underwriting_classes)} rows")
    print(f"- Dim_Region.csv: {len(regions)} rows")
    print(f"Files saved in: {output_dir}")

if __name__ == "__main__":
    main()
