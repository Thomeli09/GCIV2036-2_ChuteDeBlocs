import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import Parametres
import ROCKFELLER
import Initialisation

##### Données à remplir par l'étudiant #####

Xo  = 60   # [m] Position de l'ouvrage de protection, entre 0m et 70m
Hp  = 0  # [m] Hauteur de l'ouvrage de protection
Cas = 6    # Numéro du groupe de 1 à 10

# Détermination des paramètres en fonction du groupe
Parametre, Yprotect = Parametres.my_Parametres(Cas, Xo)
Xr = Parametre['Xt']

# Nombre de blocs qui chutent, à faire varier
N_calc = 1500

# Initialisation des matrices d'enregistrement
Hauteur_chute = []
Vitesse_init  = []
Stockage      = []

##### BOUCLE DE CALCUL #####

for i in range(N_calc):

    # Initialisation des variables pour chaque bloc qui chute
    Parametre , Variables = Initialisation.my_Initialisation(Parametre, Cas)

    # Routine de calcul de la trajectoire du bloc
    Variables, pente = ROCKFELLER.my_ROCKFELLER(Parametre, Variables)

    # Enregistrement des données utiles
    Stockage.append(Variables)
    Hauteur_chute.append(Parametre['Hchute'])
    Vitesse_init.append(Parametre['vx0'])

##### REPRÉSENTATION D'UN DES CALCULS #####

N = 5 # Choix du calcul à représenter
Variables = Stockage[N]

# Représentation du mouvement et des vitesses
plt.figure()
plt.subplot(2, 1, 1)
plt.plot(Variables['time'], Variables['type'], linewidth=1.4)
plt.grid(True)
plt.ylabel('Type de mouvement [/]', fontsize=14)
plt.title('1 - Roulement sans glissement, 2 - Avec glissement, 3 - Pas de contact')

plt.subplot(2, 1, 2)
plt.grid(True)
plt.plot(Variables['time'], Variables['VX'], linewidth=1.4)
plt.plot(Variables['time'], Variables['VY'], 'r', linewidth=1.4)
plt.legend(['VX', 'VY'])
plt.xlabel('Temps [s]', fontsize=14)
plt.ylabel('Vitesses [m/s]', fontsize=14)

plt.tight_layout()

##### CALCUL DES DISTRIBUTIONS SUR LES DONNÉES #####
nbins = 10 if N_calc < 50 else min(round(N_calc / 10), 60)

plt.figure()
plt.hist(Hauteur_chute, bins=nbins, color='blue')
plt.xlabel('Hauteur de chute [m]', fontsize=14)
plt.ylabel('Occurrence [/]', fontsize=14)
plt.title('Distribution de la hauteur de chute', fontsize=14)
plt.grid(True)

plt.figure()
plt.hist(Vitesse_init, bins=nbins, color='red')
plt.xlabel('Vitesse initiale [m/s]', fontsize=14)
plt.ylabel('Occurrence [/]', fontsize=14)
plt.title('Distribution de la vitesse initiale', fontsize=14)
plt.grid(True)

##### TRAJECTOIRES DÉPASSANT L'OBSTACLE #####
index = [] # Vecteur retenant les blocs qui peuvent atteindre l'infrastructure à risque (démarrent après l'ouvrage de protection ou bien passent par dessus)
    
# Détermination du point (X,Y)=(Xo,Yo) au pied de l'obstacle
I = np.argwhere(Parametre['topo'][0,:]>=Xo) # Obtention de la première case X > X0

X1=Parametre['topo'][0][I-1]
Y1=Parametre['topo'][1][I-1]
X2=Parametre['topo'][0][I]
Y2=Parametre['topo'][1][I]
Yo=Y1+(Y2-Y1)/(X2-X1)*(Xo-X1) # topographie au pied de l'obstacle
Yo = Yo[0]
Yo = Yo[0]

l=1

hauteur = []
vx = []
vy = []
vitesse = []
omega = []
energie = []

