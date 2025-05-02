# 🧠 Emotion Classification from Text (Machine Learning Project)

This project demonstrates a complete machine learning pipeline for training a multi-class **emotion classification model** from natural language text. It focuses on data preprocessing, exploratory analysis, model training using logistic regression, evaluation, and error analysis. This project is ideal for showcasing **practical machine learning skills**, particularly in **text classification**.
It also includes a graphical PyQt5 application that serves as a real-world use case: an interactive **Emotion Diary** that utilizes the trained model.

---

## 🎯 Objective

- Build and evaluate a supervised machine learning model to classify emotions from text using TF-IDF vectorization and logistic regression..
- Demonstrate how the model can be integrated into a user-facing application (Emotion Diary).

---

## 🧰 Tools & Libraries Used

- **Python**
- `scikit-learn` – ML pipeline, model training, grid search
- `nltk` – Text preprocessing (tokenization, stopwords, lemmatization)
- `pandas`, `numpy` – Data handling and analysis
- `matplotlib`, `seaborn` – Data visualization
- `pickle` – Saving and loading models

To install all dependencies:

```bash
pip install -r requirements.txt
```

---

## 📂 Dataset Format

```csv
text,emotion
"I am so happy today!",joy
"This is terrible and frustrating",anger
```

---

## 🚀 Pipeline Overview

1. **Data Loading & Exploration**
   - Load and validate CSV data
   - Display emotion distribution and text length stats

2. **Text Preprocessing**
   - Clean, tokenize, remove stopwords, lemmatize

3. **Model Training**
   - TF-IDF + Logistic Regression pipeline
   - Hyperparameter tuning with GridSearchCV

4. **Evaluation**
   - Accuracy score
   - Classification report
   - Confusion matrix visualization

5. **Error Analysis**
   - Common misclassifications
   - Top confusion pairs

6. **Model Saving & Reuse**
   - Save model and emotion mapping with pickle
   - Load model for batch predictions

---

## 📊 Sample Output

```
Text: I’m feeling so proud today!
Predicted Emotion: joy
Top Emotions: joy (0.89), surprise (0.06), neutral (0.04)
```

---
## 📈 Model Performance
              precision    recall  f1-score   support

       anger       0.89      0.96      0.92     11895
        fear       0.90      0.83      0.86      9930
         joy       0.98      0.90      0.94     29286
        love       0.74      0.96      0.84      7171
     sadness       0.97      0.94      0.95     25171
    surprise       0.69      0.94      0.79      3109

    accuracy                           0.92     86562
    macro avg      0.86      0.92      0.88     86562
    weighted avg   0.93      0.92      0.92     86562

---
## ✅ Skills Demonstrated

- End-to-end ML pipeline development
- NLP preprocessing techniques
- Hyperparameter optimization
- Visual performance analysis
- Model packaging for deployment

---
## 💡 GUI Application: Emotion Diary

A simple desktop application (`einference_emotion_diary_app.py`) built with PyQt5:

- Input and analyze emotions in your daily notes.
- Save entries with emotion and timestamp.
- View, edit, delete entries.
- Export diary to `.txt` format.

---

## 🔮 Future Improvements

- Use a larger and more diverse dataset to improve model accuracy.
- Add support for more emotion categories if needed.
- Improve preprocessing by handling misspellings or informal language.
- Make the GUI more interactive and user-friendly.
- Explore saving entries to a cloud service or database.

---

## 👩‍💻 Author

**EngFAI**  
> Computer Engineer passionate about AI and machine learning  
> GitHub: [EngFAI](https://github.com/EngFAI)