import numpy as np
from scipy.optimize import fsolve
import math

def my_ROCKFELLER(Parametre, Variables):

    g = 9.81  # [m/s²]

# Routine 1 : INTERSECTION
# Routine qui permet de déterminer s'il y a un contact entre le bloc et
# la topographie. On peut vérifier s'il y a une intersection et/ou un
# contact parfait.

    def intersection(topo, pente, alpha, X0, Y0, R, VY0, VX0):

        # Calcul des positions extrêmes du bloc
        X1 = X0 - R
        X2 = X0 + R

        # Initialisation de certains Paramètres
        work = 1

        # Localisation des segments présents entre X0-R et X0+R
        Segments = []
        Num_segment = 0

        for i in range(topo.shape[1] - 1):
            # Conditions individuelles sur le bloc : chacune de ses extrémités est
            # comprise dans le segment
            cr1 = (X1 >= topo[0,i] and X1 <= topo[0,i + 1])  # Côté gauche du bloc dans le segment
            cr2 = (X2 >= topo[0,i] and X2 <= topo[0,i + 1])  # Côté droit du bloc dans le segment
            # Conditions globales sur le bloc : soit il est à l'intérieur du
            # segment, soit il englobe le segment
            cr3 = (topo[0,i] >= X1 and topo[0,i + 1] <= X2)  # Le segment est englobé dans le bloc
            cr4 = (topo[0,i] <= X1 and topo[0,i + 1] >= X2)  # Le bloc est à l'intérieur du segment

            if max(cr1, cr2, cr3, cr4):  # Si une des conditions est respectée
                Segments.append(i)  # On retient dans quel segment le bloc se trouve
                Num_segment += 1

        # Recherche des points de contacts éventuels : il peut y en avoir > 1

        if len(Segments)==2 :
            Segments = [Segments[1]]

        inter = [0] * len(Segments)
        contact = [0] * len(Segments)
        l_sl = [0] * len(Segments)

        for i in range(len(Segments)):
            # Cas n°1, il y a intersection entre le prédicteur et la droite de topographie

            # Détermination des coordonnées du début du segment, ainsi que de sa pente
            Xi = topo[0,Segments[i]]
            Yi = topo[1,Segments[i]]
            d = pente[Segments[i]]

            # Calcul de la condition pour avoir un contact (DELTA) et de la vitesse
            # normale du bloc à cet instant
            A = (1 + d**2)
            B = (2 * d * (Yi - Y0 - d * Xi) - 2 * X0)
            C = X0**2 + (Yi - Y0 - d * Xi)**2 - R**2
            DELTA = B**2 - 4 * A * C
            VN0 = VX0 * math.sin(alpha[Segments[i]]) + VY0 * math.cos(alpha[Segments[i]])

            # Vérification d'une certaine tolérance pour avoir contact
            if abs(DELTA) < 1E-3 and abs(VN0) < 1E-2:
                DELTA = 0

            # Si DELTA positif, alors il y a une intersection entre le bloc et le segment
            # sur lequel il se trouve. Si DELTA nul, alors le contact est parfait.
            # /!\ On accepte une légère erreur donc on vérifie quand même le cas du
            # contact parfait
            if DELTA >= 0:

                # Calcul des deux racines (positions possibles du contact entre le bloc
                # et le segment)
                Xs1 = (-B + math.sqrt(DELTA)) / (2 * A)
                Xs2 = (-B - math.sqrt(DELTA)) / (2 * A)

                if (Xs1 >= topo[0,Segments[i]] and Xs1 <= topo[0,Segments[i]+1]) or ( Xs2 >= topo[0,Segments[i]] and Xs2 <= topo[0,Segments[i]+1]):

                    # On enregistre dans quel segment se trouve le bloc
                    l_sl[i] = Segments[i] 

                    # Est-ce un contact parfait ou bien le bloc intersecte-t'il la
                    # topographie ? (À un epsilon près, donc si les deux positions
                    # de contact sont suffisamment proches, on parle d'un contact
                    # parfait
                    if abs(Xs1-Xs2) < R*1E-5:
                        contact[i] = 1 # Contact parfait
                    else:
                        inter[i] = 1 # Intersection
            else:

                Xs = []        
        

            # Cas n°2, le bloc est passé sous la droite sans l'intersecter !
            
            # Si la pente est non-nulle, on calcule le point d'intersection entre
            # une droite normale à la topographie et qui passe par le centre du
            # prédicteur, et la droite tangente à la topographie.
            if pente[Segments[i]] != 0:
                
                # Calcul de la position selon X
                X_i = (Y0-topo[1,Segments[i]]+pente[Segments[i]]*topo[0,Segments[i]]+X0/pente[Segments[i]])/(pente[Segments[i]]+1/pente[Segments[i]])
                
                # Prise en compte d'une certaine erreur machine
                if abs(X_i) < 1E-8 :
                    X_i = 0 
                
                # Calcul de la position selon Y
                Y_i = topo[1,Segments[i]]+pente[Segments[i]]*(X_i-topo[0,Segments[i]])
                
                # Prise en compte d'une certaine erreur machine
                if abs(Y_i) < 1E-8:
                    Y_i = 0
                
            else: # Si la pente est nulle, alors la position selon X est celle du centre
                  # du bloc et sa position selon Y est connue par la topographie
                X_i = X0
                Y_i = topo[1,Segments[i]]
            
            # On vérifie que le bloc appartienne bien au segment et se trouve sous
            # la topographie, ce qui signifie qu'il y a intersection.
            if Y0 < Y_i and X_i >= topo[0,Segments[i]] and X_i <= topo[0,Segments[i]+1]:
                
                l_sl[i] = Segments[i]
                inter[i] = 1

        # S'il y a contact avec le bloc sur le premier segment, on continue 
        # à rouler/glisser sur lui. Comme on peut en rencontrer un autre après, 
        # le post-rebond s'assure qu'on ne transperce rien !

        if not contact :
            
            work = 0 
            
        elif contact[0] == 1:
            
            # On retient qu'il y a contact, pas d'intersection, et on retient le
            # numéro du segment sur lequel le contact se fait.
            contact = 1
            inter = 0 
            l_sl = l_sl[0]
            
        elif np.count_nonzero(contact) == 0: # Si aucun segment n'a de contact (donc la matrice contact est remplie de 0)
            
            if np.count_nonzero(inter) > 0: # S'il y a eu une intersection
                
                # On retient le segment de l'intersection, et on annonce qu'il y a
                # eu intersection et non contact
                l_sl = l_sl[inter==1]
                inter = 1
                contact = 0
                
            else:
                
                # Il n'y a ni contact, ni intersection
                inter = 0
                contact = 0

        return contact, l_sl, inter, work

