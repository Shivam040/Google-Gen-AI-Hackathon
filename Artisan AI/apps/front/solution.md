# ArtisanMarket — React (JavaScript) + Tailwind — Proper Pages & Components

Below is a complete, ready‑to‑run **Vite + React (JavaScript)** project with **Tailwind CSS**, organized into **pages** and **components**. It implements your Landing page and both **Artisan** and **Buyer** flows, broken into modular components.

---

## 📁 Folder Structure
```
artisan-market/
├─ package.json
├─ vite.config.js
├─ tailwind.config.js
├─ postcss.config.js
├─ index.html
└─ src/
   ├─ index.css
   ├─ main.jsx
   ├─ App.jsx
   ├─ pages/
   │  ├─ Landing.jsx
   │  ├─ Artisan.jsx
   │  └─ Buyer.jsx
   ├─ components/
   │  ├─ HeroPreview.jsx
   │  ├─ ui/
   │  │  ├─ Button.jsx
   │  │  ├─ Card.jsx
   │  │  ├─ Badge.jsx
   │  │  ├─ TopBar.jsx
   │  │  ├─ SectionTitle.jsx
   │  │  └─ Empty.jsx
   │  ├─ artisan/
   │  │  ├─ ItemManagement.jsx
   │  │  ├─ CreateItem.jsx
   │  │  ├─ QuickMarketing.jsx
   │  │  ├─ CollaborationHub.jsx
   │  │  ├─ Insights.jsx
   │  │  └─ UniqueTools.jsx
   │  └─ buyer/
   │     ├─ Explore.jsx
   │     ├─ Interactive.jsx
   │     ├─ Social.jsx
   │     └─ Commerce.jsx
   └─ assets/
      └─ logo.svg  (optional)
```

---

## ▶️ Setup & Run
```bash
# 1) Create the app (Vite + React)
npm create vite@latest artisan-market -- --template react
cd artisan-market

# 2) Install deps
npm i
npm i -D tailwindcss postcss autoprefixer
npm i lucide-react framer-motion recharts react-router-dom

# 3) Initialize Tailwind
npx tailwindcss init -p

# 4) Replace/add the files below (paths must match)

# 5) Run
npm run dev
```

---

## 🔧 Config & HTML

**package.json**
```json
{
  "name": "artisan-market",
  "private": true,
  "version": "0.0.1",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "framer-motion": "^10.18.0",
    "lucide-react": "^0.452.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.26.2",
    "recharts": "^2.12.7"
  },
  "devDependencies": {
    "@types/react": "^18.3.3",
    "@types/react-dom": "^18.3.0",
    "autoprefixer": "^10.4.19",
    "postcss": "^8.4.41",
    "tailwindcss": "^3.4.10",
    "vite": "^5.4.0"
  }
}
```

**vite.config.js**
```js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})
```

**tailwind.config.js**
```js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,jsx}',
  ],
  theme: {
    extend: {
      container: { center: true, padding: '1rem' },
      colors: {
        primary: {
          DEFAULT: '#2563eb', // indigo-600-like
          foreground: '#ffffff'
        }
      }
    },
  },
  plugins: [],
}
```

**postcss.config.js**
```js
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

**index.html**
```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ArtisanMarket</title>
  </head>
  <body class="bg-gradient-to-b from-white to-slate-50">
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

---

## 🧩 Global Entry

**src/index.css**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* App base styles */
:root {
  --radius: 1rem;
}

.card {
  @apply rounded-2xl border bg-white shadow-sm;
}
.card-header { @apply p-4 border-b; }
.card-title { @apply text-lg font-semibold; }
.card-content { @apply p-4; }

.btn { @apply inline-flex items-center justify-center rounded-2xl px-4 py-2 text-sm font-medium transition; }
.btn-primary { @apply bg-primary text-white hover:opacity-90; }
.btn-secondary { @apply bg-slate-100 text-slate-900 hover:bg-slate-200; }
.btn-outline { @apply border border-slate-200 hover:bg-slate-50; }
.btn-destructive { @apply bg-red-600 text-white hover:bg-red-700; }

.badge { @apply inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-medium; }
.badge-soft { @apply bg-slate-100 border-transparent; }
.badge-outline { @apply border-slate-200; }