for i in range(N_calc) :
    
   Variables = Stockage[i]
    
   x, I = np.unique(Variables['X'],return_index=True)
    
   if np.size(x) >= 1 and Xo < max(Variables['X']) :# Le bloc atteint l'obstacle
        
        if Variables['X'][0] < Xo : # Le bloc démarre avant l'obstacle
            
            hauteur.append(np.interp(Xo,x,np.array(Variables['Y'])[I])) # Hauteur du bloc à l'ouvrage de protection
            vx.append(np.interp(Xo,x,np.array(Variables['VX'])[I])) # Vitesse selon x à l'ouvrage de protection
            vy.append(np.interp(Xo,x,np.array(Variables['VY'])[I])) # Vitesse selon y à l'ouvrage de protection
            vitesse.append(np.sqrt(vx[-1]**2+vy[-1]**2)) # Composante de vitesse dans le plan (x,y)
            omega.append(np.interp(Xo,x,np.array(Variables['THETAV'])[I])) # Vitesse angulaire à l'ouvrage de protection
            energie.append(0.5*Parametre['M']*vitesse[-1]**2+0.5*Parametre['J']*omega[-1]**2+Parametre['M']*9.81*(hauteur[-1]-Yo)) # Énergie en chaque point enregistré, selon les composantes cinétiques de vitesse et de vitesse angulaire
                                                                                                                        
            if hauteur[-1] > Yo+Hp :# Le bloc passe par dessus l'obstacle
                
                index.append(i) # Vecteur retenant les blocs qui peuvent atteindre l'infrastructure à risque

                l = l+1
            
        if Variables['X'][0] > Xo :# Le bloc démarre après l'obstacle
            
            index.append(i) # Vecteur retenant les blocs qui peuvent atteindre l'infrastructure à risque
            
            l = l+1
            
print('Nombre de rochers qui dépassent Xo (position de l\'ouvrage de protection) : ' + str(l-1))
print('Soit une probabilité de ' + str((l-1)/N_calc))

# Moyenne pour ne pas présenter trop de données
nbins = 10 if N_calc < 50 else min(round(N_calc / 10), 60)

# Plot des hauteur, énergie et vitesse des blocs qui atteignent l'ouvrage de
# protection
if 'hauteur' in locals():

    plt.figure()
    plt.hist(hauteur, bins=nbins, color='blue') # Hauteur par rapport à l'ouvrage de protection, pas 0
    plt.xlabel("Hauteur au niveau de l'ouvrage de protection [m]", fontsize=14)
    plt.ylabel('Occurrence [/]', fontsize=14)
    plt.title("Trajectoires atteignant l'ouvrage de protection", fontsize=14)
    plt.grid(True)

    plt.figure()
    plt.hist(vitesse, bins=nbins, color='blue') # Hauteur par rapport à l'ouvrage de protection, pas 0
    plt.xlabel("Vitesse au niveau de l'ouvrage de protection [m/s]", fontsize=14)
    plt.ylabel('Occurrence [/]', fontsize=14)
    plt.title("Trajectoires atteignant l'ouvrage de protection", fontsize=14)
    plt.grid(True)

    plt.figure()
    plt.hist(energie, bins=nbins, color='blue') # Hauteur par rapport à l'ouvrage de protection, pas 0
    plt.xlabel("Energie au niveau de l'ouvrage de protection [J]", fontsize=14)
    plt.ylabel('Occurrence [/]', fontsize=14)
    plt.title("Trajectoires atteignant l'ouvrage de protection", fontsize=14)
    plt.grid(True)

##### OBSERVATION DES TRAJECTOIRES À L'ABSCISSE Xr #####
l = 1

hauteur2 = []
vx2 = []
vy2 = []
vitesse2 = []
omega2 = []
energie2 = []

if Xr >= Xo:
    for i in range(len(index)):

        Variables = Stockage[index[i]]

        x, I = np.unique(Variables['X'], return_index=True)
        
        if len(x) >= 1 and Xr < max(Variables['X']):
            hauteur2.append(np.interp(Xr,x,np.array(Variables['Y'])[I])) # Hauteur du bloc à l'ouvrage de protection
            vx2.append(np.interp(Xr,x,np.array(Variables['VX'])[I])) # Vitesse selon x à l'ouvrage de protection
            vy2.append(np.interp(Xr,x,np.array(Variables['VY'])[I])) # Vitesse selon y à l'ouvrage de protection
            vitesse2.append(np.sqrt(vx2[-1]**2+vy2[-1]**2)) # Composante de vitesse dans le plan (x,y)
            omega2.append(np.interp(Xr,x,np.array(Variables['THETAV'])[I])) # Vitesse angulaire à l'ouvrage de protection
            energie2.append(0.5 * Parametre['M'] * vitesse2[-1]**2 + 0.5 * Parametre['J'] * omega2[-1]**2 + Parametre['M'] * 9.81 * hauteur2[-1])
            l += 1
