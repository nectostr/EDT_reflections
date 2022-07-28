from matplotlib import pyplot as plt
import pandas as pd
import src.roberta as rob

df = pd.read_csv("data/anonymized_results.csv")

target = pd.DataFrame()
dump = pd.DataFrame()

for week_n in range(2, 9):
    target[f"week{week_n}_text"] = [""] * len(df)
    for col in df.columns:
        if f"week{week_n}" in col:
            if len(df.groupby([col]).size()) < 10:
                continue
            dump[col] = df[col]
            dump.loc[dump[col].astype(str).str.len() < 5,col] = ""
            dump.fillna("", inplace=True)
            target[f"week{week_n}_text"] += dump[col].astype(str)

cur_cols = target.columns
for col in cur_cols:
    print(col)
    num = col[4]
    list_col = [str(i)for i in target[col]]
    lengths = [len(i) for i in list_col]
    print(min(lengths), max(lengths), sum(lengths)/len(lengths))
    print(len([i for i in lengths if i > 500]))
    print()
    list_col = [i[:500] for i in list_col]
    target[f"week{num}_santiment"] = rob.get_scores_for(list_col)

    #See how they came - neg, neu, pos
for num in range(2, 9):
    prediction = pd.DataFrame()
    prediction["A"] = target[f"week{num}_santiment"].apply(lambda x: x[0])
    prediction["B"] = target[f"week{num}_santiment"].apply(lambda x: x[1])
    prediction["C"] = target[f"week{num}_santiment"].apply(lambda x: x[2])
    plt.scatter(prediction)
    plt.show()