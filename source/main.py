from equilibrage import *
import numpy as np

def main():
    mesure_makespan_liste = []
    mesure_makespan_LPT = []
    mesure_temps_liste = []
    mesure_temps_LPT = []
    
    for m in [10, 50, 100]:

        mesure_makespan_liste_N = []
        mesure_makespan_LPT_N = []
        mesure_temps_liste_N = []
        mesure_temps_LPT_N = []

        for n in [100 , 1000, 10000]:
            makespan_liste = []
            makespan_LPT = []
            temps_liste = []
            temps_LPT = []

            for _ in range(10):
                t_i = rand_instance(n)
                ml, tl = measure(n, m, t_i, eq_liste)
                mlpt, tlpt = measure(n, m, t_i, eq_LPT)
                makespan_liste.append(ml)
                makespan_LPT.append(mlpt)
                temps_liste.append(tl)
                temps_LPT.append(tlpt)
            
            mesure_makespan_liste_N.append(np.mean(makespan_liste))
            mesure_makespan_LPT_N.append(np.mean(makespan_LPT))
            mesure_temps_liste_N.append(np.mean(temps_liste))
            mesure_temps_LPT_N.append(np.mean(temps_LPT))

        mesure_makespan_liste.append(mesure_makespan_liste_N)
        mesure_makespan_LPT.append(mesure_makespan_LPT_N)
        mesure_temps_liste.append(mesure_temps_liste_N)
        mesure_temps_LPT.append(mesure_temps_LPT_N)

    print(np.array(mesure_makespan_liste))
    print(np.array(mesure_makespan_LPT))
    print(np.array(mesure_temps_liste))
    print(np.array(mesure_temps_LPT))

    return 0

if __name__ == "__main__":
    main()
