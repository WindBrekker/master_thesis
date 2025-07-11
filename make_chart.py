import matplotlib.pyplot as plt
import xraylib as xrl

plt.figure()
plt.title("Mass attenuation Coefficient vs Energy")
plt.xlabel("Energy (keV)")
plt.ylabel("Mass Attenuation Coefficient (cm²/g)")
plt.xscale('log')
plt.yscale('log')


elements = ["Ar", "Si", "Ge"]
Energy = list(range(1, 200)) 
p = []
r = []
c = []

for Z in elements:
    for E in Energy:
        p.append(xrl.CS_Photo_CP(Z, E))
        r.append(xrl.CS_Rayl_CP(Z, E))
        c.append(xrl.CS_Compt_CP(Z, E))

    
    plt.plot(Energy, p, label=f"{Z} Photoelectric")
    plt.plot(Energy, r, label=f"{Z} Incoherent")
    plt.plot(Energy, c, label=f"{Z} Coherent")
    p.clear()
    r.clear()
    c.clear()

plt.legend()
plt.show()
plt.savefig("mass_attenuation_coefficient.png")
    
