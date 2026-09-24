# Flutter Architecture Specification — RTConnect

This document details the architectural patterns, folder boundaries, state management choices, and layer separation rules for the RTConnect Flutter application.

---

## 1. Architecture Overview
- **Pattern:** Feature-First Clean Architecture [PROPOSED].
- **Rationale:** Separates code by business features rather than generic layers, allowing AI coding agents to implement complete vertical slices (`auth`, `letters`, `chatbot`) autonomously without touching unrelated code.
- **Client Technology:** Flutter 3.x+ with Dart null safety [CONFIRMED].
- **State Management:** Riverpod 2.x (`flutter_riverpod`) [PROPOSED].
- **Routing:** Declarative URL router (`go_router`) [PROPOSED].

---

## 2. Layer Architecture

Every feature adheres to three strict unidirectional layers:

```text
[ Presentation Layer ] (Screens, Widgets, Riverpod Notifiers / State)
         │
         ▼
[ Domain Layer ]       (Pure Dart Entities, Value Objects, Repository Interfaces)
         │
         ▼
[ Data Layer ]         (Data Sources [Remote/Local], DTOs, Repository Implementations)
```

1. **Presentation Layer:**
   - Widgets are dumb view renderers consuming immutable state.
   - User actions dispatch intent methods to Riverpod StateNotifiers / AsyncNotifiers.
   - No direct SQL or HTTP calls are allowed inside widgets.
2. **Domain Layer:**
   - Contains pure Dart domain entities without JSON serialization dependencies.
   - Defines abstract repository contracts (`ILetterRepository`, `IAuthRepository`).
   - Contains pure business logic and validation rules.
3. **Data Layer:**
   - Implements repository contracts.
   - Maps between API JSON DTOs and Domain Entities.
   - Communicates with network clients (`Dio`) and encrypted device storage.

---

## 3. Folder Structure (Proposed Standard)

```text
lib/
├── core/
│   ├── constants/            # App constants, assets, regex
│   ├── errors/               # Failure classes and AppException models
│   ├── network/              # Dio client, interceptors, API endpoints
│   ├── router/               # go_router configuration & route guards
│   ├── storage/              # flutter_secure_storage wrapper
│   └── theme/                # Color tokens, Typography, ThemeData
│
├── features/
│   ├── auth/
│   │   ├── data/             # AuthDTO, AuthRemoteDataSource, AuthRepositoryImpl
│   │   ├── domain/           # UserEntity, IAuthRepository, AuthValidators
│   │   └── presentation/     # LoginScreen, RegisterScreen, AuthNotifier
│   │
│   ├── letters/
│   │   ├── data/             # LetterDTO, LetterRemoteDataSource, LetterRepositoryImpl
│   │   ├── domain/           # LetterEntity, ILetterRepository, LetterStatusEnum
│   │   └── presentation/     # LetterFormScreen, LetterHistoryScreen, RTReviewScreen
│   │
│   ├── chatbot/
│   │   ├── data/             # ChatMessageDTO, ChatbotRemoteDataSource
│   │   ├── domain/           # ChatMessageEntity, IChatbotRepository
│   │   └── presentation/     # ChatbotScreen, ChatMessageBubble, ChatController
│   │
│   └── profile/
│       ├── data/             # ProfileRemoteDataSource
│       ├── domain/           # ProfileEntity
│       └── presentation/     # ProfileDrawerWidget
│
├── shared/
│   ├── models/               # Universal models (ApiResponse, PaginatedResponse)
│   └── widgets/              # PrimaryButton, CustomTextField, StatusBadge, ShimmerCard
│
└── main.dart                 # App initialization, ProviderScope, runApp
```

---

## 4. Dependency Rules
1. **Inner layers never depend on outer layers:** Domain cannot import Presentation or Data.
2. **Features never directly cross-import private feature components:** If an entity or widget is shared across features, move it to `lib/shared/`.
3. **External packages are wrapped:** Do not call raw `Dio` or `flutter_secure_storage` inside presentation widgets. Inject them via Core interfaces.

---

## 5. State Management
- **State Management:** UNKNOWN in source.
- **PROPOSED:** `flutter_riverpod` (v2.5.1+).
- **Reason:** Provides compile-time safety, effortless dependency injection, built-in asynchronous state caching (`AsyncValue`), testability without mocking `BuildContext`, and no runtime `ProviderNotFoundException`.
- **Trade-off:** Requires understanding `ConsumerWidget` and `ref.watch`.
- **Alternative Considered:** `flutter_bloc` (More boilerplate for simple forms).

