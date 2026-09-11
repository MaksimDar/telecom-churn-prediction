# Telecom Customer Churn Prediction

An end-to-end machine learning project for predicting the likelihood that a telecom customer will churn, based on historical account, subscription, and usage data.

---

## 1. Project Overview

The project covers the full machine learning lifecycle: exploratory data analysis, data preprocessing, training and comparison of five classification algorithms, and a Streamlit web application for real-time churn prediction, containerized with Docker.

**Dataset:** `internet_service_churn.csv` — 72,274 customer records with  subscription, contract, and usage-based features, and a binary `churn` target.

---

## 2. Repository Structure

```
telecom-churn-prediction/
├── data/                    # Raw and processed datasets
├── notebooks/
│   └── 01_eda.ipynb          # EDA + preprocessing (interleaved by design — see notes below)
│   └── 02_model_training.ipynb  # Model training, tuning, evaluation, comparison
├── functions/                # Reusable  functions
├── models/                   # Saved model artifacts (.pkl, .keras) and fitted scaler
├── history_nn/               # Training history (loss/accuracy curves) for the Neural Network
├── pages/                    # Streamlit multipage app screens
├── streamlit_app.py          # Streamlit application entry point
├── requirements.txt
├── Dockerfile                # (see Section 5)
├── .gitignore
└── LICENSE
```

**Note:** Exploratory analysis and preprocessing are intentionally combined in a single notebook, since each preprocessing decision (missing-value handling, feature engineering) was made as a direct result of the investigation that preceded it, with its reasoning documented alongside the analysis itself.

---

## 3. Data Analysis & Preprocessing

**Key EDA findings:**
- Missing values in `remaining_contract` (~30% of rows) were found to be non-random: customers missing this value churn at 91.4% vs. 40.1% for those with an active contract record. Rather than simple imputation, two features were engineered instead: `has_contract_info` (whether contract data exists at all) and `has_active_contract` (whether the contract is currently active).
- Similarly, missing `download_avg`/`upload_avg` values were linked to recently registered customers (0% churn among them), handled via an indicator feature `has_usage_data`.
- The `dual_subscriber` feature was dropped after correlation analysis revealed a near-perfect (99.99%) correlation with `is_movie_package_subscriber`.
- The `id` feature was dropped, as its correlation with churn (-0.45) was found to be an artifact of customer signup order rather than a genuine predictor.
- Standardization (`StandardScaler`) was applied uniformly across all features prior to model training — including for tree-based models, where it is not strictly required, in order to maintain a single, consistent preprocessing pipeline.

---

## 4. Models & Parameters

Five classification models were trained and compared, each tuned via `GridSearchCV` with cross-validation:

| Model | Key parameters |
|---|---|
| Logistic Regression | `C=7.5`, `penalty='l2'` |
| Decision Tree | `criterion='entropy'`, `max_depth=9`, `min_samples_leaf=3` |
| Random Forest | `criterion='entropy'`, `max_features=None`, `min_samples_leaf=4` |
| SVM | `kernel='rbf'`, `C=90`, `gamma='scale'`,`probability=True` |
| Neural Network (Keras) | Dense layers with ReLU activation, sigmoid output, Dropout regularization, Adam optimizer, `binary_crossentropy` loss |

---

## 5.  Results & Metrics

Evaluation was based on Accuracy, Precision, Recall, and F1-score (macro-averaged, and separately per class).

| Metric (macro avg) | Logistic Regression | Decision Tree | Random Forest | SVM | Neural Network |
|---|---|---|---|---|---|
| Accuracy | 0.9236 | 0.9393 | **0.9435** | 0.9322 | 0.9360 |
| Precision | 0.9219 | 0.9377 | **0.9423** | 0.9306 | 0.9347 |
| Recall | 0.9256 | 0.9401 | **0.9437** | 0.9331 | 0.9362 |
| F1-score | 0.9231 | 0.9387 | **0.9430** | 0.9316 | 0.9354 |

**Conclusion:** **Random Forest** was selected as the final model — it consistently ranks first or a close second across nearly every metric for both classes, while remaining fast to train and straightforward to deploy. Logistic Regression remains a strong alternative where interpretability is prioritized. The accuracy spread across all models does not exceed 2%, indicating a strong, largely linearly separable signal in the engineered features.

---

## 6. Integration & Interface

The web application is built with Streamlit (`streamlit_app.py` with multipage navigation via `pages/`). Users upload a CSV file containing customer data matching the feature set used during training; the app automatically applies the same preprocessing (missing-value handling, `has_contract_info`/`has_active_contract` engineering) and standardization (via the saved `scaler.pkl`), then outputs a prediction ("High/Low churn probability") and probability percentage for each customer.

**Required input columns:** `is_tv_subscriber`, `is_movie_package_subscriber`, `subscription_age`, `bill_avg`, `remaining_contract`, `service_failure_count`, `download_avg`, `upload_avg`, `download_over_limit`

---

## 7. Installation & Usage

### Local setup

```bash
git clone https://github.com/MaksimDar/telecom-churn-prediction.git
cd telecom-churn-prediction

conda create -n churn-prediction python=3.10
conda activate churn-prediction
pip install -r requirements.txt

streamlit run streamlit_app.py
```

The app will be available at: `http://localhost:8501`

### Containerization / Docker

The project is containerized to ensure a reproducible runtime environment.

```bash
# Побудова образу / Build the image
docker build -t telecom-churn-app .

# Запуск контейнера / Run the container
docker run --name telecom-churn-app -p 80:8501 -d telecom-churn-app
```

The container listens on port `8501` internally, mapped to port `80` on the host machine. After a successful start, the application will be available in your browser at:

```
http://localhost
```


To stop the container:
```bash
docker stop telecom-churn-app
docker rm telecom-churn-app
```

---

## 8. Usage Example

1. Open the app at `http://localhost` (when running via Docker) or `http://localhost:8501` (when running locally without Docker).
2. Select the interface language (Ukrainian / English) in the sidebar.
3. Navigate to the **"Customer Churn Risk Assessment"** page.
4. Upload a CSV file containing customer data with the following columns: `is_tv_subscriber`, `is_movie_package_subscriber`, `subscription_age`, `bill_avg`, `remaining_contract`, `service_failure_count`, `download_avg`, `upload_avg`, `download_over_limit`.
5. The app automatically applies preprocessing (missing-value handling, `has_contract_info`/`has_active_contract` engineering, standardization) and outputs, for each customer: a prediction ("High/Low churn probability") and a probability percentage.

**Example input row:**

| is_tv_subscriber | is_movie_package_subscriber | subscription_age | bill_avg | remaining_contract | service_failure_count | download_avg | upload_avg | download_over_limit |
|---|---|---|---|---|---|---|---|---|
| 1 | 0 | 0.5 | 18 | | 0 | 12.4 | 2.1 | 0 |

**Example output:**

> **Result:** High churn probability
> **Probability:** 87.42%

---

## 9. Tech Stack

Python 3.10 · pandas · numpy · scikit-learn · TensorFlow / Keras · Streamlit · matplotlib · seaborn · joblib · Docker

---

## 10. Ліцензія / License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 11. Автор / Author

**Maksym Dovhusha**

Developed as part of a Data Science & Machine Learning course project.
