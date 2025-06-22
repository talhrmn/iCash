import axios, { type AxiosInstance, type AxiosResponse } from "axios";
import { getApiUrl } from "../config/api.config";
import type {
	Branch,
	Product,
	PurchaseRequest,
} from "../types/CashRegister.types";
import { handleApiError } from "../config/api.config";

const cashRegisterApi = axios.create({
	timeout: 10000,
	headers: {
		"Content-Type": "application/json",
	},
});

cashRegisterApi.interceptors.response.use(
	(response) => response,
	handleApiError
);

export class CashRegisterApi {
	private api: AxiosInstance;

	constructor() {
		this.api = cashRegisterApi;
	}

	public getBranches(): Promise<AxiosResponse<Branch[]>> {
		return this.api.get(getApiUrl("CASH_REGISTER", "/branch"));
	}

	public getProducts(): Promise<AxiosResponse<Product[]>> {
		return this.api.get(getApiUrl("CASH_REGISTER", "/product"));
	}

	public createPurchase(data: PurchaseRequest): Promise<AxiosResponse<any>> {
		return this.api.post(getApiUrl("CASH_REGISTER", "/purchase"), data);
	}
}

export const cashRegisterApiClient = new CashRegisterApi();