else:
    for i in range(N_calc):
        Variables = Stockage[i]
        x, I = np.unique(Variables['X'], return_index=True)
        
        if len(x) >= 1 and Xr < max(Variables['X']):
            hauteur2.append(np.interp(Xr, x, Variables['Y']))
            vx2.append(np.interp(Xr, x, Variables['VX']))
            vy2.append(np.interp(Xr, x, Variables['VY']))
            vitesse2.append(np.sqrt(vx2[-1]**2 + vy2[-1]**2))
            omega2.append(np.interp(Xr, x, Variables['THETAV']))
            energie2.append(0.5 * Parametre['M'] * vitesse2[-1]**2 + 0.5 * Parametre['J'] * omega2[-1]**2 + Parametre['M'] * 9.81 * hauteur2[-1])
            l += 1

print('Nombre de rochers qui passent par Xr (infrastructure à protéger) : ' + str(l-1))

print('Soit une probabilité de ' + str((l-1)/N_calc))

nbins = 10 if N_calc < 50 else min(round(N_calc/10), 60)

if 'hauteur2' in locals():
    plt.figure()
    plt.hist(hauteur2, bins=nbins, color=[0.2, 0.75, 0], edgecolor='w')
    plt.xlabel("Hauteur au niveau de l'infrastructure à protéger [m]", fontsize=14)
    plt.ylabel('Occurence [/]', fontsize=14)
    plt.grid(True)
    plt.title("Trajectoires atteignant l'infrastructure à protéger", fontsize=14)

    plt.figure()
    plt.hist(vitesse2, bins=nbins, color=[1, 0.5, 0], edgecolor='w')
    plt.xlabel("Vitesse au niveau de l'infrastructure à protéger [m/s]", fontsize=14)
    plt.ylabel('Occurence [/]', fontsize=14)
    plt.grid(True)
    plt.title("Trajectoires atteignant l'infrastructure à protéger", fontsize=14)

    plt.figure()
    plt.hist(energie2, bins=nbins, color=[128/255, 132/255, 1], edgecolor='w')
    plt.xlabel("Energie au niveau de l'infrastructure à protéger [J]", fontsize=14)
    plt.ylabel('Occurence [/]', fontsize=14)
    plt.grid(True)
    plt.title("Trajectoires atteignant l'infrastructure à protéger", fontsize=14)

##### Représentation des trajectoires, qui dépassent et ne dépassent pas l'ouvrage de protection #####

plt.figure()
plt.plot(Parametre['topo'][0,:],Parametre['topo'][1,:],color='black',linewidth=1.4)
maxmax=np.max(np.max(Parametre['topo']))
minmin=np.min(Parametre['topo'][1,:])
plt.axis([0, maxmax+3*Parametre['R']-minmin, minmin, maxmax+3*Parametre['R']])
for i in range(N_calc):
    Variables = Stockage[i]
    plt.plot(Variables['X'], Variables['Y'], linestyle='--', color='blue')
plt.xlabel('X [m]', fontsize=14)
plt.ylabel('Y [m]', fontsize=14)
plt.title('Toutes les trajectoires', fontsize=16)

if Xo is not None:
    I = next(i for i, val in enumerate(Parametre['topo'][0]) if val >= Xo)
    X1 = Parametre['topo'][0][I - 1]
    Y1 = Parametre['topo'][1][I - 1]
    X2 = Parametre['topo'][0][I]
    Y2 = Parametre['topo'][1][I]
    
    ymin = Y1 + (Y2 - Y1) / (X2 - X1) * (Xo - X1)
    plt.plot([Xo, Xo], [Yo, ymin + Hp], linewidth=1.4, color='red')
    
plt.grid(True)
    
