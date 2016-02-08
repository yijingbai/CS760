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

    for (attr, value) in condP.items():
        for (v, cla) in value.items():
            for clas in cla.keys():
                condP[attr][v][clas] /= float(class_count[clas])

    for (attr, value) in condP.items():
        print(attr + ": ")
        for (v, cla) in value.items():
            print("    " + v + ": ")
            for clas in cla.keys():
                print("        " + clas + ": " + str(condP[attr][v][clas]))

    print(P)
    # classification
    is_data_line = False
    with open(test_file) as test:
        for line in test:
            if is_data_line:
                data = line.strip().split(',')
                print(data)
                max_possbility = 0.0
                dom = 0.0
                predict = ""
                for y in value_list[class_index]:
                    print("y is " + y)
                    print("P[y] is " + str(P[y]))
                    num = P[y]

                    for (i, attr) in enumerate(attribute_list):
                        print("attr: " + attr + "  at index: " + str(i))
                        if i != class_index:
                            print("    " + " * " + "P(" + attr + "|" +
                                  data[i] + ")")
                            try:
                                num *= condP[attr][data[i]][y]
                            except:
                                num *= 0.0
                            print("nums is " + str(num))

                    if num > max_possbility:
                        max_possbility = num
                        predict = y

                    dom += num
                    print("Dom is " + str(dom))

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
