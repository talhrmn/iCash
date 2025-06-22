import { QueryClientProvider } from "@tanstack/react-query";
import React from "react";

import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import styles from "./App.module.css";
import { Analytics } from "./components/Analytics/Analytics";
import { PurchaseForm } from "./components/PurchaseForm/PurchaseForm";
import { queryClient } from "./services/query.client";

const App: React.FC = () => {
	return (
		<QueryClientProvider client={queryClient}>
			<div className={styles.layout}>
				<header className={styles.header}>
					<h1>iCash</h1>
				</header>
				<main className={styles.content}>
					<div className={styles.container}>
						<div className={styles.grid}>
							<section className={styles.analyticsSection}>
								<Analytics />
							</section>
							<aside className={styles.purchaseSection}>
								<PurchaseForm />
							</aside>
						</div>
					</div>
				</main>
			</div>

			{/* Development tools - remove in production */}
			{import.meta.env.VITE_APP_ENV === "development" && <ReactQueryDevtools />}
		</QueryClientProvider>
	);
};

export default App;
