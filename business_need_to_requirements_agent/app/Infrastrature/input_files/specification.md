# Business Need to Requirements Agent — Specification

## 1. Objective

Generate standard JSON requirements from a business need.

The agent must produce two separate downstream-ready outputs:

1. `functional_requirements_output`
2. `non_functional_requirements_output`

Both outputs come from the same input but must remain structurally separate.

## 2. Input Schema

```json
{
  "TenderId": "",
  "CompanyId": "",

  "CanonicalRequirements": [],

  "RetrievedCompanyContext": [
    {
      "chunk_id": "",
      "text": "",
      "source": ""
    }
  ],

  "output_mode": "json_only"
}
```

Only `business_need` is mandatory.

## 3. Processing Flow

1. Read and normalise the business need.
2. Identify business objectives and value.
3. Identify user roles and system boundaries.
4. Generate business requirements.
5. Generate functional requirements in a dedicated schema.
6. Generate non-functional requirements in a dedicated schema.
7. Generate shared data, integration, assumption, risk and open-question sections.
8. Validate JSON.
9. Return JSON only.

## 4. Requirement ID Format

Use the following ID prefixes:

- Business requirements: `BR-001`
- Functional requirements: `FR-001`
- Non-functional requirements: `NFR-001`
- Data requirements: `DR-001`
- Integration requirements: `IR-001`
- Assumptions: `ASM-001`
- Risks: `RSK-001`
- Open questions: `Q-001`

## 5. Standard Output Schema

```json
{
  "metadata": {
    "project_name": "",
    "generated_date": "YYYY-MM-DD",
    "agent_version": "1.1",
    "output_mode": "json_only"
  },
  "input_summary": {
    "business_need": "",
    "business_objectives": [],
    "target_users": [],
    "scope_summary": "",
    "constraints_summary": ""
  },
  "business_requirements": [
    {
      "id": "BR-001",
      "title": "",
      "description": "",
      "business_value": "",
      "priority": "must | should | could | wont",
      "confidence": "high | medium | low",
      "source": "user_input | inferred | assumption"
    }
  ],
  "functional_requirements_output": {
    "summary": {
      "total_count": 0,
      "must_count": 0,
      "should_count": 0,
      "could_count": 0,
      "low_confidence_count": 0
    },
    "requirements": [
      {
        "id": "FR-001",
        "title": "",
        "description": "The system shall ...",
        "requirement_type": "functional",
        "module_or_capability": "",
        "user_roles": [],
        "trigger": "",
        "preconditions": [],
        "main_flow": [],
        "alternative_flows": [],
        "business_rules": [],
        "acceptance_criteria": [],
        "related_business_requirements": [],
        "related_data_requirements": [],
        "related_integration_requirements": [],
        "priority": "must | should | could | wont",
        "confidence": "high | medium | low",
        "source": "user_input | inferred | assumption",
        "requires_human_validation": true
      }
    ]
  },
  "non_functional_requirements_output": {
    "summary": {
      "total_count": 0,
      "must_count": 0,
      "should_count": 0,
      "could_count": 0,
      "low_confidence_count": 0
    },
    "requirements": [
      {
        "id": "NFR-001",
        "title": "",
        "description": "The system shall ...",
        "requirement_type": "non_functional",
        "category": "security | privacy | performance | availability | scalability | reliability | auditability | compliance | maintainability | usability | accessibility | observability | data_retention",
        "quality_attribute": "",
        "measurement_or_acceptance": "",
        "applies_to": [],
        "related_functional_requirements": [],
        "related_business_requirements": [],
        "priority": "must | should | could | wont",
        "confidence": "high | medium | low",
        "source": "user_input | inferred | assumption",
        "requires_human_validation": true
      }
    ]
  },
  "data_requirements": [
    {
      "id": "DR-001",
      "data_object": "",
      "description": "",
      "source": "",
      "consumer": "",
      "sensitivity": "public | internal | confidential | restricted | unknown",
      "retention_requirement": "",
      "related_functional_requirements": []
    }
  ],
  "integration_requirements": [
    {
      "id": "IR-001",
      "system_name": "",
      "purpose": "",
      "direction": "inbound | outbound | bidirectional | unknown",
      "data_exchanged": [],
      "related_functional_requirements": [],
      "confidence": "high | medium | low"
    }
  ],
  "assumptions": [
    {
      "id": "ASM-001",
      "description": "",
      "impact": "",
      "validation_needed": true
    }
  ],
  "risks": [
    {
      "id": "RSK-001",
      "risk": "",
      "impact": "",
      "mitigation": "",
      "severity": "high | medium | low"
    }
  ],
  "open_questions": [
    {
      "id": "Q-001",
      "question": "",
      "why_it_matters": "",
      "related_requirement_ids": []
    }
  ],
  "downstream_agent_handoff": {
    "recommended_next_agent": "SRS Generator",
    "ready_for_srs": true,
    "functional_requirements_ready": true,
    "non_functional_requirements_ready": true,
    "blocking_questions": [],
    "notes": []
  }
}
```

## 6. Functional Requirement Generation Rules

Functional requirements must cover relevant system behaviours such as:

- Input capture
- File upload
- Data extraction
- Search and retrieval
- Matching
- Validation
- Workflow
- Review and approval
- Notification
- Export
- Reporting
- Administration
- Audit log viewing

Each functional requirement must include acceptance criteria.

## 7. Non-Functional Requirement Generation Rules

Non-functional requirements must cover relevant quality areas such as:

- Security
- Privacy
- Performance
- Availability
- Scalability
- Reliability
- Auditability
- Compliance
- Maintainability
- Usability
- Accessibility
- Observability
- Data retention

Each non-functional requirement must include `measurement_or_acceptance`.

## 8. Priority Rules

Use MoSCoW:

- `must`: essential
- `should`: important
- `could`: useful enhancement
- `wont`: explicitly out of scope

## 9. Confidence Rules

- `high`: directly stated by the user
- `medium`: strongly implied by the business need
- `low`: inferred assumption requiring validation

## 10. Validation Checklist

Before returning output:

1. JSON is valid.
2. Functional and non-functional outputs are separate.
3. Every functional requirement starts with “The system shall”.
4. Every non-functional requirement starts with “The system shall”.
5. Functional requirements include acceptance criteria.
6. Non-functional requirements include measurement or acceptance.
7. Requirements have priority, confidence and source.
8. Assumptions and open questions are explicit.
9. No markdown is returned in JSON-only mode.
