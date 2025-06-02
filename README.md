---

## 🧠 Clean Architecture Principles

- **Domain Layer** should have no dependencies on infrastructure or presentation.
- **Infrastructure Layer** implements interfaces defined in the domain.
- **Presentation Layer** depends on domain/use cases but not infrastructure directly.

---

## 📁 Folder Structure

```
├── domain/ # Pure business logic (entities, use cases, interfaces)
│ ├── entities/ # Core domain models
│ ├── usecases/ # Application-specific business rules
│ └── abstract/ # Interfaces for data access
│
├── infrastructure/ # Frameworks, drivers, external services
| ├── admin # Django admin
│ ├── migrations/ # Database migrations
│ ├── model/ # ORM models
│ └── repositories/ # Abstract Django ORM
│
├── presentation/ # Input/output: UI, API endpoints, CLI, etc.
│ ├── routes/ # Controllers / routes (e.g., REST)
│ └── serializers/
│ └── views/
│
│
├── .env # All env(sync to api and client)
├── api/requirements/
└── README.md
```

---

## ✅ Benefits

- **Scalable** – easily adapt to new frameworks or UIs
- **Testable** – business logic is isolated and easy to test
- **Maintainable** – clear separation of concerns

---

## 🚀 Getting Started

1. **Clone the repository**
2. **Build docker**  
   (Python: `docker compose build`)
3. **Run the docker containers**
   (`docker compose up`)
4. **Frontend run on port 3000 & api runs on port 8000**

---

## TODO:

- Deploy production using wsgi
-
