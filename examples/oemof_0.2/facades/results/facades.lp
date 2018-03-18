\* Source Pyomo model name=Model *\

min 
objective:
+2000 GenericInvestmentStorageBlock_invest(storage)
+1500 InvestmentFlow_invest(connection_b0)
+1500 InvestmentFlow_invest(connection_b1)
+100 flow(conversion_b0_0)
+100 flow(conversion_b0_1)
+100 flow(conversion_b0_2)
+100 flow(conversion_b0_3)
+10 flow(generator_b0_0)
+10 flow(generator_b0_1)
+10 flow(generator_b0_2)
+10 flow(generator_b0_3)

s.t.

c_e_Bus_balance(b0_0)_:
-1 flow(b0_connection_0)
-1 flow(b0_storage_0)
+1 flow(connection_b0_0)
+1 flow(conversion_b0_0)
+1 flow(generator_b0_0)
+1 flow(storage_b0_0)
= 200

c_e_Bus_balance(b0_1)_:
-1 flow(b0_connection_1)
-1 flow(b0_storage_1)
+1 flow(connection_b0_1)
+1 flow(conversion_b0_1)
+1 flow(generator_b0_1)
+1 flow(storage_b0_1)
= 200

c_e_Bus_balance(b0_2)_:
-1 flow(b0_connection_2)
-1 flow(b0_storage_2)
+1 flow(connection_b0_2)
+1 flow(conversion_b0_2)
+1 flow(generator_b0_2)
+1 flow(storage_b0_2)
= 200

c_e_Bus_balance(b0_3)_:
-1 flow(b0_connection_3)
-1 flow(b0_storage_3)
+1 flow(connection_b0_3)
+1 flow(conversion_b0_3)
+1 flow(generator_b0_3)
+1 flow(storage_b0_3)
= 200

c_e_Bus_balance(b1_0)_:
-1 flow(b1_connection_0)
+1 flow(connection_b1_0)
= -110

c_e_Bus_balance(b1_1)_:
-1 flow(b1_connection_1)
+1 flow(connection_b1_1)
= -110

c_e_Bus_balance(b1_2)_:
-1 flow(b1_connection_2)
+1 flow(connection_b1_2)
= -110

c_e_Bus_balance(b1_3)_:
-1 flow(b1_connection_3)
+1 flow(connection_b1_3)
= -110

c_e_Bus_balance(bg_0)_:
+1 flow(bg_conversion_0)
= 0

c_e_Bus_balance(bg_1)_:
+1 flow(bg_conversion_1)
= 0

c_e_Bus_balance(bg_2)_:
+1 flow(bg_conversion_2)
= 0

c_e_Bus_balance(bg_3)_:
+1 flow(bg_conversion_3)
= 0

c_e_Transformer_relation(conversion_bg_b0_0)_:
+1 flow(bg_conversion_0)
-3.3333333333333335 flow(conversion_b0_0)
= 0

c_e_Transformer_relation(conversion_bg_b0_1)_:
+1 flow(bg_conversion_1)
-3.3333333333333335 flow(conversion_b0_1)
= 0

c_e_Transformer_relation(conversion_bg_b0_2)_:
+1 flow(bg_conversion_2)
-3.3333333333333335 flow(conversion_b0_2)
= 0

c_e_Transformer_relation(conversion_bg_b0_3)_:
+1 flow(bg_conversion_3)
-3.3333333333333335 flow(conversion_b0_3)
= 0

c_u_InvestmentFlow_max(b0_storage_0)_:
-1 InvestmentFlow_invest(b0_storage)
+1 flow(b0_storage_0)
<= 0

c_u_InvestmentFlow_max(b0_storage_1)_:
-1 InvestmentFlow_invest(b0_storage)
+1 flow(b0_storage_1)
<= 0

c_u_InvestmentFlow_max(b0_storage_2)_:
-1 InvestmentFlow_invest(b0_storage)
+1 flow(b0_storage_2)
<= 0

c_u_InvestmentFlow_max(b0_storage_3)_:
-1 InvestmentFlow_invest(b0_storage)
+1 flow(b0_storage_3)
<= 0

