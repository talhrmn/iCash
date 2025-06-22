import axios, { type AxiosInstance, type AxiosResponse } from "axios";
import { getApiUrl } from "../config/api.config";
import type {
	LoyalCustomersResponse,
	TopSellingProductsResponse,
	UniqueBuyersResponse,
} from "../types/Analytics.types";
import { handleApiError } from "../config/api.config";

const analyticsApi = axios.create({
	timeout: 10000,
	headers: {
		"Content-Type": "application/json",
	},
});

analyticsApi.interceptors.response.use((response) => response, handleApiError);

export class AnalyticsApi {
	private api: AxiosInstance;

	constructor() {
		this.api = analyticsApi;
	}

	public getUniqueBuyers(): Promise<AxiosResponse<UniqueBuyersResponse>> {
		return this.api.get(getApiUrl("ANALYTICS", "/unique-buyers"));
	}

	public getLoyalCustomers(): Promise<AxiosResponse<LoyalCustomersResponse>> {
		return this.api.get(getApiUrl("ANALYTICS", "/loyal-customers"));
	}

	public getTopSellingProducts(): Promise<
		AxiosResponse<TopSellingProductsResponse>
	> {
		return this.api.get(getApiUrl("ANALYTICS", "/top-selling-products"));
	}
}

export const analyticsApiClient = new AnalyticsApi();
