# 开发一个公司人员管理系统

## 技术栈选择 Nuxt.js + Tailwindcss + Django + PostgreSQL

### 前端页面布局实现完成

我已经成功实现了前端的主要页面布局和设计理念，包括：

#### 1. 技术栈配置

- **Nuxt.js 3.17.4** - Vue.js 全栈框架
- **Tailwind CSS v4.1.8** - 原子化 CSS 框架（已成功迁移到 v4）
- **@nuxt/ui** - UI 组件库
- **@nuxt/icon** - 图标系统
- **@iconify-json/heroicons** - Heroicons 图标集

**TailwindCSS v4 迁移亮点**：

- 使用新的 `@tailwindcss/postcss` 插件
- 移除 `@nuxtjs/tailwindcss` 模块，改为手动集成
- 所有自定义配置完全兼容，无需修改组件代码
- 性能优化和更好的开发体验

#### 2. 设计系统

- **颜色主题**：

  - Primary: `#0284c7` (sky-600) - 主要操作按钮
  - Accent: `#10b981` (emerald-500) - 强调色，用于特殊操作
  - Success: `#10b981` (emerald-600) - 成功状态
  - Warning: `#f59e0b` (amber-500) - 警告状态
  - Danger: `#dc2626` (red-600) - 危险操作

- **字体系统**：
  - Sans: Inter 字体族
  - Mono: Fira Code 字体族

#### 3. 页面布局结构

##### 主布局 (`layouts/default.vue`)

- **顶部导航栏**：固定定位，包含系统标题、用户信息和退出按钮
- **侧边栏**：响应式设计，大屏幕固定显示，小屏幕可折叠
- **主内容区域**：自适应布局，支持各种屏幕尺寸
- **移动端优化**：汉堡菜单、触摸友好的交互

##### 员工管理页面 (`pages/employees/`)

- **员工列表** (`index.vue`)：

  - 搜索和筛选功能（姓名、工号、部门、职称）
  - 数据表格展示（支持排序）
  - 分页组件
  - 操作按钮（查看、编辑、删除）
  - 权限控制（管理员可见添加/编辑/删除）

- **添加员工** (`add.vue`)：

  - 分步骤表单（基本信息、工作信息）
  - 实时表单验证
  - 错误提示和成功反馈
  - 响应式布局

- **编辑员工** (`edit/[id].vue`)：
  - 预填充现有数据
  - 与添加页面相同的验证逻辑
  - 加载状态和错误处理

##### 薪资查询页面 (`pages/salaries/index.vue`)

- **搜索筛选**：员工搜索、部门筛选、薪资期间、薪资范围
- **数据表格**：完整的薪资信息展示
- **操作功能**：查看详情、打印、编辑、删除
- **计算薪资**：管理员专用的薪资计算模态框
- **分页和排序**：完整的数据操作功能

#### 4. 用户体验设计

##### 响应式设计

- **移动优先**：从小屏幕开始设计，逐步增强
- **断点系统**：sm (640px), md (768px), lg (1024px)
- **触摸友好**：按钮大小、间距适合触摸操作

##### 交互反馈

- **加载状态**：旋转动画指示器
- **悬停效果**：按钮和链接的视觉反馈
- **过渡动画**：平滑的状态切换
- **表单验证**：实时错误提示

##### 无障碍设计

- **语义化 HTML**：正确的标签使用
- **键盘导航**：支持 Tab 键导航
- **屏幕阅读器**：适当的 ARIA 标签
- **颜色对比度**：符合 WCAG 标准

#### 5. 组件化设计

##### 可复用组件

- **表格组件**：支持排序、分页、搜索
- **表单组件**：统一的输入框、选择器样式
- **模态框组件**：确认对话框、表单弹窗
- **按钮组件**：不同状态和尺寸的按钮

##### 状态管理

- **响应式数据**：Vue 3 Composition API
- **表单状态**：验证、提交、错误处理
- **UI 状态**：加载、模态框、侧边栏

#### 6. 开发体验

##### 代码组织

- **页面路由**：基于文件系统的路由
- **布局系统**：可复用的页面布局
- **组件结构**：清晰的组件层次
- **样式管理**：Tailwind 原子化类名

##### 开发工具

- **热重载**：实时预览代码更改
- **TypeScript**：类型安全
- **ESLint**：代码质量检查
- **开发服务器**：已成功启动在 localhost:3000

### 下一步计划

<!-- 1. **后端 API 集成**：连接 Django 后端服务
2. **状态管理**：实现全局状态管理（Pinia）
3. **认证系统**：用户登录、权限控制
4. **数据持久化**：真实的 CRUD 操作
5. **打印功能**：薪资单打印模板
6. **数据导出**：Excel/PDF 导出功能
7. **测试覆盖**：单元测试和集成测试 -->

## 各个index中的数据按需从后端数据库请求所需的数据

1. 将这个请求数据的方法单独抽象出来
2. 各个index按照自己所需要的规则去申请数据

## 绩效管理
数据库建表：
名称 工号(外键) 职位 所属部门  考核期间 状态 评级 分数 评估人 操作

py脚本生成相关的数据，只需要生成考核期间和状态，但是需要和名称或者工号关联起来。

department 里的部门列表的icon申请 -> 矢量图。

薪资查询界面没有实现过滤功能

### 技术特色

- **现代化技术栈**：Vue 3 + Nuxt 3 + Tailwind CSS
- **响应式设计**：完美适配各种设备
- **用户体验优先**：流畅的交互和反馈
- **可维护性**：清晰的代码结构和组件化
- **可扩展性**：模块化设计，易于添加新功能


待修复的bug：

<!-- 1. 修改首页图标不能正确显示的问题 
2. 将员工管理界面和薪资管理界面的数据接入api从vntdb获取
3. 使得添加员工界面更加平滑
4. 使得添加员工功能可以正常使用，并添加员工数据到vnt数据库中
5. 实现管理员可以在前端界面编辑信息
6. 更改button 
7. 修复数据库插入失败-->
8. 实现基于职位的不同薪资标准
9. 在salaries page添加搜索和打印功能
10. 重构页面UI
11. 解决employees的排序，按姓名排序，按工号排序并没有生效的问题
12. 解决salaries界面的计算薪资功能出现异常，无法正确计算薪资