# Routine 2 : CALCUL_PREDICT
# Routine qui calcule le prédicteur au pas suivant, selon le cas envisagé

    def calcul_predict(contact,glissement,mu_d,alpha,R,M,VX_prec,VY_prec,X_prec,Y_prec,THETA_prec,THETAV_prec,dt,l_sl):
       
        # Initialisation de certains paramètres
        g = 9.81
        work = 1
        J = 2/5 * M * R**2 # Inertie de rotation

        if contact==1 and glissement==0: # Roulement sans glissement
            
            # Calcul de la vitesse et l'accélération du bloc
            v0 = VX_prec * math.cos(alpha[l_sl]) - VY_prec * math.sin(alpha[l_sl])
            acc = M/(M+J/R**2) * g * math.cos(alpha[l_sl]) * (math.tan(alpha[l_sl]) - mu_d[l_sl])
            
            # Calcul des incréments
            dv = acc*dt
            dthetav = acc*dt/R
            dtheta = acc*dt**2/2/R+v0/R*dt
            dx = acc*dt**2/2+v0*dt
            
            # Actualisation des vitesses et positions
            VX_curr = VX_prec+dv*math.cos(alpha[l_sl])
            VY_curr = VY_prec-dv*math.sin(alpha[l_sl])
            X_curr = X_prec+dx*math.cos(alpha[l_sl])
            Y_curr = Y_prec-dx*math.sin(alpha[l_sl])
            THETA_curr = THETA_prec+dtheta
            THETAV_curr = THETAV_prec+dthetav
            
        elif contact==1 and glissement ==1 : # Roulement avec glissement

            # Calcul de la vitesse et de l'accélération du bloc
            v0 = VX_prec*math.cos(alpha[l_sl])-VY_prec*math.sin(alpha[l_sl])
            acc = g*math.cos(alpha[l_sl])*(math.tan(alpha[l_sl])-mu_d[l_sl])
            
            # Calcul des incréments
            dv = acc*dt
            dx = acc*dt**2/2+v0*dt
            
            # Mise à jour des vitesses et positions du bloc
            VX_curr = VX_prec+dv*math.cos(alpha[l_sl])
            VY_curr = VY_prec-dv*math.sin(alpha[l_sl])
            X_curr = X_prec+dx*math.cos(alpha[l_sl])
            Y_curr = Y_prec-dx*math.sin(alpha[l_sl])
            
            # Calcul des incréments de rotation
            acc = 2/R*g*math.cos(alpha[l_sl])*mu_d[l_sl]
            theta0 = THETA_prec
            dthetav = acc*dt
            dtheta = acc*dt**2/2+theta0*dt
            
            # Actualisation de l'angle et de la vitesse de rotation
            THETA_curr  = THETA_prec  + dtheta
            THETAV_curr = THETAV_prec + dthetav
            
        elif contact==0 : # En cas de chute libre, l'accélération est purement verticale

            # Calcul des incréments de vitesse et de positions
            dvy = -g*dt
            dy = -g*dt**2/2+VY_prec*dt
            dx = VX_prec*dt
            
            # Actualisation des variables
            VX_curr = VX_prec
            VY_curr = VY_prec+dvy
            X_curr = X_prec+dx
            Y_curr = Y_prec+dy
            
            # Calcul de l'incrément de rotation en supposant une vitesse de
            # rotation constante
            dtheta = THETAV_prec*dt
            
            # Mise à jour de l'angle et de la vitesse de rotation
            THETA_curr = THETA_prec+dtheta
            THETAV_curr = THETAV_prec
            
        else: # Arrêt en cas d'erreur
            
            work = 0
            print('Erreur calcul prédicteur')

        #if VX_curr<0 :
            #print('Erreur VX_curr<0')

        return work,VX_curr,VY_curr,X_curr,Y_curr,THETA_curr,THETAV_curr

