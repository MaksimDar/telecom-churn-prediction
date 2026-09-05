import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# from functions import (get_churn_distribution, return_results_as_lists,show_graph_and_table_churns, show_all_churn_piecharts)

df = pd.read_csv('../data/raw/internet_service_churn.csv')

churned_users = df['churn'].sum()
active_users = df.shape[0] - churned_users

language = st.sidebar.selectbox(
    "Мова / Language",
    ["Українська", "English"]
)


if language == 'Українська':
    st.title('Дослідницький Аналіз Даних (EDA)')
    graph_uk = st.selectbox('Оберіть розділ:', [ "1. Активні та відтокові клієнти",
        "2. Відтік за типом підписки",
        "3. Тривалість підписки та відтік",
        "4. Середня сума рахунку та відтік",
        "5. Тривалість підписки та сума рахунку",
        "6. Відтік та збої послуг",
        "7. Відтік клієнтів із чинними контрактами",
        "8. Download/Upload та відтік",
        "9. Перевищення ліміту Download та відтік",
        "10. Кореляція між ознаками"]) 

else:
    st.title('Exploratory Data Analysis (EDA)')
    graph_en = st.selectbox('Оберіть розділ:', ["1. Active and Churned Customers",
        "2. Churn by Subscription Type",
        "3. Subscription Duration and Churn",
        "4. Average Bill Amount and Churn",
        "5. Subscription Duration and Bill Amount",
        "6. Churn and Service Outages",
        "7. Churn by Active Contract",
        "8. Download/Upload and Churn",
        "9. Download Over-Limit and Churn",
        "10. Feature Correlation"]) 

match(graph_uk):
    case '1. Активні та відтокові клієнти':
        data_users = [churned_users,active_users]
        labels_users = ['Відтік користувачів','Активні користувачі']
        explode = (0, 0.1, 0, 0)

        st.title('Частка активних користувачів та користувачів, які відмовилися від послуги компанії')
        
        fig1, ax1 = plt.subplots()
        ax1.pie(data_users, labels=labels_users, autopct='%.2f%%',colors=['Teal','Salmon'], shadow=False, labeldistance=1.1, startangle=0)
        ax1.axis('equal')  
        st.pyplot(fig1)
    case "2. Відтік за типом підписки":
        rows = ['is_tv_subscriber', 'is_movie_package_subscriber', 'dual_subscriber']

        x = ['Без підписки', 'З підпискою']
        churn_status = ['Відсутність відтоку клієнтів', 'Відтік клієнтів']
        graphichs_amount = 6
        fig, axs = plt.subplots(len(rows), 2, figsize=(12,12))
        for i, col in enumerate(rows):
            churn_count = df.groupby(rows[i])['churn'].sum().sort_index    (ascending=True)
            axs[i,0].bar(x,churn_count,label=rows[i])
            axs[i,0].set_title(f'Підписка {rows[i]}',fontsize=10)
            axs[i,0].set_xlabel(f'Кількість користувачів з {rows[i]} підпискою')
            # axs[i,0].set_xlabel(f'Users quantity with a {rows[i]} subscription') 
            axs[i,0].set_ylabel('Кількість відтоку')
            
            axs[i,1].pie(churn_count)
            axs[i,1].set_title(rows[i],fontsize=10)
            wedges, texts, autotexts = axs[i,1].pie(
                churn_count,
                autopct='%1.1f%%',  
                startangle=90
            )
            axs[i,1].legend(
                wedges, churn_status,           
                loc='upper center',
                bbox_to_anchor=(0.5, -0.05), 
                shadow=True,
                ncol=2,
                fontsize=8
            )

        fig.suptitle('Огляд відтоку клієнтів за типами підписки')
        plt.tight_layout()

        st.pyplot(fig)
    case "3. Тривалість підписки та відтік":
        ...
    case "4. Середня сума рахунку та відтік":
        ...
    case "5. Тривалість підписки та сума рахунку":
        ...
    case "6. Відтік та збої послуг":
        ...
    case "7. Відтік клієнтів із чинними контрактами":
        ...
    case "8. Download/Upload та відтік":
        ...

    case "9. Перевищення ліміту Download та відтік":
        ...

    case "10. Кореляція між ознаками":
        ...
    




