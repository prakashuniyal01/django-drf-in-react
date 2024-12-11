├── /src
│   ├── /assets                # Static assets like images, fonts, etc.
│   ├── /components            # Reusable components
│   │   ├── /Form              # For form-related components
│   │   │   ├── ArticleForm.js # Main form component for article submission
│   │   │   ├── Page1.js       # Page 1 of the form
│   │   │   └── Page2.js       # Page 2 of the form
│   │   ├── /Article           # Components related to articles
│   │   │   ├── ArticleCard.js # Component to display individual article info
│   │   │   └── ArticleList.js # Component to list all articles
│   │   └── /Auth              # Components for authentication (login, register, etc.)
│   │       ├── Login.js       # Login form
│   │       └── Register.js    # Registration form
│   ├── /context               # Context API for state management (like user authentication)
│   │   ├── AuthContext.js     # Authentication context to manage user login state
│   ├── /hooks                 # Custom hooks
│   │   ├── useForm.js         # Custom hook to handle form data and validation
│   │   └── useArticles.js     # Custom hook for fetching articles from API
│   ├── /pages                 # Page components that represent routes/screens
│   │   ├── HomePage.js        # Home page displaying articles
│   │   ├── SubmitArticle.js   # Page for article submission form
│   │   └── AdminDashboard.js  # Admin page for managing users and articles
│   ├── /services              # API service functions to interact with the backend
│   │   ├── articleService.js  # Functions to handle article-related API calls
│   │   ├── authService.js     # Functions for user authentication (login, register)
│   │   └── notificationService.js # Functions to handle email/notification APIs (if applicable)
│   ├── /styles                # Tailwind CSS and custom styles
│   │   ├── tailwind.config.js # Tailwind CSS config
│   │   ├── index.css          # Global CSS imports
│   ├── /utils                 # Utility functions like validation helpers, etc.
│   │   ├── validation.js      # Functions for form validation
│   ├── App.js                 # Main application component
│   ├── index.js               # Entry point for React app
│   └── routes.js              # Defines the routes for the application




.
├── eslint.config.js
├── index.html
├── package.json
├── package-lock.json
├── postcss.config.js
├── public
│   └── vite.svg
├── README.md
├── src
│   ├── App.jsx
│   ├── assets
│   │   └── react.svg
│   ├── components
│   │   ├── Article
│   │   │   ├── ArticleCard.jsx
│   │   │   └── ArticleList.jsx
│   │   ├── Auth
│   │   │   ├── Login.jsx
│   │   │   └── Register.jsx
│   │   ├── Form
│   │   │   ├── ArticleForm.jsx
│   │   │   ├── Page1.jsx
│   │   │   └── Page2.jsx
│   │   └── Navbar.jsx
│   ├── context
│   │   └── AuthContext.jsx
│   ├── hooks
│   │   ├── useArticles.jsx
│   │   └── useForm.jsx
│   ├── index.css
│   ├── main.jsx
│   ├── pages
│   │   ├── AdminDashboard.jsx
│   │   ├── HomePage.jsx
│   │   └── SubmitArticle.jsx
│   ├── routes.jsx
│   ├── services
│   │   ├── articleService.jsx
│   │   ├── authService.jsx
│   │   └── notificationService.jsx
│   └── utils
│       └── validation.jsx
├── tailwind.config.js
└── vite.config.js

13 directories, 32 files