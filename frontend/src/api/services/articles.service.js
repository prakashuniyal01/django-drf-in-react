import { ArticleEndpoints } from "../constants";
import { http } from "../https";

export const getArticles = () => {
  return http.get(ArticleEndpoints.list);
};

export const getSingleArticle = (id) => {
  return http.get(ArticleEndpoints.detail.replace("{id}", id));
};

export const createArticle = (data, token) => {
  const config = {
    headers: {
      "Content-Type": "multipart/form-data",
      Authorization: `Bearer ${token}`,
    },
  };

  return http.post(ArticleEndpoints.create, data, config);
}; 