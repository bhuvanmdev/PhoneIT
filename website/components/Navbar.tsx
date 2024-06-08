import Link from "next/link"

const Navbar = () => {
    return (
      <nav className="flex justify-between p-4 absolute w-full">
        <div><Link href={'/'}>Home</Link></div>
        <div>
            <ul className="flex gap-4">
                <li><Link href={'/business'}>Business</Link></li>
                <li><Link href={'/analytics'}>Analytics</Link></li>
            </ul>
        </div>
      </nav>
    )
  }
  
export default Navbar