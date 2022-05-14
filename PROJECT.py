import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from streamlit_echarts import st_echarts


def intro():
    st.header("Student Alcohol Consumption")
    st.subheader("Social, gender and study data from secondary school students")
    st.info("Анализ данных, полученных при опросе учащихся двух португальских школ. Датасет содержит информацию"
            "об успеваемости, семейном положении, возрасте и потреблении алкоголя учащимися.")
if __name__ == "__main__" :
    intro()

with st.echo(code_location='below'):
    @st.experimental_singleton()

    def get_file():
        return pd.read_csv('student-mat.csv')
    df=get_file()
    st.dataframe(df)

    df_age_alco=df.groupby('age', as_index=False).agg({'Walc':'mean', 'Dalc':'mean'})

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_age_alco['age'], y=df_age_alco['Walc'], name='Weekend'))
    fig.add_trace(go.Bar(x=df_age_alco['age'], y=df_age_alco['Dalc'], name='Workday'))
    fig.update_layout(legend_title_text="Days", title="Потребление алкоголя в зависимости от возраста "
                                                      "(1-очень мало, 5-очень много)")
    fig.update_xaxes(title_text="Age")
    fig.update_yaxes(title_text="Alcohol consumption")
    st.plotly_chart(fig)
    st.write("По графику видно, что среди людей до 20 лет большая часть потребляемого "
             "алкоголя приходится на группу восемнадцатилетних. Это связано, в первоую очередь, "
             "с тем, что в это время многие португальские подростки выпускаются из "
             "школы и физически сепарируются от родителей. Так как в португалии нет возрастного "
             "ограничения на продажу и покупку алкоголя, потребление более юными подростками "
             "алкогольной продукции ненулевое.")

    df_alco_abs = df.groupby('Dalc', as_index=False).agg({'studytime': 'mean', 'absences': 'mean'})

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_alco_abs['Dalc'], y=df_alco_abs['absences'], name='Absences'))
    fig.add_trace(go.Bar(x=df_alco_abs['Dalc'], y=df_alco_abs['studytime'], name='Study time'))
    fig.update_layout(title="Время, потраченное на учёбу и пропуски занятий без уважительной причины")
    fig.update_xaxes(title_text="Workday alcohol consumption")
    fig.update_yaxes(title_text="Study time(hours)/Absences")
    st.plotly_chart(fig)
    st.write("Как можно наблюдать, с ростом потребления алкоголя растет количество "
             "пропусков учебы без уважительной причины. Количество времени, "
             "потраченного на учебу, отрицательно зависит от количества потребляемого "
             "алкоголя в рабочие дни, однако ависимость выражена не очень ярко.")

    alco_health = df[["Walc","health"]]
    high_alco_health = alco_health[alco_health['Walc'] == 5]
    health = high_alco_health['health'].value_counts()

    health1 = str(health[1])
    health2 = str(health[2])
    health3 = str(health[3])
    health4 = str(health[4])
    health5 = str(health[5])

    options = {
        "tooltip": {"trigger": "item"},
        "legend": {"top": "1%", "left": "center"},
        "series": [
            {"name": "Оценка здоровья", "type": "pie", "radius": ["30%", "70%"],
            "avoidLabelOverlap": False,
            "itemStyle": {"borderRadius": 15,
            "borderColor": "#fff",
            "borderWidth": 3},
            "label": {"show": False, "position": "center"},
            "emphasis": {"label": {"show": True, "fontSize": "40", "fontWeight": "bold"}},
            "labelLine": {"show": False},
            "data": [{"value": health1, "name": "Очень плохо"},
                     {"value": health2, "name": "Плохо"},
                     {"value": health3, "name": "Удовлетворительно"},
                     {"value": health4, "name": "Хорошо"},
                     {"value": health5, "name": "Отлично"}]}]}

    st_echarts(
        options=options, height="500px",
    )

    st.write("Как можно заметить по ответам респондентов, употребляющих наибольшее количество алкоголя, "
             "большое количество алкоголя, по их оценке, не ухудшает здоровье.")








