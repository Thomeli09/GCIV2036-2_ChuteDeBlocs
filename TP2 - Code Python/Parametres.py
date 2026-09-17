import numpy as np
import math

def my_Parametres(Cas, Xo):
    parametre = {}
    
    # Définition des paramètres communs
    parametre['rho'] = 2600  # Masse volumique = 2600 [kg/m³]
    parametre['dt'] = 0.05  # Incrément de temps = 0.05 [s]

    if Cas == 1:  # Belle Roche 3
        # Définition de la topographie
        topo = np.array([[0, 30, 40, 40, 60],  # Selon X
                         [44, 10, 4, 0, 0]])  # Selon Y

        # Définition des hauteurs de chutes min et max [m]
        parametre['Hmin'] = 10  # 10 [m]
        parametre['Hmax'] = 44  # 44 [m]

        # Définition du type d'infrastructure à protéger (1 = maison et 2 = train)
        # ainsi que de sa position.
        parametre['Xt'] = 45  # 45 [m]
        parametre['infrastructure'] = 2

        # Définition des paramètres relatifs au cas étudié
        parametre['R'] = 0.15  # Rayon du bloc = 0.15 [m]
        parametre['mud'] = 0.6  # Coefficient de frottement = 0.6 [-]
        parametre['eymu'] = 0.7  # Moyenne du coefficient de rebond = 0.7 [-]
        parametre['eysig'] = 0.1  # Variance du coefficient de rebond = 0.1 [-]
        parametre['VXmu'] = 0.5  # Moyenne de la vitesse initiale = 0.5 [m/s]
        parametre['VXsig'] = 0.1  # Variance de la vitesse initiale = 0.1 [m/s]

        # Calcul de l'altitude topographique à l'emplacement de l'ouvrage de protection
        if Xo < topo[0, 1]:
            Yprotect = np.interp(Xo, topo[0, 0:2], topo[1, 0:2])  # Premier segment
        elif Xo < topo[0, 2]:
            Yprotect = np.interp(Xo, topo[0, 1:3], topo[1, 1:3])  # Second segment
        else:
            Yprotect = 0  # Sol

    elif Cas == 2:  # Belle Roche 4
        # Définition de la topographie
        topo = np.array([[3, 0, 0, 12, 40],  # Selon X
                         [28, 18, 15, 0, 0]])  # Selon Y

        # Définition des hauteurs de chutes min et max [m]
        parametre['Hmin'] = 18  # 18 [m]
        parametre['Hmax'] = 28  # 28 [m]

        # Définition du type d'infrastructure à protéger (1 = maison et 2 = train)
        # ainsi que de sa position.
        parametre['Xt'] = 20  # 20 [m]
        parametre['infrastructure'] = 1

        # Définition des paramètres relatifs au cas étudié
        parametre['R'] = 0.15  # Rayon du bloc = 0.15 [m]
        parametre['mud'] = 0.6  # Coefficient de frottement = 0.6 [-]
        parametre['eymu'] = 0.4  # Moyenne du coefficient de rebond = 0.4 [-]
        parametre['eysig'] = 0.05  # Variance du coefficient de rebond = 0.05 [-]
        parametre['VXmu'] = 0.2  # Moyenne de la vitesse initiale = 0.2 [m/s]
        parametre['VXsig'] = 0.05  # Variance de la vitesse initiale = 0.05 [m/s]

        # Calcul de l'altitude topographique à l'emplacement de l'ouvrage de protection
        if Xo < topo[0, 3]:
            Yprotect = np.interp(Xo, topo[0, 2:4], topo[1, 2:4])  # Pente descendante
        else:
            Yprotect = 0  # Sol

    elif Cas == 3:  # Martinrive 2
        # Définition de la topographie
        topo = np.array([[0, 4, 4, 25],  # Selon X
                         [14, 10, 0, 0]])  # Selon Y

        # Définition des hauteurs de chutes min et max [m]
        parametre['Hmin'] = 0  # 0 [m]
        parametre['Hmax'] = 14  # 14 [m]

        # Définition du type d'infrastructure à protéger (1 = maison et 2 = train)
        # ainsi que de sa position.
        parametre['Xt'] = 10  # 10 [m]
        parametre['infrastructure'] = 2

        # Définition des paramètres relatifs au cas étudié
        parametre['R'] = 0.2  # Rayon du bloc = 0.2 [m]
        parametre['mud'] = 0.5  # Coefficient de frottement = 0.5 [-]
        parametre['eymu'] = 0.4  # Moyenne du coefficient de rebond = 0.4 [-]
        parametre['eysig'] = 0.05  # Variance du coefficient de rebond = 0.05 [-]
        parametre['VXmu'] = 0.5  # Moyenne de la vitesse initiale = 0.5 [m/s]
        parametre['VXsig'] = 0.1  # Variance de la vitesse initiale = 0.1 [m/s]

        # Calcul de l'altitude topographique à l'emplacement de l'ouvrage de protection
        if Xo < topo[0, 1]:
            Yprotect = np.interp(Xo, topo[0, 0:2], topo[1, 0:2])  # Pente
        else:
            Yprotect = 0  # Sol

    elif Cas == 4:  # Sy
        # Définition de la topographie
        topo = np.array([[0, 0, 30, 32, 60],  # Selon X
                         [30, 20, 10, 0, 0]])  # Selon Y

        # Définition des hauteurs de chutes min et max [m]
        parametre['Hmin'] = 10  # 10 [m]
        parametre['Hmax'] = 20  # 20 [m]

        # Définition du type d'infrastructure à protéger (1 = maison et 2 = train)
        # ainsi que de sa position.
        parametre['Xt'] = 35  # 35 [m]
        parametre['infrastructure'] = 2

        # Définition des paramètres relatifs au cas étudié
        parametre['R'] = 0.2  # Rayon du bloc = 0.2 [m]
        parametre['mud'] = 0.35  # Coefficient de frottement = 0.35 [-]
        parametre['eymu'] = 0.7  # Moyenne du coefficient de rebond = 0.7 [-]
        parametre['eysig'] = 0.1  # Variance du coefficient de rebond = 0.1 [-]
        parametre['VXmu'] = 1  # Moyenne de la vitesse initiale = 1 [m/s]
        parametre['VXsig'] = 0.2  # Variance de la vitesse initiale = 0.2 [m/s]

        # Calcul de l'altitude topographique à l'emplacement de l'ouvrage de protection
        if Xo < topo[0, 1]:
            Yprotect = np.interp(Xo, topo[0, 0:2], topo[1, 0:2])
        elif Xo < topo[0, 2]:
            Yprotect = np.interp(Xo, topo[0, 1:3], topo[1, 1:3])
        else:
            Yprotect = 0

    elif Cas == 5:  # Sclaigneau
        # Definition of the topography
        topo = np.array([[0, 0, 1, 1, 2, 2, 30],  # Selon X
                         [26, 22, 21, 16, 15, 0, 0]])  # Selon Y

        # Definition of the minimum and maximum fall heights [m]
        parametre['Hmin'] = 0  # 0 [m]
        parametre['Hmax'] = 22  # 22 [m]

        # Definition of the type of infrastructure to protect (1 = house and 2 = train)
        # and its position.
        parametre['Xt'] = 9  # 9 [m]
        parametre['infrastructure'] = 2

        # Definition of parameters related to the case being studied
        parametre['R'] = 0.2  # Rayon du bloc = 0.2 [m]
        parametre['mud'] = 0.7  # Coefficient de frottement = 0.7 [-]
        parametre['eymu'] = 0.4  # Moyenne du coefficient de rebond = 0.4 [-]
        parametre['eysig'] = 0.05  # Variance du coefficient de rebond = 0.05 [-]
        parametre['VXmu'] = 0.1  # Moyenne de la vitesse initiale = 0.1 [m/s]
        parametre['VXsig'] = 0.05  # Variance de la vitesse initiale = 0.05 [m/s]

        # Calculate the topographic altitude at the location of the protection structure
        if Xo < topo[0, 1]:
            Yprotect = np.interp(Xo, topo[0, 0:2], topo[1, 0:2])
        elif Xo < topo[0, 3]:
            Yprotect = np.interp(Xo, topo[0, 2:4], topo[1, 2:4])
        else:
            Yprotect = 0

    elif Cas == 6:  # Anseremme 2
        # Definition of the topography
        topo = np.array([[0, 1, 3, 7, 30],  # Selon X
                         [14, 4, 4, 0, 0]])  # Selon Y

        # Definition of the minimum and maximum fall heights [m]
        parametre['Hmin'] = 4  # 4 [m]
        parametre['Hmax'] = 14  # 14 [m]

        # Definition of the type of infrastructure to protect (1 = house and 2 = train)
        # and its position.
        parametre['Xt'] = 10  # 10 [m]
        parametre['infrastructure'] = 1

        # Definition of parameters related to the case being studied
        parametre['R'] = 0.15  # Rayon du bloc = 0.15 [m]
        parametre['mud'] = 0.5  # Coefficient de frottement = 0.5 [-]
        parametre['eymu'] = 0.6  # Moyenne du coefficient de rebond = 0.6 [-]
        parametre['eysig'] = 0.1  # Variance du coefficient de rebond = 0.1 [-]
        parametre['VXmu'] = 0.5  # Moyenne de la vitesse initiale = 0.5 [m/s]
        parametre['VXsig'] = 0.1  # Variance de la vitesse initiale = 0.1 [m/s]

        # Calculate the topographic altitude at the location of the protection structure
        if Xo < topo[0, 1]:
            Yprotect = np.interp(Xo, topo[0, 0:2], topo[1, 0:2])
        elif Xo < topo[0, 2]:
            Yprotect = topo[1, 2]
        elif Xo < topo[0, 3]:
            Yprotect = np.interp(Xo, topo[0, 2:4], topo[1, 2:4])
        else:
            Yprotect = 0

    elif Cas == 7:  # Corphalie
        # Definition of the topography
        topo = np.array([[0, 5, 5, 9, 24, 60],  # Selon X
                         [45, 40, 20, 20, 0, 0]])  # Selon Y

        # Definition of the minimum and maximum fall heights [m]
        parametre['Hmin'] = 20  # 20 [m]
        parametre['Hmax'] = 45  # 45 [m]

        # Definition of the type of infrastructure to protect (1 = house and 2 = train)
        # and its position.
        parametre['Xt'] = 30  # 30 [m]
        parametre['infrastructure'] = 2

        # Definition of parameters related to the case being studied
        parametre['R'] = 0.15  # Rayon du bloc = 0.15 [m]
        parametre['mud'] = 0.5  # Coefficient de frottement = 0.5 [-]
        parametre['eymu'] = 0.4  # Moyenne du coefficient de rebond = 0.4 [-]
        parametre['eysig'] = 0.05  # Variance du coefficient de rebond = 0.05 [-]
        parametre['VXmu'] = 1  # Moyenne de la vitesse initiale = 1 [m/s]
        parametre['VXsig'] = 0.05  # Variance de la vitesse initiale = 0.05 [m/s]

        # Calculate the topographic altitude at the location of the protection structure
        if Xo < topo[0, 1]:
            Yprotect = np.interp(Xo, topo[0, 0:2], topo[1, 0:2])
        elif Xo < topo[0, 3]:
            Yprotect = topo[1, 3]
        elif Xo < topo[0, 4]:
            Yprotect = np.interp(Xo, topo[0, 3:5], topo[1, 3:5])
        else:
            Yprotect = 0

    elif Cas == 8:  # Chêneu
        # Definition of the topography
        topo = np.array([[0, 0, 2, 2, 7, 7, 35],  # Selon X
                         [21, 19, 17, 14, 10, 0, 0]])  # Selon Y

        # Definition of the minimum and maximum fall heights [m]
        parametre['Hmin'] = 19  # 19 [m]
        parametre['Hmax'] = 21  # 21 [m]

        # Definition of the type of infrastructure to protect (1 = house and 2 = train)
        # and its position.
        parametre['Xt'] = 15  # 15 [m]
        parametre['infrastructure'] = 1

        # Definition of parameters related to the case being studied
        parametre['R'] = 0.2  # Rayon du bloc = 0.2 [m]
        parametre['mud'] = 0.7  # Coefficient de frottement = 0.7 [-]
        parametre['eymu'] = 0.4  # Moyenne du coefficient de rebond = 0.4 [-]
        parametre['eysig'] = 0.05  # Variance du coefficient de rebond = 0.05 [-]
        parametre['VXmu'] = 0.2  # Moyenne de la vitesse initiale = 0.2 [m/s]
        parametre['VXsig'] = 0.05  # Variance de la vitesse initiale = 0.05 [m/s]

        # Calculate the topographic altitude at the location of the protection structure
        if Xo < topo[0, 1]:
            Yprotect = np.interp(Xo, topo[0, 0:2], topo[1, 0:2])
        elif Xo < topo[0, 3]:
            Yprotect = np.interp(Xo, topo[0, 2:4], topo[1, 2:4])
        else:
            Yprotect = 0

    elif Cas == 9:  # Rue Saint-Martin, Namur
        # Definition of the topography
        topo = np.array([[0, 0, 18, 18, 35],  # Selon X
                         [13, 10, 2, 0, 0]])  # Selon Y

        # Definition of the minimum and maximum fall heights [m]
        parametre['Hmin'] = 2  # 2 [m]
        parametre['Hmax'] = 13  # 13 [m]

        # Definition of the type of infrastructure to protect (1 = house and 2 = train)
        # and its position.
        parametre['Xt'] = 20  # 20 [m]
        parametre['infrastructure'] = 1

        # Definition of parameters related to the case being studied
        parametre['R'] = 0.15  # Rayon du bloc = 0.15 [m]
        parametre['mud'] = 0.6  # Coefficient de frottement = 0.6 [-]
        parametre['eymu'] = 0.45  # Moyenne du coefficient de rebond = 0.45 [-]
        parametre['eysig'] = 0.05  # Variance du coefficient de rebond = 0.05 [-]
        parametre['VXmu'] = 0.5  # Moyenne de la vitesse initiale = 0.5 [m/s]
        parametre['VXsig'] = 0.1  # Variance de la vitesse initiale = 0.1 [m/s]

        # Calculate the topographic altitude at the location of the protection structure
        if Xo < topo[0, 1]:
            Yprotect = np.interp(Xo, topo[0, 0:2], topo[1, 0:2])
        else:
            Yprotect = 0

    elif Cas == 10:  # Conflan, Savoie
        # Définition de la topographie
        topo = np.array([[0, 1, 2, 3, 35],  # Selon X
                         [35, 30, 10, 0, 0]])  # Selon Y

        # Définition des hauteurs de chutes min et max [m]
        parametre['Hmin'] = 0  # 0 [m]
        parametre['Hmax'] = 35  # 35 [m]

        # Définition du type d'infrastructure à protéger (1 = maison et 2 = train)
        # ainsi que de sa position.
        parametre['Xt'] = 7  # 7 [m]
        parametre['infrastructure'] = 1

        # Définition des paramètres relatifs au cas étudié
        parametre['R'] = 0.1  # Rayon du bloc = 0.1 [m]
        parametre['mud'] = 0.5  # Coefficient de frottement = 0.5 [-]
        parametre['eymu'] = 0.4  # Moyenne du coefficient de rebond = 0.4 [-]
        parametre['eysig'] = 0.05  # Variance du coefficient de rebond = 0.05 [-]
        parametre['VXmu'] = 0.2  # Moyenne de la vitesse initiale = 0.2 [m/s]
        parametre['VXsig'] = 0.1  # Variance de la vitesse initiale = 0.1 [m/s]

        # Calcul de l'altitude topographique à l'emplacement de l'ouvrage de protection
        if Xo < topo[0, 1]:
            Yprotect = np.interp(Xo, topo[0, 0:2], topo[1, 0:2])  # Pente
        elif Xo < topo[0, 2]:
            Yprotect = np.interp(Xo, topo[0, 1:3], topo[1, 1:3])  # Pente
        elif Xo < topo[0, 3]:
            Yprotect = np.interp(Xo, topo[0, 2:4], topo[1, 2:4])  # Pente
        else:
            Yprotect = 0  # Sol

    else:
        raise ValueError("Cas should be an integer between 1 and 10.")

    # Ajout des paramètres communs

    # Extension de la limite du terrain à 70m pour tous les groupes, de sorte à ce que le calcul s'arrête automatiquement au-delà.
    topo[0,-1] = 70  # Selon x [m]

    # Enregistrement de la topographie dans les paramètres
    parametre['topo'] = topo

    # Calcul de paramètres dépendants d'autres paramètres
    parametre['M'] = (4 / 3) * math.pi * parametre['R']**3 * parametre['rho']  # Masse du bloc [kg/m³]
    parametre['J'] = (2 / 5) * parametre['M'] * parametre['R']**2  # Inertie de rotation [kg.m²]
    
    return parametre, Yprotect


