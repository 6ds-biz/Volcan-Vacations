# Volcan Vacations Architecture

The current architectural direction is [the final platform architecture](final-platform-architecture.md). Launch phases control rollout; the shared core supports a Costa Rica-wide business. The initial overview below remains historical context.

## Initial System Design

The initial platform is organized as a modern web monorepo with separate frontends for public customers and internal operations, a shared API, and a PostgreSQL database.

```text
Public Web App
       │
       ▼
    FastAPI
       │
       ▼
  PostgreSQL
       ▲
       │
Operations App
```

## Application Roles

- **Public/customer experience**: A customer-facing website for marketing, tours, and booking discovery.
- **Internal VV Operations**: A polished operations shell for staff to manage bookings, customers, trips, suppliers, and accounting.
- **Supplier/operator portal**: Future portal for tour operators, hotels, and transportation providers to manage availability and costs.
- **Shared API/database**: A single backend service and database support all frontends, simplifying integrations and data consistency.

## Milestone Progression

1. Tours
2. Transportation
3. Hotels
4. Packages
5. AI-assisted travel planning
