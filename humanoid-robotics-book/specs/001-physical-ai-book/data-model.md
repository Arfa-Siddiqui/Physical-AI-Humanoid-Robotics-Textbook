# Data Model: Physical AI & Humanoid Robotics Book

## Key Entities

### Module
- **Description**: Core learning unit of the book
- **Attributes**:
  - moduleId (string): Unique identifier for the module
  - title (string): Module title (e.g., "ROS 2 Fundamentals")
  - description (string): Brief description of the module
  - priority (enum): P1, P2, or P3 based on importance
  - prerequisites (array of ModuleId): List of required modules
  - estimatedHours (number): Estimated time to complete
  - learningObjectives (array of string): What students will learn

### Chapter
- **Description**: Subdivision of a module containing related content
- **Attributes**:
  - chapterId (string): Unique identifier for the chapter
  - moduleId (string): Parent module identifier
  - title (string): Chapter title
  - content (string): The chapter's Markdown content
  - position (number): Order within the module
  - learningObjectives (array of string): Specific learning goals

### ContentBlock
- **Description**: Individual section of content (text, code, diagram, etc.)
- **Attributes**:
  - blockId (string): Unique identifier for the content block
  - chapterId (string): Parent chapter identifier
  - type (enum): "text", "code", "diagram", "exercise", "example"
  - content (string): The actual content
  - position (number): Order within the chapter

### CodeExample
- **Description**: Executable code demonstration
- **Attributes**:
  - exampleId (string): Unique identifier for the example
  - blockId (string): Associated content block
  - language (string): Programming language (e.g., "Python", "C++")
  - code (string): The actual code
  - description (string): Explanation of what the code does
  - dependencies (array of string): Required packages/libraries
  - validationStatus (enum): "not-tested", "tested", "validated", "broken"

### Citation
- **Description**: Reference to an external source
- **Attributes**:
  - citationId (string): Unique identifier for the citation
  - type (enum): "academic-paper", "documentation", "book", "web-resource"
  - title (string): Title of the source
  - authors (array of string): List of authors
  - publicationDate (date): Date of publication
  - url (string): URL to access the source
  - doi (string): Digital Object Identifier if applicable
  - isPeerReviewed (boolean): Whether the source is peer-reviewed

### Exercise
- **Description**: Practice problem or task for students
- **Attributes**:
  - exerciseId (string): Unique identifier for the exercise
  - blockId (string): Associated content block
  - title (string): Brief title of the exercise
  - description (string): Detailed instructions
  - difficulty (enum): "beginner", "intermediate", "advanced"
  - solution (string): Provided solution (if any)
  - requiredTools (array of string): Tools needed to complete exercise

### Diagram
- **Description**: Visual representation of concepts
- **Attributes**:
  - diagramId (string): Unique identifier for the diagram
  - blockId (string): Associated content block
  - title (string): Brief description of the diagram
  - description (string): Explanation of what the diagram represents
  - type (enum): "mermaid", "drawio", "custom"
  - sourceFile (string): Path to diagram source file
  - renderedFile (string): Path to rendered image file

## Relationships

1. **Module** (1) → (Many) **Chapter**
   - A module contains multiple chapters
   - Each chapter belongs to exactly one module

2. **Chapter** (1) → (Many) **ContentBlock**
   - A chapter contains multiple content blocks
   - Each content block belongs to exactly one chapter

3. **ContentBlock** (1) → (0 or 1) **CodeExample**
   - A content block may have an associated code example
   - Each code example belongs to exactly one content block

4. **ContentBlock** (1) → (0 or 1) **Exercise**
   - A content block may have an associated exercise
   - Each exercise belongs to exactly one content block

5. **ContentBlock** (1) → (0 or 1) **Diagram**
   - A content block may have an associated diagram
   - Each diagram belongs to exactly one content block

6. **Citation** (Many) → (Many) **ContentBlock**
   - Content blocks can reference multiple citations
   - Citations can be used in multiple content blocks
   - Junction table: ContentBlockCitation

## Validation Rules

1. **Module Prerequisites**: Each module's prerequisites must exist and form an acyclic dependency graph
2. **Content Length**: Each chapter should be between 2,000-5,000 words
3. **Code Validation**: All CodeExample entities must have a validationStatus of "tested" or "validated" before publication
4. **Citation Requirements**: At least 40% of citations must have isPeerReviewed = true
5. **Module Sequence**: Chapters within a module must follow a logical sequence based on dependencies
6. **Content Completeness**: Each module must have at least one chapter with learning objectives
7. **Exercise Coverage**: Each module should include at least 3 exercises of varying difficulty levels

## State Transitions

### CodeExample States:
- `not-tested` → `tested` → `validated` (fully functional)
- `not-tested` → `tested` → `broken` (needs fix)

### Chapter States:
- `draft` → `review` → `approved` → `published`
- `published` → `updated` (if content changes) → `review` → `approved` → `published`

## Indexes

1. Content search index on `ContentBlock.content` for full-text search
2. Module index on `Module.title` and `Module.description` for category browsing
3. Citation index on `Citation.title`, `Citation.authors` for reference lookup
4. Learning objective index on `Module.learningObjectives` and `Chapter.learningObjectives` for curriculum planning