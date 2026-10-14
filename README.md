# arXiv BEV/VLM 自动驾驶论文追踪 Agent
> 自动抓取 arXiv 上 BEV / VLM 方向自动驾驶最新论文，调用 DeepSeek 大模型翻译摘要、提炼核心创新，自动邮件推送。
> Python 实现，支持 PyCharm 本地调试，也可部署 GitHub Actions 云端定时执行。

## ✨ 功能介绍
1. 调用 arXiv **官方API**检索论文，检索关键词：`(BEV OR VLM) AND (autonomous driving)`，按提交时间抓取最新论文
2. 持久记录已推送论文ID，**不会重复推送旧论文**，保存至 `sent_paper_ids.txt`
3. 调用 DeepSeek 大模型：完成英文摘要专业中文翻译 + 一句话提炼论文核心创新点
4. 组装 HTML 富文本邮件，通过 QQ邮箱 SMTP 自动推送至目标邮箱
5. 支持 PyCharm / 命令行本地直接运行，可扩展云端定时任务

## 🛠️ 技术栈
- Python 3.10+
- `arxiv`：arXiv官方API库，获取论文元信息（合规，非网页爬虫）
- `python-dotenv`：读取本地密钥配置
- `langchain-deepseek`：调用DeepSeek大模型
- `smtplib`：Python内置库，实现邮件发送

## 📁 项目文件结构
```
arxiv-paper-agent/
├── paper_agent.py          # 主程序代码
├── .env                    # 密钥配置文件（⚠️ 不上传GitHub！）
├── .gitignore              # Git忽略配置文件
├── sent_paper_ids.txt      # 程序运行自动生成，记录已推送论文ID
└── README.md               # 项目说明文档
```

## 📋 前置准备
1. Python3.10 及以上版本，推荐使用 PyCharm 用于代码调试
2. DeepSeek API Key：前往 [DeepSeek开放平台](https://platform.deepseek.com/) 申请
3. QQ邮箱SMTP授权码：QQ邮箱设置页面开启POP3/SMTP服务，获取授权码（**不是邮箱登录密码**）

### `.env` 配置文件（本地新建，不要上传到GitHub）
```env
DEEPSEEK_API_KEY=sk-xxxx
MAIL_SENDER=xxx@qq.com
MAIL_RECEIVER=xxx@shturl.
MAIL_PASSWORD=QQ邮箱SMTP授权码
MAIL_SMTP_SERVER=smtp.qq.com
MAIL_SMTP_PORT=465
```

## 🚀 本地运行步骤
1. 克隆项目到本地
```bash
git clone [https://github.com/](https://github.com/)你的用户名/arxiv-paper-agent.git
cd arxiv-paper-agent
```
2. 安装依赖包
```bash
pip install arxiv langchain langchain-deepseek python-dotenv
```
3. 在项目根目录创建 `.env` 文件，填入上面的密钥信息
4. 运行主程序
```bash
python paper_agent.py
```
> 也可以直接在PyCharm中打开项目，右键 `paper_agent.py` 点击运行。