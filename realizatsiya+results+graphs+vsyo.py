import os
import time
import matplotlib.pyplot as plt
import csv

def compute_pi(pattern):
    pi = [0] * len(pattern)
    k = 0
    iterations = 0

    for i in range(1, len(pattern)):
        while k > 0 and pattern[k] != pattern[i]:
            k = pi[k - 1]
            iterations += 1
        if pattern[k] == pattern[i]:
            k += 1
        pi[i] = k
        iterations += 1

    return pi, iterations


def kmp_search(text, pattern):
    if not pattern:
        return -1, 0, 0.0

    pi, prep_iter = compute_pi(pattern)
    k = 0
    search_iter = 0

    start_time = time.perf_counter()

    for i in range(len(text)):
        while k > 0 and pattern[k] != text[i]:
            k = pi[k - 1]
            search_iter += 1

        if pattern[k] == text[i]:
            k += 1
        search_iter += 1

        if k == len(pattern):
            end_time = time.perf_counter()
            total_time = (end_time - start_time) * 1000  # мс
            return i - k + 1, prep_iter + search_iter, total_time

    end_time = time.perf_counter()
    total_time = (end_time - start_time) * 1000  # мс
    return -1, prep_iter + search_iter, total_time


def process_datasets():
    results = []

    if not os.path.exists('results'):
        os.makedirs('results')

    for i in range(1, 51):
        text_file = f'vhodnie/text{i}.txt'
        pattern_file = f'vhodnie/pattern{i}.txt'

        if not os.path.exists(text_file) or not os.path.exists(pattern_file):
            print(f"⚠️ Файлы для набора {i} не найдены!")
            continue

        with open(text_file, 'r') as f:
            text = f.read().strip()
        with open(pattern_file, 'r') as f:
            pattern = f.read().strip()

        position, iterations, time_ms = kmp_search(text, pattern)

        results.append({
            'dataset': i,
            'text_len': len(text),
            'pattern_len': len(pattern),
            'position': position,
            'iterations': iterations,
            'time_ms': time_ms
        })

        print(f"Набор {i}: текст={len(text)} симв., паттерн={len(pattern)} симв. → "
              f"Позиция: {position}, Итераций: {iterations}, Время: {time_ms:.4f} мс")

    with open('results/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['dataset', 'text_len', 'pattern_len', 'position', 'iterations', 'time_ms']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    return results

def plot_results(results):
    sizes = [r['text_len'] + r['pattern_len'] for r in results]
    times = [r['time_ms'] for r in results]
    iterations = [r['iterations'] for r in results]

    plt.figure(figsize=(12, 6))
    plt.scatter(sizes, times, c='blue', alpha=0.7)
    plt.title('Зависимость времени выполнения от суммарного размера данных')
    plt.xlabel('Суммарный размер данных (text_len + pattern_len)')
    plt.ylabel('Время выполнения (мс)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig('results/time_vs_size.png')

    plt.figure(figsize=(12, 6))
    plt.scatter(sizes, iterations, c='red', alpha=0.7)
    plt.title('Зависимость количества итераций от суммарного размера данных')
    plt.xlabel('Суммарный размер данных (text_len + pattern_len)')
    plt.ylabel('Количество итераций сравнений')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig('results/iterations_vs_size.png')

    plt.figure(figsize=(12, 6))
    plt.scatter(iterations, times, c='green', alpha=0.7)
    plt.title('Зависимость времени выполнения от количества итераций')
    plt.xlabel('Количество итераций сравнений')
    plt.ylabel('Время выполнения (мс)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig('results/time_vs_iterations.png')


results = process_datasets()
plot_results(results)