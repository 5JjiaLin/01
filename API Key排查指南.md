# API Key问题排查指南

## 当前状态

已添加API Key输入框，但仍然连接失败。需要排查以下问题：

## 排查步骤

### 步骤1：检查API Key是否加载

1. 刷新页面：http://localhost:3001/
2. 按F12打开开发者工具
3. 切换到"Console"标签
4. 查找调试信息：
   ```
   [Debug] callClaude - API Key存在: true/false, Base URL: ...
   ```

### 步骤2：检查public/apikey.txt

确认文件位置：
```
项目根目录/
  └── public/
      └── apikey.txt  ← 应该在这里
```

检查文件内容：
```bash
cd public
cat apikey.txt
```

应该看到您的API Key（纯文本，无空行）

### 步骤3：手动输入测试

1. 清空输入框
2. 手动粘贴API Key
3. 点击"生成基础元素"测试
4. 查看控制台输出

### 步骤4：检查网络请求

1. 开发者工具切换到"Network"标签
2. 点击"生成"按钮
3. 查找请求到 `backgrace.com/v1/messages`
4. 检查：
   - Request Headers是否包含 `x-api-key`
   - Status Code是什么
   - Response是什么错误

## 可能的问题

### 问题1：API Key为空
**症状**：控制台显示 `API Key存在: false`
**解决**：
1. 检查`public/apikey.txt`是否存在
2. 或手动输入API Key

### 问题2：API Key格式错误
**症状**：请求发送但返回401/403
**解决**：
1. 检查API Key是否正确
2. 确认没有多余空格或换行

### 问题3：网络连接问题
**症状**：`ERR_CONNECTION_CLOSED`
**解决**：
1. 检查网络连接
2. 尝试访问 https://backgrace.com
3. 检查防火墙设置

### 问题4：CORS问题
**症状**：CORS policy error
**解决**：
1. 这是服务器端问题
2. 联系API服务提供商

## 快速诊断命令

在控制台运行：
```javascript
// 检查API配置
import { getApiConfig } from './services/apiConfig';
console.log(getApiConfig());
```

## 测试API连接

可以用curl测试：
```bash
curl -X POST https://backgrace.com/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-5-20250929",
    "max_tokens": 100,
    "messages": [{"role": "user", "content": "test"}]
  }'
```

## 下一步

请执行步骤1-3，然后告诉我看到的调试信息。

特别关注控制台中的：
- `[Debug] callClaude - API Key存在: ???`
- `[Debug] 发送请求到: ???`
- 任何其他错误信息
