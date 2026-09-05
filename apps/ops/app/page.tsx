import styles from '../styles/page.module.css';

const dashboardCards = [
  { label: 'Bookings Today', value: '12', style: styles.cardHighlight },
  { label: 'Upcoming Arrivals', value: '27', style: styles.cardStandard },
  { label: 'Revenue', value: '$42,300', style: styles.cardStandard },
  { label: 'Balance Due', value: '$9,800', style: styles.cardHighlight }
];

export default function OpsHome() {
  return (
    <div className={styles.container}>
      <aside className={styles.sidebar}>
        <div className={styles.brand}>Volcan Ops</div>
        <nav className={styles.nav}>
          <a className={styles.navLink} href="#">Dashboard</a>
          <a className={styles.navLink} href="#">Bookings</a>
          <a className={styles.navLink} href="#">Customers</a>
          <a className={styles.navLink} href="#">Trips</a>
          <a className={styles.navLink} href="#">Suppliers</a>
          <a className={styles.navLink} href="#">Reports</a>
          <a className={styles.navLink} href="#">Settings</a>
        </nav>
      </aside>
      <main className={styles.main}>
        <header className={styles.header}>
          <div>
            <h1>Operations Dashboard</h1>
            <p>Internal Volcan Vacations operations shell placeholder.</p>
          </div>
          <div className={styles.headerMeta}>Ready</div>
        </header>
        <section className={styles.summaryGrid}>
          {dashboardCards.map((card) => (
            <article key={card.label} className={`${styles.card} ${card.style}`}>
              <span>{card.label}</span>
              <strong>{card.value}</strong>
            </article>
          ))}
        </section>
        <section className={styles.contentRow}>
          <div className={styles.panel}>
            <h2>Upcoming Bookings</h2>
            <ul>
              <li>Tour group arriving 2026-09-05</li>
              <li>Private transfer confirmed 2026-09-07</li>
              <li>Hotel check-in 2026-09-10</li>
            </ul>
          </div>
          <div className={styles.panel}>
            <h2>Needs Attention</h2>
            <ul>
              <li>Pending payment for trip #1024</li>
              <li>Supplier contract upload required</li>
              <li>Customer profile missing passport info</li>
            </ul>
          </div>
        </section>
      </main>
    </div>
  );
}
