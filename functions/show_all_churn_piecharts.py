import matplotlib.pyplot as plt
import streamlit as st

def show_all_churn_piecharts(data_structure, request_column: str, usage_labels: list, churn_labels:list, all_title: str, churns_title: str, with_churns_title: str,without_churns_title: str) -> None:
    """
    Українська версія:
    Будує чотири графіки для заданої ознаки (`request_column`):

    1. Використання ознаки серед УСІХ клієнтів. Показує, який відсоток усіх клієнтів мав ненульове значення
       заданої ознаки, а який — не мав.

    2. Використання ознаки серед КЛІЄНТІВ, ЯКІ ПІШЛИ. Показує, який відсоток клієнтів, що пішли, мав ненульове значення 
       заданої ознаки, а який — не мав. Тобто графік показує структуру групи клієнтів, які пішли. 
       Він НЕ показує, що ця ознака була причиною відтоку.

    3. Рівень відтоку серед клієнтів, ЯКІ МАЛИ ознаку. Показує, який відсоток клієнтів із ненульовим значенням
       заданої ознаки пішов, а який залишився активним.

    4. Рівень відтоку серед клієнтів, ЯКІ НЕ МАЛИ ознаки. Показує, який відсоток клієнтів із нульовим значенням 
       заданої ознаки пішов, а який залишився активним.
    
    English version: 
    Builds four pie charts for the specified feature (`request_column`):

    1. Feature usage among ALL customers. Shows what percentage of all customers had a non-zero value
       in the specified feature and what percentage did not.

    2. Feature usage among CHURNED customers. Shows what percentage of customers who churned had a non-zero value 
       in the specified feature and what percentage did not. This describes the composition of the churned group.
       It does NOT show that the feature caused the churn.

    3. Churn rate among customers WITH the feature. Shows what percentage of customers who had a non-zero value
       in the specified feature churned and what percentage remained active.

    4. Churn rate among customers WITHOUT the feature. Shows what percentage of customers who had a zero value
   in the specified feature churned and what percentage remained active.
    """

    customers_with_feature = (data_structure[request_column] > 0).sum()
    customers_without_feature = (data_structure[request_column] == 0).sum()
    
    churned_with_feature = data_structure[data_structure[request_column] > 0]['churn'].sum()
    churned_without_feature = data_structure[data_structure[request_column] == 0]['churn'].sum()

    active_with_feature = customers_with_feature - churned_with_feature
    active_without_feature = customers_without_feature - churned_without_feature

    fig, axs = plt.subplots(2, 2, figsize=(14,9))
    axs = axs.flatten()

    data_all = [customers_with_feature, customers_without_feature]
    axs[0].set_title(all_title)
    axs[0].pie(data_all,labels=usage_labels,autopct="%.2f%%",colors=['Teal','Salmon'],shadow=False, labeldistance=1.1, startangle=0, radius=1)

    data_churns = [churned_with_feature, churned_without_feature]
    axs[1].set_title(churns_title)
    axs[1].pie(data_churns,labels=usage_labels,autopct="%.2f%%",colors=['green','orange'],shadow=False, labeldistance=1.1, startangle=0, radius=1)

    customers_with_the_feature = [churned_with_feature, active_with_feature]
    axs[2].set_title(with_churns_title)
    axs[2].pie(customers_with_the_feature,labels=churn_labels,autopct="%.2f%%",colors=['green','orange'],shadow=False, labeldistance=1.1, startangle=0, radius=1)

    customers_without_the_feature = [churned_without_feature, active_without_feature]
    axs[3].set_title(without_churns_title)
    axs[3].pie(customers_without_the_feature,labels=churn_labels,autopct="%.2f%%",colors=['Teal','Salmon'],shadow=False, labeldistance=1.1, startangle=0, radius=1)
    plt.subplots_adjust(hspace=0.4, wspace=0.3)
    return fig