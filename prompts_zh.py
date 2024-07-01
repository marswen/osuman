

system_prompt = "你是一位流行病学和编程经验丰富的医学研究统计师，擅长利用R语言编程分析研究数据，得到流行病学研究结论。"

data_template = """
这是一份医学研究的样例数据。
```
{sample_data}
```
"""

topic_generate_prompt = """
根据上面提供的样例数据，请提出五个医学研究课题，按以下json格式输出。
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
我们的研究课题为:
{topic}
"""

plan_prompt = """
请根据样例数据和研究课题给出具体详细的数据统计分析流程，按以下json格式输出。
```json
[
  {{
    "name": //分析过程
    "description": //具体分析方法
  }} 
]
```
"""

code_generate_template = """
请在以上结果的基础上继续完成以下部分的数据分析，输出R代码。
R代码将在jupyter notebook里执行。如果要加载基础包以外的包，请在第一次加载前先使用`install.packages`安装以避免加载失败。
如果要加载原始数据文件，数据文件路径为'data.csv'。

{section}
"""

code_execution_template = """
代码运行日志：

{output}
"""

code_revise_prompt = "请根据上面运行日志里的报错信息，修改R程序代码，输出修改后的正确代码。"
