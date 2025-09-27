# Tasks: yt-dlp Web UI

**Input**: Design documents from `/specs/001-build-a-modern/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → If not found: ERROR "No implementation plan found"
   → Extract: tech stack, libraries, structure
2. Load optional design documents:
   → data-model.md: Extract entities → model tasks
   → contracts/: Each file → contract test task
   → research.md: Extract decisions → setup tasks
3. Generate tasks by category:
   → Setup: project init, dependencies, linting
   → Tests: contract tests, integration tests
   → Core: models, services, CLI commands
   → Integration: DB, middleware, logging
   → Polish: unit tests, performance, docs
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph
7. Create parallel execution examples
8. Validate task completeness:
   → All contracts have tests?
   → All entities have model tasks?
   → All endpoints implemented?
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Web app**: `backend/src/`, `frontend/src/`
- Paths based on plan.md structure: backend/ and frontend/ directories

## Phase 3.1: Setup
- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize Python backend with FastAPI dependencies
- [ ] T003 Initialize React frontend with Vite and dependencies
- [ ] T004 [P] Configure Python linting (ruff, black) in backend/
- [ ] T005 [P] Configure JavaScript linting (ESLint, Prettier) in frontend/
- [ ] T006 [P] Set up yt-dlp installation and verification

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [ ] T007 [P] Contract test POST /api/download in backend/tests/contract/test_download_post.py
- [ ] T008 [P] Contract test GET /api/status/{job_id} in backend/tests/contract/test_status_get.py
- [ ] T009 [P] Contract test GET /api/download/{job_id} in backend/tests/contract/test_download_get.py
- [ ] T010 [P] Contract test POST /api/metadata in backend/tests/contract/test_metadata_post.py
- [ ] T011 [P] Contract test GET /api/progress/{job_id} in backend/tests/contract/test_progress_get.py
- [ ] T012 [P] Integration test complete download flow in backend/tests/integration/test_download_flow.py
- [ ] T013 [P] Integration test error handling in backend/tests/integration/test_error_handling.py
- [ ] T014 [P] Integration test concurrent downloads in backend/tests/integration/test_concurrent_downloads.py
- [ ] T015 [P] Frontend component test UrlInput in frontend/tests/components/UrlInput.test.jsx
- [ ] T016 [P] Frontend component test FormatSelector in frontend/tests/components/FormatSelector.test.jsx
- [ ] T017 [P] Frontend component test ProgressIndicator in frontend/tests/components/ProgressIndicator.test.jsx

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [ ] T018 [P] DownloadRequest model in backend/src/models/download_request.py
- [ ] T019 [P] DownloadJob model in backend/src/models/download_job.py
- [ ] T020 [P] VideoMetadata model in backend/src/models/video_metadata.py
- [ ] T021 [P] YtDlpService in backend/src/services/ytdlp_service.py
- [ ] T022 [P] FileService in backend/src/services/file_service.py
- [ ] T023 [P] CleanupService in backend/src/services/cleanup_service.py
- [ ] T024 POST /api/download endpoint in backend/src/api/download.py
- [ ] T025 GET /api/status/{job_id} endpoint in backend/src/api/status.py
- [ ] T026 GET /api/download/{job_id} endpoint in backend/src/api/download.py
- [ ] T027 POST /api/metadata endpoint in backend/src/api/metadata.py
- [ ] T028 GET /api/progress/{job_id} endpoint in backend/src/api/progress.py
- [ ] T029 Input validation middleware in backend/src/middleware/validation.py
- [ ] T030 Error handling middleware in backend/src/middleware/error_handler.py

## Phase 3.4: Frontend Implementation
- [ ] T031 [P] UrlInput component in frontend/src/components/UrlInput.jsx
- [ ] T032 [P] FormatSelector component in frontend/src/components/FormatSelector.jsx
- [ ] T033 [P] ProgressIndicator component in frontend/src/components/ProgressIndicator.jsx
- [ ] T034 [P] DownloadButton component in frontend/src/components/DownloadButton.jsx
- [ ] T035 [P] LogPanel component in frontend/src/components/LogPanel.jsx
- [ ] T036 [P] AdvancedOptions component in frontend/src/components/AdvancedOptions.jsx
- [ ] T037 [P] API service in frontend/src/services/api.js
- [ ] T038 [P] SSE service for progress updates in frontend/src/services/sse.js
- [ ] T039 DownloadPage main component in frontend/src/pages/DownloadPage.jsx
- [ ] T040 App component with routing in frontend/src/App.jsx

## Phase 3.5: Integration
- [ ] T041 Connect YtDlpService to subprocess execution
- [ ] T042 File system integration for temporary storage
- [ ] T043 Progress tracking integration with SSE
- [ ] T044 CORS configuration for frontend-backend communication
- [ ] T045 Security headers and input sanitization
- [ ] T046 Request/response logging middleware
- [ ] T047 File cleanup scheduler (24-hour retention)
- [ ] T048 Concurrent download limit enforcement

## Phase 3.6: Polish
- [ ] T049 [P] Unit tests for models in backend/tests/unit/test_models.py
- [ ] T050 [P] Unit tests for services in backend/tests/unit/test_services.py
- [ ] T051 [P] Unit tests for API endpoints in backend/tests/unit/test_api.py
- [ ] T052 [P] Frontend integration tests in frontend/tests/integration/
- [ ] T053 Performance tests for concurrent downloads
- [ ] T054 [P] Update documentation in README.md
- [ ] T055 [P] Add API documentation with OpenAPI
- [ ] T056 Remove code duplication and optimize
- [ ] T057 Run quickstart.md validation tests
- [ ] T058 End-to-end testing with real YouTube URLs

## Dependencies
- Tests (T007-T017) before implementation (T018-T030)
- Models (T018-T020) before services (T021-T023)
- Services (T021-T023) before API endpoints (T024-T028)
- Backend API (T024-T028) before frontend (T031-T040)
- Core implementation before integration (T041-T048)
- Integration before polish (T049-T058)

## Parallel Examples
```
# Launch contract tests together (T007-T011):
Task: "Contract test POST /api/download in backend/tests/contract/test_download_post.py"
Task: "Contract test GET /api/status/{job_id} in backend/tests/contract/test_status_get.py"
Task: "Contract test GET /api/download/{job_id} in backend/tests/contract/test_download_get.py"
Task: "Contract test POST /api/metadata in backend/tests/contract/test_metadata_post.py"
Task: "Contract test GET /api/progress/{job_id} in backend/tests/contract/test_progress_get.py"

