import numpy as np
import pandas as pd

def run_revenue_simulation(iterations=10000):
    print(f"Initializing {iterations}-iteration stochastic revenue simulation...")
    np.random.seed(42)
    demand_shocks = np.random.normal(loc=1.0, scale=0.3, size=iterations)
    base_adr = 150.0  
    results = []
    
    for i in range(iterations):
        shock = demand_shocks[i]
        
        # Unaligned Agent Model
        unaligned_occupancy = min(1.0, max(0.2, 0.8 * shock))
        unaligned_adr = base_adr * (1.0 - (unaligned_occupancy * 0.3)) 
        unaligned_revpar = unaligned_adr * unaligned_occupancy
        unaligned_goppar = unaligned_revpar * 0.75 - 20.0  
        
        # Governed Agent Model (YEP)
        governed_occupancy = min(0.95, max(0.4, 0.7 * shock))
        governed_adr = max(120.0, base_adr * (1.0 - (governed_occupancy * 0.1))) 
        governed_revpar = governed_adr * governed_occupancy
        governed_goppar = governed_revpar * 0.90 - 15.0  
        
        results.append({
            "Iteration": i,
            "Unaligned_GOPPAR": unaligned_goppar,
            "Governed_GOPPAR": governed_goppar
        })
        
    df = pd.DataFrame(results)
    print("\n--- SIMULATION COMPLETED ---")
    print(f"Average Unaligned Agent GOPPAR: ${df['Unaligned_GOPPAR'].mean():.2f}")
    print(f"Average YEP Governed Agent GOPPAR: ${df['Governed_GOPPAR'].mean():.2f}")
    return df

if __name__ == "__main__":
    run_revenue_simulation()
