// apps/front/src/App.jsx
import { Routes, Route } from 'react-router-dom'
import Landing from './pages/Landing'
import Artisan from './pages/Artisan'
import Buyer from './pages/Buyer'
import NewItem from "./pages/NewItem";


export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/artisan" element={<Artisan />} />
      <Route path="/buyer" element={<Buyer />} />
      <Route path="/artisan/new" element={<NewItem />} />
    </Routes>
  )
}

