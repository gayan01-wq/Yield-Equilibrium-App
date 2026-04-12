def run(rms, adr, nts, mix, cp, fl, ev_rev=0, total_tr_cost=0):
        t_rms = sum(rms)
        if t_rms <= 0: return None
        pax = (rms[0]*1 + rms[1]*2 + rms[2]*3)
        gross_total = (adr * t_rms * nts) + (ev_rev * pax * nts)
        
        nt_rev = (adr * t_rms) / tx
        fb_cost = sum(q * m[p] * (pax / t_rms) for p, q in mix.items())
        ev_w = (ev_rev * pax) / tx
        cm = (nt_rev - fb_cost) * cp
        
        dp = ((nt_rev - fb_cost - cm) - (p01 * t_rms)) + (ev_w / t_rms)
        tp = (dp * t_rms * nts) - (total_tr_cost / tx)
        u = tp / (t_rms * nts)
        
        # Room Count Impact Logic
        impact_pct = (t_rms / h_cp) * 100
        # The Ratio: Wealth generated per 1% of inventory consumed
        yield_ratio = tp / impact_pct if impact_pct > 0 else 0
        
        af = fl * 0.75 if nts > 7 else fl
        fric = (1 - (tp / gross_total)) * 100 if gross_total > 0 else 0
        
        if fric < 26: fric_lb = "Net Contribution"
        elif 26 <= fric < 38: fric_lb = "Yield Dilution"
        else: fric_lb = "Revenue Erosion"
        
        if u < af: lb, cl = "DILUTIVE", "#e74c3c"
        elif af <= u < (af + 5): lb, cl = "MARGINAL", "#f1c40f"
        else: lb, cl = "OPTIMIZED", "#27ae60"
        
        return {
            "u": u, "s": lb, "c": cl, "tp": tp, 
            "pax": pax, "fric": fric, "fric_lb": fric_lb,
            "imp": impact_pct, "ratio": yield_ratio
        }

    def seg(nm, cl, bg, kp, ad_d, fl_d, cp, is_group=False):
        # ... (keep your existing UI code for columns c1, c2, c3) ...
        
        res = run([sgl, dbl, tpl], ad, nt, q, cp, fl, ev_r, tr_c)
        if res:
            with c4:
                st.metric("Wealth (Stay/Room)", f"{cu} {res['u']:.2f}")
                st.markdown(f"<b style='color:{res['c']}'>{res['s']}</b>", unsafe_allow_html=True)
                st.write(f"Inventory Impact: **{res['imp']:.1f}%**")
                
                # NEW: The Efficiency Ratio mentioned below Stay Wealth
                st.write(f"Wealth/Impact Ratio: **{res['ratio']:,.0f}**")
                
                st.write(f"{res['fric_lb']}: **{res['fric']:.1f}%**")
                st.write(f"Stay Wealth (Total): **{res['tp']:,.0f}**")
        return res
