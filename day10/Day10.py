import numpy as np

array = []
row_index = 0
total_syntax_error_score = 0
all_auto_complete_scores = np.array([]).astype(int)

with open('input.txt') as file:
    for line in file:
        current_list = list(line.strip())

        # remove valid chunks
        while (len(current_list)) > 1:
            len_previous_run = len(current_list)
            for index, char in enumerate(current_list[:-1]):
                open_par = current_list[index]
                close_par = current_list[index + 1]
                if (open_par == '(' and close_par == ')') or (
                        open_par == '[' and close_par == ']') or (
                        open_par == '{' and close_par == '}') or (
                        open_par == '<' and close_par == '>'):
                    current_list.pop(index + 1)
                    current_list.pop(index)
                    break
            if len_previous_run == len(current_list):
                break

        # find closing chunk in list; the first one is the syntax error, so break
        current_syntax_error_score = 0

        for char in current_list:
            if char == ')':
                current_syntax_error_score += 3
                break
            if char == ']':
                current_syntax_error_score += 57
                break
            if char == '}':
                current_syntax_error_score += 1197
                break
            if char == '>':
                current_syntax_error_score += 25137
                break

        if current_syntax_error_score > 0:
            total_syntax_error_score += current_syntax_error_score
        else:
            # if there were no syntax errors, we have an incomplete list
            # flip the list to get the right order (last one closed first)
            current_auto_complete_score = 0
            for char in current_list[::-1]:
                current_auto_complete_score = current_auto_complete_score * 5
                if char == '(':
                    current_auto_complete_score += 1
                if char == '[':
                    current_auto_complete_score += 2
                if char == '{':
                    current_auto_complete_score += 3
                if char == '<':
                    current_auto_complete_score += 4
            all_auto_complete_scores = np.append(all_auto_complete_scores, current_auto_complete_score).astype(int)

sorted_auto_complete_scores = np.sort(all_auto_complete_scores)

print(f'answer 1: {total_syntax_error_score}')
print(f'answer 2: {sorted_auto_complete_scores[int(np.floor(len(sorted_auto_complete_scores) / 2))]}')
