/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/
import {useState, ReactNode} from 'react';

// --- SVG Icons ---

const BeakerIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M4.5 3h15M6 3v12c0 3.3 2.7 6 6 6s6-2.7 6-6V3M6 12h12"/></svg>
);

const BellIcon = ({className = ''}: {className?: string}) => (
    <svg className={className} xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
);

const PlusIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
);

const UserIcon = ({className = ''}: {className?: string}) => (
    <svg className={className} xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
);

const LeafIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M11 20A7 7 0 0 1 4 13H2a10 10 0 0 0 10 10zM2 11h2a7 7 0 0 1 7-7V2a10 10 0 0 0-9 9z"/></svg>
);
const SunIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
);
const BoxIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
);
const ArrowLeftIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
);
const MapPinIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
);
const ChevronRightIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
);
const CheckCircleIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
);
const AlertTriangleIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
);



// --- Reusable Components ---
const WidgetCard = ({ title, children, className = '' }: { title: string, children: ReactNode, className?: string }) => (
  <div className={`widget-card ${className}`}>
    <h3>{title}</h3>
    <div className="widget-content">
      {children}
    </div>
  </div>
);


// --- Admin Dashboard Components ---

const FilterPanel = () => (
    <aside className="filter-panel">
        <h2>Filter Panel</h2>
        <div className="filters">
            <select aria-label="Filter by 7076">
                <option>7076</option>
            </select>
            <select aria-label="Filter by All">
                <option>All</option>
            </select>
            <select aria-label="Filter by All">
                <option>All</option>
            </select>
            <label htmlFor="compliance-status">Compliance Status</label>
            <select id="compliance-status">
                <option>All</option>
            </select>
        </div>
    </aside>
);

const HomePage = () => (
    <div className="grid-container">
        <WidgetCard title="Harvest Events" className="harvest-events">
            <div className="stat-number">150</div>
            <div className="bar-chart">
               {Array.from({ length: 12 }).map((_, i) => <div key={i} className="bar" style={{ height: `${20 + Math.random() * 60}%` }}></div>)}
            </div>
        </WidgetCard>
        <WidgetCard title="Processing Overview" className="processing-overview">
            <div className="stepper">
               <div className="step active"><span>Harvesting</span></div>
               <div className="step active"><span>Drying</span></div>
               <div className="step"><span>Grinding</span></div>
               <div className="step"><span>Grinding</span></div>
               <div className="step"><span>Packaging</span></div>
            </div>
        </WidgetCard>
        <WidgetCard title="Quality Tests" className="quality-tests">
           <div className="quality-status passed">Passed (333)</div>
           <div className="quality-status failed">Failed (20)</div>
        </WidgetCard>
        <WidgetCard title="Compliance Status" className="compliance-status">
            <ul>
                <li><span className="dot compliant"></span>Compliant <span className="value">82</span></li>
                <li><span className="dot non-compliant"></span>Non-Complaint <span className="value">12</span></li>
                <li><span className="dot pending"></span>Pending <span className="value">34</span></li>
            </ul>
        </WidgetCard>
         <WidgetCard title="Network Health" className="network-health">
            <div className="health-charts">
               <div className="line-chart-placeholder"></div>
               <div className="bar-chart-placeholder"></div>
               <div className="gauge-chart-placeholder"></div>
            </div>
        </WidgetCard>
        <WidgetCard title="Reports" className="reports">
            <button className="generate-btn">Generate Reports</button>
        </WidgetCard>
    </div>
);

const ReportsPage = () => (
    <div className="reports-page">
        <div className="page-header">
            <h2>Reports & Analytics</h2>
            <div className="date-picker">
                <label htmlFor="date-range">Date Range:</label>
                <input type="text" id="date-range" defaultValue="Oct 1, 2025 - Oct 31, 2025" readOnly />
            </div>
        </div>
        <div className="reports-grid">
            <WidgetCard title="Compliance Reports" className="report-download">
                <p>Monthly and quarterly compliance summaries, including all regulatory checks.</p>
                <button>Download PDF</button>
            </WidgetCard>
            <WidgetCard title="Harvest Yield Analysis" className="report-download">
                <p>Detailed analysis of harvest yields by region, farm, and time period.</p>
                <button>Download CSV</button>
            </WidgetCard>
             <WidgetCard title="Quality Test Summaries" className="report-download">
                <p>Aggregated results from all lab tests, highlighting pass/fail rates.</p>
                <button>Download PDF</button>
            </WidgetCard>
            <WidgetCard title="Batch Traceability Report" className="report-chart">
                <h4>Full Journey for Batch #AWR-7076</h4>
                <div className="chart-placeholder"></div>
                <p>Visual timeline of the selected batch from farm to package.</p>
            </WidgetCard>
        </div>
    </div>
);

