import React from "react";
import styles from "./AnalyticsCard.module.css";

interface AnalyticsCardProps {
	title: string;
	value: number;
	trend?: {
		value: number;
		isPositive: boolean;
	};
}

export const AnalyticsCard: React.FC<AnalyticsCardProps> = ({
	title,
	value = 0,
	trend,
}) => {
	return (
		<div className={styles.card}>
			<h3 className={styles.title}>{title}</h3>
			<p className={styles.value}>{value ? value.toLocaleString() : "N/A"}</p>
			{trend && (
				<div
					className={`${styles.trend} ${
						trend.isPositive ? styles.positive : styles.negative
					}`}
				>
					{trend.isPositive ? "↗" : "↘"} {Math.abs(trend.value)}%
				</div>
			)}
		</div>
	);
};
