'use client';

import { useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { authAPI, auth, tokenManager, profileAPI } from '@/utils/api';
import { User } from '@/types/user';
import toast, { Toaster } from 'react-hot-toast';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, LineChart, Line, XAxis, YAxis, CartesianGrid } from 'recharts';
import {
    Music,
    LogOut,
    BarChart3,
    Play,
    Clock,
    ExternalLink,
    User as UserIcon,
    RefreshCw,
    Cpu,
    Sparkles,
    Lightbulb,
    Headphones,
    Globe,
    Rocket,
    Repeat,
    TrendingUp,
    TrendingDown,
    Database,
    Target,
    Disc3,
    Search,
    Brain,
    Fingerprint,
    Compass,
    Layers,
    ChevronDown,
    ChevronUp,
    Home,
    Settings,
    Menu,
    X,
    ArrowRight,
    Activity,
    Cloud,
    Sun,
    Zap,
    Moon,
} from 'lucide-react';

export default function Dashboard() {
    const router = useRouter();
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [profileData, setProfileData] = useState<any>(null);
    const [fetchingProfile, setFetchingProfile] = useState(false);
    const [features, setFeatures] = useState<any>(null);
    const [computingFeatures, setComputingFeatures] = useState(false);
    const [cluster, setCluster] = useState<any>(null);
    const [fetchingCluster, setFetchingCluster] = useState(false);
    const [recs, setRecs] = useState<any>(null);
    const [fetchingRecs, setFetchingRecs] = useState(false);
    const [evaluation, setEvaluation] = useState<any>(null);
    const [fetchingEvaluation, setFetchingEvaluation] = useState(false);
    const [insights, setInsights] = useState<any>(null);
    const [fetchingInsights, setFetchingInsights] = useState(false);
    const [statistics, setStatistics] = useState<any>(null);
    const [fetchingStatistics, setFetchingStatistics] = useState(false);
    const [lastSync, setLastSync] = useState<Date | null>(null);
    const [activeSection, setActiveSection] = useState('home');

    // Collapsible section states
    const [profileOpen, setProfileOpen] = useState(false);
    const [featuresOpen, setFeaturesOpen] = useState(false);
    const [clusterOpen, setClusterOpen] = useState(false);
    const [recsOpen, setRecsOpen] = useState(false);
    const [evaluationOpen, setEvaluationOpen] = useState(false);
    const [insightsOpen, setInsightsOpen] = useState(false);
    const [showLogoutMenu, setShowLogoutMenu] = useState(false);

    // Tab switching function (no scrolling, just show/hide sections)
    const switchToSection = (sectionId: string) => {
        setActiveSection(sectionId);
        localStorage.setItem('dashboardActiveSection', sectionId);
    };

    // Restore active section from local storage on mount
    useEffect(() => {
        const savedSection = localStorage.getItem('dashboardActiveSection');
        if (savedSection) {
            setActiveSection(savedSection);
        }
    }, []);



    useEffect(() => {
        if (!tokenManager.isAuthenticated()) {
            router.push('/');
            return;
        }

        const fetchUser = async () => {
            try {
                const userData = await authAPI.getCurrentUser();
                setUser(userData);
                setLoading(false);

                // Auto-fetch all data parallelly for instant availability
                handleFetchProfile();
                handleComputeFeatures(true);
                handleGetCluster(true);
                handleGetRecs(true);
                handleGetEvaluation(true);
                handleGetInsights(true);

            } catch (err) {
                // Error handled gracefully
                setError('Failed to load user data');
                setLoading(false);
            }
        };

        fetchUser();
    }, [router]);

    const handleLogout = () => {
        localStorage.removeItem('dashboardActiveSection');
        auth.logout();
    };

    const confirmLogout = () => {
        auth.logout();
    };

    const handleFetchProfile = async () => {
        setFetchingProfile(true);
        try {
            const data = await profileAPI.getCompleteProfile();
            setProfileData(data);
            setStatistics(data); // Profile data now includes statistics
            // setProfileOpen(true); // Don't auto-open
            setLastSync(new Date());
        } catch (err: any) {
            // Error handled silently
        } finally {
            setFetchingProfile(false);
        }
    };

    const handleComputeFeatures = async (forceFetch = false) => {
        // If data already loaded and not forcing, just toggle display
        if (features && !forceFetch) {
            setFeaturesOpen(!featuresOpen);
            return;
        }

        // If already loading, skip
        if (computingFeatures) return;

        // Otherwise fetch data
        setComputingFeatures(true);
        try {
            const data = await profileAPI.getFeatures(true);
            setFeatures(data);
            if (!forceFetch) setFeaturesOpen(true);
        } catch (err: any) {
            // Error handled silently
        } finally {
            setComputingFeatures(false);
        }
    };

    const handleGetCluster = async (forceFetch = false) => {
        // If data already loaded and not forcing, just toggle display
        if (cluster && !forceFetch) {
            setClusterOpen(!clusterOpen);
            return;
        }

        // If already loading, skip
        if (fetchingCluster) return;

        // Otherwise fetch data
        setFetchingCluster(true);
        try {
            const data = await profileAPI.getCluster();
            setCluster(data);
            if (!forceFetch) setClusterOpen(true);
        } catch (err: any) {
            // Error handled silently
        } finally {
            setFetchingCluster(false);
        }
    };

    const handleGetRecs = async (forceFetch = false) => {
        // If data already loaded and not forcing, just toggle display
        if (recs && !forceFetch) {
            setRecsOpen(!recsOpen);
            return;
        }

        // If already loading, skip
        if (fetchingRecs) return;

        // Otherwise fetch data
        setFetchingRecs(true);
        try {
            const data = await profileAPI.getRecommendations();
            setRecs(data);
            if (!forceFetch) setRecsOpen(true);
        } catch (err: any) {
            // Error handled silently
        } finally {
            setFetchingRecs(false);
        }
    };

    const handleGetEvaluation = async (forceFetch = false) => {
        // If data already loaded and not forcing, just toggle display
        if (evaluation && !forceFetch) {
            setEvaluationOpen(!evaluationOpen);
            return;
        }

        // If already loading, skip
        if (fetchingEvaluation) return;

        // Otherwise fetch data
        setFetchingEvaluation(true);
        try {
            const response = await fetch('http://localhost:8000/api/evaluation', {
                headers: {
                    'Authorization': `Bearer ${tokenManager.getToken()}`
                }
            });
            const data = await response.json();
            setEvaluation(data);
            if (!forceFetch) setEvaluationOpen(true);
        } catch (err: any) {
            // Error handled silently
        } finally {
            setFetchingEvaluation(false);
        }
    };

    const handleGetInsights = async (forceFetch = false) => {
        // If data already loaded and not forcing, just toggle display
        if (insights && !forceFetch) {
            setInsightsOpen(!insightsOpen);
            return;
        }

        // If already loading, skip
        if (fetchingInsights) return;

        // Otherwise fetch data
        setFetchingInsights(true);
        try {
            const response = await fetch('http://localhost:8000/api/insights', {
                headers: {
                    'Authorization': `Bearer ${tokenManager.getToken()}`
                }
            });
            const data = await response.json();
            setInsights(data);
            if (!forceFetch) setInsightsOpen(true);
        } catch (err: any) {
            // Error handled silently
        } finally {
            setFetchingInsights(false);
        }
    };

    const handleGetStatistics = async () => {
        // If data already loaded, just return (statistics are always shown)
        if (statistics) {
            return;
        }

        // Otherwise fetch data
        setFetchingStatistics(true);
        try {
            const data = await profileAPI.getStatistics();
            setStatistics(data);
        } catch (err: any) {
            // Error handled silently
        } finally {
            setFetchingStatistics(false);
        }
    };

    // Helper to format percentage
    const fmt = (val: any) => typeof val === 'number' ? `${(val * 100).toFixed(0)}%` : '0%';
    // Helper to format decimal
    const dec = (val: any) => typeof val === 'number' ? val.toFixed(2) : '0.00';

    // Helper to get Mood Icon
    const getMoodIcon = (moodTarget: string) => {
        if (!moodTarget) return Activity;
        const m = moodTarget.toLowerCase();
        if (m.includes('energetic') || m.includes('party') || m.includes('intense')) return Zap;
        if (m.includes('sad') || m.includes('dark')) return Cloud;
        if (m.includes('happy') || m.includes('cheerful') || m.includes('upbeat')) return Sun;
        if (m.includes('calm') || m.includes('chill') || m.includes('relax') || m.includes('melanch') || m.includes('reflective')) return Moon;
        return Activity;
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-[#050505] flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-purple-500 mx-auto mb-4"></div>
                    <p className="text-slate-400 text-3xl tracking-tight">Loading Resona...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen bg-[#050505] flex items-center justify-center">
                <div className="text-center">
                    <p className="text-red-400 text-xl mb-4">{error}</p>
                    <button
                        onClick={handleLogout}
                        className="bg-white/10 text-white px-6 py-2 rounded-full hover:bg-white/20 transition-colors cursor-pointer"
                    >
                        Return Home
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-[#0f0b1e] text-slate-200 font-sans selection:bg-purple-500/30 relative overflow-hidden flex">
            {/* Toaster Removed */}

            {/* Animated Liquid Background - Deep Violet Dominance */}
            <div className="fixed inset-0 z-0 overflow-hidden pointer-events-none">
                <div className="absolute inset-0 bg-[#0f0b1e]"></div>

                {/* Massive Violet Wash (Across Whole) */}
                <div className="absolute top-[-20%] left-[-20%] w-[120%] h-[120%] bg-violet-900/20 rounded-full mix-blend-screen filter blur-[120px] opacity-40 animate-blob"></div>

                {/* Massive Indigo Wash (Crossing) */}
                <div className="absolute bottom-[-20%] right-[-20%] w-[120%] h-[120%] bg-indigo-950/30 rounded-full mix-blend-screen filter blur-[120px] opacity-40 animate-blob animation-delay-4000"></div>

                {/* Accents for Depth */}
                <div className="absolute top-[10%] right-[-10%] w-[40%] h-[40%] bg-cyan-600/5 rounded-full mix-blend-screen filter blur-[100px] opacity-20 animate-blob animation-delay-2000"></div>
                <div className="absolute bottom-[-10%] left-[-10%] w-[50%] h-[50%] bg-rose-600/5 rounded-full mix-blend-screen filter blur-[100px] opacity-20 animate-blob animation-delay-4000"></div>

                <div className="absolute inset-0 bg-black/20 backdrop-blur-[30px]"></div>
            </div>

            {/* Sidebar */}
            <div className="fixed left-0 top-0 h-screen w-64 bg-[#0a0614]/95 backdrop-blur-xl border-r border-violet-500/20 z-50 flex flex-col">
                {/* Logo */}
                <div className="py-4 flex items-center justify-center border-b border-violet-500/20">
                    <h1 className="text-3xl font-extrabold tracking-tighter uppercase bg-violet-200 bg-clip-text text-transparent">
                        RESONA
                    </h1>
                </div>

                {/* Navigation */}
                <nav className="flex-1 px-4 py-6 space-y-4 overflow-y-auto mt-1 ml-1">
                    {[
                        { id: 'home', icon: Home, label: 'Home' },
                        { id: 'statistics', icon: BarChart3, label: 'Statistics' },
                        { id: 'features', icon: Cpu, label: 'Features' },
                        { id: 'identity', icon: Fingerprint, label: 'Identity' },
                        { id: 'discovery', icon: Compass, label: 'Discovery' },
                        { id: 'performance', icon: Target, label: 'Performance' },
                        { id: 'analysis', icon: Brain, label: 'Deep Analysis' },
                    ].map((item) => (
                        <button
                            key={item.id}
                            onClick={() => switchToSection(item.id)}
                            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 cursor-pointer border ${activeSection === item.id
                                ? 'bg-violet-500/10 border-violet-500/50 text-white shadow-[0_0_15px_rgba(139,92,246,0.3)]'
                                : 'border-transparent text-slate-400 hover:bg-violet-500/05 hover:border-violet-500/20 hover:text-white hover:shadow-[0_0_10px_rgba(139,92,246,0.1)]'
                                }`}
                        >
                            <item.icon className="w-5 h-5" />
                            <span className="font-medium text-sm">{item.label}</span>
                        </button>
                    ))}
                </nav>

                {/* User Profile in Sidebar */}
                <div className="p-4 border-t border-violet-500/20">
                    <div className="flex items-center gap-3 mb-4">
                        {user?.profile_image ? (
                            <img src={user.profile_image} alt="Profile" className="w-10 h-10 rounded-full border-2 border-violet-500/30" />
                        ) : (
                            <div className="w-10 h-10 rounded-full bg-violet-500 flex items-center justify-center">
                                <UserIcon className="w-5 h-5 text-white" />
                            </div>
                        )}
                        <div className="flex-1 min-w-0">
                            <p className="text-sm font-medium text-white truncate">{user?.display_name || 'User'}</p>
                            <p className="text-xs text-slate-500 truncate">{user?.email}</p>
                        </div>
                    </div>

                    <button
                        onClick={handleLogout}
                        className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-white/5 hover:bg-red-500/10 text-slate-400 hover:text-red-400 rounded-xl transition-all text-sm font-medium cursor-pointer group border border-transparent hover:border-red-500/20"
                    >
                        <LogOut className="w-4 h-4 group-hover:scale-110 transition-transform" />
                        <span>Logout</span>
                    </button>
                </div>


            </div>

            {/* Main Content */}
            <div className="flex-1 ml-64 relative z-10">


                {/* Content Sections */}
                <div className="max-w-[1600px] mx-auto p-6 md:p-8 space-y-12">

                    {/* Home Section */}
                    {activeSection === 'home' && (
                        <div className="flex flex-col items-center justify-center min-h-[60vh] text-center animate-in fade-in slide-in-from-bottom-4 duration-700">
                            <div className="mb-12 max-w-2xl">
                                <h2 className="text-4xl md:text-5xl font-bold text-white mb-4 tracking-tight">Welcome to Resona</h2>
                                <p className="text-lg text-slate-400 italic">Your personalized music intelligence platform.</p>
                                <p className="text-sm text-slate-500 mt-2">Explore your unique resonance profile through our advanced analysis tools below.</p>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 w-full max-w-5xl">
                                {[
                                    { id: 'statistics', icon: BarChart3, label: 'Statistics', desc: 'Detailed insights into your listening habits & history' },
                                    { id: 'features', icon: Cpu, label: 'Audio Features', desc: 'Technical analysis of your unique sound profile' },
                                    { id: 'identity', icon: Fingerprint, label: 'Identity', desc: 'Discover your specific listener persona cluster' },
                                    { id: 'discovery', icon: Compass, label: 'Discovery', desc: 'AI-curated recommendations based on your taste' },
                                    { id: 'performance', icon: Target, label: 'Performance', desc: 'Evaluation metrics of our recommendation engine' },
                                    { id: 'analysis', icon: Brain, label: 'Deep Analysis', desc: 'Advanced mood profiling & genre evolution tracking' },
                                ].map((item) => (
                                    <button
                                        key={item.id}
                                        onClick={() => switchToSection(item.id)}
                                        className="group bg-white/[0.03] hover:bg-white/[0.06] border border-white/5 hover:border-violet-500/30 p-6 rounded-2xl transition-all duration-300 flex flex-col items-center text-center hover:-translate-y-1 cursor-pointer"
                                    >
                                        <div className="p-4 bg-white/5 rounded-full mb-4 group-hover:bg-violet-500/20 group-hover:scale-110 transition-all">
                                            <item.icon className="w-8 h-8 text-slate-400 group-hover:text-violet-400 transition-colors" />
                                        </div>
                                        <h3 className="text-lg font-bold text-white mb-2 group-hover:text-violet-200 transition-colors">{item.label}</h3>
                                        <p className="text-sm text-slate-500 group-hover:text-slate-400 transition-colors">{item.desc}</p>
                                    </button>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Statistics Section */}
                    {activeSection === 'statistics' && (
                        <div>

                            <div className="w-full bg-white/[0.02] border border-violet-500/20 hover:border-violet-500/40 hover:bg-violet-500/05 hover:shadow-[0_0_20px_-5px_rgba(139,92,246,0.2)] backdrop-blur-3xl rounded-3xl overflow-hidden transition-all duration-300 group">
                                <div className="p-6 flex flex-col h-full bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-violet-500/10 via-transparent to-transparent">
                                    <div className="flex items-center gap-4 mb-3">
                                        <div className="p-3 bg-violet-500/10 rounded-xl">
                                            <BarChart3 className="w-6 h-6 text-violet-400" />
                                        </div>
                                        <div>
                                            <h3 className="text-2xl font-bold text-white">Statistics</h3>
                                            <p className="text-xs text-slate-400 italic">Your listening insights</p>
                                        </div>
                                    </div>

                                    <div className="mt-0">

                                        {statistics ? (
                                            <div className="pt-6 animate-in fade-in slide-in-from-top-2 space-y-10">
                                                {/* 1. Top Artists Row */}
                                                {statistics.top_artists_list && statistics.top_artists_list.length > 0 && (
                                                    <div>
                                                        <div className="flex items-center justify-between mb-1">
                                                            <p className="text-[10px] text-violet-300/70 uppercase font-bold tracking-wider">Your Top Artists <span className="text-slate-500 font-normal ml-1">(All Time)</span></p>
                                                        </div>
                                                        <div className="flex items-center gap-6 overflow-x-auto pb-4 pt-4 scrollbar-none px-2">
                                                            {statistics.top_artists_list.map((artist: any, idx: number) => (
                                                                <div key={idx} className="flex flex-col items-center min-w-[80px] group/artist cursor-pointer">
                                                                    <div className="relative w-20 h-20 mb-3 group-hover/artist:scale-110 transition-transform duration-300 mt-2">
                                                                        <div className="w-full h-full rounded-full overflow-hidden border-2 border-white/10 group-hover/artist:border-violet-500 transition-all shadow-lg shadow-black/40 group-hover/artist:shadow-violet-500/20">
                                                                            {artist.image ? (
                                                                                <img src={artist.image} alt={artist.name} className="w-full h-full object-cover" />
                                                                            ) : (
                                                                                <div className="w-full h-full bg-slate-800 flex items-center justify-center"><UserIcon className="w-8 h-8 text-slate-500" /></div>
                                                                            )}
                                                                        </div>
                                                                        <div className="absolute -top-1 -right-1 w-6 h-6 bg-violet-600 rounded-full flex items-center justify-center text-[10px] font-bold text-white shadow-md border-2 border-[#1a1625] z-10">
                                                                            {idx + 1}
                                                                        </div>
                                                                    </div>
                                                                    <p className="text-xs text-center text-slate-300 font-bold truncate w-24 group-hover/artist:text-white transition-colors">
                                                                        {artist.name}
                                                                    </p>
                                                                </div>
                                                            ))}
                                                        </div>
                                                    </div>
                                                )
                                                }

                                                {/* 2. Top Genres (Mix Line + Circles) */}
                                                {statistics.top_genres_list && statistics.top_genres_list.length > 0 && (
                                                    <div>
                                                        <div className="flex items-center justify-between mb-5">
                                                            <p className="text-[10px] text-violet-300/70 uppercase font-bold tracking-wider">Your Top Genres <span className="text-slate-500 font-normal ml-1">(All Time)</span></p>
                                                        </div>

                                                        {/* Genre Mix Line (Bar Chart) */}
                                                        <div className="mb-5">
                                                            <div className="flex h-4 w-full rounded-full overflow-hidden bg-white/5 shadow-inner">
                                                                {statistics.top_genres_list.map((genre: any, idx: number) => {
                                                                    // Calculate total percentage of just the top genres to normalize the bar width to 100%
                                                                    const totalDisplayedPercent = statistics.top_genres_list.reduce((acc: number, curr: any) => acc + curr.percent, 0) || 100;
                                                                    const normalizedWidth = (genre.percent / totalDisplayedPercent) * 100;

                                                                    return (
                                                                        <div
                                                                            key={idx}
                                                                            style={{ width: `${normalizedWidth}%` }}
                                                                            className={`h-full ${['bg-violet-600', 'bg-indigo-500', 'bg-blue-500', 'bg-cyan-500', 'bg-teal-500', 'bg-emerald-500', 'bg-green-500', 'bg-lime-500', 'bg-yellow-500', 'bg-orange-500'][idx % 10]
                                                                                } hover:brightness-110 transition-all relative group/genre-bar cursor-default border-r last:border-r-0 border-black/20`}
                                                                        >
                                                                            <div className="absolute bottom-full mb-2 left-1/2 -translate-x-1/2 bg-black/90 text-white text-[10px] px-2 py-1 rounded opacity-0 group-hover/genre-bar:opacity-100 whitespace-nowrap pointer-events-none transition-opacity z-10 border border-white/10 font-bold shadow-xl">
                                                                                {genre.name} • {genre.percent}%
                                                                            </div>
                                                                        </div>
                                                                    );
                                                                })}
                                                            </div>
                                                        </div>

                                                        {/* Genre Legend (Matching Design) */}
                                                        <div className="flex gap-x-6 gap-y-3 flex-wrap pb-4">
                                                            {statistics.top_genres_list.map((genre: any, idx: number) => (
                                                                <div key={idx} className="flex items-center gap-2">
                                                                    <div className={`w-2.5 h-2.5 rounded-full ${['bg-violet-600', 'bg-indigo-500', 'bg-blue-500', 'bg-cyan-500', 'bg-teal-500', 'bg-emerald-500', 'bg-green-500', 'bg-lime-500', 'bg-yellow-500', 'bg-orange-500'][idx % 10]}`}></div>
                                                                    <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                                                                        {genre.name} <span className="text-slate-500 font-medium opacity-70">({genre.percent}%)</span>
                                                                    </span>
                                                                </div>
                                                            ))}
                                                        </div>
                                                    </div>
                                                )}

                                                {/* 3. Top Tracks Grid */}
                                                {statistics.top_tracks_list && statistics.top_tracks_list.length > 0 && (
                                                    <div>
                                                        <p className="text-[10px] text-violet-300/70 uppercase font-bold tracking-wider mb-5">Your Top Tracks <span className="text-slate-500 font-normal ml-1">(All Time)</span></p>
                                                        <div className="grid grid-cols-2 lg:grid-cols-3 gap-3 pb-4">
                                                            {statistics.top_tracks_list.map((track: any, idx: number) => {
                                                                // Construct generic Spotify URL if external_urls is missing (common in some API responses)
                                                                const spotifyUrl = track.external_urls?.spotify || (track.id ? `https://open.spotify.com/track/${track.id}` : '#');
                                                                return (
                                                                    <a
                                                                        key={idx}
                                                                        href={spotifyUrl}
                                                                        target="_blank"
                                                                        rel="noopener noreferrer"
                                                                        className="bg-white/5 hover:bg-white/10 p-2 rounded-xl flex items-center gap-3 transition-colors group/track border border-white/5 hover:border-violet-500/20 cursor-pointer block"
                                                                    >
                                                                        <div className="relative w-12 h-12 rounded-lg overflow-hidden flex-shrink-0 shadow-md">
                                                                            {track.image ? (
                                                                                <img src={track.image} className="w-full h-full object-cover group-hover/track:scale-105 transition-transform duration-500" />
                                                                            ) : (
                                                                                <div className="w-full h-full bg-slate-800" />
                                                                            )}
                                                                            <div className="absolute inset-0 flex items-center justify-center bg-black/40 opacity-0 group-hover/track:opacity-100 transition-opacity">
                                                                                <Play className="w-5 h-5 text-white fill-white" />
                                                                            </div>
                                                                        </div>
                                                                        <div className="min-w-0">
                                                                            <p className="text-xs font-bold text-white truncate group-hover/track:text-violet-300 transition-colors">{track.name}</p>
                                                                            <p className="text-[10px] text-slate-400 truncate">{track.artist}</p>
                                                                            <p className="text-[9px] text-green-500 font-medium mt-0.5">Play on Spotify</p>
                                                                        </div>
                                                                    </a>
                                                                );
                                                            })}
                                                        </div>
                                                    </div>
                                                )}

                                                {/* 4. Metrics Footer */}
                                                <div>
                                                    <p className="text-[10px] text-violet-300/70 uppercase font-bold tracking-wider mb-5">All Time Engagement</p>
                                                    <div className="grid grid-cols-3 gap-4">
                                                        <div className="bg-gradient-to-br from-white/5 to-white/[0.02] p-4 rounded-2xl border border-white/5 flex items-center gap-3">
                                                            <div className="p-3 bg-blue-500/20 rounded-xl">
                                                                <Clock className="w-5 h-5 text-blue-400" />
                                                            </div>
                                                            <div className="min-w-0">
                                                                <p className="text-xl lg:text-2xl font-bold text-white leading-none truncate">
                                                                    {(() => {
                                                                        const hours = statistics.estimated_total_hours || 0;
                                                                        if (hours > 24) {
                                                                            const days = Math.floor(hours / 24);
                                                                            const remainingHours = Math.round(hours % 24);
                                                                            return `${days}d ${remainingHours}h`;
                                                                        }
                                                                        return `${hours}h`;
                                                                    })()}
                                                                </p>
                                                                <p className="text-[9px] lg:text-[10px] text-slate-400 mt-1 uppercase tracking-wide font-medium truncate">Est. Playtime (Liked Songs)</p>
                                                            </div>
                                                        </div>
                                                        <div className="bg-gradient-to-br from-white/5 to-white/[0.02] p-4 rounded-2xl border border-white/5 flex items-center gap-3">
                                                            <div className="p-3 bg-violet-500/20 rounded-xl">
                                                                <Music className="w-5 h-5 text-violet-400" />
                                                            </div>
                                                            <div className="min-w-0">
                                                                <p className="text-xl lg:text-2xl font-bold text-white leading-none truncate">{statistics.total_liked_songs || 0}</p>
                                                                <p className="text-[9px] lg:text-[10px] text-slate-400 mt-1 uppercase tracking-wide font-medium truncate">Liked Songs</p>
                                                            </div>
                                                        </div>
                                                        <div className="bg-gradient-to-br from-white/5 to-white/[0.02] p-4 rounded-2xl border border-white/5 flex items-center gap-3">
                                                            <div className="p-3 bg-indigo-500/20 rounded-xl">
                                                                <UserIcon className="w-5 h-5 text-indigo-400" />
                                                            </div>
                                                            <div className="min-w-0">
                                                                <p className="text-xl lg:text-2xl font-bold text-white leading-none truncate">{statistics.total_followed_artists || 0}</p>
                                                                <p className="text-[9px] lg:text-[10px] text-slate-400 mt-1 uppercase tracking-wide font-medium truncate">Followed Artists</p>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        ) : (
                                            <div className="pt-4 border-t border-white/5 text-center text-slate-500 text-sm">
                                                Loading statistics...
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Features Section */}
                    {activeSection === 'features' && (
                        <div>

                            <div className="w-full">
                                {/* Feature Engineering - Standard Card */}
                                <div className="w-full bg-white/[0.02] border border-violet-500/20 hover:border-violet-500/40 hover:bg-violet-500/05 hover:shadow-[0_0_20px_-5px_rgba(139,92,246,0.2)] backdrop-blur-3xl rounded-3xl overflow-hidden transition-all duration-300 group">
                                    <div className="p-6 flex flex-col h-full bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-violet-500/10 via-transparent to-transparent">
                                        <div className="flex items-center gap-4 mb-3">
                                            <div className="p-3 bg-violet-500/10 rounded-xl">
                                                <Cpu className="w-6 h-6 text-violet-400" />
                                            </div>
                                            <div>
                                                <h3 className="text-2xl font-bold text-white">Features</h3>
                                                <p className="text-xs text-slate-400 italic">Analyze your listening patterns & habits</p>
                                            </div>
                                        </div>

                                        <div className="mt-0">
                                            {features ? (
                                                <div className="pt-6 border-t border-white/5 animate-in fade-in slide-in-from-top-2 space-y-8">

                                                    {/* Profile Summary */}
                                                    <div>
                                                        <p className="text-[10px] text-violet-300/70 uppercase font-bold tracking-wider mb-3">Profile Summary</p>
                                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                                            <div className="bg-white/5 p-4 rounded-2xl border border-white/5 flex flex-col justify-center gap-2 group/card hover:bg-white/10 transition-colors">
                                                                <div className="flex items-center gap-2 mb-1">
                                                                    <Headphones className="w-4 h-4 text-violet-400" />
                                                                    <p className="text-[10px] text-violet-300/70 uppercase font-bold tracking-wider">Listening Style</p>
                                                                </div>
                                                                <p className="text-sm font-bold text-white transition-colors group-hover/card:text-violet-200">
                                                                    {features.summary?.listening_style || 'Analyzing style...'}
                                                                </p>
                                                                <p className="text-[10px] text-slate-400 mt-1">Your unique sonic signature & habits</p>
                                                            </div>
                                                            <div className="bg-white/5 p-4 rounded-2xl border border-white/5 flex flex-col justify-center gap-2 group/card hover:bg-white/10 transition-colors">
                                                                <div className="flex items-center gap-2 mb-1">
                                                                    <Globe className="w-4 h-4 text-indigo-400" />
                                                                    <p className="text-[10px] text-violet-300/70 uppercase font-bold tracking-wider">Diversity Score</p>
                                                                </div>
                                                                <p className="text-sm font-bold text-white transition-colors group-hover/card:text-indigo-200">
                                                                    {features.summary?.diversity_level || 'Analyzing diversity...'}
                                                                </p>
                                                                <p className="text-[10px] text-slate-400 mt-1">Variety across genres & artists</p>
                                                            </div>
                                                        </div>
                                                    </div>

                                                    {/* Behavioral Patterns */}
                                                    <div>
                                                        <p className="text-[10px] text-violet-300/70 uppercase font-bold tracking-wider mb-3">Behavioral Patterns</p>
                                                        <div className="grid grid-cols-2 gap-4">
                                                            <div className="bg-white/5 p-4 rounded-2xl border border-white/5 text-center flex flex-col items-center gap-2 hover:bg-white/10 transition-colors">
                                                                <div className="p-2 bg-emerald-500/10 rounded-full mb-1">
                                                                    <Repeat className="w-5 h-5 text-emerald-400" />
                                                                </div>
                                                                <div>
                                                                    <p className="text-xl font-bold text-white">
                                                                        {features.features?.behavioral?.repeat_rate
                                                                            ? (features.features.behavioral.repeat_rate * 100).toFixed(0) + '%'
                                                                            : '0%'}
                                                                    </p>
                                                                    <p className="text-[10px] text-slate-300 uppercase tracking-wide font-bold mt-1">Repeat Rate</p>
                                                                    <p className="text-[9px] text-slate-500 mt-1">Tracks played on heavy rotation</p>
                                                                </div>
                                                            </div>
                                                            <div className="bg-white/5 p-4 rounded-2xl border border-white/5 text-center flex flex-col items-center gap-2 hover:bg-white/10 transition-colors">
                                                                <div className="p-2 bg-blue-500/10 rounded-full mb-1">
                                                                    <Rocket className="w-5 h-5 text-blue-400" />
                                                                </div>
                                                                <div>
                                                                    <p className="text-xl font-bold text-white">
                                                                        {features.features?.behavioral?.exploration_score
                                                                            ? (features.features.behavioral.exploration_score * 100).toFixed(0) + '%'
                                                                            : '0%'}
                                                                    </p>
                                                                    <p className="text-[10px] text-slate-300 uppercase tracking-wide font-bold mt-1">Exploration</p>
                                                                    <p className="text-[9px] text-slate-500 mt-1">Discovery of fresh new tracks</p>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>


                                                </div>
                                            ) : (
                                                <div className="pt-4 border-t border-white/5 text-center text-slate-500 text-sm">
                                                    {computingFeatures ? 'Processing audio features...' : 'Waiting for analysis...'}
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Identity Section */}
                    {activeSection === 'identity' && (
                        <div>

                            <div className="w-full">
                                {/* Music Identity - Standard Card */}
                                <div className="w-full bg-white/[0.02] border border-violet-500/20 hover:border-violet-500/40 hover:bg-violet-500/05 hover:shadow-[0_0_20px_-5px_rgba(139,92,246,0.2)] backdrop-blur-3xl rounded-3xl overflow-hidden transition-all duration-300 group">
                                    <div className="p-6 flex flex-col h-full bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-violet-500/10 via-transparent to-transparent">
                                        <div className="flex items-center gap-4 mb-3">
                                            <div className="p-3 bg-violet-500/10 rounded-xl">
                                                <Fingerprint className="w-6 h-6 text-violet-400" />
                                            </div>
                                            <div>
                                                <h3 className="text-2xl font-bold text-white">Identity</h3>
                                                <p className="text-xs text-slate-400 italic">Discover your unique musical persona</p>
                                            </div>
                                        </div>

                                        <div className="mt-0">

                                            {cluster ? (
                                                <div className="pt-8 border-t border-white/5 animate-in fade-in slide-in-from-top-2 flex flex-col items-center text-center relative group/identity w-full bg-white/[0.02] border border-violet-500/20 rounded-2xl p-8 mb-4">



                                                    <div className="relative z-10 flex flex-col items-center">

                                                        <p className="text-[10px] text-violet-300/70 uppercase font-bold tracking-widest mb-3">Your Personality</p>
                                                        <h4 className="text-4xl md:text-5xl font-bold text-white mb-5 tracking-tight drop-shadow-sm bg-clip-text text-transparent bg-gradient-to-br from-white via-white to-slate-400">
                                                            {cluster.cluster_label || cluster.cluster_name || 'Unknown Persona'}
                                                        </h4>
                                                        <p className="text-base text-slate-400 max-w-lg leading-relaxed mix-blend-plus-lighter font-light">
                                                            {cluster.description || 'Analyzing your listening patterns to separate you from the crowd...'}
                                                        </p>

                                                    </div>
                                                </div>
                                            ) : (
                                                <div className="pt-4 border-t border-white/5 text-center text-slate-500 text-sm">
                                                    {fetchingCluster ? 'Identifying cluster...' : 'Waiting for data...'}
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Discovery Section */}
                    {activeSection === 'discovery' && (
                        <div>
                            <div className="w-full">
                                {/* Discovery Zone - Standard Card */}
                                <div className="w-full bg-white/[0.02] border border-violet-500/20 hover:border-violet-500/40 hover:bg-violet-500/05 hover:shadow-[0_0_20px_-5px_rgba(139,92,246,0.2)] backdrop-blur-3xl rounded-3xl overflow-hidden transition-all duration-300 group">
                                    <div className="p-6 flex flex-col h-full bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-violet-500/10 via-transparent to-transparent">
                                        <div className="flex items-center gap-4 mb-3">
                                            <div className="p-3 bg-violet-500/10 rounded-xl">
                                                <Compass className="w-6 h-6 text-violet-400" />
                                            </div>
                                            <div>
                                                <h3 className="text-2xl font-bold text-white">Discovery</h3>
                                                <p className="text-xs text-slate-400 italic">AI-curated music recommendations</p>
                                            </div>
                                        </div>

                                        <div className="mt-0 space-y-4">

                                            {recs ? (
                                                <div className="pt-4 border-t border-white/5 animate-in fade-in slide-in-from-top-2">
                                                    <p className="text-[10px] text-violet-300/70 uppercase font-bold tracking-wider mb-2">
                                                        Recommended Tracks ({recs.tracks?.length || 0})
                                                    </p>
                                                    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
                                                        {recs.tracks?.slice(0, 20).map((track: any, idx: number) => {
                                                            const spotifyUrl = track.external_urls?.spotify || (track.id ? `https://open.spotify.com/track/${track.id}` : '#');
                                                            return (
                                                                <a
                                                                    key={idx}
                                                                    href={spotifyUrl}
                                                                    target="_blank"
                                                                    rel="noopener noreferrer"
                                                                    className="group/track relative flex flex-col bg-white/5 p-4 rounded-2xl border border-white/5 hover:bg-white/10 hover:border-violet-500/30 transition-all duration-300 hover:-translate-y-1 cursor-pointer block"
                                                                >
                                                                    {/* Album Art */}
                                                                    <div className="relative aspect-square w-full mb-4 overflow-hidden rounded-xl shadow-lg">
                                                                        {track.album?.image ? (
                                                                            <img src={track.album.image} alt="Art" className="w-full h-full object-cover group-hover/track:scale-105 transition-transform duration-500" />
                                                                        ) : (
                                                                            <div className="w-full h-full bg-slate-800 flex items-center justify-center"><Music className="text-slate-600" /></div>
                                                                        )}

                                                                        {/* Play Overlay */}
                                                                        <div className="absolute inset-0 bg-black/40 opacity-0 group-hover/track:opacity-100 flex items-center justify-center transition-opacity duration-300">
                                                                            <div className="w-12 h-12 rounded-full bg-[#1DB954] flex items-center justify-center shadow-xl shadow-green-500/30 transform group-hover/track:scale-110 transition-transform">
                                                                                <Play className="w-6 h-6 text-black ml-1 fill-black" />
                                                                            </div>
                                                                        </div>
                                                                    </div>

                                                                    {/* Track Info */}
                                                                    <div className="mt-auto">
                                                                        <p className="text-sm font-bold text-white truncate mb-1">{track.name}</p>
                                                                        <p className="text-xs text-slate-400 truncate">{track.artists?.[0]?.name || 'Unknown Artist'}</p>
                                                                        <p className="text-[10px] text-green-500 font-medium mt-2">Play on Spotify</p>
                                                                    </div>
                                                                </a>
                                                            );
                                                        })}
                                                    </div>
                                                </div>
                                            ) : (
                                                <div className="pt-4 border-t border-white/5 text-center text-slate-500 text-sm">
                                                    {fetchingRecs ? 'Curating recommendations...' : 'Waiting for discovery...'}
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Performance Section */}
                    {activeSection === 'performance' && (
                        <div>

                            <div className="w-full">
                                {/* Model Performance - Standard Card */}
                                <div className="w-full bg-white/[0.02] border border-violet-500/20 hover:border-violet-500/40 hover:bg-violet-500/05 hover:shadow-[0_0_20px_-5px_rgba(139,92,246,0.2)] backdrop-blur-3xl rounded-3xl overflow-hidden transition-all duration-300 group">
                                    <div className="p-6 flex flex-col h-full bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-violet-500/10 via-transparent to-transparent">
                                        <div className="flex items-center gap-4 mb-3">
                                            <div className="p-3 bg-violet-500/10 rounded-xl">
                                                <Target className="w-6 h-6 text-violet-400" />
                                            </div>
                                            <div>
                                                <h3 className="text-2xl font-bold text-white">Performance</h3>
                                                <p className="text-xs text-slate-400 italic">ML model evaluation metrics</p>
                                            </div>
                                        </div>

                                        <div className="mt-0 space-y-4">

                                            {evaluation?.metrics ? (
                                                <div className="grid grid-cols-2 gap-4 animate-in fade-in slide-in-from-top-2 border-t border-white/5 pt-4">
                                                    <div className="bg-white/5 p-4 rounded-xl text-center border border-white/5 flex flex-col items-center justify-center hover:bg-white/10 transition-colors group/metric">
                                                        <p className="text-xs text-violet-300/70 uppercase tracking-widest font-bold mb-1 group-hover/metric:text-violet-300 transition-colors">Precision</p>
                                                        <p className="text-3xl font-bold text-white mb-2">{((evaluation.metrics?.precision_at_k || 0) * 100).toFixed(0)}%</p>
                                                        <p className="text-[10px] text-slate-500 font-medium">Relevance of top recommendations</p>
                                                    </div>
                                                    <div className="bg-white/5 p-4 rounded-xl text-center border border-white/5 flex flex-col items-center justify-center hover:bg-white/10 transition-colors group/metric">
                                                        <p className="text-xs text-violet-300/70 uppercase tracking-widest font-bold mb-1 group-hover/metric:text-violet-300 transition-colors">Recall</p>
                                                        <p className="text-3xl font-bold text-white mb-2">{((evaluation.metrics?.recall_at_k || 0) * 100).toFixed(0)}%</p>
                                                        <p className="text-[10px] text-slate-500 font-medium">Coverage of your user profile</p>
                                                    </div>
                                                    <div className="bg-white/5 p-4 rounded-xl text-center border border-white/5 flex flex-col items-center justify-center hover:bg-white/10 transition-colors group/metric">
                                                        <p className="text-xs text-violet-300/70 uppercase tracking-widest font-bold mb-1 group-hover/metric:text-violet-300 transition-colors">F1 Score</p>
                                                        <p className="text-3xl font-bold text-white mb-2">{((evaluation.metrics?.f1_at_k || 0) * 100).toFixed(0)}%</p>
                                                        <p className="text-[10px] text-slate-500 font-medium">Harmonic mean of accuracy</p>
                                                    </div>
                                                    <div className="bg-white/5 p-4 rounded-xl text-center border border-white/5 flex flex-col items-center justify-center hover:bg-white/10 transition-colors group/metric">
                                                        <p className="text-xs text-violet-300/70 uppercase tracking-widest font-bold mb-1 group-hover/metric:text-violet-300 transition-colors">Diversity</p>
                                                        <p className="text-3xl font-bold text-white mb-2">{((evaluation.metrics?.diversity_score || 0) * 100).toFixed(0)}%</p>
                                                        <p className="text-[10px] text-slate-500 font-medium">Variety in artist selection</p>
                                                    </div>
                                                </div>
                                            ) : (
                                                <div className="pt-4 border-t border-white/5 text-center text-slate-500 text-sm">
                                                    {fetchingEvaluation ? 'Calculating metrics...' : 'Waiting for performance data...'}
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Deep Analysis Section */}
                    {activeSection === 'analysis' && (
                        <div>

                            <div className="w-full">
                                {/* Taste Analysis - Standard Card */}
                                <div className="w-full bg-white/[0.02] border border-violet-500/20 hover:border-violet-500/40 hover:bg-violet-500/05 hover:shadow-[0_0_20px_-5px_rgba(139,92,246,0.2)] backdrop-blur-3xl rounded-3xl overflow-hidden transition-all duration-300 group">
                                    <div className="p-6 flex flex-col h-full bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-violet-500/10 via-transparent to-transparent">
                                        <div className="flex items-center gap-4 mb-3">
                                            <div className="p-3 bg-violet-500/10 rounded-xl">
                                                <Brain className="w-6 h-6 text-violet-400" />
                                            </div>
                                            <div>
                                                <h3 className="text-2xl font-bold text-white">Deep Analysis</h3>
                                                <p className="text-xs text-slate-400 italic">Advanced ML taste profiling</p>
                                            </div>
                                        </div>

                                        <div className="mt-0 space-y-4">

                                            {insights ? (
                                                <div className="pt-4 border-t border-white/5 animate-in fade-in slide-in-from-top-2 space-y-4">
                                                    {/* Mood Profile (Hero Card) */}
                                                    <div className="bg-gradient-to-r from-violet-600/20 to-indigo-600/20 p-6 rounded-2xl border border-white/10 relative overflow-hidden group/mood flex items-center justify-between">
                                                        <div className="relative z-10">
                                                            <p className="text-xs text-violet-300 uppercase font-bold tracking-widest mb-2">Emotional Resonance</p>
                                                            <h4 className="text-3xl md:text-4xl font-bold text-white mb-2">{insights.mood?.mood_label || insights.mood?.dominant_mood}</h4>
                                                            <p className="text-sm text-slate-300 max-w-sm italic">Your musical emotional fingerprint, derived from the sonic textures of your top tracks.</p>
                                                        </div>

                                                        {/* Icon - Fully Visible & Distinct */}
                                                        <div className="text-violet-300 mr-6 filter drop-shadow-[0_0_20px_rgba(139,92,246,0.3)]">
                                                            {(() => {
                                                                const Icon = getMoodIcon(insights.mood?.mood_label || insights.mood?.dominant_mood);
                                                                return <Icon className="w-24 h-24" strokeWidth={2} fill="rgba(167, 139, 250, 0.1)" />;
                                                            })()}
                                                        </div>
                                                    </div>

                                                    {/* Advanced Metrics Grid */}
                                                    <div className="grid grid-cols-2 gap-4">
                                                        <div className="bg-white/5 p-4 rounded-2xl border border-white/5 flex flex-col items-center justify-center text-center hover:bg-white/10 transition-colors">
                                                            <p className="text-[10px] text-violet-300/70 uppercase font-bold tracking-wider mb-2">Entropy Score</p>
                                                            <p className="text-3xl font-bold text-white mb-1">{(insights.entropy_score || 0).toFixed(2)}</p>
                                                            <p className="text-[10px] text-slate-500">Chaos & unpredictability in your listening</p>
                                                        </div>
                                                        <div className="bg-white/5 p-4 rounded-2xl border border-white/5 flex flex-col items-center justify-center text-center hover:bg-white/10 transition-colors">
                                                            <p className="text-[10px] text-violet-300/70 uppercase font-bold tracking-wider mb-2">Uniqueness</p>
                                                            <p className="text-3xl font-bold text-white mb-1">
                                                                {insights.deviation?.unique_score
                                                                    ? (insights.deviation.unique_score * 100).toFixed(0) + '%'
                                                                    : 'N/A'}
                                                            </p>
                                                            <p className="text-[10px] text-slate-500">Deviation from the mainstream norm</p>
                                                        </div>
                                                    </div>

                                                    {/* Genre Evolution */}
                                                    {insights.evolution && (
                                                        <div className="mt-4 pt-4">
                                                            <p className="text-[10px] text-violet-300/70 uppercase font-bold tracking-wider mb-3">Timeline Shifts</p>
                                                            <div className="grid grid-cols-2 gap-4">
                                                                {insights.evolution.rising_genres?.length > 0 ? (
                                                                    <div className="bg-emerald-500/10 p-4 rounded-2xl border border-emerald-500/20">
                                                                        <div className="flex items-center gap-2 mb-3">
                                                                            <div className="p-1.5 bg-emerald-500/20 rounded-full">
                                                                                <TrendingUp className="w-3 h-3 text-emerald-400" />
                                                                            </div>
                                                                            <p className="text-xs font-bold text-emerald-400 uppercase tracking-wide">Rising Interest</p>
                                                                        </div>
                                                                        <div className="flex flex-wrap gap-2">
                                                                            {insights.evolution.rising_genres.slice(0, 3).map((g: any, i: number) => (
                                                                                <span key={i} className="text-xs font-medium text-emerald-300 bg-emerald-500/20 border border-emerald-500/20 px-2.5 py-1 rounded-lg">
                                                                                    {g.genre}
                                                                                </span>
                                                                            ))}
                                                                        </div>
                                                                    </div>
                                                                ) : (
                                                                    <div className="bg-white/5 p-4 rounded-2xl border border-white/5 flex items-center justify-center text-slate-500 text-xs">
                                                                        No rising trends detected
                                                                    </div>
                                                                )}

                                                                {insights.evolution.falling_genres?.length > 0 ? (
                                                                    <div className="bg-rose-500/10 p-4 rounded-2xl border border-rose-500/20">
                                                                        <div className="flex items-center gap-2 mb-3">
                                                                            <div className="p-1.5 bg-rose-500/20 rounded-full">
                                                                                <TrendingDown className="w-3 h-3 text-rose-400" />
                                                                            </div>
                                                                            <p className="text-xs font-bold text-rose-400 uppercase tracking-wide">Fading Interest</p>
                                                                        </div>
                                                                        <div className="flex flex-wrap gap-2">
                                                                            {insights.evolution.falling_genres.slice(0, 3).map((g: any, i: number) => (
                                                                                <span key={i} className="text-xs font-medium text-rose-300 bg-rose-500/20 border border-rose-500/20 px-2.5 py-1 rounded-lg">
                                                                                    {g.genre}
                                                                                </span>
                                                                            ))}
                                                                        </div>
                                                                    </div>
                                                                ) : (
                                                                    <div className="bg-white/5 p-4 rounded-2xl border border-white/5 flex items-center justify-center text-slate-500 text-xs">
                                                                        No falling trends detected
                                                                    </div>
                                                                )}
                                                            </div>
                                                        </div>
                                                    )}
                                                </div>
                                            ) : (
                                                <div className="pt-4 border-t border-white/5 text-center text-slate-500 text-sm">
                                                    {fetchingInsights ? 'Analyzing taste...' : 'Waiting for insights...'}
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div >
        </div >
    );
}
