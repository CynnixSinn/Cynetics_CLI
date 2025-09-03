import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from typing import Dict, Any, List
from cynetics.tools.base import BaseTool

class DataAnalysisTool(BaseTool):
    """A tool for analyzing and visualizing data."""
    
    def __init__(self):
        super().__init__(
            name="data_analysis",
            description="Analyze and visualize data from various sources."
        )
    
    def run(self, data: Any = None, file_path: str = None, action: str = "summary", 
            columns: List[str] = None, plot_type: str = "bar") -> Dict[str, Any]:
        """Analyze data and generate insights.
        
        Args:
            data: Raw data (list of dicts, DataFrame, etc.)
            file_path: Path to a data file (CSV, Excel, etc.)
            action: Type of analysis ('summary', 'correlation', 'plot')
            columns: Specific columns to analyze
            plot_type: Type of plot to generate ('bar', 'line', 'scatter', 'hist')
            
        Returns:
            A dictionary with analysis results and/or visualizations.
        """
        try:
            # Load data
            if file_path:
                df = self._load_data_from_file(file_path)
            elif data is not None:
                df = self._convert_to_dataframe(data)
            else:
                return {
                    "status": "error",
                    "message": "Either 'data' or 'file_path' must be provided"
                }
            
            # Filter columns if specified
            if columns:
                df = df[columns]
            
            # Perform requested action
            if action == "summary":
                return self._generate_summary(df)
            elif action == "correlation":
                return self._generate_correlation(df)
            elif action == "plot":
                return self._generate_plot(df, plot_type)
            else:
                return {
                    "status": "error",
                    "message": f"Unknown action: {action}"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _load_data_from_file(self, file_path: str) -> pd.DataFrame:
        """Load data from a file."""
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith(('.xls', '.xlsx')):
            return pd.read_excel(file_path)
        elif file_path.endswith('.json'):
            return pd.read_json(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")
    
    def _convert_to_dataframe(self, data: Any) -> pd.DataFrame:
        """Convert various data formats to a DataFrame."""
        if isinstance(data, pd.DataFrame):
            return data
        elif isinstance(data, list):
            if all(isinstance(item, dict) for item in data):
                return pd.DataFrame(data)
            else:
                return pd.DataFrame(data)
        elif isinstance(data, dict):
            return pd.DataFrame(data)
        else:
            raise ValueError(f"Unsupported data format: {type(data)}")
    
    def _generate_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate a summary of the data."""
        summary = {
            "status": "success",
            "action": "summary",
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns),
            "data_types": df.dtypes.to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "basic_stats": {}
        }
        
        # Numeric columns summary
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            summary["basic_stats"] = df[numeric_cols].describe().to_dict()
        
        return summary
    
    def _generate_correlation(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate correlation matrix for numeric columns."""
        numeric_df = df.select_dtypes(include=['number'])
        if numeric_df.empty:
            return {
                "status": "error",
                "message": "No numeric columns found for correlation analysis"
            }
        
        correlation_matrix = numeric_df.corr()
        
        return {
            "status": "success",
            "action": "correlation",
            "correlation_matrix": correlation_matrix.to_dict(),
            "strong_correlations": self._find_strong_correlations(correlation_matrix)
        }
    
    def _find_strong_correlations(self, corr_matrix: pd.DataFrame, threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Find strong correlations in the matrix."""
        strong_corrs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) >= threshold:
                    strong_corrs.append({
                        "column1": corr_matrix.columns[i],
                        "column2": corr_matrix.columns[j],
                        "correlation": corr_value
                    })
        return strong_corrs
    
    def _generate_plot(self, df: pd.DataFrame, plot_type: str) -> Dict[str, Any]:
        """Generate a plot of the data."""
        try:
            # Create a plot
            plt.figure(figsize=(10, 6))
            
            if plot_type == "bar":
                # For bar plot, we'll use the first numeric column
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) == 0:
                    return {
                        "status": "error",
                        "message": "No numeric columns found for bar plot"
                    }
                df[numeric_cols[0]].plot(kind='bar')
                plt.title(f"Bar Plot of {numeric_cols[0]}")
            elif plot_type == "line":
                # For line plot, we'll use the first numeric column
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) == 0:
                    return {
                        "status": "error",
                        "message": "No numeric columns found for line plot"
                    }
                df[numeric_cols[0]].plot(kind='line')
                plt.title(f"Line Plot of {numeric_cols[0]}")
            elif plot_type == "scatter":
                # For scatter plot, we need at least two numeric columns
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) < 2:
                    return {
                        "status": "error",
                        "message": "At least two numeric columns needed for scatter plot"
                    }
                df.plot(kind='scatter', x=numeric_cols[0], y=numeric_cols[1])
                plt.title(f"Scatter Plot: {numeric_cols[0]} vs {numeric_cols[1]}")
            elif plot_type == "hist":
                # For histogram, we'll use the first numeric column
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) == 0:
                    return {
                        "status": "error",
                        "message": "No numeric columns found for histogram"
                    }
                df[numeric_cols[0]].plot(kind='hist')
                plt.title(f"Histogram of {numeric_cols[0]}")
            else:
                return {
                    "status": "error",
                    "message": f"Unsupported plot type: {plot_type}"
                }
            
            # Save plot to base64 string
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png')
            img_buffer.seek(0)
            img_str = base64.b64encode(img_buffer.read()).decode()
            plt.close()
            
            return {
                "status": "success",
                "action": "plot",
                "plot_type": plot_type,
                "plot_data": img_str,
                "message": "Plot generated successfully"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error generating plot: {str(e)}"
            }