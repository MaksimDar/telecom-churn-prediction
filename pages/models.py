import streamlit as st
import pandas as pd
from functions import download_model

metrics_location = 'data/final_comparison'
final_comparison_churn_df = pd.read_csv(f'{metrics_location}/churn_df.csv') 

final_comparison_no_churn_df = pd.read_csv(f'{metrics_location}/no_churn_df.csv')
final_comparison_macro_df = pd.read_csv(f'{metrics_location}/macro_df.csv')


# language = st.sidebar.selectbox(
#     "Мова / Language",
#     ["Українська", "English"],
#     key="language"
# )

if st.session_state.language == "Українська":
    st.title('Розроблені моделі')
    st.markdown('### Порівняння моделей')

    st.markdown("##### 1. Порівняння моделей — метрики для класу «Відтік» (1)")
    st.dataframe(final_comparison_churn_df)

    st.markdown("##### 2. Порівняння моделей — метрики для класу «Без відтоку» (0)")
    st.dataframe(final_comparison_no_churn_df)

    st.markdown("##### 3. Порівняння моделей — макросередні метрики")
    st.dataframe(final_comparison_macro_df)

    st.markdown('### Висновок')
    st.write("На основі макросередніх показників Accuracy, Precision, Recall та F1-score модель випадкового лісу (Random Forest) переважає інші за загальними результатами, тоді як нейронна мережа показала найкращий (найнижчий) показник втрат. Однак варто також розглянути показники в розрізі окремих класів («мікро»-метрики), оскільки вони показують, наскільки добре кожна модель розрізняє клієнтів, що йдуть, від тих, що залишаються." \
    "Для класу «немає відтоку» (0) випадковий ліс демонструє найкращі precision та F1-score, хоча дерево рішень незначно випереджає його за recall (0.9477 проти 0.9454). Для класу «відтік» (1) найкращий precision має дерево рішень, але за recall та F1-score лідирує випадковий ліс." \
    "Варто зазначити, що різниця в точності на тестових даних між усіма п'ятьма моделями не перевищує 2%, а різниця у показнику втрат між логістичною регресією, SVM та нейронною мережею не перевищує 0.04. З огляду на настільки близькі результати всіх моделей, вибір «найкращої» залежить не лише від самих метрик, а й від практичних міркувань — інтерпретованості, швидкості навчання/прогнозування та простоти розгортання." \
    "З урахуванням усього цього, фінальною моделлю обрано випадковий ліс (Random Forest), оскільки вона стабільно посідає перше або близьке до нього місце практично за кожною метрикою для обох класів, залишаючись при цьому швидкою у навчанні та простою для серіалізації й розгортання. Логістична регресія залишається сильним альтернативним варіантом там, де інтерпретованість важливіша за останній відсоток продуктивності.")
    model_type = st.selectbox(
    "Оберіть модель:",
    [
        "1. Логістична регресія",
        "2. Дерево рішень",
        "3. Випадковий ліс",
        "4. Метод опорних векторів (SVM)",
        "5. Нейронна мережа",
    ],)
    match(model_type):
        case "1. Логістична регресія":
            model_direction = 'models/logistic_regression/best_logistic_regression_model.pkl'
            label = "Завантажити найкращу модель логістичної регресії"
            filename = "best_logistic_regression_model.pkl"
            download_model(model_direction,label,filename)

        case "2. Дерево рішень":
            model_direction = 'models/decision_tree/best_decision_tree_model.pkl'
            label = "Завантажити найкращу модель дерева рішень"
            filename = "best_decision_tree_model.pkl"
            download_model(model_direction,label,filename)
                
        case "3. Випадковий ліс":
            model_direction = 'models/random_forest/best_random_forest_model.pkl'
            label = "Завантажити найкращу модель «випадкового лісу»"
            filename = "best_random_tree_model.pkl"
            download_model(model_direction,label,filename)

            
        case "4. Метод опорних векторів (SVM)":
            model_direction = 'models/svm/best_svm_model.pkl'
            label = "Завантажити модель SVM"
            filename = "best_svm_model.pkl"
            download_model(model_direction,label,filename)

        case "5. Нейронна мережа":
            model_direction = 'models/neural_network/neural_network.keras'
            label = "Завантажити нейронну мережу"
            filename = "best_decision_tree_model.pkl"
            download_model(model_direction,label,filename)



else:
    st.title('Developed models')
    st.markdown('### Comparison of models')
    st.markdown("##### 1. Model Comparison — Churn Class (1) Metrics")
    st.dataframe(final_comparison_churn_df)

    st.markdown("##### 2. Model Comparison — No-Churn Class (0) Metrics")
    st.dataframe(final_comparison_no_churn_df)
    
    st.markdown("##### 3. Model Comparison — Macro-Averaged Metrics")
    st.dataframe(final_comparison_macro_df)

    st.markdown('### Conclusion')
    st.write("Based on the macro-averaged Accuracy, Precision, Recall, and F1-score, the Random Forest model outperforms the others overall, while the Neural Network achieved the best (lowest) loss score. However, it is also worth examining the class-specific `micro` metrics, since these reveal how well each model distinguishes churned customers from retained ones specifically.' \
    'For the no-churn class (0), Random Forest achieves the best precision and F1-score, though the Decision Tree edges it out slightly on recall (0.9477 vs. 0.9454). For the churn class (1), the Decision Tree obtains the best precision, but Random Forest leads on both recall and F1-score.' \
    'Notably, the difference in test accuracy across all five models does not exceed 2%, and the loss difference between Logistic Regression, SVM, and the Neural Network does not exceed 0.04. Given how closely all models perform, the choice of a best model depends not only on raw metrics but also on practical considerations such as interpretability, training/inference speed, and ease of deployment.' \
    'Taking all of this into account, Random Forest is selected as the final model, as it consistently ranks first or a close second across nearly every metric, for both classes, while remaining fast to train and straightforward to serialize and deploy. Logistic Regression remains a strong secondary option where interpretability is prioritized over the last percentage point of performance.")

    model_type = st.selectbox('Choose the model:', [ "1. Logistic Regression",
        "2. Decision Tree",
        "3. Random Forest",
        "4. Support Vector Machine (SVM)",
        "5. Neural Network",]) 
    match(model_type):
        case "1. Logistic Regression":
            model_direction = 'models/logistic_regression/best_logistic_regression_model.pkl'
            label = "Download Best Logistic Regression Model"
            filename = "best_logistic_regression_model.pkl"

            download_model(model_direction,label,filename)

        case "2. Decision Tree":
            model_direction = 'models/decision_tree/best_decision_tree_model.pkl'
            label = "Download Best Decision Tree Model"
            filename = "best_decision_tree_model.pkl"
            download_model(model_direction,label,filename)
            
        case "3. Random Forest":
            model_direction = 'models/random_forest/best_random_forest_model.pkl'
            label = "Download Best Random Forest Model"
            filename = "best_random_tree_model.pkl"
            download_model(model_direction,label,filename)

            
        case "4. Support Vector Machine (SVM)":
            model_direction = 'models/svm/best_svm_model.pkl'
            label = "Download SVM Model"
            filename = "best_svm_model.pkl"
            download_model(model_direction,label,filename)

        case "5. Neural Network":
            model_direction = 'models/neural_network/neural_network.keras'
            label = "Download Neural Network"
            filename = "best_decision_tree_model.pkl"
            download_model(model_direction,label,filename)
            
            


    
