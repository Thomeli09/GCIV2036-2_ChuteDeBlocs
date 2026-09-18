from rockfall.mechanics import kinetic_energy, potential_energy


mass = 1000.0
velocity = 10.0
height = 5.0

ke = kinetic_energy(mass, velocity)
pe = potential_energy(mass, height)

print(f"Kinetic energy: {ke:.2f} J")
print(f"Potential energy: {pe:.2f} J")
