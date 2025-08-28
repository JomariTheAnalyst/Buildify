'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Textarea } from '@/components/ui/textarea'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Download, Eye, Sparkles, Code, Monitor, Tablet, Smartphone } from 'lucide-react'
import { Alert, AlertDescription } from '@/components/ui/alert'

export default function App() {
  const [prompt, setPrompt] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedCode, setGeneratedCode] = useState('')
  const [previewMode, setPreviewMode] = useState('desktop')
  const [error, setError] = useState('')

  const examplePrompts = [
    "Create a modern portfolio website for a photographer with a dark theme and image gallery",
    "Build a restaurant website with menu sections, location, and contact form",
    "Design a SaaS landing page with pricing tiers and feature showcase",
    "Create a personal blog with article cards and author bio section"
  ]

  const generateWebsite = async () => {
    if (!prompt.trim()) return

    setIsGenerating(true)
    setError('')

    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'Failed to generate website')
      }

      setGeneratedCode(data.code)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsGenerating(false)
    }
  }

  const downloadProject = async () => {
    if (!generatedCode) return

    try {
      const response = await fetch('/api/download', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code: generatedCode }),
      })

      if (!response.ok) {
        throw new Error('Failed to create download package')
      }

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.style.display = 'none'
      a.href = url
      a.download = 'generated-website.zip'
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (err) {
      setError(err.message)
    }
  }

  const getPreviewStyles = () => {
    switch (previewMode) {
      case 'tablet':
        return 'max-w-3xl h-[600px]'
      case 'mobile':
        return 'max-w-sm h-[700px]'
      default:
        return 'w-full h-[600px]'
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4 flex items-center justify-center gap-2">
            <Sparkles className="text-blue-600" />
            AI Website Builder
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Transform your ideas into fully functional websites using the power of AI. 
            Just describe what you want, and watch it come to life!
          </p>
        </div>

        {/* Main Content */}
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Input Section */}
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Code className="w-5 h-5" />
                  Describe Your Website
                </CardTitle>
                <CardDescription>
                  Tell us what kind of website you want to create. Be as specific as possible!
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <Textarea
                  placeholder="e.g., Create a modern portfolio website for a photographer with a dark theme, image gallery, about section, and contact form using React and Tailwind CSS..."
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  className="min-h-[120px] resize-none"
                />

                <Button 
                  onClick={generateWebsite}
                  disabled={isGenerating || !prompt.trim()}
                  className="w-full"
                  size="lg"
                >
                  {isGenerating ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Generating Website...
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-4 h-4 mr-2" />
                      Generate Website
                    </>
                  )}
                </Button>

                {error && (
                  <Alert variant="destructive">
                    <AlertDescription>{error}</AlertDescription>
                  </Alert>
                )}
              </CardContent>
            </Card>

            {/* Example Prompts */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Example Prompts</CardTitle>
                <CardDescription>
                  Click on any example to get started quickly
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {examplePrompts.map((example, index) => (
                    <Badge
                      key={index}
                      variant="outline"
                      className="cursor-pointer hover:bg-blue-50 p-3 text-sm font-normal h-auto whitespace-normal text-left justify-start"
                      onClick={() => setPrompt(example)}
                    >
                      {example}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Actions */}
            {generatedCode && (
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Actions</CardTitle>
                  <CardDescription>
                    Your website is ready! Preview it or download the files.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Button 
                    onClick={downloadProject}
                    className="w-full"
                    variant="outline"
                  >
                    <Download className="w-4 h-4 mr-2" />
                    Download ZIP File
                  </Button>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Preview Section */}
          <div className="space-y-4">
            {generatedCode ? (
              <Card className="h-full">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Eye className="w-5 h-5" />
                      <CardTitle className="text-lg">Live Preview</CardTitle>
                    </div>
                    
                    {/* Device Toggle */}
                    <div className="flex gap-1 bg-gray-100 rounded-lg p-1">
                      <button
                        onClick={() => setPreviewMode('desktop')}
                        className={`p-2 rounded ${previewMode === 'desktop' ? 'bg-white shadow' : ''}`}
                      >
                        <Monitor className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => setPreviewMode('tablet')}
                        className={`p-2 rounded ${previewMode === 'tablet' ? 'bg-white shadow' : ''}`}
                      >
                        <Tablet className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => setPreviewMode('mobile')}
                        className={`p-2 rounded ${previewMode === 'mobile' ? 'bg-white shadow' : ''}`}
                      >
                        <Smartphone className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="p-4">
                  <div className={`mx-auto bg-white rounded-lg shadow-lg overflow-hidden ${getPreviewStyles()}`}>
                    <iframe
                      srcDoc={generatedCode}
                      className="w-full h-full border-0"
                      title="Website Preview"
                      sandbox="allow-scripts allow-same-origin"
                    />
                  </div>
                </CardContent>
              </Card>
            ) : (
              <Card className="h-full flex items-center justify-center">
                <CardContent className="text-center p-12">
                  <div className="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Eye className="w-12 h-12 text-gray-400" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-700 mb-2">
                    Preview Your Website
                  </h3>
                  <p className="text-gray-500 max-w-sm mx-auto">
                    Generate a website using the form on the left to see a live preview here.
                  </p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}