# Routine 3 : REBONDS
# Routine permettant de gérer les rebonds des blocs. En absence de contact
# et si la trajectoire du bloc intersecte la topographie, alors le bloc va
# rebondir sur le nouveau segment de droite.

    def rebonds(X0,Y0,VX0,VY0,THETA0,THETAV0,topo,pente,l_sl,ex,ey,alpha,dt,R):
      
        # Initialisation de certaines variables
        g = 9.81
        # Détermination des paramètres géométriques du segment étudié
        Xi = topo[0,l_sl]
        Yi = topo[1,l_sl]
        d = pente[l_sl]

        # Définition de certains paramètres
        a = d
        b = -1
        c = Yi-d*Xi

        # Résolution du problème d'intersection entre le bloc et la topographie,
        # pour trouver le temps t auquel le rebond a lieu.

        A = -b*g/2
        B = (a*VX0+b*VY0)
        # Premier cas : intérieur de la racine positif
        C = a*X0+b*Y0+c - R*math.sqrt(a**2+b**2)
        DELTA=B**2-4*A*C

        # Si DELTA est >=0, alors il y aura rebond
        if DELTA >= 0:
            
            t1=(-B+math.sqrt(DELTA))/(2*A)
            t2=(-B-math.sqrt(DELTA))/(2*A)

            if t1<0 or t1>dt:
                t1=1000000

            if t2<0 or t2>dt:
                t2=1000000
        else:
            t1=1000000
            t2=1000000

        # Si l'intérieur de la racine n'est pas positif
        C = a*X0+b*Y0+c + R*math.sqrt(a**2+b**2)
        DELTA=B**2-4*A*C

        # Si DELTA est >=0, alors il y aura rebond
        if DELTA>=0:
            t3=(-B+math.sqrt(DELTA))/(2*A)
            t4=(-B-math.sqrt(DELTA))/(2*A)
            
            if t3<0 or t3>dt:
                t3=1000000

            if t4<0 or t4>dt:
                t4=1000000
            
        else:
            t3=1000000
            t4=1000000
 
        # Dans le cas où le bloc va intersecter EXACTEMENT le noeud entre deux
        # segments de la topographie

        coin = 0 
        tp = min(t1, t2, t3, t4) 

        if tp == 1000000 :
            tp = []

        # En absence de résultat pour ti, c'est à dire en absence de rebond, alors
        # on résout un système plus précis avec des valeurs initiales différentes
        # en fonction du résultat.
        if tp!=0 and np.any(tp)==0:
            
            t0 = dt/10
            tp, coin = point(X0,Y0,VX0,VY0,Xi,Yi,R,t0)
            
            if np.any(tp)==1 and tp<0 :
                
                t0=0.05
                tp, coin = point(X0,Y0,VX0,VY0,Xi,Yi,R,t0)
                
                if tp<0:
                    
                    tp = []

        # En absence de rebond tout de même, alors les résultats finaux sont égaux
        # aux initiaux
        if tp!=0 and np.any(tp)==0:
            
            XF=X0
            YF=Y0
            VXF=VX0
            VYF=VY0
            VT0=VX0*math.cos(alpha[l_sl])-VY0*math.sin(alpha[l_sl])
            VN0=0
            THETAF=THETA0
            tp=10
            
        else: # En cas de rebond, on actualise les valeurs.
            
            XF=X0+VX0*tp
            YF=Y0+VY0*tp-g*tp**2/2
            VXr=VX0
            VYr=VY0-g*tp
            dtheta=THETAV0*dt
            THETAF=THETA0+dtheta
            
            # Si l'intersection se fait dans un coin, alors on réalise une moyenne
            # entre les angles des deux pentes et on actualise les valeurs sur base
            # de cela. Dans tous les cas, on actualise les vitesses normales et
            # tangentielles pour tenir compte du rebond.
            if coin == 1:
                
                theta=(alpha[l_sl]+alpha[l_sl-1])/2
                
                VT0=VXr*math.cos(theta)-VYr*math.sin(theta)
                VN0=VXr*math.sin(theta)+VYr*math.cos(theta)
                
                # Application du coefficient de rebond
                VN0=-VN0*(ey[l_sl]+ey[l_sl-1])/2
                VT0=VT0*(ex[l_sl]+ex[l_sl-1])/2
                
                # Retransformation en vitesses selon X et Y après le rebond
                VXF=VT0*math.cos(theta)+VN0*math.sin(theta)
                VYF=VN0*math.cos(theta)-VT0*math.sin(theta)
                
            else:
                
                VT0=VXr*math.cos(alpha[l_sl])-VYr*math.sin(alpha[l_sl])
                VN0=VXr*math.sin(alpha[l_sl])+VYr*math.cos(alpha[l_sl])
                
                # Application du coefficient de rebond
                VN0=-VN0*ey[l_sl]
                VT0=VT0*ex[l_sl]
                
                # Retransformation en vitesses selon X et Y après le rebond
                VXF=VT0*math.cos(alpha[l_sl])+VN0*math.sin(alpha[l_sl])
                VYF=VN0*math.cos(alpha[l_sl])-VT0*math.sin(alpha[l_sl])
              
        return XF,YF,THETAF,VXF,VYF,VN0,VT0,tp

