import numpy as np

# Cette fonction utilise les paramètres définis dans la routine
# Parametres.m afin de déterminer les propriétés probabilistes telles que
# la vitesse initiale, le coefficient de rebond et la hauteur de chute
# initiale.

def my_Initialisation(Parametre, Cas):

    # Initialisation des propriétés de surface sur toute la topographie
    Parametre['mu_d'] = np.ones(Parametre['topo'].shape[1]) * Parametre['mud']  # Coefficient de frottement [-]
    Parametre['ex'] = np.ones(Parametre['topo'].shape[1])  # Coefficient de rebond [-]

    # Définition de la vitesse initiale suivant la loi probabiliste définie
    Parametre['vx0'] = max(np.random.normal(Parametre['VXmu'], Parametre['VXsig']), 0)  # >=0 [m/s]

    # Initialisation de l'angle de rotation et de la vitesse de rotation
    Variables = {
        'THETA': 0,  # Angle de rotation [rad]
        'THETAV': 0  # Vitesse de rotation [rad/s]
    }

    # Création d'un vecteur dont le nombre de cellule est égale au nombre de segments de la topographie
    vec = np.ones(Parametre['topo'].shape[1] - 1)

    # Définition des coefficients de rebonds suivant la loi probabiliste définie.
    # Comme la définition se fait segment par segment, chaque segment possède un coefficient de rebond différent.
    Parametre['ey'] = np.random.normal(vec * Parametre['eymu'], vec * Parametre['eysig'])  # [-]
    Parametre['ey'][Parametre['ey'] > 1] = 1  # Valeur bornée à 1 (maximum)
    Parametre['ey'][Parametre['ey'] < 0] = 0  # Valeur bornée à 0 (minimum)
    Variables['ey'] = Parametre['ey']

    # Définition de la hauteur de chute entre les valeurs maximales et minimales définies auparavant.
    Parametre['Hchute'] = np.random.uniform(Parametre['Hmin'], Parametre['Hmax'])  # [m]

    # Calcul des coordonnées initiales
    # Sur base de la topographie, de la hauteur de chute et du rayon du bloc,
    # on calcule un position (X,Y) initiale.

    topo = Parametre['topo']

    if Cas == 1:
        # Case 1
        if Parametre['Hchute'] > topo[1, 1]:
            Xch = np.interp(Parametre['Hchute'], np.flip(topo[1, 0:2]), np.flip(topo[0, 0:2]))
            beta = abs(np.arctan((topo[1, 1] - topo[1, 0]) / (topo[0, 1] - topo[0, 0])))
        elif Parametre['Hchute'] > topo[1, 2]:
            Xch = np.interp(Parametre['Hchute'], np.flip(topo[1, 1:3]), np.flip(topo[0, 1:3]))
            beta = abs(np.arctan((topo[1, 2] - topo[1, 1]) / (topo[0, 2] - topo[0, 1])))
        else:
            Xch = topo[0, 2]
            beta = 0

        Variables['X'] = Xch + Parametre['R'] * np.cos(beta)
        Variables['Y'] = Parametre['Hchute'] + Parametre['R'] * np.sin(beta)

        # Vitesse initiale parallèle à la pente [m/s]
        Variables['VX'] = Parametre['vx0'] * np.cos(beta)
        Variables['VY'] = -Parametre['vx0'] * np.sin(beta)

    elif Cas == 2:
        # Case 2
        Xch = np.interp(Parametre['Hchute'], np.flip(topo[1, 0:2]), np.flip(topo[0, 0:2]))
        beta = abs(np.arctan((topo[1, 1] - topo[1, 0]) / (topo[0, 1] - topo[0, 0])))

        Variables['X'] = Xch + Parametre['R'] * np.cos(beta)
        Variables['Y'] = Parametre['Hchute'] + Parametre['R'] * np.sin(beta)

        # Vitesse initiale uniquement selon X (les blocs se décrochent et tombent par gravité) [m/s]
        Variables['VX'] = Parametre['vx0']
        Variables['VY'] = 0

    elif Cas == 3:
        # Case 3
        if Parametre['Hchute'] > Parametre['topo'][1, 1]:
            Xch = np.interp(Parametre['Hchute'],np.flip( Parametre['topo'][1, 0:2]), np.flip(Parametre['topo'][0, 0:2]))
            beta = abs(np.arctan((Parametre['topo'][1, 1] - Parametre['topo'][1, 0]) / (Parametre['topo'][0, 1] - Parametre['topo'][0, 0])))
        else:
            Xch = Parametre['topo'][0, 2]
            beta = 0

        Variables['X'] = Xch + Parametre['R'] * np.cos(beta)
        Variables['Y'] = Parametre['Hchute'] + Parametre['R'] * np.sin(beta)

        # Vitesse initiale parallèle to the slope [m/s]
        Variables['VX'] = Parametre['vx0'] * np.cos(beta)
        Variables['VY'] = -Parametre['vx0'] * np.sin(beta)

    elif Cas == 4:
        # Case 4
        if Parametre['Hchute'] > Parametre['topo'][1, 1]:
            Xch = 0
            beta = 0
        elif Parametre['Hchute'] > Parametre['topo'][1, 2]:
            Xch = np.interp(Parametre['Hchute'], np.flip(Parametre['topo'][1, 1:3]), np.flip(Parametre['topo'][0, 1:3]))
            beta = abs(np.arctan((Parametre['topo'][1, 2] - Parametre['topo'][1, 1]) / (Parametre['topo'][0, 2] - Parametre['topo'][0, 1])))
        else:
            Xch = np.interp(Parametre['Hchute'], np.flip(Parametre['topo'][1, 2:4]), np.flip(Parametre['topo'][0, 2:4]))
            beta = abs(np.arctan((Parametre['topo'][1, 3] - Parametre['topo'][1, 2]) / (Parametre['topo'][0, 3] - Parametre['topo'][0, 2])))

        Variables['X'] = Xch + Parametre['R'] * np.cos(beta)
        Variables['Y'] = Parametre['Hchute'] + Parametre['R'] * np.sin(beta)

        # Vitesse initiale parallèle to the slope but uniquement according to X
        # (les blocs se décrochent and tombent par gravité) [m/s]
        Variables['VX'] = Parametre['vx0'] * np.cos(beta)
        Variables['VY'] = 0

    elif Cas == 5:
        # Case 5
        if Parametre['Hchute'] < topo[1, 4]:
            Xch = topo[0, 4]
            beta = 0
        elif Parametre['Hchute'] < topo[1, 3]:
            Xch = np.interp(Parametre['Hchute'], np.flip(topo[1, 3:5]), np.flip(topo[0, 3:5]))
            beta = abs(np.arctan((topo[1, 4] - topo[1, 3]) / (topo[0, 4] - topo[0, 3])))
        elif Parametre['Hchute'] < topo[1, 2]:
            Xch = topo[0, 2]
            beta = 0
        elif Parametre['Hchute'] < topo[1, 1]:
            Xch = np.interp(Parametre['Hchute'], np.flip(topo[1, 1:3]), np.flip(topo[0, 1:3]))
            beta = abs(np.arctan((topo[1, 2] - topo[1, 1]) / (topo[0, 2] - topo[0, 1])))
        else:
            Xch = topo[0, 1]
            beta = np.pi / 2

        Variables['X'] = Xch + Parametre['R'] * np.cos(beta)
        Variables['Y'] = Parametre['Hchute'] + Parametre['R'] * np.sin(beta)

        # Vitesse initiale parallèle à la pente but uniquement selon X
        # (les blocs se décrochent et tombent par gravité) [m/s]
        Variables['VX'] = Parametre['vx0'] * np.cos(beta)
        Variables['VY'] = 0

    elif Cas == 6:
        # Case 6
        if Parametre['Hchute'] > topo[1, 1]:
            Xch = np.interp(Parametre['Hchute'], np.flip(topo[1, :2]), np.flip(topo[0, :2]))
            beta = abs(np.arctan((topo[1, 1] - topo[1, 0]) / (topo[0, 1] - topo[0, 0])))
        else:
            Xch = np.interp(Parametre['Hchute'], np.flip(topo[1, 2:4]), np.flip(topo[0, 2:4]))
            beta = abs(np.arctan((topo[1, 3] - topo[1, 2]) / (topo[0, 3] - topo[0, 2])))

        Variables['X'] = Xch + Parametre['R'] * np.cos(beta)
        Variables['Y'] = Parametre['Hchute'] + Parametre['R'] * np.sin(beta)

        # Vitesse initiale uniquement according to X
        # (les blocs se décrochent et tombent par gravité) [m/s]
        Variables['VX'] = Parametre['vx0']
        Variables['VY'] = 0

    elif Cas == 7:
        # Case 7
        if Parametre['Hchute'] > topo[1, 1]:
            Xch = np.interp(Parametre['Hchute'], np.flip(topo[1, :2]), np.flip(topo[0, :2]))
            beta = abs(np.arctan((topo[1, 1] - topo[1, 0]) / (topo[0, 1] - topo[0, 0])))
        elif Parametre['Hchute'] > topo[1, 2]:
            Xch = topo[0, 2]
            beta = 0
        else:
            Xch = np.interp(Parametre['Hchute'], np.flip(topo[1, 3:5]), np.flip(topo[0, 3:5]))
            beta = abs(np.arctan((topo[1, 4] - topo[1, 3]) / (topo[0, 4] - topo[0, 3])))

        Variables['X'] = Xch + Parametre['R'] * np.cos(beta)
        Variables['Y'] = Parametre['Hchute'] + Parametre['R'] * np.sin(beta)

        # Vitesse initiale parallèle à the slope [m/s]
        Variables['VX'] = Parametre['vx0'] * np.cos(beta)
        Variables['VY'] = -Parametre['vx0'] * np.sin(beta)

    elif Cas == 8:
        # Case 8
        if Parametre['Hchute'] > topo[1, 1]:
            Xch = topo[0, 1]
            beta = 0
        elif Parametre['Hchute'] > topo[1, 2]:
            Xch = np.interp(Parametre['Hchute'], np.flip(topo[1, 1:3]), np.flip(topo[0, 1:3]))
            beta = abs(np.arctan((topo[1, 2] - topo[1, 1]) / (topo[0, 2] - topo[0, 1])))
        elif Parametre['Hchute'] > topo[1, 3]:
            Xch = topo[0, 3]
            beta = 0
        elif Parametre['Hchute'] > topo[1, 4]:
            Xch = np.interp(Parametre['Hchute'], np.flip(topo[1, 3:5]), np.flip(topo[0, 3:5]))
            beta = abs(np.arctan((topo[1, 4] - topo[1, 3]) / (topo[0, 4] - topo[0, 3])))
        else:
            Xch = topo[0, 5]
            beta = 0

        Variables['X'] = Xch + Parametre['R'] * np.cos(beta)
        Variables['Y'] = Parametre['Hchute'] + Parametre['R'] * np.sin(beta)

        # Vitesse initiale parallèle to the slope but uniquement according to X
        # (les blocs se décrochent et tombent par gravité) [m/s]
        Variables['VX'] = Parametre['vx0'] * np.cos(beta)
        Variables['VY'] = 0

    elif Cas == 9:
        # Case 9
        if Parametre['Hchute'] > topo[1, 1]:
            Xch = topo[0, 1]
            beta = 0
        elif Parametre['Hchute'] > topo[1, 2]:
            Xch = np.interp(Parametre['Hchute'], np.flip(topo[1, 1:3]), np.flip(topo[0, 1:3]))
            beta = abs(np.arctan((topo[1, 2] - topo[1, 1]) / (topo[0, 2] - topo[0, 1])))
        else:
            Xch = topo[0, 3]
            beta = 0

        Variables['X'] = Xch + Parametre['R'] * np.cos(beta)
        Variables['Y'] = Parametre['Hchute'] + Parametre['R'] * np.sin(beta)

        # Vitesse initiale parallèle to the slope but uniquement according to X
        # (les blocs se décrochent and tombent par gravité) [m/s]
        Variables['VX'] = Parametre['vx0'] * np.cos(beta)
        Variables['VY'] = 0

    elif Cas == 10:
        # Case 10
        if Parametre['Hchute'] < topo[1, 2]:
            Xch = np.interp(Parametre['Hchute'], np.flip(topo[1, 2:4]), np.flip(topo[0, 2:4]))
            beta = abs(np.arctan((topo[1, 3] - topo[1, 2]) / (topo[0, 3] - topo[0, 2])))
        elif Parametre['Hchute'] < topo[1, 1]:
            Xch = np.interp(Parametre['Hchute'], np.flip(topo[1, 1:3]), np.flip(topo[0, 1:3]))
            beta = abs(np.arctan((topo[1, 2] - topo[1, 1]) / (topo[0, 2] - topo[0, 1])))
        else:
            Xch = np.interp(Parametre['Hchute'], np.flip(topo[1, 0:2]), np.flip(topo[0, 0:2]))
            beta = abs(np.arctan((topo[1, 1] - topo[1, 0]) / (topo[0, 1] - topo[0, 0])))

        Variables['X'] = Xch + Parametre['R'] * np.cos(beta)
        Variables['Y'] = Parametre['Hchute'] + Parametre['R'] * np.sin(beta)

        # Vitesse initiale parallèle to the slope but uniquement according to X
        # (les blocs se décrochent and tombent par gravité) [m/s]
        Variables['VX'] = Parametre['vx0']
        Variables['VY'] = 0

    return Parametre, Variables
