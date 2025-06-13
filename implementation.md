= SPEC-1: API Architecture for AI Productivity Assistant
:sectnums:
:toc:


== Background

The AI Productivity Assistant enables users to manage tasks, integrate external services like Google Calendar, and chat with an LLM for productivity support. The backend must support clean extensibility for integrations and conversational APIs, with secure session management and modular design.


== Requirements

*Must Have*
- [x] Handle Supabase-based signup and login flows
- [x] Support secure OAuth integration with Google Calendar
- [x] Provide a chat endpoint that communicates with an LLM

*Should Have*
- [ ] Company and task management
- [ ] Token refresh and integration error handling

*Could Have*
- [ ] Rate limiting and logging middleware
- [ ] Multi-tenant support

*Won't Have*
- [ ] Billing system (out of scope for MVP)


== Method

=== Architectural Pattern
- **Hexagonal Architecture (Ports and Adapters)**
  - Promotes clean separation of business logic from external systems
  - Adapters: HTTP, Supabase, OAuth providers, LLM client
  - Ports: Use cases for Auth, Chat, Integrations, Task, Company

=== Core Components
- **API Layer**: FastAPI routers for each domain
- **Service Layer**: Core logic per domain (auth, chat, etc.)
- **Domain Models**: Pydantic + ORM models
- **Persistence Layer**: Supabase client wrapper
- **Integration Layer**: External API adapters (e.g., Google, LLM)
- **Security Layer**: Token validation, session middleware

=== Token Management
- Supabase JWT is used post-login, stored in HTTP-only cookie
- Access token verified on each request
- Refresh handled by Supabase or custom token refresh endpoint

=== External Integrations
- Google OAuth 2.0 with offline scope
- Store refresh tokens encrypted in Supabase DB
- Use background tasks or Celery for token renewal

=== Project Structure
```
api_assistant/
├── main.py
├── api/              # FastAPI routers
│   ├── auth.py
│   ├── chat.py
│   ├── integrations.py
│   ├── tasks.py
│   └── companies.py
├── services/         # Business logic
│   ├── auth_service.py
│   ├── chat_service.py
│   ├── integration_service.py
│   ├── task_service.py
│   └── company_service.py
├── db/               # Supabase wrappers
│   └── client.py
├── integrations/     # Third-party logic
│   ├── google_calendar.py
│   └── llm.py
├── models/           # Pydantic and ORM models
├── core/             # Token, config, logging, utils
│   ├── config.py
│   ├── security.py
│   └── logging.py
└── tests/
```

=== Component Diagram
[plantuml]
----
@startuml
component FastAPI as API
component "Auth Service" as Auth
component "Chat Service" as Chat
component "Google Adapter" as Google
component "LLM Adapter" as LLM
component "Supabase DB" as DB
API --> Auth
API --> Chat
Auth --> DB
Chat --> LLM
API --> Google
Google --> DB
@enduml
----

== Implementation

=== v1.0
- Setup FastAPI with routers and basic middleware
- Implement Supabase user auth via `auth_service`
- Integrate Google OAuth adapter and store credentials
- Build chat endpoint with LLM adapter (streaming)

=== v1.1
- Add `companies` and `tasks` endpoints and services
- Define task model (title, status, due_date, owner_id)
- Secure all endpoints with token auth
- Add unit and integration tests for services


== Milestones

1. Project scaffolding and config setup [Day 1-2]
2. Auth and Supabase integration complete [Day 3-5]
3. Google OAuth + chat endpoint working [Day 6-8]
4. Add company/task logic and testing [Day 9-12]
5. Code freeze and QA [Day 13-14]


== Gathering Results

- Validate endpoints using Postman / Swagger
- Monitor Supabase session and DB logs
- Evaluate Google Calendar token handling and LLM response time
- Gather user feedback on integration UX and chat relevance
