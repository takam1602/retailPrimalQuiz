import pandas as pd

# CSVファイルの内容を読み込み表示する
file_path = './retailIndex.csv'
csv_data = pd.read_csv(file_path)
print(csv_data)

# CSVファイルをUTF-8エンコーディングで再保存
csv_data.to_csv('retailIndex_utf8.csv', index=False, encoding='utf-8')
