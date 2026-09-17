import numpy as np
import matplotlib.pyplot as plt
import time
import Parametres
import ROCKFELLER
import Initialisation

def TP_Chute_Blocs_Fct(N_calc, Xo, Hp, Cas):
    # Données
    Parametre, Yprotect = Parametres.my_Parametres(Cas, Xo)

    # Position de l'infrastructure
    Xr = Parametre['Xt']  # m

    Stockage = []

    for i in range(N_calc):
        Parametre, Variables = Initialisation.my_Initialisation(Parametre, Cas)
        Variables, pente = ROCKFELLER.my_ROCKFELLER(Parametre, Variables)
        Stockage.append(Variables)

    hauteur2, vitesse2, energie2 = [], [], []

    index = []

    I = np.where(Parametre['topo'][0] >= Xo)[0][0]
    X1 = Parametre['topo'][0][I - 1]
    Y1 = Parametre['topo'][1][I - 1]
    X2 = Parametre['topo'][0][I]
    Y2 = Parametre['topo'][1][I]
    Yo = Y1 + (Y2 - Y1) / (X2 - X1) * (Xo - X1)

    l = 1

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
                hauteur2.append(np.interp(Xo,x,np.array(Variables['Y'])[I])) # Hauteur du bloc à l'ouvrage de protection
                vx2.append(np.interp(Xo,x,np.array(Variables['VX'])[I])) # Vitesse selon x à l'ouvrage de protection
                vy2.append(np.interp(Xo,x,np.array(Variables['VY'])[I])) # Vitesse selon y à l'ouvrage de protection
                vitesse2.append(np.sqrt(vx2[-1]**2+vy2[-1]**2)) # Composante de vitesse dans le plan (x,y)
                omega2.append(np.interp(Xo,x,np.array(Variables['THETAV'])[I])) # Vitesse angulaire à l'ouvrage de protection
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

    Probabilite = (l - 1) / N_calc

    return hauteur2, vitesse2, energie2, Probabilite

# Define the main routine
def main():

    # Position de l'ouvrage de protection et hauteur de ce dernier
    # Mettre la hauteur à 0 pour ne rien mettre

    Xo = 25  # [m] entre 0 et 70m
    Hp = 0  # [m]

    # Choix du cas : les caractéristiques de la bille qui tombe (R, rho, M et
    # J) proviennent de la fonction Parametres.m et les caractéristiques de la
    # surface (mud, eymu, eysig, VXmu et VXsig) également. La topographie y est
    # également définie.

    Cas = 9  #1 à 10

    N_calc = 100  # Nombre INITIAL de rochers dans la fonction TP_Chute_Blocs_Fct.m
    Nb_test = 15 # Nombre de fois la fonction TP_Chute_Blocs_Fct.m sera lancée    

    # Initialisation
    Resultats = np.zeros((Nb_test, 9))

    for temp in range(1, Nb_test + 1):

        # Lancement de la fonction et enregistrement du temps requis
        hauteur2, vitesse2, energie2, Probabilite = TP_Chute_Blocs_Fct(N_calc, Xo, Hp, Cas)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        # Enregistrement des résultats jugés importants
        Resultats[temp - 1, 0] = N_calc
        Resultats[temp - 1, 1] = elapsed_time
        Resultats[temp - 1, 2] = np.mean(hauteur2)
        Resultats[temp - 1, 3] = np.std(hauteur2)
        Resultats[temp - 1, 4] = np.mean(vitesse2)
        Resultats[temp - 1, 5] = np.std(vitesse2)
        Resultats[temp - 1, 6] = np.mean(energie2)
        Resultats[temp - 1, 7] = np.std(energie2)
        Resultats[temp - 1, 8] = Probabilite

        N_calc *= 2

        if N_calc >= 5000:
            break

    # Plotting
    plt.figure()

    plt.subplot(1, 2, 1)
    plt.plot(Resultats[:temp, 0], Resultats[:temp, 2], 'o-')
    plt.xlabel('Nombre de simulations')
    plt.ylabel('Moyenne de la hauteur [m]')
    plt.grid()

    plt.subplot(1, 2, 2)
    plt.plot(Resultats[:temp, 0], Resultats[:temp, 3], 'o-')
    plt.xlabel('Nombre de simulations')
    plt.ylabel('Déviation de la hauteur [m]')
    plt.grid()

    # Plotting
    plt.figure()

    plt.subplot(1, 2, 1)
    plt.plot(Resultats[:temp, 0], Resultats[:temp, 4], 'o-')
    plt.xlabel('Nombre de simulations')
    plt.ylabel('Moyenne de la vitesse [m/s]')
    plt.grid()

    plt.subplot(1, 2, 2)
    plt.plot(Resultats[:temp, 0], Resultats[:temp, 5], 'o-')
    plt.xlabel('Nombre de simulations')
    plt.ylabel('Déviation de la vitesse [m/s]')
    plt.grid()

    # Plotting
    plt.figure()

    plt.subplot(1, 2, 1)
    plt.plot(Resultats[:temp, 0], Resultats[:temp, 6], 'o-')
    plt.xlabel('Nombre de simulations')
    plt.ylabel("Moyenne de l'énergie [J]")
    plt.grid()

    plt.subplot(1, 2, 2)
    plt.plot(Resultats[:temp, 0], Resultats[:temp, 7], 'o-')
    plt.xlabel('Nombre de simulations')
    plt.ylabel("Déviation de l'énergie [J]")
    plt.grid()

    # Plotting
    plt.figure()

    plt.plot(Resultats[:temp, 0], Resultats[:temp, 8], 'o-')
    plt.xlabel('Nombre de simulations')
    plt.ylabel("Probabilité d'impact")
    plt.grid()

    # Plotting
    plt.figure()

    plt.plot(Resultats[:temp, 0], Resultats[:temp, 1], 'o-')
    plt.xlabel('Nombre de simulations')
    plt.ylabel("Temps de calcul [s]")
    plt.grid()

    plt.show()

if __name__ == "__main__":
    start_time = time.perf_counter()  # Start the timer
    main()
