import visa
import datetime
from time import sleep
import numpy as np

rm = visa.ResourceManager()
scope = rm.open_resource("USB0::0x0957::0x1732::MY44001331::0::INSTR")
print(scope.query("*IDN?"))
t = input("Proceed? (y/n)")

if t.lower() != "y":
	exit()

f = open("power.csv", "w")
tm = 0
time_int = 10 #time intervals in seconds (1-30)
dt = time_int/10
vltVec = []

try:
        while True:
                tm_tst = str(datetime.datetime.now())[11:19]
		vltVec = []
                if tm != tm_tst and int(tm_tst[6:])%dt == 0:
                        dt_tm = datetime.datetime.now()
                        tm = str(dt_tm)[11:19]
			vltVec += [float(scope.query(":MEAS:VPP?"))*1e3]
			if nt(tm_tst[6:])%time_int == 0:
				vlt = np.mean(vltVec)#float(scope.query(":MEAS:VPP?"))*1e3
				dvlt = np.std(vltVec)
				Lsr_pwr = 0.0154*(0.204*vltVec-0.3067)
				dLsr_pwr = np.std(Lsr_pwr)
				Lsr_pwr = np.mean(Lsr_pwr)
				mcr_pwr = 0.01034*(0.204*vltVec-0.3067)
				dmcr_pwr = np.std(mcr_pwr)
				mcr_pwr = np.mean(mcr_pwr)
				l = "{0}, V={1:.3f}+-{2:.3f} meV, P_lsr={3:.3f}+-{4:.3f} mW, P_micro={5:.3f}+-{6:.3f} mW".format(dt_tm, vlt, dvlt, Lsr_pwr, dLsr_pwr, mcr_pwr, dmcr_pwr)
				print(l)
				f.write(l+"\n")
                        sleep(0.1)
except KeyboardInterrupt:
        f.close()
