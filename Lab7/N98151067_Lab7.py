import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

data = np.loadtxt("Bank_Customer.csv", skiprows=1, dtype=str, delimiter=',')

'''
Your work
非數值型資料需轉換成數值型資料 (country, gender)
去除掉無意義的特徵類別 (customer_id)
標準化特徵 (StandardScaler)
'''
# 欄位: 0 customer_id, 1 credit_score, 2 country, 3 gender, 4 age, 5 tenure,
#       6 balance, 7 products_number, 8 credit_card, 9 active_member,
#       10 estimated_salary, 11 churn

# 1. 去除無意義特徵: customer_id (第 0 欄) 只是編號，與是否流失無關
data = data[:, 1:]
# 去除後: 0 credit_score, 1 country, 2 gender, 3 age, 4 tenure, 5 balance,
#         6 products_number, 7 credit_card, 8 active_member, 9 estimated_salary, 10 churn

# 2. 非數值型資料轉數值
# gender: Female -> 0, Male -> 1
gender = (data[:, 2] == "Male").astype(float).reshape(-1, 1)

# country: 三個國家沒有大小順序，使用 One-Hot Encoding
countries = np.unique(data[:, 1])          # ['France' 'Germany' 'Spain']
country = (data[:, 1].reshape(-1, 1) == countries).astype(float)

# 其餘數值欄位
numeric = data[:, [0, 3, 4, 5, 6, 7, 8, 9]].astype(float)
label = data[:, 10].astype(float).reshape(-1, 1)   # churn

# 組合成全數值資料 (最後一欄為 churn)
features = np.hstack([numeric, gender, country])

# 標準化改在切割之後做 (只用訓練資料 fit)，避免測試資料的資訊洩漏給模型
pre_data = np.hstack([features, label])

header = ("credit_score,age,tenure,balance,products_number,credit_card,"
          "active_member,estimated_salary,gender,"
          + ",".join("country_" + c for c in countries) + ",churn")
np.savetxt("Bank_Customer_Preprocessed.csv", pre_data, delimiter=",",
           header=header, comments="", fmt="%.6f")


from sklearn.linear_model import LogisticRegression
# 決策分類器
clf = LogisticRegression()

'''
Your work
切割 data 為 x_train, x_test, y_train, y_test
請學習 train_test_split 的使用方法
'''
x = pre_data[:, :-1]
y = pre_data[:, -1]
# 70% 訓練、30% 測試；stratify 讓兩組的流失比例一致；random_state 固定結果可重現
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.3, random_state=42, stratify=y)

# 3. 標準化特徵：只用訓練資料計算平均與標準差，再套用到訓練與測試資料
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

# 使用訓練集來訓練我們的分類器
clf.fit(x_train, y_train)
# 測試資料集中進行預測
pred = clf.predict(x_test)

#print (pred) # 預測分類，即客戶是否流失
#print (y_test) # 分類
print (str(accuracy_score(pred, y_test)*100 ) + "% ")   # 預測精度
