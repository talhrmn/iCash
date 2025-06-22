import React from "react";
import styles from "./LoadingSpinner.module.css";

interface LoadingSpinnerProps {
	message?: string;
	size?: "small" | "medium" | "large";
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
	message = "Loading...",
	size = "medium",
}) => {
	return (
		<div className={`${styles.container} ${styles[size]}`}>
			<div className={styles.spinner} />
			<p className={styles.message}>{message}</p>
		</div>
	);
};