.input { @apply w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-primary/30; }
.label { @apply text-sm font-medium text-slate-700; }
.textarea { @apply input min-h-[120px]; }
.hr { @apply my-4 border-slate-200; }
```

**src/main.jsx**
```jsx
import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
import './index.css'

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
)
```

**src/App.jsx**
```jsx
import { Routes, Route } from 'react-router-dom'
import Landing from './pages/Landing'
import Artisan from './pages/Artisan'
import Buyer from './pages/Buyer'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/artisan" element={<Artisan />} />
      <Route path="/buyer" element={<Buyer />} />
    </Routes>
  )
}
```

---

## 🖼️ Core UI Primitives

**src/components/ui/Button.jsx**
```jsx
export default function Button({ variant = 'primary', size = 'md', className = '', children, ...props }) {
  const base = 'btn'
  const variants = {
    primary: 'btn-primary',
    secondary: 'btn-secondary',
    outline: 'btn-outline',
    destructive: 'btn-destructive',
    ghost: 'hover:bg-slate-100',
  }
  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2',
    lg: 'px-5 py-2.5 text-base',
  }
  return (
    <button className={`${base} ${variants[variant] || ''} ${sizes[size] || ''} ${className}`} {...props}>
      {children}
    </button>
  )
}
```

**src/components/ui/Card.jsx**
```jsx
export function Card({ className = '', children }) {
  return <div className={`card ${className}`}>{children}</div>
}
export function CardHeader({ className = '', children }) {
  return <div className={`card-header ${className}`}>{children}</div>
}
export function CardTitle({ className = '', children }) {
  return <div className={`card-title ${className}`}>{children}</div>
}
export function CardContent({ className = '', children }) {
  return <div className={`card-content ${className}`}>{children}</div>
}
```

**src/components/ui/Badge.jsx**
```jsx
export default function Badge({ variant = 'outline', className = '', children }) {
  const variants = {
    soft: 'badge badge-soft',
    outline: 'badge badge-outline',
  }
  return <span className={`${variants[variant]} ${className}`}>{children}</span>
}
```

**src/components/ui/TopBar.jsx**
```jsx
import { Layers3, Bell, Globe2 } from 'lucide-react'
import Badge from './Badge'
import Button from './Button'

export default function TopBar({ role }) {
  return (
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-2">
        <Layers3 className="h-5 w-5" />
        <span className="font-semibold">ArtisanMarket</span>
        <Badge variant="soft" className="ml-2">{role}</Badge>
      </div>
      <div className="flex items-center gap-3">
        <Button variant="outline" size="sm"><Bell className="h-4 w-4 mr-1" /> Alerts</Button>
        <Button variant="outline" size="sm"><Globe2 className="h-4 w-4 mr-1" /> Multilingual</Button>
      </div>
    </div>
  )
}
```

**src/components/ui/SectionTitle.jsx**
```jsx
export default function SectionTitle({ icon: Icon, title, right }) {
  return (
    <div className="flex items-center justify-between mb-3">
      <div className="flex items-center gap-2">
        {Icon && <Icon className="h-5 w-5" />}
        <h3 className="text-lg font-semibold">{title}</h3>
      </div>
      <div>{right}</div>
    </div>
  )
}
```

**src/components/ui/Empty.jsx**
```jsx
import { Card, CardContent } from './Card'

export default function Empty({ icon: Icon, title, subtitle, cta }) {
  return (
    <Card className="border-dashed">
      <CardContent className="py-10 flex flex-col items-center gap-3 text-center">
        {Icon && <Icon className="h-8 w-8" />}
        <div className="text-xl font-semibold">{title}</div>
        <div className="text-slate-500 max-w-xl">{subtitle}</div>
        {cta}
      </CardContent>
    </Card>
  )
}
```

---

## 🏠 Landing Page

**src/components/HeroPreview.jsx**
```jsx
import { Card, CardContent } from './ui/Card'
import SectionTitle from './ui/SectionTitle'
import { Handshake, LineChart } from 'lucide-react'
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip } from 'recharts'

