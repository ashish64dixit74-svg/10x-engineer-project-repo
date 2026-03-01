import styles from "./Layout.module.css";

function Layout({ children }) {
  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1>PromptLab</h1>
      </header>

      <main className={styles.main}>
        {children}
      </main>
    </div>
  );
}

export default Layout;