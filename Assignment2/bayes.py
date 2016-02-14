"""The sys module."""
import sys
import re
from decimal import Decimal
import math
import operator

def parse_file(input_file):
    attribute_list = []
    value_list = []
    dataset = []
    is_data_line = False
    with open(input_file) as train:
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
                is_data_line = True
    return (attribute_list, value_list, dataset)


def tan(train_file, test_file):
    """Tan."""
    attribute_list, value_list, dataset = parse_file(train_file)
    y_index = len(attribute_list) - 1
    data_size = len(dataset)

    def join_p(i, j, x_i, x_j, y):
        sum_num = sum([1 for data in dataset if data[i] == x_i and data[j] == x_j and data[y_index] == y])
        res = float(sum_num + 1) / (data_size + (len(value_list[i]) * len(value_list[j]) * len(value_list[y_index])))
        return res

    def cond_p(i, x_i, y):
        sum_num = sum([1 for data in dataset if data[i] == x_i and data[y_index] == y])
        res = float(sum_num + 1) / (sum([1 for data in dataset if data[y_index] == y]) + len(value_list[i]))
        return res

    def join_cond_p(i, j, x_i, x_j, y):
        sum_num = sum([1 for data in dataset if data[i] == x_i and data[j] == x_j and data[y_index] == y])
        res = float(sum_num + 1) / (sum([1 for data in dataset if data[y_index] == y]) + len(value_list[i]) * len(value_list[j]))
        return res

    def compute_single_mutual_info(attr_i, attr_j, attr_y):
        res = 0
        for v_i in value_list[attr_i]:
            for v_j in value_list[attr_j]:
                for v_y in value_list[attr_y]:
                    res += join_p(attr_i, attr_j, v_i, v_j, v_y) * math.log(join_cond_p(attr_i, attr_j, v_i, v_j, v_y) / (cond_p(attr_i, v_i, v_y) * cond_p(attr_j, v_j, v_y)), 2)
        return res

    edges = [[-1.0 for col in range(0, len(attribute_list) - 1)] for row in range(0, len(attribute_list) - 1)]

    def compute_all_mutual_info():
        for (i, attr_row) in enumerate(attribute_list):
            for (j, attr_col) in enumerate(attribute_list):
                if i == j or i == y_index or j == y_index:
                    continue
                edges[i][j] = compute_single_mutual_info(i, j, y_index)

    compute_all_mutual_info()

    vertices = [i for i in range(0, len(attribute_list) - 1)]

    def prim():
        v_new = [0]
        edges_new = {}
        while True:
            info, v_1, v_2 = max([(edges[v_1][v_2], v_1, v_2) for v_1 in v_new for v_2 in range(0, len(attribute_list) - 1) if v_2 not in v_new])
            v_new.append(v_2)
            edges_new[v_2] = [v_1]
            if len(v_new) == len(vertices):
                break
        return (v_new, edges_new)

    v_new, edges_new = prim()
    for k in range(0, len(attribute_list) - 1):
        if k not in edges_new:
            edges_new[k] = []
        edges_new[k].append(y_index)

    for i in xrange(0, len(attribute_list) - 1):
        print(attribute_list[i] + " " + " ".join([attribute_list[j] for j in edges_new[i]]))

    print("")

    def compute_multi_cond_p(i, attr, parents, p_values):
        sum_num = sum([1 for data in dataset if data[i] == attr and reduce(operator.__and__, [True if data[p_i] == p_values[attr_i] else False for (attr_i, p_i) in enumerate(parents)])])
        res = float(sum_num + 1) / (sum([1 for data in dataset if reduce(operator.__and__, [True if data[p_i] == p_values[attr_i] else False for (attr_i, p_i) in enumerate(parents)])]) + len(test_value_list[i]))
        return res

    def calculate_p():
        count_dict = {}
        count = 0
        for data in dataset:
            count += 1
            if data[y_index] not in count_dict:
                count_dict[data[y_index]] = 1
            else:
                count_dict[data[y_index]] += 1
        P = {}
        for (value, c) in count_dict.items():
            P[value] = float(c + 1) / (count + len(value_list[y_index]))
        return P

    P = calculate_p()

    right_count = 0
    test_attribute_list, test_value_list, test_dataset = parse_file(test_file)
    for test_data in test_dataset:
        # print(test_data)
        p_sum = 0
        max_p = 0
        res_class = ""
        for y_value in value_list[y_index]:
            num = P[y_value]
            for i in edges_new.keys():
                p_values = []
                for p in edges_new[i]:
                    if (p == y_index):
                        p_values.append(y_value)
                    else:
                        p_values.append(test_data[p])
                multi_cond_p = compute_multi_cond_p(i, test_data[i], edges_new[i], p_values)
                num *= multi_cond_p
            if num > max_p:
                max_p = num
                res_class = y_value
            p_sum += num
        predict_p = float(max_p) / p_sum
        if res_class == test_data[y_index]:
            right_count += 1
        print("%s %s %.12g" % (res_class, test_data[y_index], predict_p))

    print("")
    print(right_count)
    print("")
    return 0


