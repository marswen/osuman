

system_prompt = """
You are an experienced medical research statistician in epidemiology and programming, 
skilled in using R language to analyze research data and obtain epidemiological research conclusions.
"""

data_template = """
This is a sample data from medical research.
```
{sample_data}
```
"""

topic_generate_prompt = """
Based on the sample data provided above, please propose five medical research topics and output them in the following JSON format.
```json
[
  {
    "title":
    "description":
  } 
]
```
"""

topic_template = """
Our research topic is:
{topic}
"""

plan_prompt = """
Please provide a specific and detailed data statistical analysis process based on the sample data and research topic, and output it in the following JSON format.
```json
[
  {{
    "name": //Analysis process
    "description": //Specific analysis methods
  }} 
]
```
"""

code_generate_template = """
Please continue to complete the data analysis in the following section based on the above results and output the R code.
The R code will be executed in Jupyter Notebook. If you want to load packages other than the basic package, please use 'install. packages' before the first load to avoid loading failure.
If you want to load the original data file, the data file path is './data.csv'.

{section}
"""

code_execution_template = """
Code Run Log:

{output}
"""

code_revise_prompt = """
Please modify the R code based on the error information in the running log above and output the modified correct code.
"""
