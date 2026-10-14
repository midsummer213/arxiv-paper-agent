# arXiv 每日论文自动推送机器人（README.md）
> 项目名称：Daily Paper Crawler
> 适用场景：自动抓取arXiv机器人/自动驾驶领域最新论文，调用大模型总结摘要，邮件定时推送，避免重复推送。

## ✨ 项目介绍
本项目基于 Python + GitHub Actions 实现**自动化论文订阅推送**，无需本地长期开机。
- 定时任务：**北京时间每天下午17:00**自动执行；同时支持手动触发测试
- 数据源：arXiv 预印本平台，抓取机器人、自动驾驶、VLA视觉语言动作相关论文
- 内容处理：调用 DeepSeek 大模型，自动解析论文摘要，提炼核心创新点
- 邮件推送：自动生成格式化邮件，将当日新论文汇总发送至指定邮箱
- 去重机制：将已推送论文ID持久化保存到 `sent_paper_ids.txt`，每次运行跳过已经推送过的论文，防止重复发邮件
- 部署方式：GitHub Actions CI/CD，云端运行，本地电脑不用保持开机

## 📦 项目文件结构
```
.
├── paper_agent.py          # 主程序：爬虫、大模型调用、邮件发送逻辑
├── requirements.txt        # Python依赖包列表
├── sent_paper_ids.txt      # 记录已经推送完成的论文id，自动维护
└── .github
    └── workflows
        └── daily_run.yml   # GitHub Actions 定时工作流配置文件
```

## ⚙️ 工作流说明（daily_run.yml）
1. **触发方式**
    - 定时触发：`cron: '0 9 * * *'`，UTC 09:00 = 北京时间17:00，每日下午5点自动跑
    - 手动触发：`workflow_dispatch`，在GitHub Actions页面可以随时点击运行测试
2. **权限配置**：`permissions: contents: write`，授予Action机器人向仓库提交文件的写入权限，用于保存论文记录
3. 执行步骤：
    1. 拉取仓库代码到云端临时容器
    2. 配置 Python3.10 环境，安装项目依赖
    3. 运行 `paper_agent.py`，抓取论文、调用DeepSeek、发送邮件
    4. 脚本运行完成后，自动判断 `sent_paper_ids.txt` 是否更新；如有新增记录，自动提交并推送回仓库，永久保存已推送论文ID
    5. 无新增论文记录时，跳过提交，不产生多余commit

## 🔧 环境与密钥配置（仓库 Secrets）
需要在仓库 `Settings → Secrets and variables → Actions` 里添加4个环境密钥：
| Secret 名称 | 说明 |
| ---- | ---- |
| DEEPSEEK_API_KEY | DeepSeek平台API密钥，用于论文摘要解析 |
| MAIL_SENDER | 发件邮箱（QQ邮箱/163邮箱） |
| MAIL_RECEIVER | 收件邮箱，接收每日论文推送 |
| MAIL_PASSWORD | 邮箱SMTP授权码（不是邮箱登录密码） |

> 密钥不会在日志中明文打印，安全隔离，不会泄露。

## 🚀 使用方法
1. Fork / 将代码上传至GitHub仓库
2. 在仓库Action Secrets填入上面4项密钥
3. 确认GitHub Actions在仓库设置中启用
4. 等待每日17点自动执行，或者在Actions页面点击 `Run workflow` 手动测试
5. 运行成功后，查看收件邮箱获取论文汇总邮件

## 📝 运行日志查看
进入仓库 → Actions → Daily Paper Crawler，打开对应运行记录：
- `Run the Agent`：查看Python脚本控制台输出，打印抓取论文列表、邮件发送状态
- 绿色Success：脚本正常执行完成；不代表一定有新论文，当日无新论文则不会发送邮件
