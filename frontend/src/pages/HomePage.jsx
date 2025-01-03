import { Fragment, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import ArticlesList from "../components/Article/ArticleList";
import CategoryTagForm from "../components/CategoryAndTagForm";
import HeroSection from "../components/HeroSection";

const HomePage = () => {

  const navigator = useNavigate();

  useEffect(() => {
    const userToken = localStorage.getItem('token');
    const userInfo = localStorage.getItem('userInfo');

    if (userToken && userInfo) {
      navigator("/admin");
    }

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <Fragment>
      <section className="w-full">
        <div className="w-[100%]">
          <HeroSection />
        </div>
        <div className="w-full flex justify-center items-center flex-col my-3 mt-3">
          <div className="my-3">
            <h1 className="text-3xl">Search Articles</h1>
          </div>
          <div className="w-full">
            <CategoryTagForm />
          </div>
        </div>
        <div className="flex justify-center items-center flex-col">
          <h1 className="text-2xl text-start w-[88%] px-5 bg-blue-100">Articles</h1>
          <div className="articleContainer ">
            <ArticlesList />
          </div>
        </div>
      </section>
    </Fragment>
  );
};

export default HomePage;
