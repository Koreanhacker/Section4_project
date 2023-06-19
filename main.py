

#libraries
import numpy as np 
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification
from sklearn.linear_model import LinearRegression, LogisticRegression
from category_encoders import OneHotEncoder
from sklearn.preprocessing import StandardScaler

import pickle


import psycopg2


host = 'rajje.db.elephantsql.com'
user = 'squeplml'
password = 'RMWHdM8i_byfTMiMkoiWvf8vWDcfHhoQ'
database = 'squeplml'

connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

cur = connection.cursor()

# 데이터 가져오기
cur.execute("SELECT * FROM heart_2020;")
data = cur.fetchall()

# 컬럼 이름 가져오기
cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='heart_2020';")
columns = [col[0] for col in cur.fetchall()]

# 데이터프레임으로 변환
df = pd.DataFrame(data, columns=columns)


# 타겟 데이터 범주의 비율을 확인합니다.
y =  df['heartdisease']

df.drop('id',axis=1)
df.drop_duplicates(keep='first', inplace=True)


# 결측치는 없습니다.
df.isna().sum()

df.dropna(inplace=True)


# 수치형 특성의 아웃라이어를 삭제해주겠습니다.
def outlier_iqr(data) :
    q1, q3 = data.quantile([0.25, 0.75])
    iqr = q3 - q1
    return q3 + (iqr*1.5)

bmi_upper = outlier_iqr(df['bmi'])
ph_upper = outlier_iqr(df['physicalhealth'])
mh_upper = outlier_iqr(df['mentalhealth'])
sl_upper = outlier_iqr(df['sleeptime'])

          

df = df[(df['bmi']<bmi_upper) | (df['physicalhealth']<ph_upper) | (df['mentalhealth']<mh_upper) | (df['sleeptime'] <sl_upper)]

# 범주형 특성 일부와 타겟의 관계를 시각화해보겠습니다.


# 나이
age_encoding = {'65-69':67, '60-64':62, '70-74':72, '55-59':57, '50-54':52, '80 or older':80, '75-79':77,
                 '45-49':47, '18-24' :20, '40-44':42, '35-39':37, '30-34':32, '25-29':27}

df['agecategory'] = df['agecategory'].replace(age_encoding)
df['agecategory'].astype('float')


# 전반적인 건강상태
genh_encoding = {'Poor':1, 'Fair':2, 'Excellent':3, 'Good':4, 'Very good':5}

df['genhealth'] = df['genhealth'].replace(genh_encoding)
df['genhealth'].astype('float')


### Modeling

# train, validation, test set으로 먼저 나눠주겠습니다.


# 타겟값이 문자형이기 때문에 수치형으로 바꿔주겠습니다.
df['heartdisease'] = df['heartdisease'].replace({'No':0, 'Yes':1})

y = df['heartdisease']
X = df.drop('heartdisease', axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y,  random_state=42, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, random_state=42, stratify=y_train)



# scaling

numeric_feats = X_train.dtypes[X_train.dtypes != "object"].index

scaler = StandardScaler()
X_train[numeric_feats] = scaler.fit_transform(X_train[numeric_feats])
X_val[numeric_feats] = scaler.transform(X_val[numeric_feats])
X_test[numeric_feats] = scaler.transform(X_test[numeric_feats])

# One-Hot encoding


ohe = OneHotEncoder()

X_train_ohe = ohe.fit_transform(X_train)
X_val_ohe = ohe.transform(X_val)
X_test_ohe = ohe.transform(X_test)

#### Logistic Regression

logistic = LogisticRegression(class_weight='balanced')
logistic.fit(X_train_ohe, y_train)
y_val_pred = logistic.predict(X_val_ohe)





X_val_ohe.shape

asd = pd.DataFrame(X_val_ohe.iloc[119]).T

asd.shape

y_val_pred2 = logistic.predict(asd)

y_val_pred2

if y_val_pred2 == 1:
    print('당신은 심장 질환에 걸릴 확률이 높습니다.')
else :
    print('당신은 심장 질환에 걸릴 확률이 낮습니다.')





with open('model.pkl','wb') as pickle_file:
    pickle.dump(logistic, pickle_file)