if Parametre['infrastructure'] == 1:
    couleur = 'black'
    I = next(i for i, val in enumerate(Parametre['topo'][0]) if val >= Parametre['Xt'])
    I = I - 1
    X1 = Parametre['Xt']
    Y1 = Parametre['topo'][1][I] + pente[I] * (Parametre['Xt'] - Parametre['topo'][0][I])
    X2 = X1 + 6
    Y2 = Parametre['topo'][1][I] + pente[I] * (X2 - Parametre['topo'][0][I])
    X3 = X1
    Y3 = Y1 + 5
    X4 = X2
    Y4 = Y3
    X5 = (X1 + X2) / 2
    Y5 = Y4 + 2
    
    plt.plot([X1, X2], [Y1, Y2], color=couleur, linewidth=1.4)
    plt.plot([X1, X3], [Y1, Y3], color=couleur, linewidth=1.4)
    plt.plot([X2, X4], [Y2, Y4], color=couleur, linewidth=1.4)
    plt.plot([X3, X4], [Y3, Y4], color=couleur, linewidth=1.4)
    plt.plot([X3, X5], [Y3, Y5], color=couleur, linewidth=1.4)
    plt.plot([X5, X4], [Y5, Y4], color=couleur, linewidth=1.4)
    re = patches.Rectangle((X1 + 1, Y3 - 2), 1, 1, edgecolor=couleur)
    plt.gca().add_patch(re)
    re = patches.Rectangle((X2 - 2, Y3 - 2), 1, 1, edgecolor=couleur)
    plt.gca().add_patch(re)
    re = patches.Rectangle((X1 + 1, Y3 - 4), 1, 1, edgecolor=couleur)
    plt.gca().add_patch(re)
    re = patches.Rectangle((X2 - 2, Y3 - 4), 1, 1, edgecolor=couleur)
    plt.gca().add_patch(re)
else:
    couleur = 'black'
    I = next(i for i, val in enumerate(Parametre['topo'][0]) if val >= Parametre['Xt'])
    I = I - 1
    X1 = Parametre['Xt']
    Y1 = Parametre['topo'][1][I] + pente[I] * (Parametre['Xt'] - Parametre['topo'][0][I])
    X2 = X1 + 3.8
    Y2 = Parametre['topo'][1][I] + pente[I] * (X2 - Parametre['topo'][0][I])
    X3 = X1 + 0.4
    Y3 = Y1 + 0.4
    X4 = X2 - 0.4
    Y4 = Y3
    eproue = 0.05
    hroue = 0.4
    ecart = 1.435
    lwag = 3
    hwag = 4
    plt.plot([X1, X3], [Y1, Y3], color=couleur, linewidth=1.4)
    plt.plot([X3, X4], [Y3, Y4], color=couleur, linewidth=1.4)
    plt.plot([X4, X2], [Y4, Y2], color=couleur, linewidth=1.4)
    
    Xmil = (X1 + X2) / 2
    X5 = Xmil - ecart / 2
    Y5 = Y4
    X6 = Xmil + ecart / 2 - eproue
    Y6 = Y5
    X7 = Xmil - lwag / 2
    Y7 = Y5 + hroue
    
    re = patches.Rectangle((X5, Y5), eproue, hroue, edgecolor=couleur)
    plt.gca().add_patch(re)
    re = patches.Rectangle((X6, Y6), eproue, hroue, edgecolor=couleur)
    plt.gca().add_patch(re)
    re = patches.Rectangle((X7, Y7), lwag, hwag, linewidth=1.4, edgecolor=couleur, fill=False)
    plt.gca().add_patch(re)

##### Représentation des trajectoires qui dépassent l'ouvrage de protection #####
plt.figure()
plt.plot(Parametre['topo'][0], Parametre['topo'][1], color='black', linewidth=1.4)
maxmax=np.max(np.max(Parametre['topo']))
minmin=np.min(Parametre['topo'][1,:])
plt.axis([0, maxmax + 3 * Parametre['R'] - minmin, minmin, maxmax + 3 * Parametre['R']])

for i in range(len(index)):
    Variables = Stockage[index[i]]
    plt.plot(Variables['X'], Variables['Y'], linestyle='--', color='red')

plt.xlabel('X [m]', fontsize=14)
plt.ylabel('Y [m]', fontsize=14)
plt.title('Trajectoires | Xmax>Xo', fontsize=14)

