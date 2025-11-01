# AI Visibility Tracker - Frontend

A modern React frontend for the AI Visibility Tracker MVP, built with TypeScript, Tailwind CSS, and React Query.

## Features

- **Modern UI**: Clean, responsive design with Tailwind CSS
- **Target Management**: Create, view, and edit business targets
- **Real-time Analysis**: Run visibility analysis with detailed results
- **Interactive Charts**: Visualize analysis results with Recharts
- **API Integration**: Seamless integration with FastAPI backend
- **Error Handling**: Comprehensive error boundaries and loading states
- **Settings**: Configure OpenAI API key for AI features

## Tech Stack

- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **React Query** for data fetching and caching
- **React Router** for navigation
- **Recharts** for data visualization
- **Lucide React** for icons
- **Axios** for API calls

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- Backend API running on http://localhost:8000

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Environment Variables

Create a `.env` file in the frontend directory:

```bash
VITE_API_URL=http://localhost:8000
```

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Layout.tsx      # Main layout with sidebar
│   ├── TargetForm.tsx  # Target creation form
│   ├── TargetCard.tsx  # Target display card
│   ├── AnalysisResults.tsx # Analysis visualization
│   └── ...
├── pages/              # Page components
│   ├── Dashboard.tsx   # Main dashboard
│   ├── AnalysisPage.tsx # Analysis results page
│   └── SettingsPage.tsx # Settings page
├── lib/                # Utilities and API client
│   └── api.ts         # API client with Axios
├── types/              # TypeScript type definitions
│   └── api.ts         # API response types
└── App.tsx            # Main app component
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Features Overview

### Dashboard
- Overview of all targets
- Quick stats and metrics
- Add new targets
- Navigate to analysis

### Target Management
- Create targets with business name and website
- Edit keywords and prompts inline
- AI-generated content (when OpenAI API key is configured)
- Delete targets

### Analysis
- Run visibility analysis
- Interactive charts and visualizations
- Detailed results table
- Score breakdown and metrics

### Settings
- Configure OpenAI API key
- Enable/disable AI features
- Setup instructions

## API Integration

The frontend communicates with the FastAPI backend through:

- `POST /api/targets/init` - Create new target
- `GET /api/targets/{id}` - Get target details
- `PUT /api/targets/{id}/keywords` - Update keywords
- `PUT /api/targets/{id}/prompts` - Update prompts
- `POST /api/targets/{id}/analyze` - Run analysis

## Development

### Adding New Features

1. Create components in `src/components/`
2. Add pages in `src/pages/`
3. Update API client in `src/lib/api.ts`
4. Add types in `src/types/api.ts`

### Styling

- Use Tailwind CSS classes
- Custom components in `src/index.css`
- Responsive design with mobile-first approach

### State Management

- React Query for server state
- React hooks for local state
- No global state management needed for MVP

## Production Build

```bash
npm run build
```

The built files will be in the `dist/` directory, ready for deployment.

## License

MIT