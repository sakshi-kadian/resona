'use client';

import { useRouter } from 'next/navigation';
import {
  BarChart3,
  Zap,
  Search,
  Music,
  Database,
  Cpu,
  Layers,
  Lock,
  Radio,
  Share2,
  BrainCircuit,
  Music2,
  Compass
} from 'lucide-react';

export default function Home() {
  const router = useRouter();

  const handleConnect = () => {
    window.location.href = 'http://localhost:8000/auth/login';
  };

  const currentYear = new Date().getFullYear();

  return (
    <div className="min-h-screen bg-[#050505] text-slate-300 selection:bg-purple-500 selection:text-white relative overflow-hidden font-sans">

      {/* BACKGROUND */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        <div className="absolute top-[-50%] left-[-20%] w-[100%] h-[100%] bg-purple-900/30 rounded-full blur-[300px]"></div>
        <div className="absolute bottom-[-50%] right-[-20%] w-[100%] h-[100%] bg-purple-900/30 rounded-full blur-[300px]"></div>
      </div>

      {/* HEADER */}
      <nav className="fixed w-full z-50 bg-transparent backdrop-blur-lg border-b border-white/5">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center">
            <h1 className="text-3xl font-extrabold tracking-tighter uppercase font-[var(--font-syne)] bg-gradient-to-br from-white via-white to-white/60 bg-clip-text text-transparent hover:scale-105 transition-transform cursor-pointer">
              Resona
            </h1>
          </div>
          <div className="flex gap-8 text-sm font-medium text-slate-400">
            <a href="#" className="hover:text-white transition-colors cursor-pointer">Home</a>
            <a href="#landscape" className="hover:text-white transition-colors cursor-pointer">Problem</a>
            <a href="#methodology" className="hover:text-white transition-colors cursor-pointer">Methodology</a>
            <a href="#tech" className="hover:text-white transition-colors cursor-pointer">Technology</a>
            <a href="#features" className="hover:text-white transition-colors cursor-pointer">Capabilities</a>
          </div>
        </div>
      </nav>

      {/* SECTION 1: HERO SECTION */}
      <section className="pt-36 pb-32 px-6 relative z-10 min-h-screen flex flex-col justify-center items-center text-center">
        <div className="max-w-4xl mx-auto">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-3 py-1 mb-8 rounded-full border border-purple-500/20 bg-purple-500/10 backdrop-blur-md cursor-default">
            <Music2 size={14} className="text-purple-400" />
            <span className="text-purple-200 text-[11px] font-bold tracking-[0.2em] uppercase">Go deeper than your Spotify Wrapped</span>
            <Music2 size={14} className="text-purple-400" />
          </div>

          {/* Main Title */}
          <h1 className="text-6xl md:text-8xl font-bold mb-8 tracking-tighter leading-[0.95] text-white drop-shadow-2xl">
            Visualize Your <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-b from-white to-purple-300">Resonance</span>
          </h1>

          <p className="text-lg md:text-xl text-slate-400 mb-10 max-w-2xl mx-auto leading-relaxed">
            Resona is a <strong>music intelligence platform</strong> that maps the hidden patterns in your listening habits, revealing your comprehensive resonance profile.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-5">
            <button
              onClick={handleConnect}
              className="px-10 py-4 bg-white text-[#050505] rounded-full font-bold text-lg transition-all hover:scale-105 shadow-[0_0_30px_-5px_rgba(255,255,255,0.3)] w-full sm:w-auto flex items-center justify-center gap-2 cursor-pointer"
            >
              <Music size={24} />
              Connect with Spotify
            </button>
          </div>
        </div>
      </section>

      {/* SECTION 2: THE LANDSCAPE (THE PROBLEM) */}
      <section id="landscape" className="py-24 px-6 relative z-10">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <div className="text-purple-400 font-bold mb-2 tracking-widest text-xs uppercase">The Landscape</div>
            <h2 className="text-3xl md:text-5xl font-bold tracking-tight mb-4 text-white">Escaping the Algorithm Bubble</h2>
            <p className="text-lg text-slate-400 max-w-2xl mx-auto">Modern streaming services prioritize engagement over discovery, trapping you in a loop of familiarity.</p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <ProblemCard
              icon={<Radio size={24} />}
              title="The Echo Chamber"
              desc="Collaborative filtering algorithms reinforce what you already know, narrowing your musical horizon."
            />
            <ProblemCard
              icon={<BrainCircuit size={24} />}
              title="Black Box Logic"
              desc="Recommendations are delivered without context. You never learn *why* a song was chosen for you."
            />
            <ProblemCard
              icon={<Lock size={24} />}
              title="Data Opacity"
              desc="Your listening history is a goldmine of psychographic data, but it's locked away behind simple 'Top 10' lists."
            />
          </div>
        </div>
      </section>

      {/* SECTION 3: THE METHODOLOGY (SOLUTION) */}
      <section id="methodology" className="py-32 px-6 relative z-10">
        <div className="max-w-6xl mx-auto grid md:grid-cols-2 gap-16 items-center">
          <div>
            <div className="text-purple-400 font-bold mb-2 tracking-widest text-xs uppercase">The Methodology</div>
            <h2 className="text-4xl font-bold mb-6 tracking-tight text-white">
              Data-Driven Clarity
            </h2>
            <div className="space-y-6 text-lg text-slate-400 leading-relaxed">
              <p>
                Resona acts as a transparent layer on top of your music data. It doesn't just count plays; it analyzes specific <strong>meta-attributes</strong> like <strong>Track Popularity</strong>, <strong>Release Eras</strong>, and <strong>Genre Diversity</strong>.
              </p>
              <p>
                By applying clustering algorithms, the platform identifies the distinct "zones" of your preferences, helping you understand your habits and break out of your comfort zone.
              </p>
            </div>
          </div>

          {/* Stats/Visuals */}
          <div className="grid gap-4">
            <div className="p-6 rounded-2xl bg-white/[0.03] border border-white/[0.08] backdrop-blur-sm flex items-center gap-6 group hover:bg-white/[0.05] transition-colors">
              <div className="p-3 rounded-lg bg-pink-500/10 text-pink-400 group-hover:scale-110 transition-transform"><Database size={24} /></div>
              <div>
                <h3 className="text-white font-bold">Comprehensive Analysis</h3>
                <p className="text-sm text-slate-500">Analyzing thousands of data points per user.</p>
              </div>
            </div>
            <div className="p-6 rounded-2xl bg-white/[0.03] border border-white/[0.08] backdrop-blur-sm flex items-center gap-6 group hover:bg-white/[0.05] transition-colors">
              <div className="p-3 rounded-lg bg-pink-500/10 text-pink-400 group-hover:scale-110 transition-transform"><Share2 size={24} /></div>
              <div>
                <h3 className="text-white font-bold">Personalized Dashboard</h3>
                <p className="text-sm text-slate-500">Explore your unique music profile in real-time.</p>
              </div>
            </div>
          </div>
        </div>
      </section >

      {/* SECTION 4: ENGINEERING ARCHITECTURE (TECH STACK) */}
      < section id="tech" className="py-32 px-6 relative z-10" >
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <div className="text-purple-400 font-bold mb-2 tracking-widest text-xs uppercase">Under the Hood</div>
            <h2 className="text-3xl md:text-5xl font-bold tracking-tight mb-4 text-white">Engineering Architecture</h2>
            <p className="text-lg text-slate-400">A robust, scalable end-to-end data science pipeline.</p>
          </div>

          <div className="grid md:grid-cols-4 gap-6">
            <PipelineCard
              icon={<Database size={20} />}
              num="1"
              title="Data Acquisition"
              desc="Secure OAuth 2.0 handshake with Spotify API to fetch encrypted user history and meta-data."
            />
            <PipelineCard
              icon={<Cpu size={20} />}
              num="2"
              title="Feature Engineering"
              desc="Automated analysis pipeline to process and normalize thousands of data points into a unified profile."
            />
            <PipelineCard
              icon={<Layers size={20} />}
              num="3"
              title="ML Clustering"
              desc="K-Means algorithm executed via Sci-kit Learn to segment tracks into distinct resonance profiles."
            />
            <PipelineCard
              icon={<Zap size={20} />}
              num="4"
              title="Real-time UI"
              desc="Next.js frontend with dynamic data visualization for low-latency interactive dashboards."
            />
          </div>
        </div>
      </section >

      {/* SECTION 5: PLATFORM CAPABILITIES (FEATURES) */}
      < section id="features" className="py-24 px-6 relative z-10" >
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <div className="text-purple-400 font-bold mb-2 tracking-widest text-xs uppercase">Platform Capabilities</div>
            <h2 className="text-3xl md:text-5xl font-bold tracking-tight mb-4 text-white">Unlock Your Potential</h2>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <FeatureCard
              icon={<Compass size={24} />}
              title="Intelligent Recommendation"
              desc="Discover new artists that align with your resonance profile, ensuring high musical affinity."
              color="text-indigo-400"
              bg="bg-indigo-500/10"
            />
            <FeatureCard
              icon={<Search size={24} />}
              title="Sonic Evolution"
              desc="Visualize how your genre preferences have evolved over months and years with timeline graphs."
              color="text-indigo-400"
              bg="bg-indigo-500/10"
            />
            <FeatureCard
              icon={<BarChart3 size={24} />}
              title="Emotional Resonance"
              desc="Analyze the diversity and uniqueness of your library to reveal your distinct musical texture."
              color="text-indigo-400"
              bg="bg-indigo-500/10"
            />
          </div>
        </div>
      </section >

      {/* FOOTER */}
      < footer className="py-8 text-center px-6 relative z-10 border-t border-white/5" >
        <p className="text-xs text-slate-600 uppercase tracking-widest">
          © {currentYear} Resona. All Rights Reserved.
        </p>
      </footer >

    </div >
  );
}

// HELPER COMPONENTS

function ProblemCard({ title, desc, icon }: { title: string, desc: string, icon: React.ReactNode }) {
  return (
    <div className="p-8 rounded-3xl bg-white/[0.02] border border-white/[0.05] text-center hover:bg-white/[0.05] transition-colors">
      <div className="w-12 h-12 rounded-full bg-red-500/10 text-red-400 flex items-center justify-center mx-auto mb-6">
        {icon}
      </div>
      <h3 className="text-xl font-bold text-white mb-3">{title}</h3>
      <p className="text-slate-400 text-sm leading-relaxed">{desc}</p>
    </div>
  );
}

function FeatureCard({ title, desc, icon, color, bg }: { title: string, desc: string, icon: React.ReactNode, color: string, bg: string }) {
  return (
    <div className="group p-8 rounded-3xl bg-white/[0.02] border border-white/[0.05] hover:bg-white/[0.04] hover:border-white/10 transition-all duration-300 hover:-translate-y-1">
      <div className={`w-12 h-12 rounded-xl mb-6 flex items-center justify-center ${color} ${bg} shadow-lg transition-transform group-hover:scale-110`}>
        {icon}
      </div>
      <h3 className="text-xl font-bold mb-3 text-white tracking-tight">{title}</h3>
      <p className="text-slate-400 leading-relaxed text-sm">{desc}</p>
    </div>
  );
}

function PipelineCard({ num, title, desc, icon }: { num: string, title: string, desc: string, icon: React.ReactNode }) {
  return (
    <div className="relative p-8 rounded-2xl border border-white/5 hover:border-purple-500/30 hover:bg-white/[0.02] transition-colors group">
      <div className="flex justify-between items-start mb-6">
        <div className="text-xs font-mono font-bold text-purple-500 tracking-widest bg-purple-500/10 px-2 py-1 rounded">0{num}</div>
        <div className="text-slate-600 group-hover:text-purple-400 transition-colors">{icon}</div>
      </div>
      <h4 className="font-bold text-white text-lg mb-2 tracking-tight">{title}</h4>
      <p className="text-slate-500 text-sm leading-relaxed">{desc}</p>
    </div>
  );
}
