from equilibrage import *
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt

def main():
    mesure_makespan_liste = []
    mesure_makespan_LPT = []
    mesure_makespan_rl = defaultdict(list)
    mesure_temps_liste = []
    mesure_temps_LPT = []
    mesure_temps_rl = defaultdict(list)
    
    y = [25, 50, 75, 100, 150]
    x = [3, 5, 10, 15, 20]
    for m in x:

        mesure_makespan_liste_N = []
        mesure_makespan_LPT_N = []
        mesure_makespan_rl_N = defaultdict(list)
        mesure_temps_liste_N = []
        mesure_temps_LPT_N = []
        mesure_temps_rl_N = defaultdict(list)

        for n in y:
            print(m,n)
            makespan_liste = []
            makespan_LPT = []
            makespan_rl = defaultdict(list)
            temps_liste = []
            temps_LPT = []
            temps_rl = defaultdict(list)

            for _ in range(30):
                t_i = rand_instance(n, higher=1000)
                ml, tl = measure(n, m, t_i, eq_liste)
                mlpt, tlpt = measure(n, m, t_i, eq_LPT)
                for vo in ["insertion", "echange", "permutation"]:
                    for cr in ["cmax", "lexico", "pair"]:
                        mes, tes = measure(n, m, t_i, recherche_locale, vo = "insertion", cr = "cmax")
                        makespan_rl[vo+cr].append(mes)
                        temps_rl[vo+cr].append(tes)
                makespan_liste.append(ml)
                makespan_LPT.append(mlpt)
                temps_liste.append(tl)
                temps_LPT.append(tlpt)
            
            mesure_makespan_liste_N.append(np.mean(makespan_liste))
            mesure_makespan_LPT_N.append(np.mean(makespan_LPT))
            mesure_temps_liste_N.append(np.mean(temps_liste))
            mesure_temps_LPT_N.append(np.mean(temps_LPT))
            for vo in ["insertion", "echange", "permutation"]:
                for cr in ["cmax", "lexico", "pair"]:
                    mesure_makespan_rl_N[vo+cr].append(np.mean(makespan_rl[vo+cr]))
                    mesure_temps_rl_N[vo+cr].append(np.mean(temps_rl[vo+cr]))

        mesure_makespan_liste.append(mesure_makespan_liste_N)
        mesure_makespan_LPT.append(mesure_makespan_LPT_N)
        mesure_temps_liste.append(mesure_temps_liste_N)
        mesure_temps_LPT.append(mesure_temps_LPT_N)
        for vo in ["insertion", "echange", "permutation"]:
            for cr in ["cmax", "lexico", "pair"]:
                mesure_makespan_rl[vo+cr].append(mesure_makespan_rl_N[vo+cr])
                mesure_temps_rl[vo+cr].append(mesure_temps_rl_N[vo+cr])

    print(np.array(mesure_makespan_liste))
    print(np.array(mesure_makespan_LPT))
    for vo in ["insertion", "echange", "permutation"]:
        for cr in ["cmax", "lexico", "pair"]:
            print(vo,"+",cr)
            print(np.array(mesure_makespan_rl[vo+cr]))
    print(np.array(mesure_temps_liste))
    print(np.array(mesure_temps_LPT))
    for vo in ["insertion", "echange", "permutation"]:
        for cr in ["cmax", "lexico", "pair"]:
            print(vo,"+",cr)
            print(np.array(mesure_temps_rl[vo+cr]))
    
    for i,m in enumerate(x):
        ax = plt.figure(figsize=(16, 12), dpi=160)
        plt.plot(y,mesure_makespan_liste[i], label = "List Scheduling")
        plt.plot( y,mesure_makespan_LPT[i], label = "LPT")
        for vo in ["insertion", "echange", "permutation"]:
            for cr in ["cmax", "lexico", "pair"]:
                plt.plot(y,mesure_makespan_rl[vo+cr][i], '+:', label = vo+"+"+cr)
        plt.legend()
        plt.xlabel("Nombre de tâches")
        plt.ylabel("Makespan de la solution")
        plt.title(f"Qualité des solutions en fonction du nombre de tâches (m={m})")
        plt.savefig("source/out/res_m_"+str(m)+".png", format = 'png')
    for i,m in enumerate(x):
        ax = plt.figure(figsize=(16, 12), dpi=160)
        plt.plot(y,mesure_temps_liste[i], label = "List Scheduling")
        plt.plot( y,mesure_temps_LPT[i], label = "LPT")
        for vo in ["insertion", "echange", "permutation"]:
            for cr in ["cmax", "lexico", "pair"]:
                plt.plot(y,mesure_temps_rl[vo+cr][i], '+:', label = vo+"+"+cr)
        plt.legend()
        plt.xlabel("Nombre de tâches")
        plt.ylabel("Temps (s)")
        plt.title(f"Temps d'execution en fonction du nombre de tâches (m={m})")
        plt.savefig("source/out/temps_m_"+str(m)+".png", format = 'png')

    
    # m = 50
    # n = 500
    # t_i = rand_instance(n, higher = 2000)
    # print("liste")
    # mes = measure(n, m, t_i, eq_liste)
    # print("\t", mes)
    # print("LPT")
    # mes = measure(n, m, t_i, eq_LPT)
    # print("\t", mes)
    # for vo in ["insertion", "echange", "permutation"]:
    #     for cr in ["cmax", "lexico", "pair"]:
    #         print(vo,"+",cr)
    #         mes = measure(n, m, t_i, recherche_locale, vo = "insertion", cr = "cmax")
    #         print("\t", mes)
    
    return 0

if __name__ == "__main__":
    main()
