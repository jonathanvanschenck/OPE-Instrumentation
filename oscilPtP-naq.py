import visa
import datetime
from time import sleep

rm = visa.ResourceManager()
scope = rm.open_resource("USB0::0x0957::0x1732::MY44001331::0::INSTR")
print(scope.query("*IDN?"))
t = input("Proceed? (y/n)")

if t.lower() != "y":
	exit()

f = open("power.csv", "w")
tm = 0
time_int = 10 #time intervals in seconds (1-30)

try:
        while True:
                tm_tst = str(datetime.datetime.now())[11:19]
                if tm != tm_tst and int(tm_tst[6:])%time_int == 0:
                        dt_tm = datetime.datetime.now()
                        tm = str(dt_tm)[11:19]
                        vlt = float(scope.query(":MEAS:VPP?"))*1e3
                        Lsr_pwr = 0.0154*(0.204*vlt-0.3067)
                        mcr_pwr = 0.01034*(0.204*vlt-0.3067)
                        l = "{0}, V={1:.3f} meV, P_lsr={2:.3f} mW, P_micro={3:.3f} mW".format(dt_tm, vlt, Lsr_pwr, mcr_pwr)
                        print(l)
                        f.write(l+"\n")
                        sleep(0.5)
except KeyboardInterrupt:
        f.close()
