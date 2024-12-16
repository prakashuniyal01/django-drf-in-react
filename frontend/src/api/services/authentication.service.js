import { AuthEndpoints } from "../constants";
import { http } from "../https";

export const userLoginApiService = async (data) => {
  const response = await http.post(AuthEndpoints.login, data);
  return response.data;
};

export const userRegisterApiService = async (data) => {
  const response = await http.post(AuthEndpoints.register, data);
  return response.data;
};