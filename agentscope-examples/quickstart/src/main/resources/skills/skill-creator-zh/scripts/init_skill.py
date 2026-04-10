# Copyright 2024-2026 the original author or authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#!/usr/bin/env python3
"""
技能初始化器 - 从模板创建新技能

用法：
    init_skill.py <skill-name> --path <path>

示例：
    init_skill.py my-new-skill --path skills/public
    init_skill.py my-api-helper --path skills/private
    init_skill.py custom-skill --path /custom/location
"""

import sys
from pathlib import Path


SKILL_TEMPLATE = """---
name: {skill_name}
description: [TODO: 完整且信息丰富的解释，说明技能做什么以及何时使用。包含何时使用此技能——特定场景、文件类型或触发它的任务。]
---

# {skill_title}

## 概览

[TODO: 1-2 句话解释此技能启用什么]

## 结构化此技能

[TODO: 选择最适合此技能目的的结构。常见模式：

**1. 工作流程型**（最适合顺序流程）
- 适用于有清晰逐步程序的情况
- 示例：DOCX 技能使用"工作流程决策树" → "读取" → "创建" → "编辑"
- 结构：## 概览 → ## 工作流程决策树 → ## 步骤 1 → ## 步骤 2...

**2. 任务型**（最适合工具集合）
- 适用于技能提供不同操作/能力的情况
- 示例：PDF 技能使用"快速开始" → "合并 PDF" → "拆分 PDF" → "提取文本"
- 结构：## 概览 → ## 快速开始 → ## 任务类别 1 → ## 任务类别 2...

**3. 参考/指南型**（最适合标准或规范）
- 适用于品牌指南、编码标准或需求
- 示例：品牌样式使用"品牌指南" → "颜色" → "字体" → "功能"
- 结构：## 概览 → ## 指南 → ## 规范 → ## 用法...

**4. 能力型**（最适合集成系统）
- 适用于技能提供多个相关功能的情况
- 示例：产品管理使用"核心能力" → 编号能力列表
- 结构：## 概览 → ## 核心能力 → ### 1. 功能 → ### 2. 功能...

模式可按需混合使用。大多数技能组合模式（如以任务型开始，为复杂操作添加工作流程）。

完成后删除整个"结构化此技能"部分——这只是指导。]

## [TODO: 根据所选结构替换为第一个主要章节]

[TODO: 在此添加内容。参见现有技能示例：
- 技术技能的代码示例
- 复杂工作流程的决策树
- 带真实用户请求的具体示例
- 按需引用脚本/模板/参考资料]

## 资源

本技能包含示例资源目录，演示如何组织不同类型的捆绑资源：

### scripts/
可直接运行的可执行代码（Python/Bash 等），用于执行特定操作。

**其他技能示例：**
- PDF 技能：`fill_fillable_fields.py`、`extract_form_field_info.py` - PDF 操作工具
- DOCX 技能：`document.py`、`utilities.py` - 文档处理 Python 模块

**适用于：** Python 脚本、shell 脚本或任何执行自动化、数据处理或特定操作的可执行代码。

**注意：** 脚本可在不加载到上下文的情况下执行，但仍可被 Claude 读取以便修补或环境调整。

### references/
文档和参考材料，按需加载到上下文中以指导 Claude 的过程和思考。

**其他技能示例：**
- 产品管理：`communication.md`、`context_building.md` - 详细工作流程指南
- BigQuery：API 参考文档和查询示例
- 财务：数据库模式文档、公司政策

**适用于：** 深度文档、API 参考、数据库模式、综合指南或 Claude 工作时应参考的任何详细信息。

### assets/
不打算加载到上下文中，而是在 Claude 产生的输出中使用的文件。

**其他技能示例：**
- 品牌样式：PowerPoint 模板文件（.pptx）、logo 文件
- 前端构建器：HTML/React 脚手架项目目录
- 字体：字体文件（.ttf, .woff2）

**适用于：** 模板、脚手架代码、文档模板、图片、图标、字体或任何意在复制或用于最终输出的文件。

---

**可删除任何不需要的目录。** 不是每个技能都需要所有三种类型的资源。
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
{skill_name} 的示例辅助脚本

这是一个可直接运行的占位符脚本。
替换为实际实现或在不需要时删除。

其他技能的实际脚本示例：
- pdf/scripts/fill_fillable_fields.py - 填写 PDF 表单字段
- pdf/scripts/convert_pdf_to_images.py - 将 PDF 页面转换为图片
"""

def main():
    print("这是 {skill_name} 的示例脚本")
    # TODO: 在此添加实际脚本逻辑
    # 可以是数据处理、文件转换、API 调用等

