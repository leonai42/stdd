# {{ meta.title }}

<!-- source_hash: {{ source_hash }} -->
<!-- generated_at: {{ generated_at }} -->
<!-- canonical: canonical/proposals/{{ change_id }}.yaml -->
<!-- 此文件从 Canonical YAML 单向生成，请勿手动编辑 -->

## Why

{{ why.problem }}

{{ why.motivation }}

## What Changes

{% for item in what_changes %}
- {{ item.description }}
{% endfor %}

## Capabilities

### New Capabilities

{% for cap in capabilities.new %}
- **{{ cap.name }}**：{{ cap.description }}
{% endfor %}

### Modified Capabilities

{% for cap in capabilities.modified %}
- **{{ cap.name }}**：{{ cap.description }}
{% endfor %}

## Constraints

{% for c in constraints %}
- {{ c }}
{% endfor %}

## NonGoals

{% for g in non_goals %}
- {{ g }}
{% endfor %}

## Success Criteria

{% for s in success_criteria %}
- [ ] {{ s }}
{% endfor %}