export default function HeroPreview() {
  const data = [
    { name: 'Jan', sales: 2400 },
    { name: 'Feb', sales: 1398 },
    { name: 'Mar', sales: 2800 },
    { name: 'Apr', sales: 3908 },
  ]
  return (
    <Card className="p-6">
      <div className="grid grid-cols-2 gap-6">
        <div>
          <SectionTitle icon={LineChart} title="Trending Sales" />
          <div className="h-40">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data}>
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="sales" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
        <div>
          <SectionTitle icon={Handshake} title="Collaboration Matches" />
          <div className="space-y-3">
            {['Textile × Pottery', 'Metalwork × Wood', 'Embroidery × Jewelry'].map((s) => (
              <div key={s} className="flex items-center justify-between bg-slate-100 rounded-xl px-3 py-2">
                <span>{s}</span>
                <span className="badge">View</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </Card>
  )
}
```

**src/pages/Landing.jsx**
```jsx
import { useState } from 'react'
import { motion } from 'framer-motion'
import { Languages, Layers3, ShoppingBag, User2, ShieldCheck } from 'lucide-react'
import { Link } from 'react-router-dom'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card'
import Button from '../components/ui/Button'
import HeroPreview from '../components/HeroPreview'

export default function Landing() {
  const [lang, setLang] = useState('en')

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-slate-50 flex flex-col">
      <header className="container py-6 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Layers3 className="h-6 w-6" />
          <span className="font-bold text-xl">ArtisanMarket</span>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex items-center border rounded-xl px-2">
            <Languages className="h-4 w-4 mr-2" />
            <select value={lang} onChange={(e) => setLang(e.target.value)} className="bg-transparent py-2 text-sm outline-none">
              <option value="en">English</option>
              <option value="hi">हिन्दी</option>
              <option value="bn">বাংলা</option>
              <option value="mr">मराठी</option>
              <option value="te">తెలుగు</option>
              <option value="ta">தமிழ்</option>
            </select>
          </div>
          <Button variant="ghost">Docs</Button>
          <Button variant="ghost">About</Button>
        </div>
      </header>

      <main className="container flex-1 grid lg:grid-cols-2 gap-10 items-center">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight leading-tight">
            A cultural commerce platform for <span className="underline underline-offset-8 decoration-primary">Artisans</span> & Buyers
          </h1>
          <p className="mt-4 text-lg text-slate-600 max-w-prose">
            Showcase authentic crafts, tell immersive stories, collaborate across traditions, and sell globally with AI support (descriptions, marketing, provenance, and a dialect‑aware voice assistant).
          </p>
          <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2"><User2 className="h-5 w-5" />Login as Artisan</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <input className="input" placeholder="Email" />
                <input className="input" placeholder="Password" type="password" />
                <Link to="/artisan"><Button className="w-full">Continue</Button></Link>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2"><ShoppingBag className="h-5 w-5" />Login as Buyer</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <input className="input" placeholder="Email" />
                <input className="input" placeholder="Password" type="password" />
                <Link to="/buyer"><Button className="w-full">Continue</Button></Link>
              </CardContent>
            </Card>
          </div>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }} className="hidden lg:block">
          <HeroPreview />
        </motion.div>
      </main>

      <footer className="container py-8 text-sm text-slate-600 flex items-center justify-between">
        <div className="flex items-center gap-2"><ShieldCheck className="h-4 w-4" /> Provenance‑first • Fair‑trade • Community</div>
        <div className="flex items-center gap-4">
          <a className="hover:underline" href="#">Terms</a>
          <a className="hover:underline" href="#">Privacy</a>
          <a className="hover:underline" href="#">Contact</a>
        </div>
      </footer>
    </div>
  )
}
```

---

## 🛠️ Artisan Area

**src/pages/Artisan.jsx**
```jsx
import TopBar from '../components/ui/TopBar'
import SectionTitle from '../components/ui/SectionTitle'
import { Store, Handshake, LineChart as LineIcon, Sparkles } from 'lucide-react'
import ItemManagement from '../components/artisan/ItemManagement'
import CollaborationHub from '../components/artisan/CollaborationHub'
import Insights from '../components/artisan/Insights'
import UniqueTools from '../components/artisan/UniqueTools'
import { useState } from 'react'

export default function Artisan() {
  const [tab, setTab] = useState('items')
  const tabs = [
    { id: 'items', title: 'Item Management', icon: Store },
    { id: 'collab', title: 'Collaboration', icon: Handshake },
    { id: 'insights', title: 'Insights', icon: LineIcon },
    { id: 'unique', title: 'Unique', icon: Sparkles },
  ]

  return (
    <div className="container py-6 space-y-6">
      <TopBar role="Artisan" />

      <div className="grid grid-cols-4 gap-2">
        {tabs.map(t => (
          <button key={t.id} onClick={() => setTab(t.id)}
            className={`btn ${tab===t.id? 'btn-secondary' : 'btn-outline'} flex items-center justify-center gap-2`}>
            <t.icon className="h-4 w-4" /> {t.title}
          </button>
        ))}
      </div>

      <div>
        {tab === 'items' && <ItemManagement />}
        {tab === 'collab' && <CollaborationHub />}
        {tab === 'insights' && <Insights />}
        {tab === 'unique' && <UniqueTools />}
      </div>
    </div>
  )
}
```

**src/components/artisan/ItemManagement.jsx**
```jsx
import { useState } from 'react'
import Button from '../ui/Button'
import SectionTitle from '../ui/SectionTitle'
import Empty from '../ui/Empty'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card'
import Badge from '../ui/Badge'
import { Plus, Megaphone, Hash, Store } from 'lucide-react'
import QuickMarketing from './QuickMarketing'
import CreateItem from './CreateItem'

