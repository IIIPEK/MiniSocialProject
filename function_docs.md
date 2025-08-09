# Function Documentation - MiniSocial Project

## Table of Contents
1. [Account Functions](#account-functions)
2. [Social Functions](#social-functions)
3. [Utility Functions](#utility-functions)
4. [Template Tags](#template-tags)
5. [Management Commands](#management-commands)

---

## Account Functions

### `accounts/views.py`

#### `login_view(request)`
**Purpose**: Handle user login with form validation and redirect.

**Parameters**: 
- `request` (HttpRequest): The HTTP request object

**Returns**: 
- GET: Renders login form
- POST: Redirects to post list on success, or shows form with errors

**Example**:
```python
# URL: /accounts/login/
# Redirects to 'social:post_list' after successful login
```

---

#### `register_view(request)`
**Purpose**: Handle user registration with custom user form.

**Parameters**: 
- `request` (HttpRequest): The HTTP request object

**Returns**: 
- GET: Renders registration form
- POST: Creates user and redirects to post list

**Features**:
- Uses `CustomUserCreationForm`
- Automatically logs in user after registration
- Supports file upload for avatar

---

#### `profile_view(request)`
**Purpose**: Display user's profile page with their posts.

**Parameters**: 
- `request` (HttpRequest): The HTTP request object

**Returns**: Rendered profile template with user data and posts

**Decorators**: `@login_required`

**Template Variables**:
- `user`: Current user object
- `posts`: User's posts ordered by creation date

---

#### `toggle_follow(request, username)`
**Purpose**: Handle follow/unfollow functionality with AJAX support.

**Parameters**: 
- `request` (HttpRequest): The HTTP request object
- `username` (str): Username of user to follow/unfollow

**Returns**: 
- AJAX: JSON response with success status
- Regular: HTTP redirect

**Decorators**: `@login_required`, `@require_POST`

**Features**:
- Prevents self-following
- Creates notification on follow
- AJAX-enabled for smooth UX

---

#### `confirm_email(request, uidb64, token)`
**Purpose**: Confirm user's email address using token-based verification.

**Parameters**: 
- `request` (HttpRequest): The HTTP request object
- `uidb64` (str): Base64 encoded user ID
- `token` (str): Email confirmation token

**Returns**: Redirects to login with success/error message

**Process**:
1. Decodes user ID from base64
2. Validates token using Django's default token generator
3. Sets `is_email_confirmed = True`
4. Shows appropriate message

---

## Social Functions

### `social/views.py`

#### `post_create(request)`
**Purpose**: Create a new post with title, content, and optional image.

**Parameters**: 
- `request` (HttpRequest): The HTTP request object

**Returns**: 
- GET: Renders post creation form
- POST: Saves post and redirects to post list

**Decorators**: `@login_required`

**Features**:
- Automatically sets current user as author
- Handles file upload for images
- Uses `PostForm` for validation

---

#### `post_list(request)`
**Purpose**: Display paginated list of posts with filtering and sorting options.

**Parameters**: 
- `request` (HttpRequest): The HTTP request object

**Returns**: Rendered post list template with filtered posts

**Query Parameters**:
- `q`: Search query (searches title, content, author username)
- `filter`: Filter type ('following', 'not_following', 'followers', 'all')
- `sort`: Sort order ('-created_at', 'created_at', '-likes_count', '-comments_count')
- `page`: Page number for pagination

**Features**:
- Search functionality across multiple fields
- Advanced filtering by relationship
- Dynamic sorting with database annotations
- Pagination (10 posts per page)
- Works for both authenticated and anonymous users

---

#### `post_detail(request, pk)`
**Purpose**: Display detailed view of a post with comments and comment form.

**Parameters**: 
- `request` (HttpRequest): The HTTP request object
- `pk` (int): Primary key of the post

**Returns**: 
- GET: Renders post detail with comments
- POST: Adds new comment and redirects

**Decorators**: `@login_required`

**Features**:
- Paginated comments (10 per page)
- Comment creation form
- Automatic notification creation for comments
- Optimized with `select_related` for author data

---

#### `post_like_toggle(request, pk)`
**Purpose**: Toggle like status for a post with AJAX support.

**Parameters**: 
- `request` (HttpRequest): The HTTP request object
- `pk` (int): Primary key of the post

**Returns**: 
- AJAX: JSON response with like status and count
- Regular: HTTP redirect to referrer or home

**Decorators**: `@login_required`

**Features**:
- Toggles like/unlike status
- Creates notification on like
- AJAX-enabled for seamless UX
- Returns updated like count

---

#### `comment_delete(request, comment_id)`
**Purpose**: Delete a comment with permission checking.

**Parameters**: 
- `request` (HttpRequest): The HTTP request object
- `comment_id` (int): ID of comment to delete

**Returns**: Redirects to post detail page with success/error message

**Decorators**: `@login_required`

**Security**: 
- Uses `can_delete_comment` permission check
- Only comment author can delete within time limit

---

## Utility Functions

### `utils/notifications.py`

#### `create_notification(actor, recipient, verb, target=None)`
**Purpose**: Create system notifications for user interactions.

**Parameters**: 
- `actor` (User): User who performed the action
- `recipient` (User): User who receives the notification
- `verb` (str): Action type ('like', 'comment', 'follow')
- `target` (Model, optional): Related object (post, comment, etc.)

**Returns**: None (creates notification in database)

**Features**:
- Prevents self-notifications
- Uses Django's ContentType framework for generic relations
- Error handling for duplicate notifications
- Supports various notification types

**Example**:
```python
# Notify when someone likes a post
create_notification(
    actor=request.user,
    recipient=post.author,
    verb='like',
    target=post
)
```

---

### `utils/context_processors.py`

#### `menu_context(request)`
**Purpose**: Provide dynamic navigation menu and global context variables.

**Parameters**: 
- `request` (HttpRequest): The HTTP request object

**Returns**: Dictionary with context variables

**Context Variables**:
- `menu_items`: List of navigation menu items
- `main_title`: Application title from settings
- `year`: Current year for footer
- `notification`: Notification data with unread count

**Features**:
- Dynamic menu based on authentication status
- Admin link for superusers
- Unread notification counter
- Responsive to user permissions

---

## Template Tags

### `utils/templatetags/rights.py`

#### `@register.filter can_interact(user)`
**Purpose**: Check if user can interact with content (post, comment, like).

**Parameters**: 
- `user` (User): User object to check

**Returns**: Boolean indicating interaction permission

**Checks**:
- User is active
- Email is confirmed
- Account is not banned

**Template Usage**:
```django
{% if user|can_interact %}
    <button class="like-button">Like</button>
{% endif %}
```

---

#### `@register.filter can_edit_post(post, user)`
**Purpose**: Check if user can edit a specific post.

**Parameters**: 
- `post` (Post): Post object
- `user` (User): User object

**Returns**: Boolean indicating edit permission

**Conditions**:
- User is the post author
- User can interact with content
- Post is within edit time limit (default: 7 days)

---

#### `@register.filter can_delete_comment(comment, user)`
**Purpose**: Check if user can delete a specific comment.

**Parameters**: 
- `comment` (Comment): Comment object
- `user` (User): User object

**Returns**: Boolean indicating delete permission

**Conditions**:
- User is the comment author
- User can interact with content
- Comment is within delete time limit (default: 7 days)

---

#### `@register.filter get_interaction_restriction_reason(user)`
**Purpose**: Get human-readable reason why user cannot interact.

**Parameters**: 
- `user` (User): User object to check

**Returns**: String with restriction reason

**Possible Reasons**:
- "Ваш аккаунт не активен." (Account not active)
- "Требуется подтверждение email." (Email confirmation required)
- "" (No restrictions)

**Template Usage**:
```django
{% if not user|can_interact %}
    <div class="alert alert-warning">
        {{ user|get_interaction_restriction_reason }}
    </div>
{% endif %}
```

---

## Management Commands

### `utils/management/commands/prepare_env.py`

#### `Command.handle(*args, **options)`
**Purpose**: Prepare development environment by creating necessary directories.

**Executes**:
1. `prepare_media` - Creates media directory
2. `prepare_static` - Creates static files directory  
3. `prepare_logs` - Creates logs directory

**Usage**:
```bash
python manage.py prepare_env
```

**Features**:
- Automatically runs on app startup
- Error handling for each step
- Colored output for better UX

---

### Model Methods Documentation

### `accounts/models.py`

#### `CustomUser.is_fully_active`
**Purpose**: Property to check if user has full platform access.

**Returns**: Boolean indicating full access permission

**Checks**:
- `is_active` is True
- `is_email_confirmed` is True

**Usage**: Used by template tags and views to control access

---

#### `CustomUser.full_name()`
**Purpose**: Get user's formatted full name.

**Returns**: Concatenated first and last name, stripped of whitespace

**Fallback**: Returns empty string if no names provided

---

### `social/models.py`

#### `Post.get_absolute_url()`
**Purpose**: Get canonical URL for post detail page.

**Returns**: String URL path for the post

**Usage**: Used in notifications and template links

---

#### `Post.comments_count()`
**Purpose**: Get total number of comments for the post.

**Returns**: Integer count of related comments

**Note**: Uses Django's reverse relationship

---

#### `Post.likes_count()`
**Purpose**: Get total number of likes for the post.

**Returns**: Integer count of users who liked the post

**Note**: Uses ManyToMany count

---

## Security Notes

### Permission System
- All interactive features require `can_interact` check
- Time-limited editing/deletion prevents abuse
- CSRF protection on all state-changing operations
- Email confirmation required for full access

### Data Validation
- All forms use Django's built-in validation
- File uploads validated for type and size
- User input sanitized through template system
- SQL injection prevented through ORM usage

### Authentication
- Django's built-in session authentication
- Password validation with multiple validators
- Token-based email confirmation
- Secure password reset functionality