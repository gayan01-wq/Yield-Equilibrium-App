# --- WITHIN THE CALCULATE_YIELD FUNCTION ---

def calculate_yield(rms, adr, nts, mq, comm, hurdle, ev_p=0, tr_c=0):
    t_rms = sum(rms)
    if t_rms <= 0: return None
    
    inv_occupancy = (t_rms / h_inv) * 100
    
    # --- THE 20% REVENUE DENSITY RULE ---
    # If the segment occupies >= 20% of the hotel, 
    # we automatically apply a 'Displacement Tax' to the hurdle.
    
    logic_hurdle = hurdle
    density_alert = "✅ Normal Flow"
    
    if inv_occupancy >= 20.0:
        # Increase hurdle by 15% to account for inventory scarcity
        logic_hurdle = hurdle * 1.15 
        density_alert = "🚨 HIGH DENSITY (>20%): Displacement Risk Applied"

    # ... (rest of your net wealth calculation) ...

    # Optimization Logic
    if wpr < logic_hurdle:
        status, color = "DILUTIVE", "#e74c3c"
    elif wpr < (logic_hurdle + 5):
        status, color = "MARGINAL", "#f1c40f"
    else:
        status, color = "OPTIMIZED", "#27ae60"
        
    return {
        "wpr": wpr, 
        "s": status, 
        "c": color, 
        "alert": density_alert, 
        "h_applied": logic_hurdle
    }
