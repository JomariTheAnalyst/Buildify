import { MongoClient } from 'mongodb'
import { v4 as uuidv4 } from 'uuid'
import { NextResponse } from 'next/server'
import { GoogleGenerativeAI } from '@google/generative-ai'
import JSZip from 'jszip'

// Initialize Gemini AI
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY)

// MongoDB connection
let client
let db

async function connectToMongo() {
  if (!client) {
    client = new MongoClient(process.env.MONGO_URL)
    await client.connect()
    db = client.db(process.env.DB_NAME)
  }
  return db
}

// Helper function to handle CORS
function handleCORS(response) {
  response.headers.set('Access-Control-Allow-Origin', process.env.CORS_ORIGINS || '*')
  response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
  response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization')
  response.headers.set('Access-Control-Allow-Credentials', 'true')
  return response
}

// OPTIONS handler for CORS
export async function OPTIONS() {
  return handleCORS(new NextResponse(null, { status: 200 }))
}

// Generate website using Gemini AI
async function generateWebsiteCode(prompt) {
  const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" })

  const systemPrompt = `You are an expert web developer. Generate a complete, production-ready website based on the user's description. Follow these guidelines:

1. ALWAYS create a complete HTML document with proper structure
2. Use modern, responsive CSS (prefer Tailwind CDN if not specified otherwise)
3. Include interactive JavaScript when needed
4. Make it visually appealing with modern design principles
5. Ensure mobile responsiveness
6. Use semantic HTML elements
7. Include proper meta tags and title
8. If React is requested, create a complete HTML file with React CDN and JSX transformed to regular JavaScript
9. Default to React + Tailwind CSS if no specific framework is mentioned
10. Include sample content that makes sense for the type of website

IMPORTANT: Return ONLY the complete HTML code, no explanations or markdown formatting.`

  const fullPrompt = `${systemPrompt}\n\nUser Request: ${prompt}`

  try {
    const result = await model.generateContent(fullPrompt)
    const response = await result.response
    let code = response.text()

    // Clean up the response - remove any markdown formatting
    code = code.replace(/```html/g, '').replace(/```/g, '').trim()

    return code
  } catch (error) {
    console.error('Gemini AI Error:', error)
    throw new Error('Failed to generate website code')
  }
}

// Create downloadable ZIP file
async function createProjectZip(code) {
  const zip = new JSZip()

  // Extract title from HTML for folder name
  const titleMatch = code.match(/<title>(.*?)<\/title>/i)
  const projectName = titleMatch ? titleMatch[1].replace(/[^a-zA-Z0-9]/g, '-').toLowerCase() : 'my-website'

  // Add main HTML file
  zip.file('index.html', code)

  // Create a basic README
  const readme = `# ${titleMatch ? titleMatch[1] : 'Generated Website'}

This website was generated using AI Website Builder.

## Getting Started

1. Open \`index.html\` in your web browser to view the website
2. Upload the files to any web hosting service (Netlify, Vercel, GitHub Pages, etc.)
3. Customize the content as needed

## Files

- \`index.html\` - Main website file
- \`README.md\` - This file

## Hosting Options

- **Netlify**: Drag and drop the files to netlify.com/drop
- **Vercel**: Upload via vercel.com
- **GitHub Pages**: Commit to a GitHub repository and enable Pages
- **Any web server**: Upload files to your hosting provider

Generated on: ${new Date().toISOString()}
`

  zip.file('README.md', readme)

  return await zip.generateAsync({ type: 'nodebuffer' })
}

// Route handler function
async function handleRoute(request, { params }) {
  const { path = [] } = params
  const route = `/${path.join('/')}`
  const method = request.method

  try {
    const db = await connectToMongo()

    // Root endpoint
    if (route === '/' && method === 'GET') {
      return handleCORS(NextResponse.json({ message: "AI Website Builder API" }))
    }

    // Generate website endpoint
    if (route === '/generate' && method === 'POST') {
      const body = await request.json()
      const { prompt } = body

      if (!prompt || typeof prompt !== 'string') {
        return handleCORS(NextResponse.json(
          { error: "Prompt is required and must be a string" }, 
          { status: 400 }
        ))
      }

      try {
        const generatedCode = await generateWebsiteCode(prompt)

        // Store generation in database
        const generation = {
          id: uuidv4(),
          prompt,
          code: generatedCode,
          timestamp: new Date(),
        }

        await db.collection('generations').insertOne(generation)

        return handleCORS(NextResponse.json({
          success: true,
          code: generatedCode,
          id: generation.id
        }))

      } catch (error) {
        console.error('Generation error:', error)
        return handleCORS(NextResponse.json(
          { error: error.message || "Failed to generate website" },
          { status: 500 }
        ))
      }
    }

    // Download project endpoint
    if (route === '/download' && method === 'POST') {
      const body = await request.json()
      const { code } = body

      if (!code || typeof code !== 'string') {
        return handleCORS(NextResponse.json(
          { error: "Code is required" }, 
          { status: 400 }
        ))
      }

      try {
        const zipBuffer = await createProjectZip(code)

        return new NextResponse(zipBuffer, {
          status: 200,
          headers: {
            'Content-Type': 'application/zip',
            'Content-Disposition': 'attachment; filename="generated-website.zip"',
            'Access-Control-Allow-Origin': process.env.CORS_ORIGINS || '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
          },
        })

      } catch (error) {
        console.error('Download error:', error)
        return handleCORS(NextResponse.json(
          { error: "Failed to create download package" },
          { status: 500 }
        ))
      }
    }

    // Get generations history endpoint
    if (route === '/generations' && method === 'GET') {
      const generations = await db.collection('generations')
        .find({})
        .sort({ timestamp: -1 })
        .limit(50)
        .toArray()

      // Remove MongoDB's _id field and large code field from list
      const cleanedGenerations = generations.map(({ _id, code, ...rest }) => ({
        ...rest,
        preview: code.substring(0, 200) + '...'
      }))
      
      return handleCORS(NextResponse.json(cleanedGenerations))
    }

    // Status endpoints
    if (route === '/status' && method === 'POST') {
      const body = await request.json()
      
      if (!body.client_name) {
        return handleCORS(NextResponse.json(
          { error: "client_name is required" }, 
          { status: 400 }
        ))
      }

      const statusObj = {
        id: uuidv4(),
        client_name: body.client_name,
        timestamp: new Date()
      }

      await db.collection('status_checks').insertOne(statusObj)
      return handleCORS(NextResponse.json(statusObj))
    }

    if (route === '/status' && method === 'GET') {
      const statusChecks = await db.collection('status_checks')
        .find({})
        .limit(1000)
        .toArray()

      const cleanedStatusChecks = statusChecks.map(({ _id, ...rest }) => rest)
      
      return handleCORS(NextResponse.json(cleanedStatusChecks))
    }

    // Route not found
    return handleCORS(NextResponse.json(
      { error: `Route ${route} not found` }, 
      { status: 404 }
    ))

  } catch (error) {
    console.error('API Error:', error)
    return handleCORS(NextResponse.json(
      { error: "Internal server error" }, 
      { status: 500 }
    ))
  }
}

// Export all HTTP methods
export const GET = handleRoute
export const POST = handleRoute
export const PUT = handleRoute
export const DELETE = handleRoute
export const PATCH = handleRoute