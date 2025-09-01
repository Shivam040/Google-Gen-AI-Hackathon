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
    <div className="min-h-screen w-screen relative overflow-hidden bg-gradient-to-b from-slate-950 via-slate-900 to-slate-800 flex flex-col">

      {/* Background Layers */}
      <div className="absolute inset-0 -z-10 opacity-70 blur-3xl animate-pulse bg-gradient-to-b from-sky-900/30 via-transparent to-transparent" />
      <svg
        className="absolute top-[-40px] left-[-60px] w-96 h-96 text-sky-500/30 opacity-40 blur-[70px] -z-10"
        fill="currentColor"
        aria-hidden="true"
      >
        <circle cx="200" cy="200" r="200" />
      </svg>

      <header className="w-full py-6 flex items-center justify-between px-4 md:px-12 z-10 relative">
        <div className="flex items-center gap-2 text-slate-100">
          <Layers3 className="h-6 w-6" />
          <span className="font-bold text-xl select-none">ArtisanMarket</span>
        </div>
        <div className="flex items-center gap-3 text-slate-100">
          <div className="flex items-center border border-white/10 rounded-xl px-3 py-1 bg-white/5 backdrop-blur-md">
            <Languages className="h-4 w-4 mr-2" />
            <select
              value={lang}
              onChange={(e) => setLang(e.target.value)}
              className="bg-transparent py-2 text-sm outline-none cursor-pointer text-slate-100"
            >
              <option value="en">English</option>
              <option value="hi">हिन्दी</option>
              <option value="bn">বাংলা</option>
              <option value="mr">मराठी</option>
              <option value="te">తెలుగు</option>
              <option value="ta">தமிழ்</option>
            </select>
          </div>
          <Button variant="ghost" className="text-slate-100 hover:text-sky-300">Docs</Button>
          <Button variant="ghost" className="text-slate-100 hover:text-sky-300">About</Button>
        </div>
      </header>

      <main className="w-full flex flex-col gap-16 items-center text-center px-4 md:px-12 z-10 relative">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="space-y-8 w-full max-w-4xl"
        >
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-sky-400 to-cyan-300 drop-shadow-[0_6px_20px_rgba(56,189,248,0.25)]">
            A cultural commerce platform for{' '}
            <span className="underline decoration-sky-400 underline-offset-8">Artisans & Buyers</span>
          </h1>

          <p className="text-xl text-slate-300/90 font-medium max-w-prose mx-auto">
            Showcase authentic crafts, tell immersive stories, collaborate across traditions, and sell globally with AI support (descriptions,
            marketing, provenance, and a dialect-aware voice assistant).
          </p>

          <div className="grid sm:grid-cols-2 gap-8">
            <Card className="backdrop-blur-xl bg-white/5 border border-slate-700/60 shadow-xl hover:scale-105 transition-transform duration-300">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-sky-300">
                  <User2 className="h-5 w-5" /> Login as Artisan
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <input
                  className="px-4 py-2 rounded-xl bg-slate-800/80 border border-slate-700 placeholder-slate-400 text-slate-100 focus:ring-2 focus:ring-sky-500/60 transition w-full"
                  placeholder="Email"
                />
                <input
                  type="password"
                  className="px-4 py-2 rounded-xl bg-slate-800/80 border border-slate-700 placeholder-slate-400 text-slate-100 focus:ring-2 focus:ring-sky-500/60 transition w-full"
                  placeholder="Password"
                />
                <Link to="/artisan">
                  <Button className="w-full bg-gradient-to-r from-sky-600 to-cyan-500 text-white font-bold shadow-lg hover:from-sky-500 hover:to-cyan-400 transition-all duration-300">
                    Continue
                  </Button>
                </Link>
              </CardContent>
            </Card>

            <Card className="backdrop-blur-xl bg-white/5 border border-slate-700/60 shadow-xl hover:scale-105 transition-transform duration-300">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-sky-300">
                  <ShoppingBag className="h-5 w-5" /> Login as Buyer
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <input
                  className="px-4 py-2 rounded-xl bg-slate-800/80 border border-slate-700 placeholder-slate-400 text-slate-100 focus:ring-2 focus:ring-sky-500/60 transition w-full"
                  placeholder="Email"
                />
                <input
                  type="password"
                  className="px-4 py-2 rounded-xl bg-slate-800/80 border border-slate-700 placeholder-slate-400 text-slate-100 focus:ring-2 focus:ring-sky-500/60 transition w-full"
                  placeholder="Password"
                />
                <Link to="/buyer">
                  <Button className="w-full bg-gradient-to-r from-sky-600 to-cyan-500 text-white font-bold shadow-lg hover:from-sky-500 hover:to-cyan-400 transition-all duration-300">
                    Continue
                  </Button>
                </Link>
              </CardContent>
            </Card>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="hidden lg:block max-w-4xl w-full"
        >
          <HeroPreview />
        </motion.div>
      </main>

      <footer className="w-full py-8 text-sm text-slate-400 flex flex-col md:flex-row items-center justify-between gap-4 md:gap-0 px-4 md:px-12 z-10 relative">
        <div className="flex items-center gap-2 text-sky-300/80 select-none">
          <ShieldCheck className="h-4 w-4" /> Provenance-first • Fair-trade • Community
        </div>
        <div className="flex items-center gap-6 text-slate-400">
          <a className="hover:text-sky-300 transition-colors" href="#">Terms</a>
          <a className="hover:text-sky-300 transition-colors" href="#">Privacy</a>
          <a className="hover:text-sky-300 transition-colors" href="#">Contact</a>
        </div>
      </footer>

    </div>
  )
}