c_u_InvestmentFlow_max(connection_b0_0)_:
-1 InvestmentFlow_invest(connection_b0)
+1 flow(connection_b0_0)
<= 0

c_u_InvestmentFlow_max(connection_b0_1)_:
-1 InvestmentFlow_invest(connection_b0)
+1 flow(connection_b0_1)
<= 0

c_u_InvestmentFlow_max(connection_b0_2)_:
-1 InvestmentFlow_invest(connection_b0)
+1 flow(connection_b0_2)
<= 0

c_u_InvestmentFlow_max(connection_b0_3)_:
-1 InvestmentFlow_invest(connection_b0)
+1 flow(connection_b0_3)
<= 0

c_u_InvestmentFlow_max(connection_b1_0)_:
-1 InvestmentFlow_invest(connection_b1)
+1 flow(connection_b1_0)
<= 0

c_u_InvestmentFlow_max(connection_b1_1)_:
-1 InvestmentFlow_invest(connection_b1)
+1 flow(connection_b1_1)
<= 0

c_u_InvestmentFlow_max(connection_b1_2)_:
-1 InvestmentFlow_invest(connection_b1)
+1 flow(connection_b1_2)
<= 0

c_u_InvestmentFlow_max(connection_b1_3)_:
-1 InvestmentFlow_invest(connection_b1)
+1 flow(connection_b1_3)
<= 0

c_u_InvestmentFlow_max(storage_b0_0)_:
-1 InvestmentFlow_invest(storage_b0)
+1 flow(storage_b0_0)
<= 0

c_u_InvestmentFlow_max(storage_b0_1)_:
-1 InvestmentFlow_invest(storage_b0)
+1 flow(storage_b0_1)
<= 0

c_u_InvestmentFlow_max(storage_b0_2)_:
-1 InvestmentFlow_invest(storage_b0)
+1 flow(storage_b0_2)
<= 0

c_u_InvestmentFlow_max(storage_b0_3)_:
-1 InvestmentFlow_invest(storage_b0)
+1 flow(storage_b0_3)
<= 0

c_e_GenericInvestmentStorageBlock_balance(storage_0)_:
+1 GenericInvestmentStorageBlock_capacity(storage_0)
-1 GenericInvestmentStorageBlock_capacity(storage_3)
-1 flow(b0_storage_0)
+1 flow(storage_b0_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_1)_:
-1 GenericInvestmentStorageBlock_capacity(storage_0)
+1 GenericInvestmentStorageBlock_capacity(storage_1)
-1 flow(b0_storage_1)
+1 flow(storage_b0_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_2)_:
-1 GenericInvestmentStorageBlock_capacity(storage_1)
+1 GenericInvestmentStorageBlock_capacity(storage_2)
-1 flow(b0_storage_2)
+1 flow(storage_b0_2)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_3)_:
-1 GenericInvestmentStorageBlock_capacity(storage_2)
+1 GenericInvestmentStorageBlock_capacity(storage_3)
-1 flow(b0_storage_3)
+1 flow(storage_b0_3)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_inflow(storage)_:
-0.16666666666666666 GenericInvestmentStorageBlock_invest(storage)
+1 InvestmentFlow_invest(b0_storage)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage)_:
-0.16666666666666666 GenericInvestmentStorageBlock_invest(storage)
+1 InvestmentFlow_invest(storage_b0)
= 0

c_u_GenericInvestmentStorageBlock_max_capacity(storage_0)_:
+1 GenericInvestmentStorageBlock_capacity(storage_0)
-1 GenericInvestmentStorageBlock_invest(storage)
<= 0

c_u_GenericInvestmentStorageBlock_max_capacity(storage_1)_:
+1 GenericInvestmentStorageBlock_capacity(storage_1)
-1 GenericInvestmentStorageBlock_invest(storage)
<= 0

c_u_GenericInvestmentStorageBlock_max_capacity(storage_2)_:
+1 GenericInvestmentStorageBlock_capacity(storage_2)
-1 GenericInvestmentStorageBlock_invest(storage)
<= 0

