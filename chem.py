import pandas as pd
from chemdataextractor import Document

# 读取CSV文件
df = pd.read_csv('C:\\Users\\sy\\Desktop\\perovskite_cosine_similarity.csv', encoding='gb18030')

# 提取第一列数据
column_data = df['n']

# 定义函数来识别化学物质
def is_chemical(entity):
    doc = Document(entity)
    chem_entities = doc.cems
    return len(chem_entities) > 0

# 创建新列来表示化学物质
df['Chemical'] = column_data.apply(lambda x: 1 if is_chemical(x) else 0)

# 删除最后一列是 0 的整行
df = df[df.iloc[:, -1] != 0]

# 删除最后一列
df = df.drop(df.columns[-1], axis=1)

# 保存结果到新的CSV文件
df.to_csv('output_file.csv', index=False)
