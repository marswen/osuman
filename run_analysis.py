import re
import json
import prompts
from dotenv import load_dotenv
from JupyterClient import JupyterNotebook
from langchain.prompts import PromptTemplate
from langchain.schema import SystemMessage, HumanMessage

load_dotenv()


def extract_json(text):
    data_match = re.search('```(?:json)?(.+)```', text, re.DOTALL)
    if data_match is not None:
        data_json = json.loads(data_match.group(1).replace('\n', ''))
    else:
        try:
            data_json = json.loads(text.replace('\n', ''))
        except:
            data_json = []
    return data_json


def extract_code(text):
    results = list()
    for m in re.finditer('```(?:[R|r])?(.+?)```', text, re.DOTALL):
        for part in re.split('\n(?:#)', m.group(1)):
            if len(part) > 0:
                results.append(f'#{part}')
    return results


class RunAnalysis:
    def __init__(self, chat_llm, callbacks, data):
        self.chat_llm = chat_llm
        self.callbacks = callbacks
        self.data = data
        self.topic_generate_json = None
        self.history_messages = None

    def generate_topic(self):
        system_message = SystemMessage(content=prompts.system_prompt)
        sample_data = self.data.head().to_markdown(index=False)
        data_prompt = PromptTemplate(template=prompts.data_template, input_variables=['sample_data']).format(sample_data=sample_data)
        data_message = HumanMessage(content=data_prompt)
        self.history_messages = [system_message, data_message]
        topic_generate_message = HumanMessage(content=prompts.topic_generate_prompt)
        topic_generate_result = self.chat_llm(self.history_messages + [topic_generate_message], callbacks=self.callbacks)
        self.topic_generate_json = extract_json(topic_generate_result.content)

    def generate_code(self, topic_select_id):
        topic_select = self.topic_generate_json[topic_select_id]['title'] + '\n' + self.topic_generate_json[topic_select_id]['description']
        topic_prompt = PromptTemplate(template=prompts.topic_template, input_variables=['topic']).format(topic=topic_select)
        topic_message = HumanMessage(content=topic_prompt)
        plan_message = HumanMessage(content=prompts.plan_prompt)
        self.history_messages += [topic_message]
        plan_result = self.chat_llm(self.history_messages+[plan_message], callbacks=self.callbacks)
        plan_json = extract_json(plan_result.content)
        nb = JupyterNotebook()
        logs = list()
        for section in plan_json:
            section_plan = section['name'] + '\n' + section['description']
            code_prompt = PromptTemplate(template=prompts.code_generate_template, input_variables=['section']).format(section=section_plan)
            code_message = HumanMessage(content=code_prompt)
            try_times = 0
            while True:
                if try_times == 0:
                    input_messages = self.history_messages+[code_message]
                else:
                    revise_message = HumanMessage(content=prompts.code_revise_prompt)
                    input_messages = self.history_messages+[code_message, code_execution_message, revise_message]
                code_result = self.chat_llm(input_messages, callbacks=self.callbacks)
                execution_results = list()
                success = True
                for snippet in extract_code(code_result.content):
                    output, error = nb.add_and_run(snippet)
                    if error:
                        success = False
                    execution_results.append((snippet, f'Status: {"Error" if error else "Finish"}\n{output}'))
                execution_log = '\n\n'.join(['```R\n'+cell[0]+'\n```\nExecution result: \n'+cell[1] for cell in execution_results])
                logs.append(execution_log)
                code_execution_prompt = PromptTemplate(template=prompts.code_execution_template, input_variables=['output']).format(output=execution_log)
                code_execution_message = HumanMessage(content=code_execution_prompt)
                try_times += 1
                if try_times > 5 or success:
                    break
            self.history_messages.append(code_execution_message)
        nb.close()
        return logs
