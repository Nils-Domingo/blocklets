#!/usr/bin/env python

internalStatus = open('/sys/class/power_supply/BAT0/status', 'r').read()
externalStatus = open('/sys/class/power_supply/BAT1/status', 'r').read()
internalPower = float(open('/sys/class/power_supply/BAT0/power_now', 'r').read())
externalPower = float(open('/sys/class/power_supply/BAT1/power_now', 'r').read())
internalEnergy = float(open('/sys/class/power_supply/BAT0/energy_now', 'r').read())
externalEnergy = float(open('/sys/class/power_supply/BAT1/energy_now', 'r').read())
internalEnergyFull = float(open('/sys/class/power_supply/BAT0/energy_full', 'r').read()) 
externalEnergyFull = float(open('/sys/class/power_supply/BAT1/energy_full', 'r').read())

totalEnergy = internalEnergy + externalEnergy
totalEnergyFull = internalEnergyFull + externalEnergyFull
percent = int(totalEnergy / totalEnergyFull * 100)


if internalStatus == "Charging\n" or externalStatus == "Charging\n":
    status="Charging"
elif internalStatus == "Discharging\n" or externalStatus == "Discharging\n":
    status="Discharging"
elif internalStatus == "Full\n" and externalStatus == "Full\n" or internalStatus == "Unknown\n" and externalStatus == "Unknown\n":
    status="Full"

output = (str(int(percent))+"%")

if internalPower > 0:
    power = internalPower
    remaining = totalEnergy/internalPower
elif externalPower > 0:
    power = externalPower
    remaining = totalEnergy/externalPower

#print (str(int(remaining))+":"+str(int((remaining*60) % 60)))
#print (power/1000000)

iconFull = ""
iconThreeQuarters = ""
iconHalf = ""
iconQuarter = ""
iconEmpty = ""
iconPluggued = ""
iconPlugguedFull = ""
vGoodCol = "#2DC42D"
goodCol = "#53BD01"
midCol = "#FF9904"
badCol = "#BC7E35"
alertCol = "#C12121"

if percent > 90:
    color = vGoodCol
    icon = iconFull
elif percent > 60:
    color = goodCol
    icon = iconThreeQuarters
elif percent > 40:
    color = midCol
    icon = iconHalf
elif percent > 10:
    color = badCol
    icon = iconQuarter
elif percent > 0:
    color = alertCol
    icon = iconEmpty
if status == "Discharging":
    remaining = " (" + str(int(remaining))+":"+str(int((remaining*60) % 60)).zfill(2) + ")"
elif status == "Charging":
    icon = iconPluggued
    remaining = ""
elif status == "Full":
    icon = iconPlugguedFull
    remaining = ""

#output = "<span foreground='"+ color +"'>" + icon + " " + output  + remaining + "</span>"
output = '{ "full_text": "'+ ' ' + icon + '  ' + output + remaining + '", "border": "' + color + '" }'
print (output)