export default function ItemManagement() {
  const [items, setItems] = useState([])
  const [creating, setCreating] = useState(false)

  return (
    <div className="grid lg:grid-cols-3 gap-6">
      <div className="lg:col-span-2 space-y-4">
        <SectionTitle icon={Store} title="Your Store Items" right={<Button onClick={() => setCreating(true)}><Plus className="h-4 w-4 mr-1" />Add Item</Button>} />
        {items.length === 0 ? (
          <Empty icon={Store} title="No products yet" subtitle="Add your first craft item. Upload images, choose theme & type, and let AI help with descriptions, marketing, and storytelling." cta={<Button onClick={() => setCreating(true)}><Plus className="h-4 w-4 mr-1" />Add Product</Button>} />
        ) : (
          <div className="grid md:grid-cols-2 gap-4">
            {items.map((it, idx) => (
              <Card key={idx}>
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <span>{it.name}</span>
                    <Badge>{it.theme}</Badge>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  <img src={it.preview} alt="preview" className="w-full h-40 object-cover rounded-xl" />
                  <div className="text-sm text-slate-500">{it.type}</div>
                  <div className="flex gap-2">
                    <Button size="sm" variant="secondary">Edit</Button>
                    <Button size="sm" variant="destructive" onClick={() => setItems(items.filter((_, i) => i !== idx))}>Remove</Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>

      <div className="space-y-4">
        <SectionTitle icon={Megaphone} title="Quick Marketing" />
        <QuickMarketing />
        <hr className="hr" />
        <SectionTitle icon={Hash} title="Trending Hashtags" />
        <div className="flex flex-wrap gap-2">
          {["#HandloomLove", "#VocalForLocal", "#FestiveEdit", "#SustainableCraft"].map((h) => (
            <Badge key={h} variant="outline">{h}</Badge>
          ))}
        </div>
      </div>

      {creating && (
        <CreateItem onClose={() => setCreating(false)} onCreate={(it) => setItems([it, ...items])} />
      )}
    </div>
  )
}
```

**src/components/artisan/CreateItem.jsx**
```jsx
import { useRef, useState } from 'react'
import Button from '../ui/Button'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card'
import { Plus, Upload, Camera, Wand2, Sparkles, Loader2 } from 'lucide-react'

const THEMES = ['Traditional', 'Modern', 'Festival', 'Minimal', 'Heritage', 'Fusion']
const PRODUCT_TYPES = {
  Art: ['Drawing', 'Painting', 'Calligraphy'],
  'Craft Objects': ['Pottery', 'Woodwork', 'Metalwork'],
  Textiles: ['Clothing', 'Weaving', 'Embroidery'],
  Accessories: ['Jewelry', 'Bags', 'Home Decor'],
}
const TONES = ['Professional','Friendly','Playful','Narrative','Persuasive','Empathetic','Luxury','Minimal','Gen Z / Casual']
const LANGS = [ ['en','English'], ['hi','हिन्दी'], ['bn','বাংলা'], ['mr','मराठी'], ['te','తెలుగు'], ['ta','தமிழ்'] ]

export default function CreateItem({ onClose, onCreate }) {
  const [name, setName] = useState('')
  const [theme, setTheme] = useState(THEMES[0])
  const [ptype, setPtype] = useState('Drawing')
  const [preview, setPreview] = useState('')
  const [tone, setTone] = useState(TONES[0])
  const [lang, setLang] = useState('en')
  const [desc, setDesc] = useState('')
  const [story, setStory] = useState('')
  const [post, setPost] = useState('')
  const [busy, setBusy] = useState(false)

  const imgRef = useRef(null)

  const handleFile = (e) => {
    const f = e.target.files?.[0]
    if (!f) return
    const url = URL.createObjectURL(f)
    setPreview(url)
  }

  const fakeGen = async (setter, kind) => {
    setBusy(true)
    await new Promise((r) => setTimeout(r, 800))
    const base = kind === 'desc'
      ? `
${name || 'Handcrafted Item'} — a ${ptype.toLowerCase()} in ${theme.toLowerCase()} theme. Crafted with a ${tone.toLowerCase()} tone.`
      : kind === 'story'
      ? `
From the artisan's hut, this piece carries memories of monsoon songs. Provenance: Verified. Language: ${lang}.`
      : `
Shine this season with ${theme} ${ptype}! #Handmade #Provenance #SupportLocal`
    setter(base)
    setBusy(false)
  }

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-end md:items-center justify-center p-4 z-50">
      <div className="bg-white w-full md:w-[950px] rounded-2xl overflow-hidden shadow-xl">
        <div className="p-4 border-b flex items-center justify-between">
          <div className="flex items-center gap-2"><Plus className="h-5 w-5" /><span className="font-semibold">Add New Item</span></div>
          <Button variant="ghost" onClick={onClose}>Close</Button>
        </div>
        <div className="p-6 grid md:grid-cols-5 gap-6">
          <div className="md:col-span-2 space-y-4">
            <label className="label">Product Image</label>
            <div className="flex items-center gap-3">
              <input type="file" accept="image/*" ref={imgRef} onChange={handleFile} className="hidden" />
              <Button variant="outline" onClick={() => imgRef.current?.click()}><Upload className="h-4 w-4 mr-1" />Upload</Button>
              <span className="text-sm text-slate-500">{preview ? 'Selected' : 'No file chosen'}</span>
            </div>
            {preview ? (
              <img src={preview} alt="preview" className="rounded-xl w-full h-56 object-cover" />
            ) : (
              <div className="rounded-xl border border-dashed h-56 grid place-content-center text-slate-500">
                <Camera className="h-8 w-8 mx-auto mb-2" /> Preview
              </div>
            )}

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="label">Theme</label>
                <select value={theme} onChange={(e)=>setTheme(e.target.value)} className="input">
                  {THEMES.map(t => <option key={t} value={t}>{t}</option>)}
                </select>
              </div>
              <div>
                <label className="label">Product Type</label>
                <select value={ptype} onChange={(e)=>setPtype(e.target.value)} className="input">
                  {Object.entries(PRODUCT_TYPES).map(([grp, items]) => (
                    <optgroup key={grp} label={grp}>
                      {items.map(i => <option key={i} value={i}>{i}</option>)}
                    </optgroup>
                  ))}
                </select>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="label">Style/Tone</label>
                <select value={tone} onChange={(e)=>setTone(e.target.value)} className="input">
                  {TONES.map(t => <option key={t} value={t}>{t}</option>)}
                </select>
              </div>
              <div>
                <label className="label">Language</label>
                <select value={lang} onChange={(e)=>setLang(e.target.value)} className="input">
                  {LANGS.map(([code,name]) => <option key={code} value={code}>{name}</option>)}
                </select>
              </div>
            </div>
          </div>

          <div className="md:col-span-3 space-y-6">
            <div className="space-y-2">
              <label className="label">Product Name</label>
              <input className="input" value={name} onChange={(e)=>setName(e.target.value)} placeholder="e.g., Channapatna Lacquered Pottery Vase" />
            </div>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2"><Wand2 className="h-5 w-5" /> AI Description</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <textarea rows={4} className="textarea" value={desc} onChange={(e)=>setDesc(e.target.value)} placeholder="Generate or write your own product description..." />
                <Button onClick={() => fakeGen(setDesc, 'desc')} disabled={busy}>{busy ? <Loader2 className="h-4 w-4 mr-2 animate-spin" /> : <Wand2 className="h-4 w-4 mr-2" />}Generate Description</Button>
              </CardContent>
            </Card>

            <div className="grid md:grid-cols-2 gap-4">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2"><Sparkles className="h-5 w-5" /> Social Post</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <textarea rows={4} className="textarea" value={post} onChange={(e)=>setPost(e.target.value)} placeholder="Generate catchy posts & taglines..." />
                  <Button onClick={() => fakeGen(setPost, 'post')} disabled={busy}>{busy ? <Loader2 className="h-4 w-4 mr-2 animate-spin" /> : <Sparkles className="h-4 w-4 mr-2" />}Generate Marketing</Button>
                </CardContent>
              </Card>
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2"><Wand2 className="h-5 w-5" /> Storytelling</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <textarea rows={4} className="textarea" value={story} onChange={(e)=>setStory(e.target.value)} placeholder="Heritage, provenance, artisan journey..." />
                  <Button onClick={() => fakeGen(setStory, 'story')} disabled={busy}>{busy ? <Loader2 className="h-4 w-4 mr-2 animate-spin" /> : <Wand2 className="h-4 w-4 mr-2" />}Generate Story</Button>
                </CardContent>
              </Card>
            </div>

            <div className="flex items-center justify-end gap-3">
              <Button variant="ghost" onClick={onClose}>Cancel</Button>
              <Button onClick={() => { onCreate({ name: name||'Untitled', theme, type: ptype, preview: preview || 'https://picsum.photos/640/360' }); onClose(); }}>Save Item</Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
```

**src/components/artisan/QuickMarketing.jsx**
```jsx
import { useState } from 'react'
import Button from '../ui/Button'

const TONES = ['Professional','Friendly','Playful','Narrative','Persuasive','Empathetic','Luxury','Minimal','Gen Z / Casual']

export default function QuickMarketing() {
  const [tone, setTone] = useState('Professional')
  const [hashtags, setHashtags] = useState('#Handmade #Local #Craft')
  const [copy, setCopy] = useState('')

  const gen = async () => {
    setCopy('Generating...')
    await new Promise((r) => setTimeout(r, 500))
    setCopy(`Elevate your space with artisan‑made pieces. (${tone})
${hashtags}`)
  }

  return (
    <div className="card">
      <div className="card-content space-y-3">
        <select value={tone} onChange={(e)=>setTone(e.target.value)} className="input">
          {TONES.map(t => <option key={t} value={t}>{t}</option>)}
        </select>
        <input className="input" value={hashtags} onChange={(e)=>setHashtags(e.target.value)} />
        <Button onClick={gen}>Generate</Button>
        <textarea rows={4} className="textarea" value={copy} onChange={(e)=>setCopy(e.target.value)} />
      </div>
    </div>
  )
}
```

**src/components/artisan/CollaborationHub.jsx**
```jsx
import SectionTitle from '../ui/SectionTitle'
import Button from '../ui/Button'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card'
import Badge from '../ui/Badge'
import { Filter, Handshake, Sparkles } from 'lucide-react'

export default function CollaborationHub() {
  const artisans = [
    { name: 'Meera (Textiles)', themes: ['Traditional','Heritage'], portfolio: 24 },
    { name: 'Arun (Pottery)', themes: ['Modern','Fusion'], portfolio: 18 },
    { name: 'Lata (Jewelry)', themes: ['Festival','Luxury'], portfolio: 31 },
  ]
  return (
    <div className="grid lg:grid-cols-3 gap-6">
      <div className="lg:col-span-2 space-y-4">
        <SectionTitle title="Browse Artisans" right={<Button variant="outline"><Filter className="h-4 w-4 mr-1" />Filters</Button>} />
        <div className="grid md:grid-cols-2 gap-4">
          {artisans.map((a) => (
            <Card key={a.name}>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span>{a.name}</span>
                  <Badge variant="soft">{a.portfolio} items</Badge>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="flex gap-2 flex-wrap">
                  {a.themes.map((t) => <Badge key={t}>{t}</Badge>)}
                </div>
                <div className="flex items-center justify-between pt-2">
                  <Button size="sm" variant="secondary">View Portfolio</Button>
                  <Button size="sm"><Handshake className="h-4 w-4 mr-1" />Request Collab</Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
      <div className="space-y-4">
        <SectionTitle icon={Sparkles} title="AI Fusion Ideas" />
        <Card>
          <CardContent className="space-y-2 text-sm text-slate-600">
            <div className="font-medium text-slate-800">Suggested pairings</div>
            <ul className="list-disc pl-5 space-y-1">
              <li>Block‑print textiles with terracotta motif buttons</li>
              <li>Carved wooden frames with inlaid metal filigree</li>
              <li>Minimal pottery with embroidered sleeve wraps</li>
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
```

**src/components/artisan/Insights.jsx**
```jsx
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card'
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, Bar, BarChart } from 'recharts'

export default function Insights() {
  const sales = [
    { month: 'May', value: 120 },
    { month: 'Jun', value: 180 },
    { month: 'Jul', value: 260 },
    { month: 'Aug', value: 220 },
    { month: 'Sep', value: 310 },
  ]
  const feedback = [
    { day: 'Mon', score: 4.1 },
    { day: 'Tue', score: 4.4 },
    { day: 'Wed', score: 4.6 },
    { day: 'Thu', score: 4.3 },
    { day: 'Fri', score: 4.7 },
  ]

  return (
    <div className="grid lg:grid-cols-3 gap-6">
      <Card className="lg:col-span-2">
        <CardHeader>
          <CardTitle>Sales Trends</CardTitle>
        </CardHeader>
        <CardContent className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={sales}>
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="value" />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Customer Feedback (avg)</CardTitle>
        </CardHeader>
        <CardContent className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={feedback}>
              <XAxis dataKey="day" />
              <YAxis domain={[0, 5]} />
              <Tooltip />
              <Bar dataKey="score" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      <Card className="lg:col-span-3">
        <CardHeader>
          <CardTitle>Product Performance</CardTitle>
        </CardHeader>
        <CardContent className="grid md:grid-cols-3 gap-4">
          {['Pottery Vase', 'Embroidered Stole', 'Brass Anklet'].map((p) => (
            <div key={p} className="rounded-xl border p-4 space-y-2">
              <div className="font-medium">{p}</div>
              <div className="text-sm text-slate-500">CTR ↑ 12% • Returns ↓ 3% • Sentiment 4.6/5</div>
              <button className="btn btn-secondary">Boost</button>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  )
}
```

**src/components/artisan/UniqueTools.jsx**
```jsx
import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card'
import Button from '../ui/Button'
import { Mic, MicOff, Bell } from 'lucide-react'

export default function UniqueTools() {
  const [listening, setListening] = useState(false)
  return (
    <div className="grid lg:grid-cols-2 gap-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2"><Mic className="h-5 w-5" /> Dialect‑aware Voice Narrator</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="text-sm text-slate-600">Record story snippets in your dialect; AI aligns pronunciation and prosody to your region and generates multilingual captions.</div>
          <div className="flex items-center gap-3">
            <Button onClick={() => setListening((v) => !v)} variant={listening ? 'destructive' : 'primary'}>
              {listening ? <MicOff className="h-4 w-4 mr-1" /> : <Mic className="h-4 w-4 mr-1" />} {listening ? 'Stop' : 'Record'}
            </Button>
            <Button variant="outline">Preview</Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2"><Bell className="h-5 w-5" /> Trending Alerts</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex items-center justify-between bg-slate-100 rounded-xl px-3 py-2">
            <span>"Festival decor" searches up 35% in North India</span>
            <span className="badge badge-soft">Now</span>
          </div>
          <div className="flex items-center justify-between bg-slate-100 rounded-xl px-3 py-2">
            <span>High demand: Block‑print dupattas</span>
            <span className="badge badge-soft">Today</span>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
```

---

## 🛍️ Buyer Area

**src/pages/Buyer.jsx**
```jsx
import TopBar from '../components/ui/TopBar'
import { useState, useMemo } from 'react'
import Button from '../components/ui/Button'
import { Search, PlayCircle, Compass, Share2, Globe2, ShieldCheck, MapPin, Filter } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card'
import Badge from '../components/ui/Badge'
import Explore from '../components/buyer/Explore'
import Interactive from '../components/buyer/Interactive'
import Social from '../components/buyer/Social'
import Commerce from '../components/buyer/Commerce'

export default function Buyer() {
  const [tab, setTab] = useState('explore')
  const tabs = [
    { id: 'explore', title: 'Explore', icon: Search },
    { id: 'interactive', title: 'Interactive', icon: PlayCircle },
    { id: 'social', title: 'Social', icon: Share2 },
    { id: 'commerce', title: 'Commerce', icon: Globe2 },
  ]

  return (
    <div className="container py-6 space-y-6">
      <TopBar role="Buyer" />

      <div className="grid grid-cols-4 gap-2">
        {tabs.map(t => (
          <button key={t.id} onClick={() => setTab(t.id)}
            className={`btn ${tab===t.id? 'btn-secondary' : 'btn-outline'} flex items-center justify-center gap-2`}>
            <t.icon className="h-4 w-4" /> {t.title}
          </button>
        ))}
      </div>

      {tab === 'explore' && <Explore />}
      {tab === 'interactive' && <Interactive />}
      {tab === 'social' && <Social />}
      {tab === 'commerce' && <Commerce />}
    </div>
  )
}
```

**src/components/buyer/Explore.jsx**
```jsx
import { useMemo, useState } from 'react'
import { Card, CardContent } from '../ui/Card'
import Button from '../ui/Button'
import Badge from '../ui/Badge'
import { Filter, ShieldCheck } from 'lucide-react'

export default function Explore() {
  const [query, setQuery] = useState('')
  const recs = useMemo(() => ([
    { title: 'Terracotta Tea Set', artisan: 'Arun', theme: 'Modern', price: 1499, img: 'https://picsum.photos/id/1060/600/400' },
    { title: 'Embroidered Stole', artisan: 'Meera', theme: 'Heritage', price: 1299, img: 'https://picsum.photos/id/1025/600/400' },
    { title: 'Brass Anklet', artisan: 'Lata', theme: 'Festival', price: 999, img: 'https://picsum.photos/id/1080/600/400' },
  ]), [])

  const filtered = recs.filter((r) => r.title.toLowerCase().includes(query.toLowerCase()) || r.theme.toLowerCase().includes(query.toLowerCase()))

  return (
    <Card>
      <CardContent className="p-4">
        <div className="flex items-center gap-3 mb-4">
          <input className="input" placeholder="Search by theme, artisan, culture, festival" value={query} onChange={(e)=>setQuery(e.target.value)} />
          <Button variant="secondary"><Filter className="h-4 w-4 mr-1" />Filters</Button>
        </div>
        <div className="grid md:grid-cols-3 gap-4">
          {filtered.map((r) => (
            <div key={r.title} className="card overflow-hidden">
              <img src={r.img} className="w-full h-40 object-cover" />
              <div className="card-content space-y-2">
                <div className="flex items-center justify-between">
                  <div className="font-medium">{r.title}</div>
                  <Badge>{r.theme}</Badge>
                </div>
                <div className="text-sm text-slate-500">by {r.artisan}</div>
                <div className="text-sm font-semibold">₹ {r.price}</div>
                <div className="bg-slate-100 rounded-xl p-3 text-sm">
                  <div className="font-medium flex items-center gap-2"><ShieldCheck className="h-4 w-4" /> Provenance</div>
                  <div className="text-slate-600">Verified journey from artisan to you. View story & certificates.</div>
                </div>
                <div className="flex gap-2 pt-1">
                  <Button size="sm">Add to Cart</Button>
                  <Button size="sm" variant="secondary">View Story</Button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
```

**src/components/buyer/Interactive.jsx**
```jsx
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card'
import Button from '../ui/Button'

export default function Interactive() {
  return (
    <div className="grid lg:grid-cols-2 gap-6">
      <Card>
        <CardHeader>
          <CardTitle>Video Shopping</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="rounded-xl border h-48 grid place-content-center text-slate-500">Stream Placeholder</div>
          <div className="flex gap-2">
            <Button variant="secondary">Schedule Demo</Button>
            <Button>Join Live</Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>AR Preview</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="rounded-xl border h-48 grid place-content-center text-slate-500">360° / AR Placeholder</div>
          <Button variant="secondary">Open AR Viewer</Button>
        </CardContent>
      </Card>

      <Card className="lg:col-span-2">
        <CardHeader>
          <CardTitle>Co‑creation (AI‑guided)</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <textarea className="textarea" rows={3} placeholder="Describe your custom idea (colors, motifs, size)..." />
          <div className="flex gap-2">
            <Button variant="secondary">Suggest Designs</Button>
            <Button>Message Artisan</Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
```

**src/components/buyer/Social.jsx**
```jsx
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card'
import Button from '../ui/Button'
import { MapPin } from 'lucide-react'

export default function Social() {
  return (
    <div className="grid lg:grid-cols-2 gap-6">
      <Card>
        <CardHeader>
          <CardTitle>Festival Bundles</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {[
            { name: 'Diwali Home Set', items: 5 },
            { name: 'Eid Gift Box', items: 3 },
            { name: 'Pongal Kitchen Kit', items: 4 },
          ].map((b) => (
            <div key={b.name} className="flex items-center justify-between bg-slate-100 rounded-xl px-3 py-2">
              <span>{b.name}</span>
              <Button size="sm" variant="secondary">View ({b.items})</Button>
            </div>
          ))}
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Community Events & Workshops</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex items-center justify-between bg-slate-100 rounded-xl px-3 py-2">
            <span>Handloom Market • Dehradun</span>
            <Button size="sm" variant="secondary"><MapPin className="h-4 w-4 mr-1" />Details</Button>
          </div>
          <div className="flex items-center justify-between bg-slate-100 rounded-xl px-3 py-2">
            <span>Pottery Workshop • Rishikesh</span>
            <Button size="sm" variant="secondary"><MapPin className="h-4 w-4 mr-1" />Details</Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
```

**src/components/buyer/Commerce.jsx**
```jsx
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card'

export default function Commerce() {
  return (
    <div className="grid lg:grid-cols-2 gap-6">
      <Card>
        <CardHeader>
          <CardTitle>Multilingual Interface</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <select defaultValue="en" className="input">
            <option value="en">English</option>
            <option value="hi">हिन्दी</option>
            <option value="bn">বাংলা</option>
            <option value="mr">मराठी</option>
            <option value="te">తెలుగు</option>
            <option value="ta">தமிழ்</option>
          </select>
          <div className="text-sm text-slate-600">UI strings and voiceover adapt to your language preference.</div>
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Follow & Support</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex items-center justify-between bg-slate-100 rounded-xl px-3 py-2">
            <span>Follow artisans for updates</span>
            <button className="btn btn-secondary">Follow</button>
          </div>
          <div className="flex items-center justify-between bg-slate-100 rounded-xl px-3 py-2">
            <span>Join community innovation lab</span>
            <button className="btn btn-secondary">Join</button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
```

---

### 🔌 Next Steps (wiring AI & APIs)
- Replace the `fakeGen` stubs in `CreateItem.jsx` and `QuickMarketing.jsx` with real API calls:
  ```js
  const res = await fetch('/api/generate/description', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name, theme, ptype, tone, lang }) })
  const data = await res.json()
  setDesc(data.text)
  ```
- Add auth (e.g., Firebase/Auth0) to the Landing login cards.
- Persist items to your backend or Firestore instead of local state.
- Add AR/video integrations and provenance verification UI when endpoints are ready.

> This scaffold is **100% JavaScript + Tailwind**, with pages and components separated so you can evolve each area independently.
