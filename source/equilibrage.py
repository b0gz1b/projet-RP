from typing import List
from collections import defaultdict
import random, heapq, time
import numpy as np
from copy import copy, deepcopy

def measure(n: int, m: int, t_i: List[int], algo, vo = None, cr = None):
    """
    Renvoie le makespan et le temps d'éxecution d'un algo d'équilibrage des charges
    :param n: Le nombre de tâches
    :param m: Le nombre de machines
    :param t_i: La liste des durées d'execution de chaque tâche
    :param algo: La fonction dont on mesure la performance
    :return: Le makespan et le temps
    """
    if vo == None:
        start = time.time()
        af = algo(n, m, t_i)
        end = time.time()
    else:
        start = time.time()
        af = algo(n, m, t_i, vo, cr)
        end = time.time()

    return makespan(t_i, af), end - start

def rand_instance(n: int, lower: int = 1, higher: int = 1000) -> List[int]:
    """
    Renvoie une instance aléatoire du problème d'équilibrage des charges pour n tâches
    :param n: Le nombre de tâches
    :return: La liste des charges des tâches
    """

    return [random.randint(lower,higher) for _ in range(n)]

def makespan(t_i: List[int], af: dict) -> int:
    """
    Calcul le makespan d'une affectation
    :param t_i: La liste des durées d'execution de chaque tâche
    :param af: Une affectation des tâches
    :return: Le makespan de l'affectation
    """
    charges = []
    
    for m_a in af.values():
        c = 0
        for t in m_a:
            c += t_i[t]
        charges.append(c)

    return max(charges)

def eq_liste(n: int, m: int, t_i: List[int]) -> dict:
    """
    Affecte les tâches aux machines dans un ordre quelconque à la machine la moins chargée
    :param n: Le nombre de tâches
    :param m: Le nombre de machines
    :param t_i: La liste des durées d'execution de chaque tâche
    :return: Une affectation des tâches
    """

    ordre = list(range(n))
    random.shuffle(ordre)

    af = defaultdict(list)
    prio = []
    for machine in range(m):
        prio.append((0,machine))

    for tache in ordre:
        charge, machine = heapq.heappop(prio)
        af[machine].append(tache)
        heapq.heappush(prio, (charge + t_i[tache], machine))
    
    return af

def eq_LPT(n: int, m: int, t_i: List[int]) -> defaultdict:
    """
    Affecte les tâches aux machines dans l'ordre décroissant à la machine la moins chargée
    :param n: Le nombre de tâches
    :param m: Le nombre de machines
    :param t_i: La liste des durées d'execution de chaque tâche
    :return: Une affectation des tâches
    """

    ordre: list = np.argsort(t_i).tolist()
    ordre.reverse()

    af = defaultdict(list)
    prio = []
    for machine in range(m):
        prio.append((0,machine))

    for tache in ordre:
        charge, machine = heapq.heappop(prio)
        af[machine].append(tache)
        heapq.heappush(prio, (charge + t_i[tache], machine))
    
    return af

def insertion(m: int, af: dict, mi: int, mj: int, t: int) -> dict:
    """
    Déplace une tâche de la machine i de af à une autre machine j
    :param m: Le nombre de machines
    :param af: Une affectation des tâches
    :return: Une affectation des tâches
    """
    af_res = deepcopy(af)
    af_res[mi].remove(t)
    af_res[mj].append(t)
    return af_res

def echange(m: int, af: dict, mi, mj, ti, tj) -> dict:
    """
    Echange une tâche de la machine i avec une tâche de la machine j
    :param m: Le nombre de machine
    :param af: Une affectation des tâches
    :return: Une affectation des tâches
    """
    af_res = deepcopy(af)
    af_res[mi].remove(ti)
    af_res[mj].remove(tj)
    af_res[mi].append(tj)
    af_res[mj].append(ti)
    return af_res

