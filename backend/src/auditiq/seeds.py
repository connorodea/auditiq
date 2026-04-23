"""Seed database with default tenant and questions."""

import asyncio
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auditiq.db.engine import async_session
from auditiq.db.models.question import Question
from auditiq.db.models.tenant import Tenant


QUESTIONS = [
    # ── Dimension 1: Data Readiness (Q1-Q3) ──
    {
        "sequence": 1,
        "dimension": "data_readiness",
        "question_text": "How would you describe your organization's current data management practices?",
        "question_type": "single_choice",
        "weight": 1.0,
        "industry_filter": None,
        "help_text": "Think about how customer, financial, and operational data is currently stored and accessed.",
        "options": [
            {"value": "a", "label": "We mostly use spreadsheets, paper records, and manual tracking", "score": 1},
            {"value": "b", "label": "We have some databases but data is siloed across departments", "score": 2},
            {"value": "c", "label": "We have centralized data systems with some cross-department integration", "score": 3},
            {"value": "d", "label": "We have a modern data stack with automated pipelines and a single source of truth", "score": 4},
        ],
    },
    {
        "sequence": 2,
        "dimension": "data_readiness",
        "question_text": "How much of your critical business data is digitized and structured?",
        "question_type": "single_choice",
        "weight": 1.0,
        "industry_filter": None,
        "help_text": "Consider customer records, financials, inventory, communications, and operational data.",
        "options": [
            {"value": "a", "label": "Less than 25% — most records are physical or unstructured", "score": 1},
            {"value": "b", "label": "25-50% — we've started digitizing but significant gaps remain", "score": 2},
            {"value": "c", "label": "50-80% — most key data is digital with some legacy gaps", "score": 3},
            {"value": "d", "label": "Over 80% — nearly all data is digitized, tagged, and queryable", "score": 4},
        ],
    },
    {
        "sequence": 3,
        "dimension": "data_readiness",
        "question_text": "How do you currently handle data quality and governance?",
        "question_type": "single_choice",
        "weight": 1.0,
        "industry_filter": None,
        "help_text": "Data governance includes policies, standards, and processes for maintaining data accuracy.",
        "options": [
            {"value": "a", "label": "No formal processes — data quality issues are addressed ad hoc", "score": 1},
            {"value": "b", "label": "Some informal standards exist but enforcement is inconsistent", "score": 2},
            {"value": "c", "label": "We have documented data quality standards with periodic audits", "score": 3},
            {"value": "d", "label": "We have automated data validation, dedicated governance roles, and continuous monitoring", "score": 4},
        ],
    },

    # ── Dimension 2: Process Maturity (Q4-Q6) ──
    {
        "sequence": 4,
        "dimension": "process_maturity",
        "question_text": "How standardized and documented are your core business workflows?",
        "question_type": "single_choice",
        "weight": 1.0,
        "industry_filter": None,
        "help_text": "Consider sales, onboarding, fulfillment, support, and internal operations.",
        "options": [
            {"value": "a", "label": "Most processes live in people's heads — very little documentation", "score": 1},
            {"value": "b", "label": "Key processes are documented but rarely updated or followed consistently", "score": 2},
            {"value": "c", "label": "Processes are documented, reviewed periodically, and mostly followed", "score": 3},
            {"value": "d", "label": "Processes are documented in a central system with version control, KPIs, and regular optimization", "score": 4},
        ],
    },
    {
        "sequence": 5,
        "dimension": "process_maturity",
        "question_text": "What is your current level of workflow automation?",
        "question_type": "single_choice",
        "weight": 1.0,
        "industry_filter": None,
        "help_text": "Automation includes email workflows, form routing, data entry, approvals, and notifications.",
        "options": [
            {"value": "a", "label": "Almost everything is manual — email, phone, paper-based handoffs", "score": 1},
            {"value": "b", "label": "We use some basic automation (email rules, simple macros, form submissions)", "score": 2},
            {"value": "c", "label": "We have workflow automation tools (Zapier, Power Automate) connecting several systems", "score": 3},
            {"value": "d", "label": "We have end-to-end automated workflows with exception handling and monitoring", "score": 4},
        ],
    },
    {
        "sequence": 6,
        "dimension": "process_maturity",
        "question_text": "How do you currently measure and optimize process performance?",
        "question_type": "single_choice",
        "weight": 1.0,
        "industry_filter": None,
        "help_text": "Think about how you track efficiency, throughput, error rates, and cycle times.",
        "options": [
            {"value": "a", "label": "We don't systematically track process metrics", "score": 1},
            {"value": "b", "label": "We track a few KPIs manually (monthly reports, spreadsheets)", "score": 2},
            {"value": "c", "label": "We have dashboards tracking key process metrics in near real-time", "score": 3},
            {"value": "d", "label": "We have automated performance monitoring with alerts, bottleneck detection, and continuous improvement cycles", "score": 4},
        ],
    },

    # ── Dimension 3: Technology Infrastructure (Q7-Q9) ──
    {
        "sequence": 7,
        "dimension": "tech_infrastructure",
        "question_text": "What best describes your current technology stack?",
        "question_type": "single_choice",
        "weight": 1.0,
        "industry_filter": None,
        "help_text": "Consider your core business applications, hosting, and integration capabilities.",
        "options": [
            {"value": "a", "label": "Primarily legacy systems with limited integration capabilities", "score": 1},
            {"value": "b", "label": "Mix of legacy and modern tools with some API integrations", "score": 2},
            {"value": "c", "label": "Mostly cloud-based SaaS tools with standard integrations", "score": 3},
            {"value": "d", "label": "Cloud-native stack with robust APIs, microservices, and infrastructure-as-code", "score": 4},
        ],
    },
    {
        "sequence": 8,
        "dimension": "tech_infrastructure",
        "question_text": "How would you rate your organization's cybersecurity and IT governance posture?",
        "question_type": "single_choice",
        "weight": 1.0,
        "industry_filter": None,
        "help_text": "Security posture affects AI readiness — AI systems need secure data handling.",
        "options": [
            {"value": "a", "label": "Basic antivirus and firewalls — no formal security program", "score": 1},
            {"value": "b", "label": "Some security policies exist but enforcement and monitoring are limited", "score": 2},
            {"value": "c", "label": "Formal security program with regular assessments, MFA, and incident response plans", "score": 3},
            {"value": "d", "label": "Mature security operations with SIEM, zero-trust architecture, compliance certifications (SOC2/ISO27001)", "score": 4},
        ],
    },
    # Q9 — Healthcare variant
    {
        "sequence": 9,
        "dimension": "tech_infrastructure",
        "question_text": "Do you have EHR/EMR systems that support FHIR or HL7 integration?",
        "question_type": "single_choice",
        "weight": 1.0,
        "industry_filter": ["healthcare"],
        "help_text": "Integration standards determine how easily AI tools can access clinical data.",
        "options": [
            {"value": "a", "label": "Very difficult — most systems are closed or require manual exports", "score": 1},
            {"value": "b", "label": "Possible but requires significant custom development", "score": 2},
            {"value": "c", "label": "Most systems have standard APIs or integration connectors", "score": 3},
            {"value": "d", "label": "Fully interoperable — we can plug in new tools within days", "score": 4},
        ],
    },
    # Q9 — Finance variant
    {
        "sequence": 9,
        "dimension": "tech_infrastructure",
        "question_text": "Do your core banking or trading systems expose APIs for third-party integration?",
        "question_type": "single_choice",
        "weight": 1.0,
        "industry_filter": ["finance"],
        "help_text": "API access determines how AI tools can interact with your financial systems.",
        "options": [
            {"value": "a", "label": "Very difficult — most systems are closed or require manual exports", "score": 1},
            {"value": "b", "label": "Possible but requires significant custom development", "score": 2},
            {"value": "c", "label": "Most systems have standard APIs or integration connectors", "score": 3},
            {"value": "d", "label": "Fully interoperable — we can plug in new tools within days", "score": 4},
        ],
    },
    # Q9 — Retail/E-commerce variant
    {
        "sequence": 9,
        "dimension": "tech_infrastructure",
        "question_text": "How integrated are your POS, inventory, and e-commerce platforms?",
        "question_type": "single_choice",
        "weight": 1.0,
        "industry_filter": ["retail", "ecommerce"],
        "help_text": "Connected systems enable AI-powered demand forecasting, pricing, and personalization.",
        "options": [
            {"value": "a", "label": "Very difficult — most systems are closed or require manual exports", "score": 1},
            {"value": "b", "label": "Possible but requires significant custom development", "score": 2},
            {"value": "c", "label": "Most systems have standard APIs or integration connectors", "score": 3},
            {"value": "d", "label": "Fully interoperable — we can plug in new tools within days", "score": 4},
        ],
    },
    # Q9 — Default variant (all other industries)
    {
        "sequence": 9,
        "dimension": "tech_infrastructure",
        "question_text": "How easily can your current systems exchange data with new tools or platforms?",
        "question_type": "single_choice",
        "weight": 1.0,
        "industry_filter": [
            "manufacturing", "professional_services", "technology", "education",
            "real_estate", "construction", "logistics", "hospitality", "legal", "other",
        ],
        "help_text": "Integration capability determines how quickly you can adopt AI tools.",
        "options": [
            {"value": "a", "label": "Very difficult — most systems are closed or require manual exports", "score": 1},
            {"value": "b", "label": "Possible but requires significant custom development", "score": 2},
            {"value": "c", "label": "Most systems have standard APIs or integration connectors", "score": 3},
            {"value": "d", "label": "Fully interoperable — we can plug in new tools within days", "score": 4},
        ],
    },

    # ── Dimension 4: Team Capability (Q10-Q12) ──
    {
        "sequence": 10,
        "dimension": "team_capability",
        "question_text": "What is your team's current familiarity with AI/ML concepts?",
        "question_type": "single_choice",
        "weight": 1.0,
        "industry_filter": None,
        "help_text": "Consider awareness across leadership, operations, and technical staff.",
        "options": [
            {"value": "a", "label": "Very limited — most staff have no exposure to AI beyond consumer apps", "score": 1},
            {"value": "b", "label": "Some awareness — a few team members have experimented with AI tools", "score": 2},
            {"value": "c", "label": "Moderate — multiple team members actively use AI tools and understand capabilities", "score": 3},
            {"value": "d", "label": "Strong — we have dedicated data science/AI staff or extensive cross-team AI literacy", "score": 4},
        ],
    },
    {
        "sequence": 11,
        "dimension": "team_capability",
        "question_text": "How does your organization typically approach adopting new technology?",
        "question_type": "single_choice",
        "weight": 1.0,
        "industry_filter": None,
        "help_text": "Your adoption culture affects how quickly AI initiatives can be implemented.",
        "options": [
            {"value": "a", "label": "Very cautious — we wait until technology is well-established and competitors have adopted", "score": 1},
            {"value": "b", "label": "Selective — we adopt when there's a clear proven ROI in our industry", "score": 2},
            {"value": "c", "label": "Progressive — we actively pilot new technologies and have a formal evaluation process", "score": 3},
            {"value": "d", "label": "Aggressive — we have an innovation budget, run experiments, and accept measured risk", "score": 4},
        ],
    },
    {
        "sequence": 12,
        "dimension": "team_capability",
        "question_text": "Do you have internal champions or a team responsible for driving digital transformation?",
        "question_type": "single_choice",
        "weight": 1.0,
        "industry_filter": None,
        "help_text": "Change management and internal advocacy are critical for AI adoption success.",
        "options": [
            {"value": "a", "label": "No — technology decisions are made ad hoc by individual department heads", "score": 1},
            {"value": "b", "label": "Informally — one or two people push for change but it's not their dedicated role", "score": 2},
            {"value": "c", "label": "Yes — we have a designated person or small team focused on digital initiatives", "score": 3},
            {"value": "d", "label": "Yes — we have a Chief Digital/Technology Officer with budget, mandate, and cross-functional authority", "score": 4},
        ],
    },

    # ── Dimension 5: Strategic Alignment (Q13-Q15) ──
    {
        "sequence": 13,
        "dimension": "strategic_alignment",
        "question_text": "Does your organization have a formal AI or digital transformation strategy?",
        "question_type": "single_choice",
        "weight": 1.0,
        "industry_filter": None,
        "help_text": "A documented strategy signals organizational commitment and direction.",
        "options": [
            {"value": "a", "label": "No — we haven't discussed AI strategy at a leadership level", "score": 1},
            {"value": "b", "label": "We've discussed it informally but have no documented plan or budget", "score": 2},
            {"value": "c", "label": "We have a basic roadmap with some identified use cases and allocated budget", "score": 3},
            {"value": "d", "label": "We have a comprehensive AI strategy tied to business objectives with executive sponsorship and KPIs", "score": 4},
        ],
    },
    {
        "sequence": 14,
        "dimension": "strategic_alignment",
        "question_text": "What is driving your interest in AI adoption?",
        "question_type": "single_choice",
        "weight": 1.0,
        "industry_filter": None,
        "help_text": "Understanding your motivation helps us tailor recommendations to your goals.",
        "options": [
            {"value": "a", "label": "Mostly curiosity or pressure from competitors — no specific goal yet", "score": 1},
            {"value": "b", "label": "Cost reduction — we want to do more with less", "score": 2},
            {"value": "c", "label": "Revenue growth — we see AI as a way to create new products, services, or markets", "score": 3},
            {"value": "d", "label": "Competitive moat — AI is central to our long-term competitive advantage", "score": 4},
        ],
    },
    {
        "sequence": 15,
        "dimension": "strategic_alignment",
        "question_text": "What is your budget expectation for AI initiatives in the next 12 months?",
        "question_type": "single_choice",
        "weight": 1.0,
        "industry_filter": None,
        "help_text": "Budget signals commitment level and determines the scope of what's achievable.",
        "options": [
            {"value": "a", "label": "Under $10,000 — exploring only", "score": 1},
            {"value": "b", "label": "$10,000-$50,000 — ready to pilot one or two projects", "score": 2},
            {"value": "c", "label": "$50,000-$200,000 — committed to meaningful implementation", "score": 3},
            {"value": "d", "label": "Over $200,000 — AI is a strategic priority with significant investment", "score": 4},
        ],
    },
]


async def seed_database() -> None:
    """Seed the database with default tenant and questions."""
    async with async_session() as db:
        # Seed default tenant
        stmt = select(Tenant).where(Tenant.slug == "app")
        result = await db.execute(stmt)
        if not result.scalar_one_or_none():
            tenant = Tenant(slug="app", name="AuditIQ")
            db.add(tenant)
            print("Created default tenant: AuditIQ")

        # Seed questions
        stmt = select(Question)
        result = await db.execute(stmt)
        existing = list(result.scalars().all())
        if len(existing) == 0:
            for q_data in QUESTIONS:
                q = Question(
                    id=uuid.uuid4(),
                    sequence=q_data["sequence"],
                    dimension=q_data["dimension"],
                    question_text=q_data["question_text"],
                    question_type=q_data["question_type"],
                    options=q_data["options"],
                    weight=q_data["weight"],
                    industry_filter=q_data["industry_filter"],
                    help_text=q_data.get("help_text"),
                )
                db.add(q)
            print(f"Seeded {len(QUESTIONS)} questions")
        else:
            print(f"Questions already exist ({len(existing)}), skipping seed")

        await db.commit()


if __name__ == "__main__":
    asyncio.run(seed_database())
