"""
Visualization functions for the UCI Air Quality Dataset.

This module contains functions for creating charts and plots
to visualize air quality data patterns and relationships.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st


def plot_co_over_time(df, title="CO(GT) Concentration Over Time"):
    """
    Create a line plot showing CO concentration over time.
    
    Args:
        df (pd.DataFrame): Cleaned dataset with DateTime column
        title (str): Chart title
        
    Returns:
        matplotlib.figure.Figure: The plot figure
    """
    if df is None or 'CO(GT)' not in df.columns:
        return None
    
    # Filter out missing values
    plot_data = df[['DateTime', 'CO(GT)']].dropna()
    
    # Additional filter to remove NaT values from DateTime
    plot_data = plot_data[plot_data['DateTime'].notna()]
    
    if plot_data.empty:
        return None
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(plot_data['DateTime'], plot_data['CO(GT)'], 
            linewidth=1, alpha=0.7, color='#2E8B57')
    
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('CO(GT) Concentration (mg/m³)', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return fig


def plot_temperature_vs_humidity(df, title="Temperature vs Absolute Humidity"):
    """
    Create a scatter plot showing relationship between temperature and absolute humidity.
    
    Args:
        df (pd.DataFrame): Cleaned dataset
        title (str): Chart title
        
    Returns:
        matplotlib.figure.Figure: The plot figure
    """
    if df is None or 'T' not in df.columns or 'AH' not in df.columns:
        return None
    
    # Filter out missing values
    plot_data = df[['T', 'AH']].dropna()
    
    if plot_data.empty:
        return None
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    scatter = ax.scatter(plot_data['T'], plot_data['AH'], 
                        alpha=0.6, c=plot_data['T'], 
                        cmap='viridis', s=20)
    
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel('Temperature (°C)', fontsize=12)
    ax.set_ylabel('Absolute Humidity', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Temperature (°C)', fontsize=10)
    
    plt.tight_layout()
    
    return fig


def plot_pollutant_distribution(df, pollutant='CO(GT)', title=None):
    """
    Create a histogram showing the distribution of a pollutant.
    
    Args:
        df (pd.DataFrame): Cleaned dataset
        pollutant (str): Name of the pollutant column
        title (str): Chart title
        
    Returns:
        matplotlib.figure.Figure: The plot figure
    """
    if df is None or pollutant not in df.columns:
        return None
    
    # Filter out missing values
    plot_data = df[pollutant].dropna()
    
    if plot_data.empty:
        return None
    
    if title is None:
        title = f"Distribution of {pollutant}"
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.hist(plot_data, bins=50, alpha=0.7, color='#FF6B6B', edgecolor='black')
    
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel(f'{pollutant} Concentration', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Add statistics text
    mean_val = plot_data.mean()
    median_val = plot_data.median()
    ax.axvline(mean_val, color='red', linestyle='--', 
               label=f'Mean: {mean_val:.2f}')
    ax.axvline(median_val, color='blue', linestyle='--', 
               label=f'Median: {median_val:.2f}')
    ax.legend()
    
    plt.tight_layout()
    
    return fig


def plot_correlation_heatmap(df, title="Air Quality Variables Correlation"):
    """
    Create a correlation heatmap for numeric variables.
    
    Args:
        df (pd.DataFrame): Cleaned dataset
        title (str): Chart title
        
    Returns:
        matplotlib.figure.Figure: The plot figure
    """
    if df is None:
        return None
    
    # Select only numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if len(numeric_cols) < 2:
        return None
    
    # Calculate correlation matrix
    corr_matrix = df[numeric_cols].corr()
    
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Create heatmap
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                square=True, fmt='.2f', cbar_kws={'shrink': 0.8})
    
    ax.set_title(title, fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    return fig


def plot_daily_averages(df, pollutant='CO(GT)', title=None):
    """
    Create a line plot showing daily averages of a pollutant.
    
    Args:
        df (pd.DataFrame): Cleaned dataset
        pollutant (str): Name of the pollutant column
        title (str): Chart title
        
    Returns:
        matplotlib.figure.Figure: The plot figure
    """
    if df is None or pollutant not in df.columns:
        return None
    
    # Calculate daily averages
    daily_avg = df.groupby('Date')[pollutant].mean().reset_index()
    
    if daily_avg.empty:
        return None
    
    if title is None:
        title = f"Daily Average {pollutant} Concentration"
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(daily_avg['Date'], daily_avg[pollutant], 
            linewidth=2, marker='o', markersize=3, color='#4A90E2')
    
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel(f'Average {pollutant} Concentration', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Rotate x-axis labels
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return fig


def plot_multiple_pollutants(df, pollutants=None, title="Multiple Pollutants Over Time"):
    """
    Create a multi-line plot showing multiple pollutants over time.
    
    Args:
        df (pd.DataFrame): Cleaned dataset
        pollutants (list): List of pollutant column names
        title (str): Chart title
        
    Returns:
        matplotlib.figure.Figure: The plot figure
    """
    if df is None:
        return None
    
    if pollutants is None:
        pollutants = ['CO(GT)', 'NOx(GT)', 'NO2(GT)']
    
    # Filter pollutants that exist in the dataset
    available_pollutants = [p for p in pollutants if p in df.columns]
    
    if not available_pollutants:
        return None
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    colors = ['#2E8B57', '#FF6B6B', '#4A90E2', '#FFD93D', '#6A5ACD']
    
    for i, pollutant in enumerate(available_pollutants):
        plot_data = df[['DateTime', pollutant]].dropna()
        # Additional filter to remove NaT values from DateTime
        plot_data = plot_data[plot_data['DateTime'].notna()]
        if not plot_data.empty:
            ax.plot(plot_data['DateTime'], plot_data[pollutant], 
                   label=pollutant, linewidth=1.5, alpha=0.8,
                   color=colors[i % len(colors)])
    
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Concentration', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Rotate x-axis labels
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return fig


def plot_nox_vs_sensor(df, title="NOx(GT) vs Sensor Reading"):
    """
    Create a scatter plot showing relationship between NOx(GT) and PT08.S3(NOx) sensor reading.
    
    Args:
        df (pd.DataFrame): Cleaned dataset
        title (str): Chart title
        
    Returns:
        matplotlib.figure.Figure: The plot figure
    """
    if df is None or 'NOx(GT)' not in df.columns or 'PT08.S3(NOx)' not in df.columns:
        return None
    
    # Filter out missing values
    plot_data = df[['NOx(GT)', 'PT08.S3(NOx)']].dropna()
    
    if plot_data.empty:
        return None
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    scatter = ax.scatter(plot_data['NOx(GT)'], plot_data['PT08.S3(NOx)'], 
                        alpha=0.6, c=plot_data['NOx(GT)'], 
                        cmap='Reds', s=20)
    
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel('NOx(GT) Concentration (µg/m³)', fontsize=12)
    ax.set_ylabel('PT08.S3(NOx) Sensor Reading', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('NOx(GT) Concentration (µg/m³)', fontsize=10)
    
    plt.tight_layout()
    
    return fig


def create_summary_metrics_display(metrics):
    """
    Create a formatted display of key metrics for Streamlit.
    
    Args:
        metrics (dict): Air quality metrics from analysis.py
        
    Returns:
        dict: Formatted metrics for display
    """
    if not metrics:
        return {}
    
    display_metrics = {}
    
    # Format CO metrics
    if 'co' in metrics:
        co_metrics = metrics['co']
        display_metrics['CO Concentration'] = {
            'Average': f"{co_metrics['mean']:.2f} mg/m³",
            'Maximum': f"{co_metrics['max']:.2f} mg/m³",
            'Minimum': f"{co_metrics['min']:.2f} mg/m³"
        }
    
    # Format Temperature metrics
    if 'temperature' in metrics:
        temp_metrics = metrics['temperature']
        display_metrics['Temperature'] = {
            'Average': f"{temp_metrics['mean']:.1f} °C",
            'Maximum': f"{temp_metrics['max']:.1f} °C",
            'Minimum': f"{temp_metrics['min']:.1f} °C"
        }
    
    # Format Humidity metrics
    if 'humidity' in metrics:
        rh_metrics = metrics['humidity']
        display_metrics['Relative Humidity'] = {
            'Average': f"{rh_metrics['mean']:.1f}%",
            'Maximum': f"{rh_metrics['max']:.1f}%",
            'Minimum': f"{rh_metrics['min']:.1f}%"
        }
    
    return display_metrics
