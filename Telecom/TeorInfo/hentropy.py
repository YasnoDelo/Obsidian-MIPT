import math
import matplotlib.pyplot as plt

def calculate_entropy(probabilities):
    return -sum(p * math.log2(p) for p in probabilities if p > 0)

def run_check(probabilities):
    entropy = calculate_entropy(probabilities)
    return entropy

def quadratic_norm_list(lst):
    return math.sqrt(sum((x-1/len(lst))**2 for x in lst))

def generate_distributions(step, count):
    distr = []
    def helper(current, remaining, depth):
        if depth == count - 1:
            p_last = round(remaining, 10)
            if 0 <= p_last <= 1:
                distr.append(current + [p_last])
            return
        p = 0
        while p <= remaining:
            p_rounded = round(p, 10)
            helper(current + [p_rounded], round(remaining - p, 10), depth + 1)
            p += step

    helper([], 1, 0)
    print(f"Ready for step = {step}, count = {count}. amount or vars = {len(distr)}")
    return distr

def count_for_one(distributions):
    difference = []
    for count in range(len(distributions)):
        difference.append(quadratic_norm_list(distributions[count]))

    entropy_arr = []
    for dist in distributions:
        entropy_arr.append(run_check(dist))
    return difference, entropy_arr

def count_for_all(distr_arr):
    diff = []
    entr = []
    for i in range(len(distr_arr)):
        print("3")
        diff_one, entr_one = count_for_one(distr_arr[i])
        diff.append(diff_one)
        entr.append(entr_one)
    return diff, entr


if __name__ == "__main__":
    start_am_of_symb = 2
    end_am_of_symb = 6
    entropy_arr = []
    differences_arr = []
    distr_arr = []
    for i in range(start_am_of_symb, end_am_of_symb):
        if i != 0:  
            distr_arr.append(generate_distributions(0.02, i))

    differences_arr, entropy_arr = count_for_all(distr_arr)

    plt.ylabel("Энтропия", fontsize=18)
    plt.xlabel("Отклонение вероятностей от равномерной", fontsize=18)
    plt.title('График зависимости энтропии от отклонения вероятностей от равномерной', fontsize=20)

    counter = start_am_of_symb
    for difference, entropy in zip(differences_arr, entropy_arr):
        plt.plot(difference, entropy, label=f"Распределение для количества символов = {counter}")
        counter += 1

    plt.legend()
    plt.grid(True)

    plt.show()

