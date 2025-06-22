import { useQuery } from "@tanstack/react-query";
import { QUERY_KEYS } from "../config/api.config";

import { analyticsApiClient } from "../services/AnalyticsApi.client";
import type { AnalyticsData } from "../types/Analytics.types";

export const useAnalytics = () => {
	return useQuery({
		queryKey: QUERY_KEYS.ANALYTICS,
		queryFn: async (): Promise<AnalyticsData> => {
			const [uniqueBuyers, loyalCustomers, topSellingProducts] =
				await Promise.all([
					analyticsApiClient.getUniqueBuyers(),
					analyticsApiClient.getLoyalCustomers(),
					analyticsApiClient.getTopSellingProducts(),
				]);

			return {
				uniqueBuyers: uniqueBuyers.data,
				loyalCustomers: loyalCustomers.data,
				topSellingProducts: topSellingProducts.data,
			};
		},
		staleTime: 2 * 60 * 1000,
		retry: 3,
		refetchInterval: 5 * 60 * 1000,
	});
};