---

## 6. Navigation
- **Router:** UNKNOWN in source.
- **PROPOSED:** `go_router` (v14.0.0+).
- **Reason:** Supports declarative routing, URL-based deep linking (vital for redirecting to `/surat/preview/:id`), and authentication state redirect guards.
- **Guards:**
  - Unauthenticated users attempting to access `/warga/*` or `/rt/*` are redirected to `/login`.
  - Authenticated users attempting to access `/login` or `/register` are redirected to their dashboard.
  - Role protection: Warga accessing `/rt/*` is redirected to `/warga/home`.

---

## 7. Data Layer
- **Remote Data Sources:** Encapsulate HTTP requests via `Dio`.
- **DTOs:** Carry `fromJson` and `toJson` factory methods.
- **Entity Mappers:** Extension functions to map DTOs into domain entities (`userDto.toDomain()`).

---

## 8. Repository Layer
- Mediates between data sources and presentation controllers.
- Returns `Either<Failure, T>` or throws typed domain `AppException` to keep controllers clean.
- Example:
  ```dart
  abstract class ILetterRepository {
    Future<List<LetterEntity>> getCitizenLetters();
    Future<LetterEntity> submitLetter(LetterSubmissionParams params);
    Future<void> reviewLetter(String letterId, ReviewDecision decision);
  }
  ```

---

## 9. Service Layer
- **LLMService:** Technology-agnostic interface interacting with the backend AI drafting gateway.
- **VectorSearchService:** Manages client-side query payload preparation for RAG knowledge search.
- **FilePickerService:** Abstraction over OS file selection and image camera/gallery capture.

---

## 10. API Client
- Built upon `Dio` singleton configured in `lib/core/network/api_client.dart`.
- **Interceptors:**
  1. `AuthInterceptor`: Attaches `Authorization: Bearer <token>` to requests.
  2. `LoggingInterceptor`: Logs request/response in debug mode.
  3. `ErrorInterceptor`: Converts HTTP 401/403/500 into domain `AppException`.

---

## 11. Models
- Built with immutability (`final` fields).
- Domain entities use value equality (`operator ==` and `hashCode`).
- Sensitive fields like passwords are scrubbed before presentation.

---

## 12. Error Handling
- Structured domain failure hierarchy:
  - `NetworkFailure`: Connection timed out, offline.
  - `ServerFailure`: HTTP 500 internal server error.
  - `AuthFailure`: Invalid credentials, expired token.
  - `ValidationFailure`: Invalid NIK, missing mandatory fields.
- Presentation layers convert failures into localized, citizen-friendly Indonesian error messages.

---

## 13. Authentication Lifecycle
```text
[App Start]
    │
    ▼
Check flutter_secure_storage for 'auth_token'
    ├── [Token Found] ──► Validate via API (/auth/me)
    │                         ├── [Valid] ──► Load User Role ──► Route to Dashboard
    │                         └── [Invalid/Expired] ──► Clear Token ──► Route to /login
    └── [No Token]    ──► Route to / (Landing Page)
```

---

## 14. Local Storage
- **Package:** `flutter_secure_storage` [PROPOSED].
- **Keys:**
  - `KEY_AUTH_TOKEN`: JWT session bearer token.
  - `KEY_USER_ROLE`: Cached string role (`'warga'` or `'rt'`).
  - `KEY_USER_ID`: Cached unique user identifier.

---

## 15. Dependency Injection
- Achieved cleanly via Riverpod Providers (`Provider`, `FutureProvider`, `NotifierProvider`).
- No service locator (`GetIt`) needed, keeping code modular and testable.

---

## 16. Environment Configuration
- Uses `String.fromEnvironment` / `.env` configuration:
  - `API_BASE_URL`: Base backend URL (e.g. `http://10.0.2.2:5000/api` for Android emulator).
  - `APP_ENV`: `development` | `staging` | `production`.

---

## 17. Logging
- Uses standard Dart `developer.log()` in debug mode.
- PII (NIK, passwords, citizen addresses) is strictly masked in log outputs.

---

## 18. Security
- Transport Security: HTTPS strictly required in production builds.
- Storage: Encrypted keystore/keychain for tokens.
- QR Verification: Token generated via cryptographically secure random bytes verified against server database.

---

## 19. Testing Architecture
- Unit tests run under `test/unit/` with mocked repositories (`mockito`).
- Widget tests run under `test/widget/` using test harness wrapping widgets with `ProviderScope`.
- Integration tests run under `integration_test/` verifying end-to-end user flows.
