import math
import collections
from heapq import heapify
from colorama import init, Fore, Back, Style

init(autoreset=True)  # автоматический сброс цвета после каждого вывода

class TreeNode:
    def __init__(self, weight, children=None, symbols_codes=None):
        self.weight = weight
        self.children = children if children else []
        self.symbols_codes = symbols_codes if symbols_codes else []

def calculate_entropy(probabilities):
    return -sum(p * math.log2(p) for p in probabilities if p > 0)

def print_tree(node, prefix="", is_left=True):
    if not node:
        return
    connector = "└── " if is_left else "┌── "
    print(prefix + connector + f"Вес: {node.weight}")
    if node.children:
        for i, child in enumerate(node.children):
            is_last = (i == len(node.children) - 1)
            new_prefix = prefix + ("    " if is_left else "│   ")
            print_tree(child, new_prefix, is_left=is_last)

def huffman_code_lengths(probabilities):
    heap = [[weight, [symbol, ""]] for symbol, weight in enumerate(probabilities)]
    heapify(heap)
    print(Fore.BLUE + "Построение дерева")
    co = 0
    nodes = [TreeNode(item[0], symbols_codes=item[1:]) for item in heap]
    while len(nodes) > 1:
        nodes = sorted(nodes, key=lambda x: x.weight)
        lo = nodes.pop(0)
        hi = nodes.pop(0)

        for pair in lo.symbols_codes:
            pair[1] = '0' + pair[1]
        for pair in hi.symbols_codes:
            pair[1] = '1' + pair[1]

        combined_weight = lo.weight + hi.weight
        combined_codes = lo.symbols_codes + hi.symbols_codes
        new_node = TreeNode(combined_weight, children=[lo, hi], symbols_codes=combined_codes)
        nodes.append(new_node)
        co += 1

    print("\nИтоговое дерево:")
    print_tree(new_node)
    code_lengths = [0]*len(probabilities)
    for p in heap:
        symbol = p[1][0]
        length = len(p[1][1])
        code_lengths[symbol] = length
    return code_lengths

def average_code_length(probabilities, code_lengths):
    return sum(p * l for p, l in zip(probabilities, code_lengths))

def run_check(probabilities):

    print(Fore.GREEN + f"Probabilities: {probabilities}")
    entropy = calculate_entropy(probabilities)
    print(Fore.GREEN + f"Entropy (H): {entropy:.4f} bits")

    code_lengths = huffman_code_lengths(probabilities)
    print(Style.BRIGHT + f"Code lengths: {code_lengths}")

    avg_len = average_code_length(probabilities, code_lengths)
    print(Style.BRIGHT + f"Average code length: {avg_len:.4f} bits")

    print(Style.BRIGHT + f"Redundancy (Average length - Entropy): {avg_len - entropy:.4f} bits\n")

if __name__ == "__main__":
    # Примеры распределений
    print("Посчитаем энтропию для различных кодировок методом Хаффмана")
    distributions = [
        [0.5, 0.5],            # равновероятные символы
        [0.6, 0.4],            # сильно скошенное распределение
        [0.7, 0.3],            # сильно скошенное распределение
        [0.8, 0.2],            # сильно скошенное распределение
        [0.9, 0.1],            # сильно скошенное распределение
        [0.7, 0.2, 0.1],       # 3 символа, неравновероятные
        [0.4, 0.3, 0.2, 0.1],  # 4 символа
    ]
    for dist in distributions:
        run_check(dist)
