import Link from "next/link"
import { Home } from 'lucide-react';

const Navbar = () => {
    return (
      <nav className="flex justify-between p-4 absolute w-full">
        <div ><Link href={'/'} className="flex gap-1 justify-center items-center"><Home size={16}/>Home</Link></div>
        <div>
            <ul className="flex gap-4">
                <li><Link href={'/analytics'}>Analytics</Link></li>
                <li><Link href={'/business'}>Business</Link></li>
            </ul>
        </div>
      </nav>
    )
  }
  
export default Navbar