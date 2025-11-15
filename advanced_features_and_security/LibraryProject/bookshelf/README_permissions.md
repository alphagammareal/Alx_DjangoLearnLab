# Bookshelf Permission and Group Setup

## Custom Permissions Added
The Book model defines these permissions:
- can_view
- can_create
- can_edit
- can_delete

## Groups to Create in Django Admin

### 1. Viewers
- bookshelf.can_view

### 2. Editors
- bookshelf.can_view
- bookshelf.can_create
- bookshelf.can_edit

### 3. Admins
- All permissions including bookshelf.can_delete

## How Permissions Are Used in Views
Views use decorators such as:

@permission_required('bookshelf.can_edit', raise_exception=True)

This ensures users must have the required permission to:
- Add books
- Edit books
- Delete books