# Launch model creation together (T018-T020):
Task: "DownloadRequest model in backend/src/models/download_request.py"
Task: "DownloadJob model in backend/src/models/download_job.py"
Task: "VideoMetadata model in backend/src/models/video_metadata.py"

# Launch service creation together (T021-T023):
Task: "YtDlpService in backend/src/services/ytdlp_service.py"
Task: "FileService in backend/src/services/file_service.py"
Task: "CleanupService in backend/src/services/cleanup_service.py"

# Launch frontend components together (T031-T036):
Task: "UrlInput component in frontend/src/components/UrlInput.jsx"
Task: "FormatSelector component in frontend/src/components/FormatSelector.jsx"
Task: "ProgressIndicator component in frontend/src/components/ProgressIndicator.jsx"
Task: "DownloadButton component in frontend/src/components/DownloadButton.jsx"
Task: "LogPanel component in frontend/src/components/LogPanel.jsx"
Task: "AdvancedOptions component in frontend/src/components/AdvancedOptions.jsx"
```

## Notes
- [P] tasks = different files, no dependencies
- Verify tests fail before implementing
- Commit after each task
- Avoid: vague tasks, same file conflicts
- Follow TDD: Red → Green → Refactor cycle
- Test with real YouTube URLs in final validation

## Task Generation Rules
*Applied during main() execution*

1. **From Contracts**:
   - Each contract file → contract test task [P]
   - Each endpoint → implementation task
   
2. **From Data Model**:
   - Each entity → model creation task [P]
   - Relationships → service layer tasks
   
3. **From User Stories**:
   - Each story → integration test [P]
   - Quickstart scenarios → validation tasks

4. **Ordering**:
   - Setup → Tests → Models → Services → Endpoints → Frontend → Integration → Polish
   - Dependencies block parallel execution

## Validation Checklist
*GATE: Checked by main() before returning*

- [x] All contracts have corresponding tests
- [x] All entities have model tasks
- [x] All tests come before implementation
- [x] Parallel tasks truly independent
- [x] Each task specifies exact file path
- [x] No task modifies same file as another [P] task

