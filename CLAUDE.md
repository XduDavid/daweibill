# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

**小遥账单助手** - 隐私优先的个人账单分析工具，支持支付宝和微信账单的自动解析和多维度数据可视化分析。

核心特点：
- 数据完全本地处理，不上传任何服务器
- 支持支付宝 CSV 和微信 CSV/XLSX 账单文件
- 多维度分析：年度、月度、分类、时间、消费洞察
- 前后端分离架构（Vue 3 + Flask）

## 环境要求

- Python 3.10.11+
- Node.js 18+

## 常用开发命令

### 后端开发

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（Windows）
py -3.10 -m venv venv

# 激活虚拟环境（Windows）
venv\Scripts\activate

# 激活虚拟环境（Linux/macOS）
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 运行开发服务器
python app.py

# 运行测试
pytest

# 代码格式化
black backend/

# 退出虚拟环境
deactivate
```

### 前端开发

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview

# 运行测试
npm run test

# 代码检查
npm run lint
```

### Docker 开发

```bash
# 一键启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 重启服务
docker-compose restart
```

## 代码架构

### 后端架构（Flask + Pandas）

```
backend/
├── api/              # API 路由层（蓝草图）
│   ├── analysis.py   # 分析数据接口
│   ├── files.py      # 文件上传接口
│   └── session.py    # 会话管理接口
├── services/         # 业务逻辑层
│   ├── analysis.py   # 核心分析逻辑
│   ├── data_loader.py # 数据加载
│   └── generators.py # 数据生成器
├── parsers/          # 文件解析模块
│   ├── alipay.py    # 支付宝账单解析
│   └── wechat.py    # 微信账单解析
├── utils/            # 工具函数
├── data/             # 临时数据目录（gitignore）
├── app.py            # 应用入口（注册蓝图，启动服务）
└── config.py         # 配置管理
```

**架构风格**：模块化分层架构
- API 层：处理 HTTP 请求/响应，使用 Flask Blueprint
- Service 层：封装核心业务逻辑
- Parser 层：专注于不同格式账单的解析
- 数据处理使用 Pandas 进行高效分析

### 前端架构（Vue 3 + Vite）

```
frontend/
├── src/
│   ├── api/          # API 客户端（封装 HTTP 请求）
│   ├── views/        # 页面组件（每个功能一页）
│   ├── components/   # 公共组件（可复用）
│   ├── stores/       # 状态管理（Pinia）
│   ├── router/       # 路由配置
│   ├── utils/        # 工具函数
│   ├── App.vue       # 根组件
│   └── main.js       # 入口文件
├── public/           # 静态资源
├── vite.config.js    # Vite 配置
└── package.json      # 依赖配置
```

**架构风格**：单页应用（SPA）
- 组合式 API（Vue 3 Composition API）
- Pinia 进行状态管理
- Vue Router 进行路由管理
- ECharts 进行数据可视化
- 使用原生 Fetch API，无需额外 HTTP 客户端

## API 接口

所有 API 前缀为 `/api`，主要分为三类：
- 文件上传/清理：`/api/files/*`
- 会话管理：`/api/session/*`
- 数据分析：`/api/analysis/*`

完整文档参见 `docs/接口文档.md`

## 代码规范

### 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 文件名 | 小写字母+下划线 | `data_service.py` |
| 类名 | PascalCase | `DataService` |
| 函数名 | snake_case（Python）/ camelCase（JS）| `get_yearly_analysis` / `getYearlyAnalysis` |
| 变量名 | snake_case（Python）/ camelCase（JS）| `user_id` / `userId` |

### 语言要求

- **所有代码注释、文档、AI 回复必须使用中文**

### 格式工具

- Python：使用 `black` 格式化，每行不超过 88 字符
- JavaScript/Vue：遵循 ESLint 推荐规范

## Git 规范

- 分支策略：`main` → `dev` → `feature/*` / `fix/*`
- 提交信息遵循 [Conventional Commits](https://www.conventionalcommits.org/) 格式
- 类型：`feat`, `fix`, `refactor`, `docs`, `style`, `test`, `chore`

## 设计文档

项目所有设计文档都在 `docs/` 目录：

- [市场需求文档](docs/00-mrd.md)
- [产品需求文档](docs/01-prd.md)
- [API 接口文档](docs/接口文档.md)
- [重构方案](docs/02-老账单重构方案.md)

## 关键架构决策

- **AD-20260217-001**: 前后端分离重构，保持 API 向后兼容，渐进式迁移
- **隐私优先**: 所有数据本地处理，不上传云端
- **技术选型**: Flask + Pandas（后端），Vue 3 + Vite（前端）

## 部署

### 生产部署（Docker）

```bash
docker-compose up -d
```

访问 http://localhost:8888

### 手动部署

1. 前端构建：`cd frontend && npm run build`
2. 后端启动：`cd backend && python app.py`
3. 使用 Nginx 反向代理，前端静态文件直接服务，API 代理到后端

详细配置参见 `README.md`
