// ... existing imports ...

export default function Layout({ children }) {
    // ... existing code ...

    return (
        <div className="app-layout">
            <Header />
            <Sidebar />
            <main>
                {children}
            </main>
        </div>
    );

    // ... rest of component ...
}