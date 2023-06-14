from llama_index import SimpleDirectoryReader, LangchainEmbedding, GPTListIndex, GPTSimpleVectorIndex, PromptHelper, \
    LLMPredictor, ServiceContext
from langchain.chat_models import ChatOpenAI
import gradio as gr
import os
os.environ["OPENAI_API_KEY"] = "sk-XXX"

def construct_index(directory_path):
    max_input_size = 4096
    num_outputs = 2000
    max_chunk_overlap = 20
    chunk_size_limit = 600
    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
    # doc是你文档所存放的位置，recursive代表递归获取里面所有文档
    documents = SimpleDirectoryReader(input_dir='doc', recursive=True).load_data();
    index = GPTSimpleVectorIndex(documents);
    index.save_to_disk('index.json');
    return index


def chatbot(input_text):
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    response = index.query(input_text, response_mode="compact")
    return response.response

if __name__ == "__main__":
    index = construct_index("docs")     # 本地文件库的路径
# iface = gr.Interface(fn=chatbot,
#                      inputs=gr.inputs.Textbox(lines=7, label="请输入，您想从知识库中获取什么？"),
#                      outputs="text",
#                      title="AI 本地知识库ChatBot")
# iface.launch(share=False, server_port=8500)