import os
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as pdr


def execute_stock_to_plt(
    dts,
    keyword,
    code: str,
):
    df = pdr.get_data_yahoo(code, "2022-04-01")
    # df.to_excel('./data/NVDA.xlsx')
    df.reset_index(inplace=True, drop=False)
    # print(df.keys())
    # print(df.head())

    plt.figure(figsize=(10, 4))
    plt.plot(df["Date"], df["Close"])
    plt.xlabel("date")
    plt.ylabel("close")
    plt.tick_params(axis="x", which="both", bottom=False, top=False, labelbottom=False)
    for dt in dts:
        dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
        td = timedelta(days=0.1)
        plt.axvspan(dt - td, dt + td, facecolor="gray", alpha=0.5)
    plt.savefig(f"./data/{keyword}_sample.png", dpi=300)


def execute_read_list(keyword):
    date_count = {}
    for dir in os.listdir(f"./data/{keyword}"):
        for big_i in os.listdir(f"./data/{keyword}/{dir}"):
            for i in os.listdir(f"./data/{keyword}/{dir}/{big_i}"):
                date_str = i[8:20]
                # print(date_str) => 202206101530
                tmp_date = datetime(int(date_str[:4]), int(date_str[4:6]), int(date_str[6:8]))
                date_count[str(tmp_date)] = date_count.get(str(tmp_date), 0) + 1

    # print(date_count)
    # print(date_count.keys())
    return date_count.keys()


def get_code(name):
    code_df = pd.read_html("http://kind.krx.co.kr/corpgeneral/corpList.do?method=download", header=0)[0]
    code_df = code_df[["회사명", "종목코드"]]
    code_df = code_df.rename(columns={"회사명": "name", "종목코드": "code"})
    code_df.code = code_df.code.map("{:06d}".format)
    code = code_df.query("name=='{}'".format(name))["code"].to_string(index=False).strip()
    return code + ".KS"


if __name__ == "__main__":
    # 대한항공(003490), 엔비디아(NVDA)
    keyword = "대한항공"
    # keyword = "엔비디아"
    dts = execute_read_list(keyword)
    # True: 국내주식, False: 해외주식
    code = get_code(keyword) if True else "NVDA"
    execute_stock_to_plt(dts, keyword, code=code)
