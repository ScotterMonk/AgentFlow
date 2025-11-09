# HTML and CSS Design Patterns

## Template Structure
Reference `templates/layout.html` for the base template structure.

Standard page structure:
```html
{% extends "layout.html" %}
{% block content %}
<div class="flex items-start justify-center bg-neutral-50 p-4">
    <div style="max-width: 800px; width: 100%;">
        <div class="card">
            <div class="card-header">
                <h2>Page Title</h2>
                <p class="text-secondary" style="margin-bottom:0;">Subtitle</p>
            </div>
            <div class="card-body">
                <!-- Main content -->
            </div>
            <div class="card-footer text-center">
                <!-- Footer links -->
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

Key layout components:
- `.content-container` - Main content wrapper with max-width and padding
- `.card`, `.card-header`, `.card-body`, `.card-footer` - Card-based layouts
- `.container-table` - Table wrapper with border, rounded corners, overflow-x-auto

## CSS Variable System
Reference `static/css/main.css` for complete variable definitions. Always use CSS variables instead of hardcoded values.

Common variables:
- Brand colors: `--color-dark-blue`, `--color-light-blue`, `--color-orange`, `--color-purple`
- Text: `--color-text-primary`, `--color-text-secondary`
- Borders: `--color-border-faint`, `--color-border-light`, `--color-border-focused`
- Spacing: `--spacing-00` through `--spacing-09`
- Border radius: `--border-radius-lg`, `--border-radius-xl`, `--border-radius-full`
- Typography: `--font-size-xs` through `--font-size-5xl`

## Form Patterns

Standard form structure:
```html
<form id="formId" method="POST" action="{{ url_for('route.name') }}">
    <input id="csrf_token" name="csrf_token" type="hidden" value="{{ csrf_token() }}">
    
    <div class="form-group">
        <label class="form-label" for="field">
            Label <span class="required-indicator">*</span>
        </label>
        <input type="text" id="field" name="field" class="form-input" required>
    </div>
</form>
```

Horizontal layouts (toolbar pattern):
```html
<div class="toolbar-row">
    <div class="form-group">
        <label class="form-label">Label</label>
        <input type="text" class="form-input w-020" readonly>
    </div>
    <div class="form-group">
        <label class="form-label">Label 2</label>
        <input type="text" class="form-input w-050">
    </div>
</div>
```

Checkbox/radio controls:
```html
<div class="form-check-group">
    <input type="checkbox" name="field" id="field">
    <label for="field">Label text</label>
</div>
```

## Table Patterns

Standard table structure:
```html
<div class="container-table">
    <table class="w-full text-sm">
        <thead>
            <tr class="border-b border-light bg-neutral-200">
                <th class="text-left p-2">Header</th>
                <th class="text-center p-2">Centered</th>
            </tr>
        </thead>
        <tbody>
            {% for item in items %}
            <tr class="border-b border-light {% if loop.index is divisibleby(2) %}bg-neutral-50{% else %}bg-white{% endif %} hover:bg-primary-50">
                <td class="p-2">{{ item.field }}</td>
                <td class="text-center p-2">{{ item.value }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
```

Action buttons in tables:
```html
<td class="text-center">
    <div class="flex justify-center gap-2">
        <button class="icon-btn rounded-full bg-light-blue text-white hover:bg-dark-blue"
                onclick="editItem({{ item.id }})" title="Edit">✎</button>
        <button class="icon-btn rounded-full bg-red text-white hover:bg-orange"
                onclick="deleteItem({{ item.id }})" title="Delete">×</button>
    </div>
</td>
```

Empty state:
```html
{% if items %}
    <!-- Table -->
{% else %}
    <p class="text-secondary text-center p-4">No items found.</p>
{% endif %}
```

Form classes:
- `.form-group`, `.form-check-group` - Field wrappers with standardized spacing
- `.form-input` - All input types (text, select, textarea)
- `.form-label` - Label styling
- `.required-indicator` - Orange asterisk for required fields
- `.toolbar-row` - Horizontal layout for forms/controls

Width utilities: `.w-010` (3rem) through `.w-100` (20rem)

## Button System

Button types (defined in `static/css/main.css`):
- `.nav-link` - Navigation only; dark blue bg, white text; hover: light blue; active: orange
- `.btn` - Default button; dark blue bg; hover: light blue
- `.btn-med` - Medium size with smaller padding
- `.btn-big` - Primary actions (form submissions); larger padding
- `.icon-btn` - Square icon buttons (1.6rem × 1.6rem)

Button usage:
```html
<button class="btn">Cancel</button>
<button class="btn-big">Submit</button>
<button class="icon-btn rounded-full bg-light-blue text-white hover:bg-dark-blue" title="Edit">✎</button>
```

## Utility Classes
Reference `static/css/main.css` for full list. Common utilities:

Flexbox: `.flex`, `.flex-col`, `.items-center`, `.justify-between`, `.gap-2`
Spacing: `.m-0` through `.m-6`, `.mt-0`, `.mb-4`, `.p-0` through `.p-6`
Text: `.text-center`, `.text-xs`, `.text-sm`, `.text-primary`, `.text-secondary`
Background: `.bg-white`, `.bg-neutral-50`, `.bg-dark-blue`, `.bg-light-blue`
Border: `.border`, `.border-light`, `.rounded-lg`, `.rounded-full`
Display: `.hidden`, `.block`, `.flex`
Width: `.w-full`, `.w-020` through `.w-100`

## Design Standards

CSS file usage:
- Single CSS file: `static/css/main.css`
- Always use CSS variables instead of hardcoded values
- Minimal inline CSS (only for max-width constraints on wrappers)
- Keep CSS comments minimal

Templates:
- Set VS Code language mode to `jinja-html`
- Reference `.roo/rules/01-general.md` for naming conventions

Visual consistency:
- Curved corners: Use `--border-radius-lg` variable
- Focus states: Border changes from `--color-border-faint` to `--color-border-focused` (orange)
- Checkbox/radio spacing: 4px gap between control and label (using `.form-check-group`)
- Compact spacing throughout

Button principles:
- No borders (transparent border)
- Hover changes background color, text stays white
- Three types: `.nav-link` (navigation only), `.btn` (default), `.btn-big` (primary actions)

Accessibility:
- Favoring simplicity over complex ARIA features
- Use semantic HTML and simple, highly-compatible patterns

Movement:
- Minimize page element movement
- Avoid transitions/animations unless necessary (propose to user first)