const SettingsPage = () => {
    const [complianceAlerts, setComplianceAlerts] = useState(true);
    const [harvestAlerts, setHarvestAlerts] = useState(false);

    return (
        <div className="settings-page">
            <div className="page-header">
                <h2>System Settings</h2>
            </div>
            <div className="settings-content">
                <div className="settings-section">
                    <h3>Profile</h3>
                    <div className="form-group">
                        <label htmlFor="admin-name">Name</label>
                        <input type="text" id="admin-name" defaultValue="Admin User" />
                    </div>
                    <div className="form-group">
                        <label htmlFor="admin-email">Email</label>
                        <input type="email" id="admin-email" defaultValue="admin@ayurherb.io" />
                    </div>
                </div>
                <div className="settings-section">
                    <h3>Notifications</h3>
                    <div className="form-group">
                        <div className="toggle-switch">
                            <label htmlFor="compliance-alerts">Compliance Alerts</label>
                            <label className="toggle-container">
                                <input
                                    type="checkbox"
                                    id="compliance-alerts"
                                    checked={complianceAlerts}
                                    onChange={(e) => setComplianceAlerts(e.target.checked)}
                                />
                                <span className="slider"></span>
                            </label>
                        </div>
                        <p className="setting-description">Receive email notifications for any compliance issues.</p>
                    </div>
                    <div className="form-group">
                        <div className="toggle-switch">
                            <label htmlFor="harvest-alerts">New Harvest Events</label>
                            <label className="toggle-container">
                                <input
                                    type="checkbox"
                                    id="harvest-alerts"
                                    checked={harvestAlerts}
                                    onChange={(e) => setHarvestAlerts(e.target.checked)}
                                />
                                <span className="slider"></span>
                            </label>
                        </div>
                        <p className="setting-description">Get notified when a new harvest is logged in the system.</p>
                    </div>
                </div>
                <div className="settings-section">
                    <h3>API & Integrations</h3>
                    <div className="form-group">
                        <label htmlFor="api-key">API Key</label>
                        <input type="text" id="api-key" defaultValue="ahb_sk_******************" readOnly />
                    </div>
                    <button className="secondary-btn">Regenerate Key</button>
                </div>
                <div className="settings-actions">
                    <button className="save-btn">Save Changes</button>
                </div>
            </div>
        </div>
    );
};


type AdminPage = 'home' | 'reports' | 'settings';

const AdminDashboard = () => {
    const [activePage, setActivePage] = useState<AdminPage>('home');
    
    return (
    <div className="admin-dashboard">
        <header className="dashboard-header">
            <h1>Dashboard</h1>
            <nav>
                <a href="#" className={activePage === 'home' ? 'active' : ''} onClick={(e) => { e.preventDefault(); setActivePage('home'); }}>Home</a>
                <a href="#" className={activePage === 'reports' ? 'active' : ''} onClick={(e) => { e.preventDefault(); setActivePage('reports'); }}>Reports</a>
                <a href="#" className={activePage === 'settings' ? 'active' : ''} onClick={(e) => { e.preventDefault(); setActivePage('settings'); }}>Settings</a>
                <button className="export-btn">Export</button>
            </nav>
        </header>
        <div className="dashboard-main">
            <FilterPanel />
            <section className="dashboard-content">
                {activePage === 'home' && <HomePage />}
                {activePage === 'reports' && <ReportsPage />}
                {activePage === 'settings' && <SettingsPage />}
            </section>
        </div>
    </div>
    );
};


// --- Farmer DApp Components ---

