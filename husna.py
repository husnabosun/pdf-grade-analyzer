import pymupdf
import pandas as pd
import math


def get_df(doc):
    df_list = []
    id_counter = 0
    column_names = None

    for i in range(len(doc)):
        page = doc[i]
        tables = (page.find_tables()).tables

        if tables:
            table = tables[0]
            raw_data = table.extract()
            # df = table.to_pandas()

            if i == 0:
                column_names = raw_data[0]
                data = raw_data[1:]
                #column_names = df.columns.tolist()
            else:
                data = raw_data
                #df.columns = column_names

            df = pd.DataFrame(data, columns=column_names)
            df.index = range(id_counter, id_counter + len(df))
            id_counter += len(df)
            df_list.append(df)

        else:
            print("sorry")

    full_df = pd.concat(df_list, ignore_index=True)
    return full_df


def calc_sd(full_df, total_avg_result):
    without_nan_df = full_df[(full_df["MyAccumulated"] != 'NaN')].copy()
    grades_sum = ((without_nan_df["MyAccumulated"] - total_avg_result) ** 2).sum()
    sd = math.sqrt(grades_sum / len(without_nan_df))
    return sd

# letter grade guesses are made using my observations
# in past exams


def see_sorted_df(full_df):
    df_sorted = full_df.sort_values(by="MyAccumulated", ascending=False)
    df_sorted.reset_index(drop=True, inplace=True)
    df_sorted.index = range(1, len(df_sorted) + 1)
    print(df_sorted)


def guess_letter_grades(sd , total_avg_result):
    aa_1 = total_avg_result + 1.5 * sd
    aa_2 = total_avg_result + sd
    ba_1 = total_avg_result + 0.75 * sd
    ba_2 = total_avg_result + 0.5 * sd
    bb_1 = total_avg_result + 0.5 * sd
    bb_2 = total_avg_result + 0.3 * sd
    cb_1 = total_avg_result + 0.3 * sd
    cb_2 = total_avg_result
    cc_1 = total_avg_result
    cc_2 = total_avg_result - 0.3 * sd
    dc_1 = total_avg_result - 0.3 * sd
    dc_2 = total_avg_result - 0.5 * sd
    dd_1 = total_avg_result - 0.5 * sd
    dd_2 = total_avg_result - 0.75 * sd

    print(f"AA Interval: > {aa_1} - {aa_2}")
    print(f"BA Interval: Between {ba_1} - {ba_2}")
    print(f"BB Interval: Between {bb_1} - {bb_2}")
    print(f"CB Interval: Between {cb_1} - {cb_2}")
    print(f"CC Interval: Between {cc_1} - {cc_2}")
    print(f"DC Interval: Between {dc_1} - {dc_2}")
    print(f"DD Interval: Between {dd_1} - {dd_2}")


def calculus_letter_grade():
    aa = 85
    ba = 80
    bb = 75
    cb = 68
    cc = 60
    dc = 50
    dd = 40

    print(f"AA Interval: > {aa}")
    print(f"BA Interval: Between {aa} - {ba}")
    print(f"BB Interval: Between {ba} - {bb}")
    print(f"CB Interval: Between {bb} - {cb}")
    print(f"CC Interval: Between {cb} - {cc}")
    print(f"DC Interval: Between {cc} - {dc}")
    print(f"DD Interval: Between {dc} - {dd}")
    print(f"Failed < {dd}")


def find_my_accumulated_grade(my_number, full_df, sd, total_avg_result, col_name):
    row_founded = full_df[full_df[col_name] == my_number]
    accumulated_founded = row_founded["MyAccumulated"].iloc[0]

    exam_name = input("Is the exam you took math? y/N: ")
    if exam_name.upper() == 'Y':
        print(f"Your total accumulated grade is:  {accumulated_founded} ")
        calculus_letter_grade()
    elif exam_name.upper() == 'N':
        print(f"Your total accumulated grade is: {accumulated_founded} ")
        guess_letter_grades(sd, total_avg_result)
    else:
        print("Please enter a valid answer: ")
        exam_name = input("Is the exam you took math? y/N: ").upper()


def find_my_ranking(full_df, my_number, col_name):
    df_sorted = full_df.sort_values(by="MyAccumulated", ascending=False)
    df_sorted.reset_index(drop=True, inplace=True)
    df_sorted.index = range(1, len(df_sorted) + 1)
    # print(df_sorted)
    rank = df_sorted.index[df_sorted[col_name] == my_number]
    print(f"Your ranking is : {rank[0]} with grade {df_sorted.loc[df_sorted[col_name] == my_number, "MyAccumulated"].iloc[0]}")

def husna():
    doc = pymupdf.open("grades_multiple_col.pdf")
    page = doc[0]
    tables = (page.find_tables()).tables

    if tables:
        table = tables[0]
        df = table.to_pandas()
        column_names = df.columns.tolist()

        perc_list = []
        print("For every column name please enter the percentage that affects total grade as a number (without '%' sign)")
        print("If the column name does not relate to grade please enter 0")
        for i in column_names:
            print(i)
            perc_list.append(float(input("Enter the percentage: ")))

        exam_vs_percentage_dict = dict(zip(column_names,perc_list))

        full_df = get_df(doc)

        name_vs_avg_dict = {}
        percentage_vs_avg_dict = {}

        full_df['MyAccumulated'] = 0
        for exam, percentage in exam_vs_percentage_dict.items():
            if percentage == 0:
                name_vs_avg_dict[exam] = 0
            else:
                without_na_df = full_df[
                    (full_df[exam] != '') & (full_df[exam] != 'NA') & (full_df[exam] != 'N/A') & (full_df[exam] != '* HWs are equally graded.')].copy()
                pd.set_option('display.max_rows', None)
                without_na_df.loc[:, exam] = pd.to_numeric(without_na_df[exam].str.replace(',', '.', regex=False))
                full_df.loc[:, exam] = pd.to_numeric(full_df[exam].str.replace(',', '.', regex=False), errors="coerce")
                full_df["MyAccumulated"] += without_na_df[exam] * (percentage / 100)
                percentage_vs_avg_dict[(exam, percentage)] = int(without_na_df[exam].sum()) / (len(without_na_df))

        # pd.set_option("display.max_rows", None)
        # print(full_df)
        total_avg_result = 0
        for key, value in percentage_vs_avg_dict.items():
            total_avg_result += key[1] * (value / 100)

        for key, value in percentage_vs_avg_dict:
            print(f"{key}: {value}%\n")
        print(f"Class average is {total_avg_result}")

        sd = calc_sd(full_df, total_avg_result)
        print(f"Calculated standard deviation: {sd}")

        while True:
            answer = input("To learn your accumulated grade and its letter grade interval: 1\n"
                           "To learn your ranking: 2\n"
                           "To see the full sorted data: 3"
                           "To exit: 4\n")
            if answer == "1":
                print(full_df.columns.tolist())
                col_name = input("Please enter the column that consists your student number: ")
                my_number = input("Please enter your student number: ")
                find_my_accumulated_grade(my_number, full_df, sd, total_avg_result, col_name)

            elif answer == '2':
                print(full_df.columns.tolist())
                col_name = input("Please enter the column that consists your student number: ")
                my_number = input("Please enter your student number: ")
                find_my_ranking(full_df, my_number, col_name)

            elif answer == "3":
                see_sorted_df(full_df)

            elif answer == "4":
                print("Exiting program...")
                break
            else:
                print("Please enter a valid answer.1,2 or 3 ")

husna()