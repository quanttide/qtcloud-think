# 量潮思考云(`qtcloud-think`)

思维外脑 - 思维收集与澄清工具

## 数据目录

- 所有动态生成的数据存放在项目根目录的 `data/` 下
- 该目录**不会被提交到 Git**，可安全删除
- 首次运行应用时会自动创建所需子目录

```
data/
├── provider/             # FastAPI 产生的数据
│   ├── app.db
│   └── uploads/
├── cli/                  # CLI 产生的输出
│   └── notes/
└── shared/               # 跨项目共享的临时数据
```