def naive_bayes(train_file, test_file):
    """naive_bayes."""
    P = {}

    attribute_list, value_list, dataset = parse_file(train_file)

    class_index = len(attribute_list) - 1
    for (i, attr) in enumerate(attribute_list):
        if i < class_index:
            print("%s %s" % (attr, attribute_list[class_index]))
    print("")

    # estimate P(Y = y)

    counts = {}
    for v in value_list[class_index]:
        counts[v] = 0
    for data in dataset:
        for v in value_list[class_index]:
            if (data[class_index] == v):
                counts[v] += 1

    total_data = len(dataset)
    for (v, count) in counts.items():
        P[v] = float(count + 1) / (total_data + len(value_list[class_index]))

    condP = {}

    # estimate functon two
    class_count = {}
    for data in dataset:
        class_value = data[class_index]
        if class_value not in class_count:
            class_count[class_value] = 0
        class_count[class_value] += 1
        for (attr_index, value) in enumerate(data):
            if attr_index < class_index:
                attr = attribute_list[attr_index]
                if attr not in condP:
                    condP[attr] = {}
                if value not in condP[attr]:
                    condP[attr][value] = {}
                if class_value not in condP[attr][value]:
                    condP[attr][value][class_value] = 0
                condP[attr][value][class_value] += 1

    for (i, attr) in enumerate(attribute_list):
        if i < class_index:
            for value in value_list[i]:
                if value not in condP[attr]:
                    condP[attr][value] = {}
                for class_value in value_list[class_index]:
                    if class_value not in condP[attr][value]:
                        condP[attr][value][class_value] = float(1) / (len(value_list[i]) + class_count[class_value])
                    else:
                        condP[attr][value][class_value] = float(condP[attr][value][class_value] + 1) / (len(value_list[i]) + class_count[class_value])

    # classification
    res = parse_file(test_file)
    test_data_set = res[2]
    right_count = 0
    for data in test_data_set:
        max_possbility = 0.0
        dom = 0.0
        predict = ""
        for y in value_list[class_index]:
            num = P[y]

            for (i, attr) in enumerate(attribute_list):
                if i != class_index:
                    num *= condP[attr][data[i]][y]

            if num > max_possbility:
                max_possbility = num
                predict = y

            dom += num
        prob = (max_possbility) / (dom)
        if data[class_index] == predict:
            right_count += 1
        print(predict + " " + data[class_index] + " %.12g" % Decimal(prob))

    print("\n%d\n" % right_count)
    return 0


if __name__ == "__main__":
    arg_len = len(sys.argv)
    if arg_len > 4 or arg_len < 4:
        print("wrong argument")
        sys.exit(0)

    train_file = sys.argv[1]
    test_file = sys.argv[2]
    mode = sys.argv[3]

    if mode == 'n':
        naive_bayes(train_file, test_file)
    elif mode == 't':
        tan(train_file, test_file)
