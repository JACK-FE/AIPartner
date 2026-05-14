## ADDED Requirements

### Requirement: Square page shows public characters
The system SHALL return a paginated list of public AI characters (is_public=true) for the square page.

#### Scenario: Browse public characters
- **WHEN** any user (authenticated or not) requests the character list
- **THEN** system returns paginated results of public characters

#### Scenario: Pagination works
- **WHEN** user requests page 2 with page_size=20
- **THEN** system returns characters 21-40 and total count

### Requirement: User can search characters by name
The system SHALL allow searching public characters by name (case-insensitive partial match).

#### Scenario: Search by name
- **WHEN** user searches for "helper"
- **THEN** system returns public characters whose name contains "helper"

#### Scenario: No results
- **WHEN** user searches for a non-existent name
- **THEN** system returns empty list

### Requirement: User can sort characters
The system SHALL support sorting public characters by popularity (follow_count) and newest (created_at).

#### Scenario: Sort by popularity
- **WHEN** user selects sort=hot
- **THEN** system returns characters ordered by follow_count descending

#### Scenario: Sort by newest
- **WHEN** user selects sort=new
- **THEN** system returns characters ordered by created_at descending

### Requirement: User can filter characters by model
The system SHALL allow filtering public characters by model provider or model name.

#### Scenario: Filter by model
- **WHEN** user filters by model_id=1
- **THEN** system returns only characters using that model

### Requirement: User can view character detail
The system SHALL return full details of a specific character including creator info, model info, and follow count.

#### Scenario: View character detail
- **WHEN** user requests a specific public character
- **THEN** system returns full character details

#### Scenario: Character not found
- **WHEN** user requests a non-existent character
- **THEN** system returns 404 error
