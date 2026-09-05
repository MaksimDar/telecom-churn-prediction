import matplotlib.pyplot as plt

def show_graph_and_table_churns(churn_list: list,input_list: list, title:str,x_label:str,table_height: float = 1.4) -> None:
    total_churn = sum(churn_list)
    cell_text = [['%1.2f' % ((x / total_churn) * 100)] for x in churn_list]

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(input_list,churn_list)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel('Кількість відтоку')
        
    the_table = ax.table(cellText=cell_text,rowLabels=input_list,colLabels=['Відтік y %'], loc='left',bbox=[-0.45, 0, 0.2, table_height] )
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(10)
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(10)

    return fig