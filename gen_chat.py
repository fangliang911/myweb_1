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
    law_point_list=df_point.loc[df_point['law_name']==radio_btn,'law_point'].unique().tolist()
    radio_return = gr.Radio.update(choices=law_point_list, value=None)
    return radio_return
def clear_txt(input_txt):
    return gr.Text.update(value='')

def gen_prompt(input_txt,law_radio,point_radio):
    try:
        return gr.Text.update(value=prompt_template.format(law_radio,point_radio))
    except:
        return gr.Text.update(value='Some Error')
def save_chat():
    try:
        t_df=pd.DataFrame(data=None,columns=['chat_datetime','chat_content'])
        t_df.loc[1]=[datetime.now().strftime('%Y-%m-%d %H:%M:%S'),str(messages)]
        t_df.to_sql('message_chatmsg',con,if_exists="append",index=False)
        return gr.Radio.update(value='Save Ok')
    except:
        return gr.Radio.update(value='Save Failed')


def main():
    with gr.Blocks() as main:
        with gr.Row():
            with gr.Column():
                input_law_radio=gr.Radio(choices=law_name_list, label='法律方向')
                input_point_radio=gr.Radio(choices=[], label='重要考点')
                input_prompt_txt=gr.Textbox(default=prompt_template,lines=7, label="试试ChatGPT")
                with gr.Row():
                    clear_btn=gr.Button(value="清除内容")
                    generate_btn = gr.Button(value="生成提示词")
                    submit_btn=gr.Button(value="提交问题")
                    save_btn = gr.Button(value="对话存储")
            with gr.Column():
                save_status=gr.Radio(choices=['Save Ok','Save Failed'],label='对话存储情况',interactive=False)
                outputs = gr.Textbox(label="ChatGPT回复：")
        input_law_radio.change(reload_point,inputs=[input_law_radio],outputs=[input_point_radio])
        clear_btn.click(clear_txt,inputs=[input_prompt_txt],outputs=[input_prompt_txt])
        generate_btn.click(gen_prompt,inputs=[input_prompt_txt,input_law_radio,input_point_radio],outputs=[input_prompt_txt])
        submit_btn.click(chatbot,inputs=[input_prompt_txt],outputs=[outputs])
        save_btn.click(save_chat,inputs=[],outputs=[save_status])
    main.launch(auth=("admin", "woshiyizhixiaobaitu"),share=False)

if __name__ == "__main__":
    openai.api_key = "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"
    con = sqlite3.connect('db.sqlite3', check_same_thread=False)
    df_point = pd.read_sql_query('select * from lawpoint_lawpoint;', con)
    law_name_list = df_point['law_name'].unique().tolist()
    prompt_template = "我是一名准备参加中国司法考试的学生。请为我提供{0}方向{1}考点的法律专业讲解和真题解析。"
    messages = [{"role": "system", "content": "You are a helpful and kind AI Assistant."}, ]
    main()
    con.close()
