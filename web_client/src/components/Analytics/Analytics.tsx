import React from "react";
import { useAnalytics } from "../../hooks/useAnalyticsApi";
import type {
	LoyalCustomer,
	TopSellingProduct,
} from "../../types/Analytics.types";
import { ErrorMessage } from "../ui/ErrorMessage/ErrorMessage";
import { LoadingSpinner } from "../ui/LoadingSpinner/LoadingSpinner";
import styles from "./Analytics.module.css";
import { AnalyticsCard } from "./AnalyticsCard/AnalyticsCard";
import { AnalyticsList } from "./AnalyticsList/AnalyticsList";
import { toTitleCase } from "../../utils/formatters";

export const Analytics: React.FC = () => {
	const { data, isLoading, error } = useAnalytics();

	if (isLoading) {
		return <LoadingSpinner message="Loading analytics..." />;
	}

	if (error) {
		return <ErrorMessage message="Error loading analytics" />;
	}

	if (!data) {
		return null;
	}

	return (
		<div className={styles.analytics}>
			<div className={styles.grid}>
				<AnalyticsCard
					title="Unique Buyers"
					value={data.uniqueBuyers.unique_buyers_count}
				/>
				<AnalyticsCard
					title="Loyal Customers"
					value={data.loyalCustomers.total_loyal_customers}
				/>
			</div>

			<div className={styles.detailsGrid}>
				<AnalyticsList
					title="Top Loyal Customers"
					items={data.loyalCustomers.loyal_customers.slice(0, 3)}
					renderItem={(customer: LoyalCustomer) => (
						<div>
							<span>{customer.user_id}</span>
							<span>{customer.purchase_count} purchases</span>
						</div>
					)}
				/>
				<AnalyticsList
					title="Top Selling Products"
					items={data.topSellingProducts.top_selling_products}
					renderItem={(product: TopSellingProduct) => (
						<div>
							<span>{toTitleCase(product.product_name)}</span>
							<span>{product.total_sold} sold</span>
						</div>
					)}
				/>
			</div>
		</div>
	);
};
