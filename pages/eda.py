import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from functions import (get_churn_distribution, return_results_as_lists,show_graph_and_table_churns, show_all_churn_piecharts)

df = pd.read_csv('data/eda_data/df_eda.csv')

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

        st.markdown('### Частка активних користувачів та користувачів, які відмовилися від послуги компанії')
        
        fig1, ax1 = plt.subplots()
        ax1.pie(data_users, labels=labels_users, autopct='%.2f%%',colors=['Teal','Salmon'], shadow=False, labeldistance=1.1, startangle=0)
        ax1.axis('equal')  
        st.pyplot(fig1)
        st.markdown('### Висновок:')
        st.write('Кругова діаграма демонструє, що набір даних містить більше користувачів, які припинили користуватися послугами, і їхня частка становить 55,41%.')

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

        st.markdown('### Огляд відтоку клієнтів за типами підписки')
        plt.tight_layout()

        st.pyplot(fig)
        st.markdown('### Висновок:')
        st.write('На основі отриманих графіків можна чітко помітити, що понад 70 % користувачів із підпискою на телебачення відмовилися від телекомунікаційних послуг, тоді як 79,5 % користувачів, які мають підписку на фільми, не відмовилися від послуг, що доводить: підписка на пакет фільмів є важливою причиною збереження телекомунікаційних послуг. Крім того, абоненти, які мають підписку як на кінопакет, так і на подвійний пакет, демонструють однакові результати за відсотковою різницею, і лише 2 користувачі мають підписку на кінопакет, але не мають підписки на телебачення.')
    case "3. Тривалість підписки та відтік":

        min_subscription_age = df['subscription_age'].min()
        max_subscription_age = df['subscription_age'].max()
        column_comparison = 'subscription_age'
        sub_age_interval = 0.5
        sub_procedural_slip = 0.2
        
        necessary_dict = get_churn_distribution(df,min_subscription_age,      max_subscription_age,column_comparison,sub_age_interval,sub_procedural_slip)
        list_subscription_ages,list_churn_quantity = return_results_as_lists(min_subscription_age, max_subscription_age,column_comparison, necessary_dict,sub_age_interval,sub_procedural_slip)

        sub_age_title = 'Кількість відтоку за інтервалом тривалості підписки'
        x_sub_age = 'Тривалість підписки'
        
        final_sub_age_graph = show_graph_and_table_churns(list_churn_quantity,  list_subscription_ages,sub_age_title,x_sub_age)

        st.markdown('### Кількість відтоку за інтервалом тривалості підписки')
        st.pyplot(final_sub_age_graph)
        st.markdown('### Висновок:')
        st.write('На основі графіка видно, що найбільший рівень відтоку спостерігається в період від 0,5 до 2,5 років, після чого, починаючи з 3,0 років, відбувається його значне зниження. Отже, це свідчить про те, що позначка 3,0 роки є межею, після якої показники відтоку суттєво зменшуються.')

    case "4. Середня сума рахунку та відтік":
        min_bill_avg = df['bill_avg'].min()
        max_bill_avg = 220.0
        column_bill_avg = 'bill_avg'
        bill_avg_interval = 10
        bill_procedural_slip = 1
        necessary_bill_dict = get_churn_distribution(df, min_bill_avg, max_bill_avg,column_bill_avg,bill_avg_interval,bill_procedural_slip)
        bill_avg_list,churn_quantity_list = return_results_as_lists(min_bill_avg, max_bill_avg,column_bill_avg, necessary_bill_dict,bill_avg_interval,bill_procedural_slip)
        bill_avg_title = 'Кількість відтоку за інтервалом середньої суми'
        x_bill_avg = 'Середній чек'

        final_bill_avg_graph = show_graph_and_table_churns(churn_quantity_list,bill_avg_list,bill_avg_title,x_bill_avg)

        st.markdown('### Графік взаємозв’язку між середнью сумою та відтоком клієнтів')
        st.pyplot(final_bill_avg_graph)
        st.markdown('### Висновок:')
        st.write('Наведений нижче графік демонструє, що найбільший відсоток відтоку клієнтів (понад 91%) спостерігається серед облікових записів середнього розміру із залишком на рахунку 30 або менше, причому пік відтоку припадає на діапазон середнього розміру рахунку від 10 до 30. Отже, варто зазначити: що вищою є сума рахунку (починаючи з 30), то менша ймовірність того, що користувач скасує підписку. Крім того, середнє значення показника `bill_avg` становить 18,9 — це величина в межах діапазону від 10 до 20, на який припадає 35,58% випадків відтоку.')
    case "5. Тривалість підписки та сума рахунку":
        graph = sns.relplot(x='subscription_age',y='bill_avg', hue='churn', col='churn',data=df)
    
        st.markdown('### Графік взаємозв’язку між середнью сумою та відтоком клієнтів')
        st.pyplot(graph)
        st.markdown('### Висновок:')
        st.write('На даному графіку не спостерігається суттєвих відмінностей (через надмірне накладання графіків) у взаємодії змінних bill_avg та subscription_age: показники відтоку клієнтів майже однакові, за винятком того, що користувачі з найдорожчими рахунками не відмовляються від послуг і продовжують користуватися телекомунікаційними послугами.')

        df_filtered = df[df['bill_avg'] <= 150]

        fig1, ax1 = plt.subplots()
        ax1 = sns.lineplot(x='bill_avg',y='subscription_age',data=df_filtered)
        ax1.set_xlabel('Середня сума рахунку (bill_avg)')
        ax1.set_ylabel('Середній термін підписки (subscription_age)')
        plt.tight_layout()

        st.markdown('### Співвідношення між терміном підписки та середньою сумою рахунку')
        st.pyplot(fig1)
        st.markdown('### Висновок:')
        st.write("Графік показує середнє значення subscription_age для кожного значення bill_avg (обмежено діапазоном 0–150). Затінена область навколо лінії — це 95% довірчий інтервал, обчислений методом бутстрепінгу. У діапазоні bill_avg від 0 до ~150, де зосереджена переважна більшість клієнтів, середня тривалість підписки коливається приблизно між 1.5 та 5.5 роками, без чіткого монотонного зв'язку між сумою рахунку та тривалістю підписки — тобто клієнти з різними тарифами затримуються в компанії приблизно однаково довго. Після позначки bill_avg ≈ 150 лінія стає різкою та нестабільною, а довірчий інтервал — значно ширшим. Це не відображає реальну закономірність, а є артефактом малої вибірки: лише 93 з 72,274 клієнтів (0.13%) мають bill_avg вище 150, тому середнє значення стає надзвичайно чутливим до окремих викидів.")


    case "6. Відтік та збої послуг":
        feature_column_sv = 'service_failure_count'

        feature_presence_labels_sv = ['Мали сервісні збої','Не мали сервісних збоїв']

        customer_status_labels_sv = ['Пішли','Залишилися активними']
        
        title_all_customers_sv = 'Сервісні збої серед усіх клієнтів'
        title_churned_customers_sv = 'Сервісні збої серед клієнтів, які пішли'
        
        title_churn_rate_with_feature_sv = 'Пішли чи залишилися: клієнти із сервісними збоями'
        title_churn_rate_without_feature_sv = 'Пішли чи залишилися: клієнти без сервісних збоїв'


        result_sv = show_all_churn_piecharts(df,feature_column_sv,feature_presence_labels_sv,customer_status_labels_sv,title_all_customers_sv,title_churned_customers_sv,title_churn_rate_with_feature_sv,title_churn_rate_without_feature_sv)

        st.title('Графіки залежності відтоку клієнтів від кількості збоїв у наданні послуг')
        st.pyplot(result_sv)
        st.markdown('### Висновок:')
        st.write("Перші два графіки показують, що поширеність збоїв у наданні послуг є майже однаковою як серед усіх клієнтів, так і серед тих, хто відмовився від послуг: 16,42 % усіх клієнтів та 16,69 % клієнтів, які відмовилися від послуг, стикалися принаймні з одним збоєм у наданні послуг. Третій і четвертий графіки показують, що показники відтоку клієнтів також дуже схожі між цими двома групами: 56,34% серед клієнтів, які стикалися з перебоями в наданні послуг, проти 55,23% серед клієнтів, які цього не зазнали. Отже, виходячи з цих результатів, істотної різниці в рівні відтоку клієнтів між тими, хто стикався з перебоями в наданні послуг, та тими, хто не стикався, немає. Хоча більше половини клієнтів, які стикалися з перебоями в наданні послуг, зрештою відтоку (56,34 %), дуже схожа частка клієнтів, які не стикалися з такими перебоями, також відтоку (55,23 %). Отже, самі по собі ці результати не дають переконливих доказів того, що перебої в наданні послуг пов’язані з вищим ризиком відтоку клієнтів.")

        min_service_failure = float(df['service_failure_count'].min())
        max_service_failure = float(df['service_failure_count'].max())
        column_service_failure = 'service_failure_count'
        service_failure_interval = 1
        service_failure_procedural_slip = 1

        necessary_service_dict = get_churn_distribution(df, min_service_failure, max_service_failure,column_service_failure,service_failure_interval,service_failure_procedural_slip)
        service_failure_list,churn_quantity_list_f = return_results_as_lists(min_service_failure, max_service_failure,column_service_failure, necessary_service_dict,service_failure_interval,service_failure_procedural_slip)

        service_failure_title = 'Кількість відтоку від кількості збоїв'
        x_service_failure = 'Кількість збоїв'
        
        table_height_service_failure = 1
        final_service_failure_graph = show_graph_and_table_churns(churn_quantity_list_f, service_failure_list,service_failure_title,x_service_failure, table_height_service_failure) 
        final_service_failure_graph
        st.pyplot(final_service_failure_graph)

    case "7. Відтік клієнтів із чинними контрактами":
        ...
    case "8. Download/Upload та відтік":
        ...

    case "9. Перевищення ліміту Download та відтік":
        ...

    case "10. Кореляція між ознаками":
        ...
    




