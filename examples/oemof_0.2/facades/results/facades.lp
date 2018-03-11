\* Source Pyomo model name=Model *\

min 
objective:
+2000 GenericInvestmentStorageBlock_invest(storage)
+1500 InvestmentFlow_invest(connector_b0)
+1500 InvestmentFlow_invest(connector_b1)
+10 flow(generator_b0_0)
+10 flow(generator_b0_1)
+10 flow(generator_b0_2)
+10 flow(generator_b0_3)

s.t.

c_e_Bus_balance(b0_0)_:
-1 flow(b0_connector_0)
-1 flow(b0_storage_0)
+1 flow(connector_b0_0)
+1 flow(generator_b0_0)
+1 flow(storage_b0_0)
= 200

c_e_Bus_balance(b0_1)_:
-1 flow(b0_connector_1)
-1 flow(b0_storage_1)
+1 flow(connector_b0_1)
+1 flow(generator_b0_1)
+1 flow(storage_b0_1)
= 200

c_e_Bus_balance(b0_2)_:
-1 flow(b0_connector_2)
-1 flow(b0_storage_2)
+1 flow(connector_b0_2)
+1 flow(generator_b0_2)
+1 flow(storage_b0_2)
= 200

c_e_Bus_balance(b0_3)_:
-1 flow(b0_connector_3)
-1 flow(b0_storage_3)
+1 flow(connector_b0_3)
+1 flow(generator_b0_3)
+1 flow(storage_b0_3)
= 200

c_e_Bus_balance(b1_0)_:
-1 flow(b1_connector_0)
+1 flow(connector_b1_0)
= -110

c_e_Bus_balance(b1_1)_:
-1 flow(b1_connector_1)
+1 flow(connector_b1_1)
= -110

c_e_Bus_balance(b1_2)_:
-1 flow(b1_connector_2)
+1 flow(connector_b1_2)
= -110

c_e_Bus_balance(b1_3)_:
-1 flow(b1_connector_3)
+1 flow(connector_b1_3)
= -110

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

c_u_InvestmentFlow_max(connector_b0_0)_:
-1 InvestmentFlow_invest(connector_b0)
+1 flow(connector_b0_0)
<= 0

c_u_InvestmentFlow_max(connector_b0_1)_:
-1 InvestmentFlow_invest(connector_b0)
+1 flow(connector_b0_1)
<= 0

c_u_InvestmentFlow_max(connector_b0_2)_:
-1 InvestmentFlow_invest(connector_b0)
+1 flow(connector_b0_2)
<= 0

c_u_InvestmentFlow_max(connector_b0_3)_:
-1 InvestmentFlow_invest(connector_b0)
+1 flow(connector_b0_3)
<= 0

c_u_InvestmentFlow_max(connector_b1_0)_:
-1 InvestmentFlow_invest(connector_b1)
+1 flow(connector_b1_0)
<= 0

c_u_InvestmentFlow_max(connector_b1_1)_:
-1 InvestmentFlow_invest(connector_b1)
+1 flow(connector_b1_1)
<= 0

c_u_InvestmentFlow_max(connector_b1_2)_:
-1 InvestmentFlow_invest(connector_b1)
+1 flow(connector_b1_2)
<= 0

c_u_InvestmentFlow_max(connector_b1_3)_:
-1 InvestmentFlow_invest(connector_b1)
+1 flow(connector_b1_3)
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

c_e_LinkBlock_relation(connector_b0_b1_0)_:
-0.96999999999999997 flow(b0_connector_0)
+1 flow(connector_b1_0)
= 0

c_e_LinkBlock_relation(connector_b0_b1_1)_:
-0.96999999999999997 flow(b0_connector_1)
+1 flow(connector_b1_1)
= 0

c_e_LinkBlock_relation(connector_b0_b1_2)_:
-0.96999999999999997 flow(b0_connector_2)
+1 flow(connector_b1_2)
= 0

c_e_LinkBlock_relation(connector_b0_b1_3)_:
-0.96999999999999997 flow(b0_connector_3)
+1 flow(connector_b1_3)
= 0

c_e_LinkBlock_relation(connector_b1_b0_0)_:
-0.96999999999999997 flow(b1_connector_0)
+1 flow(connector_b0_0)
= 0

c_e_LinkBlock_relation(connector_b1_b0_1)_:
-0.96999999999999997 flow(b1_connector_1)
+1 flow(connector_b0_1)
= 0

c_e_LinkBlock_relation(connector_b1_b0_2)_:
-0.96999999999999997 flow(b1_connector_2)
+1 flow(connector_b0_2)
= 0

c_e_LinkBlock_relation(connector_b1_b0_3)_:
-0.96999999999999997 flow(b1_connector_3)
+1 flow(connector_b0_3)
= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(b0_connector_0) <= +inf
   0 <= flow(b0_connector_1) <= +inf
   0 <= flow(b0_connector_2) <= +inf
   0 <= flow(b0_connector_3) <= +inf
   0 <= flow(b0_storage_0) <= +inf
   0 <= flow(b0_storage_1) <= +inf
   0 <= flow(b0_storage_2) <= +inf
   0 <= flow(b0_storage_3) <= +inf
   0 <= flow(b1_connector_0) <= +inf
   0 <= flow(b1_connector_1) <= +inf
   0 <= flow(b1_connector_2) <= +inf
   0 <= flow(b1_connector_3) <= +inf
   0 <= flow(connector_b0_0) <= +inf
   0 <= flow(connector_b0_1) <= +inf
   0 <= flow(connector_b0_2) <= +inf
   0 <= flow(connector_b0_3) <= +inf
   0 <= flow(connector_b1_0) <= +inf
   0 <= flow(connector_b1_1) <= +inf
   0 <= flow(connector_b1_2) <= +inf
   0 <= flow(connector_b1_3) <= +inf
   0 <= flow(generator_b0_0) <= 1000
   0 <= flow(generator_b0_1) <= 1000
   0 <= flow(generator_b0_2) <= 1000
   0 <= flow(generator_b0_3) <= 1000
   0 <= flow(storage_b0_0) <= +inf
   0 <= flow(storage_b0_1) <= +inf
   0 <= flow(storage_b0_2) <= +inf
   0 <= flow(storage_b0_3) <= +inf
   0 <= InvestmentFlow_invest(b0_storage) <= +inf
   0 <= InvestmentFlow_invest(connector_b0) <= +inf
   0 <= InvestmentFlow_invest(connector_b1) <= +inf
   0 <= InvestmentFlow_invest(storage_b0) <= +inf
   0 <= GenericInvestmentStorageBlock_capacity(storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_capacity(storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_capacity(storage_2) <= +inf
   0 <= GenericInvestmentStorageBlock_capacity(storage_3) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage) <= +inf
end
