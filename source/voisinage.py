import random
import copy

def insertion(m: int, af: dict) -> dict:
    """
    Déplace une tâche de la machine i de af à une autre machine j
    :param m: Le nombre de machines
    :param af: Une affectation des tâches
    :return: Une affectation des tâches
    """
    af_res = copy.deepcopy(af)
    i = random.randrange(m)
    j = random.randrange(m)
    listi_t = af_res[i]
    while( i == j ) or ( listi_t == [] ):
        i = random.randrange(m)
        j = random.randrange(m)
        listi_t = af_res[i]
    t = random.randrange(len(listi_t))
    af_res[j].append(listi_t[t])
    del af_res[i][t]

    return af_res

def echange(m: int, af: dict) -> dict:
    """
    Echange une tâche de la machine i avec une tâche de la machine j
    :param m: Le nombre de machine
    :param af: Une affectation des tâches
    :return: Une affectation des tâches
    """
    af_res = copy.deepcopy(af)
    i = random.randrange(m)
    j = random.randrange(m)
    listi_t = af_res[i]
    listj_t = af_res[j]
    while( i == j ) or ( listi_t == [] ) or ( listj_t == [] ):
        i = random.randrange(m)
        j = random.randrange(m)
        listi_t = af_res[i]
        listj_t = af_res[j]
    ti = random.randrange(len(listi_t))
    tj = random.randrange(len(listj_t))
    af_res[j].append(listi_t[ti])
    af_res[i].append(listj_t[tj])
    del af_res[i][ti]
    del af_res[j][tj]

    return af_res

def permutation(m: int, af: dict) -> dict:
    """
    Permute un ensemble de tâches de la machine i avec un ensemble de tâches de la machine j
    :param m: Le nombre de machine
    :param af: Une affectation des tâches
    :return: Une affectation des tâches
    """
    af_res = copy.deepcopy(af)
    i = random.randrange(m)
    j = random.randrange(m)
    listi_t = af_res[i]
    listj_t = af_res[j]
    while( i == j ) or ( listi_t == [] and listj_t == [] ):
        i = random.randrange(m)
        j = random.randrange(m)
        listi_t = af_res[i]
        listj_t = af_res[j]
    #proba de 0,5 d'affecter une tâche
    bi = []
    bj = []
    for ind, ti in enumerate(listi_t):
        if random.random() < 0.5 :
            bi.append(ti)
            del af_res[i][ind]
    for ind, tj in enumerate(listj_t):
        if random.random() < 0.5 :
            bj.append(tj)
            del af_res[j][ind]
    af_res[j] += bi
    af_res[i] += bj

    return af_res

def main():
    s={0:[6,7],1:[2,4],2:[],3:[3,1]}
    print(permutation(4,s))

    return 0

if __name__ == "__main__":
    main()