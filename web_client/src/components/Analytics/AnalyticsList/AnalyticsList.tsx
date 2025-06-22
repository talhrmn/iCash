import React from "react";
import styles from "./AnalyticsList.module.css";

interface AnalyticsListProps<T> {
	title: string;
	items?: T[];
	renderItem: (item: T) => React.ReactNode;
	emptyMessage?: string;
}

export const AnalyticsList = <T,>({
	title,
	items,
	renderItem,
	emptyMessage = "No data available",
}: AnalyticsListProps<T>) => {
	return (
		<div className={styles.container}>
			<h3 className={styles.title}>{title}</h3>
			{items && items.length > 0 ? (
				<ul className={styles.list}>
					{(items || []).map((item, index) => (
						<li key={index} className={styles.listItem}>
							{renderItem(item)}
						</li>
					))}
				</ul>
			) : (
				<p className={styles.emptyMessage}>{emptyMessage}</p>
			)}
		</div>
	);
};
