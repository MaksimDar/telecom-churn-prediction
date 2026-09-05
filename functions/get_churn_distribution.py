def get_churn_distribution(data_structure,min_value, max_value,column_comparison, interval,procedural_slip) -> dict:
    """ 
    Українська версія: Функція обчислює кількість випадків відтоку для кожного кроку в заданій колонці набору даних 
    і повертає словник, що містить набір записів по кроках, кожен з яких містить інтервал колонки та відповідну кількість відтоку.

    English version: The function calculates the quantity of churns per step in a given dataset column, 
    and returns a dictionary containing a set of step-level entries, each with the column interval and 
    the corresponding churn quantity.
    """
    dict_values = {}

    previous_ind = 0
    attempt = 0
    i = min_value
    
    while (i <= max_value + procedural_slip):
    
        if attempt == 0:
            column_value = i
            churn_quantity = data_structure.loc[data_structure[column_comparison] <= i, 'churn'].sum()
            attempt = 1
        else:
            column_value = i
            churn_quantity = data_structure.loc[(data_structure[column_comparison] > previous_ind) & (data_structure[column_comparison] <= i), 'churn'].sum()
            
        list_values = {}
        final_result = {f'{column_comparison}': column_value, 'churn_quantity': churn_quantity}
        dict_values[f'{i}_step:'] = final_result
        previous_ind = i
        i += interval
        
    return dict_values