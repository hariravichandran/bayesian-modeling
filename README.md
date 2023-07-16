# Bayesian Modeling
Author: Hari Ravichandran

## Table of Contents
- [Problem Statement](#problem-statement)
- [Repo Overview](#repo-overview)
  * [Description](#description)
  * [Data Structure Choice](#data-structure-choice)
  * [Summing-Out Algorithm – O(N) Time Complexity, O(N) Space Complexity](#summing-out-algorithm---o-n--time-complexity--o-n--space-complexity)
  * [Multiplying Algorithm – O(N) Time Complexity, O(N) Space Complexity](#multiplying-algorithm---o-n--time-complexity--o-n--space-complexity)
  * [Unit Tests](#unit-tests)
  * [Materials Used](#materials-used)
- [Instructions for Running Code](#instructions-for-running-code)
  * [Building the Code](#building-the-code)
  * [Running the Code](#running-the-code)
  * [Files](#files)
  * [Output](#output)

# Problem Statement
A factor is a function that maps each variable in a set to a number greater than or equal to zero.

Given two sets of variables **A** and **B** , and the set of shared variables, , the instantiation of the aforementioned variables **a** and **b** are consistent, if the instantiation of the shared variables **c** in **a** and **b** are the same.

Here is an example Bayesian Network for a Sprinkler:
![Bayesian Network Image should display here.](SampleBayesianNetwork.png)

![Bayesian Network Image should display here.](https://github.com/hariravichandran/bayesian-factors/blob/f847dc2a708f6de59468f91581a5b8c2b1d8d586/SampleBayesianNetwork.PNG)

For this network, the factors are as follows:

Factor A over Rain, Sprinkler:

| Rain | Sprinkler | Value |
| --- | --- | --- |
| FALSE | FALSE | 0.45 |
| FALSE | TRUE | 0.55 |
| TRUE | FALSE | 0.95 |
| TRUE | TRUE | 0.05 |

Factor B over Rain:

| Rain | Value |
| --- | --- |
| TRUE | 0.3 |
| FALSE | 0.7 |

Factor C over Sprinkler, Rain, Grass Wet:

| Sprinkler | Rain | Grass Wet | Value |
| --- | --- | --- | --- |
| FALSE | FALSE | TRUE | 0 |
| FALSE | TRUE | TRUE | 0.95 |
| TRUE | FALSE | TRUE | 0.85 |
| TRUE | TRUE | TRUE | 0.97 |
| FALSE | FALSE | FALSE | 1 |
| FALSE | TRUE | FALSE | 0.05 |
| TRUE | FALSE | FALSE | 0.15 |
| TRUE | TRUE | FALSE | 0.03 |

This repository implements two factor operations that each produce a new factor:

**Summing-out operation:**
Where is a factor over variables , and is a variable in . By summing out variable from factor , we get a result that is another factor over the set of variables with removed.

For example, if we sum out the &quot;Sprinkler&quot; Variable from Factor C, we get the following resulting factor:

| Rain | Grass Wet | Value |
| --- | --- | --- |
| FALSE | FALSE | 1.15 |
| FALSE | TRUE | 0.85 |
| TRUE | FALSE | 0.08 |
| TRUE | TRUE | 1.92 |

In the above example, we essentially sum the probabilities while disregarding the summed-out variable.

**Multiplication operation:**
When we multiply two factors , we get another factor that has the variables . In the equation above, is consistent with and . Here is the result of multiplying the example factors A and B:

| Rain | Sprinkler | Value |
| --- | --- | --- |
| FALSE | FALSE | 0.315 |
| FALSE | TRUE | 0.385 |
| TRUE | FALSE | 0.285 |
| TRUE | TRUE | 0.015 |

# Repo Overview
## Description
As defined in the problem statement, a factor &#39;is a function over a set of variables&#39;. The &#39;Factor&#39; class implemented in &#39;factor.py&#39; provides a framework that facilitates factor operations. These operations include:

- **constructor** – create Factor object from CSV file or Pandas DataFrame
- **save** – save Factor to CSV file
- **get\_data** – fetch data from Factor object
- **print\_data** – print factor data to console
- **get\_vars** – get set of all variables in Factor
- **summation** – summing over operation
- **multiplication** – multiplication operation

In addition to the class, &#39;Factor.py&#39; includes some driver code with examples, and the unit tests. Running the code saves the results from the summation and multiplication examples into the files &#39;summation.csv&#39; and &#39;multiplication.csv&#39; respectively. All of the example factors (A, B, and C) are stored in the main directory in CSV format.

## Data Structure Choice
The Factor data itself is stored in a Pandas DataFrame within the object. This facilitates easy array level operations on the Factors. Data frames can only be as large as the memory that the system has. In case of massive datasets that exceed the memory capacity, Apache Spark can be used. Each row in a factor will be a key-value pair. Each key could be an immutable tuple that has one to many factors. These keys can be processed across many compute nodes in a parallel fashion. Apache Data Frames can be potentially employed for this purpose, and the operations have to be parallelized.

## Summing-Out Algorithm – O(N) Time Complexity, O(N) Space Complexity
The summing out algorithm works as follows: getting the desired column list by removing the &#39;Value&#39; column and Value of Interest, dropping the column with the variable of interest, and grouping by the desired columns to find the aggregated sum. Since the aggregation operation has to look at all the elements in the dataframe once, the time complexity is O(N). The space complexity is O(N) since a new data structure is made to store the results.

## Multiplying Algorithm – O(N) Time Complexity, O(N) Space Complexity
The multiplication algorithm assumes that when multiplying Factor A and Factor B, the variables in Factor B are a subset of the variables in Factor A. If Factor B is a superset of Factor A, then the order of arguments can be switched inside the multiplication operation as a first step. Using this assumption, we can get the set of variables in both factors, as well as their unions and intersections. Then, we can iterate over all the rows in Factor A and match the relevant variables with those in Factor B to get the product. Since each row is examined only once, the time complexity is O(N). The space complexity is O(N) since we make a new DataFrame to store the result.

## Unit Tests
Included in &#39;factor.py&#39; are unit tests that test the summation and multiplication algorithms. Unit tests for the Factor class constructor for additional code coverage are also included. Together, these tests cover nearly all of the lines of code.

## Materials Used
- Python &#39;pandas&#39; documentation: [https://pandas.pydata.org/docs/](https://pandas.pydata.org/docs/)
- Python &#39;unittest&#39; documentation: [https://docs.python.org/3/library/unittest.html](https://docs.python.org/3/library/unittest.html)

# Instructions for Running Code

## Building the Code
The following libraries are required to run the code, as listed in requirements.txt:

```
pandas==1.2.1
```

The program was developed using Python 3.8.3.

To install all the needed packages to run this code using pip, go to the program directory and run the following command:

```bash
python3 -m pip install -r requirements.txt
```

More information can be found [here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

## Running the Code
To run the code, navigate to the directory in the command line, and run the following command:

```bash
python ./factor.py
```

Alternatively, if Python 3 is accessible through the 'python3' command:

```bash
python3 ./factor.py
```

The code can also be run in an IDE. For this project, Spyder 4 was used. Simply open the 'factor.py' file and click the run button in Spyder to run the code.

## Files
The files in the directory are as follows:

`README`: Readme file for the code

`requirements.txt`: Contains required Python libraries

`factor.py`: code for the factor class, driver code, and unit tests

`FactorA.csv`: stored form of factor A (CSV format)

`FactorB.csv`: stored form of factor B (CSV format)

`FactorC.csv`: stored form of factor C (CSV format)

`summationResult.csv`: manually computed result for summing Factor C over the `Sprinkler` variable, for testing purposes (CSV format)

`multiplicationResult.csv`: manually computed result for multiplying Factors A and B, for testing purposes (CSV format)

`SampleBayesianNetwork.png`: shows the example Bayesian Network image

## Output
Once the code has finished running, it will print out the results of the summing out and multiplying operation on the examples given. It will also print whether all the unit tests passed or failed. The driver code also stores the results of the summation operation on Factor C over the `Sprinkler` variable in`summation.csv`. In addition, the results of the multiplication operation on Factor A and Factor B from the driver code are stored in `multiplication.csv`.
