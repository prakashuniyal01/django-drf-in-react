/* eslint-disable react/prop-types */
import { ArrowRight, Clock, User } from 'lucide-react';
import { Fragment } from 'react';

const ArticleCard = (props) => {
  return (
    <Fragment>
      <article className="max-w-sm bg-white rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition-shadow duration-300">
        {/* Image */}
        <div className="relative">
          <img
            src={props.imageUrl}
            alt={props.title}
            className="w-full h-48 object-cover"
          />
          <span className="absolute top-4 left-4 bg-blue-500 text-white text-sm px-3 py-1 rounded-full">
            {props.category}
          </span>
        </div>

        {/* Content */}
        <div className="p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-2 line-clamp-2">
            {props.title}
          </h2>

          <p className="text-gray-600 mb-4 line-clamp-3">
            {props.excerpt}
          </p>

          {/* Meta information */}
          <div className="flex items-center gap-4 text-sm text-gray-500 mb-4">
            <div className="flex items-center gap-1">
              <User size={16} />
              <span>{props.author}</span>
            </div>
            <div className="flex items-center gap-1">
              <Clock size={16} />
              <span>{props.readTime}</span>
            </div>
          </div>

          {/* Date and Read More */}
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-500">{props.date}</span>
            <button className="flex items-center gap-1 text-blue-500 hover:text-blue-600 transition-colors">
              Read More
              <ArrowRight size={16} />
            </button>
          </div>
        </div>
      </article>
    </Fragment>
  );
};

export default ArticleCard;