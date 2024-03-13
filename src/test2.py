import ast


a = "{'BMS_Time(POSIX)':1707779358,'Alive(s)':1289,'App_FW(#)':155,'PCU_FW(#)':001,'WMU_FW(#)':None,'BMS_FW(#)':001,'LV_FW(#)':001,'HV_FW(#)':001,'Raw_SoC(%)':98,'LCD_SoC(%)':100,'Input_7909(V)':22.9,'Input_HPP(V)':22.9,'Input_AC(V)':120.2,'Input_7909(A)':10,'Input_HPP(A)':20,'Input_AC(A)':15,'Input_7909(W)':275,'Input_HPP(W)':600,'Input_AC(W)':1000,'Output_12V(V)':13.5,'Output_USB(V)':None,'Output_AC(V)':120.3,'Output_12V(A)':33,'Output_USB(A)':8,'Output_AC(A)':15,'Output_12V(W)':276,'Output_USB(W)':296,'Output_AC(W)':2500,'TTE(Hours)':99.5,'TTF(Hours)':99.5,'Icon_HPP(ON/OFF)':0,'Icon_7909(ON/OFF)':0,'Icon_AC(ON/OFF)':0,'Icon_12V(ON/OFF)':0,'Icon_USB(ON/OFF)':0,'Icon_AC(ON/OFF)':0,'APS(ON/OFF)':0,'50hz(ON/OFF)':0,'AC_Fast(ON/OFF)':0,'TBOOST(ON/OFF)':0,'Fan(%)':55.5,'Batt(A)':-57.2,'Batt(V)':51.2,'Batt_Max(degC)':85.6,'Batt_Min(degC)':-3.5,'Batt(degC)':25.6,'LV_Inv(degC)':25.6,'HV_Inv(degC)':25.6,'PD65W(degC)':25.6,'PD140W(degC)':25.6,'Charge_Profile_max(%)':100,'Charge_Profile_recharge(%)':95,'Charge_Profile_min(%)':0,'ChargeCV(?)':None}"
b = a.replace(':00',':').replace(':0', ':')
print(b)
dict1 = ast.literal_eval(b)
print(dict1)
