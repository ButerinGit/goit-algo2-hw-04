from collections import deque, defaultdict
from typing import Dict, List, Tuple


class EdmondsKarp:
    def __init__(self):
        # cap[u][v] = залишкова пропускна здатність ребра u -> v
        self.cap: Dict[str, Dict[str, int]] = defaultdict(dict)
        # список початкових орієнтованих ребер (u, v)
        self.edges: List[Tuple[str, str]] = []
        # список всіх сусідів (для обходу в ширину)
        self.graph: Dict[str, set] = defaultdict(set)

    def add_edge(self, u: str, v: str, c: int) -> None:
        """Додає орієнтоване ребро u -> v з ємністю c."""
        self.edges.append((u, v))
        self.cap[u][v] = self.cap[u].get(v, 0) + c  # якщо декілька ребер — сумуємо
        self.cap[v].setdefault(u, 0)                # зворотну ємність 0
        self.graph[u].add(v)
        self.graph[v].add(u)

    def max_flow(self, s: str, t: str) -> int:
        """Повертає значення максимального потоку між s та t."""
        flow = 0
        while True:
            parent = {s: None}
            q = deque([s])

            # пошук шляху збільшення потоку (BFS)
            while q and t not in parent:
                u = q.popleft()
                for v in self.graph[u]:
                    if self.cap[u][v] > 0 and v not in parent:
                        parent[v] = u
                        q.append(v)

            if t not in parent:
                # шляху більше немає — потік максимальний
                break

            # знаходимо "вузьке місце" на шляху
            bottleneck = float("inf")
            v = t
            while v != s:
                u = parent[v]
                bottleneck = min(bottleneck, self.cap[u][v])
                v = u

            # пропускаємо потік по цьому шляху
            v = t
            while v != s:
                u = parent[v]
                self.cap[u][v] -= bottleneck
                self.cap[v][u] += bottleneck
                v = u

            flow += bottleneck

        return flow

    def get_flows(self) -> List[Tuple[str, str, int]]:
        """Повертає фактичні потоки по початкових ребрах (u, v, flow)."""
        flows: List[Tuple[str, str, int]] = []
        for u, v in self.edges:
            f = self.cap[v][u]  # скільки накопичилось у зворотній ємності
            flows.append((u, v, f))
        return flows


def build_logistic_network() -> Tuple[EdmondsKarp, str, str]:
    """Створює граф для задачі з логістичною мережею."""
    ek = EdmondsKarp()

    S, T = "S", "T"
    # умовні імена вузлів
    t1, t2 = "T1", "T2"
    w1, w2, w3, w4 = "W1", "W2", "W3", "W4"

    shops = [f"Shop{i}" for i in range(1, 15)]

    # S -> термінали (обмеження на загальний потік через кожен термінал)
    ek.add_edge(S, t1, 25 + 20 + 15)  # 60
    ek.add_edge(S, t2, 15 + 30 + 10)  # 55

    # Термінал -> Склад
    edges_tw = [
        (t1, w1, 25),
        (t1, w2, 20),
        (t1, w3, 15),
        (t2, w3, 15),
        (t2, w4, 30),
        (t2, w2, 10),
    ]
    for u, v, c in edges_tw:
        ek.add_edge(u, v, c)

    # Склад -> Магазин
    edges_ws = [
        (w1, "Shop1", 15),
        (w1, "Shop2", 10),
        (w1, "Shop3", 20),
        (w2, "Shop4", 15),
        (w2, "Shop5", 10),
        (w2, "Shop6", 25),
        (w3, "Shop7", 20),
        (w3, "Shop8", 15),
        (w3, "Shop9", 10),
        (w4, "Shop10", 20),
        (w4, "Shop11", 10),
        (w4, "Shop12", 15),
        (w4, "Shop13", 5),
        (w4, "Shop14", 10),
    ]
    for u, v, c in edges_ws:
        ek.add_edge(u, v, c)

    # Магазин -> T (щоб товар не заходив у магазин більше ємності ребра зі складу)
    capacities = {
        1: 15, 2: 10, 3: 20,
        4: 15, 5: 10, 6: 25,
        7: 20, 8: 15, 9: 10,
        10: 20, 11: 10, 12: 15, 13: 5, 14: 10,
    }
    for i, shop in enumerate(shops, start=1):
        ek.add_edge(shop, T, capacities[i])

    return ek, S, T


def distribute_terminal_to_shop(flows: List[Tuple[str, str, int]]):
    """
    Розкладає потоки від терміналів до магазинів через склади.
    Повертає словник: (terminal, shop) -> flow.
    """
    term_to_wh = defaultdict(lambda: defaultdict(int))
    wh_to_shop = defaultdict(lambda: defaultdict(int))

    # збираємо потоки Термінал -> Склад та Склад -> Магазин
    for u, v, f in flows:
        if f == 0:
            continue
        if u.startswith("T") and v.startswith("W"):
            term_to_wh[u][v] += f
        if u.startswith("W") and v.startswith("Shop"):
            wh_to_shop[u][v] += f

    result = defaultdict(float)

    for wh, shops_dict in wh_to_shop.items():
        # сумарний вхід у склад з терміналів
        incoming = {t: term_to_wh[t][wh] for t in term_to_wh if wh in term_to_wh[t]}
        total_incoming = sum(incoming.values())
        if total_incoming == 0:
            continue

        # для кожного магазину, що живиться зі складу, розподіляємо потік пропорційно
        for shop, flow_wh_shop in shops_dict.items():
            for t, inc in incoming.items():
                share = flow_wh_shop * inc / total_incoming
                result[(t, shop)] += share

    return result


def main():
    ek, S, T = build_logistic_network()

    max_flow = ek.max_flow(S, T)
    print(f"Максимальний потік: {max_flow} одиниць\n")

    flows = ek.get_flows()

    print("Потік від терміналів до складів:")
    for u, v, f in flows:
        if u.startswith("T") and v.startswith("W") and f > 0:
            print(f"  {u} -> {v}: {f}")

    print("\nПотік від складів до магазинів:")
    for u, v, f in flows:
        if u.startswith("W") and v.startswith("Shop") and f > 0:
            print(f"  {u} -> {v}: {f}")

    # таблиця Термінал–Магазин
    term_shop = distribute_terminal_to_shop(flows)

    print("\nТаблиця потоків (Термінал–Магазин):")
    print(f"{'Термінал':<10} {'Магазин':<10} {'Потік':>10}")
    for (t, shop), f in sorted(term_shop.items()):
        print(f"{t:<10} {shop:<10} {f:10.2f}")


if __name__ == "__main__":
    main()