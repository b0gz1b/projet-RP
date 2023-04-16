from typing import List
from collections import defaultdict
import random, heapq, time
import numpy as np

def measure(n: int, m: int, t_i: List[int], algo):
    """
    Renvoie le makespan et le temps d'éxecution d'un algo d'équilibrage des charges
    :param n: Le nombre de tâches
    :param m: Le nombre de machines
    :param t_i: La liste des durées d'execution de chaque tâche
    :param algo: La fonction dont on mesure la performance
    :return: Le makespan et le temps
    """
    start = time.time()
    af = algo(n, m, t_i)
    end = time.time()

    return makespan(t_i, af), end - start

def rand_instance(n: int, lower: int = 1, higher: int = 100) -> List[int]:
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
