import Header from "./Header";

function Layout({ sidebar, children }) {
  return (
    <div className="app-shell">
      <Header />
      <div className="app-body">
        {sidebar}
        <main className="app-main">
          <div className="app-main-inner">{children}</div>
        </main>
      </div>
    </div>
  );
}

export default Layout;
