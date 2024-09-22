import streamlit as st
import plotly.graph_objects as go
from typing import Dict

def display_coverage(coverage: Dict):
    """
    Display code coverage information using a gauge chart.
    """
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = coverage['coverage_percentage'],
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Code Coverage"},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps' : [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 75], 'color': "gray"},
                {'range': [75, 100], 'color': "darkgray"}
            ],
            'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 90}
        }
    ))
    
    st.plotly_chart(fig)
    
    st.write(f"Total Lines: {coverage['total_lines']}")
    st.write(f"Covered Lines: {coverage['covered_lines']}")

def display_test_quality(quality: Dict):
    """
    Display test quality information using a bar chart.
    """
    fig = go.Figure(data=[
        go.Bar(name='Count', x=list(quality.keys()), y=list(quality.values()))
    ])
    
    fig.update_layout(title_text='Test Quality Metrics')
    st.plotly_chart(fig)

def display_functional_coverage(coverage: Dict):
    """
    Display functional test coverage information using a pie chart.
    """
    labels = ['Tested', 'Untested']
    values = [coverage['tested_functions'], coverage['total_functions'] - coverage['tested_functions']]
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(title_text='Functional Test Coverage')
    
    st.plotly_chart(fig)
    
    st.write(f"Total Functions: {coverage['total_functions']}")
    st.write(f"Tested Functions: {coverage['tested_functions']}")
    st.write(f"Coverage Percentage: {coverage['coverage_percentage']:.2f}%")
