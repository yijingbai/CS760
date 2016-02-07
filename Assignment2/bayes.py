"""The sys module."""
import sys
import re


def tan(train_file, test_file):
    """Tan."""
    return 0


def naive_bayes(train_file, test_file):
    """naive_bayes."""
    attribute_list = []
    value_list = []
    dataset = []
    is_data_line = False
    P = {}

    with open(train_file) as train:
        for line in train:
            if is_data_line:
                data = line.strip().split(',')
                dataset.append(data)

            result = re.search("@attribute\s+\'(.+)\'\s+{\s+(.+)\s*}", line)
            if result:
                attribute_list.append(result.group(1))
                values = map(lambda v: v.strip(),
                             result.group(2).strip().split(','))
                value_list.append(values)
            elif re.search("@data", line):
                print(attribute_list)
                is_data_line = True

    # estimate P(Y = y)
    class_index = len(attribute_list) - 1
    counts = {}
    for v in value_list[class_index]:
        counts[v] = 0
    for data in dataset:
        for v in value_list[class_index]:
            if (data[class_index] == v):
                counts[v] += 1

    total_data = len(dataset)
    for (v, count) in counts.items():
        P[v] = float(count) / total_data
    # print counts
    # print P

    condP = {}

    # estimate P(Xi = x | Y = y) for each Xi
    # for i in range(0, class_index):
    #     attr = attribute_list[i]
    #     if attr not in condP:
    #         condP[attr] = {}
    #
    #     for value in value_list[i]:
    #         if attr not in condP[attr]:
    #             condP[attr][value] = {}
    #         y_count = 0
    #         attr_count = 0
    #         for y in value_list[class_index]:
    #             for data in dataset:
    #                 if data[class_index] == y:
    #                     y_count += 1
    #                 if data[class_index] == y and data[i] == value:
    #                     attr_count += 1
    #             condP[attr][value][y] = float(attr_count) / y_count
    #             y_count = 0
    #             attr_count = 0

    # estimate functon two

    # print condP

    # classification
    is_data_line = False
    with open(test_file) as test:
        for line in test:
            if is_data_line:
                data = line.strip().split(',')
                max_possbility = 0.0

                num = P[y]
                dom = 0.0
                predict = ""
                for y in value_list[class_index]:
                    for (i, attr) in enumerate(attribute_list):
                        if i != class_index:
                            num *= condP[attr][data[i]][y]

                    if num > max_possbility:
                        max_possbility = num
                        predict = y

                    dom += num
                    num = P[y]

                prob = max_possbility / dom
                print(predict + " " + data[class_index] + str(prob))

            if re.search("@data", line):
                is_data_line = True

    return 0


if __name__ == "__main__":
    arg_len = len(sys.argv)
    if arg_len > 4 or arg_len < 4:
        print("wrong argument")
        sys.exit(0)

    train_file = sys.argv[1]
    test_file = sys.argv[2]
    mode = sys.argv[3]

    print("train_file is " + train_file)
    print("test_file is " + test_file)
    print("mode is " + mode)

    if mode == 'n':
        naive_bayes(train_file, test_file)
    elif mode == 't':
        tan(train_file, test_file)