def permutation(m: int, af: dict, mi, mj, bi, bj) -> dict:
    """
    Permute un ensemble de tâches de la machine i avec un ensemble de tâches de la machine j
    :param m: Le nombre de machine
    :param af: Une affectation des tâches
    :return: Une affectation des tâches
    """
    af_res = deepcopy(af)
    for ti in bi:
        af_res[mi].remove(ti)
    for tj in bj:
        af_res[mj].remove(tj)
    for tj in bj:
        af_res[mi].append(tj)
    for ti in bi:
        af_res[mj].append(ti)
    return af_res

def lexico(n: int, m: int, t_i: List[int], af1, af2, mi = None, mj = None):
    """
    Renvoie vrai si le makespan de l'affection 2 est meilleur que celui de l'affectation 1 et en cas d'égalité, si le nombre de machine critique est plus faible
    :param n: Le nombre de tâches
    :param m: Le nombre de machines
    :param t_i: La liste des durées d'execution de chaque tâche
    :param af1: L'affectation de départ
    :param af2: La nouvelle affectation
    :return: Le makespan et le temps
    """
    def _cout(n: int, m: int, af):
        ms = makespan(t_i, af)
        crit = 0
        for taches in af.values():
            c = 0
            for i in taches:
                c += t_i[i]
            
            if not(c < ms):
                crit += 1
        
        return ms, crit

    ms1, crit1 = _cout(n, m, af1)
    ms2, crit2 = _cout(n, m, af2)
    
    return ms1 > ms2 or (ms1 == ms2 and crit1 > crit2)

def pair(n: int, m: int, t_i: List[int], af1, af2, mi, mj):
    """
    Renvoie vrai la plus grande des deux charges impliquées a strictement diminué
    :param n: Le nombre de tâches
    :param m: Le nombre de machines
    :param t_i: La liste des durées d'execution de chaque tâche
    :param af1: L'affectation de départ
    :param af2: La nouvelle affectation
    :return: Le makespan et le temps
    """
    return max(sum([t_i[i] for i in af1[mi]]), sum([t_i[i] for i in af1[mj]])) > max(sum([t_i[i] for i in af2[mi]]), sum([t_i[i] for i in af2[mj]]))
    

def recherche_locale(n: int, m: int, t_i: List[int], vo, cr):
    def _sub_lists(l):
        lists = [[]]
        for i in range(len(l) + 1):
            for j in range(i):
                lists.append(l[j: i])
        return lists
    
    if cr == "cmax":
        c_func = lambda n, m, t_i, af1, af2, mi = None, mj = None : makespan(t_i, af1) > makespan(t_i, af2)
    elif cr == "lexico":
        c_func = lexico
    elif cr == "pair":
        c_func = pair

    start_af = defaultdict(list)
    for i in range(n):
        start_af[int(random.random()*m)].append(i)
    
    def _recherche_locale(af):
        perm_mi = list(range(m))
        # random.shuffle(perm_mi)
        perm_mj = list(range(m))
        # random.shuffle(perm_mj)
        for mi in perm_mi:
            perm_t = copy(af[mi])
            # random.shuffle(perm_t)
            for mj in perm_mj:
                perm_tj = copy(af[mj])
                # random.shuffle(perm_tj)
                if mi != mj:
                    if vo == "insertion" or vo == "echange":
                        for t in perm_t:
                            if vo == "insertion":
                                new_af = insertion(m, af, mi, mj, t)
                                if c_func(n, m, t_i, af, new_af, mi, mj):
                                    return _recherche_locale(new_af) # Ameliorant
                            else:
                                for tj in perm_tj:
                                    new_af = echange(m, af, mi, mj, t, tj)
                                    if c_func(n, m, t_i, af, new_af, mi, mj):
                                        return _recherche_locale(new_af) # Ameliorant
                    elif vo == "permutation":
                        subsets_mi = _sub_lists(af[mi])
                        subsets_mj = _sub_lists(af[mj])
                        # random.shuffle(subsets_mi)
                        # random.shuffle(subsets_mj)
                        for bi in subsets_mi:
                            for bj in subsets_mj:
                                new_af = permutation(m, af, mi, mj, bi, bj)
                                if c_func(n, m, t_i, af, new_af, mi, mj):
                                    return _recherche_locale(new_af) # Ameliorant
        return af # Stable
    return _recherche_locale(start_af)