# Routine 4 : POINT

    def point(X0,Y0,VX0,VY0,Xp,Yp,R,t0):

        # Initialisation de certains paramètres
        g = 9.81
        coin = 0

    # Résolution du système
        A = g**2/4
        B = -VY0*g
        C = VX0**2+VY0**2+Yp*g-g*Y0
        D = -2*Xp*VX0+2*X0*VX0-2*VY0*Yp+2*Y0*VY0
        E = Xp**2+X0**2-2*X0*Xp+Yp**2+Y0**2-2*Yp*Y0-R**2

        def func(x):
            return A*x**4+B*x**3+C*x**2+D*x+E
        x,infodict,ier,mesg = fsolve(func,[t0,t0,t0,t0])
        del infodict, mesg

        if ier == 1 :
            t = x 
        else :
            t = []

        return t,coin
    
# Routine 5 : VERIF
# Si le mobile glissait ou roulait sans glisser sur un tronçon de pente, on
# vérifie qu'il ne rencontre pas un autre tronçon après le prédicteur. En
# effet, la routine intersection passe outre ce genre de considérations.
# Attention ! Cette routine ne fonctionne que pour un VX positif, utiliser le sign(VX) 
# pour que tous les cas soient possibles

    def verif(X_prec,Y_prec,VX_prec,VY_prec,THETA_prec,THETAV_prec,X_curr,Y_curr,VX_curr,VY_curr,THETA_curr,THETAV_curr,pente,alpha,topo,mu_d,ex,ey,l_sl,R,glissement,t):
       
        # Initialisation de certains paramètres
        g=9.81
        Xi=topo[0,l_sl+1]
        Yi=topo[1,l_sl+1]
        d1=pente[l_sl]
        d2=pente[l_sl+1]

        # Calcul de l'intersection entre une droite parallèle au tronçon i et le
        # tronçon i+1
        xint = (Yi-Y_prec+d1*X_prec-d2*Xi)/(d1-d2) # prévoir un garde-fou si les pentes sont identiques !
        yint = Y_prec+d1*(xint-X_prec)

        # Calcul du point de la position du CG du mobile correspondant à ce cas
        # limite
        dx=R/math.sin(alpha[l_sl]-alpha[l_sl+1]) * math.cos(alpha[l_sl])
        dy=R/math.sin(alpha[l_sl]-alpha[l_sl+1]) * math.sin(alpha[l_sl])
        xlim=xint-dx
        ylim=yint+dy

        # Test avec le prédicteur pour voir si on dépasse la limite. Si oui, alors
        # on amène le bloc en position de rebond sur le tronçon suivant.
        if X_curr > xlim:
            
            X_curr = xlim
            Y_curr = ylim
            tp = (xlim-X_prec)/VX_prec
            
            # On réalise le calcul en cas de roulement avec ou sans glissement.
            if glissement==0:
                acc=2/3*g*(math.sin(alpha[l_sl]))
                dthetav=acc*t/R
                dtheta=acc*t**2/2/R+math.sqrt(VX_prec**2+VY_prec**2)/R*t
            else:
                acc=g*(math.sin(alpha[l_sl])-mu_d[l_sl]*math.cos(alpha[l_sl]))
                dthetav=acc*t
                dtheta=acc*t**2/2+THETA_prec*t
            
            accx=acc*math.cos(alpha[l_sl])
            accy=acc*math.sin(alpha[l_sl])
            THETA_curr=THETA_prec+dtheta
            THETAV_curr=THETAV_prec+dthetav
            
            # On actualise les vitesses au moment du rebond sur le tronçon suivant
            VXr=VX_prec*accx*t
            VYr=VY_prec*accy*t
            VT0=VXr*math.cos(alpha[l_sl+1])-VYr*math.sin(alpha[l_sl+1])
            VN0=VXr*math.sin(alpha[l_sl+1])+VYr*math.cos(alpha[l_sl+1])
            
            # On applique le coefficient de rebond
            VN0=-VN0*ey[l_sl]
            VT0=VT0*ex[l_sl]
            
            # Retransformation en vitesses selon X et Y après le rebond
            VX_curr=VT0*math.cos(alpha[l_sl+1])+VN0*math.sin(alpha[l_sl+1])
            VY_curr=VN0*math.cos(alpha[l_sl+1])-VT0*math.sin(alpha[l_sl+1])
            
            # On actualise le temps de calcul
            t=t-tp
            
            # On repasse en rebond sans contact
            contact=0
            
            
        else: # Si on ne dépasse pas la limite, alors rien ne change et on garde le contact lors du roulement.
            
            # On garde le contact et repart de 0s
            contact=1
            t=0

        return X_curr,Y_curr,VX_curr,VY_curr,THETA_curr,THETAV_curr,contact,t

