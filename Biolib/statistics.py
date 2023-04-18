"""
File: statistics.py
Description: 
Date: 2022/1/10
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import warnings
import pandas as pd


def display_set(decimal: int = 2):
    warnings.filterwarnings("ignore")
    pd.set_option('display.float_format', lambda x: f'%.{decimal}f' % x)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_columns', None)
    # pd.set_option('display.max_rows', None)


def read_in_gene_expression_as_dataframe(gene_exp_file: str):
    function_dict = {'txt': pd.read_table, 'xlsx': pd.read_excel, 'xls': pd.read_excel, 'csv': pd.read_csv}
    df = function_dict[gene_exp_file.split('.')[-1]](gene_exp_file, index_col=0)
    return df


def merge_duplicate_indexes(data_frame: pd.DataFrame) -> pd.DataFrame:
    """Sums the column values of rows with the same index"""
    index_name = data_frame.index.name
    data_frame = data_frame.groupby(index_name).sum()
    return data_frame


def filter_by_min_value(data_frame: pd.DataFrame, min_value: float, start_column_num: int = 1,
                        end_column_num: int = None) -> pd.DataFrame:
    """Delete rows where all column values are less than the specified value"""
    if end_column_num is None:
        data_frame = data_frame[~(data_frame.iloc[:, start_column_num - 1:] <= min_value).all(axis=1)]
        return data_frame
    else:
        data_frame = data_frame[~(data_frame.iloc[:, start_column_num - 1:end_column_num - 1] <= min_value).all(axis=1)]
        return data_frame
