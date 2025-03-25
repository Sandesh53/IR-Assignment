import { useState, useCallback } from 'react';
import './App.css';
import logo from './logo.png';

function SearchBar({ onSearch, placeholder }) {
  const [query, setQuery] = useState('');

  const handleSearch = useCallback((e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query);
    }
  }, [onSearch, query]);

  return (
    <form onSubmit={handleSearch} className="search-bar">
      <input
        type="text"
        placeholder={placeholder}
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="search-input"
      />
      <button type="submit" className="search-button">Search</button>
    </form>
  );
}

function ItemList({ items, hasSearched }) {
  return (
    <div className="results-container">
      {hasSearched && items.length === 0 ? (
        <div className="no-results">No result found</div>
      ) : (
        <ul className="item-list">
          {items.map((item, index) => (
            <li key={index} className="item">
              <a href={item.url} target="_blank" rel="noopener noreferrer" className="result-title">
                {item.title}
              </a>
              <p className="result-url">{item?.url}</p>
              <p className="result-description">{item?.description}</p>
              <div className="result-meta">
                <span><strong> Journal: </strong> {item?.journal}</span>
                <span><strong> Year: </strong> {item?.year}</span>
                <span><strong> Authors: </strong> {item?.authors}</span>
              </div>
              <span className="result-score">Score: {item.score.toFixed(2)}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

function Pagination({ currentPage, totalPages, onPageChange }) {
  const pageNumbers = [];

  for (let i = 1; i <= totalPages; i++) {
    pageNumbers.push(i);
  }

  return (
    <div className="pagination">
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        className="pagination-button"
        aria-label="Previous Page"
      >
        &laquo; Previous
      </button>

      <div className="page-numbers">
        {pageNumbers.map((number) => (
          <button
            aria-label={`Go to page ${number}`}
            key={number}
            onClick={() => onPageChange(number)}
            className={`page-number ${currentPage === number ? 'active' : ''}`}
          >
            {number}
          </button>
        ))}
      </div>

      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        className="pagination-button"
        aria-label="Next Page"
      >
        Next &raquo;
      </button>
    </div>
  );
}

function PublicationPage({ results, currentPage, totalPages, onPageChange, onSearch, isLoading }) {
  const resultsPerPage = 5;
  const displayedResults = results.slice(
    (currentPage - 1) * resultsPerPage,
    currentPage * resultsPerPage
  );

  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = useCallback((query) => {
    setHasSearched(true);
    onSearch(query);
  }, [onSearch]);

  return (
    <div className="page-container">
      <h1 className="page-title">Academic Publication Search</h1>
      <p className="page-description">
        Search academic publications by title or keywords of the Accounting, Economics and Finance.
      </p>

      <SearchBar onSearch={handleSearch} placeholder="Search Academic publications..." />

      {isLoading ? (
        <div className="loading-spinner">Loading...</div>
      ) : (
        <>
          <ItemList items={displayedResults} hasSearched={hasSearched} />
          {results.length > 0 && (
            <Pagination
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={onPageChange}
            />
          )}
        </>
      )}
    </div>
  );
}

function PredictionPage({ category, onPredict, isLoading }) {
  const [predictionMade, setPredictionMade] = useState(false);

  const handlePredict = useCallback((query) => {
    onPredict(query);
    setPredictionMade(true);
  }, [onPredict]);

  return (
    <div className="page-container prediction-page">
      <h1 className="page-title">Category Prediction</h1>
      <p className="page-description">
        Enter text to predict its category.
      </p>

      <SearchBar onSearch={handlePredict} placeholder="Enter text to predict category..." />

      {isLoading ? (
        <div className="loading-spinner">Processing...</div>
      ) : (
        predictionMade && (
          <div className="prediction-result-container">
            <h2 className="prediction-header">Prediction Results</h2>

            <div className="prediction-card">
              <div className="prediction-main">
                <div className="prediction-label">Category:</div>
                <div className="prediction-value">{category || 'No category detected'}</div>
              </div>

              <div className="prediction-metrics">
                <div className="metric">
                  <div className="metric-label">Accuracy</div>
                  <div className="metric-value">67.2%</div>
                </div>
                <div className="metric">
                  <div className="metric-label">F1 Score</div>
                  <div className="metric-value">0.661</div>
                </div>
              </div>
            </div>
          </div>
        )
      )}
    </div>
  );
}

function App() {
  const [results, setResults] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [category, setCategory] = useState('');
  const [activePage, setActivePage] = useState('publication');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null); // Add error state
  const resultsPerPage = 5;

  const fetchResults = useCallback(async (query) => {
    setIsLoading(true);
    setError(null); // Clear previous errors
    try {
      const response = await fetch('/cu_publication/_search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: { "multi_match": { query, "fields": ["title", "description", "journal", "authors"] } } }),
      });
      if (!response.ok) {
        throw new Error(`Failed to fetch search results. Status: ${response.status}`);
      }
      const data = await response.json();
      const searchResults = data.hits.hits.map((hit) => ({
        url: hit._source.publication_url || '#',
        title: hit._source.title || 'No Title',
        description: hit._source.abstract || 'No Description',
        score: hit._score,
        journal: hit._source.journal || 'Unknown Journal',
        year: hit._source.publication_year || 'Unknown Year',
        authors: hit._source.authors || ['Unknown Author'],
      }));
      setResults(searchResults);
      setCurrentPage(1);
    } catch (err) {
      setError(err.message); // Set error message
      console.error('Error fetching search results:', err);
      //  alert('An error occurred while fetching search results.'); // Removed alert
    } finally {
      setIsLoading(false);
    }
  }, []);

  const fetchCategory = useCallback(async (text) => {
    setIsLoading(true);
    setError(null);  // Clear previous error
    try {
      const response = await fetch('http://127.0.0.1:5000/predictions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });
      if (!response.ok) {
        throw new Error(`Failed to fetch category. Status: ${response.status}`);
      }
      const data = await response.json();
      setCategory(data?.prediction[0] || 'No Prediction');
    } catch (err) {
      setError(err.message);
      console.error('Error fetching category:', err);
      // alert('An error occurred while fetching category.'); //Removed alert
    } finally {
      setIsLoading(false);
    }
  }, []);

  const totalPages = Math.ceil(results.length / resultsPerPage);

  const handlePageChange = useCallback((page) => {
    setActivePage(page);
    setCurrentPage(1);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <div className="app-top">
          <img src={logo} alt="Logo" className="app-logo" />
        </div>

        <nav className="main-navigation">
          <button
            className={`nav-button ${activePage === 'publication' ? 'active' : ''}`}
            onClick={() => handlePageChange('publication')}
            aria-label="Go to Publications Page"
          >
            Publications
          </button>
          <button
            className={`nav-button ${activePage === 'prediction' ? 'active' : ''}`}
            onClick={() => handlePageChange('prediction')}
            aria-label="Go to Predictions Page"
          >
            Predictions
          </button>
        </nav>

        <main className="main-content">
          {error && <div className="error-message">{error}</div>} {/* Display error */}
          {activePage === 'publication' ? (
            <PublicationPage
              results={results}
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={setCurrentPage}
              onSearch={fetchResults}
              isLoading={isLoading}
            />
          ) : (
            <PredictionPage
              category={category}
              onPredict={fetchCategory}
              isLoading={isLoading}
            />
          )}
        </main>
      </header>
    </div>
  );
}

export default App;
