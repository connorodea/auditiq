USER_PROMPT_TEMPLATE = """Generate an AI Readiness Assessment Report for the following company.

## COMPANY PROFILE
- Industry: {industry}
- Company Size: {company_size} employees
- Company Name: {company_name}

## ASSESSMENT SCORES (0-100 scale)
- Overall Score: {score_overall}/100 ({level_overall})
- Data Readiness: {score_data_readiness}/100 ({level_data_readiness})
- Process Maturity: {score_process_maturity}/100 ({level_process_maturity})
- Technology Infrastructure: {score_tech_infrastructure}/100 ({level_tech_infrastructure})
- Team Capability: {score_team_capability}/100 ({level_team_capability})
- Strategic Alignment: {score_strategic_alignment}/100 ({level_strategic_alignment})

## RAW RESPONSES
{formatted_responses}

## INDUSTRY BENCHMARK
- Industry median: {industry_median}/100
- Top quartile: {industry_top_quartile}/100
- This company vs median: {vs_median}

## REQUIRED OUTPUT SCHEMA
Respond with a JSON object matching this exact structure:

{{
  "executive_summary": {{
    "headline": "string — one compelling sentence summarizing readiness level",
    "summary": "string — 2-3 paragraph executive overview",
    "overall_assessment": "Nascent|Emerging|Established|Advanced",
    "key_finding": "string — single most important insight"
  }},
  "dimension_analysis": [
    {{
      "dimension": "data_readiness",
      "title": "Data Readiness",
      "score": 0,
      "level": "Nascent|Emerging|Established|Advanced",
      "analysis": "string — 2-3 paragraphs analyzing this dimension based on their specific answers",
      "strengths": ["string — specific strength based on answers"],
      "gaps": ["string — specific gap identified"],
      "priority": "high|medium|low"
    }}
  ],
  "opportunity_zones": [
    {{
      "title": "string — name of the AI opportunity",
      "description": "string — what this would look like implemented",
      "dimension_addressed": "string — primary dimension this improves",
      "effort": "low|medium|high",
      "impact": "low|medium|high",
      "timeline": "string — e.g., '4-6 weeks'",
      "estimated_roi": "string — e.g., '15-25% reduction in processing time'",
      "prerequisites": ["string — what needs to be true before starting"],
      "recommended_tools": ["string — specific tools or platforms to consider"]
    }}
  ],
  "implementation_roadmap": {{
    "phase_1_quick_wins": {{
      "timeline": "0-3 months",
      "initiatives": ["string — specific actionable items"],
      "expected_outcomes": ["string"],
      "estimated_investment": "string — cost range"
    }},
    "phase_2_foundation": {{
      "timeline": "3-6 months",
      "initiatives": ["string"],
      "expected_outcomes": ["string"],
      "estimated_investment": "string"
    }},
    "phase_3_scale": {{
      "timeline": "6-12 months",
      "initiatives": ["string"],
      "expected_outcomes": ["string"],
      "estimated_investment": "string"
    }}
  }},
  "roi_analysis": {{
    "estimated_annual_savings_range": "string — e.g., '$50,000 - $150,000'",
    "productivity_gain_estimate": "string — e.g., '20-30% in targeted processes'",
    "payback_period": "string — e.g., '4-8 months'",
    "key_assumptions": ["string — transparency about estimation basis"]
  }},
  "risk_factors": [
    {{
      "risk": "string — what could go wrong",
      "severity": "high|medium|low",
      "mitigation": "string — how to address it"
    }}
  ],
  "next_steps": [
    "string — immediate action item 1",
    "string — immediate action item 2",
    "string — immediate action item 3"
  ]
}}

Include exactly 5 entries in dimension_analysis (one per dimension).
Include 5-8 entries in opportunity_zones, ordered by effort/impact ratio (best first).
Include 3-5 entries in risk_factors.
Include exactly 3 entries in next_steps."""
