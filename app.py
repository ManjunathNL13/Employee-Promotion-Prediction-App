import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from functions import input_data_to_prediction, promotion_percentage

import warnings
warnings.filterwarnings("ignore")


# Define the Streamlit app
def main():
    # app
    st.set_page_config(
        page_title="Employee Promotion Prediction App",
        page_icon="🧑‍💻")

    # add heading title
    title_style = """
    <style>
        h1 {
            color: rgb(255, 75, 75);
        }
    </style>
    """
    st.markdown(title_style, unsafe_allow_html=True)
    st.title("Employee Promotion Prediction App")
    st.markdown("<hr>", unsafe_allow_html=True)

    # add image
    st.image("https://images.shiksha.com/mediadata/images/1589449997phpxQRvIu.jpeg", caption='EPPA', use_container_width=True)

    # user inputs
    input_data = list()
    input_data.append(int(st.number_input("Employee ID:", min_value=0, value=0)))
    input_data.append(st.selectbox("Department:", options=[
        'Analytics', 'Finance', 'HR', 'Legal', 'Operations', 'Procurement', 'R&D',
        'Sales & Marketing', 'Technology'
         ]))
    input_data.append(st.selectbox("Region:", options=[
        'region_1', 'region_2', 'region_3', 'region_4', 'region_5', 'region_6', 'region_7',
        'region_8', 'region_9', 'region_10', 'region_11', 'region_12', 'region_13', 'region_14',
        'region_15', 'region_16', 'region_17', 'region_18', 'region_19', 'region_20', 'region_21',
        'region_22', 'region_23', 'region_24', 'region_25', 'region_26', 'region_27', 'region_28',
        'region_29', 'region_30', 'region_31', 'region_32', 'region_33', 'region_34'
    ]))
    input_data.append(st.selectbox("Education:", options=[
        "Below Secondary", "Bachelor's", "Master's & above"
    ]))
    input_data.append("m" if st.selectbox("Gender:", options=["Male", "Female"]) == "Male" else "f")
    input_data.append(st.selectbox("Recruitment Channel:", options=[
        "Sourcing", "Referred", "Other"
    ]).lower())
    input_data.append(int(st.number_input("No of Trainings:", min_value=0, value=0)))
    input_data.append(int(st.number_input("Age:", min_value=18, value=18)))
    input_data.append(float(st.slider("Previous Year Rating:", min_value=1, max_value=5, value=1)))
    input_data.append(int(st.number_input("Length of Service:", min_value=1, value=1)))
    input_data.append(1 if st.selectbox("Awards Won:", options=["Yes", "No"]) == "Yes" else 0)
    input_data.append(int(st.slider("Average Training Score: ", min_value=0, max_value=100, value=50)))

    st.write("Filter Analysis by:")
    col_d, col_r, col_rc = st.columns(3)

    with col_d:
        department = st.checkbox("department")

    with col_r:
        region = st.checkbox("region")

    with col_rc:
        recruitment_channel = st.checkbox("recruitment channel")


    st.markdown("<hr>", unsafe_allow_html=True)

    # prediction
    button_style = '''
    <style>
    .stButton>button {
        width: 150px;
        height: 60px;
    }
    </style>
    '''
    st.markdown(button_style, unsafe_allow_html=True)
    col1b, col2b = st.columns(2)
    with col1b:
            prediction = st.button("Predict")
    with col2b:
            if st.button('Reset'):
                st.rerun()
    
    if prediction:

        # results
        st.header("Results")

        result = input_data_to_prediction(input_data)
        if result == 1:
            st.success("Congratulations! you deserve promotion.")
        else:
            st.error("Sorry! you couldn't be promoted. You need to work harder to fulfill promotion criteria.")
        # defining and filtering dataframe
        df = pd.read_csv("datasets/train.csv")
        df = df.dropna()

        # filters\
        columns_to_filter = []

        if department:
            df = df[df['department'] == input_data[1]]

        if region:
            df = df[df['region'] == input_data[2]]

        if recruitment_channel:
            df = df[df['recruitment_channel'] == input_data[5]]

        # data visualization
        st.markdown(
            "<h2 style='text-align: center;'>Visualization</h2>",
            unsafe_allow_html=True
        )

        # first row
        col1, col2, col3 = st.columns(3)

        # education
        with col1:
            column = "education"
            df_for_plot = promotion_percentage(df, column)
            fig1, ax1 = plt.subplots()
            ax1.bar(df_for_plot[column], df_for_plot['percentage'], color=['tab:red' if df_for_plot[column][i] == input_data[3] else 'skyblue' for i in range(len(df_for_plot[column]))])
            ax1.set_xlabel(column)
            ax1.set_ylabel('Percentage of Promotion')
            ax1.set_title(f"Promotion by {column}")
            st.pyplot(fig1)

        # gender
        with col2:
            column = "gender"
            df_for_plot = promotion_percentage(df, column)
            fig2, ax2 = plt.subplots()
            ax2.bar(df_for_plot[column], df_for_plot['percentage'], color=['tab:red' if df_for_plot[column][i] == input_data[4] else 'skyblue' for i in range(len(df_for_plot[column]))])
            ax2.set_xlabel(column)
            ax2.set_ylabel('Percentage of Promotion')
            ax2.set_title(f"Promotion by {column}")
            st.pyplot(fig2)

        # no_of_trainings
        with col3:
            column = "no_of_trainings"
            df_for_plot = promotion_percentage(df, column)
            fig3, ax3 = plt.subplots()
            ax3.bar(df_for_plot[column], df_for_plot['percentage'], color=['tab:red' if df_for_plot[column][i] == input_data[6] else 'skyblue' for i in range(len(df_for_plot[column]))])
            ax3.set_xlabel(column)
            ax3.set_ylabel('Percentage of Promotion')
            ax3.set_title(f"Promotion by {column}")
            st.pyplot(fig3)

        # age
        column = "age"
        plt.figure(figsize=(20, 6))
        df_for_plot = promotion_percentage(df, column)
        plt.plot(df_for_plot[column], df_for_plot['percentage'], color="skyblue")
        plt.scatter(df_for_plot[column], df_for_plot['percentage'], color=['red' if df_for_plot[column][i] == input_data[7] else 'skyblue' for i in range(len(df_for_plot[column]))])
        plt.xlabel(column)
        plt.ylabel('%')
        plt.title(f"Promotion by {column}")
        st.pyplot(plt)

        col4, col5 = st.columns(2)

        # education
        with col4:
            column = "previous_year_rating"
            df_for_plot = promotion_percentage(df, column)
            fig4, ax4 = plt.subplots()
            ax4.bar(df_for_plot[column], df_for_plot['percentage'], color=['tab:red' if df_for_plot[column][i] == input_data[8] else 'skyblue' for i in range(len(df_for_plot[column]))])
            ax4.set_xlabel(column)
            ax4.set_ylabel('Percentage of Promotion')
            ax4.set_title(f"Promotion by {column}")
            st.pyplot(fig4)

        # gender
        with col5:
            column = "awards_won?"
            df_for_plot = promotion_percentage(df, column)
            fig5, ax5 = plt.subplots()
            ax5.bar(df_for_plot[column], df_for_plot['percentage'], color=['tab:red' if df_for_plot[column][i] == input_data[10] else 'skyblue' for i in range(len(df_for_plot[column]))])
            ax5.set_xlabel(column)
            ax5.set_ylabel('Percentage of Promotion')
            ax5.set_title(f"Promotion by {column}")
            st.pyplot(fig5)

        # length_of_service
        column = "length_of_service"
        plt.figure(figsize=(20, 6))
        df_for_plot = promotion_percentage(df, column)
        plt.plot(df_for_plot[column], df_for_plot['percentage'], color='skyblue')
        plt.scatter(df_for_plot[column], df_for_plot['percentage'], color=['tab:red' if df_for_plot[column][i] == input_data[9] else 'skyblue' for i in range(len(df_for_plot[column]))])
        plt.xlabel(column)
        plt.ylabel('%')
        plt.title(f"Promotion by {column}")
        st.pyplot(plt)

        # avg_training_score
        column = "avg_training_score"
        plt.figure(figsize=(20, 6))
        df_for_plot = promotion_percentage(df, column)
        plt.plot(df_for_plot[column], df_for_plot['percentage'], color='skyblue')
        plt.scatter(df_for_plot[column], df_for_plot['percentage'], color=['tab:red' if df_for_plot[column][i] == input_data[11] else 'skyblue' for i in range(len(df_for_plot[column]))])
        plt.xlabel(column)
        plt.ylabel('%')
        plt.title(f"Promotion by {column}")
        st.pyplot(plt)


if __name__ == '__main__':
    main()