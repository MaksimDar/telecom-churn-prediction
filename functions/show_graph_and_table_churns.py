import matplotlib.pyplot as plt

def show_graph_and_table_churns(churn_list: list,input_list: list, title:str,x_label:str,table_height: float = 1.4) -> None:
    total_churn = sum(churn_list)
    cell_text = [['%1.2f' % ((x / total_churn) * 100)] for x in churn_list]

    plt.figure(figsize=(9, 5))
    plt.plot(input_list,churn_list)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel('Кількість відтоку')
        
    the_table = plt.table(cellText=cell_text,rowLabels=input_list,colLabels=['Відтік y %'], loc='left',bbox=[-0.45, 0, 0.2, table_height] )
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(10)
    plt.show()