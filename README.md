# 🚀 AI Website Builder

> Transform your ideas into fully functional websites using the power of AI. Just describe what you want, and watch it come to life!

[![Next.js](https://img.shields.io/badge/Next.js-14.2.3-black?style=flat-square&logo=next.js)](https://nextjs.org/)
[![React](https://img.shields.io/badge/React-18-blue?style=flat-square&logo=react)](https://reactjs.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4-06B6D4?style=flat-square&logo=tailwindcss)](https://tailwindcss.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-6.6-green?style=flat-square&logo=mongodb)](https://mongodb.com/)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini%20AI-4285F4?style=flat-square&logo=google)](https://ai.google.dev/)

## ✨ Features

### 🤖 **AI-Powered Generation**
- **Natural Language Input**: Describe your website in plain English
- **Google Gemini AI**: Powered by advanced `gemini-1.5-flash` model
- **Intelligent Code Generation**: Creates semantic HTML, modern CSS, and interactive JavaScript
- **Framework Support**: Automatic React, Tailwind CSS, and vanilla JavaScript generation

### 👀 **Live Preview System**
- **Real-time Rendering**: Instant preview of generated websites
- **Responsive Design Testing**: Desktop, tablet, and mobile viewports
- **Interactive Preview**: Full functionality testing within sandbox
- **Secure Execution**: Sandboxed iframe for safe code execution

### 📦 **Download & Export**
- **One-Click Download**: Complete website as ZIP file
- **Production Ready**: Optimized code for immediate deployment
- **Deployment Instructions**: Comprehensive README with hosting guides
- **Cross-Platform Compatibility**: Works with all major hosting services

### 🎨 **Modern UI/UX**
- **Clean Interface**: Intuitive design with shadcn/ui components
- **Example Prompts**: Pre-built inspiration for quick starts
- **Progressive Enhancement**: Smooth workflow from input to download
- **Responsive Design**: Perfect experience on all devices

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ ([Download](https://nodejs.org/))
- **MongoDB** ([Local Installation](https://docs.mongodb.com/manual/installation/) or [MongoDB Atlas](https://www.mongodb.com/cloud/atlas))
- **Google Gemini API Key** ([Get API Key](https://ai.google.dev/))

### Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd ai-website-builder
   ```

2. **Install Dependencies**
   ```bash
   yarn install
   ```

3. **Environment Setup**
   
   Create `.env` file in the project root:
   ```env
   # Required: Google Gemini AI API Key
   GEMINI_API_KEY=your_gemini_api_key_here
   
   # Required: MongoDB Connection
   MONGO_URL=mongodb://localhost:27017
   DB_NAME=ai_website_builder
   
   # Optional: Application Configuration
   NEXT_PUBLIC_BASE_URL=http://localhost:3000
   CORS_ORIGINS=*
   ```

4. **Start Development Server**
   ```bash
   yarn dev
   ```

5. **Open Application**
   
   Visit [http://localhost:3000](http://localhost:3000) in your browser

## 🎯 How to Use

### 1. **Describe Your Website**
Write a natural language description of your desired website:

```
Create a modern portfolio website for a photographer with:
- Dark theme and elegant typography
- Image gallery with lightbox functionality  
- About section with bio and services
- Contact form with social media links
- Mobile-responsive design using Tailwind CSS
```

### 2. **Generate & Preview**
- Click **"Generate Website"** button
- Watch as AI creates your website in real-time
- Use responsive preview modes to test different screen sizes
- Interact with the generated website directly in the preview

### 3. **Download & Deploy**
- Click **"Download ZIP File"** to get your complete website
- Extract the ZIP file containing:
  - `index.html` - Your complete website
  - `README.md` - Deployment instructions and documentation

### 4. **Deploy Anywhere**
Your generated website works with all major hosting platforms:
- **Netlify**: Drag & drop deployment
- **Vercel**: Git-based or direct upload
- **GitHub Pages**: Repository-based hosting
- **Traditional Web Hosting**: FTP/SFTP upload

## 🛠️ Technical Architecture

### Frontend Stack
```
Next.js 14.2.3        # React framework with SSR
React 18               # Modern React with hooks
Tailwind CSS 3.4+      # Utility-first CSS framework
shadcn/ui              # High-quality component library
Radix UI               # Accessible primitive components
```

### Backend Stack
```
Next.js API Routes     # Serverless API endpoints
Google Generative AI   # Gemini AI integration
MongoDB 6.6+           # Document database
JSZip                  # Client-side ZIP creation
```

### Project Structure
```
ai-website-builder/
├── app/                    # Next.js app directory
│   ├── api/               # API routes
│   │   └── [[...path]]/   # Dynamic API routing
│   ├── globals.css        # Global styles
│   ├── layout.js          # Root layout
│   └── page.js            # Main application page
├── components/            # Reusable UI components
│   └── ui/               # shadcn/ui components
├── hooks/                # Custom React hooks
├── lib/                  # Utility functions
├── public/               # Static assets
├── .env                  # Environment variables
├── package.json          # Dependencies
├── tailwind.config.js    # Tailwind configuration
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GEMINI_API_KEY` | Google Gemini AI API key | ✅ Yes | - |
| `MONGO_URL` | MongoDB connection string | ✅ Yes | `mongodb://localhost:27017` |
| `DB_NAME` | MongoDB database name | ✅ Yes | `ai_website_builder` |
| `NEXT_PUBLIC_BASE_URL` | Application base URL | No | `http://localhost:3000` |
| `CORS_ORIGINS` | CORS allowed origins | No | `*` |

### MongoDB Collections

The application automatically creates these collections:

- **`generations`**: Stores website generation history
  ```json
  {
    "id": "uuid",
    "prompt": "user description",
    "code": "generated HTML",
    "timestamp": "2025-01-01T00:00:00Z"
  }
  ```

- **`status_checks`**: System health monitoring
  ```json
  {
    "id": "uuid", 
    "client_name": "status check",
    "timestamp": "2025-01-01T00:00:00Z"
  }
  ```

## 📡 API Reference

### Generate Website
**POST** `/api/generate`

Generate a website from natural language description.

```bash
curl -X POST http://localhost:3000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Create a modern portfolio website..."}'
```

**Response:**
```json
{
  "success": true,
  "code": "<!DOCTYPE html><html>...</html>",
  "id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Download Project
**POST** `/api/download`

Create downloadable ZIP file from generated code.

```bash
curl -X POST http://localhost:3000/api/download \
  -H "Content-Type: application/json" \
  -d '{"code": "<!DOCTYPE html>..."}' \
  --output website.zip
```

### Generation History
**GET** `/api/generations`

Retrieve recent website generations.

```bash
curl http://localhost:3000/api/generations
```

## 🎨 Customization

### UI Components

The application uses [shadcn/ui](https://ui.shadcn.com/) components. To customize:

1. **Colors & Themes**: Edit `app/globals.css` CSS variables
2. **Components**: Modify files in `components/ui/`
3. **Layout**: Update `app/layout.js` and `app/page.js`

### AI Prompting

Customize AI behavior in `/app/api/[[...path]]/route.js`:

```javascript
const systemPrompt = `You are an expert web developer. Generate a complete, production-ready website...`
```

### Database Schema

Add new fields to MongoDB collections by updating the API route handlers.

## 🚦 Development

### Available Scripts

```bash
# Development server with hot reload
yarn dev

# Production build
yarn build

# Start production server  
yarn start

# Development without reload (debugging)
yarn dev:no-reload
```

### Code Quality

- **ESLint**: Code linting and formatting
- **Prettier**: Code formatting (configured in VS Code)
- **TypeScript**: Gradual type safety adoption

### Testing

Run manual tests:
```bash
# Test API endpoints
curl -X POST http://localhost:3000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Create a simple landing page"}'

# Test database connection
curl http://localhost:3000/api/generations
```

## 📈 Performance

### Optimization Features

- **Next.js SSR**: Server-side rendering for faster initial loads
- **Code Splitting**: Automatic bundle optimization
- **Image Optimization**: Built-in Next.js image optimization
- **Caching**: Browser and server-side caching strategies

### Monitoring

- **Generation Success Rate**: Track AI generation quality
- **Response Times**: Monitor API performance
- **Error Tracking**: Comprehensive error logging
- **Resource Usage**: Memory and CPU monitoring

## 🔒 Security

### AI Safety
- **Input Validation**: Sanitize user prompts
- **Output Filtering**: Validate generated code
- **Rate Limiting**: Prevent API abuse

### Data Protection
- **Environment Variables**: Secure API key storage
- **Sandbox Execution**: Isolated preview rendering
- **CORS Configuration**: Controlled cross-origin requests

## 🌍 Deployment

### Production Deployment

#### Vercel (Recommended)
1. **Deploy to Vercel**
   ```bash
   npx vercel --prod
   ```

2. **Configure Environment Variables**
   - Add all `.env` variables in Vercel dashboard
   - Update `NEXT_PUBLIC_BASE_URL` to your domain

#### Netlify
1. **Build Settings**
   - Build command: `yarn build`
   - Publish directory: `.next`

2. **Environment Variables**
   - Configure in Netlify site settings

#### Docker Deployment
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN yarn install --production
COPY . .
RUN yarn build
EXPOSE 3000
CMD ["yarn", "start"]
```

### Database Hosting

#### MongoDB Atlas (Recommended)
1. Create cluster at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Get connection string
3. Update `MONGO_URL` environment variable

#### Self-hosted MongoDB
```bash
# Using Docker
docker run -d -p 27017:27017 --name mongodb mongo:6.6
```

## 🤝 Contributing

### Development Setup

1. **Fork the Repository**
2. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make Changes**
4. **Test Thoroughly**
5. **Submit Pull Request**

### Contribution Guidelines

- Follow existing code style and patterns
- Add tests for new features
- Update documentation for API changes
- Ensure responsive design compatibility
- Test across different browsers and devices

## 📞 Support & Community

### Getting Help

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues) for bugs and features
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions) for questions
- **Documentation**: This README and inline code comments

### Common Issues & Solutions

#### AI Generation Failures
```bash
# Check API key configuration
echo $GEMINI_API_KEY

# Verify MongoDB connection
curl http://localhost:3000/api/status
```

#### Build Issues
```bash
# Clear Next.js cache
rm -rf .next

# Reinstall dependencies  
rm -rf node_modules package-lock.json
yarn install
```

#### Performance Issues
- Monitor MongoDB performance and add indexes
- Check Gemini API rate limits and quotas
- Optimize large file handling and chunking

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** - Powering the intelligent code generation
- **Next.js Team** - Amazing React framework and developer experience  
- **shadcn** - Beautiful and accessible UI components
- **Tailwind CSS** - Utility-first CSS framework
- **MongoDB** - Flexible document database
- **Open Source Community** - Libraries and tools that make this possible

---

## 🚀 Start Building Today!

Ready to create amazing websites with AI? Get started in minutes:

```bash
git clone <repository-url>
cd ai-website-builder
yarn install
# Add your GEMINI_API_KEY to .env
yarn dev
```

Visit [http://localhost:3000](http://localhost:3000) and describe your dream website! 🎨✨