if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = """# {skill_title} 的参考文档

这是详细参考文档的占位符。
替换为实际参考内容或在不需要时删除。

其他技能的实际参考文档示例：
- product-management/references/communication.md - 状态更新的综合指南
- product-management/references/context_building.md - 收集上下文的深入指南
- bigquery/references/ - API 参考和查询示例

## 参考文档何时有用

参考文档适用于：
- 综合性 API 文档
- 详细工作流程指南
- 复杂多步骤流程
- 对 SKILL.md 过长的信息
- 仅在特定用例需要的内容

## 结构建议

### API 参考示例
- 概览
- 认证
- 带示例的端点
- 错误代码
- 速率限制

### 工作流程指南示例
- 前置条件
- 逐步说明
- 常见模式
- 故障排除
- 最佳实践
"""

EXAMPLE_ASSET = """# 示例资产文件

此占位符代表资产文件的存储位置。
替换为实际资产文件（模板、图片、字体等）或在不需要时删除。

资产文件不打算加载到上下文中，而是在 Claude 产生的输出中使用。

其他技能的资产文件示例：
- 品牌指南：logo.png、slides_template.pptx
- 前端构建器：包含 HTML/React 脚手架的 hello-world/ 目录
- 字体：custom-font.ttf、font-family.woff2
- 数据：sample_data.csv、test_dataset.json

## 常见资产类型

- 模板：.pptx、.docx、脚手架目录
- 图片：.png、.jpg、.svg、.gif
- 字体：.ttf、.otf、.woff、.woff2
- 脚手架代码：项目目录、起始文件
- 图标：.ico、.svg
- 数据文件：.csv、.json、.xml、.yaml

注意：这是文本占位符。实际资产可以是任何文件类型。
"""


def title_case_skill_name(skill_name):
    """将连字符分隔的技能名称转换为标题大小写用于显示。"""
    return ' '.join(word.capitalize() for word in skill_name.split('-'))


def init_skill(skill_name, path):
    """
    用模板 SKILL.md 初始化新技能目录。

    Args:
        skill_name: 技能名称
        path: 技能目录应创建的路径

    Returns:
        创建的技能目录路径，或出错时返回 None
    """
    # 确定技能目录路径
    skill_dir = Path(path).resolve() / skill_name

    # 检查目录是否已存在
    if skill_dir.exists():
        print(f"❌ 错误：技能目录已存在：{skill_dir}")
        return None

    # 创建技能目录
    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"✅ 已创建技能目录：{skill_dir}")
    except Exception as e:
        print(f"❌ 创建目录出错：{e}")
        return None

    # 从模板创建 SKILL.md
    skill_title = title_case_skill_name(skill_name)
    skill_content = SKILL_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=skill_title
    )

    skill_md_path = skill_dir / 'SKILL.md'
    try:
        skill_md_path.write_text(skill_content)
        print("✅ 已创建 SKILL.md")
    except Exception as e:
        print(f"❌ 创建 SKILL.md 出错：{e}")
        return None

    # 创建带示例文件的资源目录
    try:
        # 创建 scripts/ 目录及示例脚本
        scripts_dir = skill_dir / 'scripts'
        scripts_dir.mkdir(exist_ok=True)
        example_script = scripts_dir / 'example.py'
        example_script.write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name))
        example_script.chmod(0o755)
        print("✅ 已创建 scripts/example.py")

        # 创建 references/ 目录及示例参考文档
        references_dir = skill_dir / 'references'
        references_dir.mkdir(exist_ok=True)
        example_reference = references_dir / 'api_reference.md'
        example_reference.write_text(EXAMPLE_REFERENCE.format(skill_title=skill_title))
        print("✅ 已创建 references/api_reference.md")

        # 创建 assets/ 目录及示例资产占位符
        assets_dir = skill_dir / 'assets'
        assets_dir.mkdir(exist_ok=True)
        example_asset = assets_dir / 'example_asset.txt'
        example_asset.write_text(EXAMPLE_ASSET)
        print("✅ 已创建 assets/example_asset.txt")
    except Exception as e:
        print(f"❌ 创建资源目录出错：{e}")
        return None

    # 打印下一步
    print(f"\n✅ 技能 '{skill_name}' 已成功初始化于 {skill_dir}")
    print("\n下一步：")
    print("1. 编辑 SKILL.md 以完成 TODO 项目并更新描述")
    print("2. 定制或删除 scripts/、references/ 和 assets/ 中的示例文件")
    print("3. 准备好后运行验证器检查技能结构")

    return skill_dir


def main():
    if len(sys.argv) < 4 or sys.argv[2] != '--path':
        print("用法：init_skill.py <skill-name> --path <path>")
        print("\n技能名称要求：")
        print("  - 连字符分隔的标识符（如 'data-analyzer'）")
        print("  - 仅小写字母、数字和连字符")
        print("  - 最长 40 个字符")
        print("  - 必须与目录名称完全匹配")
        print("\n示例：")
        print("  init_skill.py my-new-skill --path skills/public")
        print("  init_skill.py my-api-helper --path skills/private")
        print("  init_skill.py custom-skill --path /custom/location")
        sys.exit(1)

    skill_name = sys.argv[1]
    path = sys.argv[3]

    print(f"🚀 正在初始化技能：{skill_name}")
    print(f"   位置：{path}")
    print()

    result = init_skill(skill_name, path)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()