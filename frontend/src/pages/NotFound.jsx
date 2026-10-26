import { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { EmptyState } from '../components/Skeleton.jsx';
import { setPageTitle } from '../lib/site.js';
export default function NotFound() {
  useEffect(() => { setPageTitle('Page not found'); }, []);
  return <div className="px-4 py-20"><EmptyState title="Page not found" hint="Check the address and try again." action={<Link to="/" className="btn-primary">Go home</Link>} /></div>;
}
