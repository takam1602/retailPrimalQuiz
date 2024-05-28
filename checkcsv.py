import pandas as pd

# CSVファイルの内容を読み込み表示する
file_path = './retailIndex.csv'
sfile_path = './salableIndex.csv'
csv_data = pd.read_csv(file_path)
scsv_data = pd.read_csv(sfile_path)
print(csv_data)
print(scsv_data)

# CSVファイルをUTF-8エンコーディングで再保存
csv_data.to_csv('retailIndex_utf8.csv', index=False, encoding='utf-8')
scsv_data.to_csv('salableIndex_utf8.csv', index=False, encoding='utf-8')
