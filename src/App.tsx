import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { lazy, Suspense } from 'react'
import Layout from './components/Layout'

const Home = lazy(() => import('./pages/Home'))
const ExercisePage = lazy(() => import('./pages/ExercisePage'))

function PageLoader() {
  return (
    <div className="flex items-center justify-center py-32">
      <div className="flex flex-col items-center gap-4">
        <div className="w-8 h-8 border-2 border-apple-blue border-t-transparent rounded-full animate-spin" />
        <span className="text-sm text-apple-gray-400">Đang tải...</span>
      </div>
    </div>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Suspense fallback={<PageLoader />}><Home /></Suspense>} />
          <Route path="/bai/:slug" element={<Suspense fallback={<PageLoader />}><ExercisePage /></Suspense>} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
