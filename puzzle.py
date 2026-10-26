import heapq

initial_state = (1, 2, 3, 8, 0, 4, 7, 6, 5)

def est_solvable(etat, but):
    rang = {v: i for i, v in enumerate([v for v in but if v != 0])}
    suite = [rang[v] for v in etat if v != 0]
    inversions = 0
    for a in range(len(suite)):
        for b in range(a + 1, len(suite)):
            if suite[a] > suite[b]:
                inversions += 1
    return inversions % 2 == 0

"""somme de distance de chaque jeton à sa place cible (Manhattan)"""
def manhattan(etat, but):
    pos_but = {v: i for i, v in enumerate(but)}
    total = 0
    for i, v in enumerate(etat):
        if v != 0:
            j = pos_but[v]
            total += abs(i // 3 - j // 3) + abs(i % 3 - j // 3)
    return total

def voisins(etat):
    i = etat.index(0)
    """la case vide"""
    l, c = divmod(i, 3)
    resultat = []
    for cl, cc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nl, nc = l + cl, c + cc
        if 0 <= nl < 3 and 0 <= nc < 3:
            j = nl * 3 + nc
            s = list(etat)
            s[i], s[j] = s[j], s[i]
            resultat.append(tuple(s))
    return resultat

def A_star(depart, but):
    etapes = []
    compteur = 0
    file = [(manhattan(depart, but), 0, compteur, depart)]
    parent = {depart: None}
    milleur_g = {depart: 0}
    explores = set()

    while file:
        f, g, _, etat = heapq.heappop(file)
        if etat in explores:
            continue
        explores.add(etat)
        etapes.append((etat, g, f - g, f))

        if etat == but:
            chemin = []
            while etat is not None:
                chemin.append(etat)
                etat = parent[etat]
            return chemin[::-1], etapes

        for v in voisins(etat):
            ng = g + 1
            if v not in milleur_g or ng < milleur_g[v]:
                milleur_g[v] = ng
                parent[v] = etat
                compteur += 1
                heapq.heappush(file, (ng + manhattan(v, but), ng, compteur, v))
    return None, etapes