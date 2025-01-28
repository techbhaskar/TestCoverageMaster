import streamlit as st
import plotly.graph_objects as go
from typing import Dict


def display_coverage(coverage: Dict):
    """
    Display code coverage information using a gauge chart.
    """
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=coverage['coverage_percentage'],
            domain={
                'x': [0, 1],
                'y': [0, 1]
            },
            title={'text': "Code Coverage"},
            gauge={
                'axis': {
                    'range': [None, 100],
                    'tickwidth': 1,
                    'tickcolor': "darkblue"
                },
                'bar': {'color': "royalblue"},
                'steps': [
                    {'range': [0, 30], 'color': "#FF4136"},  # Critical - Red
                    {'range': [30, 50], 'color': "#FF851B"},  # Warning - Orange
                    {'range': [50, 70], 'color': "#FFDC00"},  # Caution - Yellow
                    {'range': [70, 85], 'color': "#2ECC40"},  # Good - Light Green
                    {'range': [85, 100], 'color': "#01FF70"}  # Excellent - Bright Green
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 3},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
    
    # Update layout for better appearance
    fig.update_layout(
        font={'color': "darkblue", 'family': "Arial"},
        height=400,
        margin=dict(l=10, r=10, t=40, b=10)
    )

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
    values = [
        coverage['tested_functions'],
        coverage['total_functions'] - coverage['tested_functions']
    ]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(title_text='Functional Test Coverage')

    st.plotly_chart(fig)

    st.write(f"Total Functions: {coverage['total_functions']}")
    st.write(f"Tested Functions: {coverage['tested_functions']}")
    st.write(f"Coverage Percentage: {coverage['coverage_percentage']:.2f}%")
