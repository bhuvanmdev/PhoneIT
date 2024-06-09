// const page = () => {
//   return (
//     <div className="flex min-h-screen flex-col gap-4 p-24">Analytics page</div>
//   )
// }

// export default page

// const page = () => {
//   return (
//     <div className="flex min-h-screen flex-col gap-4 p-24">
//       <h1>Analytics page</h1>
//       <img src="/Num_calls_map.jpeg" alt="Num Calls Map" />
//       <img src="/Num_calls.jpeg" alt="Num Calls" />
//       <img src="/Num_conv.jpeg" alt="Num Conversions" />
//     </div>
//   );
// }

// export default page;

// import Image from 'next/image';

// const page = () => {
//   return (
//     <div className="flex min-h-screen flex-col gap-4 p-24">
//       <h1 className="text-2xl font-bold">Analytics Page</h1>

//       <div className="flex flex-col items-center gap-2">
//         <h2 className="text-xl">Number of Calls Map</h2>
//         <p>This graph shows the distribution of call numbers across different regions.</p>
//         <Image src="/Num_calls_map.jpeg" alt="Number of Calls Map" width={800} height={400} />
//       </div>

//       <div className="flex flex-col items-center gap-2">
//         <h2 className="text-xl">Number of Calls Over Time</h2>
//         <p>This graph represents the number of calls made over a specified time period.</p>
//         <Image src="/Num_calls.jpeg" alt="Number of Calls" width={800} height={400} />
//       </div>

//       <div className="flex flex-col items-center gap-2">
//         <h2 className="text-xl">Number of Conversions</h2>
//         <p>This graph displays the number of conversions achieved from the calls.</p>
//         <Image src="/Num_conv.jpeg" alt="Number of Conversions" width={800} height={400} />
//       </div>
//     </div>
//   );
// }

// export default page;

import Image from 'next/image';

const page = () => {
  return (
    <>
    <div className=" min-h-screen  p-8">
    <h1 className="text-3xl font-bold text-center w-[100%] my-6">Analytics Page</h1>
      <div className='flex flex-col-3 items-center justify-center gap-8'>
        <div className="flex flex-col items-center text-center">
          <h2 className="text-xl mb-2">Number of Calls Over Time</h2>
          <p className="mb-4">This graph represents the number of calls made over a specified time period.</p>
          <Image
            src="/Num_calls.jpeg"
            alt="Number of Calls"
            width={800}
            height={400}
            className="rounded-lg"
            style={{ maxWidth: '100%', height: 'auto' }}
          />
        </div>

      <div className="flex flex-col items-center text-center">
        <h2 className="text-xl mb-2">Number of Calls Map</h2>
        <p className="mb-4">This graph shows the distribution of call numbers across different regions.</p>
        <Image
          src="/Num_calls_map.jpeg"
          alt="Number of Calls Map"
          width={800}
          height={400}
          className="rounded-lg"
          style={{ maxWidth: '100%', height: 'auto' }}
        />
      </div>

      <div className="flex flex-col items-center text-center">
        <h2 className="text-xl mb-2">Number of Conversions</h2>
        <p className="mb-4">This graph displays the number of conversions achieved from the calls.</p>
        <Image
          src="/Num_conv.jpeg"
          alt="Number of Conversions"
          width={800}
          height={400}
          className="rounded-lg"
          style={{ maxWidth: '100%', height: 'auto' }}
        />
      </div>
      </div>

      </div>
    </>
  );
}

export default page;
