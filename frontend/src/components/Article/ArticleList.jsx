import { ChevronLeft, ChevronRight } from 'lucide-react';
import { Fragment, useEffect, useState } from 'react';
import { getArticles } from '../../api/services/articles.service';
import ArticleCard from './ArticleCard';

const ArticlesList = () => {
  const [currentPage, setCurrentPage] = useState(1);
  const [allArticles, setAllArticles] = useState([]);
  const articlesPerPage = 6;

  // Sample articles data
  // const articles = [
  //   {
  //     id: 1,
  //     title: "Getting Started with React Hooks",
  //     excerpt: "Learn how to use React Hooks to manage state and side effects in your functional components.",
  //     author: "Jane Smith",
  //     date: "Dec 16, 2024",
  //     readTime: "5 min read",
  //     category: "React",
  //     imageUrl: "https://i.pinimg.com/736x/8f/cf/82/8fcf82c7e11c6a9296438d2564fde3e4.jpg"
  //   },
  //   {
  //     id: 2,
  //     title: "Understanding TypeScript Generics",
  //     excerpt: "Deep dive into TypeScript generics and how they can make your code more reusable and type-safe.",
  //     author: "John Doe",
  //     date: "Dec 15, 2024",
  //     readTime: "7 min read",
  //     category: "TypeScript",
  //     imageUrl: "https://i.pinimg.com/736x/8f/cf/82/8fcf82c7e11c6a9296438d2564fde3e4.jpg"
  //   },
  //   {
  //     id: 3,
  //     title: "CSS Grid Layout Mastery",
  //     excerpt: "Master CSS Grid Layout with practical examples and best practices for modern web layouts.",
  //     author: "Sarah Johnson",
  //     date: "Dec 14, 2024",
  //     readTime: "6 min read",
  //     category: "CSS",
  //     imageUrl: "https://i.pinimg.com/736x/8f/cf/82/8fcf82c7e11c6a9296438d2564fde3e4.jpg"
  //   },
  //   {
  //     id: 4,
  //     title: "Next.js Server Components",
  //     excerpt: "Explore the power of Next.js Server Components and how they can improve your app's performance.",
  //     author: "Mike Wilson",
  //     date: "Dec 13, 2024",
  //     readTime: "8 min read",
  //     category: "Next.js",
  //     imageUrl: "https://i.pinimg.com/736x/8f/cf/82/8fcf82c7e11c6a9296438d2564fde3e4.jpg"
  //   },
  //   {
  //     id: 5,
  //     title: "State Management with Redux Toolkit",
  //     excerpt: "Learn how to efficiently manage state in your React applications using Redux Toolkit.",
  //     author: "Emily Brown",
  //     date: "Dec 12, 2024",
  //     readTime: "10 min read",
  //     category: "Redux",
  //     imageUrl: "https://i.pinimg.com/736x/8f/cf/82/8fcf82c7e11c6a9296438d2564fde3e4.jpg"
  //   },
  //   {
  //     id: 6,
  //     title: "Tailwind CSS Best Practices",
  //     excerpt: "Discover the best practices and techniques for building efficient UIs with Tailwind CSS.",
  //     author: "Alex Chen",
  //     date: "Dec 11, 2024",
  //     readTime: "6 min read",
  //     category: "CSS",
  //     imageUrl: "https://i.pinimg.com/736x/8f/cf/82/8fcf82c7e11c6a9296438d2564fde3e4.jpg"
  //   },
  //   {
  //     id: 7,
  //     title: "Advanced Git Workflows",
  //     excerpt: "Master advanced Git workflows and improve your team's collaboration process.",
  //     author: "Chris Taylor",
  //     date: "Dec 10, 2024",
  //     readTime: "9 min read",
  //     category: "Git",
  //     imageUrl: "https://i.pinimg.com/736x/8f/cf/82/8fcf82c7e11c6a9296438d2564fde3e4.jpg"
  //   }
  // ];

  const totalPages = Math.ceil(allArticles.length / articlesPerPage);
  const indexOfLastArticle = currentPage * articlesPerPage;
  const indexOfFirstArticle = indexOfLastArticle - articlesPerPage;
  const currentArticles = allArticles.slice(indexOfFirstArticle, indexOfLastArticle);

  const paginate = (pageNumber) => {
    if (pageNumber >= 1 && pageNumber <= totalPages) {
      setCurrentPage(pageNumber);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const getAllArticlesHandler = async () => {
    const response = await getArticles();
    console.log(response);
    setAllArticles(response.data);
  };

  useEffect(() => {
    getAllArticlesHandler();
  }, []);

  return (
    <Fragment>
      {allArticles.length === 0 ? (
        <div className='my-4 bg-red-200 rounded-md p-5 flex flex-col justify-center items-center'>
          <span className='text-2xl font-bold'>🥺 Sorry!!</span>
          <span>Articles are not available</span>
        </div>
      ) : (
        <Fragment>
          <div className="max-w-7xl mx-auto px-4 py-8">
            {/* Articles Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
              {currentArticles.map((article) => (
                <ArticleCard key={article.id} {...article} />
              ))}
            </div>

            {/* Pagination */}
            <div className="flex justify-center items-center gap-2">
              <button
                onClick={() => paginate(currentPage - 1)}
                disabled={currentPage === 1}
                className="p-2 rounded-lg hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <ChevronLeft className="w-5 h-5" />
              </button>

              {[...Array(totalPages)].map((_, index) => (
                <button
                  key={index}
                  onClick={() => paginate(index + 1)}
                  className={`w-8 h-8 rounded-lg flex items-center justify-center transition-colors ${currentPage === index + 1
                    ? 'bg-blue-500 text-white'
                    : 'hover:bg-gray-100'
                    }`}
                >
                  {index + 1}
                </button>
              ))}

              <button
                onClick={() => paginate(currentPage + 1)}
                disabled={currentPage === totalPages}
                className="p-2 rounded-lg hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <ChevronRight className="w-5 h-5" />
              </button>
            </div>
          </div>
        </Fragment>
      )}
    </Fragment>
  );
};

export default ArticlesList;