# DEBUT ROUTINE ROCKFELLER À PROPREMENT PARLER

    # Données d'entrée

    g = 9.81  # [m/s²]

    topo = Parametre['topo'] # la géométrie de la paroi rocheuse
    mu_d = Parametre['mu_d'] # le coefficient de frottement dynamique
    ey = Parametre['ey'] # le coefficient de rebond pour la vitesse normale
    ex = Parametre['ex'] # le coefficient de rebond pour la vitesse tangentielle
    M = Parametre['M'] # la masse du mobile
    R = Parametre['R'] # le rayon du bloc considéré comme étant circulaire
    dt = Parametre['dt'] # le pas de temps pour le calcul des trajectoires
    
    X = [Variables['X']]
    Y = [Variables['Y']]
    VY = [Variables['VY']]
    VX = [Variables['VX']]
    THETA = [Variables['THETA']]
    THETAV = [Variables['THETAV']]

    # Conditions pour éviter des problèmes par la suite
    work = 1 # Si =1, alors le code peut tourner, si =0, c'est qu'il y a une erreur.

    if dt > 1:
        print('Valeur de dt supérieure à 1.')
        work = 0
    elif R < 0.01:
        print("Pas la peine de calculer ça pour un si petit caillou !")
        work = 0
    elif np.any(ey > 1):
        print('Attention: Coefficient e_y > 1 !')
        work = 0
    elif np.any(ex > 1):
        print('Attention: Coefficient e_x > 1 !')
        work = 0
    elif np.any(mu_d > 1) or np.any(mu_d < 0):
        print('Coefficient de frottement négatif ou supérieur à 1!')
        work = 0
    elif VX[0] < 0:
        print('Vitesse initiale négative')
        work = 0

    # Début de la routine de calcul

    # Calcul des pentes des différents tronçons (et leur angles)
    pente = [0] * (topo.shape[1]-1)
    alpha = [0] * (topo.shape[1]-1)
    for i in range(topo.shape[1]-1):
        if (topo[0,i+1]-topo[0,i]) != 0 : # Si tronçon non vertical
            pente[i] = (topo[1,i+1]-topo[1,i])/(topo[0,i+1]-topo[0,i])

        alpha[i] = -(math.atan(pente[i]))  # Angle entre deux tronçons [rad]

        #if alpha[i]<0 :
        #    alpha[i]=abs(alpha[i]) #-0.0 #Correction pour VX négative si tronçon à pente négative

    # Roulement avec ou sans glissement ? (voir article Marghitu)
    gliss = [0] * topo.shape[1]
    for i in range(topo.shape[1]-1):
        if math.tan(alpha[i])>=3*mu_d[i]:
            gliss[i]=1

    # Définition du tronçon de départ et du précédent, ainsi que du temps
    # initial
    l_sl = 0 
    l_slprec = 0 
    time = [0]
    type = [0]

    # Type de mouvement à l'instant initial: Contact, intersection ou rien ?

    contact,l_sl,inter,work = intersection(topo,pente,alpha,X[0],Y[0],R,VY[0],VX[0])

    # Enregistrement du type de mouvement: Roulement avec glissement, sans
    # glissement ou chute libre
    if contact == 1:
        
        if gliss[0]:
            type[0] = 2  # Si contact et glissement : roulement avec glissement
        else:
            type[0] = 1  # Si contact sans glissement : roulement sans glissement
        
    elif contact==0:
        type[0] = 3  # Si pas de contact : chute libre

    else :
        work = 0

    # Début du calcul : initialisation du pas à 1 et vérification de la valeur
    # de la variable "work"

    j_step = 0

    while work==1:
        
        # Incrémentation du pas et calcul du temps
        j_step = j_step+1 

        time.append(time[j_step-1]+dt)
        
        if type[j_step-1]==1: # Roulement sans glissement
            contact = 1
            glissement = 0
        elif type[j_step-1]==2: # Roulement avec glissement
            contact = 1
            glissement = 1
        elif type[j_step-1]==3: # Chute libre
            contact = 0 
            inter = 0
            glissement = 0
        
        # Enregistrement des valeurs des pas précédents
        X_prec=X[j_step-1]
        Y_prec=Y[j_step-1]
        VX_prec=VX[j_step-1]
        VY_prec=VY[j_step-1]
        THETA_prec=THETA[j_step-1]
        THETAV_prec=THETAV[j_step-1]
        type_prec=type[j_step-1]
        t = dt

        # Initialisation du nombre d'itération et début de la boucle de calcul
        n_iterations=0
        
        while t >0:
            n_iterations = n_iterations+1
            
            # Calcul de la position suivante à l'aide d'un prédicteur
            work,VX_curr,VY_curr,X_curr,Y_curr,THETA_curr,THETAV_curr = calcul_predict(contact,glissement,mu_d,alpha,R,M,VX_prec,VY_prec,X_prec,Y_prec,THETA_prec,THETAV_prec,t,l_slprec)
            
            # On vérifie si la position suivante intersecte ou rentre en
            # contact avec la topographie
            contact,l_sl,inter,work = intersection(topo,pente,alpha,X_curr,Y_curr,R,VY_curr,VX_curr)

            # Si le segment sur lequel on se trouve existe et n'est pas nul,
            # alors en cas de contact, le glissement du pas précédent est
            # fourni au pas actuel????
            if contact==1 and np.count_nonzero(np.add(l_sl,1).tolist())>0:
                glissement=gliss[contact==1]
            else:
                glissement=0
            
            # En absence de contact et si la trajectoire intersecte la
            # topographie, il faut gérer un rebond.
            if contact==0 and inter==1:
                
                # On s'assure qu'aucune ancienne variable n'est récupérée
                Xinter = [0]*len([inter])
                Yinter = [0]*len([inter])
                tp = [0]*len([inter])
                XF = [0]*len([inter])
                YF = [0]*len([inter])
                VXinter = [0]*len([inter])
                VYinter = [0]*len([inter])
                THETAinter = [0]*len([inter])
                THETAVinter = [0]*len([inter])
                VN = [0]*len([inter])
                VT = [0]*len([inter])
                
                # On initialise le segment actuel
                l_slcurr=[]

                # On calcule le point de rebonds
                for j in range(len([inter])) :
                    Xinter[j],Yinter[j],THETAinter[j],VXinter[j],VYinter[j],VN[j],VT[j],tp[j] = rebonds(X_prec,Y_prec,VX_prec,VY_prec,THETA_prec,THETAV_prec,topo,pente,[l_sl][j],ex,ey,alpha,t,R)

                # En absence de temps de rebond, on repasse en roulement avec ou sans glissement
                if tp!=[0] and np.any(tp)==0:
                    
                    if gliss[l_slprec]:
                        type_prec=2
                    else:
                        type_prec=1
                    
                else: # Si plusieurs solutions au problème du rebond existe, alors on prend la solution la plus proche
                    
                    # Choix du plus petit temps auquel le rebond a lieu (on
                    # retient son index)
                    index = tp.index(min(tp))
                    
                    # L'ancienne vitesse de rotation devient la nouvelle
                    THETAV_curr=THETAV_prec
                    
                    # Si le temps auquel se passe le rebond est le temps
                    # actuel, alors on sauvegarde les valeurs dans les
                    # variables actuelles
                    if t-tp[index]==0:
                        
                        X_curr=Xinter[index]
                        Y_curr=Yinter[index]
                        VX_curr=VXinter[index]
                        VY_curr=VYinter[index]
                        VN=VN[index]
                        VT=VT[index]
                        THETA_curr=THETAinter[index]
                        l_slcurr=l_sl[index]
                        
                    else: # Sinon, on sauvegarde les valeurs dans celles du pas précédent
                        
                        X_prec=Xinter[index]
                        Y_prec=Yinter[index]
                        VX_prec=VXinter[index]
                        VY_prec=VYinter[index]
                        VN=VN[index]
                        VT=VT[index]
                        THETA_prec=THETAinter[index]
                        l_sl = [l_sl]
                        l_slprec=l_sl[index]
                    
                    # On remet le contact et l'intersection à 0 puisqu'on
                    # repart en chute libre (rebond)
                    contact=0
                    inter=0
                    
                    # On réalise un test sur la vitesse de rebond normale :
                    # Si elle est inférieure à un certain seuil, alors on
                    # change de mouvement (de chute libre à roulement) mais on
                    # garde les mêmes positions actuelles
                    if np.any(VN)==0 or abs(VN)<0.01 or tp[index]<0.0001:
                        
                        VN = 0 
                        
                        if t-tp[index]==0:
                            
                            VX_curr=VT*math.cos(alpha[l_slcurr])
                            VY_curr=-VT*math.sin(alpha[l_slcurr])
                            glissement=gliss[l_slcurr]
                            
                        else:
                            
                            VX_prec=VT*math.cos(alpha[l_slprec])
                            VY_prec=-VT*math.sin(alpha[l_slprec])
                            glissement=gliss[l_slprec]
                        
                        # Le mouvement change pour redevenir du roulement
                        contact=1
                        inter=0
                       
                    # Actualisation du temps de calcul
                    t = t-tp[index]
                    
            # En cas de contact sans intersection, on roule avec ou sans
            # glissement le long de la surface précédente, on doit alors
            # vérifier qu'on ne change pas de surface ou de type de mouvement.
            elif contact==1 and inter==0 and l_slprec!=topo.shape[1]-2:
                
                X_curr,Y_curr,VX_curr,VY_curr,THETA_curr,THETAV_curr,contact,t = verif(X_prec,Y_prec,VX_prec,VY_prec,THETA_prec,THETAV_prec,X_curr,Y_curr,VX_curr,VY_curr,THETA_curr,THETAV_curr,pente,alpha,topo,mu_d,ex,ey,l_slprec,R,glissement,t)
                
                b=0
                
            else:
                
                t=0
                
            if n_iterations>200: # pour éviter de tomber dans un problème de boucle infinie, souvent
                                        # dû à un bloc qui rencontre un coin
                work=0
                print('Erreur: boucle infinie')
                break

        # En cas de contact, on vérifie les paramètres à postériori pour éviter
        # l'accumulation d'erreurs numériques
        if contact==1: 
            
            # Définition des paramètres géométriques du segment
            Xi=topo[0,l_slprec]
            Yi=topo[1,l_slprec]
            d=pente[l_slprec]
            
            # Calcul de la distance du point final au segment
            a=-d
            b=1
            c=d*Xi-Yi

            dist=abs(a*X_curr+b*Y_curr+c)/math.sqrt(a**2+b**2)
            
            if abs(dist)<R:
                X_curr=X_curr+(R-dist)*math.sin(alpha[l_slprec])
                Y_curr=Y_curr+(R-dist)*math.cos(alpha[l_slprec])
            
        # Sauvetage des résultats
        X.append(X_curr)
        Y.append(Y_curr)
        VX.append(VX_curr)
        VY.append(VY_curr)
        THETA.append(THETA_curr)
        THETAV.append(THETAV_curr)

        # Définition et sauvetage du type de mouvement à la fin du pas
        if np.any(contact) and isinstance(contact,list) :
            contact = contact[-1]

        if contact==1 and glissement ==0:
              
            type.append(1) # Roulement sans glissement
            
        elif contact==1 and glissement ==1:
            
            type.append(2) # Roulement avec glissement
            
        elif contact==0: # Chute libre
            
            type.append(3)
            
        else: # pour les cas non prévus, stop le programme
            
            type.append(0)
            work=0
            #print('Erreur cas non prévu')
            
        # Condition d'arrêt

        if X[j_step]+R<max(topo[0,:]) :
        
            I = np.argwhere(topo[0,:]>=X[j_step]) # Obtention de la première case X > X0
            
            if I[0,0] != 0 :
                I2 = I[0]
            else :
                I2 = I[1] 

            X1=topo[0,I2-1]
            Y1=topo[1,I2-1]
            X2=topo[0,I2]
            Y2=topo[1,I2]
            Yo=Y1+(Y2-Y1)/(X2-X1)*(X[j_step]-X1)# topographie au pied de l'obstacle

        if X[j_step]+R>max(topo[0,:]): #or Y[j_step]<Yo: # Bloc hors topographie
            work=0
            #print('Bloc hors topographie')
            break
        elif Y[j_step]<Yo: # Bloc hors topographie
            #Y[j_step] = Yo[0]+R
            work=0
            #print('Bloc hors topographie')
            break
        elif math.sqrt(VX[j_step]**2+VY[j_step]**2)<0.01: # Vitesse trop faible
            work=0
            #print('Vitesse trop faible')
            break
        elif  contact==1 and VX[j_step]<0: # Vitesse selon X négative
            work=0
            #print('Vitesse selon X négative')
            break

    Variables['X'] = X
    Variables['Y'] = Y
    Variables['ey'] = ey
    Variables['VX'] = VX
    Variables['VY'] = VY
    Variables['time'] = time
    Variables['type'] = type
    Variables['THETA'] = THETA
    Variables['THETAV'] = THETAV
    
    return Variables, pente