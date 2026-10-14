import os
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import arxiv
from dotenv import load_dotenv
from openai import OpenAI

# 加载.env
load_dotenv()

# ========= 配置区 =========
# DeepSeek API
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# 邮箱（QQ邮箱SMTP）
MAIL_SENDER = os.getenv("MAIL_SENDER")
MAIL_RECEIVER = os.getenv("MAIL_RECEIVER")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465

# arxiv检索关键词
SEARCH_QUERY = "(BEV OR VLM) AND (autonomous driving)"
MAX_RESULT = 5
SENT_ID_FILE = "sent_paper_ids.txt"
# =========================

def load_sent_ids():
    """读取已经推送过的论文ID，防止重复推送"""
    if not os.path.exists(SENT_ID_FILE):
        return set()
    with open(SENT_ID_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f.readlines())

def save_sent_id(paper_id):
    """保存已推送论文id"""
    with open(SENT_ID_FILE, "a", encoding="utf-8") as f:
        f.write(paper_id + "\n")

def deepseek_translate_abstract(abstract: str):
    """调用DeepSeek：翻译摘要 + 提炼创新点"""
    prompt = f"""下面是arXiv自动驾驶论文英文摘要：
{abstract}

请完成两件任务：
1. 将摘要通顺翻译成中文，自动驾驶专业术语准确；
2. 在末尾单独一段【核心创新】，一句话总结论文的创新点。
"""
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return resp.choices[0].message.content

def send_email(subject, html_content):
    """发送邮件"""
    msg = MIMEText(html_content, "html", "utf-8")
    msg["From"] = Header(MAIL_SENDER)
    msg["To"] = Header(MAIL_RECEIVER)
    msg["Subject"] = Header(subject, "utf-8")
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(MAIL_SENDER, MAIL_PASSWORD)
        server.sendmail(MAIL_SENDER, MAIL_RECEIVER, msg.as_string())

def run_agent():
    print("===== 开始抓取arXiv论文 =====")
    sent_ids = load_sent_ids()
    arxiv_client = arxiv.Client()
    search = arxiv.Search(
        query=SEARCH_QUERY,
        max_results=MAX_RESULT,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    papers_html = ""
    for result in arxiv_client.results(search):
        paper_id = result.entry_id.split("/")[-1]
        if paper_id in sent_ids:
            print(f"跳过已推送论文：{paper_id}")
            continue
        print(f"处理论文：{result.title}")
        translated_text = deepseek_translate_abstract(result.summary)
        paper_html = f"""
        <h3>{result.title}</h3>
        <p><b>作者：</b>{', '.join(a.name for a in result.authors)}</p>
        <p><b>链接：</b><a href="{result.entry_id}">{result.entry_id}</a></p>
        <p><b>提交日期：</b>{result.published.date()}</p>
        <p>{translated_text}</p>
        <hr>
        """
        papers_html += paper_html
        save_sent_id(paper_id)
        time.sleep(1.2)
    if papers_html:
        send_email("arXiv自动驾驶BEV/VLM新论文推送", papers_html)
        print("✅ 邮件发送成功")
    else:
        print("本次没有新论文")

if __name__ == "__main__":
    run_agent()
