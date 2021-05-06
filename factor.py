# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 18:13:34 2021

@author: Hari Ravichandran
"""
import pandas as pd
import unittest
from pandas.util.testing import assert_frame_equal


class Factor:
    # Attribute df -> contains pandas dataframe with relevant tables
    
    # Upon initialization, specify either csv file path (string), pandas dataframe, or no argument
    def __init__(self, *args):
        if len(args) == 0:  # Argument does not exist -> empty dataframe
            raise ValueError("Error - No Arguments Provided for Factor Initialization")
        elif isinstance(args[0], str):  # Argument is string -> load from csv (filename or path)
            self.df = pd.read_csv(args[0])
        elif isinstance(args[0], pd.DataFrame):   # Argument is dataframe -> new factor using dataframe
            self.df = args[0]
        else:
            raise ValueError("Error - Invalid Arguments for Factor Initialization")
    
    # Saves the data in the factor to a CSV file
    def save(self, csv_filename: str):
        self.df.to_csv(csv_filename, index=False)  # skip index
    
    # Returns data in dataframe format - included for testing purposes
    def get_data(self):
        return self.df
    
    # Prints head of self.df, nrows is the number of rows to print
    def print_data(self, nrows=5):
        print(self.df.head(nrows))     
        
    # Returns a set with the variables in the factor
    def get_vars(self):
        return set(self.df.columns.tolist()[:-1])  # Remove last column, which is always 'Value'
        
    # Completes the summing-out operation, only works on one variable at a time
    # 'variableOfInterest' imported as string - variable to sum over
    # O(1) time complexity
    def summation(self, variableOfInterest: str):
        df1 = self.df  # make copy of df
        column_list = df1.columns.tolist()  # get list of all columns
        
        # Remove 'Value' and variableOfInterest from desired column list
        column_list.remove('Value')
        column_list.remove(variableOfInterest)
        
        # Drop variable of interest from dataframe
        df1 = df1.drop(columns=variableOfInterest)
        
        # Group by variables remaining, and aggregate to sum
        aggregation_functions = {'Value': 'sum'}
        fc_sum = df1.groupby(column_list).aggregate(aggregation_functions)
        fc_sum = fc_sum.reset_index()  # ungroup after grouping to retain format
        return Factor(fc_sum)
    
    # Complete multiplication operation (FactorA * FactorB), FactorA = self
    # Assumes that the variables in FactorB are a subset of the variables in FactorA
    # O(N) time complexity
    def multiplication(self, factorB):
        fa = self.df
        fb = factorB.df
        
        # Get the variables for both factors
        fa_vars = self.get_vars()
        fb_vars = factorB.get_vars()
        
        # Get the union of the variables in the two dataframes
        ab_union = fa_vars.union(fb_vars)
        ab_union_list = list(ab_union)
        
        # Todo - Need to pass an empty factor for checking
        if len(ab_union) == 0:
            raise Exception("Error - Product Union is Empty")
        
        # Get the intersection of the variables in the two dataframes
        ab_intersection = fa_vars.intersection(fb_vars)
        ab_intersection_list = list(ab_intersection)
        
        ab_column_list = ab_union_list
        multi_df = pd.DataFrame(columns = ab_column_list)
        multi_df = multi_df.astype(bool) # Cast types of columns to bool by default
        multi_df['Value'] = None
        
        for i, row in fa.iterrows():  # O(N) time complexity
            left = row.Value  # First value for product is simply row value
            row_variable_of_interest = row[ab_intersection_list][1]  # get variable of interest (ex: 'Rain') for multiplication
            
            # For the second value, it needs to be extracted from the second data frame
            right_df1 = fb[ab_intersection_list]
            right_df1_series = right_df1.squeeze('columns')  # squeeze by columns to produce df series
            right_df = fb.loc[row_variable_of_interest == right_df1_series]  # Compare variable of interest values to df series

            # Get the second value by looking at the series
            right_series = right_df.Value
            right = right_series.iloc[1]
            
            # Find the product for this row in the dataframe
            product = left * right
            
            # Create new row with same variables as FactorA row, but add the new calculated value instead
            new_row = row
            new_row['Value'] = product
            multi_df = multi_df.append(new_row)
            
        return Factor(multi_df)
    
# Unit Tests for Summation and Multiplication Operations, and Object Initialization
class Tests(unittest.TestCase):
    def test_summation_c(self):
        answer_factor = Factor('summationResult.csv')  # Expected result is pre-stored in CSV
        
        fc = Factor("FactorC.csv")
        sum_factor = fc.summation('Sprinkler')
                       
        assert sum_factor.get_vars() == {'Rain', 'Grass Wet'}  # Expected variables in sum factor
        assert_frame_equal(sum_factor.get_data(), answer_factor.get_data())  # Computed factor should be identical to retrieved factor
                
    def test_multiplication_a_b(self):
        answer_factor = Factor('multiplicationResult.csv')
        
        fa = Factor("FactorA.csv")
        fb = Factor("FactorB.csv")
        
        mult_factor = fa.multiplication(fb)
               
        assert mult_factor.get_vars() == {'Rain', 'Sprinkler'}
        assert_frame_equal(mult_factor.get_data(), answer_factor.get_data())
        
    # Test case for initializing factor with no arguments
    def test_init_blank(self):
        self.assertRaises(ValueError, Factor, None)
    
    # Test case for initializing factor with dataframe argument
    def test_init_df(self):
        df = pd.DataFrame()
        f = Factor(df)
        assert_frame_equal(f.get_data(), df)  # Dataframe should be stored in factor
        
    # Test case for initializing factor with csv file argument
    def test_init_csv(self):
        f = Factor('FactorA.csv')
        assert f.get_vars() == {'Rain', 'Sprinkler'}  # Variables should be loaded correctly
    
    # Test case for initializing factor with boolean (not string or dataframe) argument
    def test_init_bool(self):
        self.assertRaises(ValueError, Factor, True)


""" =============================== Driver Code ==============================="""
def main():
    # Load Factors from CSV files
    fa = Factor("FactorA.csv")
    fb = Factor("FactorB.csv")
    fc = Factor("FactorC.csv")
    
    # Summation Example
    print("=== Results for Summation: ===")
    sum_factor = fc.summation('Sprinkler')
    sum_factor.print_data()
    print('Sum Factor Variables: ', sum_factor.get_vars())
    sum_factor.save('summation.csv')
    
    # Multiplication Example
    print("=== Results for Multiplication: ===")
    mult_factor = fa.multiplication(fb)
    mult_factor.print_data()
    print('Multiplication Factor Variables: ', mult_factor.get_vars())
    mult_factor.save('multiplication.csv')


if __name__ == '__main__':
    main()
    unittest.main()
