import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Shield,
  ShieldAlert,
  ShieldCheck,
  TrendingUp,
  DollarSign,
  History,
  User,
  LogOut,
  Key,
  RefreshCw,
  Lock,
  PlusCircle,
  CheckCircle,
  XCircle,
  Info,
  Sliders,
  Mail,
  UserCheck,
  CreditCard,
  Building,
  AlertTriangle
} from 'lucide-react';
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid
} from 'recharts';

const API_BASE_URL = 'http://localhost:8000/api';

export default function App() {
  // Auth state
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [user, setUser] = useState(JSON.parse(localStorage.getItem('user')) || null);
  
  // Navigation
  const [currentPage, setCurrentPage] = useState('dashboard');
  
  // Login / Register Form states
  const [isLoginTab, setIsLoginTab] = useState(true);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('user');
  const [authError, setAuthError] = useState('');
  const [authSuccess, setAuthSuccess] = useState('');
  
  // Simulation Form states
  const [cardNumber, setCardNumber] = useState('');
  const [amount, setAmount] = useState('');
  const [merchant, setMerchant] = useState('');
  const [profile, setProfile] = useState('genuine');
  const [simError, setSimError] = useState('');
  const [simLoading, setSimLoading] = useState(false);
  const [predictionResult, setPredictionResult] = useState(null);

  // History & Metrics states
  const [history, setHistory] = useState([]);
  const [metrics, setMetrics] = useState({
    total_count: 0,
    approved_count: 0,
    review_count: 0,
    blocked_count: 0,
    total_amount: 0,
    fraud_rate_pct: 0,
    status_distribution: []
  });
  const [loadingHistory, setLoadingHistory] = useState(false);
  const [historyError, setHistoryError] = useState('');

  // Configure Axios default headers when token changes
  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      localStorage.setItem('token', token);
      fetchUserData();
    } else {
      delete axios.defaults.headers.common['Authorization'];
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      setUser(null);
      setCurrentPage('login');
    }
  }, [token]);

  // Fetch metrics and history on state update
  useEffect(() => {
    if (token && currentPage !== 'login') {
      fetchMetrics();
      fetchHistory();
    }
  }, [token, currentPage]);

  const fetchUserData = async () => {
    try {
      const res = await axios.get(`${API_BASE_URL}/auth/me`);
      setUser(res.data);
      localStorage.setItem('user', JSON.stringify(res.data));
    } catch (err) {
      handleAuthFailure();
    }
  };

  const handleAuthFailure = () => {
    setToken('');
    setUser(null);
    setAuthError('Session expired or unauthorized. Please log in.');
    setCurrentPage('login');
  };

  const fetchMetrics = async () => {
    try {
      const res = await axios.get(`${API_BASE_URL}/transactions/metrics`);
      setMetrics(res.data);
    } catch (err) {
      console.error('Failed to load metrics:', err);
    }
  };

  const fetchHistory = async () => {
    setLoadingHistory(true);
    try {
      const res = await axios.get(`${API_BASE_URL}/transactions/history`);
      setHistory(res.data);
      setHistoryError('');
    } catch (err) {
      setHistoryError('Failed to retrieve history logs.');
      console.error(err);
    } finally {
      setLoadingHistory(false);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setAuthError('');
    setAuthSuccess('');
    try {
      const res = await axios.post(`${API_BASE_URL}/auth/login`, { username, password });
      setToken(res.data.access_token);
      setUsername('');
      setPassword('');
      setCurrentPage('dashboard');
    } catch (err) {
      setAuthError(err.response?.data?.detail || 'Incorrect username or password.');
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setAuthError('');
    setAuthSuccess('');
    try {
      await axios.post(`${API_BASE_URL}/auth/register`, { username, email, password, role });
      setAuthSuccess('Account registered successfully! You can now log in.');
      setIsLoginTab(true);
      setEmail('');
      setPassword('');
    } catch (err) {
      setAuthError(err.response?.data?.detail || 'Registration failed. Check your inputs.');
    }
  };

  const handleSimulationSubmit = async (e) => {
    e.preventDefault();
    setSimError('');
    setPredictionResult(null);
    setSimLoading(true);
    
    try {
      const res = await axios.post(`${API_BASE_URL}/transactions/predict`, {
        card_number: cardNumber,
        amount: parseFloat(amount),
        merchant,
        profile
      });
      
      setPredictionResult(res.data);
      // Reset form on success
      setCardNumber('');
      setAmount('');
      setMerchant('');
      
      // Update global states
      fetchMetrics();
      fetchHistory();
    } catch (err) {
      setSimError(err.response?.data?.detail || 'Simulation prediction request failed.');
    } finally {
      setSimLoading(false);
    }
  };

  const handleAdminOverride = async (id, status) => {
    try {
      await axios.patch(`${API_BASE_URL}/transactions/${id}/override?target_status=${status}`);
      fetchMetrics();
      fetchHistory();
    } catch (err) {
      alert('Override action failed: ' + (err.response?.data?.detail || 'Unknown error'));
    }
  };

  const logout = () => {
    setToken('');
    setUser(null);
    setCurrentPage('login');
  };

  const COLORS = ['#10b981', '#f59e0b', '#f43f5e'];

  // ----------------------------------------------------
  // RENDER INTERFACE - AUTH/LOGIN VIEW
  // ----------------------------------------------------
  if (!token) {
    return (
      <div className="min-h-screen bg-dark-950 flex flex-col justify-center items-center px-4 relative overflow-hidden select-none">
        {/* Dynamic Background Gradients */}
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl -z-10 animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-violet-600/10 rounded-full blur-3xl -z-10 animate-pulse"></div>

        {/* Branding Title */}
        <div className="flex items-center space-x-3 mb-8">
          <div className="p-3 bg-cyan-500/10 rounded-2xl border border-cyan-500/30 shadow-[0_0_15px_rgba(6,182,212,0.2)]">
            <Shield className="w-8 h-8 text-cyan-400" />
          </div>
          <div>
            <h1 className="text-3xl font-extrabold tracking-wider bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
              FRAUD<span className="text-cyan-400">SHIELD</span>
            </h1>
            <p className="text-xs text-slate-400 font-medium tracking-widest uppercase">AI Transaction Audit Suite</p>
          </div>
        </div>

        {/* Auth Box Container */}
        <div className="w-full max-w-md glass-panel-glow rounded-3xl p-8 border border-slate-800">
          <div className="flex space-x-4 mb-6 border-b border-slate-800 pb-2">
            <button
              onClick={() => { setIsLoginTab(true); setAuthError(''); setAuthSuccess(''); }}
              className={`flex-1 pb-3 text-sm font-semibold border-b-2 transition-all ${
                isLoginTab ? 'text-cyan-400 border-cyan-400' : 'text-slate-400 border-transparent hover:text-slate-200'
              }`}
            >
              Sign In
            </button>
            <button
              onClick={() => { setIsLoginTab(false); setAuthError(''); setAuthSuccess(''); }}
              className={`flex-1 pb-3 text-sm font-semibold border-b-2 transition-all ${
                !isLoginTab ? 'text-cyan-400 border-cyan-400' : 'text-slate-400 border-transparent hover:text-slate-200'
              }`}
            >
              Register
            </button>
          </div>

          {authError && (
            <div className="p-3 mb-4 bg-rose-500/10 border border-rose-500/30 rounded-xl flex items-center space-x-2 text-rose-400 text-xs">
              <ShieldAlert className="w-4 h-4 flex-shrink-0" />
              <span>{authError}</span>
            </div>
          )}

          {authSuccess && (
            <div className="p-3 mb-4 bg-emerald-500/10 border border-emerald-500/30 rounded-xl flex items-center space-x-2 text-emerald-400 text-xs">
              <CheckCircle className="w-4 h-4 flex-shrink-0" />
              <span>{authSuccess}</span>
            </div>
          )}

          {isLoginTab ? (
            <form onSubmit={handleLogin} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-2 uppercase tracking-wide">Username or Email</label>
                <div className="relative">
                  <User className="absolute left-3.5 top-3.5 w-4 h-4 text-slate-500" />
                  <input
                    type="text"
                    required
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Enter admin or user"
                    className="w-full bg-slate-900/60 border border-slate-800 rounded-xl py-3 pl-10 pr-4 text-sm text-slate-200 placeholder:text-slate-500 cyan-glow-focus transition-all"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-2 uppercase tracking-wide">Password</label>
                <div className="relative">
                  <Lock className="absolute left-3.5 top-3.5 w-4 h-4 text-slate-500" />
                  <input
                    type="password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Enter admin123 or user123"
                    className="w-full bg-slate-900/60 border border-slate-800 rounded-xl py-3 pl-10 pr-4 text-sm text-slate-200 placeholder:text-slate-500 cyan-glow-focus transition-all"
                  />
                </div>
              </div>

              <button
                type="submit"
                className="w-full py-3.5 mt-2 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-bold rounded-xl text-sm shadow-[0_4px_20px_rgba(6,182,212,0.25)] hover:shadow-[0_4px_20px_rgba(6,182,212,0.4)] transition-all flex justify-center items-center space-x-2"
              >
                <span>Authorize Login</span>
              </button>
            </form>
          ) : (
            <form onSubmit={handleRegister} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-2 uppercase tracking-wide">Username</label>
                <div className="relative">
                  <User className="absolute left-3.5 top-3.5 w-4 h-4 text-slate-500" />
                  <input
                    type="text"
                    required
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Create a username"
                    className="w-full bg-slate-900/60 border border-slate-800 rounded-xl py-3 pl-10 pr-4 text-sm text-slate-200 placeholder:text-slate-500 cyan-glow-focus transition-all"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-2 uppercase tracking-wide">Email Address</label>
                <div className="relative">
                  <Mail className="absolute left-3.5 top-3.5 w-4 h-4 text-slate-500" />
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Enter email address"
                    className="w-full bg-slate-900/60 border border-slate-800 rounded-xl py-3 pl-10 pr-4 text-sm text-slate-200 placeholder:text-slate-500 cyan-glow-focus transition-all"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-2 uppercase tracking-wide">Password</label>
                <div className="relative">
                  <Lock className="absolute left-3.5 top-3.5 w-4 h-4 text-slate-500" />
                  <input
                    type="password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="At least 6 characters"
                    className="w-full bg-slate-900/60 border border-slate-800 rounded-xl py-3 pl-10 pr-4 text-sm text-slate-200 placeholder:text-slate-500 cyan-glow-focus transition-all"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-2 uppercase tracking-wide">System Role Mapping</label>
                <div className="relative">
                  <UserCheck className="absolute left-3.5 top-3.5 w-4 h-4 text-slate-500" />
                  <select
                    value={role}
                    onChange={(e) => setRole(e.target.value)}
                    className="w-full bg-slate-900/60 border border-slate-800 rounded-xl py-3 pl-10 pr-4 text-sm text-slate-200 cyan-glow-focus transition-all appearance-none"
                  >
                    <option value="user">Standard User (Compliance Evaluator)</option>
                    <option value="admin">System Administrator (Full Overrides)</option>
                  </select>
                </div>
              </div>

              <button
                type="submit"
                className="w-full py-3.5 mt-2 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-bold rounded-xl text-sm shadow-[0_4px_20px_rgba(6,182,212,0.25)] hover:shadow-[0_4px_20px_rgba(6,182,212,0.4)] transition-all"
              >
                Create Account
              </button>
            </form>
          )}
          
          <div className="mt-6 pt-4 border-t border-slate-900 text-center text-xs text-slate-500 font-medium">
            FraudShield Dev Seed Environment V1.0.0
          </div>
        </div>
      </div>
    );
  }

  // ----------------------------------------------------
  // RENDER INTERFACE - MAIN SYSTEM PANEL
  // ----------------------------------------------------
  return (
    <div className="min-h-screen bg-dark-950 flex flex-col md:flex-row relative">
      {/* Sidebar Navigation */}
      <aside className="w-full md:w-64 bg-slate-900/40 border-r border-slate-800/80 flex flex-col justify-between flex-shrink-0">
        <div>
          {/* Header Brand */}
          <div className="p-6 border-b border-slate-900 flex items-center space-x-2.5">
            <div className="p-2 bg-cyan-500/10 rounded-xl border border-cyan-500/30">
              <Shield className="w-5 h-5 text-cyan-400" />
            </div>
            <div>
              <h2 className="text-xl font-bold tracking-wide text-white">
                FRAUD<span className="text-cyan-400">SHIELD</span>
              </h2>
              <p className="text-[10px] text-slate-500 uppercase tracking-widest font-semibold">Real-Time Core</p>
            </div>
          </div>

          {/* User Badge Profile */}
          {user && (
            <div className="p-5 mx-4 my-4 bg-slate-900/70 border border-slate-800/60 rounded-2xl flex items-center space-x-3">
              <div className="p-2.5 bg-gradient-to-br from-slate-800 to-slate-700 rounded-xl border border-slate-700">
                <User className="w-4 h-4 text-cyan-300" />
              </div>
              <div className="overflow-hidden">
                <h4 className="text-xs font-bold text-slate-200 truncate">{user.username}</h4>
                <div className="flex items-center space-x-1 mt-1">
                  <span className={`px-2 py-0.5 rounded-full text-[9px] font-bold uppercase ${
                    user.role === 'admin' 
                      ? 'bg-violet-500/10 border border-violet-500/30 text-violet-400 shadow-[0_0_10px_rgba(139,92,246,0.1)]' 
                      : 'bg-cyan-500/10 border border-cyan-500/30 text-cyan-400'
                  }`}>
                    {user.role}
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* Sidebar Nav Links */}
          <nav className="px-4 space-y-1.5">
            <button
              onClick={() => setCurrentPage('dashboard')}
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-sm font-semibold transition-all ${
                currentPage === 'dashboard'
                  ? 'bg-cyan-500/10 border-l-4 border-cyan-400 text-cyan-300'
                  : 'text-slate-400 hover:bg-slate-900/50 hover:text-slate-200 border-l-4 border-transparent'
              }`}
            >
              <TrendingUp className="w-4 h-4" />
              <span>Metrics Console</span>
            </button>

            <button
              onClick={() => setCurrentPage('simulate')}
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-sm font-semibold transition-all ${
                currentPage === 'simulate'
                  ? 'bg-cyan-500/10 border-l-4 border-cyan-400 text-cyan-300'
                  : 'text-slate-400 hover:bg-slate-900/50 hover:text-slate-200 border-l-4 border-transparent'
              }`}
            >
              <Sliders className="w-4 h-4" />
              <span>Predict Simulator</span>
            </button>

            <button
              onClick={() => setCurrentPage('history')}
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-sm font-semibold transition-all ${
                currentPage === 'history'
                  ? 'bg-cyan-500/10 border-l-4 border-cyan-400 text-cyan-300'
                  : 'text-slate-400 hover:bg-slate-900/50 hover:text-slate-200 border-l-4 border-transparent'
              }`}
            >
              <History className="w-4 h-4" />
              <span>Audit Ledger</span>
            </button>
          </nav>
        </div>

        {/* Sidebar Footer Logout */}
        <div className="p-4 border-t border-slate-900">
          <button
            onClick={logout}
            className="w-full flex items-center justify-between px-4 py-3 bg-slate-900/80 border border-slate-800/80 hover:bg-slate-800/50 text-slate-300 hover:text-rose-400 text-sm font-semibold rounded-xl transition-all"
          >
            <span>Exit Session</span>
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 p-6 md:p-8 overflow-y-auto max-w-7xl">
        
        {/* =================================------------------
            PAGE VIEW: DASHBOARD
            =================================------------------ */}
        {currentPage === 'dashboard' && (
          <div className="space-y-6">
            {/* Page Header */}
            <div>
              <h1 className="text-3xl font-extrabold text-white tracking-wide">Metrics Telemetry</h1>
              <p className="text-sm text-slate-400 mt-1">Real-time fraud audit analytics and statistical probability models.</p>
            </div>

            {/* KPI Metrics Cards Grid */}
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="glass-panel p-5 rounded-2xl relative overflow-hidden">
                <div className="absolute top-0 right-0 w-24 h-24 bg-cyan-500/5 rounded-full blur-2xl"></div>
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Total Evaluated</span>
                  <div className="p-2 bg-cyan-500/10 rounded-lg"><PlusCircle className="w-4 h-4 text-cyan-400" /></div>
                </div>
                <h3 className="text-2xl font-extrabold mt-4 text-white">{metrics.total_count}</h3>
                <p className="text-[10px] text-slate-500 font-semibold mt-1">Transactions Evaluated</p>
              </div>

              <div className="glass-panel p-5 rounded-2xl relative overflow-hidden">
                <div className="absolute top-0 right-0 w-24 h-24 bg-emerald-500/5 rounded-full blur-2xl"></div>
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Approved</span>
                  <div className="p-2 bg-emerald-500/10 rounded-lg"><ShieldCheck className="w-4 h-4 text-emerald-400" /></div>
                </div>
                <h3 className="text-2xl font-extrabold mt-4 text-white">{metrics.approved_count}</h3>
                <p className="text-[10px] text-slate-500 font-semibold mt-1">Low-Risk Transactions</p>
              </div>

              <div className="glass-panel p-5 rounded-2xl relative overflow-hidden">
                <div className="absolute top-0 right-0 w-24 h-24 bg-rose-500/5 rounded-full blur-2xl"></div>
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Blocked</span>
                  <div className="p-2 bg-rose-500/10 rounded-lg"><XCircle className="w-4 h-4 text-rose-400" /></div>
                </div>
                <h3 className="text-2xl font-extrabold mt-4 text-white">{metrics.blocked_count}</h3>
                <p className="text-[10px] text-slate-500 font-semibold mt-1">Identified Fraud Attempts</p>
              </div>

              <div className="glass-panel p-5 rounded-2xl relative overflow-hidden">
                <div className="absolute top-0 right-0 w-24 h-24 bg-amber-500/5 rounded-full blur-2xl"></div>
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Fraud Rate</span>
                  <div className="p-2 bg-amber-500/10 rounded-lg"><AlertTriangle className="w-4 h-4 text-amber-400" /></div>
                </div>
                <h3 className="text-2xl font-extrabold mt-4 text-white">{metrics.fraud_rate_pct}%</h3>
                <p className="text-[10px] text-slate-500 font-semibold mt-1">Blocked vs Total Volume</p>
              </div>
            </div>

            {/* Volume Aggregate Panel */}
            <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex items-center justify-between">
              <div>
                <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Total Audited Volume</span>
                <h2 className="text-3xl font-extrabold mt-2 text-transparent bg-gradient-to-r from-white via-slate-100 to-slate-400 bg-clip-text">
                  ${metrics.total_amount.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                </h2>
              </div>
              <div className="p-4 bg-cyan-500/10 border border-cyan-500/20 rounded-2xl">
                <DollarSign className="w-8 h-8 text-cyan-400" />
              </div>
            </div>

            {/* Charts Row Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              {/* Pie Chart: Status Distribution */}
              <div className="glass-panel p-6 rounded-2xl border border-slate-800 lg:col-span-5 flex flex-col justify-between">
                <h3 className="text-lg font-bold text-white mb-4">Risk Profile Distribution</h3>
                <div className="h-64 flex justify-center items-center">
                  {metrics.total_count === 0 ? (
                    <div className="text-center text-xs text-slate-500 flex flex-col items-center">
                      <Info className="w-8 h-8 text-slate-600 mb-2" />
                      No transaction metadata recorded.
                    </div>
                  ) : (
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={metrics.status_distribution}
                          cx="50%"
                          cy="50%"
                          innerRadius={60}
                          outerRadius={80}
                          paddingAngle={5}
                          dataKey="value"
                        >
                          {metrics.status_distribution.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                          ))}
                        </Pie>
                        <Tooltip contentStyle={{ background: '#0f172a', borderColor: '#1e293b', borderRadius: '12px' }} />
                        <Legend verticalAlign="bottom" height={36} />
                      </PieChart>
                    </ResponsiveContainer>
                  )}
                </div>
              </div>

              {/* Bar Chart: Recent History Distribution */}
              <div className="glass-panel p-6 rounded-2xl border border-slate-800 lg:col-span-7 flex flex-col justify-between">
                <h3 className="text-lg font-bold text-white mb-4">Recent Core Transactions History</h3>
                <div className="h-64 flex justify-center items-center">
                  {history.length === 0 ? (
                    <div className="text-center text-xs text-slate-500 flex flex-col items-center">
                      <Info className="w-8 h-8 text-slate-600 mb-2" />
                      No evaluated transaction data available.
                    </div>
                  ) : (
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={history.slice(0, 10).reverse()}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                        <XAxis dataKey="merchant" stroke="#475569" fontSize={10} tickLine={false} />
                        <YAxis stroke="#475569" fontSize={10} tickLine={false} />
                        <Tooltip 
                          contentStyle={{ background: '#0f172a', borderColor: '#1e293b', borderRadius: '12px' }}
                          formatter={(value) => [`$${value}`, 'Amount']}
                        />
                        <Bar dataKey="amount" radius={[4, 4, 0, 0]}>
                          {history.slice(0, 10).reverse().map((entry, index) => {
                            let fill = '#10b981';
                            if (entry.status === 'REVIEW') fill = '#f59e0b';
                            if (entry.status === 'BLOCKED') fill = '#f43f5e';
                            return <Cell key={`cell-${index}`} fill={fill} />;
                          })}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* =================================------------------
            PAGE VIEW: PREDICT SIMULATOR
            =================================------------------ */}
        {currentPage === 'simulate' && (
          <div className="space-y-6">
            <div>
              <h1 className="text-3xl font-extrabold text-white tracking-wide">Predictive Audit Sandbox</h1>
              <p className="text-sm text-slate-400 mt-1">Submit high-volume transaction variables to trigger XGBoost classifiers and security policy checks.</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
              {/* Submission Form */}
              <div className="glass-panel p-6 rounded-3xl border border-slate-800/80 lg:col-span-5">
                <h3 className="text-lg font-bold text-white mb-5 flex items-center space-x-2">
                  <CreditCard className="w-5 h-5 text-cyan-400" />
                  <span>Ingestion Engine</span>
                </h3>

                {simError && (
                  <div className="p-3 mb-4 bg-rose-500/10 border border-rose-500/30 rounded-xl flex items-center space-x-2 text-rose-400 text-xs">
                    <ShieldAlert className="w-4 h-4 flex-shrink-0" />
                    <span>{simError}</span>
                  </div>
                )}

                <form onSubmit={handleSimulationSubmit} className="space-y-4">
                  <div>
                    <label className="block text-xs font-semibold text-slate-400 mb-2 uppercase tracking-wide">Credit Card Number</label>
                    <div className="relative">
                      <CreditCard className="absolute left-3.5 top-3.5 w-4 h-4 text-slate-500" />
                      <input
                        type="text"
                        required
                        value={cardNumber}
                        onChange={(e) => setCardNumber(e.target.value)}
                        placeholder="e.g. 4111 2222 3333 4444"
                        className="w-full bg-slate-900/60 border border-slate-800 rounded-xl py-3 pl-10 pr-4 text-sm text-slate-200 placeholder:text-slate-500 cyan-glow-focus transition-all"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-400 mb-2 uppercase tracking-wide">Merchant Agency</label>
                    <div className="relative">
                      <Building className="absolute left-3.5 top-3.5 w-4 h-4 text-slate-500" />
                      <input
                        type="text"
                        required
                        value={merchant}
                        onChange={(e) => setMerchant(e.target.value)}
                        placeholder="e.g. Stripe Gateway, Amazon Inc"
                        className="w-full bg-slate-900/60 border border-slate-800 rounded-xl py-3 pl-10 pr-4 text-sm text-slate-200 placeholder:text-slate-500 cyan-glow-focus transition-all"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-400 mb-2 uppercase tracking-wide">Transaction Amount ($)</label>
                    <div className="relative">
                      <DollarSign className="absolute left-3.5 top-3.5 w-4 h-4 text-slate-500" />
                      <input
                        type="number"
                        step="0.01"
                        required
                        value={amount}
                        onChange={(e) => setAmount(e.target.value)}
                        placeholder="0.00"
                        className="w-full bg-slate-900/60 border border-slate-800 rounded-xl py-3 pl-10 pr-4 text-sm text-slate-200 placeholder:text-slate-500 cyan-glow-focus transition-all"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-400 mb-2 uppercase tracking-wide">ML Simulation Profile</label>
                    <div className="relative">
                      <Sliders className="absolute left-3.5 top-3.5 w-4 h-4 text-slate-500" />
                      <select
                        value={profile}
                        onChange={(e) => setProfile(e.target.value)}
                        className="w-full bg-slate-900/60 border border-slate-800 rounded-xl py-3 pl-10 pr-4 text-sm text-slate-200 cyan-glow-focus transition-all appearance-none"
                      >
                        <option value="genuine">Genuine Profile (Normal PCA space)</option>
                        <option value="suspicious">Suspicious Profile (Medium Risk space)</option>
                        <option value="fraudulent">Fraudulent Profile (Blocked PCA space)</option>
                      </select>
                    </div>
                  </div>

                  <button
                    type="submit"
                    disabled={simLoading}
                    className="w-full py-3.5 mt-2 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-bold rounded-xl text-sm shadow-[0_4px_20px_rgba(6,182,212,0.25)] transition-all flex justify-center items-center space-x-2"
                  >
                    {simLoading ? (
                      <>
                        <RefreshCw className="w-4 h-4 animate-spin" />
                        <span>Processing Neural Audit...</span>
                      </>
                    ) : (
                      <>
                        <Shield className="w-4 h-4" />
                        <span>Execute Prediction Engine</span>
                      </>
                    )}
                  </button>
                </form>
              </div>

              {/* Simulation Result Panel */}
              <div className="lg:col-span-7 space-y-4">
                {predictionResult ? (
                  <div className="glass-panel p-6 rounded-3xl border border-slate-800 relative overflow-hidden">
                    {/* Visual Backdrop Rings */}
                    <div className={`absolute top-0 right-0 w-32 h-32 rounded-full blur-3xl -z-10 opacity-30 ${
                      predictionResult.status === 'APPROVED' ? 'bg-emerald-500' :
                      predictionResult.status === 'REVIEW' ? 'bg-amber-500' : 'bg-rose-500'
                    }`}></div>

                    <h3 className="text-xl font-bold text-white mb-4">Inference Response Result</h3>
                    
                    <div className="flex items-center space-x-4 mb-6">
                      <div className={`p-4 rounded-2xl border ${
                        predictionResult.status === 'APPROVED' ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400' :
                        predictionResult.status === 'REVIEW' ? 'bg-amber-500/10 border-amber-500/30 text-amber-400' :
                        'bg-rose-500/10 border-rose-500/30 text-rose-400'
                      }`}>
                        {predictionResult.status === 'APPROVED' ? <ShieldCheck className="w-8 h-8" /> :
                         predictionResult.status === 'REVIEW' ? <AlertTriangle className="w-8 h-8" /> :
                         <XCircle className="w-8 h-8" />}
                      </div>
                      <div>
                        <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Evaluation Audit status</span>
                        <h2 className={`text-2xl font-extrabold tracking-wide uppercase ${
                          predictionResult.status === 'APPROVED' ? 'text-emerald-400' :
                          predictionResult.status === 'REVIEW' ? 'text-amber-400' :
                          'text-rose-400'
                        }`}>
                          {predictionResult.status}
                        </h2>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4 border-t border-slate-800/80 pt-4 mb-6">
                      <div>
                        <span className="text-[10px] text-slate-500 font-bold uppercase tracking-widest">Fraud Probability</span>
                        <h3 className="text-2xl font-extrabold text-white mt-1">
                          {(predictionResult.prediction.probability * 100.0).toFixed(2)}%
                        </h3>
                      </div>
                      <div>
                        <span className="text-[10px] text-slate-500 font-bold uppercase tracking-widest">Model Version</span>
                        <h3 className="text-2xl font-extrabold text-slate-300 mt-1">
                          {predictionResult.prediction.model_version}
                        </h3>
                      </div>
                    </div>

                    {/* Feature Weight Logs */}
                    <div className="bg-slate-950/80 border border-slate-900 rounded-2xl p-4">
                      <div className="flex items-center space-x-2 text-slate-400 text-xs font-bold mb-3 uppercase tracking-wider">
                        <Info className="w-4 h-4 text-cyan-400" />
                        <span>PCA Feature Dimensions Log</span>
                      </div>
                      
                      <div className="max-h-36 overflow-y-auto grid grid-cols-3 gap-2 pr-1">
                        {predictionResult.prediction.features && 
                          Object.entries(predictionResult.prediction.features)
                            .filter(([key]) => key.startsWith('V'))
                            .slice(0, 15)
                            .map(([key, val]) => (
                              <div key={key} className="bg-slate-900/60 border border-slate-850 p-2 rounded-xl text-center">
                                <span className="text-[10px] text-slate-500 font-bold block">{key}</span>
                                <span className={`text-xs font-semibold ${
                                  val < -2.0 ? 'text-rose-400' : val > 2.0 ? 'text-emerald-400' : 'text-slate-300'
                                }`}>
                                  {val.toFixed(4)}
                                </span>
                              </div>
                            ))}
                      </div>
                      <div className="text-[9px] text-slate-600 font-medium mt-3 text-center">
                        V1-V28 vectors derived from PCA projections. Shifted properties denote covariance models.
                      </div>
                    </div>

                  </div>
                ) : (
                  <div className="glass-panel p-8 rounded-3xl border border-slate-800 flex flex-col items-center justify-center h-full text-center text-slate-500 min-h-[300px]">
                    <Sliders className="w-12 h-12 text-slate-700 mb-3 animate-pulse" />
                    <h3 className="text-lg font-bold text-slate-400">Awaiting Simulation Ingestion</h3>
                    <p className="text-xs text-slate-500 max-w-sm mt-1">Fill out the ingestion sandbox form to test card inputs and evaluate rule engines.</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* =================================------------------
            PAGE VIEW: AUDIT LEDGER (HISTORY)
            =================================------------------ */}
        {currentPage === 'history' && (
          <div className="space-y-6">
            <div className="flex justify-between items-center flex-wrap gap-4">
              <div>
                <h1 className="text-3xl font-extrabold text-white tracking-wide">Audit Ledger</h1>
                <p className="text-sm text-slate-400 mt-1">Comprehensive trace audits and historical logs of neural evaluations.</p>
              </div>
              <button
                onClick={fetchHistory}
                className="px-4 py-2.5 bg-slate-900 border border-slate-800 hover:bg-slate-800 text-slate-300 text-xs font-bold rounded-xl transition-all flex items-center space-x-1.5"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                <span>Reload Ledger</span>
              </button>
            </div>

            {historyError && (
              <div className="p-3 bg-rose-500/10 border border-rose-500/30 rounded-xl flex items-center space-x-2 text-rose-400 text-xs">
                <ShieldAlert className="w-4 h-4 flex-shrink-0" />
                <span>{historyError}</span>
              </div>
            )}

            {/* Audit Table Grid */}
            <div className="glass-panel rounded-3xl border border-slate-850 overflow-hidden">
              {loadingHistory ? (
                <div className="p-12 text-center text-slate-500 text-xs flex flex-col items-center">
                  <RefreshCw className="w-8 h-8 animate-spin text-cyan-400 mb-3" />
                  Accessing core database transaction stacks...
                </div>
              ) : history.length === 0 ? (
                <div className="p-12 text-center text-slate-500 text-xs flex flex-col items-center">
                  <Info className="w-8 h-8 text-slate-600 mb-3" />
                  No transactions registered. Go to the simulator to generate database logs.
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full text-left border-collapse">
                    <thead>
                      <tr className="bg-slate-900/60 border-b border-slate-800/80 text-[10px] font-bold uppercase tracking-wider text-slate-400">
                        <th className="py-4 px-6">Timestamp</th>
                        <th className="py-4 px-6">Card Segment</th>
                        <th className="py-4 px-6">Merchant</th>
                        <th className="py-4 px-6">Amount</th>
                        <th className="py-4 px-6">Neural Risk</th>
                        <th className="py-4 px-6 text-center">Status Flag</th>
                        {user && user.role === 'admin' && <th className="py-4 px-6 text-center">Security Overrides</th>}
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-850/60 text-slate-300 text-xs">
                      {history.map((row) => (
                        <tr key={row.id} className="hover:bg-slate-900/30 transition-all">
                          <td className="py-4 px-6 font-medium text-slate-400 whitespace-nowrap">
                            {new Date(row.created_at).toLocaleString()}
                          </td>
                          <td className="py-4 px-6 font-mono font-semibold tracking-wider text-slate-200">
                            {row.card_number}
                          </td>
                          <td className="py-4 px-6 font-semibold text-slate-100">
                            {row.merchant}
                          </td>
                          <td className="py-4 px-6 font-extrabold text-slate-200">
                            ${row.amount.toFixed(2)}
                          </td>
                          <td className="py-4 px-6 font-semibold text-slate-400">
                            {row.prediction ? `${(row.prediction.probability * 100.0).toFixed(1)}%` : 'N/A'}
                          </td>
                          <td className="py-4 px-6 text-center whitespace-nowrap">
                            <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold uppercase ${
                              row.status === 'APPROVED' ? 'bg-emerald-500/10 border border-emerald-500/20 text-emerald-400' :
                              row.status === 'REVIEW' ? 'bg-amber-500/10 border border-amber-500/20 text-amber-400' :
                              'bg-rose-500/10 border border-rose-500/20 text-rose-400'
                            }`}>
                              {row.status}
                            </span>
                          </td>
                          {user && user.role === 'admin' && (
                            <td className="py-4 px-6 text-center whitespace-nowrap">
                              {row.status === 'APPROVED' ? (
                                <button
                                  onClick={() => handleAdminOverride(row.id, 'BLOCKED')}
                                  className="px-2 py-1 bg-rose-500/10 hover:bg-rose-500/20 border border-rose-500/30 text-rose-400 font-bold rounded-lg text-[10px] transition-all"
                                >
                                  Override to Block
                                </button>
                              ) : (
                                <button
                                  onClick={() => handleAdminOverride(row.id, 'APPROVED')}
                                  className="px-2 py-1 bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/30 text-emerald-400 font-bold rounded-lg text-[10px] transition-all"
                                >
                                  Override to Approve
                                </button>
                              )}
                            </td>
                          )}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        )}

      </main>
    </div>
  );
}
