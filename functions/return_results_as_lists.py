def return_results_as_lists(min_value, max_value, column_comparison, dictionary,interval,procedural_slip):
    """ 
    Українська версія: Функція повертає два списки для спрощення подальших обчислень або графічного представлення 
    залежності між інтервалами колонки та кількістю відтоку.
    
    English version: The function returns two lists for simpler further calculations or graphical representation 
    of the relationship between column intervals and churn quantity.
    """ 
    i = min_value
    list_column_values = []
    list_churn_quantity = []
    
    while (i <= max_value + procedural_slip):
        list_column_values.append(dictionary[f'{i}_step:'][column_comparison])
        list_churn_quantity.append(dictionary[f'{i}_step:']['churn_quantity'])
        i += interval
        
    return list_column_values,list_churn_quantity