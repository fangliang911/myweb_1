import os
from llama_index import SimpleDirectoryReader, LangchainEmbedding, GPTListIndex, GPTSimpleVectorIndex, PromptHelper, \
    LLMPredictor, ServiceContext
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate   # 想了下觉得可以不用
import openai
import gradio as gr
import sqlite3
import pandas as pd
from datetime import datetime


def chatbot(input):
    if input:
        messages.append({"role": "user", "content": input})
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        reply = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        return reply


def reload_point(radio_btn):
    law_point_list = df_point.loc[df_point['law_name'] == radio_btn, 'law_point'].unique().tolist()
    radio_return = gr.Radio.update(choices=law_point_list, value=None)
    return radio_return


def reload_action(radio_btn):
    return gr.Text.update(value=radio_btn)


def clear_txt(input_txt):
    return gr.Text.update(value='')


def gen_prompt(input_txt, law_radio, point_radio):
    try:
        return gr.Text.update(value=input_txt.format(law_radio, point_radio))
    except:
        return gr.Text.update(value='Some Error')


def direct_prompt(radio_btn):
    return gr.Text.update(value=radio_btn)


def save_chat():
    try:
        t_df = pd.DataFrame(data=None, columns=['chat_datetime', 'chat_content'])
        t_df.loc[1] = [datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(messages)]
        t_df.to_sql('message_chatmsg', con, if_exists="append", index=False)
        return gr.Radio.update(value='Save Ok')
    except:
        return gr.Radio.update(value='Save Failed')


def construct_index(directory_path):
    max_input_size = 4096
    num_outputs = 2000
    max_chunk_overlap = 20
    chunk_size_limit = 600
    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.8, model_name="gpt-3.5-turbo", max_tokens=num_outputs))
    documents = SimpleDirectoryReader(directory_path, recursive=True).load_data()
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
    index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)
    index.save_to_disk('index.json')
    return index


def chatbot_local(input_text):
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    response = index.query(input_text, response_mode="compact")
    return response.response


def main():
    # 创建法律考点
    with gr.Blocks() as lawpoint:
        with gr.Row():
            with gr.Column():
                input_law_radio = gr.Radio(choices=law_name_list, label='法律方向')
                input_point_radio = gr.Radio(choices=[], label='重要考点')
                input_action_radio = gr.Radio(choices=prompt_templates, label='学习模式')
                input_prompt_txt = gr.Textbox(default=prompt_templates[0], lines=7, label="试试ChatGPT")
                with gr.Row():
                    clear_btn = gr.Button(value="清除内容")
                    generate_btn = gr.Button(value="生成提示词")
                    submit_btn = gr.Button(value="提交问题")
                    save_btn = gr.Button(value="对话存储")
            with gr.Column():
                save_status = gr.Radio(choices=['Save Ok', 'Save Failed'], label='对话存储情况', interactive=False)
                outputs = gr.outputs.Textbox(label="ChatGPT回复：")
        input_law_radio.change(reload_point, inputs=[input_law_radio], outputs=[input_point_radio])
        input_action_radio.change(reload_action, inputs=[input_action_radio], outputs=[input_prompt_txt])
        clear_btn.click(clear_txt, inputs=[input_prompt_txt], outputs=[input_prompt_txt])
        generate_btn.click(gen_prompt, inputs=[input_prompt_txt, input_law_radio, input_point_radio],
                           outputs=[input_prompt_txt])
        submit_btn.click(chatbot, inputs=[input_prompt_txt], outputs=[outputs])
        save_btn.click(save_chat, inputs=[], outputs=[save_status])
    # 创建模拟法庭
    with gr.Blocks() as lawcourt:
        with gr.Row():
            with gr.Column():
                input_law_radio = gr.Radio(choices=prompt_list, label='提示词模板')
                input_prompt_txt = gr.Textbox(default=prompt_templates[0], lines=7, label="试试ChatGPT")
                with gr.Row():
                    clear_btn = gr.Button(value="清除内容")
                    submit_btn = gr.Button(value="提交问题")
                    save_btn = gr.Button(value="对话存储")
            with gr.Column():
                save_status = gr.Radio(choices=['Save Ok', 'Save Failed'], label='对话存储情况', interactive=False)
                outputs = gr.Textbox(label="ChatGPT回复：")
        input_law_radio.change(direct_prompt, inputs=[input_law_radio], outputs=[input_prompt_txt])
        clear_btn.click(clear_txt, inputs=[input_prompt_txt], outputs=[input_prompt_txt])
        submit_btn.click(chatbot, inputs=[input_prompt_txt], outputs=[outputs])
        save_btn.click(save_chat, inputs=[], outputs=[save_status])
    # local_index = construct_index("docs")
    local_knowledge = gr.Interface(fn=chatbot_local,
                                   inputs=gr.inputs.Textbox(lines=7, label="请输入，您想从知识库中获取什么？"),
                                   outputs="text",
                                   title="AI 本地知识库ChatBot")
    multi_gr = gr.TabbedInterface(([lawpoint, lawcourt, local_knowledge]),
                                  ["法律考点", "模拟法庭", "本地知识库应用"])
    multi_gr.launch(auth=("admin", "woshiyizhixiaobaitu"),server_name="0.0.0.0",server_port=8010)


if __name__ == "__main__":
    openai.api_key = "Your API key"
    os.environ["OPENAI_API_KEY"] = openai.api_key
    con = sqlite3.connect('db.sqlite3', check_same_thread=False)
    df_point = pd.read_sql_query('select * from lawpoint_lawpoint;', con)
    law_name_list = df_point['law_name'].unique().tolist()
    df_prompt = pd.read_sql_query('select * from prompt_prompt_manage limit 5;', con)
    prompt_list = df_prompt['prompt_template'].tolist()
    prompt_templates = ["我是一名准备参加中国司法考试的学生。请为我提供[{0}]方向[{1}]考点的法律专业讲解和真题解析。",
                        "我是一名中国的实习律师。你作为一名专业律师，为我提供一个[{0}]方向[{1}]考点的法律场景，并对我的回答进行[好]或[差]的评价。",]
    messages = [{"role": "system", "content": "You are a helpful and kind AI Assistant."}, ]
    main()
    con.close()
