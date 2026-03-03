# FRONTEND SPECIFICATION
Project: Prompt Management SaaS Dashboard
Stack: React + Vite + React Router v6
Architecture: Modular, Scalable, Production-Ready

------------------------------------------------------------
1. PROJECT GOAL
------------------------------------------------------------

Build a professional SaaS-style dashboard for managing:

- Prompts (Full CRUD)
- Collections (Create + Delete)
- Filtering prompts by collection
- Searching prompts
- Modal-based create/edit forms
- Responsive UI
- Proper loading & error handling
- Backend integration via REST API

------------------------------------------------------------
2. TECH STACK
------------------------------------------------------------

- React (Functional components only)
- Vite
- React Router DOM v6
- Fetch API
- CSS Modules
- No UI libraries
- No Redux
- Local state via useState / useEffect

------------------------------------------------------------
3. FOLDER STRUCTURE (STRICT)
------------------------------------------------------------

src/
  api/
    client.js
    prompts.js
    collections.js

  components/
    prompts/
      PromptList.jsx
      PromptCard.jsx
      PromptForm.jsx
      PromptDetail.jsx

    collections/
      CollectionList.jsx
      CollectionForm.jsx

    shared/
      Button.jsx
      Modal.jsx
      SearchBar.jsx
      LoadingSpinner.jsx
      ErrorMessage.jsx

  layouts/
    Layout.jsx
    Layout.module.css
    Header.jsx
    Header.module.css
    Sidebar.jsx
    Sidebar.module.css

  pages/
    Dashboard.jsx

  App.jsx
  main.jsx

------------------------------------------------------------
4. NAMING RULES (CRITICAL)
------------------------------------------------------------

- Component files MUST use PascalCase
  Example: LoadingSpinner.jsx

- CSS Modules MUST match component:
  Example:
    LoadingSpinner.jsx
    LoadingSpinner.module.css

- Imports MUST match exact casing
- NEVER mix layout.jsx and Layout.jsx
- NEVER mix sidebar.jsx and Sidebar.jsx

------------------------------------------------------------
5. API LAYER SPEC
------------------------------------------------------------

All API calls must go through:

src/api/client.js

client.js:
- Use import.meta.env.VITE_API_BASE_URL
- Handle JSON headers
- Throw normalized errors
- Handle non-2xx responses

prompts.js:
- getPrompts()
- getPrompt(id)
- createPrompt(data)
- updatePrompt(id, data)
- deletePrompt(id)

collections.js:
- getCollections()
- createCollection(data)
- deleteCollection(id)

No hardcoded URLs anywhere.

------------------------------------------------------------
6. ROUTING SPEC
------------------------------------------------------------

Use React Router v6:

App.jsx:

- Wrap everything inside <Layout>
- Routes:
    "/" → Dashboard
    "/prompts/:id" → PromptDetail

------------------------------------------------------------
7. LAYOUT BEHAVIOR
------------------------------------------------------------

Layout:
- Header at top (fixed height 64px)
- Sidebar left (width 260px)
- Content area scrollable
- Flex-based layout
- Responsive: sidebar collapses under 768px

------------------------------------------------------------
8. DASHBOARD RESPONSIBILITIES
------------------------------------------------------------

Dashboard.jsx must:

- Fetch prompts on mount
- Fetch collections on mount
- Show LoadingSpinner during fetch
- Show ErrorMessage on error
- Show empty state if no prompts
- Filter prompts by selected collection
- Filter prompts by search query
- Open Modal for create/edit
- Show delete confirmation Modal
- Refresh list after create/update/delete

------------------------------------------------------------
9. PROMPT COMPONENT RESPONSIBILITIES
------------------------------------------------------------

PromptList:
- Accept prompts array
- Show grid layout (3 desktop, 1 mobile)
- Show empty state
- Call onEdit / onDelete

PromptCard:
- Show title
- Show truncated content
- Edit button
- Delete button

PromptForm:
- Accept initialData
- Validate required fields
- Disable submit while loading
- Call create or update API
- Call onSuccess()

PromptDetail:
- Fetch prompt by ID
- Show full content
- Show loading and error states

------------------------------------------------------------
10. COLLECTION COMPONENT RESPONSIBILITIES
------------------------------------------------------------

CollectionList:
- Show list of collections
- Highlight selected
- Call onSelect

CollectionForm:
- Simple create form
- Validate name required
- Refresh collections on success

------------------------------------------------------------
11. SHARED COMPONENT RULES
------------------------------------------------------------

All shared components must:

- Use default export
- No named exports
- No inline styles (unless absolutely required)
- Clean minimal SaaS style

Button:
- Variants: primary | secondary | danger
- Loading state
- Disabled when loading

Modal:
- Overlay
- ESC closes
- Click outside closes
- Centered

SearchBar:
- Controlled input

LoadingSpinner:
- CSS animation

ErrorMessage:
- Display readable message
- Optional retry button

------------------------------------------------------------
12. UX REQUIREMENTS
------------------------------------------------------------

- All async operations must:
    set loading true before request
    set loading false after request

- Disable buttons while loading
- Show spinner inside buttons when loading
- Show user-friendly error messages
- Show empty states

------------------------------------------------------------
13. ENVIRONMENT VARIABLES
------------------------------------------------------------

Root .env must contain:

VITE_API_BASE_URL=http://localhost:8000

Restart server after modifying.

------------------------------------------------------------
14. BACKEND REQUIREMENTS
------------------------------------------------------------

Backend must allow CORS:

allow_origins=["http://localhost:5173"]

------------------------------------------------------------
15. CODE QUALITY RULES
------------------------------------------------------------

- Functional components only
- Default exports only
- No duplicate folders
- No unused components
- No casing mismatches
- No .jsx in import paths
- No inline styles unless required
- Keep components under 200 lines

------------------------------------------------------------
END OF SPEC
------------------------------------------------------------