# Autonomous Coding Agent - Modern Dashboard

A stunning, modern AI-powered coding assistant interface with full-page layout and professional design.

## Features

### Visual Design
- **Full Page Layout**: 100% width and height utilization
- **Modern Glassmorphism**: Frosted glass effects with backdrop blur
- **Animated Background**: Floating particles with gradient effects
- **Professional Dashboard**: Similar to ChatGPT and GitHub Copilot interfaces

### Layout Structure
- **Header**: Attractive title with gradient text effect
- **3-Column Grid Layout**:
  - Left Panel (25%): Code generation controls
  - Center Panel (50%): Large Monaco-style code editor
  - Right Panel (25%): Agent activity monitoring
- **Bottom Console**: Terminal-style output display

### Interactive Elements
- **Animated Buttons**: Gradient effects with hover animations
- **Agent Status**: Real-time workflow visualization
- **Code Editor**: Dark theme with syntax highlighting
- **Console**: Terminal-style output with timestamps

### Responsive Design
- Full HD screens (1920x1080)
- Laptop screens (1366x768)
- Tablets (768px and below)
- Mobile-optimized layout

## Technical Specifications

### Colors & Gradients
- Primary: `linear-gradient(135deg, #667eea, #764ba2)`
- Success: `linear-gradient(135deg, #4facfe, #00f2fe)`
- Warning: `linear-gradient(135deg, #fa709a, #fee140)`
- Glass: `rgba(255, 255, 255, 0.1)` with backdrop blur

### Typography
- Font: Inter (Google Fonts)
- Weights: 300, 400, 500, 600, 700
- Monospace: Monaco, Menlo, Consolas

### Animations
- Floating particles (20s duration)
- Button hover effects (0.3s cubic-bezier)
- Panel entrance animations
- Agent status transitions
- Loading spinners

### Performance Features
- GPU-accelerated animations
- Will-change optimizations
- Reduced motion support
- High DPI display optimizations

## File Structure

```
frontend/
dashboard.html          # Main dashboard interface
styles.css              # Additional styling and animations
simple.html             # Original simple interface
fixed_frontend_server.py # Frontend server
```

## Usage

1. Start the backend server:
   ```bash
   cd backend
   python simple_server.py
   ```

2. Start the frontend server:
   ```bash
   cd frontend
   python fixed_frontend_server.py
   ```

3. Open http://localhost:3000 in your browser

## Interface Features

### Code Generation Controls
- Programming language dropdown (Python, JavaScript, Java, C++, C)
- Prompt input textarea with placeholder text
- Generate Code button with gradient styling
- Action buttons: Run, Debug, Optimize, Explain

### Code Editor
- Monaco editor-style dark theme
- File tab with language-specific extensions
- Copy, download, and settings buttons
- Full-height editor with line numbers

### Agent Activity Panel
- 6 AI agents with real-time status
- Animated status indicators
- Execution time tracking
- Progress descriptions

### Output Console
- Terminal-style dark background
- Timestamped messages
- Clear and copy functionality
- Auto-scroll to latest output

## Keyboard Shortcuts

- `Ctrl+Enter`: Generate Code
- `Ctrl+R`: Run Code
- `Ctrl+D`: Debug Code
- `Ctrl+O`: Optimize Code
- `Ctrl+E`: Explain Code

## Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Performance

- 60fps animations
- <100ms interaction response
- Optimized for GPU acceleration
- Memory-efficient particle system

## Design Inspiration

- ChatGPT interface aesthetics
- GitHub Copilot dashboard
- Modern AI developer tools
- Glassmorphism design trends

## Customization

### Colors
Modify CSS variables in `dashboard.html`:
```css
:root {
    --primary-gradient: linear-gradient(135deg, #667eea, #764ba2);
    --glass-bg: rgba(255, 255, 255, 0.1);
    /* Add more variables */
}
```

### Layout
Adjust grid percentages in `.main-container`:
```css
.main-container {
    grid-template-columns: 25% 50% 25%; /* Customize as needed */
}
```

### Animations
Modify particle count and speed in JavaScript:
```javascript
// Change particle count
for (let i = 0; i < 50; i++) { /* Adjust number */

// Change animation duration
particle.style.animationDuration = (15 + Math.random() * 10) + 's';
```

## Development

The dashboard uses modern web technologies:
- HTML5 semantic elements
- CSS3 with custom properties
- Vanilla JavaScript (ES6+)
- CSS Grid and Flexbox
- Font Awesome icons
- Google Fonts typography

## License

This project is part of the Autonomous Coding Agent system.
