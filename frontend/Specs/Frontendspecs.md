# PromptLab Frontend Specification
Version: 1.0  
Framework: React (Vite)  
Backend: FastAPI  

---

# 1. Project Overview

This frontend connects to a FastAPI backend providing:

## Prompt Endpoints
- GET /prompts
- GET /prompts/{id}
- POST /prompts
- PUT /prompts/{id}
- PATCH /prompts/{id}
- DELETE /prompts/{id}
- GET /tags/{tag}/prompts

## Collection Endpoints
- GET /collections
- GET /collections/{id}
- POST /collections
- DELETE /collections/{id}

---

# 2. Goals (Tasks 4.2 – 4.6)

## Task 4.2 – Core Components
Build reusable UI components.

## Task 4.3 – API Integration
Create centralized API client and endpoint wrappers.

## Task 4.4 – Full CRUD Flow
Implement:
- View prompts
- View prompt details
- Create prompt
- Edit prompt
- Delete prompt
- Manage collections
- Filter by collection

## Task 4.5 – UX Polish
- Loading states
- Error handling
- Empty states
- Responsive design
- Form validation
- Keyboard accessibility

## Task 4.6 – Backend Integration
- CORS compatibility
- Environment config
- Network error handling

---

# 3. Folder Structure

src/
  api/
    client.js
    prompts.js
    collections.js

  components/
    prompts/
      PromptCard.jsx
      PromptList.jsx
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
    Header.jsx
    Sidebar.jsx

  pages/
    Dashboard.jsx
    PromptPage.jsx

  styles/
    global.css
    components.css

  context/
    PromptContext.jsx (optional)

  hooks/
    usePrompts.js
    useCollections.js

---

# 4. API Layer Specification

## client.js
Responsibilities:
- Set base URL from environment variable
- Wrap fetch
- Parse JSON
- Handle errors consistently
- Return null for 204 responses

Environment Variable:
VITE_API_BASE_URL=http://localhost:8000

---

## prompts.js

Functions:
- getPrompts(queryParams?)
- getPrompt(id)
- createPrompt(data)
- updatePrompt(id, data)
- deletePrompt(id)

---

## collections.js

Functions:
- getCollections()
- createCollection(data)
- deleteCollection(id)

---

# 5. Layout Components

## Layout.jsx
Structure:
Header  
Sidebar  
Main Content  

Responsibilities:
- Wrap all pages
- Provide responsive layout

---

## Header.jsx
Displays:
- App name
- Optional navigation

---

## Sidebar.jsx
Displays:
- List of collections
- "All Prompts" option
- Create Collection button

Triggers:
- Filter prompts by collection

---

# 6. Prompt Components

## PromptCard.jsx
Displays:
- Title
- Short description
- Tags
- Last updated date

Click behavior:
- Navigate to PromptPage

---

## PromptList.jsx
Displays:
- Grid or list of PromptCard

States:
- Loading
- Empty
- Error

---

## PromptForm.jsx
Used for:
- Create prompt
- Edit prompt

Fields:
- title (required)
- content (required, min 10 chars)
- description
- collection_id (dropdown)
- tags (comma separated)

Validation:
- Title required
- Content min length 10

---

## PromptDetail.jsx
Displays:
- Title
- Content
- Description
- Tags
- Collection
- Created date
- Updated date

Buttons:
- Edit
- Delete
- Back

---

# 7. Collection Components

## CollectionList.jsx
Displays:
- List of collections
- Highlight active collection

---

## CollectionForm.jsx
Fields:
- name (required)
- description

---

# 8. Shared Components

## Button.jsx
Reusable button with variants:
- primary
- secondary
- danger

---

## Modal.jsx
Reusable modal component for:
- Confirm delete
- Create collection
- Edit prompt

---

## SearchBar.jsx
Debounced search input

---

## LoadingSpinner.jsx
Shown during async operations

---

## ErrorMessage.jsx
Displays user-friendly error messages

---

# 9. Pages

## Dashboard.jsx

Displays:
- SearchBar
- CollectionList (sidebar)
- PromptList
- Create Prompt button
- Create Collection button

State:
- prompts[]
- collections[]
- loading
- error
- selectedCollection
- searchQuery

Responsibilities:
- Fetch prompts
- Apply filters
- Handle CRUD

---

## PromptPage.jsx

Route:
`/prompts/:id`

Displays:
- PromptDetail

Handles:
- Fetch single prompt
- Edit
- Delete

---

# 10. Routing

Use React Router:

- `/` → Dashboard
- `/prompts/:id` → PromptPage

---

# 11. UX Requirements

## Loading States
Show spinner while fetching data.

## Empty States
Show helpful message when:
- No prompts exist
- No collections exist

## Error Handling
Catch:
- Network errors
- Backend validation errors
- 404 errors

Display via ErrorMessage component.

---

# 12. Acceptance Criteria

✔ Can view prompts  
✔ Can create prompt  
✔ Can edit prompt  
✔ Can delete prompt  
✔ Can create collection  
✔ Can filter by collection  
✔ Loading indicators visible  
✔ Errors handled gracefully  
✔ Responsive layout  
✔ Fully connected to backend  
✔ No console errors  

---

END OF SPEC