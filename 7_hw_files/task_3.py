def writing_to_file(*args):
    dict_files = {}
    for file in args:
        with open(file, 'r') as f:
            dict_files[file] = len(f.readlines())
    sort_dict = sorted(dict_files.items(), key=lambda x: x[1])
    dict_files = dict(sort_dict)

    for name, count in dict_files.items():
        with open('result.txt', 'a') as result_file:
            result_file.write(f'{name}\n')
            result_file.write(f'{str(count)}\n')
            with open(name, 'r') as f:
                for line in f:
                    result_file.write(line)
                result_file.write('\n')


writing_to_file('1.txt', '2.txt', '3.txt')