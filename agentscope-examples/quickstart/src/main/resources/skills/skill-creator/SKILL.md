---
name: skill-creator
description: Guide for creating effective skills with optional MySQL persistence. This skill should be used when users want to create a new skill (or update an existing skill) that extends capabilities with specialized knowledge, workflows, or tool integrations. Supports saving skills to MySQL database.
---

# Skill Creator

This skill provides guidance for creating effective skills and optionally persisting them to MySQL database.

## About Skills

Skills are modular, self-contained packages that extend capabilities by providing specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific domains or tasks—they transform a general-purpose agent into a specialized agent equipped with procedural knowledge.

### What Skills Provide

1. **Specialized workflows** - Multi-step procedures for specific domains
2. **Tool integrations** - Instructions for working with specific file formats or APIs
3. **Domain expertise** - Company-specific knowledge, schemas, business logic
4. **Bundled resources** - Scripts, references, and assets for complex tasks

## Core Principles

### Concise is Key

The context window is a public good. Skills share the context window with everything else: system prompt, conversation history, other skills' metadata, and the actual user request.

**Default assumption: The agent is already very smart.** Only add context it doesn't already have. Challenge each piece: "Does it really need this?" and "Does this justify its token cost?"

Prefer concise examples over verbose explanations.

### Set Appropriate Degrees of Freedom

Match specificity to task fragility:

- **High freedom (text-based)**: Multiple valid approaches, context-dependent decisions
- **Medium freedom (pseudocode/scripts with parameters)**: Preferred pattern exists, some variation acceptable
- **Low freedom (specific scripts)**: Fragile operations, consistency critical

### Anatomy of a Skill

Every skill consists of a required SKILL.md file:

```
skill-name/
└── SKILL.md (required)
    ├── YAML frontmatter with name and description
    └── Markdown instructions
```

**SKILL.md structure:**
- **Frontmatter (YAML)**: Contains `name` and `description` fields—these determine when the skill gets used
- **Body (Markdown)**: Instructions loaded AFTER skill triggers

### Progressive Disclosure

Skills use three-level loading:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **References** - As needed (unlimited, loaded on demand)

## Skill Creation Process

### Step 1: Understand with Concrete Examples

Ask clarifying questions:
- "What functionality should this skill support?"
- "Can you give examples of how this skill would be used?"
- "What would trigger this skill?"

### Step 2: Initialize the Skill

Use `init_skill.py` to create the skill structure:

```bash
python scripts/init_skill.py <skill-name> --path <output-directory>
```

This creates:
- `SKILL.md` - Template with proper frontmatter
- Skill directory with the specified name

### Step 3: Write SKILL.md Content

**Frontmatter requirements:**
```yaml
---
name: my-skill-name
description: Clear explanation of what this skill does and when to use it. Include specific triggers and use cases.
---
```

**Writing guidelines:**
- Use imperative/infinitive form
- Keep under 500 lines
- Include concrete examples
- Link to references for detailed info

### Step 4: Save to MySQL (Optional)

To persist the skill to MySQL database, use the `save_skill_to_mysql.py` script:

```bash
python scripts/save_skill_to_mysql.py <path/to/SKILL.md> --db-config <db-config-path>
```

Or with inline configuration:
```bash
python scripts/save_skill_to_mysql.py <path/to/SKILL.md> \
    --host localhost \
    --port 3306 \
    --database agentscope \
    --user root \
    --password secret
```

**Database configuration file format (JSON):**
```json
{
    "host": "localhost",
    "port": 3306,
    "database": "agentscope",
    "user": "root",
    "password": "your_password",
    "skills_table": "agentscope_skills",
    "resources_table": "agentscope_skill_resources"
}
```

The script will:
- Parse the SKILL.md file
- Extract metadata from frontmatter
- Save to MySQL with the skill content
- Return the skill ID on success

### Step 5: Validate and Package

Validate the skill:
```bash
python scripts/quick_validate.py <skill-directory>
```

Package for distribution:
```bash
python scripts/package_skill.py <skill-directory> [output-dir]
```

## File Tools

When creating skills, use these file operations:

- **write_text_file** - Create SKILL.md with proper frontmatter
- **read_text_file** - Read existing skills as reference
- **create_directory** - Create skill directory structure

## MySQL Integration

The MySQL skill repository provides:

- Automatic table creation
- UTF-8 (utf8mb4) support for internationalization
- Transaction support for atomic operations
- Full CRUD operations

**Table Schema:**

```sql
CREATE TABLE agentscope_skills (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT NOT NULL,
    skill_content LONGTEXT NOT NULL,
    source VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## Example: Creating a Data Analysis Skill

**User request:** "Create a skill for analyzing CSV files"

**Process:**

1. **Understand requirements**
   - What analysis features? (stats, charts, filtering)
   - What triggers this skill? ("analyze this CSV", "show me trends")

2. **Initialize skill**
   ```bash
   python scripts/init_skill.py csv-analyzer --path ./skills
   ```

3. **Edit SKILL.md**
   ```markdown
   ---
   name: csv-analyzer
   description: Analyze CSV files to generate statistics, detect patterns, and create visualizations. Use when users want to analyze tabular data, compute aggregates, find correlations, or generate insights from CSV files.
   ---

   # CSV Analyzer

   ## Overview

   This skill enables analysis of CSV files with statistical computations and visualization recommendations.

   ## Capabilities

   - Load and validate CSV files
   - Generate descriptive statistics (mean, median, std dev)
   - Detect data types and missing values
   - Identify correlations between columns
   - Recommend appropriate visualizations

   ## Usage

   When given a CSV file:

   1. Load and inspect structure
   2. Generate summary statistics
   3. Identify patterns and anomalies
   4. Suggest visualizations
   ```

4. **Save to MySQL (optional)**
   ```bash
   python scripts/save_skill_to_mysql.py ./skills/csv-analyzer/SKILL.md --db-config db.json
   ```

5. **Validate**
   ```bash
   python scripts/quick_validate.py ./skills/csv-analyzer
   ```