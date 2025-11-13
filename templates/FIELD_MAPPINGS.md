# Jira Field Mappings

This document contains the mappings between human-readable template values and actual Jira field IDs.

## Project Mappings

| Human-Readable | Jira Project ID | Description |
|----------------|-----------------|-------------|
| `RTDEV` | `10129` | Artifactory Lifecycle Management |
| `APP` | `10246` | Customer-Facing Application |

## Issue Type Mappings

| Human-Readable | Jira Issue Type ID | Description |
|----------------|-------------------|-------------|
| `epic` | `10000` | Epic issue type |
| `story` | `10001` | User story issue type |
| `task` | `10003` | Task issue type |
| `bug` | `10004` | Bug issue type |

## Team Mappings

| Human-Readable | Jira Team ID | Project | Description |
|----------------|--------------|---------|-------------|
| `dev-artifactory-lifecycle` | `10145` | RTDEV | Main RTDEV lifecycle team |
| `app-core` | `12980` | APP | Core APP development team |
| `security-team` | `10146` | RTDEV | RTDEV security specialists |
| `platform-team` | `10147` | RTDEV | RTDEV platform infrastructure |
| `devops-team` | `10149` | RTDEV | RTDEV CI/CD and operations |
| `qa-team` | `10150` | RTDEV | RTDEV quality assurance |
| `performance-team` | `10151` | RTDEV | RTDEV performance optimization |
| `data-team` | `10152` | RTDEV | RTDEV data and analytics |


## Priority Mappings

| Human-Readable | Jira Priority ID | Description |
|----------------|------------------|-------------|
| `Blocker` | `1` | Blocks development/production |
| `Highest` | `2` | Highest priority |
| `Critical` | `3` | Critical priority |
| `High` | `4` | High priority |
| `Normal` | `5` | Normal priority (default) |
| `Minor` | `6` | Minor priority |
| `Low` | `7` | Low priority |
| `Trivial` | `8` | Trivial priority |

## Commitment Level Mappings

| Human-Readable | Jira Value ID | Description |
|----------------|---------------|-------------|
| `Hard Commitment` | `12345` | Firm commitment to deliver |
| `Soft Commitment` | `12346` | Best effort commitment |
| `KTLO` | `12347` | Keep the lights on |

## Area Mappings

| Human-Readable | Jira Value ID | Description |
|----------------|---------------|-------------|
| `Features & Innovation` | `23456` | New features and innovation |
| `Enablers & Tech Debt` | `23457` | Technical enablers and debt |
| `KTLO` | `23458` | Keep the lights on work |

## Commitment Reason Mappings

| Human-Readable | Jira Value ID | Description |
|----------------|---------------|-------------|
| `Roadmap` | `34567` | Part of product roadmap |
| `Customer Commitment` | `34568` | Committed to customer |
| `Security` | `34569` | Security requirement |

## Product Priority Mappings

| Human-Readable | Jira Value ID | Description |
|----------------|---------------|-------------|
| `P0` | `45678` | Highest product priority |
| `P1` | `45679` | High product priority |
| `P2` | `45680` | Medium product priority |
| `P3` | `45681` | Low product priority |
| `P4` | `45682` | Lowest product priority |

## Custom Field Mappings

| Field Name | Custom Field ID | Description |
|------------|-----------------|-------------|
| `team` | `customfield_10129` | Team Assignment |
| `product_backlog` | `customfield_10119` | Product Backlog |
| `product_manager` | `customfield_10044` | Product Manager |
| `commitment_level` | `customfield_10450` | Commitment Level |
| `area` | `customfield_10167` | Area |
| `commitment_reason` | `customfield_10508` | Commitment Reason |
| `product_priority` | `customfield_10327` | Product Priority |
| `ux_designer` | `customfield_10200` | UX Designer |
| `technical_writer` | `customfield_10201` | Technical Writer |
| `architect` | `customfield_10202` | Architect |

## Special Field Formats

### Product Backlog Format
- Format: `Qx-2x-Backlog` or `Qx-2x-Candidate`
- Examples: `Q4-25-Backlog`, `Q1-26-Candidate`

### User Account IDs
- Product Manager default: `yonatan.philip`
- Format: Jira account ID or username

## Template Usage

In templates, use the human-readable values:

```json
{
  "fields": {
    "project": "RTDEV",
    "issue_type": "epic",
    "team": "dev-artifactory-lifecycle",
    "priority": "Normal",
    "commitment_level": "Hard Commitment",
    "area": "Features & Innovation",
    "commitment_reason": "Roadmap"
  }
}
```

The system will automatically translate these to the correct Jira field IDs and values.
