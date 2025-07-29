from sklearn.linear_model import LogisticRegression
import joblib
import numpy as np

# بيانات وهمية
X = np.array([
    [5000, 2000, 5],
    [10000, 3000, 8],
    [8000, 5000, 4],
    [4000, 3500, 6],
    [12000, 4000, 9]
])
y = [1, 2, 1, 0, 2]  # تمثيل للتوصيات

model = LogisticRegression()
model.fit(X, y)

joblib.dump(model, 'model.pkl')
print("✅ تم حفظ النموذج في model.pkl")
