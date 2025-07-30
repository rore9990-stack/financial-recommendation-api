import mysql.connector
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# الاتصال بقاعدة البيانات
conn = mysql.connector.connect(
    host="fdb1027.biz.nf",
    user="4515138_maly",
    password="Ro0597980060-",
    database="4515138_maly"
)
cursor = conn.cursor(dictionary=True)

# جلب المستخدمين
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
users_df = pd.DataFrame(users)

# جلب العمليات
cursor.execute("SELECT user_id, category, amount FROM transactions")
transactions = cursor.fetchall()
transactions_df = pd.DataFrame(transactions)

cursor.close()
conn.close()

# التأكد من وجود بيانات كافية
if users_df.empty or transactions_df.empty:
    raise ValueError("لا توجد بيانات كافية لتدريب النموذج.")

# تجهيز الميزات لكل مستخدم
features = []
labels = []

for _, user in users_df.iterrows():
    user_id = user['id']
    user_transactions = transactions_df[transactions_df['user_id'] == user_id]

    if user_transactions.empty:
        continue

    income = user['income']
    total_spent = user_transactions['amount'].sum()
    category_count = user_transactions['category'].nunique()

    # الميزات
    X = [income, total_spent, category_count]
    features.append(X)

    # التصنيف المؤقت: دخل أكبر من المصروف → "ادخر المزيد"
    if total_spent < income:
        label = "ادخر المزيد"
    else:
        label = "قلل المصروف"

    labels.append(label)

# تدريب النموذج
model = RandomForestClassifier()
model.fit(features, labels)

# حفظ النموذج
joblib.dump(model, 'model.pkl')
print("✅ تم تدريب النموذج وحفظه بنجاح.")
