import streamlit as st
from src.visualization import VisualizationUtils
from src.perform_database_operations import perform_database_operations

def plot(data_file, sat_file, visualize):
    metric_options = ["User Analysis", "Engagement Analysis", "Satisfaction Analysis"]
    selected_metric = st.sidebar.selectbox("Select Metrics for Visualization", metric_options)
    
    if selected_metric == 'User Analysis':
        st.header('User Analysis')
        user_data = data_file.groupby('IMSI')
        user_analysis = {
            'Top 10 Session Duration per User': (user_data['Dur. (ms)'].sum() / 1000).sort_values(ascending=False).head(10),
            'Top 10 Total Download (DL) (Bytes) per User': user_data['Total DL (Bytes)'].sum().sort_values(ascending=False).head(10),
            'Top 10 Total Upload (UL) (Bytes) per User': user_data['Total UL (Bytes)'].sum().sort_values(ascending=False).head(10)
        }
        for plot_title, plot_data in user_analysis.items():
            st.subheader(plot_title)
            fig = visualize.plot_bar(plot_data, xlabel="User", ylabel=f"{' '.join(plot_title.split()[2:-2])}", title=plot_title)
            st.pyplot(fig)
    
    elif selected_metric == 'Engagement Analysis':
        st.header('Engagement Analysis')
        engagement_metrics = data_file.groupby('MSISDN/Number').agg({
            'Bearer Id': 'count',
            'Dur. (ms)': 'sum',
            'Total DL (Bytes)': 'sum',
            'Total UL (Bytes)': 'sum'
        })
        engagement_analysis = {
            'Top 10 Session Frequency per Customer': engagement_metrics['Bearer Id'].nlargest(10),
            'Top 10 Session Duration per Customer': engagement_metrics['Dur. (ms)'].nlargest(10),
            'Top 10 Total Traffic per Customer': (engagement_metrics['Total DL (Bytes)'] + engagement_metrics['Total UL (Bytes)']).nlargest(10)
        }
        for plot_title, plot_data in engagement_analysis.items():
            st.subheader(plot_title)
            fig = visualize.plot_bar(plot_data, xlabel="Customer", ylabel=f"{' '.join(plot_title.split()[2:-2])}", title=plot_title)
            st.pyplot(fig)
    
    elif selected_metric == 'Satisfaction Analysis':
        st.header('Satisfaction Analysis')
        satisfaction_analysis = {
            'Top 10 Satisfied Customer': sat_file['satisfactory_score'].nlargest(10)
        }
        for plot_title, plot_data in satisfaction_analysis.items():
            st.subheader(plot_title)
            fig = visualize.plot_bar(plot_data, xlabel="Customer", ylabel=f"{' '.join(plot_title.split()[2:])}", title=plot_title)
            st.pyplot(fig)

if __name__ == "__main__":
    st.title('TellCo Dashboard')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    
    try:
        config_file_path = 'config_database.json'
        database_name = 'telecom'
        sat_query = 'SELECT * FROM satisfaction_table' 
        data_query = 'SELECT * FROM xdr_data' 
        data_file = perform_database_operations(config_file_path, database_name, data_query)
        sat_file = perform_database_operations(config_file_path, database_name, sat_query)
        visualize = VisualizationUtils()
        plot(data_file, sat_file, visualize)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