const DAppHomePage = () => (
    <>
        <section className="dapp-section">
            <h4>Farm Map</h4>
            <div className="farm-map-placeholder"></div>
        </section>
        <section className="dapp-section">
            <h4>Lab tests</h4>
            <div className="lab-tests">
                <div className="test-icon"><BeakerIcon /></div>
                <div className="test-icon"><BeakerIcon /></div>
                <div className="test-icon"><BeakerIcon /></div>
                <div className="test-icon"><BeakerIcon /></div>
            </div>
        </section>
         <section className="dapp-section">
            <h4>Recent Entries</h4>
            <ul className="recent-entries">
                <li className="entry">
                    <div className="entry-icon"></div>
                    <div className="entry-details">
                        <p>Herb Name</p>
                        <span>Geo location</span>
                    </div>
                    <div className="entry-status">
                        <span>12/10/2025</span>
                        <span className="status-passed">Test Passed</span>
                    </div>
                </li>
                <li className="entry">
                    <div className="entry-icon"></div>
                    <div className="entry-details">
                        <p>Herb Name</p>
                        <span>Geo location</span>
                    </div>
                    <div className="entry-status">
                        <span>12/10/2025</span>
                        <span className="status-passed">Test Passed</span>
                    </div>
                </li>
                 <li className="entry">
                    <div className="entry-icon"></div>
                    <div className="entry-details">
                        <p>Herb Name</p>
                        <span>Geo location</span>
                    </div>
                    <div className="entry-status">
                        <span>12/10/2025</span>
                        <span className="status-passed">Test Passed</span>
                    </div>
                </li>
            </ul>
        </section>
    </>
);

const DAppNewEntry = ({ onBack }: { onBack: () => void }) => (
    <div className="dapp-form-container">
        <form>
            <div className="dapp-form-group">
                <label htmlFor="herb-name">Herb Name</label>
                <input type="text" id="herb-name" className="dapp-input" placeholder="e.g., Ashwagandha" />
            </div>
            <div className="dapp-form-group">
                <label htmlFor="harvest-date">Harvest Date</label>
                <input type="date" id="harvest-date" className="dapp-input" />
            </div>
            <div className="dapp-form-group">
                 <label>Location</label>
                 <button type="button" className="dapp-location-btn">
                    <MapPinIcon /> Get Current Location
                 </button>
            </div>
            <div className="dapp-form-group">
                <label>Photo</label>
                <div className="dapp-file-upload">
                    <p>Tap to upload a photo</p>
                    <input type="file" />
                </div>
            </div>
            <div className="dapp-btn-group">
                 <button type="button" className="dapp-submit-btn" onClick={onBack}>Submit Entry</button>
            </div>
        </form>
    </div>
);

const DAppNotifications = () => (
    <div className="notifications-page">
        <ul className="notifications-list">
            <li className="notification-item success">
                <div className="notification-icon"><CheckCircleIcon /></div>
                <div className="notification-content">
                    <p>Lab test results for Batch #AWR-7076 are in: <strong>Passed</strong></p>
                    <span>2 hours ago</span>
                </div>
            </li>
             <li className="notification-item warning">
                <div className="notification-icon"><AlertTriangleIcon /></div>
                <div className="notification-content">
                    <p>Compliance documentation for Q3 is due next week.</p>
                    <span>1 day ago</span>
                </div>
            </li>
            <li className="notification-item success">
                <div className="notification-icon"><CheckCircleIcon /></div>
                <div className="notification-content">
                    <p>New harvest of Tulsi successfully logged.</p>
                    <span>3 days ago</span>
                </div>
            </li>
        </ul>
    </div>
);

const DAppProfile = () => (
    <div className="profile-page">
        <div className="profile-card">
            <div className="profile-avatar"></div>
            <h3>R. K. Sharma</h3>
            <p>Farm ID: F-JPR-045</p>
        </div>
        <div className="profile-menu">
            <ul>
                <li><a href="#">Edit Profile <ChevronRightIcon /></a></li>
                <li><a href="#">Farm Settings <ChevronRightIcon /></a></li>
                <li><a href="#">Help & Support <ChevronRightIcon /></a></li>
                <li><a href="#" className="logout">Logout</a></li>
            </ul>
        </div>
    </div>
);


type DAppPage = 'home' | 'newEntry' | 'notifications' | 'profile';
const pageTitles: Record<DAppPage, string> = {
    home: 'DApp',
    newEntry: 'New Harvest Entry',
    notifications: 'Notifications',
    profile: 'Profile & Settings',
};

