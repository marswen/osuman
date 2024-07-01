# OSUMAN
Clinical data analytics agent

### Installation
1. Install Python dependencies
```
pip install -r requirements.txt
```

2. Install R according to the corresponding operating system.

3. Install IRkernel in R command line
```
install.packages('IRkernel')
IRkernel::installspec()
```

4. Install tidyverse
```
install.packages('tidyverse')
```
(If the installation fails under Linux, please refer to: https://medium.com/@jamie84mclaughlin/installing-r-and-the-tidyverse-on-ubuntu-20-04-60170020649b)


### Run
* Add "model_name" to the `config.py` file.
* Copy `. env. example` to `. env`, then modify "OPENAI-API_KEY" or "DASHSCOPE.API_KEY".
```
streamlit run webui.py
```
