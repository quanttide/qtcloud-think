# Workspace 最佳实践

Workspace（工作空间）帮助团队将不同类型的数据隔离管理。以下是公司的最佳实践：

## 推荐 Workspace 划分

| Workspace | 用途 | 说明 |
|-----------|------|------|
| `personal` | 个人思考 | 员工私人的思维碎片和笔记 |
| `meta` | 系统自省 | 系统的运行数据分析和建议 |
| `shared` | 团队共享 | 团队共同的知识库 |

## 部门级 Workspace

对于大型组织，可以按部门创建独立 Workspace：

| Workspace | 部门 |
|-----------|------|
| `engineering` | 工程部 |
| `marketing` | 市场部 |
| `sales` | 销售部 |
| `product` | 产品部 |
| `hr` | 人力资源部 |

## 命名规范

- **小写字母**：使用小写字母和下划线
- **有意义**：名称应反映用途
- **避免冲突**：不要与系统保留字冲突

```
# 推荐
personal
shared
engineering

# 不推荐
my_workspace
test123
workspace1
```

## 数据流转建议

1. **个人 → 团队**：重要的个人思考可以移动到 `shared`
2. **团队 → 部门**：部门共性内容上升为部门级
3. **定期归档**：过期数据可以归档到 `archive/{year}/`

## 访问控制（未来规划）

| Workspace | 访问权限 |
|-----------|---------|
| personal | 仅本人 |
| shared | 团队成员 |
| department:* | 部门成员 |
| meta | 管理员 |