if Xo is not None:
    I = next(i for i, val in enumerate(Parametre['topo'][0]) if val >= Xo)
    X1 = Parametre['topo'][0][I - 1]
    Y1 = Parametre['topo'][1][I - 1]
    X2 = Parametre['topo'][0][I]
    Y2 = Parametre['topo'][1][I]
    
    ymin = Y1 + (Y2 - Y1) / (X2 - X1) * (Xo - X1)
    plt.plot([Xo, Xo], [Yo, ymin + Hp], linewidth=1.4, color='red')

if Parametre['infrastructure'] == 1:
    couleur = 'black'
    I = next(i for i, val in enumerate(Parametre['topo'][0]) if val >= Parametre['Xt'])
    I = I - 1
    X1 = Parametre['Xt']
    Y1 = Parametre['topo'][1][I] + pente[I] * (Parametre['Xt'] - Parametre['topo'][0][I])
    X2 = X1 + 6
    Y2 = Parametre['topo'][1][I] + pente[I] * (X2 - Parametre['topo'][0][I])
    X3 = X1
    Y3 = Y1 + 5
    X4 = X2
    Y4 = Y3
    X5 = (X1 + X2) / 2
    Y5 = Y4 + 2
    
    plt.plot([X1, X2], [Y1, Y2], color=couleur, linewidth=1.4)
    plt.plot([X1, X3], [Y1, Y3], color=couleur, linewidth=1.4)
    plt.plot([X2, X4], [Y2, Y4], color=couleur, linewidth=1.4)
    plt.plot([X3, X4], [Y3, Y4], color=couleur, linewidth=1.4)
    plt.plot([X3, X5], [Y3, Y5], color=couleur, linewidth=1.4)
    plt.plot([X5, X4], [Y5, Y4], color=couleur, linewidth=1.4)
    re = patches.Rectangle((X1 + 1, Y3 - 2), 1, 1, edgecolor=couleur)
    plt.gca().add_patch(re)
    re = patches.Rectangle((X2 - 2, Y3 - 2), 1, 1, edgecolor=couleur)
    plt.gca().add_patch(re)
    re = patches.Rectangle((X1 + 1, Y3 - 4), 1, 1, edgecolor=couleur)
    plt.gca().add_patch(re)
    re = patches.Rectangle((X2 - 2, Y3 - 4), 1, 1, edgecolor=couleur)
    plt.gca().add_patch(re)
else:
    couleur = 'black'
    I = next(i for i, val in enumerate(Parametre['topo'][0]) if val >= Parametre['Xt'])
    I = I - 1
    X1 = Parametre['Xt']
    Y1 = Parametre['topo'][1][I] + pente[I] * (Parametre['Xt'] - Parametre['topo'][0][I])
    X2 = X1 + 3.8
    Y2 = Parametre['topo'][1][I] + pente[I] * (X2 - Parametre['topo'][0][I])
    X3 = X1 + 0.4
    Y3 = Y1 + 0.4
    X4 = X2 - 0.4
    Y4 = Y3
    eproue = 0.05
    hroue = 0.4
    ecart = 1.435
    lwag = 3
    hwag = 4
    plt.plot([X1, X3], [Y1, Y3], color=couleur, linewidth=1.4)
    plt.plot([X3, X4], [Y3, Y4], color=couleur, linewidth=1.4)
    plt.plot([X4, X2], [Y4, Y2], color=couleur, linewidth=1.4)
    
    Xmil = (X1 + X2) / 2
    X5 = Xmil - ecart / 2
    Y5 = Y4
    X6 = Xmil + ecart / 2 - eproue
    Y6 = Y5
    X7 = Xmil - lwag / 2
    Y7 = Y5 + hroue
    
    re = patches.Rectangle((X5, Y5), eproue, hroue, edgecolor=couleur)
    plt.gca().add_patch(re)
    re = patches.Rectangle((X6, Y6), eproue, hroue, edgecolor=couleur)
    plt.gca().add_patch(re)
    re = patches.Rectangle((X7, Y7), lwag, hwag, linewidth=1.4, edgecolor=couleur, fill=False)
    plt.gca().add_patch(re)

plt.grid(True)
plt.show()