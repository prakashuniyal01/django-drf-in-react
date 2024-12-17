import { ArticleEndpoints } from "../constants";
import { http } from "../https";

export const getArticles = () => {
  return http.get(ArticleEndpoints.list);
};

export const getSingleArticle = (id) => {
  return http.get(ArticleEndpoints.detail.replace("{id}", id));
};