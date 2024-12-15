import React, { useState } from 'react';

const ArticleSubmissionForm = () => {
  const [page, setPage] = useState(1);
  const [errors, setErrors] = useState({});
  const [formData, setFormData] = useState({
    title: '',
    subtitle: '',
    content: '',
    authorName: '',
    email: '',
    image: null,
    tags: [],
    category: '',
    publishDate: '',
    agreeToTerms: false
  });

  const categories = ['News', 'Opinion', 'Feature'];
  const availableTags = ['Politics', 'Sports', 'Tech', 'Entertainment', 'Science'];

  const validatePage1 = () => {
    const newErrors = {};

    if (formData.title.length < 10) {
      newErrors.title = 'Title must be at least 10 characters long';
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    if (!formData.authorName.trim()) {
      newErrors.authorName = 'Author name is required';
    }

    if (!formData.content.trim()) {
      newErrors.content = 'Article content is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const validatePage2 = () => {
    const newErrors = {};

    if (!formData.category) {
      newErrors.category = 'Please select a category';
    }

    const selectedDate = new Date(formData.publishDate);
    const today = new Date();
    if (selectedDate <= today) {
      newErrors.publishDate = 'Publish date must be in the future';
    }

    if (!formData.agreeToTerms) {
      newErrors.agreeToTerms = 'You must agree to the terms';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value, type, checked, files } = e.target;

    if (type === 'checkbox' && name === 'tags') {
      const updatedTags = formData.tags.includes(value)
        ? formData.tags.filter(tag => tag !== value)
        : [...formData.tags, value];
      setFormData(prev => ({ ...prev, tags: updatedTags }));
    } else if (type === 'checkbox') {
      setFormData(prev => ({ ...prev, [name]: checked }));
    } else if (type === 'file') {
      setFormData(prev => ({ ...prev, [name]: files[0] }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleNext = () => {
    if (validatePage1()) {
      setPage(2);
    }
  };

  const handlePrevious = () => {
    setPage(1);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validatePage2()) {
      console.log('Form submitted:', formData);
      // Handle form submission here
    }
  };

  const ErrorMessage = ({ error }) => (
    error ? <p className="text-red-500 text-sm mt-1">{error}</p> : null
  );

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="bg-white shadow-md rounded-lg px-8 py-6">
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              Submit Article - Page {page} of 2
            </h2>
            <div className="w-full bg-gray-200 rounded-full h-2.5">
              <div
                className="bg-blue-600 h-2.5 rounded-full transition-all duration-300"
                style={{ width: page === 1 ? '50%' : '100%' }}
              ></div>
            </div>
          </div>

          <form onSubmit={handleSubmit}>
            {page === 1 ? (
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Title
                  </label>
                  <input
                    type="text"
                    placeholder='Here..'
                    name="title"
                    value={formData.title}
                    onChange={handleChange}

                    className="mt-1 block w-full border-b border-gray-600 outline-none shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  />
                  <ErrorMessage error={errors.title} />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Subtitle
                  </label>
                  <input
                    type="text"
                    placeholder='Here..'
                    name="subtitle"
                    value={formData.subtitle}
                    onChange={handleChange}
                    className="mt-1 block w-full border-b border-gray-600 outline-none shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Article Content
                  </label>
                  <textarea
                    name="content"
                    value={formData.content}
                    onChange={handleChange}
                    rows="6"
                    className="mt-1 block w-full border outline-none rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  />
                  <ErrorMessage error={errors.content} />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Author Name
                  </label>
                  <input
                    type="text"
                    placeholder='Here..'
                    name="authorName"
                    value={formData.authorName}
                    onChange={handleChange}
                    className="mt-1 block w-full border-b border-gray-600 outline-none shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  />
                  <ErrorMessage error={errors.authorName} />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Email Address
                  </label>
                  <input
                    type="email"
                    placeholder='someone@example.com'
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    className="mt-1 block w-full border-b border-gray-600 outline-none shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  />
                  <ErrorMessage error={errors.email} />
                </div>

                <div className="flex justify-end">
                  <button
                    type="button"
                    onClick={handleNext}
                    className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                  >
                    Next
                  </button>
                </div>
              </div>
            ) : (
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Article Image
                  </label>
                  <input
                    type="file"
                    name="image"
                    onChange={handleChange}
                    accept="image/*"
                    className="mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Tags
                  </label>
                  <div className="space-y-2">
                    {availableTags.map(tag => (
                      <label key={tag} className="flex items-center">
                        <input
                          type="checkbox"
                          name="tags"
                          value={tag}
                          checked={formData.tags.includes(tag)}
                          onChange={handleChange}
                          className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                        />
                        <span className="ml-2 text-gray-700">{tag}</span>
                      </label>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Category
                  </label>
                  <select
                    name="category"
                    value={formData.category}
                    onChange={handleChange}
                    className="mt-1 block w-full p-2 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  >
                    <option value="">Select a category</option>
                    {categories.map(category => (
                      <option key={category} value={category}>
                        {category}
                      </option>
                    ))}
                  </select>
                  <ErrorMessage error={errors.category} />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Publish Date
                  </label>
                  <input
                    type="date"
                    name="publishDate"
                    value={formData.publishDate}
                    onChange={handleChange}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  />
                  <ErrorMessage error={errors.publishDate} />
                </div>

                <div>
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      name="agreeToTerms"
                      checked={formData.agreeToTerms}
                      onChange={handleChange}
                      className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                    <span className="ml-2 text-sm text-gray-700">
                      I agree to the terms and conditions
                    </span>
                  </label>
                  <ErrorMessage error={errors.agreeToTerms} />
                </div>

                <div className="flex justify-between">
                  <button
                    type="button"
                    onClick={handlePrevious}
                    className="bg-gray-200 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
                  >
                    Previous
                  </button>
                  <button
                    type="submit"
                    className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                  >
                    Submit
                  </button>
                </div>
              </div>
            )}
          </form>
        </div>
      </div>
    </div>
  );
};

export default ArticleSubmissionForm;