c_u_GenericInvestmentStorageBlock_max_capacity(storage_3)_:
+1 GenericInvestmentStorageBlock_capacity(storage_3)
-1 GenericInvestmentStorageBlock_invest(storage)
<= 0

c_e_LinkBlock_relation(connection_b0_b1_0)_:
-0.96999999999999997 flow(b0_connection_0)
+1 flow(connection_b1_0)
= 0

c_e_LinkBlock_relation(connection_b0_b1_1)_:
-0.96999999999999997 flow(b0_connection_1)
+1 flow(connection_b1_1)
= 0

c_e_LinkBlock_relation(connection_b0_b1_2)_:
-0.96999999999999997 flow(b0_connection_2)
+1 flow(connection_b1_2)
= 0

c_e_LinkBlock_relation(connection_b0_b1_3)_:
-0.96999999999999997 flow(b0_connection_3)
+1 flow(connection_b1_3)
= 0

c_e_LinkBlock_relation(connection_b1_b0_0)_:
-0.96999999999999997 flow(b1_connection_0)
+1 flow(connection_b0_0)
= 0

c_e_LinkBlock_relation(connection_b1_b0_1)_:
-0.96999999999999997 flow(b1_connection_1)
+1 flow(connection_b0_1)
= 0

c_e_LinkBlock_relation(connection_b1_b0_2)_:
-0.96999999999999997 flow(b1_connection_2)
+1 flow(connection_b0_2)
= 0

c_e_LinkBlock_relation(connection_b1_b0_3)_:
-0.96999999999999997 flow(b1_connection_3)
+1 flow(connection_b0_3)
= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(b0_connection_0) <= +inf
   0 <= flow(b0_connection_1) <= +inf
   0 <= flow(b0_connection_2) <= +inf
   0 <= flow(b0_connection_3) <= +inf
   0 <= flow(b0_storage_0) <= +inf
   0 <= flow(b0_storage_1) <= +inf
   0 <= flow(b0_storage_2) <= +inf
   0 <= flow(b0_storage_3) <= +inf
   0 <= flow(b1_connection_0) <= +inf
   0 <= flow(b1_connection_1) <= +inf
   0 <= flow(b1_connection_2) <= +inf
   0 <= flow(b1_connection_3) <= +inf
   0 <= flow(bg_conversion_0) <= +inf
   0 <= flow(bg_conversion_1) <= +inf
   0 <= flow(bg_conversion_2) <= +inf
   0 <= flow(bg_conversion_3) <= +inf
   0 <= flow(connection_b0_0) <= +inf
   0 <= flow(connection_b0_1) <= +inf
   0 <= flow(connection_b0_2) <= +inf
   0 <= flow(connection_b0_3) <= +inf
   0 <= flow(connection_b1_0) <= +inf
   0 <= flow(connection_b1_1) <= +inf
   0 <= flow(connection_b1_2) <= +inf
   0 <= flow(connection_b1_3) <= +inf
   0 <= flow(conversion_b0_0) <= 10
   0 <= flow(conversion_b0_1) <= 10
   0 <= flow(conversion_b0_2) <= 10
   0 <= flow(conversion_b0_3) <= 10
   0 <= flow(generator_b0_0) <= 1000
   0 <= flow(generator_b0_1) <= 1000
   0 <= flow(generator_b0_2) <= 1000
   0 <= flow(generator_b0_3) <= 1000
   0 <= flow(storage_b0_0) <= +inf
   0 <= flow(storage_b0_1) <= +inf
   0 <= flow(storage_b0_2) <= +inf
   0 <= flow(storage_b0_3) <= +inf
   0 <= InvestmentFlow_invest(b0_storage) <= +inf
   0 <= InvestmentFlow_invest(connection_b0) <= +inf
   0 <= InvestmentFlow_invest(connection_b1) <= +inf
   0 <= InvestmentFlow_invest(storage_b0) <= +inf
   0 <= GenericInvestmentStorageBlock_capacity(storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_capacity(storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_capacity(storage_2) <= +inf
   0 <= GenericInvestmentStorageBlock_capacity(storage_3) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage) <= +inf
end
