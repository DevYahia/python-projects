import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import tabula

file_path = str(input('enter file path: '))
subject = input('enter subject name: ')

sns.set()


def draw_graph(f, subject):
    df_list = tabula.read_pdf(f, pages='all')
    id_mark_dict = {}

    try:
        for df in df_list:
            for lab, row in df.iterrows():
                if row[2] <= 100 and not None:
                    id_mark_dict[row[0]] = row[1] + row[2] + row[3]
    except IndexError:
        print('jumped here')
        for df in df_list:
            for lab, row in df.iterrows():
                if row[1] <= 100:
                    id_mark_dict[row[0]] = row[1]
    except TypeError:
        print('jumped here')
        id_mark_dict = {}
        for df in df_list:
            for lab, row in df.iterrows():
                if row[3] <= 100:
                    id_mark_dict[row[2]] = row[3]

    print(id_mark_dict)
    marks_arr_np = np.array([id_mark_dict[i] for i in id_mark_dict])

    marks_arr_np = marks_arr_np[~np.isnan(marks_arr_np)]
    average = marks_arr_np.mean()
    median = np.median(marks_arr_np)

    try:
        del (id_mark_dict['Average'],
             id_mark_dict['Max.'],
             id_mark_dict['Min.'],
             id_mark_dict['MEDIAN'],
             id_mark_dict['STDEV'])
    except KeyError as e:
        print(e)

    marks_dict = {}
    for mark in id_mark_dict.values():
        if mark in marks_dict:
            marks_dict[mark] += 1
        else:
            marks_dict[mark] = 1

    marks_count_np, marks_num_np = np.array([]), np.array([])

    for k, v in marks_dict.items():
        marks_count_np = np.append(marks_count_np, v)
        marks_num_np = np.append(marks_num_np, k)

    all_marks_np = np.column_stack((marks_num_np, marks_count_np))
    sorted_arr = all_marks_np[all_marks_np[:, 0].argsort()]
    marks_count_np, marks_num_np = sorted_arr[:, 1], sorted_arr[:, 0]

    x_ticks = list(range(len(marks_dict.keys())))
    x_labels = list(marks_dict.keys())
    x_labels.sort()

    plt.figure(figsize=(16, 9), dpi=100)
    ax = plt.axes()
    ax.set_facecolor('#e0e0e0')
    bar_list = plt.bar(x_ticks, marks_count_np, width=.7, color='#26a69a')
    for x, y in zip(x_ticks, marks_count_np):
        label = "{:}".format(int(y))
        plt.annotate(
            label,  # this is the text
            (x, y),  # this is the point to label
            textcoords="offset points",  # how to position the text
            xytext=(0, 5),  # distance from text to points (x,y)
            ha='center')  # horizontal alignment can be left, right or center

    plt.xticks(x_ticks, x_labels, rotation=90)
    plt.xlabel('Marks', weight='bold', fontsize=12)
    plt.ylabel('Count', weight='bold', fontsize=12)
    plt.title('Doctor {subject} Marks'.format(subject=subject),
              weight='bold',
              fontsize=16)

    all_marks_np = all_marks_np[~np.isnan(all_marks_np[:, 0])]
    print(all_marks_np[:, 0])
    i, c = 0, 0
    print(average)
    all_marks_np_s = np.sort(all_marks_np[:, 0])
    print(all_marks_np)
    while i < average:
        i = all_marks_np_s[c]
        print(i)
        c += 1
    average_ind = np.where(all_marks_np[:, 0] == i)[0] - 0.5
    print('all: ' + str(all_marks_np))
    # print(np.where(all_marks_np[:, 0] == i))
    print(average_ind)
    plt.axvline(average_ind, color='#00695c')
    plt.annotate(
        'Average: {:}'.format(average),
        (average_ind, max(marks_count_np) - 0.5),
        textcoords='offset points',
        xytext=(0, 0),
        ha='center',
        weight='bold')
    bar_list[int(np.where(marks_num_np == median)[0])].set_color('#00838f')
    plt.savefig('D:\\foo.png')
    plt.show()
    plt.clf()


draw_graph(file_path, subject)