const FarmerDApp = () => {
    const [activePage, setActivePage] = useState<DAppPage>('home');

    return (
        <div className="mobile-view-container">
          <div className="mobile-view">
            <header className="dapp-header">
                {activePage === 'newEntry' && (
                    <button className="back-btn" onClick={() => setActivePage('home')}><ArrowLeftIcon /></button>
                )}
                <h2>{pageTitles[activePage]}</h2>
            </header>
            <main className="dapp-main">
                {activePage === 'home' && <DAppHomePage />}
                {activePage === 'newEntry' && <DAppNewEntry onBack={() => setActivePage('home')} />}
                {activePage === 'notifications' && <DAppNotifications />}
                {activePage === 'profile' && <DAppProfile />}
            </main>
            <footer className="dapp-footer">
                <button aria-label="Notifications" onClick={() => setActivePage('notifications')}>
                    <BellIcon className={activePage === 'notifications' ? 'active' : ''}/>
                </button>
                <button aria-label="Add new entry" className="add-btn" onClick={() => setActivePage('newEntry')}>
                    <PlusIcon />
                </button>
                <button aria-label="Profile" onClick={() => setActivePage('profile')}>
                    <UserIcon className={activePage === 'profile' ? 'active' : ''}/>
                </button>
            </footer>
          </div>
        </div>
    );
};


// --- Customer View Components ---
const CustomerView = () => {
    const [scanned, setScanned] = useState(false);

    if (!scanned) {
        return (
            <div className="customer-view">
                <div className="qr-scanner">
                    <h2>Trace Your Herb</h2>
                    <p>Scan the QR code on your product to see its journey.</p>
                    <button className="scan-btn" onClick={() => setScanned(true)}>
                        Simulate QR Scan
                    </button>
                </div>
            </div>
        );
    }
    
    return (
        <div className="customer-view">
            <div className="product-journey">
                <header className="journey-header">
                    <h2>Ashwagandha Root Powder</h2>
                    <p>Batch #AWR-7076</p>
                </header>
                <div className="timeline">
                    <div className="timeline-item">
                        <div className="timeline-icon"><LeafIcon/></div>
                        <div className="timeline-content">
                            <h3>Harvested</h3>
                            <p>October 12, 2025</p>
                            <span>Jaipur, Rajasthan</span>
                        </div>
                    </div>
                    <div className="timeline-item">
                        <div className="timeline-icon"><SunIcon/></div>
                        <div className="timeline-content">
                            <h3>Sun Dried</h3>
                            <p>October 14, 2025</p>
                            <span>Processing Unit, Jaipur</span>
                        </div>
                    </div>
                     <div className="timeline-item">
                        <div className="timeline-icon"><BeakerIcon/></div>
                        <div className="timeline-content">
                            <h3>Lab Tested for Quality</h3>
                            <p>October 18, 2025</p>
                            <span className="status-passed">Purity Test Passed</span>
                        </div>
                    </div>
                    <div className="timeline-item">
                        <div className="timeline-icon"><BoxIcon/></div>
                        <div className="timeline-content">
                            <h3>Packaged</h3>
                            <p>October 20, 2025</p>
                            <span>AyurHerb Facility</span>
                        </div>
                    </div>
                </div>
                 <WidgetCard title="Product Details" className="product-details-card">
                    <ul>
                        <li><strong>Harvest Date:</strong> <span>Oct 12, 2025</span></li>
                        <li><strong>Origin:</strong> <span>Jaipur, Rajasthan</span></li>
                        <li><strong>Quality Test:</strong> <span className="status-passed">Passed</span></li>
                        <li><strong>Farmer:</strong> <span>R. K. Sharma</span></li>
                    </ul>
                </WidgetCard>
            </div>
        </div>
    );
};


// --- Main App Component with View Switcher ---
type View = 'admin' | 'farmer' | 'customer';

function App() {
  const [currentView, setCurrentView] = useState<View>('admin');

  return (
    <div className="app-container">
      <div className="view-switcher">
        <button className={currentView === 'admin' ? 'active' : ''} onClick={() => setCurrentView('admin')}>Admin Dashboard</button>
        <button className={currentView === 'farmer' ? 'active' : ''} onClick={() => setCurrentView('farmer')}>Farmer DApp</button>
        <button className={currentView === 'customer' ? 'active' : ''} onClick={() => setCurrentView('customer')}>Customer View</button>
      </div>
      {currentView === 'admin' && <AdminDashboard />}
      {currentView === 'farmer' && <FarmerDApp />}
      {currentView === 'customer' && <CustomerView />}
    </div>
  );
}

export default App;