\* Source Pyomo model name=Model *\

min 
objective:
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
= 40

c_e_Bus_balance(b0_1)_:
-1 flow(b0_connector_1)
-1 flow(b0_storage_1)
+1 flow(connector_b0_1)
+1 flow(generator_b0_1)
+1 flow(storage_b0_1)
= 40

c_e_Bus_balance(b0_2)_:
-1 flow(b0_connector_2)
-1 flow(b0_storage_2)
+1 flow(connector_b0_2)
+1 flow(generator_b0_2)
+1 flow(storage_b0_2)
= 40

c_e_Bus_balance(b0_3)_:
-1 flow(b0_connector_3)
-1 flow(b0_storage_3)
+1 flow(connector_b0_3)
+1 flow(generator_b0_3)
+1 flow(storage_b0_3)
= 40

c_e_Bus_balance(b1_0)_:
-1 flow(b1_connector_0)
+1 flow(connector_b1_0)
= -20

c_e_Bus_balance(b1_1)_:
-1 flow(b1_connector_1)
+1 flow(connector_b1_1)
= -20

c_e_Bus_balance(b1_2)_:
-1 flow(b1_connector_2)
+1 flow(connector_b1_2)
= -20

c_e_Bus_balance(b1_3)_:
-1 flow(b1_connector_3)
+1 flow(connector_b1_3)
= -20

c_e_GenericStorageBlock_balance(storage_0)_:
+1 GenericStorageBlock_capacity(storage_0)
-1 GenericStorageBlock_capacity(storage_3)
-1 flow(b0_storage_0)
+1 flow(storage_b0_0)
= 0

c_e_GenericStorageBlock_balance(storage_1)_:
-1 GenericStorageBlock_capacity(storage_0)
+1 GenericStorageBlock_capacity(storage_1)
-1 flow(b0_storage_1)
+1 flow(storage_b0_1)
= 0

c_e_GenericStorageBlock_balance(storage_2)_:
-1 GenericStorageBlock_capacity(storage_1)
+1 GenericStorageBlock_capacity(storage_2)
-1 flow(b0_storage_2)
+1 flow(storage_b0_2)
= 0

c_e_GenericStorageBlock_balance(storage_3)_:
-1 GenericStorageBlock_capacity(storage_2)
+1 GenericStorageBlock_capacity(storage_3)
-1 flow(b0_storage_3)
+1 flow(storage_b0_3)
= 0

c_e_LinkBlock_relation(connector_b0_b1_0)_:
-0.94999999999999996 flow(b0_connector_0)
+1 flow(connector_b1_0)
= 0

c_e_LinkBlock_relation(connector_b0_b1_1)_:
-0.94999999999999996 flow(b0_connector_1)
+1 flow(connector_b1_1)
= 0

c_e_LinkBlock_relation(connector_b0_b1_2)_:
-0.94999999999999996 flow(b0_connector_2)
+1 flow(connector_b1_2)
= 0

c_e_LinkBlock_relation(connector_b0_b1_3)_:
-0.94999999999999996 flow(b0_connector_3)
+1 flow(connector_b1_3)
= 0

c_e_LinkBlock_relation(connector_b1_b0_0)_:
-0.94999999999999996 flow(b1_connector_0)
+1 flow(connector_b0_0)
= 0

c_e_LinkBlock_relation(connector_b1_b0_1)_:
-0.94999999999999996 flow(b1_connector_1)
+1 flow(connector_b0_1)
= 0

c_e_LinkBlock_relation(connector_b1_b0_2)_:
-0.94999999999999996 flow(b1_connector_2)
+1 flow(connector_b0_2)
= 0

c_e_LinkBlock_relation(connector_b1_b0_3)_:
-0.94999999999999996 flow(b1_connector_3)
+1 flow(connector_b0_3)
= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(b0_connector_0) <= +inf
   0 <= flow(b0_connector_1) <= +inf
   0 <= flow(b0_connector_2) <= +inf
   0 <= flow(b0_connector_3) <= +inf
   0 <= flow(b0_storage_0) <= 100
   0 <= flow(b0_storage_1) <= 100
   0 <= flow(b0_storage_2) <= 100
   0 <= flow(b0_storage_3) <= 100
   0 <= flow(b1_connector_0) <= +inf
   0 <= flow(b1_connector_1) <= +inf
   0 <= flow(b1_connector_2) <= +inf
   0 <= flow(b1_connector_3) <= +inf
   0 <= flow(connector_b0_0) <= 1000
   0 <= flow(connector_b0_1) <= 1000
   0 <= flow(connector_b0_2) <= 1000
   0 <= flow(connector_b0_3) <= 1000
   0 <= flow(connector_b1_0) <= 1000
   0 <= flow(connector_b1_1) <= 1000
   0 <= flow(connector_b1_2) <= 1000
   0 <= flow(connector_b1_3) <= 1000
   0 <= flow(generator_b0_0) <= 100
   0 <= flow(generator_b0_1) <= 100
   0 <= flow(generator_b0_2) <= 100
   0 <= flow(generator_b0_3) <= 100
   0 <= flow(storage_b0_0) <= 100
   0 <= flow(storage_b0_1) <= 100
   0 <= flow(storage_b0_2) <= 100
   0 <= flow(storage_b0_3) <= 100
   0 <= GenericStorageBlock_capacity(storage_0) <= 1000
   0 <= GenericStorageBlock_capacity(storage_1) <= 1000
   0 <= GenericStorageBlock_capacity(storage_2) <= 1000
   0 <= GenericStorageBlock_capacity(storage_3) <= 1000
end
