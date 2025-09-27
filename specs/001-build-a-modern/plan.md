# Implementation Plan: yt-dlp Web UI

**Branch**: `001-build-a-modern` | **Date**: 2024-12-19 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-build-a-modern/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type from file system structure or context (web=frontend+backend, mobile=app+api)
   → Set Structure Decision based on project type
3. Fill the Constitution Check section based on the content of the constitution document.
4. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Simplify approach first"
   → Update Progress Tracking: Initial Constitution Check
5. Execute Phase 0 → research.md
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
6. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file (e.g., `CLAUDE.md` for Claude Code, `.github/copilot-instructions.md` for GitHub Copilot, `GEMINI.md` for Gemini CLI, `QWEN.md` for Qwen Code or `AGENTS.md` for opencode).
7. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
8. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
9. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
Build a modern web interface for yt-dlp that allows users to download YouTube videos in various formats (video, audio MP3/WAV, subtitles, metadata) with a clean, responsive UI and real-time progress feedback.

## Technical Context
**Language/Version**: Python 3.11  
**Primary Dependencies**: FastAPI + React + yt-dlp  
**Storage**: Temporary file system (24-hour cleanup)  
**Testing**: pytest + Jest  
**Target Platform**: Web browser + Linux server  
**Project Type**: web (frontend + backend)  
**Performance Goals**: <2s response time, handle 5 concurrent downloads per user  
**Constraints**: 24-hour file retention, YouTube-only support, secure command execution  
**Scale/Scope**: Single-user focused, moderate traffic  

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Test-First Principle**: ✅ TDD approach with contract tests before implementation
**Library-First**: ✅ yt-dlp as core library, web UI as wrapper
**CLI Interface**: ✅ Backend exposes yt-dlp functionality via REST API
**Integration Testing**: ✅ Contract tests for API endpoints, integration tests for download flows
**Simplicity**: ✅ Single-purpose tool, minimal dependencies

## Project Structure

### Documentation (this feature)
```
specs/001-build-a-modern/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
backend/
├── src/
│   ├── models/
│   │   ├── download_request.py
│   │   ├── download_job.py
│   │   └── video_metadata.py
│   ├── services/
│   │   ├── ytdlp_service.py
│   │   ├── file_service.py
│   │   └── cleanup_service.py
│   ├── api/
│   │   ├── download.py
│   │   ├── metadata.py
│   │   └── status.py
│   └── main.py
└── tests/
    ├── contract/
    ├── integration/
    └── unit/

frontend/
├── src/
│   ├── components/
│   │   ├── UrlInput.jsx
│   │   ├── FormatSelector.jsx
│   │   ├── ProgressIndicator.jsx
│   │   ├── DownloadButton.jsx
│   │   └── LogPanel.jsx
│   ├── pages/
│   │   └── DownloadPage.jsx
│   ├── services/
│   │   └── api.js
│   └── App.jsx
└── tests/
    ├── components/
    └── integration/
```

**Structure Decision**: Web application structure with separate frontend (React) and backend (FastAPI) components. Frontend handles UI/UX, backend manages yt-dlp execution and file operations.

## Phase 0: Outline & Research
1. **Extract unknowns from Technical Context** above:
   - Research yt-dlp Python integration patterns
   - Research FastAPI + React best practices
   - Research file cleanup and security patterns
   - Research progress tracking for long-running operations

2. **Generate and dispatch research agents**:
   ```
   Task: "Research yt-dlp Python integration for web applications"
   Task: "Find best practices for FastAPI + React architecture"
   Task: "Research secure command execution patterns"
   Task: "Find patterns for real-time progress tracking in web apps"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*

1. **Extract entities from feature spec** → `data-model.md`:
   - DownloadRequest: URL, format, options, user_id
   - DownloadJob: status, progress, file_path, created_at
   - VideoMetadata: title, duration, thumbnail, available_formats

2. **Generate API contracts** from functional requirements:
   - POST /api/download - Start download
   - GET /api/metadata/{url} - Get video metadata
   - GET /api/status/{job_id} - Check download status
   - GET /api/download/{job_id} - Download completed file

3. **Generate contract tests** from contracts:
   - One test file per endpoint
   - Assert request/response schemas
   - Tests must fail (no implementation yet)

4. **Extract test scenarios** from user stories:
   - Each story → integration test scenario
   - Quickstart test = story validation steps

5. **Update agent file incrementally** (O(1) operation):
   - Run `.specify/scripts/bash/update-agent-context.sh cursor`
     **IMPORTANT**: Execute it exactly as specified above. Do not add or remove any arguments.
   - If exists: Add only NEW tech from current plan
   - Preserve manual additions between markers
   - Update recent changes (keep last 3)
   - Keep under 150 lines for token efficiency
   - Output to repository root

**Output**: data-model.md, /contracts/*, failing tests, quickstart.md, agent-specific file

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `.specify/templates/tasks-template.md` as base
- Generate tasks from Phase 1 design docs (contracts, data model, quickstart)
- Each contract → contract test task [P]
- Each entity → model creation task [P] 
- Each user story → integration test task
- Implementation tasks to make tests pass

**Ordering Strategy**:
- TDD order: Tests before implementation 
- Dependency order: Models before services before UI
- Mark [P] for parallel execution (independent files)

**Estimated Output**: 25-30 numbered, ordered tasks in tasks.md

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)  
**Phase 4**: Implementation (execute tasks.md following constitutional principles)  
**Phase 5**: Validation (run tests, execute quickstart.md, performance validation)

## Complexity Tracking
*Fill ONLY if Constitution Check has violations that must be justified*

No violations detected - design follows constitutional principles.

## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command)
- [x] Phase 1: Design complete (/plan command)
- [ ] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS
- [x] Post-Design Constitution Check: PASS
- [x] All NEEDS CLARIFICATION resolved
- [x] Complexity deviations documented

---
*Based on Constitution v2.1.1 - See `/memory/constitution.md`*