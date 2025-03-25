import joblib
import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split

from sklearn.metrics import f1_score, confusion_matrix

file_path = "data/news/news.json"

with open(file_path, "r", encoding="utf-8") as file:
    data = [json.loads(line) for line in file]

df = pd.DataFrame(data)
df.head()

filtered_columns = {"short_description", "category"}

df.rename(columns={"short_description": "text"}, inplace=True)
df.dropna(subset=["text", "category"], inplace=True)

df = df[df["category"].str.strip() != ""]
df.head()

X_train, X_test, y_train, y_test = train_test_split(df["text"], df["category"], test_size=0.2, random_state=42)

assert len(X_train) == len(y_train), "Mismatch in training data samples"
assert len(X_test) == len(y_test), "Mismatch in testing data samples"

model = make_pipeline(TfidfVectorizer(), MultinomialNB())
model.fit(X_train, y_train)
joblib.dump(model, "news_classification_model.pkl")

print("Model saved successfully!")