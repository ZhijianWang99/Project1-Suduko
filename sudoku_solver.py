## reference https://gist.github.com/allisonmorgan/c2f831cb01532fe51834f471634f4d58

import pandas as pd
import numpy as np
from itertools import chain
import pulp


def sudoku_constraint(input_quiz):
    current_var = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    vals = current_var
    rows = current_var
    cols = current_var

    boxes = list()
    for i in range(3):
        for j in range(3):
            innerElement = list()
            for k in range(3):
                for l in range(3):
                    innerElement.append((rows[3 * i + k], cols[3 * j + l]))
            boxes.append(innerElement)

    prob = pulp.LpProblem("Sudoku", pulp.LpMaximize)
    choices = pulp.LpVariable.dict("Choices", (rows, cols, vals), lowBound=0, upBound=1, cat=pulp.LpInteger)

    prob += 0, "My function"

    # Grit constraint
    for r in rows:
        for c in cols:
            prob += pulp.lpSum([choices[r, c, v] for v in vals]) == 1, ""
    # Column constraint
    for v in vals:
        for r in rows:
            prob += pulp.lpSum([choices[r, c, v] for c in cols]) == 1, ""
    # Row constraint
    for v in vals:
        for c in cols:
            prob += pulp.lpSum([choices[r, c, v] for r in rows]) == 1, ""
    # Box constraint
    for v in vals:
        for b in boxes:
            prob += pulp.lpSum([choices[r, c, v] for (r, c) in b]) == 1, ""
    # constant point
    for index, element in enumerate(input_quiz):
        col = index % 9 + 1
        row = index // 9 + 1
        if int(element) != 0:
            prob += choices[row, col, int(element)] == 1, ""

    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    my_solution = str()
    for r in rows:
        for c in cols:
            for v in vals:
                if pulp.value(choices[r, c, v]) == 1:
                    my_solution += str(v)
    return my_solution


def small_data(route):
    df = pd.read_csv(route)
    quizzes = df.loc[:, ["quizzes"]]
    solutions = df.loc[:, ["solutions"]]
    quiz_list = quizzes.values.tolist()
    quiz_list = list(chain.from_iterable(quiz_list))
    solutions_list = solutions.values.tolist()
    solutions_list = np.array(list(chain.from_iterable(solutions_list)))
    my_solution = np.array([sudoku_constraint(e) for e in quiz_list])
    return sum(solutions_list == my_solution), len(quiz_list)


def large_data(route, my_seed=42):
    df = pd.read_csv(route)
    df = df.sample(n=1000, random_state=my_seed)
    quizzes = df.loc[:, ["quizzes"]]
    solutions = df.loc[:, ["solutions"]]
    quiz_list = quizzes.values.tolist()
    quiz_list = list(chain.from_iterable(quiz_list))
    solutions_list = solutions.values.tolist()
    solutions_list = np.array(list(chain.from_iterable(solutions_list)))
    my_solution = np.array([sudoku_constraint(e) for e in quiz_list])
    return sum(solutions_list == my_solution), len(quiz_list)


if __name__ == '__main__':
    print("Small Data Result")
    print("  Small Data1 Result:")
    correct1, total1 = small_data(r"data/small1.csv")
    p = correct1 / total1
    print(f"  Total: {correct1}, Correct: {total1}, Correct_Percentage: {p}")
    print("  Small Data2 Result:")
    correct2, total2 = small_data(r"data/small2.csv")
    p = correct2 / total2
    print(f"  Total: {correct2}, Correct: {total2}, Correct_Percentage: {p}")
    print("  All Small Data Result:")
    correct = correct1 + correct2
    total = total1 + total2
    p = correct / total
    print(f"  Total: {correct}, Correct: {total}, Correct_Percentage: {p}")
    print("Large Data Result")
    print("  Large Data1 Result:")
    correct1, total1 = large_data(r"data/large1.csv")
    p = correct1 / total1
    print(f"  Total: {correct1}, Correct: {total1}, Correct_Percentage: {p}")
    print("  Large Data2 Result")
    correct2, total2 = large_data(r"data/large2.csv")
    p = correct2 / total2
    print(f"  Total: {correct2}, Correct: {total2}, Correct_Percentage: {p}")
    print("  All large Data Result:")
    correct = correct1 + correct2
    total = total1 + total2
    p = correct / total
    print(f"  Total: {correct}, Correct: {total}, Correct_Percentage: {p}")
