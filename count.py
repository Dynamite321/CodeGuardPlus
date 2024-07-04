import os

def count_lang():
    num_py = 0
    num_c = 0
    c_cwe_list = []
    for cwe in os.listdir('prompts'):
        if not cwe.startswith('cwe-'):
            continue
        for scenario in os.listdir('prompts/' + cwe):
            if scenario.startswith('.DS_Store'):
                continue
            if scenario.endswith('-py'):
                num_py += 1
            elif scenario.endswith('-c'):
                num_c += 1
                c_cwe_list.append(cwe)
    c_cwe_list = list(set(c_cwe_list))
    print('Python:', num_py)
    print('C:', num_c)
    print('CWEs with C:', sorted(c_cwe_list))

count_lang()